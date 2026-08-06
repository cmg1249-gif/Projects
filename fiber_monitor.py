#!/usr/bin/env python3
"""
fiber_monitor.py — three-target connection monitor for catching
intermittent drops and latency trouble (bufferbloat) in the act.

Pings three points on every cycle, so when an outage hits, the log
shows WHERE the failure happened:

    ROUTER    192.168.0.1      your side (should stay up during a fiber event)
    ISP_EDGE  216.196.65.254   first hop inside the ISP's network
    INTERNET  8.8.8.8          the wider internet

How to read an event:
    ROUTER up, ISP_EDGE down        -> failure between your ONT and their edge
                                       (drop fiber / splitter / OLT territory)
    all three down, router included -> local problem (router or this PC)
    ISP_EDGE up, INTERNET down      -> upstream of the ISP edge (core/transit)

When a DOWN event fires, a LINK line records this machine's adapter
link states at that moment, splitting the "local problem" case:
    LINK ... connected    -> cable/Wi-Fi association was fine, so the
                             router itself stopped answering
    LINK ... disconnected -> this machine's link dropped (cable, port,
                             adapter, or Wi-Fi disassociation)

Latency: every minute a STATS line records each target's round-trip
times over that window as min/avg/max, jitter (average change between
consecutive replies), and lost pings, plus whether the game was running:

    STATS | ROUTER 1/2/9ms jitter 1ms loss 0/28 | ... | game=on

How to read a laggy gaming session:
    ROUTER avg/jitter climb while game=on -> the router or your upload is
                                             saturating (bufferbloat); the
                                             problem is inside the house
    ROUTER stays ~1-2ms, ISP_EDGE climbs  -> the router is innocent; the
                                             congestion is on the line/ISP

GAME lines mark when Arc Raiders (PioneerGame.exe) starts and stops,
so lag windows line up with play sessions without guesswork.

ROUTE lines show which adapter is actually carrying traffic (the OS
decides this, not the script — pings just follow the routing table).
Logged at startup and whenever it changes, and stamped on every STATS
line as via=<adapter>. Gotcha this exists to catch: Wi-Fi being ON
does not mean Wi-Fi is being USED — with the cable still plugged in,
traffic usually keeps riding Ethernet. If you think you're testing
Wi-Fi but the log says via=Ethernet, unplug the cable.

The log stays otherwise quiet: state changes (DOWN, then UP with the
outage duration), latency spikes over SPIKE_MS (rate-limited to one
per target per SPIKE_COOLDOWN_SECONDS so a bad session doesn't flood
the file), and an hourly heartbeat that proves the monitor was alive
between events.

Run it and leave it running:
    python fiber_monitor.py

Stop with Ctrl+C — it prints a summary of every event it caught.

Windows note: set your power plan so the PC never sleeps, or the log
stops when the machine does. Turning the display off is fine.
"""

import os
import platform
import re
import socket
import subprocess
import time
from datetime import datetime

# --- configuration ------------------------------------------------------

TARGETS = [
    ("ROUTER", "192.168.0.1"),
    ("ISP_EDGE", "216.196.65.254"),
    ("INTERNET", "8.8.8.8"),
]

CYCLE_SECONDS = 2            # pause between full ping cycles
TIMEOUT_MS = 1000            # how long to wait for each reply
FAILS_TO_DOWN = 2            # consecutive misses before declaring DOWN
OKS_TO_UP = 2                # consecutive replies before declaring UP again
SPIKE_MS = 150               # replies slower than this get logged as spikes
SPIKE_COOLDOWN_SECONDS = 30  # at most one SPIKE line per target per window
STATS_SECONDS = 60           # latency summary (STATS line) interval
HEARTBEAT_SECONDS = 3600     # hourly "still alive" line
GAME_PROCESS = "PioneerGame.exe"  # Arc Raiders' actual process name
GAME_LABEL = "Arc Raiders"
GAME_CHECK_SECONDS = 15      # how often to look for the game process
ROUTE_CHECK_SECONDS = 15     # how often to check which adapter has the route
LOG_FILE = "fiber_monitor.log"

# ------------------------------------------------------------------------

IS_WINDOWS = platform.system() == "Windows"

# Matches "time=23ms", "time<1ms", and Linux's "time=22.9 ms"
RTT_PATTERN = re.compile(r"time[=<]\s*([\d.]+)\s*ms", re.IGNORECASE)


def log(message):
    """Print a timestamped line and append it to the log file."""
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"{stamp} | {message}"
    print(entry, flush=True)
    with open(LOG_FILE, "a", encoding="utf-8") as handle:
        handle.write(entry + "\n")


def ping_once(address):
    """
    Send one ping. Returns (reply_received, rtt_ms_or_None).

    Uses the system ping command so no admin rights or extra
    packages are needed on either Windows or Linux.
    """
    if IS_WINDOWS:
        command = ["ping", "-n", "1", "-w", str(TIMEOUT_MS), address]
    else:
        timeout_seconds = max(1, TIMEOUT_MS // 1000)
        command = ["ping", "-c", "1", "-W", str(timeout_seconds), address]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=(TIMEOUT_MS / 1000) + 2,
        )
    except subprocess.TimeoutExpired:
        return False, None
    except OSError:
        return False, None

    output = result.stdout or ""

    if IS_WINDOWS:
        # Windows ping can exit 0 on "Destination host unreachable",
        # because a reply DID arrive — just from the wrong machine.
        # A genuine echo reply always includes a TTL value, so
        # require that before counting it as a success.
        reply_received = result.returncode == 0 and "ttl=" in output.lower()
    else:
        reply_received = result.returncode == 0

    rtt = None
    if reply_received:
        match = RTT_PATTERN.search(output)
        if match:
            rtt = float(match.group(1))

    return reply_received, rtt


def get_link_states():
    """
    Return a one-line summary of this machine's adapter link states,
    e.g. "Ethernet: connected, Wi-Fi: disconnected".

    Captured when a DOWN event fires: if the local link was still
    connected while the router stopped answering, the fault is the
    router's, not this machine's cable or adapter.
    """
    try:
        if IS_WINDOWS:
            result = subprocess.run(
                ["netsh", "interface", "show", "interface"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            adapters = []
            for line in result.stdout.splitlines():
                parts = line.split()
                # Data rows start with the admin state; this skips the
                # header and separator lines.
                if len(parts) >= 4 and parts[0] in ("Enabled", "Disabled"):
                    name = " ".join(parts[3:])
                    adapters.append(f"{name}: {parts[1].lower()}")
        else:
            adapters = []
            for name in sorted(os.listdir("/sys/class/net")):
                if name == "lo":
                    continue
                try:
                    with open(f"/sys/class/net/{name}/operstate") as handle:
                        adapters.append(f"{name}: {handle.read().strip()}")
                except OSError:
                    pass
        return ", ".join(adapters) if adapters else "no adapters found"
    except Exception:
        return "unavailable"


def is_game_running():
    """
    Return True when the game process is present. Never raises —
    if the check itself fails, the game is just reported as absent.
    """
    try:
        if IS_WINDOWS:
            result = subprocess.run(
                ["tasklist", "/FI", f"IMAGENAME eq {GAME_PROCESS}", "/NH"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            return GAME_PROCESS.lower() in (result.stdout or "").lower()
        result = subprocess.run(
            ["pgrep", "-f", os.path.splitext(GAME_PROCESS)[0]],
            capture_output=True,
            text=True,
            timeout=5,
        )
        return result.returncode == 0
    except Exception:
        return False


def get_local_ip():
    """
    The local IP the OS would use to reach the internet right now.

    Opening a UDP socket toward 8.8.8.8 sends NO packets — connect()
    on UDP just consults the routing table — but getsockname() then
    reveals which local address (and so which adapter) won the route.
    """
    try:
        probe = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            probe.connect(("8.8.8.8", 53))
            return probe.getsockname()[0]
        finally:
            probe.close()
    except OSError:
        return None


def get_active_interface():
    """
    Return (adapter_name, local_ip) for whichever adapter currently
    carries internet traffic, e.g. ("Wi-Fi", "192.168.0.42").
    Falls back to ("unknown", ...) rather than raising.
    """
    ip = get_local_ip()
    if ip is None:
        return "unknown", "no route"
    try:
        if IS_WINDOWS:
            # ipconfig groups addresses under headers like
            # "Wireless LAN adapter Wi-Fi:" — find the block that
            # holds our IP and report that adapter's name.
            result = subprocess.run(
                ["ipconfig"], capture_output=True, text=True, timeout=5
            )
            adapter = None
            for line in (result.stdout or "").splitlines():
                if line and not line[0].isspace() and line.rstrip().endswith(":"):
                    header = line.rstrip().rstrip(":")
                    for prefix in (
                        "Ethernet adapter ",
                        "Wireless LAN adapter ",
                        "PPP adapter ",
                    ):
                        if header.startswith(prefix):
                            header = header[len(prefix):]
                            break
                    adapter = header
                    continue
                stripped = line.strip()
                if "IPv4" in stripped and ":" in stripped:
                    value = stripped.split(":")[-1].strip()
                    value = value.split("(")[0].strip()  # drop "(Preferred)"
                    if value == ip:
                        return (adapter or "unknown"), ip
            return "unknown", ip
        result = subprocess.run(
            ["ip", "route", "get", "8.8.8.8"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        match = re.search(r"\bdev\s+(\S+)", result.stdout or "")
        return (match.group(1) if match else "unknown"), ip
    except Exception:
        return "unknown", ip


def build_initial_states():
    """One state record per target. Everything starts as 'up'."""
    states = {}
    for name, _address in TARGETS:
        states[name] = {
            "up": True,
            "fail_streak": 0,
            "ok_streak": 0,
            "first_fail_time": None,
            "down_since": None,
            "event_count": 0,
            "last_spike_time": 0.0,
        }
    return states


def new_stats_window():
    """Fresh per-target sample buckets for the next STATS interval."""
    window = {}
    for name, _address in TARGETS:
        window[name] = {"rtts": [], "sent": 0, "lost": 0}
    return window


def format_stats(window, game_running, active_iface):
    """Build the once-a-minute STATS line from a window of samples."""
    parts = []
    for name, _address in TARGETS:
        data = window[name]
        rtts = data["rtts"]
        if rtts:
            avg = sum(rtts) / len(rtts)
            diffs = [abs(b - a) for a, b in zip(rtts, rtts[1:])]
            jitter = sum(diffs) / len(diffs) if diffs else 0.0
            parts.append(
                f"{name} {min(rtts):.0f}/{avg:.0f}/{max(rtts):.0f}ms "
                f"jitter {jitter:.0f}ms loss {data['lost']}/{data['sent']}"
            )
        else:
            parts.append(f"{name} no replies ({data['lost']}/{data['sent']} lost)")
    game = "on" if game_running else "off"
    return "STATS | " + " | ".join(parts) + f" | game={game} via={active_iface}"


def handle_success(name, address, state, rtt):
    state["fail_streak"] = 0
    state["ok_streak"] += 1

    if not state["up"] and state["ok_streak"] >= OKS_TO_UP:
        state["up"] = True
        outage_seconds = int(time.time() - state["down_since"])
        log(f"EVENT | {name} ({address}) UP again after {outage_seconds}s down")
        state["down_since"] = None

    if rtt is not None and rtt >= SPIKE_MS:
        now = time.time()
        if now - state["last_spike_time"] >= SPIKE_COOLDOWN_SECONDS:
            log(f"SPIKE | {name} ({address}) reply took {int(rtt)}ms")
            state["last_spike_time"] = now


def handle_failure(name, address, state):
    """Returns True when this failure crossed the threshold into a DOWN event."""
    state["ok_streak"] = 0
    state["fail_streak"] += 1

    if state["fail_streak"] == 1:
        # Remember when trouble started, in case this becomes an event.
        state["first_fail_time"] = time.time()

    if state["up"] and state["fail_streak"] >= FAILS_TO_DOWN:
        state["up"] = False
        state["down_since"] = state["first_fail_time"]
        state["event_count"] += 1
        log(f"EVENT | {name} ({address}) DOWN")
        return True
    return False


def heartbeat(states, cycle_count):
    parts = []
    for name, _address in TARGETS:
        status = "ok" if states[name]["up"] else "DOWN"
        parts.append(f"{name} {status}")
    summary = ", ".join(parts)
    total_events = sum(s["event_count"] for s in states.values())
    log(f"HEARTBEAT | {summary} | cycles={cycle_count} events_so_far={total_events}")


def final_summary(states):
    log("MONITOR | stopped by user")
    for name, address in TARGETS:
        count = states[name]["event_count"]
        log(f"SUMMARY | {name} ({address}): {count} outage event(s) recorded")


def main():
    target_list = ", ".join(f"{name}={address}" for name, address in TARGETS)
    log(f"MONITOR | started on {platform.system()} | watching: {target_list}")
    log(
        f"MONITOR | cycle={CYCLE_SECONDS}s timeout={TIMEOUT_MS}ms "
        f"down_after={FAILS_TO_DOWN} misses, spike_threshold={SPIKE_MS}ms, "
        f"stats_every={STATS_SECONDS}s, game_process={GAME_PROCESS}"
    )

    states = build_initial_states()
    stats_window = new_stats_window()
    game_running = is_game_running()
    if game_running:
        log(f"GAME | {GAME_LABEL} already running ({GAME_PROCESS})")
    active_iface, active_ip = get_active_interface()
    log(f"ROUTE | traffic via {active_iface} ({active_ip})")
    last_heartbeat = time.time()
    last_stats = time.time()
    last_game_check = time.time()
    last_route_check = time.time()
    cycle_count = 0

    try:
        while True:
            any_new_down = False
            for name, address in TARGETS:
                reply_received, rtt = ping_once(address)
                bucket = stats_window[name]
                bucket["sent"] += 1
                if reply_received:
                    if rtt is not None:
                        bucket["rtts"].append(rtt)
                    handle_success(name, address, states[name], rtt)
                else:
                    bucket["lost"] += 1
                    if handle_failure(name, address, states[name]):
                        any_new_down = True

            # One LINK line per burst, even if several targets went
            # down in the same cycle.
            if any_new_down:
                log(f"LINK | local adapters: {get_link_states()}")

            cycle_count += 1
            now = time.time()

            if now - last_game_check >= GAME_CHECK_SECONDS:
                running_now = is_game_running()
                if running_now != game_running:
                    game_running = running_now
                    verb = "started" if running_now else "stopped"
                    log(f"GAME | {GAME_LABEL} {verb} ({GAME_PROCESS})")
                last_game_check = now

            if now - last_route_check >= ROUTE_CHECK_SECONDS:
                iface_now, ip_now = get_active_interface()
                # Ignore "unknown" (mid-outage there may be no route at
                # all); DOWN events already tell that story.
                if iface_now != "unknown" and (
                    iface_now != active_iface or ip_now != active_ip
                ):
                    log(f"ROUTE | traffic now via {iface_now} ({ip_now})")
                    active_iface, active_ip = iface_now, ip_now
                last_route_check = now

            if now - last_stats >= STATS_SECONDS:
                log(format_stats(stats_window, game_running, active_iface))
                stats_window = new_stats_window()
                last_stats = now

            if now - last_heartbeat >= HEARTBEAT_SECONDS:
                heartbeat(states, cycle_count)
                last_heartbeat = now

            time.sleep(CYCLE_SECONDS)
    except KeyboardInterrupt:
        final_summary(states)


if __name__ == "__main__":
    main()

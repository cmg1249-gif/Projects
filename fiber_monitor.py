#!/usr/bin/env python3
"""
fiber_monitor.py — three-target connection monitor for catching
intermittent drops in the act.

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

The log stays quiet on purpose: it records state changes (DOWN, then UP
with the outage duration), latency spikes, and an hourly heartbeat that
proves the monitor was alive between events.

Run it and leave it running:
    python fiber_monitor.py

Stop with Ctrl+C — it prints a summary of every event it caught.

Windows note: set your power plan so the PC never sleeps, or the log
stops when the machine does. Turning the display off is fine.
"""

import platform
import re
import subprocess
import time
from datetime import datetime

# --- configuration ------------------------------------------------------

TARGETS = [
    ("ROUTER", "192.168.0.1"),
    ("ISP_EDGE", "216.196.65.254"),
    ("INTERNET", "8.8.8.8"),
]

CYCLE_SECONDS = 2          # pause between full ping cycles
TIMEOUT_MS = 1000          # how long to wait for each reply
FAILS_TO_DOWN = 2          # consecutive misses before declaring DOWN
OKS_TO_UP = 2              # consecutive replies before declaring UP again
SPIKE_MS = 500             # replies slower than this get logged as spikes
HEARTBEAT_SECONDS = 3600   # hourly "still alive" line
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
        }
    return states


def handle_success(name, address, state, rtt):
    state["fail_streak"] = 0
    state["ok_streak"] += 1

    if not state["up"] and state["ok_streak"] >= OKS_TO_UP:
        state["up"] = True
        outage_seconds = int(time.time() - state["down_since"])
        log(f"EVENT | {name} ({address}) UP again after {outage_seconds}s down")
        state["down_since"] = None

    if rtt is not None and rtt >= SPIKE_MS:
        log(f"SPIKE | {name} ({address}) reply took {int(rtt)}ms")


def handle_failure(name, address, state):
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
        f"down_after={FAILS_TO_DOWN} misses, spike_threshold={SPIKE_MS}ms"
    )

    states = build_initial_states()
    last_heartbeat = time.time()
    cycle_count = 0

    try:
        while True:
            for name, address in TARGETS:
                reply_received, rtt = ping_once(address)
                if reply_received:
                    handle_success(name, address, states[name], rtt)
                else:
                    handle_failure(name, address, states[name])

            cycle_count += 1

            if time.time() - last_heartbeat >= HEARTBEAT_SECONDS:
                heartbeat(states, cycle_count)
                last_heartbeat = time.time()

            time.sleep(CYCLE_SECONDS)
    except KeyboardInterrupt:
        final_summary(states)


if __name__ == "__main__":
    main()

import subprocess
from datetime import datetime

def run(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr

code, out, err = run(["pacman", "-Syu", "--noconfirm"])

with open("/var/log/auto_update.log", "a") as f:
        f.write(f"\n[{datetime.now()}]\n")
        if code == 0:
            f.write("Update successful:\n" + out)
        else:
            f.write ("Update Failed:\n" + err)

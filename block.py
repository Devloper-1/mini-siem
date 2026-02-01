# block.py
import subprocess
import json
from pathlib import Path
from datetime import datetime
from events import log_event


DATA_DIR =  Path("data")
BLOCKED_FILE = DATA_DIR /"blocked_ips.json"



def load_blocked():
    # if blocked_ips is not created 
    DATA_DIR.mkdir(exist_ok=True)
    
    if not  BLOCKED_FILE.exists():
        BLOCKED_FILE.write_text("[]")
        return []
     
    raw = BLOCKED_FILE.read_text().strip()

    # 🛡️ DEFENSE: empty file
    if not raw:
        return {}

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # 🛡️ DEFENSE: corrupted file
        print("[WARN] Blocked.json corrupted, resetting")
        return {}

def save_blocked(blocked):
    BLOCKED_FILE.write_text(json.dumps(blocked , indent=2))


def is_already_blocked(ip,blocked):
    for entry in blocked:
        if entry["ip"] == ip:
            return True
    return False


def block_ip(ip, failed_count):
    blocked = load_blocked()

    if is_already_blocked(ip, blocked):
        print(f"[BLOCK] {ip} already blocked")
        return

    subprocess.run(
        ["sudo", "ufw", "deny", "from", ip, "to", "any"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    block_data = {
        "ip": ip,
        "timestamp": datetime.now().isoformat(),
        "failed_attempts": failed_count,
        "reason": "BRUTE_FORCE"
    }

    blocked.append(block_data)
    save_blocked(blocked)

    print(f"[BLOCK] {ip} blocked")
    log_event(ip, failed_count, "IP_BLOCKED")

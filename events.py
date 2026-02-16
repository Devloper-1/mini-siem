# events.py
import json
from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR/"data"
EVENTS_FILE = DATA_DIR/"events.json"



def load_events():
    "if events.json does not exits "
    DATA_DIR.mkdir(exist_ok=True)

    """Load existing events from events.json"""
    if not EVENTS_FILE.exists():
       EVENTS_FILE.write_text("{}")
       return {}  # return empty list if file doesn't exist
   
    raw = EVENTS_FILE.read_text().strip()

    # 🛡️ DEFENSE: empty file
    if not raw:
        return {}

    try:
        data = json.loads(raw)

        # 🛡️ DEFENSE: old format (list) → reset
        if isinstance(data, list):
            print("[WARN] events.json old format (list), migrating to dict")
            return {}

        return data
    except json.JSONDecodeError:
        # 🛡️ DEFENSE: corrupted file
        print("[WARN] events.json corrupted, resetting")
        return {}

def save_events(events):
    """Save events dict to events.json"""
    DATA_DIR.mkdir(exist_ok=True)
    EVENTS_FILE.write_text(json.dumps(events, indent=2))


def log_event(info, blocked=False):


    events = load_events()
    now = datetime.now().isoformat()

    ip = info["ip"]
    service = info.get("service", "unknown")
    user = info.get("user", "unknown")
    event_type = info["event"]

    # 1️⃣ Create profile if new IP
    if ip not in events:
        events[ip] = {
            "ip": ip,
            "service": service,
            "failed_count": 0,
            "success_count": 0,
            "unique_users": [],
            "first_seen": now,
            "last_seen": now,
            "blocked": False
        }

    # 2️⃣ Update counters
    if event_type == "FAILED_LOGIN":
        events[ip]["failed_count"] += 1

    elif event_type == "LOGIN_SUCCESS":
        events[ip]["success_count"] += 1

    # 3️⃣ Track unique users
    if user not in events[ip]["unique_users"]:
        events[ip]["unique_users"].append(user)

    # 4️⃣ Update timestamps
    events[ip]["last_seen"] = now

    # 5️⃣ Update blocked state
    if blocked:
        events[ip]["blocked"] = True

    save_events(events)

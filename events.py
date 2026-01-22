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
       EVENTS_FILE.write_text("[]")
       return []  # return empty list if file doesn't exist
    return json.loads(EVENTS_FILE.read_text())  # store & return

def save_events(events):
    """if events.json does not exits """
    DATA_DIR.mkdir(exist_ok=True)

    """Save events list to events.json"""
    EVENTS_FILE.write_text(json.dumps(events, indent=2))

def log_event(ip, count, event_type):
    """Add a new event to events.json"""
    events = load_events()

    event_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ip": ip,
        "count": count,
        "event": event_type
    }

    events.append(event_data)
    save_events(events)

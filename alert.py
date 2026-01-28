# alert.py
from datetime import datetime
import json
from pathlib import Path

LOG_DIR = Path("logs")
LOGFILE  = LOG_DIR/"system.log"

def log_alert(info):

     # Ensure logs directory exists
    LOG_DIR.mkdir(exist_ok=True)


    alert = {
        "TimeStamp" : datetime.now().isoformat(),
        "Alert!": info
    }
    with open(LOGFILE , "a") as f :
        f.write(json.dumps(alert)+"\n")

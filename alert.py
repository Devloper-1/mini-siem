from datetime import datetime
import json

LOGFILE  = "logs/system.log"

def log_alert(info):

    alert = {
        "TimeStamp" : datetime.now().isoformat(),
        "Alert!": info
    }
    with open(LOGFILE , "a") as f :
        f.write(json.dumps(alert)+"\n")

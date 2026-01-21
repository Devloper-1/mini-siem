from datetime import datetime
import json

LOGFILE  = "logs/system.log"

def log_alert(info):
    with open(LOGFILE , "a") as f :
        f.write(f"{datetime.now()} - ALERT : {info}\n")

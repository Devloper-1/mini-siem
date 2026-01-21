import subprocess
import json
from pathlib import Path
from datetime import datetime
from events import load_events


DATA_DIR =  Path("data")
BLOCKED_FILE = DATA_DIR /"blocked_ips.json"



def load_blocked():
    # if blocked_ips is not created 
    DATA_DIR.mkdir(exist_ok=True)
    
    if BLOCKED_FILE.exists():
        BLOCKED_FILE.write_text("[]")
        return []
        
    return json.loads(BLOCKED_FILE.read_text())

def save_blocked(blocked):
    BLOCKED_FILE.write_text(json.dumps(blocked , indent=2))

def block_ip(ip , failed_count):
    
    # 1 load existen blocked ips 
    blocked = load_blocked()

     # 2 add new ip 
    if ip not in blocked :
        # code for block ip
        subprocess.run(["sudo","ufw","deny","from",ip,"to","any"] )
        # add in it 
        blocked.append(ip)
    else:
      print(f"{ip} already blocked")
    
    block_data = {
        "ip" : ip,
        "timestamp": datetime.now().strftime("%Y-%m-%d  %H.%m.%s"),
        "failed_attempt": failed_count,
        "resoan":"Brout-Force"
    }

    blocked.append(block_data)
    # save back to file 
    save_blocked(blocked)
    print(f"Blocked{ip}")

    load_events(ip,failed_count,"BlockedIP")


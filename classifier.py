# MINI-SIEM/classifier.py

from datetime import datetime

def classify_attack(event):
    attack_type = "UNKNOWN"
    severity = "LOW"

    fail_count = event.get("fail_count" , 0)
    success = event.get("success",False)
    unique_users = event.get("unique_users",1)

    
    # 1️⃣ Successful login after failures (highest priority)
    if success and fail_count >= 3:
     attack_type = "POSSIBLE_COMPROMISE"
     severity = "CRITICAL"

     # 2️⃣ Credential stuffing
    elif fail_count >= 5 and unique_users >= 3:
     attack_type = "CREDENTIAL_STUFFING"
     severity = "HIGH"

     # 3️⃣ SSH brute-force
    elif fail_count >= 5:
     attack_type = "SSH_BRUTE_FORCE"
     severity = "HIGH"

     # 4️⃣ Recon
    else:
     attack_type = "RECONNAISSANCE"
     severity = "LOW"

    return {
        "attack_type": attack_type,
        "severity": severity,
        "classified_at": datetime.now().isoformat()
    }

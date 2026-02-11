# MINI-SIEM/classifier.py

from datetime import datetime

def classify_attack(event):
    attack_type = "UNKNOWN"
    severity = "LOW"

    fail_count = event.get("fail_count" , 0)
    success = event.get("success",False)
    unique_users = event.get("unique_users",1)

    
    # 1️⃣ SSH brute-force
    if fail_count >= 5 and not success:
        attack_type = "SSH_BRUTE_FORCE"
        severity = "HIGH"

    # 2️⃣ Credential stuffing (same IP, many users)
    if fail_count >= 5 and unique_users >= 3:
        attack_type = "CREDENTIAL_STUFFING"
        severity = "HIGH"

    # 3️⃣ Successful login after failures (very dangerous)
    if success and fail_count >= 3:
        attack_type = "POSSIBLE_COMPROMISE"
        severity = "CRITICAL"

    # 4️⃣ Recon / probing
    if fail_count < 5 and not success:
        attack_type = "RECONNAISSANCE"
        severity = "LOW"

    return {
        "attack_type": attack_type,
        "severity": severity,
        "classified_at": datetime.now().isoformat()
    }

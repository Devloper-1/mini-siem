# main.py
from monitor_log import monitor_log
from parser import parser_log
from block import block_ip
from alert import log_alert
from  events import log_event
from detector import record_failed_attempt , is_attack , blocked_ips
from classifier import classify_attack


def main():
    try:
        for line in monitor_log():
            print("[LOG]", line)  # 👈 DEBUG

            info = parser_log(line)

            if not info:
              continue
            
             # ---- FAILED LOGIN ----
            if info["event"] == "FAILED_LOGIN":
               ip = info["ip"]
               user = info["user"]
               attempt_count = record_failed_attempt(ip)
               event = {
                    "ip": ip,
                    "user": user,
                    "event": "FAILED_LOGIN",
                    "fail_count": attempt_count,
                    "success": False,
                    "unique_users": 1  
                }
               
               # Classify attack
               classification = classify_attack(event)
               event.update(classification)

               # Log after every fail
               log_event(info, blocked=is_attack(ip))
                

               # check if this is an attack
               if is_attack(ip):
                   print("[attacker]: ",ip,"[Failed_attempot]: ",attempt_count)
     
                   block_ip(ip,attempt_count,event)
                   blocked_ips.add(ip)
                   log_alert(event)
               else:
                    print("[INFO]", ip, "attempts:", attempt_count)

              # ---- SUCCESSFUL LOGIN (CRITICAL) ----

            elif info["event"] == "LOGIN_SUCCESS":
               
              ip = info["ip"]
              user = info["user"]

              event = {
                    "ip": ip,
                    "user": user,
                    "event": "LOGIN_SUCCESS",   
                    "fail_count": 0,
                    "success": True,
                    "unique_users": 1
                }
              
              classification = classify_attack(event)
              event.update(classification)

              log_event(event, blocked=False)
              log_alert(event)

              print("🚨 CRITICAL: SSH LOGIN SUCCESS 🚨")
    
              
    except KeyboardInterrupt:
        print("\n[+] Mini-SIEM stopped")

if __name__ == "__main__":
    main()
    

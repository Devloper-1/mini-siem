# main.py
from monitor_log import monitor_log
from parser import parser_line
from block import block_ip
from alert import log_alert
from  events import log_event
from detector import record_failed_attempt , is_attack , blocked_ips


def main():
    try:
        for line in monitor_log():
            print("[LOG]", line)  # 👈 DEBUG

            info = parser_line(line)

            if  info.get("event") != "FAILED_SSH_LOGIN":
                continue
            ip = info["ip"]

            # Record failAttapem
            attempt_count = record_failed_attempt(ip)

            # Log after every fail
            log_event(
                ip,
                attempt_count,
                "Failed ssh login"
            )

            # check if this is an attack
            if is_attack(ip):
                print("[attacker]: ",ip,"[Failed_attempot]: ",attempt_count)

                block_ip(ip,attempt_count)
                blocked_ips.add(ip)
                log_alert({
                    "ip": ip,
                    "failed_attempt":attempt_count,
                    "attack_type": "BRUTE_FORCE",
                    "severity": "HIGH"
                })
            else:
              print("[INFO]", ip, "attempts:", attempt_count)

                
    except KeyboardInterrupt:
        print("\n[+] Mini-SIEM stopped")

if __name__ == "__main__":
    main()
    

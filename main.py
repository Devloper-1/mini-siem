from monitor_log import monitor_log
from parser import parser_line
from block import block_ip
from alert import log_alert
from  events import log_event



def main():
    try:
        for line in monitor_log():
            print("[LOG]", line)  # 👈 DEBUG

            info = parser_line(line)

            if "ip" in info and not info["attack"]:
                print("[INFO]", info)
                log_event(
                    info["ip"],
                    info.get("failed_count", 0),
                    "Failed SSH login"
                )

            if info.get("attack"):
                print("[ATTACK]", info)
                block_ip(info["ip"] , info["failed_count"])
                log_alert(info)

    except KeyboardInterrupt:
        print("\n[+] Mini-SIEM stopped")

if __name__ == "__main__":
    main()
    

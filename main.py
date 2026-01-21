from monitor_log import monitor_log
from parser import parser_line
from block import block_ip
from alert import log_alert
from  events import log_event



def main():
    for line in monitor_log() :
        info = parser_line(line)

        # If parser detected a failed login (but not attack yet)
        if "ip" in info and not info["attack"]:
            log_event(
                info["ip"],
                info["count"],
                "Failed ssh  login "
            )

        # If attack detected
        if info.get["attack"]:
            block_ip(info["ip"], info["count"])
            log_alert(info)
        
if __name__ == "__main__":
    main()

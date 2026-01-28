# monitor_log.py
import subprocess

LOGFILE = "/var/log/auth.log"
def monitor_log():
    with subprocess.Popen(["tail" , "-f" , LOGFILE], stdout=subprocess.PIPE , text=True) as p :
        for line in p.stdout:
            yield line.strip()

            
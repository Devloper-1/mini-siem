# detector.py
import time

TIME_WINDOW = 60 
FAIL_THRESHOLD = 5 

failed_attempts = {}

blocked_ips = set()

def record_failed_attempt(ip):
   """
    Records a failed attempt and returns count within time window
    """
   now = int(time.time())

   if ip  not in failed_attempts:
      failed_attempts[ip] = []

   failed_attempts[ip].append(now)


 #    for removing old ip if its pass time limite
   failed_attempts[ip]=[
      t for t in failed_attempts[ip]
      if now -t <= TIME_WINDOW
   ]
   return len(failed_attempts[ip])


def is_attack(ip):
    if ip in blocked_ips:
       return False
    """
    Returns True if IP crosses threshold
    """
    return len(failed_attempts.get(ip, [])) >= FAIL_THRESHOLD

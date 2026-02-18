# detector.py
import json
from datetime import datetime
import time


TIME_WINDOW = 60 
FAIL_THRESHOLD = 5 

failed_attempts = {}

blocked_ips = set()

total_failures = {}

unique_users = {}



def record_failed_attempt(ip,user):
   """
    Records a failed attempt and returns count within time window
    """
   now = int(time.time())

   if ip  not in failed_attempts:
      failed_attempts[ip] = []
   
   if ip not in total_failures:
      total_failures[ip] = 0

   if ip not in unique_users:
      unique_users[ip] = set()


   failed_attempts[ip].append(now)
   total_failures[ip] +=1
   unique_users[ip].add(user)


 #    for removing old ip if its pass time limite
   failed_attempts[ip]=[
      t for t in failed_attempts[ip]
      if now -t <= TIME_WINDOW
   ]
   return len(failed_attempts[ip])


def is_attack(ip):
    if ip in blocked_ips:
       return False
    print("DEBUG total_failures:", total_failures.get(ip))
    """
    Returns True if IP crosses threshold
    """
    return len(failed_attempts.get(ip, [])) >= FAIL_THRESHOLD

def record_sucess(ip , username , fail_count):

   event = {
      "ip": ip,
        "username": username,
        "time": datetime.now().isoformat(),
        "fail_attemp": fail_count
   }

   try:
      with open("success_log.json", "r") as f:
         data = json.load(f)

   except:
      data = []

   data.append(event)

   with open("success_log.json" , "w") as f:
      json.dump(data,f,indent=4)

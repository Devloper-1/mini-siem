# parser.py
# re 
import re 

# detect  the text "fail password"
failed_re = re.compile(r"Failed password",re.IGNORECASE)
success_re = re.compile(r"Accepted password", re.IGNORECASE)
# extract ip 
ip_re = re.compile(r"(\d+\.\d+\.\d+\.\d+)")
user_re = re.compile(r"for(invalide user)?(\w+)")



def parser_log(line):

    ip_match = ip_re.search(line)
    user_match = user_re.search(line)

    if not ip_match :
        return None
    
    ip = ip_match.group(1) if ip_match else None
    user = user_match.group(1) if user_match else "unknown"

    
    if "Failed password" in line :
       if "Failed password" in line:
        return {
            "event": "FAILED_LOGIN",
            "ip": ip_match.group(1),
            "user": user,
            "service": "ssh"
        }

    if "Accepted password" in line:
        return {
            "event": "LOGIN_SUCCESS",
            "ip": ip_match.group(1),
            "user": user,
            "service": "ssh"
        }
    
    return None 

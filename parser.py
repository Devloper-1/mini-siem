# parser.py
# re 
import re 

# detect  the text "fail password"
failed_re = re.compile(r"Failed password",re.IGNORECASE)
success_re = re.compile(r"Accepted password", re.IGNORECASE)
# extract ip 
ip_re = re.compile(r"(\d+\.\d+\.\d+\.\d+)")



def parser_log(line):

    ip_match = ip_re.search(line)
    ip = ip_match.group(1) if ip_match else None

    
    if "Failed password" in line :
        return {"event": "FAILED_LOGIN",
                "ip": ip ,
            "severity": "medium",
            "raw": line
        }
    
    if "Accepted password" in line :
        return {
            "event": "LOGIN_SUCCESS",
            "ip": ip,
            "severity": "critical",
            "raw": line
        }
    
    return None 

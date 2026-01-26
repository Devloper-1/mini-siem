# re 
import re 

# detect  the text "fail password"
failed_re = re.compile(r"Failed password",re.IGNORECASE)
# extract ip 
ip_re = re.compile(r"(\d+\.\d+\.\d+\.\d+)")



def parser_line(line):
    # extract ip if log failed 
    if failed_re.search(line) :
        return{}
    
    ip_match = ip_re.search(line)
    if not ip_match:
        return{}
    ip = ip_match.group(1)

    
    return {
        "ip": ip,
        "event": "FAILED_SSH_LOGIN"
    }

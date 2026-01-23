# re 
import re 

# detect  the text "fail password"
failed_re = re.compile(r"Failed password",re.IGNORECASE)
# extract ip 
ip_re = re.compile(r"(\d+\.\d+\.\d+\.\d+)")

#  cont attemp
failed_attemps = {}


def parser_line(line):

    if failed_re.search(line) :
        # if the log line show failed  log attemp
        ip_match = ip_re.search(line)
        if  not ip_match :
            return {"attack": False}
        
             
         # extract ip 
        ip= ip_match.group(1)
        # count failed login attemp 
        failed_attemps[ip] = failed_attemps.get(ip,0) + 1
        count = failed_attemps[ip]

         # retrun result main siem 
        return{
            "ip" : ip,
            "failed_count" : count,
            "attack": count >= 5
         }
     
    return {"attack": False , "failed_count":0} 

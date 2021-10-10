import urllib.request
import datetime

defaultRoute = "0.0.0.0"
blocklist = "https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts"
zoneHeader = """$TTL 1w    ; default TTL = 1w
           ; TODO: should be adjusted to frequency of list updates

@   IN  SOA localhost. root.localhost. (
            2019102401      ; serial yyyymmddvv
            1w              ; refresh (match default TTL)
            1w              ; retry (match default TTL)
            1w              ; expiry (match default TTL)
            1d              ; negative caching
        )
    IN  NS  localhost.      ;

; ***** START OF BLOCKLIST *****"""

file = open("/etc/bind/adsblocker.db","w")  
file.write(zoneHeader + "\n")
now = datetime.datetime.now()

totalDomains = 0

with urllib.request.urlopen(blocklist) as f:
    for bytes in f:
      
        line = bytes.decode("utf-8").strip()
        
        if (line.startswith(defaultRoute)):
          # ignore the ip address; extract the domain
          domain = line[8:]
          
          if domain == defaultRoute or "#" in domain:
            continue
          
          file.write(domain+" CNAME .\n")

          totalDomains = totalDomains + 1

file.close()

print("List updated successfully at",now.strftime("%Y-%m-%d %H:%M:%S"),", with total updated domains", totalDomains)

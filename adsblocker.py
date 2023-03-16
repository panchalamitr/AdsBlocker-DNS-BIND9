# Import the necessary modules
import urllib.request
import datetime

# Define the default route and the blocklist URL
defaultRoute = "0.0.0.0"
blocklist = "https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts"

# Define the zone header for the output file
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

# Open the output file for writing
file = open("/etc/bind/adsblocker.db","w")  

# Write the zone header to the output file
file.write(zoneHeader + "\n")

# Get the current date and time
now = datetime.datetime.now()

# Initialize the total number of updated domains to 0
totalDomains = 0

# Open the blocklist URL and iterate through each line
with urllib.request.urlopen(blocklist) as f:
    for bytes in f:
      
        # Decode the line from bytes to string and remove any leading/trailing white space
        line = bytes.decode("utf-8").strip()
        
        # If the line starts with the default route, extract the domain
        if (line.startswith(defaultRoute)):
          # Ignore the IP address and extract the domain
          domain = line[8:]
          
          # If the domain is the default route or contains a comment, skip it
          if domain == defaultRoute or "#" in domain:
            continue
          
          # Write the domain as a CNAME record to the output file
          file.write(domain+" CNAME .\n")

          # Increment the total number of updated domains
          totalDomains = totalDomains + 1

# Close the output file
file.close()

# Print a success message with the current date/time and the total number of updated domains
print("List updated successfully at",now.strftime("%Y-%m-%d %H:%M:%S"),", with total updated domains", totalDomains)


# coding: utf-8

# In[3]:

# Post Scanner in Python
# Sockets are used to handle the actual data channel such as converting
# a server's name to an address and formatting data to be sent across the network.

import socket
import subprocess
import sys
from datetime import datetime

# Clear the screen
subprocess.call('clear', shell=True)

# Ask for input
remoteServer = raw_input("Enter a remote host to scan: ")
remoteServerIP = socket.gethostbyname(remoteServer) # Translate a host name to IPv4 address Format

# Print a banner with information on which host we are about to scan
print "-" * 60
print "Please wait, scanning remote host", remoteServerIP
print "-" * 60

# Check what ttime the scan started
t1=datetime.now()
print t1

try:
    for port in range(1,1025):
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # Creates a stream socket
        result = sock.connect_ex((remoteServerIP, port))
        
        if result== 0:
            print "Port {}: \t Open".format(port)
        sock.close()
        
except KeyboardInterrupt:
    print "You pressed Ctrl+C"
    sys.exit()
    
except socket.gaierror:
    print "Hostname could not be resolved. Exiting"
    sys.exit()

except socket.socket.error:
    print "Couldn't connect to server"
    sys.exit()
    
# Checking the time again
t2 = datetime.now()
print t2

total = t2 - t1

print 'Scanning Completed in: ', total


# In[7]:

# Google Command Line Script with Python
# We need 3 modules to make a request to the Web search API
# urllib2 for loading the URL response
# urllib for making use of urlencode
# json for Google returning JSON output

import urllib2
import urllib
import json

url = "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&"
query = raw_input("What do you want to search for? >>")
query = urllib.urlencode({'q': query})
response = urllib2.urlopen(url+query).read()
data = json.loads(response)

results = data['responseData']['results']

print "-" * 60
print data
print "-" * 60

for result in results:
    title = result['title']
    url = result['url']
    print (title + '; ' + url)


# In[ ]:




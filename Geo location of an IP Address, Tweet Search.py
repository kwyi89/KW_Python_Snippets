
# coding: utf-8

# In[4]:

# Get the Geo Location of an IP address
import re
import sys
import urllib2
import BeautifulSoup

usage = "Run the script: ./geolocate.py IPAddress"

if len(sys.argv)!=2:
    print(usage)
    sys.exit(0)
    
if len(sys.argv) >1:
    ipaddr = sys.argv[1]
    
geody = "http://www.geody.com/geoip.php?ip=" + ipaddr
html_page = urllib2.urlopen(geody).read()
soup = BeautifulSoup.BeautifulSoup(html_page)

# Filter paragraph containing geolocation info
paragraph = soup('p')[3]

# Remove html tags using regex.
geo_txt = re.sub(r'<.*?>','',str(paragraph))
print geo_txt[32:].strip()


# In[5]:

# Tweet Search Using Python
import urllib2
import json

screen_name = "wordpress"

url = "http://api.twitter.com/1/statuses/user_timeline.json?screen_name=" + screen_name

data = json.load(urllib2.urlopen(url))

print len(data), "tweets"

for tweet in data:
    print tweet['text']


# In[ ]:




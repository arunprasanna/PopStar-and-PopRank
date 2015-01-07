import requests
import json
from lxml import html

domainlist = []
keywordlist = []

# we check each URL parsed from Dmoz on Alexa to get the keywords
# Alexa provides keywords on the related page.

limit=100 # too many requests will cuase us blacklisted by Alexa
i=0
with open('seeds.txt', 'r') as f:
    while i<limit:
        domain = f.readline()
        domainlist.append(domain.strip())
        i+=1

for domain in domainlist:
    englishkeywords = []
    keyworddict = dict()
    r = requests.get("http://www.alexa.com/siteinfo/"+domain) # check on Alexa
    response = html.fromstring(r.text)
    keywords = response.xpath('//td/span[2]/text()') # where Keywords located on the page
    for item in keywords:        
        if ord(item[0]) < 127:
            englishkeywords.append(item)
    keyworddict[domain] = englishkeywords
    keywordlist.append(keyworddict)
    
with open("keywords.txt","w") as f:
    json.dump(keywordlist, f)

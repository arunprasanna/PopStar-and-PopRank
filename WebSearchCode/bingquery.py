import json
from bing_search_api import BingSearchAPI

#read the top keywords(usually 1-3) and generate the search keyword parameter
k = []
with open("topkeywords.txt") as f:
    for line in f:
        k.append(line.strip())
s=' '.join(k)

n=1000  #search result limit

my_key = "uAZ6dYNEodLuQxx1W3UKkLegY+Uj8y7e1E3AxPwqtmM"  #API key
query_string = s    #the query string. currently only has keyword parameter.
bing = BingSearchAPI(my_key)    #initialize search request
params = {'$format': 'json'}    #response format as json

#output file
f = open("bingresults.txt","w")

#get first 50 results from Bing
for obj in bing.search('web',query_string,params).json()['d']['results']:
    for lnk in obj['Web']:
        f.write(lnk['Url'])
        f.write('\n')

i=50

#get the rest results
while i<n:
    params = {'$format': 'json','$skip': i} #skip first i results
    for obj in bing.search('web',query_string,params).json()['d']['results']:
        for lnk in obj['Web']:
            f.write(lnk['Url'])
            f.write('\n')
    i+=50

f.close()   #close output file
#!/usr/bin/env python

import urllib, bs4
from urlparse import urlparse

f = open('processedresults.txt', 'r')   #input file
f2 = open('filterresult.txt', 'w')  #output file

for line in f:
    arr = line.strip().split(' ')   #process input
    site = arr[0]   #site without scheme
    avgrank = arr[1]    #average rank in search engine
    fullurl = arr[2]    #site url with schme
    #Try accessing alexa rank page of the site. If not found, add the site to filterresult.
    try:
        alexarank = bs4.BeautifulSoup(urllib.urlopen("http://data.alexa.com/data?cli=10&dat=s&url="+ site).read(), "xml").find("REACH")['RANK']
    #print "Site rank is: ", alexarank
    except:
        f2.write(site+' '+avgrank+' '+fullurl+'\n')

#close files
f.close()
f2.close()
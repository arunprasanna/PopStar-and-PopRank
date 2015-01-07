import collections
from urlparse import urlparse

urldict = dict()    #store input urls
domaindict = dict() #store each occurance of a domain in the search result
resultdict = dict() #store the average rank of a domain in the search result
parsedurldict = dict()  #store the urls with scheme
gtldlist = ['com','org','net','edu','co'] #list of General Top Level Domainnames
i=0 #search engine rank counter

#read search engine rank of each URL
with open('bingresults.txt','r') as f:
    for line in f:
        i+=1
        urldict[line.strip()]=i

#Classify the ranks by site
for key,val in sorted(urldict.items(), key=lambda t: t[1]):
    parsedkey = urlparse(key)   #parse URL
    parsedurl = parsedkey.scheme + "://" + parsedkey.netloc #generate site URL with scheme for future use
    
    urltemp = parsedkey.netloc  #site URL without scheme
    
    #if site URL is like "aa.XXX", do nothing. Otherwise (eg: en.wikipedia.com) remove the first part.
    count_temp = urltemp.count('.')
    if count_temp >= 2 :
        domain=urltemp.split('.',1)[1]
        if (domain.split('.')[0] in gtldlist):
            domain=urltemp
        if domain not in domaindict:
            domaindict[domain]=[]   #initialize domain rank list
            parsedurldict[domain]=parsedurl #save the URL with scheme for future use
        domaindict[domain].append(val)  #append rank to domain rank list
    else:
        domain=urltemp
        if domain not in domaindict:
            domaindict[domain]=[]
            parsedurldict[domain]=parsedurl
        domaindict[domain].append(val)

#sort the result by first appearance in search engine result
resultitems = sorted(domaindict.items(), key=lambda t: t[1][0])

#output the result as site, times of appearance, appearances, URL with scheme
with open('processedfullresults.txt', 'w') as f:
    for key,val in resultitems:
        f.write( "{} {} {} ".format(key,len(val),val) )
        f.write( "{}\n".format(parsedurldict[key]))

#calculate average search engine rank
for key,val in domaindict.items():
    resultdict[key]=sum(val) / float(len(val))

#sort by average rank
resultitems = sorted(resultdict.items(), key=lambda t: t[1])

#output average rank
with open('processedresults.txt', 'w') as f:
    for key,val in resultitems:
        f.write( "{} {} {}\n".format(key,val,parsedurldict[key]) )
import requests
import json
from lxml import html
from collections import OrderedDict

keywordlist = []    #input list
blacklist = ['in','on','and','of','at'] #list of words that should not count as keyword

nkws = 3    #int(raw_input('Top Keywords:')) #uncomment to customize keywords

#read input
with open("keywords.txt") as tweetfile:
    keywordlist = json.load(tweetfile)

keyworddict=dict()  #output dict
# count appearances of each keyword
for keywordobj in keywordlist:
    for keywords in keywordobj.values():
        for keyword in keywords:
            for x in keyword.split(' '):
                if x not in blacklist:  #if the word is not blacklisted
                    if keyworddict.has_key(x):
                        keyworddict[x]+=1   #increment counter of that word
                    else:
                        keyworddict[x]=1

#order result by appearance from most to least often
kworder = OrderedDict(sorted(keyworddict.items(), key=lambda t: t[1], reverse=True));
#items to output
kwitems = kworder.items()

#output iterator
i=0

#output top keywords
with open("topkeywords.txt","w") as f:
    while i<nkws:
        f.write(str(kwitems[i][0])+'\n')
        i+=1

#output rank of all keywords to a separate file
with open("keywordsrank.txt","w") as f:
    json.dump(kworder, f)

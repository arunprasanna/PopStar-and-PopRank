#!/usr/bin/python

import json
import requests
import re
import collections
from collections import OrderedDict

# Use "sharedcount.com" API, to request the social reputation 
# of specific  websites not in Alexa, according to former Bing search results.
# the social reputation contains eight indicators collecting from six popular 
# social network sites. 
# They are  Stumbleupon, Google+, Twitter, Pininterest, Linkedin and Facebook.
# For Facebook, there are three more detailed indicators as the number of "Like",
# "Share" and "Comment".
# With these indicators, 
# we compute their reputation score by our Social Score Formula:
#       First, calculate the sum of each indicator of all the sites
#       Then, use each indicator's number of each site divided by each indicator's sum
#       Thus, we obtain the normalized indicator for each site of each indicator.
#       Last, we calculate each site's social score using weights collected form machine learning process.
#             Social Score = ((70.84*a[0]+96.08*a[1]+80.41*a[2]+80.35*a[3]+92.13*a[4]+96.07*a[5]+90.6*a[6]+97.5*a[7])/8)*1.134
# print the domain names on the first column 
# and the  social ranks of sites-not-on-Alexa, on the second column, according to social score
# and their rank according to Bing search, on the third column.

apikey = "9fe0c9cf72184c72f4cf1564923282dba1bd177f"
social_score = dict()
searchrank = dict()
social_data = dict()
site_name = []
sum_rep = [0 for i in range(8)]

with open('filterresult.txt', 'r') as f:
    for line in f:
        arr = line.strip().split(' ')
        site = arr[0] # site name 
        avgrank = arr[1] # ave search rank
        fullurl = arr[2] # full url for API request, http://www.
        site_name.append(site) 
        searchrank[site]=avgrank
        social_score[site] = 0
        # get social data 
        sharedcount_request = 'http://free.sharedcount.com/?apikey=' + apikey + '&url=' + fullurl
        
        socialrepdict = dict()
        socialrep = requests.get(sharedcount_request)
        socialrepdict['stumbleupon'] = int(re.findall(r'(?<="StumbleUpon":)\d+', socialrep.text)[0])
        socialrepdict['googleplusone'] = int(re.findall(r'(?<="GooglePlusOne":)\d+', socialrep.text)[0])
        socialrepdict['twitter'] = int(re.findall(r'(?<="Twitter":)\d+', socialrep.text)[0])
        socialrepdict['pininterest'] = int(re.findall(r'(?<="Pinterest":)\d+', socialrep.text)[0])
        socialrepdict['linkedin'] = int(re.findall(r'(?<="LinkedIn":)\d+', socialrep.text)[0])
        socialrepdict['fblike'] = int(re.findall(r'(?<="like_count":)\d+', socialrep.text)[0])
        socialrepdict['fbshare'] = int(re.findall(r'(?<="share_count":)\d+', socialrep.text)[0])
        socialrepdict['fbcomment'] = int(re.findall(r'(?<="comment_count":)\d+', socialrep.text)[0])
        
        # save each data for the website
        social_data[site] = [socialrepdict['stumbleupon'], socialrepdict['googleplusone'],socialrepdict['twitter'],socialrepdict['pininterest'] \
                               ,socialrepdict['linkedin'], socialrepdict['fblike'],socialrepdict['fbshare'],socialrepdict['fbcomment'] ]     
        # calculate the sum of each indicator
        sum_rep[0] += socialrepdict['stumbleupon'] 
        sum_rep[1] += socialrepdict['googleplusone'] 
        sum_rep[2] += socialrepdict['twitter'] 
        sum_rep[3] += socialrepdict['pininterest'] 
        sum_rep[4] += socialrepdict['linkedin']
        sum_rep[5] += socialrepdict['fblike'] 
        sum_rep[6] += socialrepdict['fbshare'] 
        sum_rep[7] += socialrepdict['fbcomment']

# a[] for normalized indicator for each site        
a = [0 for i in range(8)]
for i in site_name: # for each site
    for j in xrange(8): # for each indicator
        if sum_rep[j] == 0: # in case of devided by 0
            a[j] = 0
        else:
            a[j] = (float(social_data[i][j]) / float(sum_rep[j]))**(0.1) # normalizing the indicator
    # for each site, calculate its social score       
    social_score[i] = ((70.84*a[0]+96.08*a[1]+80.41*a[2]+80.35*a[3]+92.13*a[4]+96.07*a[5]+90.6*a[6]+97.5*a[7])/8)*1.134

# creat the rank of social score, descendingly.
social_score = OrderedDict(sorted(social_score.iteritems(), key=lambda d:d[1], reverse = True))
with open ('social_rank_search.txt', 'w') as sr:
    for k,v in  social_score.items():
        sr.write( "{} {} {}\n".format(k,v,searchrank[k]) )

#!/usr/bin/python
import re                                  
import subprocess
import socket

# This program is used to calculate the danger score of the websties-not-on-Alexa
# We first convert the domain names of the websites to IP
# Then, we "dig" these IP on the famous Blacklist Databses and count the number of been blacklisted.
# The number of been blacklisted by different Blacklists is recognizes as website's danger score.
# Last, we create the rank using their danger score, descendingly.

url_list = []
IP_list = []
Blacklist_Count = 0
Blacklist_Check = dict()
spamdbs = []

def ipformatcheck(x):
    global flag
    global Blacklist_Count
    global samdbs
    pattern = r"\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9]?[0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"
    if re.match(pattern, x): # check the input IP pattern
        # print ('Ip format valid')
        ip = str(x).split('.') 
        rev = '%s.%s.%s.%s' % (ip[3],ip[2],ip[1],ip[0]) # reverse the IP order 
        for db in spamdbs:           
            p = subprocess.Popen(["dig", "+short", rev+db], stdout=subprocess.PIPE)
            output, err = p.communicate()
            if output != '': # if IP is blacklisted, we'll get an output
              Blacklist_Count += 1
    else:
        print ('IP format InValid')
# URLs to be checked
with open('filterresult.txt','r') as f:
      for each_url in f:
        url_list.append(each_url.split(' ')[0])
# list of blacklist databases
with open('DB_BlackList','r') as DB:
      for each in DB:
        each = each.strip()
        spamdbs.append('.' + each)

# find URLs' IP
for each_url in url_list:
  each_url = each_url.strip()
  temp = socket.gethostbyname(each_url)
  # print temp, each_url
  IP_list.append( temp )

# check each IP, save the danger score
for x,y in zip(IP_list, url_list):
  ipformatcheck(x)
  # print x, y
  Blacklist_Check[y] = [x, Blacklist_Count]
  Blacklist_Count = 0
with open('Blacklist_Check_Score.txt','w') as BCS:
  for k, v in Blacklist_Check.items():
    BCS.write("{} {}\n".format(k,v[1]))
    

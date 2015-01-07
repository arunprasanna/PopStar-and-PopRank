#!/usr/bin/python

import sys
# read domain name from command line
mysite1 = str(sys.argv[1])
import os
import sqlite3 as lite
import json

conn=lite.connect('newalexa.db', 86400)
conn.text_factory = str
c=conn.cursor()

c.execute('select socialrep from AlexaInstance where domain = ?', [mysite1])
social1 = c.fetchall()

count=0;
key_values = [float(0)]*8
key_names = ('stumbleupon','twitter', 'linkedin','pininterest','fbcomment','googleplusone','fblike','fbshare')
for j in range (0, len(social1)):

        if(social1[j][0]):
                count=count+1;
                dict = json.loads(social1[j][0])
                #print dict
                my_index=0
                for key in key_names:
                        #print key
                        key_values[my_index] = dict[key] + key_values[my_index]
                        my_index = my_index+1

# normalization values
repsum = [421134.5175, 526307035.4, 1700302.238, 53943716.57, 25697982.28, 330558527.4, 37916308.55, 69369204.93]
for i in range(0, 8):
        key_values[i]=key_values[i]/count
        key_values[i]=((key_values[i]/repsum[i])**0.01)
print "DOMAIN: ", mysite1
#print "SOCIAL REP: ", key_values
#print key_names

#compute socialrep by calculating weighted linear combination
socialrep = (((70.84*key_values[0]+96.08*key_values[1]+80.41*key_values[2]+80.35*key_values[3]+92.13*key_values[4]+96.07*key_values[5]+90.6*key_values[6]+97.5*key_values[7])/8)*(1.134))
print "Social Reputation:", socialrep

conn.commit()
conn.close()

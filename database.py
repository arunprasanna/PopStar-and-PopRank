#!/usr/bin/python
import sys

# Input arguments
mydate1 = str(sys.argv[1]) #date1
mydate2 = str(sys.argv[2]) #date2
myrank1 = int(str(sys.argv[3])) #starting rank
myrank2 = int(str(sys.argv[4])) #ending rank

print mydate1, mydate2, myrank1, myrank2

import os

# connect to the sqlite db
import sqlite3 as lite
conn=lite.connect('newalexa.db', 86400)
conn.text_factory = str
c=conn.cursor()

# create table for storing the results
c.execute("DROP table Difftest")
c.execute("CREATE TABLE Difftest(Id INTEGER primary key AUTOINCREMENT, domain TEXT, date TEXT, rank TEXT NOT NULL, ld TEXT, nd TEXT, l1 TEXT, l2 TEXT, total_links TEXT, out_links TEXT, in_links TEXT, avg_len TEXT, stddev_len TEXT, imdiff1 TEXT, imdiff2 TEXT, imdiff3 TEXT, imdiff4 TEXT, stumbleupon TEXT, twitter TEXT, linkedin TEXT, pininterest TEXT, fbcomment TEXT, googleplusone TEXT, fblike TEXT, fbshare TEXT);")

# need to import json for processing the socialrep
import json
from bs4 import BeautifulSoup  # library "bs4 needed"
import sys
from Levenshtein import *     # library "python-Levenshtein-0.11.2" needed

# Get levenshtein distance between sourcecode from the given dates
def get_body_distance(website1,website2):  #Get the distance and normalized distance between two websites
    soup1 = BeautifulSoup(website1)
    soup2 = BeautifulSoup(website2)
    text1 = soup1.get_text()
    text2 = soup2.get_text()
    ld = distance(text1, text2)
    l1 = len(text1)
    l2 = len(text2)
    if((float(l1+l2))!=0):
        nld = ld/float(l1+l2)
    else:
        nld = "NA"
    return ld, nld, l1, l2      #ld: levenshtein distance  nld: normalized levenshtein distance l1: length of the first website l2:length of the second website


import urllib2
import re
import numpy as np

# count links' related stats
def link_counter(html,domain):

    links = re.findall('"((http|ftp)s?://.*?)"', html)
    link_length = []
    #domain = sys.argv[2]
    inlink_pt1 = '.'+ domain
    inlink_pt2 = '://'+domain
    in_link = 0
    for link in links:
        link_length.append(len(link[0]))  #record the len of each link
        if((inlink_pt1 in link[0]) or (inlink_pt2 in link[0])):
            in_link += 1           #record the number of internal links
    total_links = len(links)
    average_length = np.mean(link_length)
    out_link = total_links - in_link
    stddev_len = np.std(link_length)
    return total_links,out_link,in_link,average_length,stddev_len

from scipy.spatial import distance as dist
import numpy as np
import argparse
import glob
import cv2

# Compute image difference using image processing techniques
def scrshot_comp(shot1, shot2):
        index = {}
        images = {}
        results = {}

        image = cv2.imread(shot1) #input1
        #image = shot1
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        hist = cv2.normalize(hist).flatten()
        index[0] = hist

        image = cv2.imread(shot2)#input2
        #image = shot2
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        hist = cv2.normalize(hist).flatten()
        index[1] = hist
        #hist = index[0]



        # initialize OpenCV methods for histogram comparison
        OPENCV_METHODS = (
        ("Correlation", cv2.cv.CV_COMP_CORREL),
        ("Chi-Squared", cv2.cv.CV_COMP_CHISQR),
        ("Intersection", cv2.cv.CV_COMP_INTERSECT),
        ("Hellinger", cv2.cv.CV_COMP_BHATTACHARYYA))


        # loop over the comparison methods

        for (methodName, method) in OPENCV_METHODS:
                # initialize the results dictionary and the sort
                # direction
                #results = {}
                reverse = False

                # if we are using the correlation or intersection
                # method, then sort the results in reverse order
                if methodName in ("Correlation", "Intersection"):
                        reverse = True

                # loop over the index
                for (k, hist) in index.items():
                        # compute the distance between the two histograms
                        # using the method and update the results dictionary
                        d = cv2.compareHist(index[0], index[1], method)#marked
                        if methodName in ("Correlation"):
                                results[0] = d
                        if methodName in ("Chi-Squared"):
                                results[1] = d
                        if methodName in ("Intersection"):
                                results[2] = d
                        if methodName in ("Hellinger"):
                                results[3] = d
        return results[0], results[1], results[2], results[3]


# Read the two columns for two different dates
c.execute('select domain from AlexaInstance where date = ?', [mydate1])
domain1 = c.fetchall()
c.execute('select body from AlexaInstance where date =? ', [mydate1])
sourcecode1 = c.fetchall()
c.execute('select rank from AlexaInstance where date = ?', [mydate1])
rank1=c.fetchall()
c.execute('select snapshot from AlexaInstance where date = ?', [mydate1])
snap1 = c.fetchall()
c.execute('select socialrep from AlexaInstance where date = ?', [mydate1])
social1 = c.fetchall()
c.execute('select webkitbody from AlexaInstance where date = ?', [mydate1])
webkitbody1 = c.fetchall()

c.execute('select domain from AlexaInstance where date = ?', [mydate2])
domain2 = c.fetchall()
c.execute('select body from AlexaInstance where date = ?', [mydate2])
sourcecode2 = c.fetchall()
c.execute('select rank from AlexaInstance where date = ?', [mydate2])
rank2=c.fetchall()
c.execute('select snapshot from AlexaInstance where date = ?', [mydate2])
snap2 = c.fetchall()
c.execute('select socialrep from AlexaInstance where date = ?', [mydate2])
social2 = c.fetchall()
c.execute('select webkitbody from AlexaInstance where date = ?', [mydate2])
webkitbody2 = c.fetchall()

print len(domain1)
print len(domain2)

idd=1;
for i in range (0, len(domain1)):
        for j in range (0, len(domain2)):
                if(domain1[i][0]==domain2[j][0]):
                        if(not(((int(rank1[i][0]) >=myrank1) and (int(rank1[i][0]) <=myrank2)) or ((int(rank2[j][0])>=myrank1) and (int(rank2[j][0])<=myrank2)) or (int(rank1[i][0])>=1000000 or int(rank2[j][0])>=1000000))):
                                continue

                        key_names = ('stumbleupon','twitter', 'linkedin','pininterest','fbcomment','googleplusone','fblike','fbshare')
                        key_values = [None]*8
                        if(social2[j][0]):
                                dict2 = json.loads(social2[j][0])
                                my_index=0
                                for key in key_names:
                                        key_values[my_index] = dict2[key]
                                        my_index = my_index+1

                        socialagility = (((70.84*key_values[0]+96.08*key_values[1]+80.41*key_values[2]+80.35*key_values[3]+92.13*key_values[4]+96.07*key_values[5]+90.6*key_values[6]+97.5*key_values[7])/8)*(113.64/100))
                        v1=""
                        v2=""
                        v3=""
                        v4=""
                        if(int(rank1[i][0])>=900000 or int(rank2[j][0])>=900000):
                                v1,v2,v3,v4 = get_body_distance(str(webkitbody1[i][0]), str(webkitbody2[j][0]))
                        else:
                                v1,v2,v3,v4 = get_body_distance(str(sourcecode1[i][0]), str(sourcecode2[j][0]))
                        #ll1,ll2,ll3,ll4,ll5 = link_counter(str(sourcecode1[i][0]), str(domain1[i][0]))
                        ll6,ll7,ll8,ll9,ll10 = link_counter(str(sourcecode2[j][0]), str(domain2[j][0]))
                        #ll1 = ll6-ll1
                        #ll2 = ll7-ll2
                        #ll3 = ll8-ll3
                        #ll4 = ll9-ll4
                        #ll5 = ll10-ll5
                        #print "links done"
                        if( (snap1[i][0]) and (snap2[j][0])):
                                with open("mysnap1.png", "wb") as f:
                                        f.write(snap1[i][0])
                                with open("mysnap2.png", "wb") as f:
                                        f.write(snap2[j][0])
                                res1,res2,res3,res4 = scrshot_comp("mysnap1.png", "mysnap2.png")
                        else:
                                res1="NA"
                                res2="NA"
                                res3="NA"
                                res4="NA"
                        d1=str(domain1[i][0])
                        r1=str(rank2[j][0])
                        print "DOMAIN: ", d1
                        print "RANK: ", r1
                        print "DISTANCES: ", str(v1), str(v2), str(v3), str(v4)
                        print "LINKS: ",str(ll6), str(ll7) , str(ll8), str(ll9), str(ll10)
                        print "IMAGE DIFF:", str(res1), str(res2), str(res3), str(res4)
                        print "SOCIAL FOOTPRINT: ", key_values
                        c.execute("INSERT INTO Difftest  (domain, date, rank, ld, nd, l1, l2, total_links, out_links, in_links, avg_len, stddev_len, imdiff1, imdiff2, imdiff3, imdiff4, stumbleupon, twitter, linkedin, pininterest, fbcomment, googleplusone, fblike, fbshare) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",[d1, mydate2, r1, str(v1), str(v2), str(v3), str(v4), str(ll6), str(ll7) , str(ll8), str(ll9), str(ll10), str(res1), str(res2), str(res3), str(res4), key_values[0],key_values[1],key_values[2],key_values[3],key_values[4],key_values[5],key_values[6],key_values[7]])
                        print i

conn.commit()
conn.close()

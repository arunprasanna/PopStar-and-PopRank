#!/usr/bin/python

"""
PhantomSpider.py written by Malcolm Haynes (mghaynes@gatech.edu), last modified 11/19/14
This code crawls a list of websites in the Alexa1M and renders the sites in a headless PhantomJS webkit.
After rendering the page, it takes a snapshot of the page and gets the source code. It also gets 
social network information on the site. It then stores all this in a SQLite database.
"""

from StringIO import StringIO
from zipfile import ZipFile
from urllib import urlopen
from csv import DictReader
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import sqlite3 as lite
import threading
import json
import datetime
import time
import json
import requests
import re

# My api key for SharedCount website to get social network information
apikey = "9fe0c9cf72184c72f4cf1564923282dba1bd177f"

# settings for PhantomJS to emulate Internet Explorer
dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; chromeframe/11.0.696.57")
dcap['acceptSslCerts'] = True

today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
today = today.isoformat()
yesterday = yesterday.isoformat()
readerlist = []

# code for thread to run multiple PhantomJS instances
class PhantomThread(threading.Thread):
     def __init__(self, urlist):
        super(PhantomThread, self).__init__()         
        self.urlist = urlist
        self.seldata = [] 
        
            
     def run(self):
     	# establish connection to database
        con = lite.connect('/nethome/mhaynes35/AlexaStuff/newalexa.db', 86400)
        cur = con.cursor()    
        for item in self.urlist:
            print "Getting site #%s. %s..." % (item['rank'], item['domain'])
            
            # initialize PhantomJS instance
            self.driver=webdriver.PhantomJS(desired_capabilities=dcap)
            self.driver.maximize_window()            
            self.driver.set_page_load_timeout(60)
            self.driver.set_script_timeout(60)
            
            #start timer
            ts = time.time()
            
            #try to get the website
            error = False
            try:
                site = requests.get("http://www."+item['domain'])
            except:
                print "Couldn't get site. Trying without www extension..."
                try:
                    site = requests.get("http://"+item['domain'])
                    print "That worked!"
                except:
                    print "No joy! Moving on to next site"
                    error = True
            
            if not error:
                try:
                    self.driver.get(site.url)
                    sel_error = False
                except:
                    print "Selenium can't get the site...but Requests did. Weird."
                    sel_error = True
                if not sel_error:
                	scrollheight = .1
                	time.sleep(.3)
                	try:
                		# scroll down site in case of AJAX and to ensure load of all images
                		while scrollheight < 10:
                			self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight*%s);" % scrollheight)
                			scrollheight += .1    
                			time.sleep(.1)          
                	except:
                		print "Something wrong with scrolling function"
                	time.sleep(.3)
                try:
                	snapshot = lite.Binary(self.driver.get_screenshot_as_png())
                except:
                	print "error with photo"
                    snapshot = ''
                webkitbody = self.driver.page_source 
                rankdate = item['rank']+'-'+today
                basicinfo = (rankdate, today, item['rank'], item['domain'])
                url = site.url
                if self.driver.current_url == 'about:blank':
                	pass
                else:
                	url = self.driver.current_url
                if self.driver.title == '':
                	webkitbody = site.text
                body = webkitbody

                # Get the social network information
                sharedcount_request = 'http://free.sharedcount.com/?apikey=' + apikey + '&url=' + url
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

				# write everything to the database                
                with con:                                     
                    cur.execute("INSERT OR IGNORE INTO AlexaInstance(rankdate, date, rank, domain) VALUES(?, ?, ?, ?)", basicinfo)
                    cur.execute("UPDATE AlexaInstance SET url=?, body=?, webkitbody=?, snapshot=?, socialrep=? WHERE rankdate = ?;", (url, body, webkitbody, snapshot, json.dumps(socialrepdict), rankdate))                                     
                self.driver.quit()
                print "Completed site #%s. %s in %d seconds" % (item['rank'], url, int(time.time()-ts))
        
        
"""-----------------------
    THIS IS THE MAIN BODY 
   -----------------------"""
#Get the current list of Alexa 1M
with open("/nethome/mhaynes35/AlexaStuff/top-1m.json", "r") as f:
    readerlist = json.load(f)

#Asks for number of sites to get. Any random input returns 10 sites
try:
    startrank = int(input("Enter rank of first site you would like to get (Default is 1): "))
    startrank -= 1
    endrank = int(input("Enter rank of last site you would like to get (Default is 10): "))
except:
    startrank = 0
    endrank = 9

threadlist = []
numthreads = 2 
numsites = endrank - startrank 
sitesper = numsites/numthreads

ts = time.time()

# initiate each thread
for cnt in range(0, numthreads):
    start = sitesper * cnt + startrank
    last = sitesper * (cnt + 1) + startrank
    urlist = readerlist[start:last]
    thread = PhantomThread(urlist)
    thread.start()
    threadlist.append(thread)

for thread in threadlist:
    thread.join()
    
print "Total time to get all sites is: ", int(time.time()-ts)
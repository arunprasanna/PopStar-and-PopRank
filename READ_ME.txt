————READ_ME—————

————POP STAR GENERAL DOCUMENTATION———

The code is sub divided into four sub-modules:

1.Crawler script - PhantomSpider.py
3.Database script and extraction of Features - database.py, websiteagility.py, socialrep.py.
4.Machine learning scripts.
5.Web Search Scripts.

Step 0: 
If the below scripts are being run in a different virtual machine than the one we have worked on, type the following to create the database:
python created.py

1.Crawler

Description:Crawls websites in the Alexa 1M. For each crawled site it renders the page, scrolls down to the bottom of the page, and then stores a snapshot of the page as well as the source code, url, social reputation metrics and other miscellaneous elements. The information is stored in a SQLite database in the directory /nethome/mhaynes35/AlexaStuff/newalexa.db

Libraries Required: selenium

Other Requirements: PhantomJS installed, SQLite installed

License type of libraries: Open source

Steps to run the script:
From the command line, type ‘python PhantomSpider.py’. 
The script will ask you to enter the rank of the first and last website you want to crawl within the Alexa top 1 million.







2.Database and Extraction of Features

Description: Queries the database created by the crawler and calculates all agility parameters. Stores these parameters in a new database for further analysis and running of the machine learning script.

Libraries Required:
	1.Beautiful soup. INSTALL library bs4 to calculate source code 	distance parameters.
	2.Levenshtein library . Version-.0.11.2 needed.
	3.INSTALL numpy.
	4.INSTALL open cv version 2.0 or later.


License type of libraries:open source

Steps to run the script:
1. python database.py <date1> <date2> <rankstart> <rankend>
eg. python database 2014-10-30 2014-10-31 1 100
2.To calculate the social reputation run the following script:
socialrep.py:
python socialrep.py <domain>
eg. socialrep.py yahoo.com
3.To calculate the website agility, run the following script:
websiteagility.py:
python websiteagility.py <date1> <date2> <domain>
eg. python websiteagility.py 2014-11-04 2014-11-05 bing.com



4.Machine Learning Scripts

Description:Script to 

Packages Required:
	1.pandas (v0.14.1 or higher)
	2.numpy (v1.8.0 or higher)
	3.sklearn (v0.7.3 or higher )

License type of libraries:Open Source

Description of machine learning scripts:

—-‘Get_data4ML_fromDB.py’ is used to extract data of benign and malicious websites from the database, compute statistics from the data, removes invalid data points, and store them in the following files: 
‘valid_simp_leg.pkl’   
'valid_simp_mal.pkl’
’valid_simplified_leg_stats_M.csv’
’valid_simplified_mal_stats_M.csv'
The execution might take several minutes due to the huge size of our database. 
You need to run this scripts on our virtual machine

—- ‘MachineLearning_Validation.py’ take 'valid_simp_leg.pkl’ and 'valid_simp_mal.pkl’ (outputs of ‘Get_data4ML_fromDB.py’) as inputs, train and validate our machine learning detector with the data, and output the results. (For convinience, we have also include'valid_simp_leg.pkl’ and 'valid_simp_mal.pkl’ in the same directory, so that you run this script directly) By default, the machine learning algorithm will use all the features that we mention in the paper. If you want to use only part of the features in the classifier, you can remove some features in the ‘used_feature’, which is located on the first row of the script. The following are the categories of these features:

source code change: ‘ave_ld','ave_nd'
image change: 'ave_imdiff4'
link information: ‘ave_links','ave_out'
social reputation: ’stumbleupon','twitter','linkedin','pininterest','fbcomment','googleplusone','fblike'


Steps to run the script:
1. python Get_data4ML_fromDB.py
2. python MachineLearning_Validation.py




5.Web Search

Description: 
	Parse websites in specific category from DMOZ. Crawl each site’s page on Alexa to get its keywords and then process these keywords to get top 3 keywords on given industry. Using Bing search API with top 3 keywords, get the search results. Process these results to give each domain final search rank according to their each time position on Bing results. Comparing the results with Alexa to get a set of website-not-on-Alexa. Using our Social Rep Algorithm to give them PopRank. Meanwhile, check their appearance on multiple blacklist databases to calculate Danger Score.

Libraries Required:
	1. BeautifulSoup4
	2. numpy
	3. lxml
	4. json

Data Source Required:
	The DMOZ content from
	http://rdf.dmoz.org/rdf/content.rdf.u8.gz
	

License type of libraries: 
	Open Source.

Steps to run the script:
1	Extract the WebSearchCode(version).zip and the DMOZ content to the same folder
2	In Terminal, cd to the extracted folder
3	Execute ‘python run_all.py’
4	When prompted, enter the target category name. Category name is listed as subcategory on “http://www.alexa.com/topsites/category” under each category link.
5	Wait for the workflow to complete. The Ranking result is in ‘social_rank_search.txt’
Attention:	This workflow may take up to 1500s to finish all its work. The BlackList check may take up to 600s depending on network latency.

To Plot Graphs:
When run_all.py successfully finishes, the Danger Score v.s. Social Rep Score/Search Engine Rank distribution of current category will show up.
To Plot the 2D distribution of Danger Score v.s. Social Rep Rank, cd the category folder and Execute ‘python plot.py’
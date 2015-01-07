import sqlite3
import csv
import pandas as pd
import numpy as np
import urllib2
import re

conn = sqlite3.connect('/nethome/mhaynes35/AlexaStuff/newalexa.db')
conn.text_factory = str
c=conn.cursor()


date_list=['10281029','10291030','10301031','10311101','11011103','11031104','11041105','11051106','11061107','11071108']
domain_list = []
difference_list = ['ld','nd','imdiff1','imdiff2','imdiff3','imdiff4','stumbleupon','twitter','linkedin','pininterest','fbcomment','googleplusone','fblike','fbshare']
feature_list = ['ld','nd','imdiff1','imdiff2','imdiff3','imdiff4','stumbleupon','twitter','linkedin','pininterest','fbcomment','googleplusone','fblike','fbshare','total_links','out_links','in_links','ave_len','stddev_len']
not_social_feature_list = ['ld','nd','imdiff1','imdiff2','imdiff3','imdiff4','total_links','out_links','in_links','ave_len','stddev_len']
social_feature_list = ['stumbleupon','twitter','linkedin','pininterest','fbcomment','googleplusone','fblike','fbshare']



def link_counter(html,domain):
    
    links = re.findall('"((http|ftp)s?://.*?)"', str(html))
    link_length = []
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

# ======================================== Get benign websites from the database=====================================================
# create unique domain name list
for date in date_list:

      table = 'Diff' + date+'_new';
      c.execute('select domain from '+table+' where rank not like \'1______\'' )  #Only for benign website at this time
      results = c.fetchall()
      for row in results:
            domain_list.append(row[0])

# remove duplicate domain names
domain_list = list(set(domain_list))  

# create a content matrix 
content_M = pd.DataFrame(index = domain_list, columns = feature_list)
for domain in domain_list:                          # initialize content matrix
      for feature in feature_list:
            content_M.loc[domain,feature] = []

# extract agility and social reputation information
for date in date_list: # for each difference table
    
      table = 'Diff' + date + '_new';
      c.execute('select domain,ld,nd,imdiff1,imdiff2,imdiff3,imdiff4,stumbleupon,twitter,linkedin,pininterest,fbcomment,googleplusone,fblike,fbshare from '+table+' where rank not like \'1______\'')
      results = c.fetchall()
      for row in results:    # for each domain in a table
            if (row[2] == 'NA') or (row[6] == 'NA'):    # check whether a domain record is valid
                continue
            i = 1;
            for feature in difference_list:   # for each feature of a domain
                  if row[i] == '':     # for empty result
                      continue
                  elif 'E' in row[i]:
                      content_M.loc[row[0],feature].append(0)  # for very small number that contains E, regard it as 0
                  else:
                      content_M.loc[row[0],feature].append(float(row[i]))
                  i+=1

# extract link information
for domain in domain_list:
     query = 'select body from AlexaInstance where domain ='+'\''+ domain + '\''
     c.execute(query)
     results = c.fetchall()
     for row in results:
         if row[0] == []:
             continue
         total_links,out_links,in_links,average_length,stddev_len =  link_counter(row[0], domain)
         content_M.loc[domain,'total_links'].append(total_links)
         content_M.loc[domain,'out_links'].append(out_links)
         content_M.loc[domain,'in_links'].append(in_links)
         content_M.loc[domain,'ave_len'].append(average_length)
         content_M.loc[domain,'stddev_len'].append(stddev_len)



# create a statistic matrix
stat_feature = ['ave_ld','std_ld','med_ld','ave_nd','std_nd','med_ld','ave_imdiff1','std_imdiff1','med_imdiff1','ave_imdiff2','std_imdiff2','med_imdiff2','ave_imdiff3','std_imdiff3', 'med_imdiff3','ave_imdiff4','std_imdiff4','med_imdiff4','ave_links','std_links','med_links','ave_out','std_out','med_out','ave_in','std_in','med_in','ave_len','std_ave_len','med_ave_len','stddev_len','std_stddev_len','med_stddev_len','stumbleupon','twitter','linkedin','pininterest','fbcomment','googleplusone','fblike','fbshare']
stats_M = pd.DataFrame(index = domain_list, columns = stat_feature)

for domain in domain_list:
    i = 0
    for feature in not_social_feature_list:
        if content_M.loc[domain,feature]!=[]:
               stats_M.loc[domain,stat_feature[3*i + 0]] = float(np.mean(content_M.loc[domain,feature]))
               stats_M.loc[domain,stat_feature[3*i + 1]] = float(np.std(content_M.loc[domain,feature]))
               stats_M.loc[domain,stat_feature[3*i + 2]] = float(np.median(content_M.loc[domain,feature]))
        else:
               stats_M.loc[domain,stat_feature[3*i]] = -1
               stats_M.loc[domain,stat_feature[3*i + 1]] = -1
               stats_M.loc[domain,stat_feature[3*i + 2]] = -1
        i+=1
    
    for feature in social_feature_list:
        if content_M.loc[domain,feature]!=[]:
               stats_M.loc[domain,feature]= float(np.mean(content_M.loc[domain,feature]))
        else:
               stats_M.loc[domain,feature] = -1


content_M.to_pickle('datagram_new.pkl')
stats_M.to_pickle('stats_new.pkl')

#============================ Get malicious websites from the database ==========================================================

date_list=['11051106']
domain_list = []
difference_list = ['ld','nd','imdiff1','imdiff2','imdiff3','imdiff4','stumbleupon','twitter','linkedin','pininterest','fbcomment','googleplusone','fblike','fbshare']
feature_list = ['ld','nd','imdiff1','imdiff2','imdiff3','imdiff4','stumbleupon','twitter','linkedin','pininterest','fbcomment','googleplusone','fblike','fbshare','total_links','out_links','in_links','ave_len','stddev_len']
not_social_feature_list = ['ld','nd','imdiff1','imdiff2','imdiff3','imdiff4','total_links','out_links','in_links','ave_len','stddev_len']
social_feature_list = ['stumbleupon','twitter','linkedin','pininterest','fbcomment','googleplusone','fblike','fbshare']


for date in date_list:

      table = 'Diff' + date+'_new';
      c.execute('select domain from '+table+' where rank like \'1______\'' )  #Only for benign website at this time
      results = c.fetchall()
      for row in results:
            domain_list.append(row[0])

# remove duplicate domain names
domain_list = list(set(domain_list))  

# create a content matrix
content_M = pd.DataFrame(index = domain_list, columns = feature_list)
for domain in domain_list:                          # initialize content matrix
      for feature in feature_list:
            content_M.loc[domain,feature] = []


for date in date_list: # for each difference table
    
      table = 'Diff' + date + '_new';
      c.execute('select domain,ld,nd,imdiff1,imdiff2,imdiff3,imdiff4,stumbleupon,twitter,linkedin,pininterest,fbcomment,googleplusone,fblike,fbshare from '+table+' where rank like \'1______\'')
      results = c.fetchall()
      for row in results:    # for each domain in a table
            if (row[2] == 'NA') or (row[6] == 'NA'):    # check whether a domain record is valid
                continue
            i = 1;
            for feature in difference_list:   # for each feature of a domain
                  if row[i] == '':     # for empty result
                      continue
                  elif 'E' in row[i]:
                      content_M.loc[row[0],feature].append(0)  # for very small number that contains E, regard it as 0
                  else:
                      content_M.loc[row[0],feature].append(float(row[i]))
                  i+=1


for domain in domain_list:
     query = 'select webkitbody from AlexaInstance where domain ='+'\''+ domain + '\''
     c.execute(query)
     results = c.fetchall()
     for row in results:
         if row[0] == []:
             continue
         total_links,out_links,in_links,average_length,stddev_len =  link_counter(row[0], domain)
         content_M.loc[domain,'total_links'].append(total_links)
         content_M.loc[domain,'out_links'].append(out_links)
         content_M.loc[domain,'in_links'].append(in_links)
         content_M.loc[domain,'ave_len'].append(average_length)
         content_M.loc[domain,'stddev_len'].append(stddev_len)



# create a statistic matrix
stat_feature = ['ave_ld','std_ld','med_ld','ave_nd','std_nd','med_ld','ave_imdiff1','std_imdiff1','med_imdiff1','ave_imdiff2','std_imdiff2','med_imdiff2','ave_imdiff3','std_imdiff3', 'med_imdiff3','ave_imdiff4','std_imdiff4','med_imdiff4','ave_links','std_links','med_links','ave_out','std_out','med_out','ave_in','std_in','med_in','ave_len','std_ave_len','med_ave_len','stddev_len','std_stddev_len','med_stddev_len','stumbleupon','twitter','linkedin','pininterest','fbcomment','googleplusone','fblike','fbshare']
stats_M = pd.DataFrame(index = domain_list, columns = stat_feature)

for domain in domain_list:
    i = 0
    for feature in not_social_feature_list:
        if content_M.loc[domain,feature]!=[]:
               stats_M.loc[domain,stat_feature[3*i + 0]] = float(np.mean(content_M.loc[domain,feature]))
               stats_M.loc[domain,stat_feature[3*i + 1]] = float(np.std(content_M.loc[domain,feature]))
               stats_M.loc[domain,stat_feature[3*i + 2]] = float(np.median(content_M.loc[domain,feature]))
        else:
               stats_M.loc[domain,stat_feature[3*i]] = -1
               stats_M.loc[domain,stat_feature[3*i + 1]] = -1
               stats_M.loc[domain,stat_feature[3*i + 2]] = -1
        i+=1
    
    for feature in social_feature_list:
        if content_M.loc[domain,feature]!=[]:
               stats_M.loc[domain,feature]= float(np.mean(content_M.loc[domain,feature]))
        else:
               stats_M.loc[domain,feature] = -1

content_M.to_pickle('malicious_datagram_new.pkl')
stats_M.to_pickle('malicious_stats_new.pkl')

conn.commit()
conn.close()

# =================================== Remove Invalid  data=======================================================================

# create a statistic matrix
important_feature = ['ave_ld','ave_nd','ave_imdiff1','ave_imdiff2','ave_imdiff3','ave_imdiff4','ave_links','ave_out','ave_in','ave_len','stddev_len','stumbleupon','twitter','linkedin','pininterest','fbcomment','googleplusone','fblike']

#legitimate websites
leg_stats_M = pd.read_pickle('stats_new.pkl')
leg_domain = leg_stats_M.index
valid_leg_domain = []


for domain in leg_domain:
    valid = 1
    for feature in important_feature:
        if leg_stats_M.loc[str(domain)][feature] == -1:
            valid = 0
            break
    if valid == 0:
         continue
    elif valid == 1:
         valid_leg_domain.append(domain)

simp_leg_stats_M = pd.DataFrame(index = valid_leg_domain, columns = important_feature)

for domain in valid_leg_domain:
    for feature in important_feature:
        simp_leg_stats_M.loc[str(domain)][feature] = leg_stats_M.loc[str(domain)][feature]

simp_leg_stats_M.to_csv('valid_simplified_leg_stats_M.csv')
simp_leg_stats_M.to_pickle('valid_simp_leg.pkl')

#malicious websites
mal_stats_M = pd.read_pickle('malicious_stats_new.pkl')
mal_domain = mal_stats_M.index
valid_mal_domain = []

for domain in mal_domain:
    valid = 1
    for feature in important_feature:
        if mal_stats_M.loc[str(domain)][feature] == -1:
            valid = 0
            break
    if valid == 0:
        continue
    elif valid == 1:
        valid_mal_domain.append(domain)

simp_mal_stats_M = pd.DataFrame(index = valid_mal_domain, columns = important_feature)

for domain in valid_mal_domain:
    for feature in important_feature:
        simp_mal_stats_M.loc[str(domain)][feature] = mal_stats_M.loc[str(domain)][feature]


simp_mal_stats_M.to_csv('valid_simplified_mal_stats_M.csv')
simp_mal_stats_M.to_pickle('valid_simp_mal.pkl')

import sqlite3
import csv
import pandas as pd
import numpy as np
import urllib2
import re
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn import cross_validation

# Default features for 'used feature':
# ['ave_ld','ave_nd','ave_imdiff4','ave_links','ave_out','stumbleupon','twitter','linkedin','pininterest','fbcomment','googleplusone','fblike']

used_feature = ['ave_ld','ave_nd','ave_imdiff4','ave_links','ave_out','stumbleupon','twitter','linkedin','pininterest','fbcomment','googleplusone','fblike']


#Get data from legitimate websites
leg_stats_M = pd.read_pickle('valid_simp_leg.pkl')
leg_list = []


for domain in leg_stats_M.index:
    temp = []
    for feature in used_feature:
        temp.append(leg_stats_M.loc[domain,feature])
    leg_list.append(temp)


leg_label = list(np.ones(len(leg_list)))


#Get data from malicious websites
mal_stats_M = pd.read_pickle('valid_simp_mal.pkl')
mal_list = []

for domain in mal_stats_M.index:
    temp = []
    for feature in used_feature:
        temp.append(mal_stats_M.loc[domain,feature])
    mal_list.append(temp)

mal_label = list(np.zeros(len(mal_list)))

data = leg_list + mal_list
label = leg_label + mal_label


AC2 = []
TP2 = []
FP2 = []

# Machine learning and Validation
for i in range(100):

    x_train, x_test, y_train, y_test = cross_validation.train_test_split(data,label, test_size=0.2, random_state=0)
    
    clf2 = RandomForestClassifier(n_estimators=10)
    clf2.fit(x_train,y_train)
    y_pred2 = clf2.predict(x_test)
    result2 = confusion_matrix(y_test, y_pred2)

    AC2.append(accuracy_score(y_test, y_pred2))
    TP2.append(float(result2[0][0])/(result2[0][0]+result2[0][1]))
    FP2.append(float(result2[1][0])/(result2[1][0]+result2[1][1]))


print 'Feature_used:'
print used_feature
print '\n'
print 'Results:'
print 'average acurracy:'+ str(np.mean(AC2))
print 'average true positive rate:' + str(np.mean(TP2))
print 'average false positive rate:'+ str(np.mean(FP2))+'\n'




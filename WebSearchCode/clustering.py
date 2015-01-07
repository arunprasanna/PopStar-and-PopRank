from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import math
from collections import OrderedDict

xaxis = [OrderedDict(),OrderedDict(),OrderedDict(),OrderedDict(),OrderedDict()]
yaxis = [OrderedDict(),OrderedDict(),OrderedDict(),OrderedDict(),OrderedDict()]
# read socialrep score and search rank from file



iterator = 0
with open('Food/social_rank_search.txt','r') as food:
    for dn in food:
        xaxis[iterator][dn.split(' ')[0]] = [dn.split(' ')[1],dn.split(' ')[2]]
iterator += 1
with open('Football/social_rank_search.txt') as football:
    for dn in football:
        xaxis[iterator][dn.split(' ')[0]] = [dn.split(' ')[1],dn.split(' ')[2]]
iterator += 1
with open('Education/social_rank_search.txt') as education:
    for dn in education:
        xaxis[iterator][dn.split(' ')[0]] = [dn.split(' ')[1],dn.split(' ')[2]]
iterator += 1
with open('Energy/social_rank_search.txt') as energy:
    for dn in energy:
        xaxis[iterator][dn.split(' ')[0]] = [dn.split(' ')[1],dn.split(' ')[2]]
iterator += 1
with open('Environment/social_rank_search.txt') as environment:
    for dn in environment:
        xaxis[iterator][dn.split(' ')[0]] = [dn.split(' ')[1],dn.split(' ')[2]]

# read danger score from file
iterator = 0
with open('Food/Blacklist_Check_Score.txt','r') as food:
    for dn in food:
        yaxis[iterator][dn.split(' ')[0]] = dn.split(' ')[1]
iterator += 1
with open('Football/Blacklist_Check_Score.txt') as football:
    for dn in football:
        yaxis[iterator][dn.split(' ')[0]] = dn.split(' ')[1]
iterator += 1
with open('Education/Blacklist_Check_Score.txt') as education:
    for dn in education:
        yaxis[iterator][dn.split(' ')[0]] = dn.split(' ')[1]
iterator += 1
with open('Energy/Blacklist_Check_Score.txt') as energy:
    for dn in energy:
        yaxis[iterator][dn.split(' ')[0]] = dn.split(' ')[1]
iterator += 1
with open('Environment/Blacklist_Check_Score.txt') as environment:
    for dn in environment:
        yaxis[iterator][dn.split(' ')[0]] = dn.split(' ')[1]


# convert strings into floats
xf = [OrderedDict(),OrderedDict(),OrderedDict(),OrderedDict(),OrderedDict()]
yf = [OrderedDict(),OrderedDict(),OrderedDict(),OrderedDict(),OrderedDict()]
for i in xrange(len(xaxis)):
    for k,v in xaxis[i].items():
        v[1] = v[1].strip()
        xf[i][k] = [float(v[0]), float(v[1])/10.0]
    for k,bl in yaxis[i].items():
        bl = bl.strip()
        yf[i][k] = float(bl)

# sort the social rank and search rank
x_social = [OrderedDict(),OrderedDict(),OrderedDict(),OrderedDict(),OrderedDict()]
x_search = [OrderedDict(),OrderedDict(),OrderedDict(),OrderedDict(),OrderedDict()]
for i in xrange(len(xf)):
    x_social[i] = OrderedDict(sorted(xf[i].iteritems(), key=lambda (k,v): v[0], reverse = True)) # descending
    x_search[i] = OrderedDict(sorted(xf[i].iteritems(), key=lambda (k,v): v[1], reverse = False)) # ascending

# map the danger score to the sequence of social rank
yfm_social = [OrderedDict(),OrderedDict(),OrderedDict(),OrderedDict(),OrderedDict()]

normsocial = []
normsearch = []
for ii in range (0, 5):
    new = []
    new1 = []
    for jj in range (0, 10):
        new.append(0)
        new1.append(0)
    normsocial.append(new)
    normsearch.append(new1)



for i in xrange(len(x_social)):
    for k,v in x_social[i].items():
        if(yf[i][k]>0):
            normsocial[i][int(math.floor(v[0]/10))]+=1
        
        for p in yf[i].items():
            if k == p[0]:
                yfm_social[i][p[0]] = p[1]
            
            else:
                continue


# map the danger score to the sequence of search rank
yfm_search = [OrderedDict(),OrderedDict(),OrderedDict(),OrderedDict(),OrderedDict()]
for i in xrange(len(x_search)):
    for k,v in x_search[i].items():
        if(yf[i][k]>0):
            normsearch[i][int(math.floor(v[1]/10))]+=1
        
        for p in yf[i].items():
            if k == p[0]:
                yfm_search[i][p[0]] = p[1]
            else:
                continue

# plot

fig1 = plt.figure()
fig2 = plt.figure()
ax1 = fig1.add_subplot(111, projection='3d')
ax2 = fig2.add_subplot(111, projection='3d')

for i, c, z in zip(reversed(range(len(x_social))), ['r', 'g', 'b', 'y', 'c'], [40, 30, 20, 10, 0]):
    cs = [c] * len(x_social)
    x = range(len(x_social[i]))
#ax1.bar(x, yfm_social[i].values(), zs=z, zdir='y', color=cs, alpha=0.8)
    ax1.bar(range(10), normsocial[i], zs=z, zdir='y', color=cs, alpha=0.8)

ax1.set_xlabel('Social Rank')
ax1.set_ylabel('Food  Fb  Edu  Eng  Env')
ax1.set_zlabel('Danger Score')

for i, c, z in zip(reversed(range(len(x_search))), ['r', 'g', 'b', 'y', 'c'], [40, 30, 20, 10, 0]):
    cs = [c] * len(x_search)
    x = range(len(x_search[i]))
#ax2.bar(x, yfm_search[i].values(), zs=z, zdir='y', color=cs, alpha=0.8)
    ax2.bar(range(10), normsearch[i], zs=z, zdir='y', color=cs, alpha=0.8)

ax2.set_xlabel('Bing Search Rank')
ax2.set_ylabel('Food  Fb  Edu  Eng  Env')
ax2.set_zlabel('Danger Score')
plt.show()
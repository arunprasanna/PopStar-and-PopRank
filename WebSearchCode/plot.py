from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from collections import OrderedDict

xaxis1 = OrderedDict()
xaxis2_temp = OrderedDict()
xaxis2 = OrderedDict()
yaxis = OrderedDict()

# social rank, key = domain, value[0] = social rep score, value[1] = search rank
with open('social_rank_search.txt','r') as sr:
	for dn in sr:
		xaxis1[dn.split(' ')[0]] = dn.split(' ')[1]
		xaxis2_temp[dn.split(' ')[0]] = dn.split(' ')[2]

xaxis2 = OrderedDict(sorted(xaxis2_temp.iteritems(), key=lambda d:d[1], reverse = False))


with open('Blacklist_Check_Score.txt','r') as bl:
	for dn in bl:
		yaxis[dn.split(' ')[0]] = dn.split(' ')[1]

# change strings to floats
xf1 = OrderedDict()
xf2 = OrderedDict()
yf = OrderedDict()
for each in xaxis1.items():
	xf1[each[0]] = float(each[1])
for each in xaxis2.items():
	xf2[each[0]] = float(each[1])
for each in yaxis.items():
	yf[each[0]] = float(each[1])

# map y to x
yf1 = OrderedDict()
yf2 = OrderedDict()
for i in xf1.items():
	for j in yf.items():
		if i[0] == j[0]:
			yf1[i[0]] = j[1]
		else:
			continue
for i in xf2.items():
	for j in yf.items():
		if i[0] == j[0]:
			yf2[i[0]] = j[1]
		else:
			continue


# plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
x1 = range(len(xf1))
x2 = range(len(xf2))
x3 = []
for i in xrange(len(xf1)):
	x3.append(0)
y3 = []
for i in xrange(len(xf1)):
	y3.append(0)
ax.bar(x1, yf1.values(), zs=15, zdir='y', color='g', alpha=0.8)
ax.bar(x2, yf2.values(), zs=0, zdir='y', color='y', alpha=0.8)
ax.bar(x3, y3, zs=20, zdir='y', color='b', alpha=0.8)
ax.set_xlabel('Rank')
ax.set_ylabel('Bing Search                 Social Rep')
ax.set_zlabel('Number of Blacklisted')
plt.yticks([])
plt.show()

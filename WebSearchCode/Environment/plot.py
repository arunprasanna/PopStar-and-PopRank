from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from collections import OrderedDict
# from pylab import *
xaxis1 = OrderedDict()
# xaxis2 = dict()
xaxis2_temp = OrderedDict()
xaxis2 = OrderedDict()
yaxis = OrderedDict()

# social rank, key = domain, value = social rank
with open('social_rank_search.txt','r') as sr:
	for dn in sr:
		xaxis1[dn.split(' ')[0]] = dn.split(' ')[1]
		xaxis2_temp[dn.split(' ')[0]] = dn.split(' ')[2]

xaxis2 = OrderedDict(sorted(xaxis2_temp.iteritems(), key=lambda d:d[1], reverse = False))
# search rank, key = do

# br = open('filterresult.txt','r')
# for line in br:
# 	xaxis2[line.split(' ')[0]] = line.split(' ')[1]
# br.close()
with open('Blacklist_Check_Score.txt','r') as bl:
	for dn in bl:
		yaxis[dn.split(' ')[0]] = dn.split(' ')[1]

# x1 = xaxis1.values()
# x2 = xaxis2.values()
# y = yaxis.values()
# change strings to floats
# print xaxis2.items()
xf1 = OrderedDict()
xf2 = OrderedDict()
yf = OrderedDict()
for each in xaxis1.items():
	xf1[each[0]] = float(each[1])
for each in xaxis2.items():
	xf2[each[0]] = float(each[1])
for each in yaxis.items():
	yf[each[0]] = float(each[1])

yf1 = OrderedDict()
yf2 = OrderedDict()
# print x
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')



# get related y with x
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
# reverse the order of x, y
xs1 = OrderedDict() # social xaxis
xs2 = OrderedDict() # search xaxis
ys1 = OrderedDict()
ys2 = OrderedDict()
for i in reversed(xf1.items()):
	xs1[i[0]] = i[1]
for i in reversed(xf2.items()):
	xs2[i[0]] = i[1]
for i in reversed(yf1.items()):
	ys1[i[0]] = i[1]
for i in reversed(yf2.items()):
	ys2[i[0]] = i[1]


# print xf2
# print len(ys1)
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
# for c, z in zip(['g', 'y'], [20, 10]):
#     xs = x
#     ys = y
#     # print xs 
#     # print ys
#     # print z 
#     # You can provide either a single color or an array. To demonstrate this,
#     # the first bar of each set will be colored cyan.
#     cs = [c] * len(xs)
#     cs[0] = 'c'
#     print cs
#     ax.bar(xs, ys, zs=z, zdir='y', color=cs, alpha=0.8)

# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Z')

# plt.show()
# pyplot.plot(x, y, 'ro')
# pyplot.show()
# plot(x,y)
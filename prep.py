import networkx as nx
from util import readEstabGraph
from geopy.distance import vincenty
import matplotlib.pylab as plt
import numpy as np

targets=['11101', '11215', '90047', '80221', '02145','83278']
labels=['Manhattan', 'Brooklyn', 'LA', 'Denver', 'Boston (Sommerville)','Stanley, ID']
maxKm=300


G=readEstabGraph('graph.gp', './pop/pop2015.tsv', './zbp/out2015.tsv')

totalP=0
totalB=0

for n in G:
    totalP+=G.node[n]['P']
    totalB+=G.node[n]['B']

totalR=totalB/totalP

data={}
for tz in targets:
    curP=0
    curB=0
    to_look=[tz,]
    used={}
    tcenter=(G.node[tz]['y'],G.node[tz]['x'])
    data[tz]={'x':[],'y':[]}
    while to_look:
        z=to_look.pop(0)
        if (z in used):
            continue            
        used[z]=True
        dist=vincenty(tcenter,(G.node[z]['y'],G.node[z]['x'])).km
        if (dist <= maxKm):
            curP+=G.node[z]['P']
            curB+=G.node[z]['B']
            data[tz]['x'].append(dist)
            data[tz]['y'].append(curB/curP)
            to_look.extend(G.neighbors(z))

plt.figure(1)
# plt.figure(2)
for i,tz in enumerate(targets):
    X=np.array(data[tz]['x'])
    Y=np.array(data[tz]['y'])
    inds=np.argsort(X)
    X=X[inds]
    Y=Y[inds]
    # plt.figure(2)
    # plt.plot(X,Y,label=labels[i]+' ('+tz+')')    
    plt.figure(1)
    plt.plot(X,Y/totalR,label=labels[i]+' ('+tz+')')

plt.legend()
plt.xlabel('Distance (km)')
plt.ylabel('Ratio / US Ratio')
plt.grid()
plt.show()

        






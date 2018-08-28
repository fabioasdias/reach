import networkx as nx
from util import readEstabGraph, getAllCodes, readNaicsGraph
import matplotlib.pylab as plt
import numpy as np
from geopy.distance import vincenty
import matplotlib
from numpy.linalg import norm
from multiprocessing import Pool

cmap = matplotlib.cm.get_cmap('viridis')


pop='./pop/pop2015.tsv'
zbp='./zbp/out2015.tsv'
graphName='graph.gp'



def plotDistances(G,D,pos,seed):
    colors=[D[seed][n] for n in G.nodes()]
    minC=np.min(colors)
    maxC=np.max(colors)
    colors=[cmap((c-minC)/(maxC-minC)) for c in colors]
    nx.draw(G,pos=pos, node_color=colors, node_size=10)


def calcForce(s,z,W):
    return(W[s]/(1E-9+D[s][z]**2))

def doThings(G,centre,others,W):
    D={}
    # DR={}
    # DR[centre]=0
    D[centre]=0
    todo=[centre,]
    while todo:
        z=todo.pop(0)
        for zz in G.neighbors(z):
            if (zz not in D) and (zz not in fasterSeeds):
                D[zz]=D[z]+1
                # DR[zz]=DR[z]+vincenty((G.node[zz]['y'],G.node[zz]['x']),(G.node[z]['y'],G.node[z]['x'])).km
                todo.append(zz)
    return(D)#,DR)

if __name__=='__main__':

    allNaics=getAllCodes(zbp,3)

    for naics in allNaics:
        G=readNaicsGraph(graphName,pop,zbp,naics)
        seeds=[]
        W={}
        for z in G.nodes():
            B=G.node[z]['B']
            if (B>0):
                seeds.append(z)
                W[z]=B
                # if (len(seeds)>9):
                #     break


        print(naics,'seeds',len(seeds))
        fasterSeeds={k:True for k in seeds}
        D={}
        for i,s in enumerate(seeds):
            D[s] = doThings(G,s,seeds,W) #,DR[s]

        
        s2id={k:i for i,k in enumerate(seeds)}
        with open('out_{0}.tsv'.format(naics),'w') as fout:
            for z in sorted(G.nodes()):
                cSW=[(s,calcForce(s,z,W)) for s in seeds if z in D[s]]
                cW=[x[1] for x in cSW]
                fout.write('\t'.join([z, cSW[np.argmax(cW/norm(cW))][0]])+'\n')

            
import networkx as nx
from util import readEstabGraph, getAllCodes, readNaicsGraph
import matplotlib.pylab as plt
import numpy as np
from geopy.distance import vincenty
import matplotlib
from numpy.linalg import norm
from multiprocessing import Pool
from os.path import exists

cmap = matplotlib.cm.get_cmap('tab20b')


pop='./pop/pop2015.tsv'
zbp='./zbp/out2015.tsv'
naicsNames='./naics2012.csv'
graphName='graph.gp'

nDigits=3



def plotDistances(G,D,pos,seed):
    colors=[D[seed][n] for n in G.nodes()]
    minC=np.min(colors)
    maxC=np.max(colors)
    colors=[cmap((c-minC)/(maxC-minC)) for c in colors]
    nx.draw(G,pos=pos, node_color=colors, node_size=10)


def calcForce(d:float,B:float):
    return(B/(d**2))

if __name__=='__main__':

    allNaics=getAllCodes(zbp,nDigits)

    nnames={}
    with open(naicsNames,'r') as fin:
        for line in fin:
            vals=[x.strip().replace('"','') for x in line.strip().split(',')]
            ncode=vals[0][:nDigits]
            if (ncode not in nnames):
                nnames[ncode]=vals[1]


    for naics in allNaics:
        # if (exists('./res/{0}.png'.format(naics))):
        #     continue
        G=readNaicsGraph(graphName,pop,zbp,naics)
        # G=nx.subgraph(G,[x for x in G.nodes() if (x[0]=='1') or (x[0]=='0') or (x[0]=='2')])
        pos={}
        seeds=[]
        W={}
        for z in G.nodes():
            B=G.node[z]['B']
            G.node[z]['s']=''
            G.node[z]['f']=0
            pos[z]=[G.node[z]['x'],G.node[z]['y']]
            if (B>0):
                seeds.append(z)
                W[z]=B

        print(naics,'seeds',len(seeds))
        for z in seeds:
            G.node[z]['D']=1
            G.node[z]['s']=z
            G.node[z]['f']=calcForce(G.node[z]['D'],W[G.node[z]['s']])

        todo=seeds[:]

        while todo:
            z=todo.pop(0)
            for n in G.neighbors(z):
                if (G.node[z]['s']!=G.node[n]['s']): #different clusters
                    maybeDist=G.node[z]['D']+vincenty((G.node[z]['y'],G.node[z]['x']),(G.node[n]['y'],G.node[n]['x'])).km
                    maybeForce=calcForce(maybeDist,W[G.node[z]['s']])
                    if (maybeForce>G.node[n]['f']):
                        G.node[n]['s']=G.node[z]['s']
                        G.node[n]['D']=maybeDist
                        G.node[n]['f']=maybeForce
                        todo.append(n)

        allNodes=sorted(G.nodes())

        sources=set([G.node[x]['s'] for x in G.nodes()])

        with open('./res/list_{0}.tsv'.format(naics),'w') as fout:
            for z in allNodes:
                fout.write('\t'.join([z, G.node[z]['s']])+'\n')


        # C={k:cmap(float(i)/len(sources)) for i,k in enumerate(sources)}

        # plt.figure()                
        # plt.title(nnames[naics])
        # for s in sources:
        #     ob=[x for x in G.nodes() if G.node[x]['s']==s]
        #     nx.draw(nx.subgraph(G,ob),pos=pos, node_size=10, node_color=[C[s],])
        #     nx.draw_networkx_nodes(nx.subgraph(G,[s,]),pos=pos,node_color='white', node_size=W[s]+4, node_shape='^')
        #     nx.draw_networkx_nodes(nx.subgraph(G,[s,]),pos=pos,node_color='r', node_size=W[s], node_shape='^')


        
        # plt.savefig('./res/{0}.png'.format(naics),dpi=900)
        # plt.close()

            
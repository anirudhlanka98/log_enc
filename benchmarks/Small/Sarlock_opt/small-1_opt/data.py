from __future__ import print_function
import glob
import numpy as np
from scipy.sparse import csr_matrix
import pickle as pkl
from collections import defaultdict
import itertools
import random
features1 = []
features2 = []
test_ind = []
i = 0
o = 1
visited = set()
types = {}
ntypes1 = {}
ntypes2 = {}
fanins = {}
nfanins = {}
outputs = []
noutputs = []
maps = {}
zgats = set()

def dfs(n, depth, visited):
    if depth == 0 or n in visited :
        return
    visited.add(n)
    for f in nfanins[n]:
        dfs(f,depth-1,visited)

for z in glob.glob("*.bench"):
    #print(o," : ",z)
    te = z[-10:]
    file = open(z, "r")
    for x in file.readlines() :
        f = []
        if 'INPUT' in x:
            y = x.replace("INPUT(", "").replace(")", "").replace("\n", "")
            if 'keyinput' in y:
                types.update({y:'keyinput'})
                if te == "test.bench":
                    ntypes1.update({i:'keyinput'})
                else:
                    ntypes2.update({i:'keyinput'})
            else:
                types.update({y:'input'})
                if te == "test.bench":
                    ntypes1.update({i:'input'})
                else:
                    ntypes2.update({i:'input'})
            fanins.update({y:[]})
            nfanins.update({i:[]})
            maps.update({y:i})
            i = i + 1

        elif 'OUTPUT' in x:
            y = x.replace("OUTPUT(", "").replace(")", "").replace("\n", "")
            outputs = outputs + [y]

        elif '=' in x:
            parts = [p.strip() for p in x.split('=')]
            if parts[1] != 'vdd':
                gate_name = parts[1][:parts[1].find('(')]
                types.update({parts[0]:gate_name})
                within_br = parts[1][parts[1].find('(')+1:parts[1].find(')')]
                f = [p.strip() for p in within_br.split(',')]
                fanins.update({parts[0]:f})
                maps.update({parts[0]:i})
                nf = []
                for x in f:
                    nf = nf + [maps[x]]
                if te == "test.bench":
                    ntypes1.update({i:gate_name})
                else:
                    ntypes2.update({i:gate_name})
                nfanins.update({i:nf})
            else:
                types.update({parts[0]:'vdd'})
                fanins.update({parts[0]:[]})
                maps.update({parts[0]:i})
                if te == "test.bench":
                    ntypes1.update({i:'vdd'})
                else:
                    ntypes2.update({i:'vdd'})
                nfanins.update({i:[]})
            i = i + 1

    if te != 'test.bench':
        zgats.add(maps['ZGAT'])
    for x in outputs:
        noutputs = noutputs + [maps[x]]
    o += 1

print(len(zgats))

for j in sorted(ntypes1.keys()):
    if ntypes1[j] == 'AND' or ntypes1[j] == 'and':
        features1.append([0,2,0,0,0,1])
    elif ntypes1[j] == 'NOT' or ntypes1[j] == 'not':
        features1.append([1,1,1,1,0,0])
    elif ntypes1[j] == 'INPUT' or ntypes1[j] == 'input':
        features1.append([2,0,0,0,1,1])
    elif ntypes1[j] == 'KEYINPUT' or ntypes1[j] == 'keyinput':
        features1.append([3,0,0,0,1,1])
    else:
        features1.append([4,0,0,0,0,0])

for j in sorted(ntypes2.keys()):
    if ntypes2[j] == 'AND' or ntypes2[j] == 'and':
        features2.append([0,2,0,0,0,1])
    elif ntypes2[j] == 'NOT' or ntypes2[j] == 'not':
        features2.append([1,1,1,1,0,0])
    elif ntypes2[j] == 'INPUT' or ntypes2[j] == 'input':
        features2.append([2,0,0,0,1,1])
    elif ntypes2[j] == 'KEYINPUT' or ntypes2[j] == 'keyinput':
        features2.append([3,0,0,0,1,1])
    else:
        features2.append([4,0,0,0,0,0])

labels1 = np.ndarray(shape=([len(ntypes1),2]),dtype=int)
labels2 = np.ndarray(shape=([len(ntypes2),2]),dtype=int)

for z in zgats:
    dfs(z,3,visited)
    visited.remove(z)

'''
for i, j in enumerate(sorted(ntypes1.keys())):
    if j in zgats: labels1[i] = [1,0]
    else: labels1[i] = [0,1]

for i, j in enumerate(sorted(ntypes2.keys())):
    if j in zgats: labels2[i] = [1,0]
    else: labels2[i] = [0,1]
'''

for i in range(ntypes1.keys()):
    labels1[i] = [0,0]

for i, j in enumerate(sorted(ntypes2.keys())):
    if j in zgats: labels2[i] = [1,0]
    elif j in visited: labels2[i] = [0,1]
    else: labels2[i] = [0,0]


feat1 = csr_matrix(features1)
feat2 = csr_matrix(features2)

feat_csr1 = csr_matrix.astype(feat1,np.float32)
feat_csr2 = csr_matrix.astype(feat2,np.float32)

x = open("ind.small-1.x","wt")
tx = open("ind.small-1.tx","wt")
allx = open("ind.small-1.allx","wt")
graf = open("ind.small-1.graph","wt")
y = open("ind.small-1.y","wt")
ty = open("ind.small-1.ty","wt")
ally = open("ind.small-1.ally","wt")

pkl.dump(labels2,y)
pkl.dump(labels2,ally)
pkl.dump(labels1,ty)
pkl.dump(feat_csr2,x)
pkl.dump(feat_csr2,allx)
pkl.dump(feat_csr1,tx)
pkl.dump(nfanins,graf)

x.close()
allx.close()
tx.close()
y.close()
ally.close()
ty.close()
graf.close()

with open('ind.small-1.test.index', 'wt') as f:
    for i in ntypes1:
        print ('%d' % i, file=f)


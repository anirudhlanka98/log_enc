from __future__ import print_function
import glob
import numpy as np
from scipy.sparse import csr_matrix
import pickle as pkl
from collections import defaultdict
import itertools
import random
import sys
import os.path

features1 = []
features2 = []
test_ind = set()
train = set()
test = set()
sel_train = set()
sel_test = set()
i = 0
o = 1
visited1 = set()
visited2 = set()
types = {}
ntypes1 = {}
ntypes2 = {}
nfanins = {}
gr = {}
noutputs1 = set()
noutputs2 = set()
zgats1 = set()
zgats2 = set()

def dfs(n, depth, visited):
    if depth == 0 or n in visited :
        return
    visited.add(n)
    for f in nfanins[n]:
        dfs(f,depth-1,visited)

for z in glob.glob(os.path.join(sys.argv[1], "*.bench")):
    print(o," : ",z)
    te = z[-10:]
    file = open(z, "r")
    fanins = {}
    maps = {}
    outputs1 = set()
    outputs2 = set()
    gen1 = []
    gen2 = []

    l = file.readlines()
    for x in l:
        f = []
        if 'INPUT' in x:
            y = x.replace("INPUT(", "").replace(")", "").replace("\n", "")
            if 'keyinput' in y:
                types[y] = 'keyinput'
                if te == "test.bench":
                    ntypes1[i] = 'keyinput'
                else:
                    ntypes2[i] = 'keyinput'
            else:
                types[y] = 'input'
                if te == "test.bench":
                    ntypes1[i] = 'input'
                else:
                    ntypes2[i] = 'input'
            fanins[y] = []
            nfanins[i] = []
            maps[y] = i
            i = i + 1

        elif 'OUTPUT' in x:
            y = x.replace("OUTPUT(", "").replace(")", "").replace("\n", "")
            if te == "test.bench":
                outputs1.add(y)
            else:
                outputs2.add(y)

        elif '=' in x:
            parts = [p.strip() for p in x.split('=')]
            if parts[1] != 'vdd':
                gate_name = parts[1][:parts[1].find('(')]
                types[parts[0]] = gate_name
                within_br = parts[1][parts[1].find('(')+1:parts[1].find(')')]
                f = [p.strip() for p in within_br.split(',')]
                fanins[parts[0]] = f
                maps[parts[0]] = i
                nf = []
                for x in f:
                    nf = nf + [maps[x]]
                if te == "test.bench":
                    ntypes1[i] = gate_name
                else:
                    ntypes2[i] = gate_name
                nfanins[i] = nf
            else:
                types[parts[0]] = 'vdd'
                fanins[parts[0]] = []
                maps[parts[0]] = i
                if te == "test.bench":
                    ntypes1[i] = 'vdd'
                else:
                    ntypes2[i] = 'vdd'
                nfanins[i] = []
            i = i + 1

    if te == "test.bench":
        zgats1.add(maps['ZGAT'])
    else:
        zgats2.add(maps['ZGAT'])

    for x in outputs1:
        noutputs1.add(maps[x])
        if x != 'ZGAT':
            gen1.append(maps[x])

    for x in outputs2:
        noutputs2.add(maps[x])
        if x != 'ZGAT':
            gen2.append(maps[x])

    if te == "test.bench":
        test.add(random.choice(gen1))
    else:
        train.add(random.choice(gen2))

    o += 1


for r in train:
    dfs(r,3,sel_train)

for r in test:
    dfs(r,3,sel_test)

for z in zgats1:
    dfs(z,3,visited1)
    visited1.remove(z)

for z in zgats2:
    dfs(z,3,visited2)
    visited2.remove(z)


for j in sorted(sel_test):
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

for j in sorted(visited1):
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

for j in sorted(zgats1):
    features1.append([0,2,0,0,0,1])

for j in sorted(sel_train):
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

for j in sorted(visited2):
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

for j in sorted(zgats2):
    features2.append([0,2,0,0,0,1])


labels1 = np.ndarray(shape=([len(sel_test)+len(visited1)+len(zgats1),3]),dtype=np.int32)
labels2 = np.ndarray(shape=([len(sel_train)+len(visited2)+len(zgats2),3]),dtype=np.int32)

k = 0
for i in sorted(sel_test):
    labels1[k] = [1,0,0]
    k += 1

for i in sorted(visited1):
    labels1[k] = [0,1,0]
    k += 1

for i in sorted(zgats1):
    labels1[k] = [0,0,1]
    k += 1


k = 0
for i in sorted(sel_train):
    labels2[k] = [1,0,0]
    k += 1

for i in sorted(visited2):
    labels2[k] = [0,1,0]
    k += 1

for i in sorted(zgats2):
    labels2[k] = [0,0,1]
    k += 1

sel_train.union(visited2)
sel_train.union(zgats2)

for i, j in enumerate(sel_train):
     gr[i] = nfanins[j]


feat1 = csr_matrix(features1)
feat_csr1 = csr_matrix.astype(feat1,np.float32)

feat2 = csr_matrix(features2)
feat_csr2 = csr_matrix.astype(feat2,np.float32)


x = open("ind.logdec.x","wb")
tx = open("ind.logdec.tx","wb")
allx = open("ind.logdec.allx","wb")
graf = open("ind.logdec.graph","wb")
y = open("ind.logdec.y","wb")
ty = open("ind.logdec.ty","wb")
ally = open("ind.logdec.ally","wb")


pkl.dump(labels2,y)
pkl.dump(labels2,ally)
pkl.dump(labels1,ty)
pkl.dump(feat_csr2,x)
pkl.dump(feat_csr2,allx)
pkl.dump(feat_csr1,tx)
pkl.dump(gr,graf)

print(len(labels2),len(labels2),len(labels1),feat_csr2.shape[0],feat_csr2.shape[0],feat_csr1.shape[0],len(gr))

x.close()
allx.close()
tx.close()
y.close()
ally.close()
ty.close()
graf.close()

sel_test.union(visited1)
sel_test.union(zgats1)

with open('ind.logdec.test.index', 'wt') as f:
    for i in sel_test:
        print ('%d' % i, file=f)

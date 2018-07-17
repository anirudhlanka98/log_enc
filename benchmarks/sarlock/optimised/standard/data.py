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

i = 0
ntypes  = {}
ntypes1 = {}
ntypes2 = {}
nfanins = {}
tag = {}
zgats = set()

def dfs(n, depth, visited):
    if n in visited :
        return
    visited.add(n)
    if depth == 0:
        return
    for f in nfanins[n]:
        dfs(f,depth-1,visited)

files = glob.glob(os.path.join(sys.argv[1], "*.bench"))
for cnt, filename in enumerate(files):
    print(cnt+1," : ",filename)
    is_test = filename.endswith('test.bench')
    file = open(filename, "r")

    fanins = {}
    maps = {}

    l = file.readlines()
    for x in l:
        f = []
        if 'INPUT' in x:
            y = x.replace("INPUT(", "").replace(")", "").replace("\n", "")
            if 'keyinput' in y:
                ntypes[i] = 'keyinput'
            else:
                ntypes[i] = 'input'
            fanins[y] = []
            nfanins[i] = []
            maps[y] = i
            tag[i] = 'test' if is_test else 'train'
            i = i + 1
        elif 'OUTPUT' in x:
            y = x.replace("OUTPUT(", "").replace(")", "").replace("\n", "")

        elif '=' in x:
            parts = [p.strip() for p in x.split('=')]
            if parts[1] != 'vdd':
                gate_name = parts[1][:parts[1].find('(')]
                within_br = parts[1][parts[1].find('(')+1:parts[1].find(')')]
                f = [p.strip() for p in within_br.split(',')]
                fanins[parts[0]] = f
                maps[parts[0]] = i
                nf = []
                for x in f:
                    nf = nf + [maps[x]]
                ntypes[i] = gate_name
                nfanins[i] = nf
            else:
                fanins[parts[0]] = []
                maps[parts[0]] = i
                ntypes[i] = 'vdd'
                nfanins[i] = []
            tag[i] = 'test' if is_test else 'train'
            i = i + 1

    zgats.add(maps['ZGAT'])

# Mark ZGAT and related nodes.
visited = set()
for z in zgats:
    dfs(z,3,visited)
    visited.remove(z)

features1, features2 = [], []
labels1, labels2 = [], []
c1, c2, c3 = 0, 0, 0

total_positive = float(len(visited) + len(zgats))
undersampling_ratio = total_positive / (float(len(ntypes)) - total_positive)

for i in ntypes.keys():
    if tag[i] == 'test':
        features, labels = features1, labels1
    else:
    #elif i in zgats or i in visited or random.random() < undersampling_ratio:
        features, labels = features2, labels2
    #else:
    #    continue
    
    if ntypes[i].upper() == 'AND':
        features.append([0,2,0,0,0,1])
    elif ntypes[i].upper() == 'NOT':
        features.append([1,1,1,1,0,0])
    elif ntypes[i].upper() == 'INPUT':
        features.append([2,0,0,0,1,1])
    elif ntypes[i].upper() == 'KEYINPUT':
        features.append([3,0,0,0,1,1])
    else:
        features.append([4,0,0,0,0,0])

    if i in zgats: 
        labels.append([1,0,0])
        c1 += 1
    elif i in visited: 
        labels.append([0,1,0])
        c2 += 1
    else: 
        labels.append([0,0,1])
        c3 += 1

def to_ndarray(l,dtype=int):
    assert len(l) > 0 and len(l[0]) > 0
    rows = len(l)
    cols = len(l[0])
    arr = np.ndarray(shape=(rows, cols), dtype=int)
    for i, row in enumerate(l):
        arr[i] = row
    return arr

labels1 = to_ndarray(labels1)
labels2 = to_ndarray(labels2)
feat_csr1 = csr_matrix.astype(csr_matrix(features1),np.float32)
feat_csr2 = csr_matrix.astype(csr_matrix(features2),np.float32)

x = open("ind.logdec.x","wt")
tx = open("ind.logdec.tx","wt")
allx = open("ind.logdec.allx","wt")
graf = open("ind.logdec.graph","wt")
y = open("ind.logdec.y","wt")
ty = open("ind.logdec.ty","wt")
ally = open("ind.logdec.ally","wt")

print(len(labels1), len(labels2),feat_csr1.shape,feat_csr2.shape)

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

with open('ind.logdec.test.index', 'wt') as f:
    for i in tag:
        if tag[i] == 'test':
            print ('%d' % i, file=f)


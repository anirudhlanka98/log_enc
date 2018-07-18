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

features_test, features_train, features_train_all = [], [], []
labels_test, labels_train, labels_train_all = [], [], []
indices = {}

total_positive = float(len(visited) + len(zgats))
undersampling_ratio =  ((total_positive) / (float(len(ntypes)) - total_positive))
print (len(zgats), len(visited), len(ntypes), undersampling_ratio)

incCnt, c1, c2, c3, c4 = 0, 0, 0, 0, 0
def to_one_hot(i, n):
    l = [0] * n
    l[i] = 1
    return l

for i in ntypes.keys():
    include = (i in zgats) or (i in visited) or (random.random() < undersampling_ratio)
    included_test = False
    if not include:
        c4 += 1
    elif tag[i] == 'test':
        incCnt += 1
        features, labels = features_test, labels_test
        included_test = True
    else:
        incCnt += 1
        features, labels = features_train, labels_train
    
    if ntypes[i].upper() == 'AND':
        #f = to_one_hot(0, 5) + to_one_hot(2, 3) + [0,0,0,1]
        f = [0,2,0,0,0,1]
        #f = [0,2]
    elif ntypes[i].upper() == 'NOT':
        #f = to_one_hot(1, 5) + to_one_hot(1, 3) + [1,1,0,0]
        f = [1,1,1,1,0,0]
        #f = [1,1]
    elif ntypes[i].upper() == 'INPUT':
        #f = to_one_hot(2, 5) + to_one_hot(0, 3) + [0,0,1,1]
        f = [2,0,0,0,1,1]
        #f = [2,0]
    elif ntypes[i].upper() == 'KEYINPUT':
        #f = to_one_hot(3, 5) + to_one_hot(0, 3) + [0,0,1,1]
        f = [3,0,0,0,1,1]
        #f = [3,0]
    else:
        #f = to_one_hot(4, 5) + to_one_hot(0, 3) + [0,0,0,0]
        f = [4,0,0,0,0,0]
        #f = [4,0]

    if i in zgats: 
        l = [1,0,0]
        if include and tag[i] == 'test':
            c1 += 1
    elif i in visited: 
        l = [0,1,0]
        if include and tag[i] == 'test':
            c2 += 1
    else: 
        l = [0,0,1]
        if include and tag[i] == 'test':
            c3 += 1

    if include:
        indices[i] = len(features)
        features.append(f)
        labels.append(l)
    elif not included_test:
        features_train_all.append(f)
        labels_train_all.append(l)


features_train_all = features_train + features_train_all
labels_train_all = labels_train + labels_train_all

print ("nodes: ", len(ntypes))
print ("counts:", c1, c2, c3, c4)

def to_ndarray(l,dtype=int):
    assert len(l) > 0 and len(l[0]) > 0
    rows = len(l)
    cols = len(l[0])
    arr = np.ndarray(shape=(rows, cols), dtype=int)
    for i, row in enumerate(l):
        arr[i] = row
    return arr

labels_test = to_ndarray(labels_test)
labels_train = to_ndarray(labels_train)
labels_train_all = to_ndarray(labels_train_all)
feat_csr_test = csr_matrix.astype(csr_matrix(features_test), np.float32)
feat_csr_train = csr_matrix.astype(csr_matrix(features_train), np.float32)
feat_csr_train_all = csr_matrix.astype(csr_matrix(features_train_all), np.float32)

f_x = open("ind.logdec.x","wb")
f_tx = open("ind.logdec.tx","wb")
f_allx = open("ind.logdec.allx","wb")
f_graf = open("ind.logdec.graph","wb")
f_y = open("ind.logdec.y","wb")
f_ty = open("ind.logdec.ty","wb")
f_ally = open("ind.logdec.ally","wb")

print ("label lengths (test, train, all, cnt):", len(labels_test), len(labels_train), len(labels_train_all), len(nfanins)),
print ("features size (test, train, all, cnt):", feat_csr_test.shape, feat_csr_train.shape, feat_csr_train_all.shape, len(nfanins))

pkl.dump(labels_train, f_y)
pkl.dump(labels_train_all, f_ally)
pkl.dump(labels_test, f_ty)
pkl.dump(feat_csr_train, f_x)
pkl.dump(feat_csr_train_all, f_allx)
pkl.dump(feat_csr_test, f_tx)
pkl.dump(nfanins, f_graf)

f_x.close()
f_allx.close()
f_tx.close()
f_y.close()
f_ally.close()
f_ty.close()
f_graf.close()

with open('ind.logdec.test.index', 'wt') as f:
    for i in tag:
        if i in indices and tag[i] == 'test':
            print ('%d' % indices[i], file=f)


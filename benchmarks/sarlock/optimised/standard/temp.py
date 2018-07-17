from __future__ import print_function
from collections import Counter
from sklearn.datasets import make_classification
from imblearn.under_sampling import RandomUnderSampler 
import glob
import numpy as np
from scipy.sparse import csr_matrix
import pickle as pkl
from collections import defaultdict
from imblearn.over_sampling import RandomOverSampler
import itertools
import random
import sys
import os.path

features1 = []
features2 = []
test_ind = []
i = 0
o = 1
visited = set()
types = {}
ntypes1 = {}
ntypes2 = {}
nfanins = {}
noutputs = set()
zgats = set()

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
    outputs = set()

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
            outputs.add(y)

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

    zgats.add(maps['ZGAT'])
    for x in outputs:
        noutputs.add(maps[x])
    o += 1


for j in sorted(ntypes1.keys()):
    if ntypes1[j] == 'AND' or ntypes1[j] == 'and':
        features1.append([j,0,2,0,0,0,1])
    elif ntypes1[j] == 'NOT' or ntypes1[j] == 'not':
        features1.append([j,1,1,1,1,0,0])
    elif ntypes1[j] == 'INPUT' or ntypes1[j] == 'input':
        features1.append([j,2,0,0,0,1,1])
    elif ntypes1[j] == 'KEYINPUT' or ntypes1[j] == 'keyinput':
        features1.append([j,3,0,0,0,1,1])
    else:
        features1.append([j,4,0,0,0,0,0])

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

for z in zgats:
    dfs(z,3,visited)
    visited.remove(z)

labels1p = []
labels2 = np.ndarray(shape=([len(ntypes2),3]),dtype=np.int32)

for i, j in enumerate(sorted(ntypes1.keys())):
    if j in zgats: labels1p.append(-1)
    elif j in visited: labels1p.append(1)
    else: labels1p.append(0)

for i, j in enumerate(sorted(ntypes2.keys())):
    if j in zgats: labels2[i] = [1,0,0]
    elif j in visited: labels2[i] = [0,1,0]
    else: labels2[i] = [0,0,1]

ros = RandomOverSampler(random_state=42)
x_resp, y_res = ros.fit_sample(features1, labels1p)

test_index = []
x_res = []

for i, j in enumerate(x_resp):
    test_index.append(j[0])
    x_res.append(j[1:])

feat1 = csr_matrix(x_res)
feat_csr1 = csr_matrix.astype(feat1,np.float32)

feat2 = csr_matrix(features2)
feat_csr2 = csr_matrix.astype(feat2,np.float32)

labels1 = np.ndarray(shape=([len(y_res),3]),dtype=np.int32)

print(len(x_res),len(y_res))
print(len(features1),len(labels1p))

for i, val in enumerate(y_res):
    if val == -1: labels1[i] = [1,0,0]
    elif val == 1: labels1[i] = [0,1,0]
    else: labels1[i] = [0,0,1]

print(labels1)

#print('Resampled dataset shape {}'.format(Counter(y_res)))

x = open("ind.logdec.x","wb")
tx = open("ind.logdec.tx","wb")
allx = open("ind.logdec.allx","wb")
graf = open("ind.logdec.graph","wb")
y = open("ind.logdec.y","wb")
ty = open("ind.logdec.ty","wb")
ally = open("ind.logdec.ally","wb")

print(len(labels2),len(labels2),len(labels1),feat_csr2.shape[0],feat_csr2.shape[0],feat_csr1.shape[0],len(nfanins))


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
    for i in test_index:
        print ('%d' % i, file=f)

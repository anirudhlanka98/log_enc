from __future__ import print_function
import glob
import numpy as np
from scipy.sparse import csr_matrix
import pickle as pkl
from collections import defaultdict
import itertools
import random
seen = []
features = []
test_ind = []
d = defaultdict(list)
i = 0

types = {}
ntypes = {}
fanins = {}
nfanins = {}
outputs = []
noutputs = []
maps = {}
zgats = set()


for z in glob.glob("*_keych.bench"):
    file = open(z, "r")
    for x in file.readlines() :
        f = []
        if 'INPUT' in x:
            y = x.replace("INPUT(", "").replace(")", "").replace("\n", "")
            if 'keyinput' in y:
                types.update({y:'keyinput'})
                ntypes.update({i:'keyinput'})
            else:
                types.update({y:'input'})
                ntypes.update({i:'input'})
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
                ntypes.update({i:gate_name})
                nfanins.update({i:nf})
            else:
                types.update({parts[0]:'vdd'})
                fanins.update({parts[0]:[]})
                maps.update({parts[0]:i})
                ntypes.update({i:'vdd'})
                nfanins.update({i:[]})
            i = i + 1

    zgats.add(maps['ZGAT'])
    for x in outputs:
        noutputs = noutputs + [maps[x]]

#for j in sorted(nfanins.keys()):
#    if ntypes[j] != 'input':
#        f = nfanins[j]
#        for x in f:
#            d[x] += [j]
#            d[j] += [x]

labels = []
for j in ntypes:
    if ntypes[j] == 'AND' or ntypes[j] == 'and':
        features.append([j] + [0,2,0,0,0,1])
    elif ntypes[j] == 'NOT' or ntypes[j] == 'not':
        features.append([j] + [1,1,1,1,0,0])
    elif ntypes[j] == 'INPUT' or ntypes[j] == 'input':
        features.append([j] + [2,0,0,0,1,1])
    elif ntypes[j] == 'KEYINPUT' or ntypes[j] == 'keyinput':
        features.append([j] + [3,0,0,0,1,1])
    else:
        features.append([j] + [4,0,0,0,0,0])

    if j in zgats: labels.append('AndTree')
    else: labels.append('Other')

    assert len(features[-1]) == 7

contents = []
for f, l in itertools.izip(features, labels):
    q = f + [l]
    contents.append(q)
    assert len(contents[-1]) == 8

random.shuffle(contents)
print (len(ntypes.keys()), len(ntypes), len(contents))

with open('logdec.content', 'wt') as f:
    for c in contents:
        line = '\t'.join(str(ci) for ci in c)
        print (line, file=f)

with open('logdec.edges', 'wt') as f:
    for e1 in nfanins.keys():
        fanins = nfanins[e1]
        assert len(fanins) <= 2
        for e2 in fanins:
            print ('%d %d' % (e2, e1), file=f)

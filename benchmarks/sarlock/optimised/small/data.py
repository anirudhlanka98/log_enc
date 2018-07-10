from __future__ import print_function
import glob
import numpy as np
from scipy.sparse import csr_matrix
import pickle as pkl
from collections import defaultdict
import itertools
import random
seen = []
features1 = []
features2 = []
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

	for x in outputs:
		noutputs = noutputs + [maps[x]]

def splitDict(d):
	all_keys = d.keys()
	random.shuffle(all_keys)
	n = int(len(d) * (0.2))
	d1, d2 = {}, {}
	for i, k in enumerate(all_keys):
		if i < n:
			d1[k] = d[k]
		else:
			d2[k] = d[k]
	return d1, d2

ntypes1, _ = splitDict(ntypes)
ntypes2 = ntypes


for j in sorted(nfanins.keys()):
			if ntypes[j] != 'input':
				f = nfanins[j]
				for x in f:
					d[x] += [int(j)]

for j in sorted(ntypes1.keys()):
	if ntypes1[j] == 'AND' or ntypes1[j] == 'and':
		features1.append([1,2,0,0,0,1])
	elif ntypes1[j] == 'NOT' or ntypes1[j] == 'not':
		features1.append([-1,1,1,1,0,0])
	elif ntypes1[j] == 'INPUT' or ntypes1[j] == 'input':
		features1.append([0,0,0,0,1,1])
	elif ntypes1[j] == 'KEYINPUT' or ntypes1[j] == 'keyinput':
		features1.append([2,0,0,0,1,1])

for j in sorted(ntypes2.keys()):
	if ntypes2[j] == 'AND' or ntypes2[j] == 'and':
		features2.append([1,2,0,0,0,1])
	elif ntypes2[j] == 'NOT' or ntypes2[j] == 'not':
		features2.append([-1,1,1,1,0,0])
	elif ntypes2[j] == 'INPUT' or ntypes2[j] == 'input':
		features2.append([0,0,0,0,1,1])
	elif ntypes2[j] == 'KEYINPUT' or ntypes2[j] == 'keyinput':
		features2.append([2,0,0,0,1,1])

labels1 = np.ndarray(shape=([len(ntypes1),2]),dtype=int)
labels2 = np.ndarray(shape=([len(ntypes2),2]),dtype=int)


for i, j in enumerate(sorted(ntypes1)):
	if maps['ZGAT']:
		labels1[i] = [1,0]
	else:
		labels1[i] = [0,1]


with open('ind.logdec.test.index', 'wt') as f:
    for i in ntypes1:
        print ('%d' % i, file=f)

for k, j in enumerate(sorted(ntypes2)):
	if maps['ZGAT']:
		labels2[k] = [1,0]
	else:
		labels2[k] = [0,1]


feat1 = csr_matrix(features1)
feat2 = csr_matrix(features2)

feat_csr1 = csr_matrix.astype(feat1,np.float32)
feat_csr2 = csr_matrix.astype(feat2,np.float32)

x = open("ind.logdec.x","wt")
tx = open("ind.logdec.tx","wt")
allx = open("ind.logdec.allx","wt")
graf = open("ind.logdec.graph","wt")
y = open("ind.logdec.y","wt")
ty = open("ind.logdec.ty","wt")
ally = open("ind.logdec.ally","wt")

pkl.dump(labels2,y)
pkl.dump(labels2,ally)
pkl.dump(labels1,ty)
pkl.dump(feat_csr2,x)
pkl.dump(feat_csr2,allx)
pkl.dump(feat_csr1,tx)
pkl.dump(d,graf)

x.close()
allx.close()
tx.close()
y.close()
ally.close()
ty.close()
graf.close()


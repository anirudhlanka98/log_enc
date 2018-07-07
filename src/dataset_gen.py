import glob
import numpy as np
from scipy.sparse import csr_matrix
import pickle as pkl
from collections import defaultdict
seen = []
features = []
labels = []
d = defaultdict(list)
i = 0

for z in glob.glob("*.bench"):
	if z not in seen:
		file = open(z, "r")
		types = {}
		ntypes = {}
		fanins = {}
		nfanins = {}
		outputs = []
		noutputs = []
		maps = {}
		f = []

		for x in file.readlines() :
		    
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
		    	i = i + 1

		for x in outputs:
			noutputs = noutputs + [maps[x]]

	seen += [z]


for j in sorted(nfanins.keys()):
			if ntypes[j] != 'input':
				f = nfanins[j]
				for x in f:
					d[x] += [int(j)]

for j in sorted(ntypes.keys()):
	if ntypes[j] == 'AND' or ntypes[j] == 'and':
		features.append([1,2,0,0,0,1])
	elif ntypes[j] == 'NOT' or ntypes[j] == 'not':
		features.append([-1,1,1,1,0,0])
	elif ntypes[j] == 'INPUT' or ntypes[j] == 'input':
		features.append([0,0,0,0,1,1])
	elif ntypes[j] == 'KEYINPUT' or ntypes[j] == 'keyinput':
		features.append([2,0,0,0,1,1])

labels = np.ndarray([len(ntypes),2])

for j in sorted(ntypes):
	if maps['ZGAT']:
		labels[j] = [1,0]
	else:
		labels[j] = [0,1]

feat_csr = csr_matrix(features)

x = open("ind.logdec.x","wb")
allx = open("ind.logdec.allx","wb")
graf = open("ind.logdec.graph","wb")
y = open("ind.logdec.y","wb")
ally = open("ind.logdec.ally","wb")

pkl.dump(labels,y)
pkl.dump(labels,ally)
pkl.dump(feat_csr,x)
pkl.dump(feat_csr,allx)
pkl.dump(d,graf)

x.close()
allx.close()
graf.close()
y.close()
ally.close()



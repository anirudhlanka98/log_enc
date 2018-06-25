import random
import sys
from log_desc import *

fname = sys.argv[1]
types, fanins, input_values, outputs, seq = readfile(fname)

lk = []
k = 0
y = []
key = []
lis = []

ran_gat = random.sample(types.keys(),random.randint(1,len(types)))

for i in ran_gat:
	y = fanins[i]
	t = types[i]
	kgat = 'enc'+str(k)
	kin = 'keyinput'+str(k)
	types.update({kin:'keyinput'})
	fanins.update({kgat:y})
	del fanins[i]
	fanins.update({i:[kgat,kin]})
	if random.randint(0,1) :
		types.update({i:'xor'})
		types.update({kgat:t})
		key = key + [0]
	else :
		types.update({i:'xnor'})
		types.update({kgat:t})
		key = key + [1]

	if t == 'input':
		ind = seq.keys()[seq.values().index(i)]
		seq[ind] = kgat
	
	k = k + 1

f = open("smallenc.bench","w+")

for i in sorted(seq.keys()):
	f.write("INPUT(%s)\n"%seq[i])


for i in range(len(key)):
	f.write("INPUT(keyinput%d)\n"%i)	

for i in outputs:
	f.write("OUTPUTS(%s)\n"%i)

for i in fanins:
	if types[i] != 'input':
		f.write("%s = %s("%(i,types[i]))
		z = ''
		for i in fanins[i]:
			z = z + i + ', '
		z = z[:-2]
		f.write(z)
		f.write(")\n")

'''print 'Random gates: ', ran_gat, '\n'
print 'Types: ', types, '\n'
print 'Fanins', fanins, '\n'
print 'Keys: ', key
'''
import random
import sys
from natsort import natsorted, ns
import os
from log_desc import *

fname = sys.argv[1]
types, fanins, input_values, outputs, seq = readfile(fname)

r = random.choice(outputs)

new_r = r + 'new'

types[new_r] = types.pop(r)
fanins[new_r] = fanins.pop(r)

new_inp = []
key_inp = []
slis = []
k = 0

for i in natsorted(types.keys(), alg=ns.IGNORECASE):
	if types[i] == 'input':
		if random.randint(0,1):
			new_inp = new_inp + [i]
			key_inp = key_inp + [1]
		else:
			neg = i + 'bar'
			types.update({neg:'NOT'})
			fanins.update({neg:[i]})
			new_inp = new_inp + [neg]
			key_inp = key_inp + [0]

		s = 'SGAT'+str(k)
		slis = slis + [s]
		key = 'keyinput'+str(k)
		types.update({s:'xnor'})
		fanins.update({s:[i,key]})
		k = k + 1
		
types.update({'ZGAT':'AND'})
fanins.update({'ZGAT':new_inp})

types.update({'XGAT':'AND'})
fanins.update({'XGAT':slis})


types.update({'UGAT':'XOR'})
fanins.update({'UGAT':[new_r,'ZGAT']})

types.update({r:'XOR'})
fanins.update({r:['UGAT','XGAT']})

def get_nonexistant_path(fname_path):
	    if not os.path.exists(fname_path):
	        return fname_path
	    filename, file_extension = os.path.splitext(fname_path)
	    i = 1
	    new_fname = "{}_enc-{}{}".format(filename, i, file_extension)
	    while os.path.exists(new_fname):
	        i += 1
	        new_fname = "{}_enc-{}{}".format(filename, i, file_extension)
	    return new_fname

encname = get_nonexistant_path(fname)

f = open(encname,"w+")

f.write("#Key = ")
for i in key_inp:
	f.write("%s"%i)
f.write("\n\n")

for i in sorted(seq.keys()):
	f.write("INPUT(%s)\n"%seq[i])

f.write("\n")

for i in range(len(key_inp)):
	f.write("INPUT(keyinput%d)\n"%i)	

f.write("\n")

for i in outputs:
	f.write("OUTPUT(%s)\n"%i)

f.write("OUTPUT(ZGAT)\n")
f.write("\n")

for i in fanins:
	if types[i] != 'input':
		f.write("%s = %s("%(i,types[i].upper()))
		z = ''
		for i in fanins[i]:
			z = z + i + ', '
		z = z[:-2]
		f.write(z)
		f.write(")\n")


import random
from log_desc import *

fname = raw_input("Enter the bench file name with extension: ")
types, fanins, input_values, outputs = readfile(fname)

lk = []
k = 0
y = []
key = []

ran_gat = random.sample(types.keys(),random.randint(1,len(types)))

for i in ran_gat:
	y = fanins[i]
	kgat = 'enc'+str(k)
	kin = 'keyinput'+str(k)
	types.update({kin:'input'})
	fanins.update({kgat:y})
	del fanins[i]
	fanins.update({i:[kgat,kin]})
	if random.randint(0,1) :
		types.update({i:'xor'})
		types.update({kgat:'input'})
		key = key + [0]
	else :
		types.update({i:'xnor'})
		types.update({kgat:'input'})
		key = key + [1]
	k = k + 1

f = open("smallenc.bench","w+")

for i in types:
	if types[i] == 'input':
		f.write("INPUT(%s)\n"%i)

for i in outputs:
	f.write("OUTPUTS(%s)\n"%i)

for i in fanins:
	if types[i] != 'input':
		f.write("%s=%s("%(i,types[i]))
		z = ''
		for i in fanins[i]:
			z = z + i + ','
		z = z[:-1]
		print z
		f.write(z)
		f.write(")\n")

print 'Random gates: ', ran_gat, '\n'
print 'Types: ', types, '\n'
print 'Fanins', fanins, '\n'
print 'Keys: ', key

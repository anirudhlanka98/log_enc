import random
import os
import sys

types = {}
fanins = {}
outputs = []

lk = ['AND','OR','NOT','NAND','NOR','XOR','XNOR']
n_str = sys.argv[1]
n = int(n_str)
n_in = int(0.25 * n)
n_op = n - int(0.15 * n)

for i in range(n_in):
	types.update({i:'INPUT'})

k = n_in
while k <= n:
	x = random.choice(lk)
	if x == 'NOT':
		f = random.choice(types.keys())
		fanins.update({k:f})
	else:
		f = random.sample(types.keys(),2)
		fanins.update({k:f})
	types.update({k:x})
	k = k + 1

for i in range(n_op,n):
	outputs = outputs + [i]

fname = 'c' + n_str + '.bench'

f = open(fname,"w+")

for i in sorted(types.keys()):
	if types[i] == 'INPUT':
		f.write("INPUT(%s)\n"%i)

f.write("\n")

for i in outputs:
	f.write("OUTPUT(%s)\n"%i)

f.write("\n")

for i in fanins:
	if types[i] != 'INPUT' and types[i] != 'NOT':
		f.write("%s = %s("%(i,types[i]))
		z = ''
		for i in fanins[i]:
			z = z + str(i) + ', '
		z = z[:-2]
		f.write(z)
		f.write(")\n")

	if types[i] == 'NOT':
		f.write("%s = %s("%(i,types[i]))
		f.write(str(fanins[i]))
		f.write(")\n")

f.write("\n")



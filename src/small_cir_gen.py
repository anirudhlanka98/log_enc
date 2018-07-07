import random
import os
import sys

w = int(sys.argv[1])
m = 0
while m < w :
	types = {}
	fanins = {}
	outputs = []

	lk = ['AND','OR','NOT','NAND','NOR','XOR','XNOR']
	s = "Enter the number of gates for circuit ",m,": "
	n_str = input(s)
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

	def get_nonexistant_path(fname_path):
	    if not os.path.exists(fname_path):
	        return fname_path
	    filename, file_extension = os.path.splitext(fname_path)
	    i = 1
	    new_fname = "{}-{}{}".format(filename, i, file_extension)
	    while os.path.exists(new_fname):
	        i += 1
	        new_fname = "{}-{}{}".format(filename, i, file_extension)
	    return new_fname

	fname = get_nonexistant_path("small.bench")

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

	m = m + 1



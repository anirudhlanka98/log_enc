import random
from temp2 import *

types, fanins, input_values, outputs = readfile("small.bench")

lk = []
z = []
k = 0
y = []
key = []

ran_gat = random.sample(types.keys(),random.randint(1,len(types)))
print(ran_gat)
print(fanins)
for x in range(1,20):
	lk = lk + [random.randint(0,1)]

for i in ran_gat:
	y = fanins[i]
	z = 'enc'+str(k)
	fanins.update({z:y})
	del fanins[i]
	fanins.update({i:[z,e_k]})
	types.update({e_k:'input'})
	if lk[x] == 0 :
		types.update({z:'xor'})
		key = key + [0]
	else :
		types.update({z:'xnor'})
		key = key + [1]
	k = k + 1

print('types: ',types)
print('outputs: ',outputs)
print(key)

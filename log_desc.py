def readfile(filename):
	file = open(filename, "r")
	types = {}
	fanins = {}
	outputs = []
	_input_values = {}
	f = []
	i = 0

	for x in file.readlines() :
	    
	    if 'INPUT' in x:
			y = x.replace("INPUT(", "").replace(")", "").replace("\n", "")
			types.update({y:'input'})
			_input_values.update({y:_inp[i]})
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
	return types, fanins, _input_values, outputs

if __name__ == "__main__":
	def simulate(types, fanins, input_values, n):
		if(types[n] == 'input'):
			return _input_values[n]

		elif(types[n] == 'and'):
			f = fanins[n]
			res = []
			for i in range(len(f)):
				res.append(simulate(types, fanins, _input_values, f[i]))
			return all(res)

		elif(types[n] == 'or'):
			f = fanins[n]
			res = []
			for i in range(len(f)):
				res.append(simulate(types, fanins, _input_values, f[i]))
			return any(res)

		elif(types[n] == 'not'):
			return not(simulate(types, fanins, _input_values, fanins[n][0]))

		elif(types[n] == 'nand'):
			f = fanins[n]
			res = []
			for i in range(len(f)):
				res.append(simulate(types, fanins, _input_values, f[i]))
			return not(all((res)))

		elif(types[n] == 'nor'):
			f = fanins[n]
			res = []
			for i in range(len(f)):
				res.append(simulate(types, fanins, _input_values, f[i]))
			return not(any((res)))

		elif(types[n] == 'xor'):
			f = fanins[n]
			return reduce(lambda i, j: simulate(types, fanins, _input_values, i) ^ simulate(types, fanins, _input_values, j), f)

		elif(types[n] == 'xnor'):
			f = fanins[n]
			return not(reduce(lambda i, j: simulate(types, fanins, _input_values, i) ^ simulate(types, fanins, _input_values, j), f))
	
	_fil = raw_input("Enter the bench file name with extension: ")
	_z = raw_input('Enter the input values: ')
	_inp = []

	for i in range(len(_z)):
		_inp = _inp + [int(_z[i])]

	types, fanins, _input_values, outputs = readfile(_fil)

	for i in range(len(outputs)):
		print(outputs[i]+' = '+str(simulate(types, fanins, _input_values, outputs[i]))+'\n')
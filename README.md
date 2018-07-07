# logic_encryption

All circuit specificaions are mentioned in .bench format and are available in benchmarks directory.

log_desc.py is used to logically represent and simulate a circuit.

ran_enc.py is used to encrypt the given circuit by randomly adding intermediate xor and xnor gates. It creates a new bench file of the encrypted circuit with the name <original_circuit_enc.bench> 
The format to run is: python ran_enc.py <name_of_circuit.bench>

sar_enc.py is used to encrypt the given circuit using SARLock methodology. It creates a new bench file of the encrypted circuit with the name <original_circuit_sar_enc.bench>
The format to run is: python sar_enc.py <name_of_circuit.bench>

cir_gen.py is used to generate circuits. It creates a new bench file with the name <c"no_of_nodes".bench>
The format to run is: python cir_gen.py <no_of_nodes>

small_cir_gen.py is used to generate multiple small circuits. It creates a new bench file with the name <small-"i".bench> where i increments based on the existency of the file with the same name in the same directory.
The format to run is: python cir_gen.py <no_of_circuits>

dataset_gen.py takes in all the bench files in the directory and generates a dataset used for training a Graph Convolution Network.

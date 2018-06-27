# logic_encryption

All circuit specificaions are mentioned in .bench format and are available in benchmarks directory.

log_desc.py is used to logically represent and simulate a circuit.

ran_enc.py is used to encrypt the given circuit by randomly adding intermediate xor and xnor gates. It creates a new bench file of the encrypted circuit with the name <original_circuit_enc.bench> 
The format to run is: python ran_enc.py <name_of_circuit.bench>

sar_enc.py is used to encrypt the given circuit using SARLock methodology. It creates a new bench file of the encrypted circuit with the name <original_circuit_sar_enc.bench>
The format to run is: python sar_enc.py <name_of_circuit.bench>

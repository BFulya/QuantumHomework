from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator

qc = QuantumCircuit(2)   # QuantumCircuit: create circuit
qc.h(0)
qc.cx(0, 1)

sv = Statevector.from_instruction(qc)  # Statevector
print(sv.probabilities_dict())

qc.measure_all()
result = AerSimulator().run(qc, shots=1000).result()
print(result.get_counts())              # AerSimulator
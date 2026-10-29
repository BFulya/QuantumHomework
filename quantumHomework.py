
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# 1. Create Quantum Circuit
qc = QuantumCircuit(1)

# 2.Apply the Hadamard gate
qc.h(0)

# 3.Calculate the State Vector
state = Statevector.from_instruction(qc)

print("Quantum Circuit:")
print(qc.draw("text"))

print("\nState Vector:")
print(state.data)

# 4. Add Measurement
qc.measure_all()

# 5. Run Simulator
simulator = AerSimulator()
result = simulator.run(qc, shots=1000).result()

counts = result.get_counts()

print("\nMeasurement Results:")
print(counts)

# 6. Create Histogram
plot_histogram(counts)
plt.title("Hadamard Gate - Measurement Results")
plt.show()


from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# Create a two-qubit quantum circuit
qc = QuantumCircuit(2)

# Apply the Hadamard gate to create superposition
qc.h(0)

# Create entanglement
qc.cx(0, 1)

# Calculate the State Vector
state = Statevector.from_instruction(qc)

print("Bell Circuit:")
print(qc.draw("text"))

print("\nState Vector:")
print(state.data)

# Add measurement
qc.measure_all()

# Run the simulation
simulator = AerSimulator()
result = simulator.run(qc, shots=1000).result()

counts = result.get_counts()
print("\nMeasurement Results:")
print(counts)

# Histogram
plot_histogram(counts)
plt.title("Bell State - Measurement Results")
plt.show()

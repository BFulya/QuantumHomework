
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# Create a three-qubit quantum circuit
qc = QuantumCircuit(3)

# Apply Hadamard gate to the first qubit
qc.h(0)

# Apply CNOT gates to create GHZ entanglement
qc.cx(0, 1)
qc.cx(1, 2)

# Calculate the state vector
state = Statevector.from_instruction(qc)

print("GHZ Quantum Circuit:")
print(qc.draw("text"))

print("\nState Vector:")
print(state.data)

print("\nTheoretical Probabilities:")
print(state.probabilities_dict())

# Add measurement operations
qc.measure_all()

# Initialize the simulator
simulator = AerSimulator()

# Run the simulation with 1000 shots
result = simulator.run(qc, shots=1000).result()

# Retrieve measurement results
counts = result.get_counts()

print("\nMeasurement Results:")
print(counts)

# Plot measurement histogram
plot_histogram(counts)
plt.title("GHZ State - Measurement Results")
plt.xlabel("Quantum States")
plt.ylabel("Measurement Counts")
plt.show()

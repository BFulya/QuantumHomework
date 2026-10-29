
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, Operator

# Single-qubit quantum gates
single_gates = ["x", "y", "z", "h", "rx", "ry", "rz"]

for gate in single_gates:
    qc = QuantumCircuit(1)

    # Apply the selected gate
    if gate in ["rx", "ry", "rz"]:
        getattr(qc, gate)(np.pi / 2, 0)
    else:
        getattr(qc, gate)(0)

    # Calculate matrix and output state
    matrix = Operator(qc).data
    state = Statevector.from_instruction(qc)

    print("\n" + "=" * 50)
    print("Quantum Gate:", gate.upper())

    print("\nMatrix Representation:")
    print(np.round(matrix, 4))

    print("\nQuantum Circuit:")
    print(qc.draw("text"))

    print("\nInput State: |0>")
    print("Output State:")
    print(np.round(state.data, 4))


# CNOT gate - Demonstrating controlled operation
qc = QuantumCircuit(2)

# Set control qubit to |1>
qc.x(0)

# Apply CNOT gate
qc.cx(0, 1)

print("\n" + "=" * 50)
print("Quantum Gate: CNOT - Active Control")

print("\nQuantum Circuit:")
print(qc.draw("text"))

print("\nInput State: |01>")
print("Output State:")
print(Statevector.from_instruction(qc).data)

print("\nExpected Output: |11>")



# Pauli-Z gate - Phase flip demonstration
qc = QuantumCircuit(1)

# Prepare |+> state
qc.h(0)

input_state = Statevector.from_instruction(qc)

# Apply Pauli-Z gate
qc.z(0)

output_state = Statevector.from_instruction(qc)

print("\n" + "=" * 50)
print("Pauli-Z Phase Flip Demonstration")

print("\nInput State |+>:")
print(np.round(input_state.data, 4))

print("\nQuantum Circuit:")
print(qc.draw("text"))

print("\nOutput State |->:")
print(np.round(output_state.data, 4))

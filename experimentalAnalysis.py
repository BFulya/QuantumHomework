
import os
import csv
import numpy as np
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error

# Create output directory
OUTPUT_DIR = "experiment_results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Reproducible simulation settings
SEED = 42
SHOTS_LIST = [100, 500, 1000, 5000, 10000]


# Create quantum circuits without measurements
def create_circuit(name):
    if name == "Hadamard":
        qc = QuantumCircuit(1)
        qc.h(0)

    elif name == "Bell":
        qc = QuantumCircuit(2)
        qc.h(0)
        qc.cx(0, 1)

    elif name == "GHZ":
        qc = QuantumCircuit(3)
        qc.h(0)
        qc.cx(0, 1)
        qc.cx(1, 2)

    else:
        raise ValueError("Unknown circuit")

    return qc


# Run a circuit with measurements
def run_simulation(qc, shots, simulator, seed=SEED):
    measured = qc.copy()
    measured.measure_all()

    result = simulator.run(
        measured,
        shots=shots,
        seed_simulator=seed
    ).result()

    return result.get_counts()


# Calculate probabilities and mean absolute error
def analyze_counts(counts, theoretical, shots):
    states = sorted(theoretical.keys())

    probabilities = {
        state: counts.get(state, 0) / shots
        for state in states
    }

    mae = np.mean([
        abs(probabilities[state] - theoretical[state])
        for state in states
    ])

    return probabilities, mae


# Experiment 1: Theory vs simulation
def experiment_theory():
    print("\nEXPERIMENT 1: THEORY VS SIMULATION")

    simulator = AerSimulator()
    rows = []

    for name in ["Hadamard", "Bell", "GHZ"]:
        qc = create_circuit(name)

        theoretical = Statevector.from_instruction(
            qc
        ).probabilities_dict()

        # Include all computational basis states
        n = qc.num_qubits
        theoretical = {
            format(i, f"0{n}b"): float(
                theoretical.get(format(i, f"0{n}b"), 0)
            )
            for i in range(2 ** n)
        }

        counts = run_simulation(qc, 1000, simulator)

        probabilities, mae = analyze_counts(
            counts, theoretical, 1000
        )

        print(f"\n{name} Circuit")
        print("Theoretical:", theoretical)
        print("Measured:", counts)
        print("MAE:", round(mae, 5))

        states = list(theoretical.keys())
        x = np.arange(len(states))

        plt.figure(figsize=(9, 5))
        plt.bar(
            x - 0.2,
            [theoretical[s] for s in states],
            width=0.4,
            label="Theoretical"
        )
        plt.bar(
            x + 0.2,
            [probabilities[s] for s in states],
            width=0.4,
            label="Simulation"
        )

        plt.xticks(x, states)
        plt.ylim(0, 0.65)
        plt.ylabel("Probability")
        plt.xlabel("Quantum State")
        plt.title(f"{name}: Theory vs Simulation")
        plt.legend()
        plt.tight_layout()

        plt.savefig(
            f"{OUTPUT_DIR}/{name.lower()}_comparison.png",
            dpi=200
        )
        plt.close()

        for state in states:
            rows.append([
                name,
                state,
                theoretical[state],
                probabilities[state],
                abs(theoretical[state] - probabilities[state])
            ])

    with open(
        f"{OUTPUT_DIR}/theory_comparison.csv",
        "w",
        newline=""
    ) as file:
        writer = csv.writer(file)
        writer.writerow([
            "Circuit", "State", "Theoretical",
            "Experimental", "Absolute Error"
        ])
        writer.writerows(rows)


# Experiment 2: Effect of shots
def experiment_shots():
    print("\nEXPERIMENT 2: EFFECT OF SHOTS")

    simulator = AerSimulator()
    qc = create_circuit("Hadamard")

    results = []
    errors = []

    for shots in SHOTS_LIST:
        counts = run_simulation(qc, shots, simulator)

        p0 = counts.get("0", 0) / shots
        p1 = counts.get("1", 0) / shots

        mae = (abs(p0 - 0.5) + abs(p1 - 0.5)) / 2

        results.append([shots, p0, p1, mae])
        errors.append(mae)

        print(
            f"Shots: {shots}, "
            f"P(0): {p0:.4f}, "
            f"P(1): {p1:.4f}, "
            f"MAE: {mae:.4f}"
        )

    plt.figure(figsize=(9, 5))
    plt.plot(
        SHOTS_LIST,
        [row[1] for row in results],
        marker="o",
        label="Measured P(0)"
    )
    plt.plot(
        SHOTS_LIST,
        [row[2] for row in results],
        marker="s",
        label="Measured P(1)"
    )

    plt.axhline(
        y=0.5,
        linestyle="--",
        color="black",
        label="Theoretical Probability"
    )

    plt.xscale("log")
    plt.ylim(0.35, 0.65)
    plt.xlabel("Number of Shots")
    plt.ylabel("Probability")
    plt.title("Effect of Measurement Shots")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()

    plt.savefig(
        f"{OUTPUT_DIR}/shots_comparison.png",
        dpi=200
    )
    plt.close()

    with open(
        f"{OUTPUT_DIR}/shots_analysis.csv",
        "w",
        newline=""
    ) as file:
        writer = csv.writer(file)
        writer.writerow(["Shots", "P0", "P1", "MAE"])
        writer.writerows(results)


# Experiment 3: Ideal vs noisy simulation
def experiment_noise():
    print("\nEXPERIMENT 3: IDEAL VS NOISY")

    qc = create_circuit("Bell")
    shots = 10000

    ideal_simulator = AerSimulator()

    # Define a simple depolarizing noise model
    noise_model = NoiseModel()

    error_1q = depolarizing_error(0.02, 1)
    error_2q = depolarizing_error(0.10, 2)

    noise_model.add_all_qubit_quantum_error(
        error_1q, ["h"]
    )
    noise_model.add_all_qubit_quantum_error(
        error_2q, ["cx"]
    )

    noisy_simulator = AerSimulator(
        noise_model=noise_model
    )

    ideal_counts = run_simulation(
        qc, shots, ideal_simulator
    )

    noisy_counts = run_simulation(
        qc, shots, noisy_simulator
    )

    print("Ideal Results:", ideal_counts)
    print("Noisy Results:", noisy_counts)

    states = ["00", "01", "10", "11"]

    ideal_probs = [
        ideal_counts.get(s, 0) / shots for s in states
    ]
    noisy_probs = [
        noisy_counts.get(s, 0) / shots for s in states
    ]

    x = np.arange(len(states))

    plt.figure(figsize=(9, 5))
    plt.bar(
        x - 0.2, ideal_probs,
        width=0.4, label="Ideal"
    )
    plt.bar(
        x + 0.2, noisy_probs,
        width=0.4, label="Noisy"
    )

    plt.xticks(x, states)
    plt.xlabel("Quantum State")
    plt.ylabel("Probability")
    plt.title("Bell State: Ideal vs Noisy Simulation")
    plt.legend()
    plt.tight_layout()

    plt.savefig(
        f"{OUTPUT_DIR}/noise_comparison.png",
        dpi=200
    )
    plt.close()

    with open(
        f"{OUTPUT_DIR}/noise_analysis.csv",
        "w",
        newline=""
    ) as file:
        writer = csv.writer(file)
        writer.writerow([
            "State", "Ideal Probability", "Noisy Probability"
        ])
        for i, state in enumerate(states):
            writer.writerow([
                state, ideal_probs[i], noisy_probs[i]
            ])


# Main execution
if __name__ == "__main__":
    experiment_theory()
    experiment_shots()
    experiment_noise()

    print("\nAll experiments completed successfully.")
    print("Results saved in:", OUTPUT_DIR)

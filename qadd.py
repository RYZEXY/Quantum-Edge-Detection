from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.circuit.library import QFTGate  
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import Sampler as AerSampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import numpy as np
from qiskit.circuit.library.basis_change import QFT


def qft_adder(x, y, c):
    adder = QuantumCircuit(x,y,c, name = "Add")
    num_bits = len(x)

    # QFT on y
    adder.append(QFT(num_bits+1, do_swaps=False).to_gate(), list(y) + [c[0]])
    
    for i in range(num_bits):
        for j in range(i + 1):
            angle = np.pi / (2 ** (i - j))
            adder.cp(angle, x[j], y[i])

    for j in range(num_bits):
        angle = np.pi / (2 ** (num_bits - j))
        adder.cp(angle, x[j], c[0])

    # Inverse QFT on y
    adder.append(QFT(num_bits+1, do_swaps=False, inverse=True).to_gate(), list(y) + [c[0]])


    adder = adder.to_gate()
    return adder


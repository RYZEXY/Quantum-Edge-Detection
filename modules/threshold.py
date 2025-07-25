from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.circuit.library import QFTGate  
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import Sampler as AerSampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import numpy as np
from qiskit.circuit.library.basis_change import QFT
from qiskit.circuit.library import GroverOperator, MCMT, ZGate
from modules.enhanced_grover import filter_oracle

def threshold(oracle, sign, grad, ancillary, threshold):
    qc = QuantumCircuit(grad, sign, ancillary, oracle, name = 'Threshold')
    og = filter_oracle(threshold)  
    cog = og.control(2, label="Og")
    qc.x(ancillary)
    qc.h(oracle)

    qc.append(cog, list(oracle) + list(sign) + list(grad))
    qc.append(cog, list(oracle) + list(sign) + list(grad))

    qc.h(oracle)

    return qc

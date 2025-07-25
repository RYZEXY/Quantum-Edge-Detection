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

def copy(src, dest):
    qc = QuantumCircuit(src, dest, name='Copy')
    for src, dest in zip(src,dest):
        qc.cx(src, dest)

    return qc

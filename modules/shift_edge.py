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
from modules.ladder import ladder_up

def shift_edge(pos,sign,a):
    qc = QuantumCircuit(pos, sign, a, name = 'Shift')
    
    qc.cx(sign,a)
    qc.ch(a,sign) 

    ladder_control = ladder_up(pos).control(1,label="cladder")


    qc.append(ladder_control, list(sign) + list(pos))

    return qc


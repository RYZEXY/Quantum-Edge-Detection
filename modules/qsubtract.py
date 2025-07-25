from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.circuit.library import QFTGate  
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import Sampler as AerSampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import numpy as np
from qiskit.circuit.library.basis_change import QFT
from modules.qadd import qft_adder

def multi_x_gate(num_targets, num_ctrl):
    qc = QuantumCircuit(num_targets, name="X")
    for i in range(num_targets):
        qc.x(i)
    return qc.to_gate().control(num_ctrl)

def s2c(x,y,c):
    num_bits = len(x)

    qc = QuantumCircuit(y, c, name="S2C")

    sum_reg = list(y) + [c[0]]  # q = y0 ... yn,c


    for i in range(1, num_bits + 1):
        controls = sum_reg[:i]                 
        targets = sum_reg[i:]                  
        if targets:
            gate = multi_x_gate(num_targets=len(targets), num_ctrl=len(controls))
            qc.append(gate, controls + targets)

        if i != num_bits:
            qc.x(sum_reg[i-1])
        elif num_bits > 1:
            qc.x(sum_reg[0:num_bits - 1])

    qc = qc.to_gate()

    return qc



def smalls2c(y):
    num_bits = len(y)
    qc = QuantumCircuit(y, name="S2C")

    sum_reg = list(y)  # q = y0 ... yn


    for i in range(1, num_bits + 1):
        controls = sum_reg[:i]                 
        targets = sum_reg[i:]                  
        if targets:
            gate = multi_x_gate(num_targets=len(targets), num_ctrl=len(controls))
            qc.append(gate, controls + targets)
        if i != num_bits:
            qc.x(sum_reg[i-1])
        elif num_bits > 1:
            qc.x(sum_reg[0:num_bits - 1])

    qc = qc.to_gate().control()

    return qc

def ctrls2c(x,y,c):


    qc = smalls2c(y)

    qc.append(qc, list(c) + list(y))

    return qc

def subtract(x,y,c):
    qc = QuantumCircuit(x,y,c, name = "Sub")
    num_bits = len(x)
    s2c_gate = s2c(x,y,c)
    qc.append(s2c_gate, list(y) + list(c))

    adder = qft_adder(x,y,c)
    qc.append(adder,list(x) + list(y) + list(c))
    ctrls2c = smalls2c(y)
    qc.append(ctrls2c, list(c)+list(y))

    qc = qc.to_gate()
    return qc
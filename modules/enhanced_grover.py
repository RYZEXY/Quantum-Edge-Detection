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

def grover_phase_oracle(marked):
    num_qubits = len(marked[0])

    oracle = QuantumCircuit(num_qubits)

    for state in marked:
        qstate = state[::-1]
        flip = [i for i in range(num_qubits) if qstate.startswith("0",i)]
        oracle.x(flip)
        oracle.compose(MCMT(ZGate(),num_qubits-1,1), inplace=True)
        oracle.x(flip)
    
    return oracle

def filter_oracle(threshold):
    num_qubits = len(threshold)
    print(num_qubits)
    oracle = QuantumCircuit(num_qubits, name="Oracle")

    state = threshold[::-1]
    bstr = [int(b) for b in state]
    print(bstr)

    temp = []
    max = num_qubits - 1

    

    for i in reversed(range(num_qubits)):
        print(i, bstr[i])
        if bstr[i] == 0:
            if num_qubits == 1:
                oracle.z(i)
            else:
                if i != max:
                    
                    controls = list(range(i + 1, num_qubits))
                    cz = ZGate().control(len(controls))
                    target = i

                    #equivalent to multi control z
                    # oracle.h(target)
                    # oracle.mcx(controls, target, mode='noancilla')
                    # oracle.h(target)

                    all_qubits = [oracle.qubits[i] for i in controls + [target]]
                    oracle.append(cz, all_qubits)
                else:
                    oracle.z(i)
            oracle.x(i)
            temp.append(i)
    oracle.x(temp)
    return oracle.to_gate()
    
        
        

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.circuit.library import QFTGate  
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import Sampler as AerSampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import numpy as np
from qiskit.circuit.library.basis_change import QFT
from modules.neqr import neqr
from modules.ladder import ladder_up
from modules.enhanced_grover import filter_oracle
from modules.qsubtract import subtract
from modules.qadd import qft_adder
from PIL import Image
import numpy as np

def qedgevh(image, threshold, num_bits, intensity_bits):

    x = QuantumRegister(num_bits, name='x')
    y = QuantumRegister(num_bits, name='y')
    i1 = QuantumRegister(intensity_bits, name='I₁')
    i2 = QuantumRegister(intensity_bits, name='I₂')
    grad1 = QuantumRegister(intensity_bits, name='Grad1')
    oracle_a = QuantumRegister(1, name = 'oracle_a')
    grad2c = QuantumRegister(1, name='Grad2c')
    anc = QuantumRegister(1, name='a')
    anc2 = QuantumRegister(1, name = 'a2')
    cr = ClassicalRegister(num_bits*2 + 1, name='c')

    qc = QuantumCircuit(x, y, i1, i2, grad1, grad2c, anc, anc2, oracle_a, cr)

    qc.h(x)
    qc.h(y)
    qc.barrier()


    neqr_gate1 = neqr(i1,x,y,image)
    qc.append(neqr_gate1, list(i1) + list(x) + list(y))

    # Shift up: ladder_up
    ladder = ladder_up(x)
    qc.append(ladder, list(x))

    qc.append(neqr_gate1, list(i2) + list(x) + list(y))
    ladder_down = ladder.inverse()


    qc.draw('mpl')

    for i in range(intensity_bits):
        qc.cx(i2[i], grad1[i])


    sub1 = subtract(i1, grad1, anc)
    qc.append(sub1, list(i1) + list(grad1) + list(anc))

    neqr1_inverse = neqr_gate1.inverse()
    qc.append(neqr1_inverse, list(i2) + list(x) + list(y))

    ladder_down = ladder.inverse()
    qc.append(ladder_down,list(x))
    qc.append(ladder, list(y))

    qc.append(neqr_gate1, list(i2) + list(x) + list(y))

    qc.append(ladder_down,list(y))



    qc.append(sub1, list(i1) + list(i2) + list(anc2))

    add = qft_adder(grad1,i2,grad2c)
    qc.append(add, list(grad1) + list(i2) + list(grad2c))

    qc.h(oracle_a)

    og = filter_oracle(threshold)
    cog = og.control(1,label="Og")
    qc.append(cog, list(oracle_a) + list(i2) + list(grad2c))

    qc.h(oracle_a)

    qc.measure(list(x) + list(y) + list(oracle_a), list(cr))


    qc.draw('mpl')

    simulator = AerSimulator()
    circ = transpile(qc, simulator)

    result = simulator.run(circ).result()
    counts = result.get_counts(circ)
    plot_histogram(counts, title='Bell-State counts')
    return counts.items()



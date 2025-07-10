from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.circuit.library import QFTGate  
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import Sampler as AerSampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import numpy as np
from qiskit.circuit.library.basis_change import QFT
from neqr import neqr
from ladder import ladder_up
from enhanced_grover import filter_oracle
from qsubtract import subtract
from qadd import qft_adder
from PIL import Image
import numpy as np

def qedge(image):
    num_bits = 2
    intensity_bits =  2

    x = QuantumRegister(num_bits, name='x')
    y = QuantumRegister(num_bits, name='y')
    i1 = QuantumRegister(intensity_bits, name='I₁')
    i2 = QuantumRegister(intensity_bits, name='I₂')
    grad1 = QuantumRegister(intensity_bits, name='GradX')
    grad2 = QuantumRegister(intensity_bits, name='GradY')
    grad_diag = QuantumRegister(intensity_bits, name='GradDiag')
    grad2c = QuantumRegister(1, name='GradYc')
    grad_diag_c = QuantumRegister(1, name='GradDiagC')
    grad_sum_c = QuantumRegister(1, name='GradSumC')
    anc = QuantumRegister(1, name='a')
    anc2 = QuantumRegister(1, name = 'a2')
    anc3 = QuantumRegister(1, name = 'a3')
    oracle_a = QuantumRegister(1, name = 'oracle_a')
    cr = ClassicalRegister(num_bits*2 + 1, name='c')

    qc = QuantumCircuit(x, y, i1, i2, grad1, grad2, grad2c, grad_diag, grad_diag_c,grad_sum_c, anc, anc2, anc3, oracle_a, cr)
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

    for i in range(intensity_bits):
        qc.cx(i2[i], grad1[i])

    sub1 = subtract(i1, grad1, anc)
    qc.append(sub1, list(i1) + list(grad1) + list(anc))

    neqr1_inverse = neqr_gate1.inverse()
    qc.append(neqr1_inverse, list(i2) + list(x) + list(y))

    ladder_down = ladder.inverse()
    qc.append(ladder, list(y))

    qc.append(neqr_gate1, list(i2) + list(x) + list(y))

    for i in range(intensity_bits):
        qc.cx(i2[i], grad_diag[i])

    qc.append(sub1, list(i1) + list(grad_diag) + list(anc3))

    qc.append(neqr1_inverse, list(i2) + list(x) + list(y))

    qc.append(ladder_down,list(x))
    qc.append(neqr_gate1, list(i2) + list(x) + list(y))
    qc.append(ladder_down,list(y))


    for i in range(intensity_bits):
        qc.cx(i2[i], grad2[i])

    qc.append(sub1, list(i1) + list(grad2) + list(anc2))

    add = qft_adder(grad1,grad2,grad2c)
    qc.append(add, list(grad1) + list(grad2) + list(grad2c))

    add2 = qft_adder(list(grad2)+list(grad2c),list(grad_diag)+list(grad_diag_c),grad_sum_c)
    qc.append(add2, list(grad2)+list(grad2c)+list(grad_diag)+list(grad_diag_c)+list(grad_sum_c))

    qc.barrier()
    qc.h(oracle_a)

    og = filter_oracle("000")
    cog = og.control(1,label="Og")
    qc.append(cog, list(oracle_a) + list(grad_diag)+list(grad_diag_c))

    qc.h(oracle_a)

    qc.barrier()

    qc.measure(list(x) + list(y) + list(oracle_a), list(cr))

    qc.draw('mpl')

    simulator = AerSimulator()
    circ = transpile(qc, simulator)

    result = simulator.run(circ).result()
    counts = result.get_counts(circ)
    plot_histogram(counts, title='Bell-State counts')
    return counts.items()

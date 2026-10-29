import numpy as np
from scipy.optimize import minimize
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from .graphs import cut_value


def circuit(graph, params, p=1, measure=True):
    n = graph['n']
    qc = QuantumCircuit(n)
    for q in range(n):
        qc.h(q)
    for layer in range(p):
        gamma, beta = params[layer], params[p + layer]
        for u, v, weight in graph['edges']:
            # U_C = exp(-i gamma * cut), global phase ignored.
            qc.cx(u, v)
            qc.rz(-gamma * weight, v)
            qc.cx(u, v)
        for q in range(n):
            qc.rx(2 * beta, q)
    if measure:
        qc.measure_all()
    return qc


def ideal_expectation(graph, params, p):
    qc = circuit(graph, params, p=p, measure=False)
    probs = Statevector.from_instruction(qc).probabilities_dict()
    return sum(cut_value(bits, graph) * prob for bits, prob in probs.items())


def optimize_qaoa(graph, p=1, restarts=4, seed=42, maxiter=150):
    rng = np.random.default_rng(seed)
    choices = [np.array([0.6] * p + [0.35] * p)]
    choices += [rng.uniform(0, np.pi, size=2*p) for _ in range(restarts-1)]
    best = None
    for x0 in choices:
        opt = minimize(lambda x: -ideal_expectation(graph, x, p), x0,
                       method='COBYLA', options={'maxiter': maxiter, 'rhobeg': 0.3})
        if best is None or opt.fun < best.fun:
            best = opt
    return best.x, -float(best.fun)

import json
from pathlib import Path
from qiskit import transpile
from qiskit.transpiler import CouplingMap
from qiskit_aer.noise import NoiseModel, depolarizing_error, ReadoutError


def load_processors(folder):
    out = {}
    for label in ('A', 'B'):
        data = json.loads((Path(folder) / f'processor_{label}.json').read_text(encoding='utf-8'))
        if data.get('official') is not False:
            raise ValueError('This demonstration only accepts configs explicitly labeled illustrative')
        out[label] = data
    return out


def coupling(config):
    links = []
    for u, v in config['coupling_map']:
        links.extend([[u, v], [v, u]])
    return CouplingMap(couplinglist=links)


def compile_circuit(qc, config, seed=42):
    return transpile(qc, coupling_map=coupling(config),
                     basis_gates=config['basis_gates'],
                     initial_layout=list(range(qc.num_qubits)),
                     optimization_level=1, seed_transpiler=seed)


def noise_model():
    # Phase 1 Master Guide synthetic noise baseline (page 2).
    noise = NoiseModel()
    noise.add_all_qubit_quantum_error(depolarizing_error(0.001, 1), ['sx', 'x'])
    noise.add_all_qubit_quantum_error(depolarizing_error(0.005, 2), ['cx'])
    noise.add_all_qubit_readout_error(ReadoutError([[0.99, 0.01], [0.01, 0.99]]))
    return noise


def circuit_metrics(qc):
    ops = qc.count_ops()
    return {
        'depth': qc.depth(),
        'cx_gates': int(ops.get('cx', 0)),
        'two_qubit_gates': sum(x.operation.num_qubits == 2 for x in qc.data),
        'explicit_swaps': int(ops.get('swap', 0)),
        'circuit_width': qc.num_qubits,
    }


def reference_circuit(qc, config, seed=42):
    n = qc.num_qubits
    links = [[u, v] for u in range(n) for v in range(n) if u != v]
    return transpile(qc, coupling_map=CouplingMap(couplinglist=links),
                     basis_gates=config['basis_gates'],
                     initial_layout=list(range(n)),
                     optimization_level=1, seed_transpiler=seed)

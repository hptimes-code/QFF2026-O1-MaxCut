"""PS-O1 Phase 2: compare official Processor B with a candidate Processor D.
Run from the official starter pack folder. Does not modify qff_phase2.py.
"""
import json
from pathlib import Path
from qiskit import QuantumCircuit
from qff_phase2 import PROCESSOR_B, circuit_metrics, validate_processor_d

root = Path(__file__).resolve().parent
instance = json.loads((root / 'instances.json').read_text(encoding='utf-8'))['PS-O1']
D = json.loads((root / 'processor_D.json').read_text(encoding='utf-8'))
errors = validate_processor_d(D, instance['num_vertices'])
if errors:
    raise ValueError('Processor D failed validation: ' + '; '.join(errors))
print('Processor D rule check: OK')
print('NOTE: This is a fixed-parameter routing benchmark, not optimized QAOA.')

n = instance['num_vertices']
qc = QuantumCircuit(n)
qc.h(range(n))
gamma, beta = 0.6, 0.35
for u,v,w in instance['weighted_edges']:
    qc.cx(u,v)
    qc.rz(-gamma*w, v)
    qc.cx(u,v)
for q in range(n):
    qc.rx(2*beta,q)
qc.measure_all()

for processor in [PROCESSOR_B, D]:
    metrics = circuit_metrics(qc, processor)
    print(json.dumps(metrics, indent=2))

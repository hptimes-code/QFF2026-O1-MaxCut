"""QFF2026 PS-O1 Objective 1: provisional Processor D Bell verification.
Run from the official starter-pack directory; leaves qff_phase2.py unchanged.
"""
import csv
from pathlib import Path

from qff_phase2 import (
    SHOTS,
    coupling_map_from_edges,
    bell_experiment,
    load_processor,
    validate_processor_d,
)

# Use the starter template for an initial test only. Change to
# 'processors/processor_D.json' after finalizing your team architecture.
processor = load_processor('processor_D.json')
errors = validate_processor_d(processor, required_qubits=6)
if errors:
    raise ValueError('Invalid Processor D: ' + '; '.join(errors))

cm = coupling_map_from_edges(processor['edges'], processor['num_qubits'])
adjacent = tuple(processor['edges'][0])
n = processor['num_qubits']
# Deterministic tie-breaking if multiple pairs share the maximum distance.
farthest = max(
    ((a, b) for a in range(n) for b in range(a + 1, n)),
    key=lambda pair: (cm.distance(*pair), -pair[0], -pair[1]),
)

rows = []
for pair_type, pair in [('adjacent', adjacent), ('farthest', farthest)]:
    for noisy in (False, True):
        result = bell_experiment(processor, physical_pair=pair, noisy=noisy, shots=SHOTS)
        row = {'pair_type': pair_type, **result}
        row['pair'] = f'{pair[0]}-{pair[1]}'
        rows.append(row)
        print(f"{pair_type:8} pair={pair} distance={result['pair_distance']} "
              f"noisy={noisy} XX={result['XX']:.3f} YY={result['YY']:.3f} "
              f"ZZ={result['ZZ']:.3f} F={result['fidelity']:.4f} "
              f"+/- {result['fidelity_se']:.4f} CX={result['cx']}")

outdir = Path('results') / 'tables'
outdir.mkdir(parents=True, exist_ok=True)
output = outdir / 'bell.csv'
with output.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
print(f'\nSaved {output}')
print("NOTE: Final custom 6-qubit Processor D Bell verification.")

"""Create master-guide-compatible aggregate tables and figures without altering trial results."""
from pathlib import Path
import shutil
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
RESULTS = BASE / 'results'
TABLES = RESULTS / 'tables'
FIGURES = RESULTS / 'figures'
TABLES.mkdir(parents=True, exist_ok=True)
FIGURES.mkdir(parents=True, exist_ok=True)
frames = []
for folder in sorted(RESULTS.iterdir()):
    if not folder.is_dir() or not (folder/'architecture.csv').exists():
        continue
    name = folder.name
    arch = pd.read_csv(folder/'architecture.csv').assign(graph=name)
    frames.append(arch)
    for f in ['architecture.csv', 'summary.csv', 'paired_comparison.csv']:
        source = folder/f
        if source.exists(): shutil.copy2(source, TABLES / f'{name}_{f}')
    for f in ['architecture.png', 'compilation_overhead.png','cut_comparison.png','maxcut_graph.png']:
        source = folder/f
        if source.exists(): shutil.copy2(source, FIGURES / f'{name}_{f}')
if frames:
    pd.concat(frames, ignore_index=True).to_csv(TABLES/'all_architecture.csv', index=False)
print('Exported submission tables/figures to', RESULTS)

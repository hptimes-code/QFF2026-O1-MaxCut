"""QFF 2026 PS-O1: generate report-ready figures from measured Phase 2 CSVs.
Run in the starter-pack root: python phase2_figures.py
"""
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
TABLES = ROOT / 'results' / 'tables'
FIGURES = ROOT / 'results' / 'figures'
FIGURES.mkdir(parents=True, exist_ok=True)

results = pd.read_csv(TABLES / 'results.csv')
bell = pd.read_csv(TABLES / 'bell.csv')
required = {'seed', 'processor', 'mode', 'executable', 'mean_cut',
            'approximation_ratio', 'cx', 'depth', 'swaps'}
assert required.issubset(results.columns), f'Missing columns: {required - set(results.columns)}'
active = results[results['executable'].astype(str).str.lower() == 'true'].copy()
active['seed'] = pd.to_numeric(active['seed'], errors='raise').astype(int)
assert len(active) == 20 and set(active['seed']) == set(range(5)), 'Unexpected active results'
processors = ['Processor B', 'Processor D']
colors = {'Processor B':'#2457A7', 'Processor D':'#DA722F'}

# 1: seed-by-seed mean cut, ideal and noisy
fig, axes = plt.subplots(1, 2, figsize=(11, 4.1), sharey=True)
for ax, mode in zip(axes, ['Ideal', 'Noisy']):
    for processor in processors:
        t = active[(active.processor == processor) & (active['mode'] == mode)].sort_values('seed')
        assert len(t) == 5
        ax.plot(t.seed, t.mean_cut, marker='o', linewidth=2, color=colors[processor], label=processor)
    ax.axhline(22, color='gray', linestyle='--', linewidth=1, label='Exact optimum (22)')
    ax.set(title=f'{mode} simulation', xlabel='Optimization seed', xticks=list(range(5)))
    ax.grid(alpha=.18)
axes[0].set_ylabel('Mean weighted cut')
axes[1].legend(fontsize=8, loc='upper left')
fig.suptitle('QAOA p=1: five-seed cut quality')
fig.tight_layout()
fig.savefig(FIGURES / 'qaoa_mean_cut_by_seed.png', dpi=200)
plt.close(fig)

# 2: aggregate mean approximation ratio by processor and mode
fig, ax = plt.subplots(figsize=(8, 4.5))
x = np.arange(len(processors)); width=.34
for i, mode in enumerate(['Ideal','Noisy']):
    means = [active[(active.processor==p)&(active['mode']==mode)].approximation_ratio.mean() for p in processors]
    bars = ax.bar(x+(i-.5)*width, means, width, label=mode)
    ax.bar_label(bars, fmt='%.4f', padding=3, fontsize=9)
ax.set_xticks(x, processors)
ax.set_ylabel('Mean approximation ratio across five seeds')
ax.set_ylim(0, 1)
ax.legend()
ax.grid(axis='y', alpha=.18)
ax.set_title('QAOA approximation ratio: ideal vs noisy')
fig.tight_layout(); fig.savefig(FIGURES / 'approximation_ratio.png', dpi=200); plt.close(fig)

# 3: resource bars, independent panels for different scales
fig, axes = plt.subplots(1, 3, figsize=(11, 3.8))
for ax, field, title in zip(axes, ['cx','depth','swaps'], ['CX gates','Circuit depth','SWAP gates']):
    vals = [active[active.processor==p][field].mean() for p in processors]
    bars = ax.bar(['B','D'], vals, color=[colors[p] for p in processors])
    ax.bar_label(bars, fmt='%.0f', padding=3)
    ax.set_title(title)
    ax.set_ylim(0, max(vals) * 1.22 if max(vals) else 1)
    ax.grid(axis='y', alpha=.18)
fig.suptitle('Compiled circuit resource comparison')
fig.tight_layout(); fig.savefig(FIGURES / 'processor_resources.png', dpi=200); plt.close(fig)

# 4: Bell fidelity with error bars
assert {'pair_type','noisy','fidelity','fidelity_se'}.issubset(bell.columns)
fig, ax = plt.subplots(figsize=(8, 4.5))
pairs = ['adjacent', 'farthest']
for i, is_noisy in enumerate([False, True]):
    subset = bell[bell.noisy.astype(str).str.lower() == str(is_noisy).lower()]
    vals, errs = [], []
    for pair in pairs:
        t = subset[subset.pair_type.astype(str).str.lower() == pair]
        assert len(t) == 1, f'Expected one row for {pair}, noisy={is_noisy}'
        vals.append(float(t.fidelity.iloc[0])); errs.append(float(t.fidelity_se.iloc[0]))
    bars = ax.bar(np.arange(2)+(i-.5)*.34, vals, .34, yerr=errs, capsize=4,
                  label='Noisy' if is_noisy else 'Ideal')
    ax.bar_label(bars, fmt='%.4f', padding=4, fontsize=9)
ax.set_xticks(range(2), ['Adjacent pair','Farthest pair'])
ax.set_ylim(.88, 1.025)
ax.set_ylabel('Bell fidelity')
ax.legend()
ax.grid(axis='y', alpha=.18)
ax.set_title('Custom Processor D: Bell-state verification')
fig.tight_layout(); fig.savefig(FIGURES / 'bell_fidelity.png', dpi=200); plt.close(fig)

print('Generated 4 figures in:', FIGURES)
for p in sorted(FIGURES.glob('*.png')):
    if p.name in {'qaoa_mean_cut_by_seed.png','approximation_ratio.png','processor_resources.png','bell_fidelity.png'}:
        print(' -', p.name)

# QFF 2026 — Phase 2 | PS-O1 Weighted Max-Cut

**Project:** QFF2026-O1-MaxCut  
**Track:** Quantum Optimization  
**Problem:** PS-O1 — Quantum Optimization of Network Partitioning Using QAOA  
**Previous work:** [`Phase One/`](Phase%20One/) preserves the entire original Phase 1 submission. The current Phase 2 work lives in the repository root.

## Problem and approach

We solve the organizers' **locked six-vertex, nine-edge weighted Max-Cut** instance with the Quantum Approximate Optimization Algorithm (QAOA), required depth **p=1**. Each vertex is a qubit, and the objective is to maximize the weight of edges crossing the partition. We enumerate all 64 bitstrings for an exact classical benchmark, optimize QAOA angles using COBYLA and ideal statevector expectations, and evaluate compiled circuits under the *official* ideal and synthetic-noisy Aer simulations on Processor B and our custom Processor D. Processor A has five physical qubits and **cannot execute the six-qubit task**.

### Exact baselines

| Metric | Value |
|---|---:|
| Optimum weighted cut C* | 22 |
| Optimal bitstrings (q5…q0) | `001011`, `110100` |
| Uniform-random mean cut | 13.5 |
| Uniform-random approximation ratio | 0.613636 |
| Uniform-random probability of optimal cut | 0.03125 (3.125%) |

The random baseline is computed by exact enumeration of all 64 bitstrings, not simulation.

## Processor D

Our problem-aware Processor D has **6 physical qubits and 9 undirected couplings**, each corresponding to an edge of the locked problem graph. It satisfies the organizer's topology validator and has maximum degree 4. Its configuration is in `processors/processor_D.json` (see final submission packaging notes below).

## Validated Phase 2 findings

The results below are from the October 29 corrected five-seed p=1 QAOA run (seeds 0–4), with both initial angles sampled from [0, π], COBYLA, 4,096 shots per circuit and the official simulation helpers. The scripts ran successfully in a fresh repository virtual environment; all six code cells in `main.ipynb` executed with zero reported errors.

| Metric | Processor B | Processor D |
|---|---:|---:|
| Physical qubits | 9 | 6 |
| CX gates | 21 | 18 |
| Circuit depth | 37 | 29 |
| Two-qubit depth | 17 | 14 |
| SWAP gates | 1 | 0 |
| Mean noisy approximation ratio across 5 starts | 0.705857 | 0.705913 |
| Mean noisy cut across 5 starts | 15.528857 | 15.530078 |
| Mean noisy P(opt) | 0.049219 | 0.047705 |
| Mean ideal approximation ratio | 0.718364 | 0.717625 |
| Best-sampled ratio, all runs | 1.0000 | 1.0000 |

The circuit-resource advantage is clear for the measured compilation: **14.3% fewer CX gates** and **21.6% lower depth**. The mean noisy approximation-ratio difference (D−B) is only **+0.000056**, and the mean noisy cut difference is **+0.001221**; these do **not** establish a statistically meaningful solution-quality improvement. The best-sampled ratio of 1.0 means at least one optimal sample appeared in each run, not that every shot was optimal.

### Bell verification on custom D

| Qubits | Distance | Ideal fidelity | Noisy fidelity | CX |
|---|---:|---:|---:|---:|
| Adjacent (0,2) | 1 | 1.0000 | 0.9633 ± 0.0021 | 1 |
| Farthest (0,1) | 2 | 1.0000 | 0.9542 ± 0.0023 | 4 |

## Environment and reproduction

Use **Python 3.12**. In PowerShell, from the **repository root**:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python phase2_d_benchmark.py
python phase2_bell_test.py
python phase2_qaoa.py
python phase2_figures.py
```

Open `main.ipynb` using the same `.venv` kernel and select **Run All**. It calls those scripts in order and displays CSV tables and figures. The official `qff_phase2.py` must remain unchanged. Results are written to `results/tables/` and `results/figures/`.

**Validation and packaging:** Both angles are initialized in `[0, π]`; `results/tables/results.csv` includes `r_best`, and `results/tables/classical_baseline.csv` records the exact random baseline. The plots were regenerated after the corrected run. The repository contains `data/instance.json` and `processors/processor_D.json`, as well as the original root-level files retained for compatibility with existing scripts. A fresh Python 3.12 environment installed the requirements and executed all four scripts successfully; `main.ipynb` reported 6/6 executed code cells and no stored errors. Final human review of the organizer's submission checklist, elapsed notebook runtime, and any required topology/partition figure is still recommended.

## Repository layout

```text
Phase One/                   Archived Phase 1 submission (preserved)
main.ipynb                  Reproducible Phase 2 entry notebook
qff_phase2.py               Official helper — do not edit
instances.json              Official locked instances — do not edit
phase2_qaoa.py              QAOA optimization and measurement
phase2_bell_test.py         Bell correlation and fidelity experiments
phase2_d_benchmark.py       B versus D routing comparison
phase2_figures.py           Figure generation
processors/processor_D.json Final processor design
data/instance.json          PS-O1 instance copy
results/tables/             Experiment CSVs including classical_baseline.csv
results/figures/            Visual results
report.md                   Technical analysis
requirements.txt            Dependencies
```



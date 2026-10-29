# Quantum Optimization (PS-O1): Weighted Max-Cut

**Qiskit Fall Fest 2026 — Phase 1 | SRM University-AP**

## Problem and method

We implement the Max-Cut problem using the Quantum Approximate Optimization Algorithm (QAOA, p=1). A classical exhaustive solver supplies the exact optimal cut for comparison. The same logical circuits are compiled and simulated on participant-designed architectures: **Processor A (5 qubits)** and **Processor B (9 qubits)**.

## Processor setup

| Setting | Processor A | Processor B |
|---|---|---|
| Physical qubits | 5 | 9 |
| Gate basis | `rz`, `sx`, `x`, `cx` | same |
| Connectivity | participant-designed branching tree | participant-designed 12-edge sparse network |

Phase 1 Master Guide synthetic noise: **1q depolarizing 0.001; CX depolarizing 0.005; readout 0.01**, identically applied on A and B. Compilation: optimization level 1, seed 42, 4096 shots. Connectivity is a documented design choice, not a calibrated real-device map.

## Installation and execution

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Open **`main.ipynb`** in VS Code or Jupyter and run its cells from the repository root. Equivalent terminal commands:

```powershell
python scripts/generate_o1_graph.py
python main.py --all --processors AB --shots 4096 --trials 20 --restarts 3 --maxiter 100 --seed 42
python main.py --graph data/raw/o1_weighted_6node.json --processors B --shots 4096 --trials 20 --restarts 3 --maxiter 100 --seed 42
python scripts/export_submission.py
python scripts/plot_topologies.py
```

**Why two experiment groups?** PS-O1 specifies a **six-node weighted graph**, but Processor A has only five physical qubits. A direct six-qubit QAOA circuit therefore cannot run on A. We evaluate the specified six-node graph on B and retain four <=5-node graph instances for valid A/B comparison. We do not invent an A result for the six-node task.

## Results

`results/graph1` through `results/graph4` store A/B benchmark data. `results/o1_weighted_6node` stores the B-only weighted graph results. `results/tables/` and `results/figures/` hold submission exports. Output includes exact cut, mean cut, approximation ratio, depth, CX count and connectivity-constrained overhead. **Excess CX does not equal an exact router-inserted SWAP count.**

The prior experiment used different noise rates; **rerun the notebook before treating existing result files as Master Guide benchmark results**. See [report.md](report.md) and [ROUTING_ANALYSIS.md](ROUTING_ANALYSIS.md) for detailed architecture analysis and measurement limitations.

## Repository layout

`main.ipynb`, `main.py`, `requirements.txt`, `data/raw/`, `data/processed/`, `processors/`, `src/`, `results/tables/`, `results/figures/`, `report.md`, `assets/`.

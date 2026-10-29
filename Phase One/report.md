# Phase 1 PS-O1 — Architecture-aware Weighted Max-Cut

## Design

QAOA p=1; COBYLA with three restarts and 100 iterations; exhaustive classical Max-Cut baseline; Qiskit Aer ideal and synthetic noisy simulation at 4096 shots per trial. Processor A has five physical qubits; Processor B has nine. Coupling graphs are participant-designed as the Master Guide permits.

## Guide noise baseline (new specification)

Single-qubit depolarizing: 0.001. CX depolarizing: 0.005. Readout bit-flip: 0.01. Both processors use the same synthetic rates. Seed 42 and optimization level 1.

## Problem-size conflict in PS-O1

The Master Guide requires a six-node weighted graph (Erdős–Rényi n=6, p=0.5, seed=42, integer weights 1–5) while giving Processor A only five physical qubits. Without extra qubit resources or a problem-reduction method, direct six-logical-qubit QAOA on A is not possible. Therefore we explicitly separate:

1. **Primary six-node weighted Max-Cut:** executed on Processor B only, validated against exact enumeration.
2. **A/B architecture benchmark:** four smaller unweighted graphs with four or five nodes, executable on both processors.

A six-node A result is neither fabricated nor claimed. The six-node graph is generated using `scripts/generate_o1_graph.py`.

## Updated experimental results

Run `main.ipynb` or the commands in `README.md` and use the generated `results/*/report.md` and `results/tables/` files. **Numerical results obtained with the previous 0.02 CX / 0.015 readout noise are historical only and must not be represented as the new Master Guide benchmark.** No fresh benchmark figures are claimed before rerunning.

## Metrics and routing caveat

Exact optimum, sampled mean cut, approximation ratio, depth, native CX count, reference-adjusted depth/CX overhead and ideal/noisy comparisons are computed. The native basis excludes SWAP, so `explicit_swaps=0` in final compiled circuits is not an exact inserted SWAP count. Exact routing-stage SWAP counts require a separate instrumented transpilation analysis.

## Limitations

All results are from Qiskit Aer simulation with synthetic noise, a fixed initial layout and participant-designed topologies. No physical-hardware performance or calibrated fidelity is claimed. Statistical intervals reflect finite-shot variation under fixed fitted parameters. Check the published experiment outputs to assess specific graph-dependent conclusions.

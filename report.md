# QFF 2026 Phase 2 — Technical Report
## PS-O1: Weighted Max-Cut with QAOA and a Problem-Aware Processor D

QAOA run with five initialization seeds (0–4), both initial angles sampled uniformly from [0, π]. The experiment and plots were reproduced from a newly created Python 3.12 repository environment, and all six notebook code cells were executed without stored errors. Results are Qiskit Aer simulations, not physical-device measurements.

## 1. Objective and formulation

We study how hardware connectivity influences the resources and simulated noisy performance of depth-one QAOA for a six-vertex weighted Max-Cut instance. The official locked input has nine edges of total weight 27. Let x_i ∈ {0,1} indicate the partition assigned to vertex i. The cut value is

\[
C(x)=\sum_{(i,j)\in E}w_{ij}(x_i+x_j-2x_ix_j).
\]

The QUBO minimizes −C(x). With Pauli Z, x_i=(1−Z_i)/2, so the cut operator is \(\hat C=\frac12\sum_{(i,j)}w_{ij}(I-Z_iZ_j)\). The cost Hamiltonian for minimizing the QUBO is \(H_{QUBO}=-\hat C\); the cost-unitary sign must be applied consistently with the chosen convention. We optimize the expected cut value directly. The p=1 ansatz applies H to all qubits, one ZZ phase for each weighted edge, and RX(2β) on every qubit, then measures in the computational basis.

### Locked graph edges

| Edge | Weight | Edge | Weight | Edge | Weight |
|---|---:|---|---:|---|---:|
| 0–2 | 1 | 0–3 | 4 | 0–4 | 4 |
| 1–4 | 3 | 1–5 | 3 | 2–3 | 5 |
| 2–4 | 1 | 3–4 | 4 | 3–5 | 2 |

All 64 bitstrings are enumerated to obtain **C*=22**, realized by `001011` and its complement `110100` (displayed q5…q0). Uniform random sampling yields a mean cut **13.5**, an expected approximation ratio **13.5/22 = 0.613636**, and **P_opt = 2/64 = 0.03125**. These are exactly computed baselines, not fitted results.

## 2. Optimization and evaluation protocol

Our final implementation uses p=1 QAOA, the SciPy **COBYLA** optimizer (`maxiter=120`, `rhobeg=0.25`), and an exact **Qiskit Statevector** objective. The optimized angles were reused when evaluating all processors, making the ideal/noisy and B/D comparisons consistent at each initialization. The initialization seeds are **0,1,2,3,4** with `numpy.random.default_rng(seed)`; **both starting angles are sampled from [0,π]**. Sampling uses 4096 shots with the official simulator and noise helper. The circuit is compiled using the official helper for each processor.

For every shot, we calculate weighted cut C(x). The main metrics are the shot-average cut, approximation ratio r=E[C]/C*, best sampled cut, r_best=C_best/C*, and probability of an optimal sample P_opt. Across the five independent optimization starts we report means and sample standard deviations. **`r_best` is included in `results.csv` and `qaoa_summary.csv`.** A processor lacking six physical qubits must be shown as *not executable* rather than assigned an estimated score.

## 3. Processor D design and routing

Processor A has **5 qubits**, Processor B **9 qubits** and our custom **Processor D 6 qubits**. D uses the following undirected couplings:

`(0,2), (0,3), (0,4), (1,4), (1,5), (2,3), (2,4), (3,4), (3,5)`.

This connected, maximum-degree-four architecture aligns each interacting logical Max-Cut pair to a native physical connection. The official validation helper returned **`Processor D rule check: OK`**. The design is deliberately specialized to PS-O1 rather than optimized for arbitrary workloads. The primary trade-off is that more targeted couplings may be less versatile and, on actual hardware, high-degree connectivity could increase calibration complexity or crosstalk. These are design considerations, **not observed effects** in our synthetic-noise simulation.

### Measured routing benchmark (fixed parameters γ=0.6, β=0.35)

| Metric | Official B | Custom D | Interpretation |
|---|---:|---:|---|
| Physical qubits | 9 | 6 | D uses exactly the six required qubits |
| Logical CX | 18 | 18 | Same logical interaction workload |
| Compiled CX | 21 | 18 | D eliminates 3 routing CX |
| Circuit depth | 37 | 29 | D is 8 layers shallower |
| Two-qubit depth | 17 | 14 | D reduces two-qubit layer count |
| SWAP gates | 1 | 0 | One B routing SWAP avoided |
| CX overhead | 3 | 0 | No excess CX over logical count for D |

D reduces compiled CX by **14.3%** and circuit depth by **21.6%** in this test. These are compiler-resource metrics, not physical execution-time measurements. We must keep the precise distinction between a count of reported SWAP operations and decomposed routing gates.

## 4. Bell-state verification

The official Bell procedure measures XX, YY and ZZ, with fidelity estimated as

\[
F=(1+\langle XX\rangle-\langle YY\rangle+\langle ZZ\rangle)/4.
\]

Measurements from the **final six-qubit custom D**, with statistical standard errors reported by the helper:

| Physical pair | Shortest-path distance | Mode | XX | YY | ZZ | Fidelity ± SE | CX |
|---|---:|---|---:|---:|---:|---|---:|
| (0,2) | 1 | Ideal | 1.000 | −1.000 | 1.000 | 1.0000 ± 0.0000 | 1 |
| (0,2) | 1 | Noisy | 0.946 | −0.952 | 0.955 | 0.9633 ± 0.0021 | 1 |
| (0,1) | 2 | Ideal | 1.000 | −1.000 | 1.000 | 1.0000 ± 0.0000 | 4 |
| (0,1) | 2 | Noisy | 0.944 | −0.934 | 0.938 | 0.9542 ± 0.0023 | 4 |

The longer-distance pair needs more CX gates and has lower noisy fidelity (0.9542 versus 0.9633). This is consistent with extra gate-noise exposure in the defined model, not a claim about measured physical devices.

## 5. Corrected five-seed QAOA outcomes

The final corrected run produces **20 executable measurement rows** (B and D × ideal/noisy × 5 starts), plus **5 Processor A non-executable records** because A has insufficient qubits. Every reported circuit uses 4,096 measurement shots. `r_best=1.0000` in each executable run indicates that at least one optimum (cut 22) was sampled, **not** that the average approximation ratio was 1.0.

| Five-start mean metric | B ideal | D ideal | B noisy | D noisy |
|---|---:|---:|---:|---:|
| Mean cut | 15.804004 | 15.787744 | 15.528857 | 15.530078 |
| Approximation ratio | 0.718364 | 0.717625 | 0.705857 | 0.705913 |
| P_opt | 0.051514 | 0.049365 | 0.049219 | 0.047705 |
| Best-sampled approximation ratio | 1.000000 | 1.000000 | 1.000000 | 1.000000 |
| Compiled CX gates | 21 | 18 | 21 | 18 |
| Circuit depth | 37 | 29 | 37 | 29 |
| SWAPs | 1 | 0 | 1 | 0 |

The **uniform-random mean cut is 13.5** (approximation ratio **0.613636**), below both noisy QAOA means. Among the five starts, **seed 3** had the highest exact ideal statevector expectation, **17.712817**. Its observed noisy means were **17.3220 on B** and **17.2969 on D**. Across seeds the noisy mean-cut difference D−B was only **+0.001221**, corresponding to an approximation-ratio difference of **+0.000056**. These small differences do not demonstrate a statistically significant solution-quality advantage. D's measured advantage is **resource efficiency** on the locked circuit.

The generated figures are `results/figures/qaoa_mean_cut_by_seed.png`, `approximation_ratio.png`, `processor_resources.png`, and `bell_fidelity.png`, regenerated using the corrected QAOA CSVs. The exact classical and random baselines are exported to `results/tables/classical_baseline.csv`.

## 6. Limitations and further work

- Five optimizer starts and 4,096 shots per compiled circuit allow a reproducible exploratory comparison, but do **not** establish statistical significance for the tiny D−B quality differences. Across-seed standard deviations reflect variation in optimized starts, not a calibrated hardware error bound.
- The common fixed simulator seed aids reproducibility, but does not itself prove a valid paired inferential design across two different compiled circuits.
- `r_best = 1` is a best-observed-sample metric, and should not be confused with the expected approximation ratio or a guarantee of optimal output in an individual shot.
- Processor D is specialized to the locked graph; its benefits may not generalize to other workloads. Further graphs, higher QAOA depth p=2, and alternative layouts are useful future tests but are not claimed as completed here.
- All comparisons use **Qiskit Aer with organizer-provided synthetic noise**, not physical quantum devices, measured execution time, or calibrated hardware crosstalk.
- The notebook orchestrates standalone Python scripts, and its six code cells were executed successfully in the repository virtual environment. A timed fresh run against the organizer's complete grading environment has not been independently verified here.




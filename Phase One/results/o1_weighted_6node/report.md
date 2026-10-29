# o1_weighted_6node — O1 Max-Cut A/B experiment

**Processor coupling graphs are participant-defined; noise matches the Phase 1 Master Guide.**

- Graph: 6 nodes; 9 edges
- Exact classical optimal cut: 16
- p=1; statevector-optimized expected cut: 11.978903
- Shots per trial: 4096; trial seeds: 20

## A/B quality

| processor   | mode   |   trials |   mean_cut |    sd_cut |   ci95_low |   ci95_high |   mean_approximation_ratio |   mean_optimal_probability |   mean_best_sampled_cut |
|:------------|:-------|---------:|-----------:|----------:|-----------:|------------:|---------------------------:|---------------------------:|------------------------:|
| B           | Ideal  |       20 |    11.9745 | 0.0434512 |    11.9555 |     11.9935 |                   0.748406 |                   0.147876 |                      16 |
| B           | Noisy  |       20 |    11.6552 | 0.0481235 |    11.6341 |     11.6763 |                   0.728448 |                   0.131653 |                      16 |

## Architecture metrics

| processor   |   physical_qubits |   depth |   cx_gates |   two_qubit_gates |   explicit_swaps |   circuit_width |   reference_depth |   reference_cx |   depth_overhead |   cx_overhead |
|:------------|------------------:|--------:|-----------:|------------------:|-----------------:|----------------:|------------------:|---------------:|-----------------:|--------------:|
| B           |                 9 |      55 |         30 |                30 |                0 |               9 |                30 |             18 |               25 |            12 |

## Paired A/B differences

Not applicable: only Processor B can run a six-node QAOA circuit (Processor A has five physical qubits).

## Interpretation and limitations

The two implementations use the same logical graph, QAOA parameters, transpilation seed,
native gate basis and Phase 1 Master Guide synthetic noise rates. Circuit resource differences reflect
the chosen example topology and layout, not measured IBM quantum hardware.
Explicit SWAP count can be zero even when routing gates are decomposed into CX.
Extra CX gates relative to a fully connected compilation are not an exact SWAP count.
Intervals are approximate finite-shot confidence intervals at fixed parameters.
Do not infer a hardware speed advantage from simulator runtime.

## Guide-specific limitation

PS-O1 specifies six logical vertices but Processor A has five physical qubits. The six-vertex case is therefore run only on Processor B; four smaller cases support an actual A/B comparison.

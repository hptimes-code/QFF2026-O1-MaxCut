# graph1 — O1 Max-Cut A/B experiment

**Processor coupling graphs are participant-defined; noise matches the Phase 1 Master Guide.**

- Graph: 4 nodes; 5 edges
- Exact classical optimal cut: 4
- p=1; statevector-optimized expected cut: 3.237109
- Shots per trial: 4096; trial seeds: 20

## A/B quality

| processor   | mode   |   trials |   mean_cut |     sd_cut |   ci95_low |   ci95_high |   mean_approximation_ratio |   mean_optimal_probability |   mean_best_sampled_cut |
|:------------|:-------|---------:|-----------:|-----------:|-----------:|------------:|---------------------------:|---------------------------:|------------------------:|
| A           | Ideal  |       20 |    3.23234 | 0.00780498 |    3.22892 |     3.23576 |                   0.808084 |                   0.325659 |                       4 |
| A           | Noisy  |       20 |    3.16609 | 0.0083261  |    3.16244 |     3.16974 |                   0.791522 |                   0.302808 |                       4 |
| B           | Ideal  |       20 |    3.23984 | 0.0106296  |    3.23519 |     3.2445  |                   0.809961 |                   0.33241  |                       4 |
| B           | Noisy  |       20 |    3.17545 | 0.0108414  |    3.1707  |     3.1802  |                   0.793863 |                   0.310071 |                       4 |

## Architecture metrics

| processor   |   physical_qubits |   depth |   cx_gates |   two_qubit_gates |   explicit_swaps |   circuit_width |   reference_depth |   reference_cx |   depth_overhead |   cx_overhead |
|:------------|------------------:|--------:|-----------:|------------------:|-----------------:|----------------:|------------------:|---------------:|-----------------:|--------------:|
| A           |                 5 |      40 |         16 |                16 |                0 |               5 |                24 |             10 |               16 |             6 |
| B           |                 9 |      32 |         16 |                16 |                0 |               9 |                24 |             10 |                8 |             6 |

## Paired A/B differences

| mode   |   difference_B_minus_A |   ci95_low |   ci95_high |
|:-------|-----------------------:|-----------:|------------:|
| Ideal  |             0.00750732 | 0.00218368 |   0.012831  |
| Noisy  |             0.00936279 | 0.00475871 |   0.0139669 |

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

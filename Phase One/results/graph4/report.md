# graph4 — O1 Max-Cut A/B experiment

**Processor coupling graphs are participant-defined; noise matches the Phase 1 Master Guide.**

- Graph: 5 nodes; 10 edges
- Exact classical optimal cut: 6
- p=1; statevector-optimized expected cut: 5.905212
- Shots per trial: 4096; trial seeds: 20

## A/B quality

| processor   | mode   |   trials |   mean_cut |     sd_cut |   ci95_low |   ci95_high |   mean_approximation_ratio |   mean_optimal_probability |   mean_best_sampled_cut |
|:------------|:-------|---------:|-----------:|-----------:|-----------:|------------:|---------------------------:|---------------------------:|------------------------:|
| A           | Ideal  |       20 |    5.902   | 0.0070137  |    5.89893 |     5.90508 |                   0.983667 |                   0.975488 |                       6 |
| A           | Noisy  |       20 |    5.79656 | 0.00991897 |    5.79221 |     5.8009  |                   0.966093 |                   0.923499 |                       6 |
| B           | Ideal  |       20 |    5.902   | 0.0070137  |    5.89893 |     5.90508 |                   0.983667 |                   0.975488 |                       6 |
| B           | Noisy  |       20 |    5.80718 | 0.00919911 |    5.80315 |     5.81121 |                   0.967863 |                   0.929053 |                       6 |

## Architecture metrics

| processor   |   physical_qubits |   depth |   cx_gates |   two_qubit_gates |   explicit_swaps |   circuit_width |   reference_depth |   reference_cx |   depth_overhead |   cx_overhead |
|:------------|------------------:|--------:|-----------:|------------------:|-----------------:|----------------:|------------------:|---------------:|-----------------:|--------------:|
| A           |                 5 |      60 |         35 |                35 |                0 |               5 |                30 |             20 |               30 |            15 |
| B           |                 9 |      47 |         29 |                29 |                0 |               9 |                30 |             20 |               17 |             9 |

## Paired A/B differences

| mode   |   difference_B_minus_A |   ci95_low |   ci95_high |
|:-------|-----------------------:|-----------:|------------:|
| Ideal  |              0         | 0          |     0       |
| Noisy  |              0.0106201 | 0.00818028 |     0.01306 |

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

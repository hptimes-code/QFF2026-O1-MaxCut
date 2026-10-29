# graph3 — O1 Max-Cut A/B experiment

**Processor coupling graphs are participant-defined; noise matches the Phase 1 Master Guide.**

- Graph: 5 nodes; 4 edges
- Exact classical optimal cut: 4
- p=1; statevector-optimized expected cut: 3.000000
- Shots per trial: 4096; trial seeds: 20

## A/B quality

| processor   | mode   |   trials |   mean_cut |    sd_cut |   ci95_low |   ci95_high |   mean_approximation_ratio |   mean_optimal_probability |   mean_best_sampled_cut |
|:------------|:-------|---------:|-----------:|----------:|-----------:|------------:|---------------------------:|---------------------------:|------------------------:|
| A           | Ideal  |       20 |    3.00039 | 0.0151096 |    2.99377 |     3.00701 |                   0.750098 |                   0.451257 |                       4 |
| A           | Noisy  |       20 |    2.92695 | 0.0163931 |    2.91977 |     2.93414 |                   0.731738 |                   0.417029 |                       4 |
| B           | Ideal  |       20 |    3.00205 | 0.0215324 |    2.99261 |     3.01149 |                   0.750513 |                   0.451648 |                       4 |
| B           | Noisy  |       20 |    2.92841 | 0.0213368 |    2.91905 |     2.93776 |                   0.732101 |                   0.417627 |                       4 |

## Architecture metrics

| processor   |   physical_qubits |   depth |   cx_gates |   two_qubit_gates |   explicit_swaps |   circuit_width |   reference_depth |   reference_cx |   depth_overhead |   cx_overhead |
|:------------|------------------:|--------:|-----------:|------------------:|-----------------:|----------------:|------------------:|---------------:|-----------------:|--------------:|
| A           |                 5 |      29 |         11 |                11 |                0 |               5 |                21 |              8 |                8 |             3 |
| B           |                 9 |      26 |         11 |                11 |                0 |               9 |                21 |              8 |                5 |             3 |

## Paired A/B differences

| mode   |   difference_B_minus_A |    ci95_low |   ci95_high |
|:-------|-----------------------:|------------:|------------:|
| Ideal  |             0.00166016 | -0.00275708 |  0.00607739 |
| Noisy  |             0.00145264 | -0.00281838 |  0.00572366 |

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

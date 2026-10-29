# graph2 — O1 Max-Cut A/B experiment

**Processor coupling graphs are participant-defined; noise matches the Phase 1 Master Guide.**

- Graph: 5 nodes; 5 edges
- Exact classical optimal cut: 4
- p=1; statevector-optimized expected cut: 3.750000
- Shots per trial: 4096; trial seeds: 20

## A/B quality

| processor   | mode   |   trials |   mean_cut |    sd_cut |   ci95_low |   ci95_high |   mean_approximation_ratio |   mean_optimal_probability |   mean_best_sampled_cut |
|:------------|:-------|---------:|-----------:|----------:|-----------:|------------:|---------------------------:|---------------------------:|------------------------:|
| A           | Ideal  |       20 |    3.74922 | 0.0112438 |    3.74429 |     3.75415 |                   0.937305 |                   0.878906 |                       4 |
| A           | Noisy  |       20 |    3.63608 | 0.0115354 |    3.63103 |     3.64114 |                   0.909021 |                   0.822974 |                       4 |
| B           | Ideal  |       20 |    3.74644 | 0.0105168 |    3.74183 |     3.75104 |                   0.936609 |                   0.877515 |                       4 |
| B           | Noisy  |       20 |    3.65894 | 0.0123277 |    3.65353 |     3.66434 |                   0.914734 |                   0.834119 |                       4 |

## Architecture metrics

| processor   |   physical_qubits |   depth |   cx_gates |   two_qubit_gates |   explicit_swaps |   circuit_width |   reference_depth |   reference_cx |   depth_overhead |   cx_overhead |
|:------------|------------------:|--------:|-----------:|------------------:|-----------------:|----------------:|------------------:|---------------:|-----------------:|--------------:|
| A           |                 5 |      35 |         19 |                19 |                0 |               5 |                24 |             10 |               11 |             9 |
| B           |                 9 |      25 |         11 |                11 |                0 |               9 |                24 |             10 |                1 |             1 |

## Paired A/B differences

| mode   |   difference_B_minus_A |    ci95_low |   ci95_high |
|:-------|-----------------------:|------------:|------------:|
| Ideal  |             -0.0027832 | -0.00709242 |  0.00152601 |
| Noisy  |              0.0228516 |  0.0173461  |  0.028357   |

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

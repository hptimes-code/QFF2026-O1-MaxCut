# Guide interpretation and open requirements

The Phase 1 Master Guide explicitly permits custom coupling maps for Processor A (5q) and B (9q); the configured noise rates and basis gates follow its page 2 baseline.

PS-O1 on page 4 specifies a six-node weighted instance, while Processor A has only five physical qubits. We therefore include a Processor B-only six-node experiment and separate A/B experiments on graphs fitting both machines. This is a physical capacity limitation, not a claim of completing a six-node A/B run.

The guide requests an end-to-end `main.ipynb` and `results/tables/` plus `results/figures/`, which are supplied by this update after running the notebook/export script.

Routing-stage inserted SWAPs are not directly measured by the native final-circuit `explicit_swaps` field. Quantitative depth/CX excess is provided but cannot be relabeled as the exact inserted-SWAP count.

Submission portal: https://qffsrmap2026.com/learning/hackathon. Deadline: 14 October 2026 at 23:59 IST. Confirm any required team details, and comply with any AI-use declaration in the actual portal.

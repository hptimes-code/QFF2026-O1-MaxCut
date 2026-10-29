# Source and result audit notes (11 October 2026)

## Checks completed

- Inspected actual `main.py` and all modules in `src/` from the uploaded ZIP.
- Checked requirements include `tabulate`, which `pandas.DataFrame.to_markdown()` needs.
- Syntax compilation completed for the Python files (not equivalent to running Qiskit).
- Four graph JSON files and A/B illustrative JSON processor definitions are present.
- Read all four `metadata.json`, `summary.csv`, `architecture.csv`, `paired_comparison.csv` and `trials.csv` datasets.
- All four trials tables contain exactly 80 distinct `(processor,mode,trial)` combinations: 2 processors × 2 modes × 20 trials.
- Independently recomputed trial means and B-minus-A means from `trials.csv`; the saved reported values match.
- Added `report.md` and strengthened `README.md` to consolidate the four-graph findings.

## Important limitations / further work

1. No local Qiskit execution or Windows clean-install verification performed during this audit. The user has separately demonstrated successful Qiskit runs on Windows.
2. The A/B configurations are intentionally illustrative; exact official configurations and O1 challenge instance have not been verified.
3. The source calculates approximate `mean ± 1.96·SE` intervals from trial samples. For just 20 trials, Student-t intervals or bootstrap intervals could be considered, especially for formal inference, with caveats about the shared RNG seeds. A zero-width interval (G4 ideal) can occur because seeded simulator outputs were identical; do not interpret it as absolute certainty.
4. Seed matching alone does not guarantee correctly controlled random-number pairing for differently compiled quantum circuits. A/B results should be described as simulator estimates. A stronger statistical design would use truly independent A/B replicates and explicitly compare two-sample or valid paired confidence intervals.
5. `explicit_swaps=0` under a CX native gate basis does not mean no routing. The resource gap relative to all-to-all reference is a proxy, not exact SWAP accounting.
6. The pipeline currently hardwires `noise_model()` with uniform synthetic noise; organizer-specific per-qubit/per-edge noise specifications, directional couplings, target capabilities, and official device instructions are **not yet supported**.
7. Each rerun overwrites that graph's results folder. Preserve archived experimental results before smoke tests.
8. `load_graph` allows a JSON-provided name as an output directory. Use unique safe graph names and trusted input files for reproducible local tests.
9. Some constraints depend on graph size: controlled A/B comparisons on these examples are capped at 5 vertices; this is not an arbitrary algorithm-wide limit.
10. QAOA parameters were optimized on the ideal statevector once per graph and then held fixed across A/B and noisy/ideal runs. They were *not* optimized separately under noise on each processor.

## Recommended next actions

1. Ask organizers for official O1 instance(s), coupling maps, gate bases, noise specifications, report format and required disclosure language.
2. Test environment isolation: `python -c "import sys; print(sys.executable)"` must show this project's `.venv`.
3. After confirming official requirements, implement official processor/noise config loading and rerun a controlled benchmark under organizer-defined settings.
4. Run from a fresh environment and verify generated files against saved metadata and reports.
5. Confirm GitHub upload, repository naming/access and AI disclosure as required.

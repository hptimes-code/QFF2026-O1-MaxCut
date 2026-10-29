
"""QFF 2026 Phase 2 / PS-O1: Reproducible p=1 QAOA, seeds 0-4."""

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

from qff_phase2 import (
    PROCESSOR_A, PROCESSOR_B, SEED, SHOTS,
    circuit_metrics, counts_to_x, load_processor,
    simulator, transpile_for, validate_processor_d,
)

ROOT = Path(__file__).resolve().parent

# Load official locked PS-O1 instance
instance_path = ROOT / "data" / "instance.json"

if not instance_path.exists():
    instance_path = ROOT / "instances.json"

instance = json.loads(instance_path.read_text(encoding="utf-8"))

if "PS-O1" in instance:
    instance = instance["PS-O1"]

n = instance["num_vertices"]
edges = [
    (int(u), int(v), float(w))
    for u, v, w in instance["weighted_edges"]
]
seeds = instance["initialization_seeds"]

assert n == 6 and seeds == [0, 1, 2, 3, 4]
assert SHOTS == 4096 and SEED == 42

# Load custom Processor D
processor_path = ROOT / "processors" / "processor_D.json"

if not processor_path.exists():
    processor_path = ROOT / "processor_D.json"

processor_d = load_processor(str(processor_path))

violations = validate_processor_d(processor_d, n)

if violations:
    raise ValueError(
        "Processor D invalid: " + "; ".join(violations)
    )


# Classical exact Max-Cut solver
def cut_integer(bitmask):
    return sum(
        w for u, v, w in edges
        if ((bitmask >> u) & 1) != ((bitmask >> v) & 1)
    )


costs = np.array(
    [cut_integer(i) for i in range(2 ** n)],
    dtype=float
)

optimum = float(costs.max())

optimal_bitmasks = set(
    np.flatnonzero(np.isclose(costs, optimum)).tolist()
)

# Uniform-random baseline
random_mean_cut = float(costs.mean())
random_ratio = random_mean_cut / optimum
random_p_opt = len(optimal_bitmasks) / (2 ** n)

print("Locked PS-O1: vertices =", n, ", edges =", len(edges))
print("Exact maximum cut =", optimum)
print("Optimal states =", len(optimal_bitmasks))

print(
    "Optimal bitstrings (q5...q0) =",
    [format(i, f"0{n}b") for i in sorted(optimal_bitmasks)]
)

print("\nUniform-random baseline:")
print(f"Mean cut = {random_mean_cut:.4f}")
print(f"Approximation ratio = {random_ratio:.4f}")
print(f"P(opt) = {random_p_opt:.5f}")


# QAOA circuit (p=1)
def qaoa(gamma, beta, measure=True):
    qc = QuantumCircuit(n)
    qc.h(range(n))

    for u, v, w in edges:
        qc.cx(u, v)
        qc.rz(-gamma * w, v)
        qc.cx(u, v)

    for q in range(n):
        qc.rx(2 * beta, q)

    if measure:
        qc.measure_all()

    return qc


# Exact ideal expectation
def expectation(params):
    gamma, beta = params

    probabilities = Statevector.from_instruction(
        qaoa(gamma, beta, False)
    ).probabilities()

    return float(costs @ probabilities)


# Metrics calculated from measurement counts
def shot_metrics(counts):
    total = sum(counts.values())

    total_cut = 0.0
    optimal_count = 0
    sampled_best = 0.0

    for key, count in counts.items():
        bits = counts_to_x(key)

        # x[0] corresponds to qubit 0
        mask = sum(
            int(bit) << i
            for i, bit in enumerate(bits)
        )

        value = float(costs[mask])

        total_cut += value * count
        optimal_count += int(mask in optimal_bitmasks) * count
        sampled_best = max(sampled_best, value)

    mean_cut = total_cut / total

    return dict(
        mean_cut=mean_cut,
        approximation_ratio=mean_cut / optimum,
        p_opt=optimal_count / total,
        best_sampled_cut=sampled_best,
        r_best=sampled_best / optimum,
    )


# Output directory
out_dir = ROOT / "results" / "tables"
out_dir.mkdir(parents=True, exist_ok=True)

rows = []
params_rows = []

# Five seeded QAOA optimizations
for seed in seeds:
    rng = np.random.default_rng(seed)

    # Both parameters initialized in [0, pi]
    x0 = [
        rng.uniform(0, np.pi),
        rng.uniform(0, np.pi),
    ]

    opt = minimize(
        lambda p: -expectation(p),
        x0,
        method="COBYLA",
        options={
            "maxiter": 120,
            "rhobeg": 0.25,
        },
    )

    gamma, beta = map(float, opt.x)
    ideal_exact = expectation(opt.x)

    params_rows.append(dict(
        seed=seed,
        initial_gamma=float(x0[0]),
        initial_beta=float(x0[1]),
        gamma=gamma,
        beta=beta,
        optimizer="COBYLA",
        iterations=opt.nfev,
        ideal_exact_expectation=ideal_exact,
        optimization_success=bool(opt.success),
    ))

    print(
        f"\nseed={seed}: "
        f"gamma={gamma:.6f}, "
        f"beta={beta:.6f}, "
        f"ideal expectation={ideal_exact:.6f}"
    )

    logical = qaoa(gamma, beta, True)

    # Evaluate official Processor A/B and custom D
    for processor in (PROCESSOR_A, PROCESSOR_B, processor_d):
        name = processor["name"]
        resource = circuit_metrics(logical, processor)

        if not resource["executable"]:
            print(name, ": not executable (capacity)")

            rows.append(dict(
                seed=seed,
                mode="N/A",
                status="not executable (capacity)",
                **resource,
            ))
            continue

        compiled = transpile_for(logical, processor)

        for noisy in (False, True):
            sim = simulator(noisy, processor)

            counts = sim.run(
                compiled,
                shots=SHOTS,
                seed_simulator=SEED,
            ).result().get_counts()

            values = shot_metrics(counts)
            mode = "Noisy" if noisy else "Ideal"

            rows.append(dict(
                seed=seed,
                mode=mode,
                status="ok",
                shots=SHOTS,
                simulator_seed=SEED,
                gamma=gamma,
                beta=beta,
                exact_optimum=optimum,
                random_mean_cut=random_mean_cut,
                random_approximation_ratio=random_ratio,
                random_p_opt=random_p_opt,
                **values,
                **resource,
            ))

            print(
                f"  {name:11s} {mode:5s}: "
                f"mean={values['mean_cut']:.4f}  "
                f"ratio={values['approximation_ratio']:.4f}  "
                f"P(opt)={values['p_opt']:.4f}  "
                f"r_best={values['r_best']:.4f}  "
                f"CX={resource['cx']} "
                f"depth={resource['depth']} "
                f"swaps={resource['swaps']}"
            )


# Save detailed results
results = pd.DataFrame(rows)

results.to_csv(
    out_dir / "results.csv",
    index=False
)

# Save optimization parameters
pd.DataFrame(params_rows).to_csv(
    out_dir / "qaoa_parameters.csv",
    index=False
)

# Summary across seeds
summary = (
    results[results["status"] == "ok"]
    .groupby(["processor", "mode"])[[
        "mean_cut",
        "approximation_ratio",
        "p_opt",
        "r_best",
        "cx",
        "depth",
        "swaps",
        "cx_overhead",
    ]]
    .agg(["mean", "std"])
)

summary.columns = [
    f"{metric}_{stat}"
    for metric, stat in summary.columns
]

summary = summary.reset_index()

summary.to_csv(
    out_dir / "qaoa_summary.csv",
    index=False
)

# Classical baseline CSV
baseline = pd.DataFrame([{
    "vertices": n,
    "edges": len(edges),
    "exact_optimum": optimum,
    "optimal_states": len(optimal_bitmasks),
    "random_mean_cut": random_mean_cut,
    "random_approximation_ratio": random_ratio,
    "random_p_opt": random_p_opt,
}])

baseline.to_csv(
    out_dir / "classical_baseline.csv",
    index=False
)

print("\nSaved:", out_dir / "results.csv")
print("Saved:", out_dir / "qaoa_parameters.csv")
print("Saved:", out_dir / "qaoa_summary.csv")
print("Saved:", out_dir / "classical_baseline.csv")

print("\nSummary across optimization seeds:")
print(summary.to_string(index=False))

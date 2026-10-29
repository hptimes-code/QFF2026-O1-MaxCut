import numpy as np
import pandas as pd
from qiskit_aer import AerSimulator
from .graphs import cut_value
from .processors import noise_model, circuit_metrics, reference_circuit


def evaluate(counts, graph, optimal):
    total = sum(counts.values())
    mean = sum(cut_value(b, graph) * k for b, k in counts.items()) / total
    prob = sum(k for b, k in counts.items() if abs(cut_value(b, graph)-optimal) < 1e-8) / total
    return {'mean_cut': mean, 'best_sampled_cut': max(cut_value(b, graph) for b in counts),
            'approximation_ratio': mean/optimal, 'optimal_probability': prob}


def run_validation(graph, optimum, compiled, configs, shots, trials, seed):
    rows, arch = [], []
    ideal, noisy = AerSimulator(), AerSimulator(noise_model=noise_model())
    for label, qc in compiled.items():
        for mode, sim in (('Ideal', ideal), ('Noisy', noisy)):
            for trial in range(trials):
                outcome = sim.run(qc, shots=shots, seed_simulator=seed+trial).result().get_counts()
                rows.append({'processor': label, 'mode': mode, 'trial': trial+1,
                             'seed': seed+trial, 'shots': shots,
                             **evaluate(outcome, graph, optimum)})
    data = pd.DataFrame(rows)
    summaries = []
    for (label, mode), part in data.groupby(['processor', 'mode']):
        n = len(part)
        mean = part.mean_cut.mean()
        sd = part.mean_cut.std(ddof=1) if n > 1 else 0.0
        se = sd / np.sqrt(n)
        summaries.append({'processor': label, 'mode': mode, 'trials': n,
                          'mean_cut': mean, 'sd_cut': sd,
                          'ci95_low': mean-1.96*se, 'ci95_high': mean+1.96*se,
                          'mean_approximation_ratio': part.approximation_ratio.mean(),
                          'mean_optimal_probability': part.optimal_probability.mean(),
                          'mean_best_sampled_cut': part.best_sampled_cut.mean()})
    summary = pd.DataFrame(summaries)
    if not {'A', 'B'}.issubset(compiled):
        # For the required six-node O1 graph, Processor A has only five qubits.
        # A B-only run is valid but must never fabricate an A/B paired difference.
        return data, summary, pd.DataFrame(columns=['mode','difference_B_minus_A','ci95_low','ci95_high'])
    paired = data.pivot(index=['mode','seed'], columns='processor', values='mean_cut').reset_index()
    diffrows = []
    for mode, part in paired.groupby('mode'):
        d = part.B - part.A
        se = d.std(ddof=1)/np.sqrt(len(d)) if len(d) > 1 else 0
        diffrows.append({'mode': mode, 'difference_B_minus_A': d.mean(),
                         'ci95_low': d.mean()-1.96*se, 'ci95_high': d.mean()+1.96*se})
    return data, summary, pd.DataFrame(diffrows)

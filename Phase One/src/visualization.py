
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
import networkx as nx


def plot_graph(graph, solution, path):
    g = nx.Graph()
    g.add_nodes_from(range(graph['n']))
    g.add_weighted_edges_from(graph['edges'])

    colors = ['skyblue' if bit == 0 else 'orange' for bit in solution]

    fig, ax = plt.subplots(figsize=(6, 5))
    nx.draw_networkx(
        g,
        pos=nx.spring_layout(g, seed=42),
        node_color=colors,
        with_labels=True,
        node_size=850,
        ax=ax
    )

    ax.set_title(f"{graph['name']}: classical optimal partition")
    ax.axis('off')
    fig.tight_layout()
    fig.savefig(path, dpi=170)
    plt.close(fig)


def plot_results(summary, arch, out):
    # Detect which processors were used in the experiment.
    processors = [
        p for p in ('A', 'B')
        if p in arch['processor'].values
    ]

    if not processors:
        raise ValueError("No processor results available for plotting.")

    x = np.arange(len(processors))

    # Plot 1: Ideal and noisy mean Max-Cut
    fig, ax = plt.subplots(figsize=(8, 5))

    for offset, mode in [(-0.18, 'Ideal'), (0.18, 'Noisy')]:
        d = (
            summary[summary['mode'] == mode]
            .set_index('processor')
            .reindex(processors)
        )

        if d['mean_cut'].isna().any():
            raise ValueError(f"Missing {mode} results for a processor.")

        err = (
            d['ci95_high'] - d['mean_cut']
        ).to_numpy()

        ax.bar(
            x + offset,
            d['mean_cut'].to_numpy(),
            width=0.35,
            yerr=err,
            capsize=4,
            label=mode
        )

    ax.set_xticks(x, processors)
    ax.set_ylabel('Average Max-Cut')
    ax.set_title('Mean Max-Cut (95% CI)')
    ax.legend()
    fig.tight_layout()
    fig.savefig(out / 'cut_comparison.png', dpi=170)
    plt.close(fig)

    # Plot 2: Circuit depth and CX gates
    a = arch.set_index('processor').reindex(processors)

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.bar(
        x - 0.18,
        a['depth'].to_numpy(),
        0.35,
        label='Circuit depth'
    )

    ax.bar(
        x + 0.18,
        a['cx_gates'].to_numpy(),
        0.35,
        label='CX gates'
    )

    ax.set_xticks(x, processors)
    ax.set_title('Circuit Resources')
    ax.legend()
    fig.tight_layout()
    fig.savefig(out / 'architecture.png', dpi=170)
    plt.close(fig)

    # Plot 3: Compilation overhead
    fig, ax = plt.subplots(figsize=(8, 5))

    ax.bar(
        x - 0.18,
        a['depth_overhead'].to_numpy(),
        0.35,
        label='Extra depth'
    )

    ax.bar(
        x + 0.18,
        a['cx_overhead'].to_numpy(),
        0.35,
        label='Extra CX'
    )

    ax.axhline(0, linewidth=1)
    ax.set_xticks(x, processors)
    ax.set_title('Compilation Overhead vs Fully Connected Reference')
    ax.legend()
    fig.tight_layout()
    fig.savefig(out / 'compilation_overhead.png', dpi=170)
    plt.close(fig)

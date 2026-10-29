"""Draw the two participant-designed architectures used in Phase 1."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / 'results' / 'figures'
OUT.mkdir(parents=True, exist_ok=True)
for label in ('A', 'B'):
    config = json.loads((BASE / 'processors' / f'processor_{label}.json').read_text(encoding='utf-8'))
    G = nx.Graph()
    G.add_nodes_from(range(config['num_qubits']))
    G.add_edges_from(config['coupling_map'])
    fig, ax = plt.subplots(figsize=(6, 4))
    nx.draw_networkx(G, nx.spring_layout(G, seed=42), ax=ax, with_labels=True,
                     node_size=650, font_weight='bold')
    ax.set_title(f'Processor {label}: {G.number_of_nodes()} qubits, {G.number_of_edges()} links')
    ax.axis('off')
    fig.savefig(OUT / f'processor_{label}_coupling.png', dpi=160, bbox_inches='tight')
    plt.close(fig)
print('Created Processor A/B coupling diagram PNGs in', OUT)

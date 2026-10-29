"""Generate PS-O1 six-node weighted Erdős–Rényi instance reproducibly."""
import json
from pathlib import Path
import networkx as nx
import random


def main():
    graph = nx.erdos_renyi_graph(n=6, p=0.5, seed=42)
    rng = random.Random(42)
    edges = [[int(u), int(v), rng.randint(1,5)] for u,v in sorted(graph.edges())]
    payload = {'name':'o1_weighted_6node','num_nodes':6,'edges':edges}
    target = Path(__file__).resolve().parents[1]/'data'/'raw'/'o1_weighted_6node.json'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload,indent=2)+'\n',encoding='utf-8')
    print('Created',target,'edges:',len(edges))


if __name__ == '__main__':
    main()

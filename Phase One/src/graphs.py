import json
from pathlib import Path
from itertools import product


def load_graph(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    n = data.get("num_nodes")
    if type(n) is not int or n < 2:
        raise ValueError("num_nodes must be an integer >= 2")
    edges = []
    seen = set()
    for edge in data.get("edges", []):
        if len(edge) not in (2, 3):
            raise ValueError("Edges must be [u,v] or [u,v,weight]")
        u, v = edge[:2]
        w = edge[2] if len(edge) == 3 else 1.0
        if any(type(x) is not int or not 0 <= x < n for x in (u, v)) or u == v:
            raise ValueError(f"Invalid edge: {edge}")
        if not isinstance(w, (int, float)) or isinstance(w, bool) or not 0 < float(w) < float('inf'):
            raise ValueError("Edge weights must be positive finite numbers")
        pair = tuple(sorted((u, v)))
        if pair in seen:
            raise ValueError(f"Duplicate edge: {edge}")
        seen.add(pair)
        edges.append((u, v, float(w)))
    if not edges:
        raise ValueError("Graph must contain at least one edge")
    return {"name": data.get("name", Path(path).stem), "n": n, "edges": edges}


def cut_value(bitstring, graph):
    # Qiskit prints the highest-index classical bit on the left.
    bits = [int(x) for x in bitstring.replace(' ', '')[::-1]]
    return sum(w for u, v, w in graph['edges'] if bits[u] != bits[v])


def exact_baseline(graph, max_nodes=18):
    n = graph['n']
    if n > max_nodes:
        raise ValueError(f"Exact brute-force baseline limited to {max_nodes} nodes")
    best, winners = -1.0, []
    for bits in product((0, 1), repeat=n):
        score = sum(w for u, v, w in graph['edges'] if bits[u] != bits[v])
        if score > best + 1e-9:
            best, winners = score, [bits]
        elif abs(score - best) <= 1e-9:
            winners.append(bits)
    return best, winners

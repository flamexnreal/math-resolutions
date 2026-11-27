"""Exact check of a 21-vertex counterexample to Du et al., Conjecture 3.1.

Run with Python 3.8 or later. Only the standard library is required.
"""

from collections import Counter
from itertools import combinations
from math import isqrt


N = 21
SUPPORTS = (
    (1, 2), (1, 2), (1, 3), (4, 5), (6, 7),
    (8, 9), (10, 12), (11, 12), (11, 12),
)


def witness():
    edges = {(i, j) for i, j in combinations(range(1, 13), 2) if j - i <= 2}
    for v, (a, b) in enumerate(SUPPORTS, start=13):
        assert (a, b) in edges and a < b < v
        edges.update(((a, v), (b, v)))
    return edges


def figure_four():
    # Number down each full column, top then bottom. The final top vertex
    # closes the triangle on the right of the tenth full column.
    edges = set()
    for k in range(10):
        top = 2 * k + 1
        bottom = top + 1
        edges.add((top, bottom))
        edges.add((top, top + 2))
        edges.add((bottom, top + 2))
        if k < 9:
            edges.add((bottom, bottom + 2))
    assert edges == {(a, b) for a, b in combinations(range(1, N + 1), 2)
                     if b - a <= 2}
    return edges


def check_two_tree(edges):
    assert all(1 <= u < v <= N for u, v in edges)
    remaining = set(edges)
    for v in range(N, 2, -1):
        neighbors = sorted(u for u, w in remaining if w == v)
        assert len(neighbors) == 2 and tuple(neighbors) in remaining
        for u in neighbors:
            remaining.remove((u, v))
    assert remaining == {(1, 2)}
    assert len(edges) == 2 * N - 3


def nonedge_weights(edges):
    degree = Counter(u for edge in edges for u in edge)
    weights = Counter()
    for u, v in combinations(range(1, N + 1), 2):
        if (u, v) not in edges:
            weights[degree[u] ** 2 + degree[v] ** 2] += 1
    return weights


def radical_sum(weights):
    # Store each term as coefficient * sqrt(square-free radicand).
    terms = Counter()
    for r, count in weights.items():
        factor = max(d for d in range(1, isqrt(r) + 1) if r % (d * d) == 0)
        terms[r // (factor * factor)] += count * factor
    return terms


def enclose(terms, scale):
    low = high = 0
    for r, coefficient in terms.items():
        scaled_square = r * scale * scale
        a = isqrt(scaled_square)
        b = a if a * a == scaled_square else a + 1
        low += min(coefficient * a, coefficient * b)
        high += max(coefficient * a, coefficient * b)
    return low, high


def main():
    g, h = witness(), figure_four()
    for edges in (g, h):
        check_two_tree(edges)
    gw, hw = nonedge_weights(g), nonedge_weights(h)
    assert sum(gw.values()) == sum(hw.values()) == 171
    gs, hs = radical_sum(gw), radical_sum(hw)
    assert gs == {2: 297, 29: 90}
    assert hs == {1: 150, 2: 425, 5: 64, 13: 2}

    # Collect the terms in the published upper bound on page 18992.
    printed = {1: 10*N - 60, 2: 2*N*N - 26*N*N + 89, 5: 4*N - 20, 13: 2}
    h_minus_printed = hs.copy()
    h_minus_printed.subtract(printed)
    assert {r: c for r, c in h_minus_printed.items() if c} == {2: 10920}

    gap = gs.copy()
    gap.subtract(hs)
    scale = 10**6
    low, high = enclose(gap, scale)
    assert low > 0
    print("G and H: two-tree deletion checks passed; 21 vertices, 39 edges, 171 nonedges each")
    print("G coindex = 297*sqrt(2) + 90*sqrt(29)")
    print("H coindex = 150 + 425*sqrt(2) + 64*sqrt(5) + 2*sqrt(13)")
    print(f"Certified gap: {low}/{scale} <= coindex(G)-coindex(H) <= {high}/{scale}")
    print("coindex(H) - printed upper bound = 10920*sqrt(2)")


if __name__ == "__main__":
    main()

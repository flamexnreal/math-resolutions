"""Verify the double-star counterexample from its edge list using exact arithmetic."""

from collections import deque
from fractions import Fraction
from itertools import combinations
from math import isqrt


VERTICES = range(26)
EDGES = [(0, 1)] + [(0, v) for v in range(2, 14)] + [(1, v) for v in range(14, 26)]


def distances(adjacency, start):
    distance = {start: 0}
    queue = deque([start])
    while queue:
        u = queue.popleft()
        for v in adjacency[u]:
            if v not in distance:
                distance[v] = distance[u] + 1
                queue.append(v)
    return distance


def upper_bound(counts):
    scale = 10**6
    total = Fraction()
    for u, v in EDGES:
        a, b = counts[u], counts[v]
        scaled_radicand = scale * scale * 4 * a * b
        numerator = isqrt(scaled_radicand)
        if numerator * numerator < scaled_radicand:
            numerator += 1
        total += Fraction(numerator, scale * (a + b))
    return total


def main():
    adjacency = {v: set() for v in VERTICES}
    for u, v in EDGES:
        assert u < v and v not in adjacency[u]
        adjacency[u].add(v)
        adjacency[v].add(u)

    distance_maps = {u: distances(adjacency, u) for u in VERTICES}
    assert all(len(distance) == len(VERTICES) for distance in distance_maps.values())
    assert len(EDGES) == len(VERTICES) - 1

    # The complement of a minimum vertex cover is a maximum independent set.
    for size in range(len(VERTICES) + 1):
        if any(all(u in cover or v in cover for u, v in EDGES)
               for cover in combinations(VERTICES, size)):
            independence = len(VERTICES) - size
            break
    assert independence == 24

    for include_start in (True, False):
        counts = {
            u: sum((0 if include_start else 1) <= d <= 2 for d in distance.values())
            for u, distance in distance_maps.items()
        }
        bound = upper_bound(counts)
        assert bound < independence
        label = "including" if include_start else "excluding"
        print(f"RGA {label} the starting vertex <= {bound} < {independence}")


if __name__ == "__main__":
    main()

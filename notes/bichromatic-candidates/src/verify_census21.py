"""Standalone exact certificate for census order 21; Python standard library only."""

import json
import sys
from itertools import combinations
from pathlib import Path

RECORD = "Tl?GWCJ@oB?Jp?AIK?P?@K?C?JoWEG?WySUH"
RIM = [0, 1, 2, 3]
WIDTH = 250
POINTS = [
    (0, 0), (250, 0), (250, 250), (0, 250), (125, 124), (119, 120), (121, 126),
    (121, 130), (125, 128), (114, 129), (128, 133), (117, 134), (132, 90), (130, 127),
    (189, 128), (168, 169), (128, 190), (144, 130), (130, 118), (129, 148), (92, 133),
]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def det(a, b, c):
    x, y = POINTS[a]
    u, v = POINTS[b]
    s, t = POINTS[c]
    return (u - x) * (t - y) - (v - y) * (s - x)


def same_side(e, f):
    return det(*e, f[0]) * det(*e, f[1]) > 0


def cyclic_key(face):
    a, b, c = face
    return min((a, b, c), (b, c, a), (c, a, b))


def verify(referee_json=None):
    digits = [ord(c) - 63 for c in RECORD]
    n = digits[0]
    require(n == 21 and len(digits) == 36 and all(0 <= d < 64 for d in digits),
            "invalid short graph6")
    vertices = range(n)
    pairs = ((u, v) for v in vertices for u in range(v))
    bits = ((d >> i) & 1 for d in digits[1:] for i in range(5, -1, -1))
    edges = {e for e, bit in zip(pairs, bits, strict=True) if bit}
    adj = [{b if a == v else a for a, b in edges if v in (a, b)} for v in vertices]

    require({(a, b) for a, b in edges if a in RIM and b in RIM}
            == {(0, 1), (1, 2), (2, 3), (0, 3)}, "boundary is not an induced 4-cycle")
    require(all(len(adj[v]) >= 5 for v in vertices if v not in RIM), "low inside degree")
    require(len(POINTS) == len(set(POINTS)) == n, "repeated or missing point")
    require([POINTS[v] for v in RIM] == [(0, 0), (WIDTH, 0), (WIDTH, WIDTH), (0, WIDTH)]
            and WIDTH > 0, "not the specified square")
    require(all(0 < x < WIDTH and 0 < y < WIDTH for x, y in POINTS[4:]), "not inside square")
    require(all(det(*e, v) != 0 for e in edges for v in vertices if v not in e),
            "vertex on a nonincident edge line")
    require(all(same_side(e, f) or same_side(f, e)
                for e, f in combinations(edges, 2) if set(e).isdisjoint(f)), "edge crossing")

    faces = [(a, b, c) if det(a, b, c) > 0 else (a, c, b)
             for a, b, c in combinations(vertices, 3)
             if b in adj[a] and c in adj[b] and c in adj[a]]
    for a, b, c in faces:
        require(det(a, b, c) > 0, "degenerate face")
        require(all(min(det(a, b, v), det(b, c, v), det(c, a, v)) < 0
                    for v in vertices if v not in (a, b, c)), "vertex in a face")
    require(sum(det(*face) for face in faces) == 2 * WIDTH**2, "square not filled")

    if referee_json is not None:
        given = json.loads(referee_json.read_text())
        require(given["outer"] == RIM and given["source"]["graph6"] == RECORD
                and sorted(map(tuple, given["edges"])) == sorted(edges)
                and sorted(map(cyclic_key, given["triangles"])) == sorted(map(cyclic_key, faces)),
                "certificate differs from referee input")

    require({0, 1} <= adj[12], "vertex 12 cannot name the third color")
    colored = {0: 0, 1: 1, 2: 0, 3: 1, 12: 2}
    palette = set(range(4))
    for v in (14, 20, 16, 15, 17, 19):
        possible = palette - {colored[w] for w in adj[v] if w in colored}
        if v == 19:
            require(not possible, "vertex 19 has a color")
        else:
            require(len(possible) == 1, f"vertex {v} not forced")
            colored[v] = possible.pop()

    later = (3, 4, 12)
    gap = n - 4 - 12
    require(0 < gap < 2 * min(later) and gap not in later, "order obstruction failed")
    print(f"Verified: {n} vertices, {len(edges)} edges, {len(faces)} bounded faces; "
          "alternating boundary impossible, projected order unreachable.")


if __name__ == "__main__":
    if len(sys.argv) > 2:
        sys.exit(f"Usage: {sys.argv[0]} [referee-json]")
    verify(Path(sys.argv[1]) if len(sys.argv) == 2 else None)

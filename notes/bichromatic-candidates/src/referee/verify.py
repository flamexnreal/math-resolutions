"""Exact disk and boundary-color checks for Conjecture 30 (standard library)."""

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def unique_object(pairs):
    obj = dict(pairs)
    require(len(obj) == len(pairs), "duplicate JSON key")
    return obj


def cycle(walk):
    return zip(walk, (*walk[1:], walk[0]))


def edge(u, v):
    return (min(u, v), max(u, v))


def cliquesthree(adj):
    return {(u, v, w) for u in adj for v in adj[u] if u < v
            for w in adj[u] & adj[v] if v < w}


def adjacency(edges):
    adj = defaultdict(set)
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    return dict(adj)


def connected(adj):
    if not adj:
        return False
    pending = [next(iter(adj))]
    seen = set(pending)
    while pending:
        new = adj[pending.pop()] - seen
        pending.extend(new)
        seen.update(new)
    return seen == adj.keys()


def check_disk(data):
    def labels(row, length):
        require(type(row) is list and len(row) == length
                and all(type(v) is int for v in row) and len(set(row)) == length,
                f"invalid vertex tuple: {row}")
        return tuple(row)

    outer = labels(data["outer"], 4)
    edges = [edge(*labels(row, 2)) for row in data["edges"]]
    faces = [labels(row, 3) for row in data["triangles"]]
    require(len(set(edges)) == len(edges), "duplicate undirected edge")
    adj = adjacency(edges)
    require(connected(adj), "disconnected graph")
    rim = set(outer)
    sides = set(cycle(outer))
    require({edge(*uv) for uv in sides} <= set(edges), "outer cycle edge absent")
    face_sets = {tuple(sorted(f)) for f in faces}
    require(len(face_sets) == len(faces), "duplicate unordered triangle")
    require(face_sets == cliquesthree(adj), "listed faces are not exactly graph triangles")
    darts = Counter(uv for f in faces for uv in cycle(f))
    for u, v in edges:
        uv, vu = (u, v), (v, u)
        if uv in sides or vu in sides:
            require((darts[uv], darts[vu]) == (int(uv in sides), int(vu in sides)),
                    f"wrong boundary incidence/orientation at {u, v}")
        else:
            require(darts[uv] == darts[vu] == 1,
                    f"wrong interior incidence/orientation at {u, v}")

    links = defaultdict(list)
    for f in faces:
        for i, v in enumerate(f):
            links[v].append(edge(f[i - 1], f[i - 2]))
    for v in adj:
        link = adjacency(links[v])
        require(link.keys() == adj[v] and connected(link), f"bad link at {v}")
        if v in rim:
            i = outer.index(v)
            ends = {outer[i - 1], outer[(i + 1) % 4]}
        else:
            ends = set()
        require(all(len(link[w]) == (1 if w in ends else 2) for w in link),
                f"bad link degrees at {v}")
    require(len(adj) - len(edges) + len(faces) == 1, "wrong disk Euler characteristic")
    require(all(len(adj[v]) >= 5 for v in adj.keys() - rim), "internal degree below five")
    return outer, adj


def find_coloring(adj, fixed):
    """Return one proper 4-coloring (colors 0..3), or None after exact search."""
    assigned = dict(fixed)
    require(assigned.keys() <= adj.keys() and set(assigned.values()) <= set(range(4)),
            "invalid pinned colors")
    if any(assigned[v] == assigned.get(w) for v in assigned for w in adj[v]):
        return None

    def search():
        if len(assigned) == len(adj):
            return dict(assigned)
        choices = [(set(range(4)) - {assigned[w] for w in adj[v] if w in assigned}, v)
                   for v in adj.keys() - assigned.keys()]
        colors, v = min(choices, key=lambda p: (len(p[0]), -len(adj[p[1]]), p[1]))
        for color in sorted(colors):
            assigned[v] = color
            found = search()
            if found is not None:
                return found
        assigned.pop(v, None)
        return None

    found = search()
    if found is not None:
        require(found.keys() == adj.keys() and
                all(found[v] != found[w] for v in adj for w in adj[v]) and
                all(found[v] == color for v, color in fixed.items()), "bad color certificate")
    return found


def canvas_from_graph6(record):
    """Decode a short graph6 record and recover all oriented triangle faces."""
    raw = [ord(c) - 63 for c in record]
    require(raw and all(0 <= k < 64 for k in raw), "invalid graph6 characters")
    n = raw[0]
    length = n * (n - 1) // 2
    require(3 < n <= 62 and len(raw) == 1 + (length + 5) // 6, "bad short graph6 length")
    bits = [(k >> j) & 1 for k in raw[1:] for j in reversed(range(6))]
    require(not any(bits[length:]), "nonzero graph6 padding")
    pairs = ((u, v) for v in range(n) for u in range(v))
    edges = [uv for uv, bit in zip(pairs, bits) if bit]
    adj = adjacency(edges)
    require(adj.keys() == set(range(n)), "graph6 contains isolated vertex")
    incident = defaultdict(list)
    ts = cliquesthree(adj)
    for t in ts:
        for uv in cycle(t):
            incident[edge(*uv)].append(t)
    require(incident and all(len(uses) in (1, 2) for uses in incident.values()),
            "triangle incidence incompatible with disk")
    first = min(ts)
    oriented = {first: first}
    pending = [first]
    rim_next = {}
    while pending:
        face = pending.pop()
        cur = tuple(sorted(face))
        for u, v in cycle(face):
            uses = incident[edge(u, v)]
            if len(uses) == 1:
                require(u not in rim_next, "ambiguous graph6 boundary")
                rim_next[u] = v
                continue
            a, b = uses
            other = b if a == cur else a
            if other not in oriented:
                third, = set(other) - {u, v}
                oriented[other] = (v, u, third)
                pending.append(oriented[other])
    require(oriented.keys() == ts and len(rim_next) == 4, "not a 4-canvas")
    outer = [min(rim_next)]
    for _ in range(3):
        require(outer[-1] in rim_next, "open graph6 boundary")
        outer.append(rim_next[outer[-1]])
    require(len(set(outer)) == 4 and rim_next.get(outer[-1]) == outer[0],
            "not a cyclic graph6 boundary")
    return dict(outer=outer, edges=list(map(list, edges)),
                triangles=list(map(list, oriented.values())))


def verify(data, expect_forbidding):
    outer, adj = check_disk(data)
    pins = dict(zip(outer, (0, 1, 0, 1), strict=True))
    pinned = find_coloring(adj, pins)
    rainbow = find_coloring(adj, dict(zip(outer, range(4), strict=True)))
    ordinary = rainbow if rainbow is not None else find_coloring(adj, {})
    require(ordinary is not None, "no ordinary proper 4-coloring")
    degrees = tuple(len(adj[v]) for v in outer)
    print(f"V={len(adj)}, E={sum(map(len, adj.values())) // 2}, "
          f"F_int={len(data['triangles'])}, boundary={outer}, degrees={degrees}")
    print(f"alternating={pinned}; {'rainbow' if rainbow is not None else 'ordinary'}={ordinary}")
    if expect_forbidding:
        require(pinned is None, "alternating coloring extends")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", type=Path)
    parser.add_argument("--census", type=Path, help="authors' raw bernard25.log")
    parser.add_argument("--forbidding", action="store_true", help="require pinned UNSAT")
    args = parser.parse_args()
    for path in args.inputs:
        print(path.name)
        data = json.loads(path.read_text(), object_pairs_hook=unique_object)
        verify(data, args.forbidding)
        if args.census and "source" in data:
            src = data["source"]
            line = args.census.read_text().splitlines()[src["line"] - 1]
            require(line == src["graph6"], "census record differs")
            decoded_outer, decoded_adj = check_disk(canvas_from_graph6(line))
            outer, adj = check_disk(data)
            require(decoded_adj == adj and {edge(*uv) for uv in cycle(decoded_outer)}
                    == {edge(*uv) for uv in cycle(outer)}, "census graph/outer differs")
            print(f"Census line {src['line']} independently decoded and checked")


if __name__ == "__main__":
    main()

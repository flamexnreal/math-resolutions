import copy
import unittest

from verify import check_disk, cycle, edge, find_coloring


def canvas(outer, triangles):
    return dict(outer=list(outer), triangles=list(map(list, triangles)),
                edges=[list(e) for e in sorted({edge(*uv) for t in triangles for uv in cycle(t)})])


DIAMOND = canvas(range(4), [(0, 1, 2), (0, 2, 3)])


def icosahedron_minus_edge():
    a, b = range(1, 6), range(6, 11)
    faces = []
    for i in range(5):
        j = (i + 1) % 5
        faces += [(a[j], a[i], b[i]), (b[i], a[i], b[i - 1]), (11, b[i], b[i - 1])]
        if i not in (0, 4):
            faces.append((0, a[i], a[j]))
    return canvas((0, 2, 1, 5), faces)


def collar(data, operation):
    v = data["outer"]
    start = max(w for row in data["edges"] for w in row) + 1
    t = list(map(tuple, data["triangles"]))
    if operation == 27:
        x, y, u = range(start, start + 4), range(start + 4, start + 8), range(start + 8, start + 12)
        for i in range(4):
            j = (i + 1) % 4
            t += [(v[j], v[i], x[i]), (v[j], x[i], y[i]), (v[j], y[i], x[j]),
                  (u[i], y[i], x[i]), (u[i], x[i], y[i - 1]), (u[i], u[j], y[i])]
    else:
        if operation == 29:
            old = next(f for f in t if {v[0], v[1]} <= set(f))
            t.remove(old)
            reused, = set(old) - {v[0], v[1]}
            u = [reused, *range(start, start + 3)]
        else:
            u = list(range(start, start + 4))
        for i in range(4):
            j = (i + 1) % 4
            if operation != 29 or i != 0:
                t.append((u[i], v[j], v[i]))
            t.append((u[i], u[j], v[j]))
    return canvas(u, t)


class Controls(unittest.TestCase):
    def test_pinned_sat_and_unpinned_sat(self):
        outer, adj = check_disk(icosahedron_minus_edge())
        self.assertIsNotNone(find_coloring(adj, dict(zip(outer, (0, 1, 0, 1)))))
        self.assertIsNotNone(find_coloring(adj, {}))

    def test_pinned_unsat_diamond_and_known_generated_examples(self):
        g27 = collar(DIAMOND, 27)
        for data, n, degrees in [
            (DIAMOND, 4, [2, 2, 3, 3]),
            (g27, 16, [5, 5, 5, 5]),
            (collar(g27, 28), 20, [4, 4, 4, 4]),
            (collar(g27, 29), 19, [4, 4, 4, 7]),
        ]:
            with self.subTest(n=n):
                outer, adj = check_disk(data)
                self.assertEqual(len(adj), n)
                self.assertEqual(sorted(len(adj[v]) for v in outer), degrees)
                self.assertIsNone(find_coloring(adj, dict(zip(outer, (0, 1, 0, 1)))))
                self.assertIsNotNone(find_coloring(adj, dict(zip(outer, range(4)))))

    def test_bad_29_predecessor_does_not_create_candidate(self):
        g28 = collar(collar(DIAMOND, 27), 28)
        with self.assertRaisesRegex(ValueError, "internal degree below five"):
            check_disk(collar(g28, 29))

    def test_triangle_orientation(self):
        data = copy.deepcopy(DIAMOND)
        data["triangles"][0].reverse()
        with self.assertRaisesRegex(ValueError, "orientation"):
            check_disk(data)
        data["triangles"][1].reverse()
        data["outer"].reverse()
        check_disk(data)

    def test_reversed_duplicate_edge(self):
        data = copy.deepcopy(DIAMOND)
        data["edges"].append(data["edges"][0][::-1])
        with self.assertRaisesRegex(ValueError, "duplicate undirected edge"):
            check_disk(data)

    def test_wrong_boundary(self):
        data = copy.deepcopy(DIAMOND)
        data["outer"] = [0, 2, 1, 3]
        with self.assertRaisesRegex(ValueError, "outer cycle edge absent"):
            check_disk(data)

    def test_separating_triangle(self):
        data = canvas(range(4), [(0, 1, 4), (1, 2, 4), (2, 0, 4), (0, 2, 3)])
        with self.assertRaisesRegex(ValueError, "not exactly graph triangles"):
            check_disk(data)


if __name__ == "__main__":
    unittest.main()

"""Check the sector identities and enumerate polygon examples by exact mutation.

Requires SymPy 1.14.0. Run without options to check polygons of orders 4 to 8.
"""

from functools import lru_cache
from itertools import combinations, product

import sympy as sp


ONE = (1,)


def check_sector_identities():
    a, b, c, d, x, y = sp.symbols("a b c d x y", real=True)
    A, B, z = a + b * sp.I, c + d * sp.I, x + y * sp.I

    def forms(first, second):
        return (sp.im(second * sp.conjugate(first)),
                sp.im(z * first * sp.conjugate(second)))

    F, G = forms(A, B)
    aa, bb, zz = a * a + b * b, c * c + d * d, x * x + y * y
    cases = (
        (A + B, B, F, G + y * bb),
        (A, B + z * A, F + y * aa, G),
        (A, A + B, F, G + y * aa),
        (B, B + z * A, G, zz * F + y * bb),
    )
    for first, second, expected_f, expected_g in cases:
        actual_f, actual_g = forms(first, second)
        assert sp.expand(actual_f - expected_f) == 0
        assert sp.expand(actual_g - expected_g) == 0
    assert sp.expand(forms(A, -A)[1] + y * aa) == 0
    assert sp.expand(forms(A, -z * A)[0] + y * aa) == 0


@lru_cache(maxsize=None)
def triangulations(lo, hi):
    """Return the triangle lists, splitting on the triangle at side (lo, hi)."""
    if hi - lo < 2:
        return ((),)
    return tuple(
        left + right + ((lo, mid, hi),)
        for mid in range(lo + 1, hi)
        for left, right in product(triangulations(lo, mid), triangulations(mid, hi))
    )


def edge(a, b):
    return (min(a, b), max(a, b))


def crosses(first, second):
    a, b = first
    c, d = second
    return a < c < b < d or c < a < d < b


def triangulation_data(triangles, boundary):
    opposites = {}
    for a, b, c in triangles:
        for side, opposite in (((a, b), c), ((b, c), a), ((a, c), b)):
            opposites.setdefault(side, []).append(opposite)
    diagonals = tuple(sorted(opposites.keys() - boundary))
    index = {side: i for i, side in enumerate(diagonals)}
    matrix = [[0] * len(diagonals) for _ in diagonals]
    for a, b, c in triangles:
        sides = ((a, b), (b, c), (a, c))
        for first, second in zip(sides, sides[1:] + sides[:1]):
            if first in index and second in index:
                i, j = index[first], index[second]
                matrix[i][j] += 1
                matrix[j][i] -= 1
    return diagonals, tuple(map(tuple, matrix)), opposites


def mutate(matrix, slot):
    pivot_row = matrix[slot]
    return tuple(
        tuple(
            -value if i == slot or j == slot else
            value + max(row[slot], 0) * max(pivot_row[j], 0)
            - max(-row[slot], 0) * max(-pivot_row[j], 0)
            for j, value in enumerate(row)
        )
        for i, row in enumerate(matrix)
    )


def add(first, second):
    return tuple(
        (first[i] if i < len(first) else 0) + (second[i] if i < len(second) else 0)
        for i in range(max(len(first), len(second)))
    )


def multiply(first, second):
    result = [0] * (len(first) + len(second) - 1)
    for i, a in enumerate(first):
        for j, b in enumerate(second):
            result[i + j] += a * b
    return tuple(result)


def shear_row(diagonals, quad_opposites, segment):
    """Compute shear coordinates from the signs of the two opposite side pairs."""
    a, b = segment
    blue = set(range(a + 1, b + 1))
    row = []
    for side in diagonals:
        u, v = side
        quad = sorted((u, v, *quad_opposites[side]))
        i = quad.index(u)
        corners = quad[i:] + quad[:i]
        assert corners[2] == v
        colors = [corner in blue for corner in corners]
        if colors[0] == colors[3] and colors[1] == colors[2] and colors[0] != colors[1]:
            row.append(1)
        elif colors[0] == colors[1] and colors[2] == colors[3] and colors[0] != colors[2]:
            row.append(-1)
        else:
            row.append(0)
    return tuple(row)


def exchange_polynomial(initial_matrix, slots):
    """Use the extended exchange relation, with polynomials in ascending degree."""
    matrix = initial_matrix
    values = [ONE] * len(matrix[0])
    for step, slot in enumerate(slots):
        exponent = matrix[-1][slot]
        positive = (0,) * max(exponent, 0) + ONE
        negative = (0,) * max(-exponent, 0) + ONE
        for i, value in enumerate(values):
            power = matrix[i][slot]
            for _ in range(abs(power)):
                if power > 0:
                    positive = multiply(positive, value)
                else:
                    negative = multiply(negative, value)
        # Each flipped slot still contains its original variable, specialized to 1.
        assert values[slot] == ONE
        values[slot] = add(positive, negative)
        if step + 1 < len(slots):
            matrix = mutate(matrix, slot)
    return values[slots[-1]] if slots else ONE


def flip_path(n, diagonals, opposites, target):
    start, _ = target
    position = {v: (v - start) % n for v in range(n)}
    steps = []
    for slot, side in enumerate(diagonals):
        if crosses(side, target):
            u, v = sorted(side, key=position.__getitem__)
            (w,) = (w for w in opposites[side] if position[u] < position[w] < position[v])
            steps.append((slot, u, v, w))
    steps.sort(key=lambda step: position[step[2]] - position[step[1]], reverse=True)
    assert not steps or steps[-1][3] == target[1]
    return steps


def recurrence(segment, target, path):
    start, _ = target
    a, b = segment
    start_in_block = a < start <= b
    values = {}
    latest = ONE
    for _, u, v, w in path:
        u_blue = (a < u <= b) != start_in_block
        v_blue = (a < v <= b) != start_in_block
        w_blue = (a < w <= b) != start_in_block
        first, second = values.get(u, ONE), values.get(v, ONE)
        if w_blue and u_blue != v_blue:
            if u_blue:
                second = (0,) + second
            else:
                first = (0,) + first
        latest = add(first, second)
        values[w] = latest
    return latest


@lru_cache(maxsize=None)
def check_roots(coefficients):
    assert coefficients[0] > 0 and all(value >= 0 for value in coefficients)
    if len(coefficients) > 1:
        poly = sp.Poly.from_list(list(reversed(coefficients)), sp.Symbol("q"))
        squarefree = poly.sqf_part()
        assert squarefree.count_roots(-sp.oo, 0) == squarefree.degree()


def check_polygon(n):
    boundary = {edge(v, (v + 1) % n) for v in range(n)}
    diagonals = tuple(side for side in combinations(range(n), 2) if side not in boundary)
    data = {}
    for triangles in triangulations(0, n - 1):
        sides, matrix, opposites = triangulation_data(triangles, boundary)
        data[sides] = matrix, opposites

    # The elementary lamination at diagonal (a,b) has ends on the boundary
    # sides starting at a and b. In a fan at a it has a single positive entry.
    total = 0
    for segment in diagonals:
        a, b = segment
        fan = tuple(side for side in diagonals if a in side)
        pending = [fan]
        rows = {fan: tuple(int(side == segment) for side in fan)}
        while pending:
            sides = pending.pop()
            matrix, opposites = data[sides]
            row = rows[sides]
            assert row == shear_row(sides, opposites, segment)
            extended = matrix + (row,)
            for target in diagonals:
                path = flip_path(n, sides, opposites, target)
                poly = exchange_polynomial(extended, tuple(step[0] for step in path))
                assert poly == recurrence(segment, target, path)
                check_roots(poly)
                total += 1
            for slot, side in enumerate(sides):
                after_flip = sides[:slot] + (edge(*opposites[side]),) + sides[slot + 1:]
                neighbor = tuple(sorted(after_flip))
                new_row = mutate(extended, slot)[-1]
                normalized_row = tuple(new_row[after_flip.index(diagonal)] for diagonal in neighbor)
                if neighbor in rows:
                    assert rows[neighbor] == normalized_row
                else:
                    rows[neighbor] = normalized_row
                    pending.append(neighbor)
        assert rows.keys() == data.keys()
    return total


def figure_polynomial(n, drawn_diagonals, segment, target):
    boundary = {edge(v, (v + 1) % n) for v in range(n)}
    edges = boundary | set(drawn_diagonals)
    triangles = tuple(
        triple for triple in combinations(range(n), 3)
        if all(side in edges for side in combinations(triple, 2))
    )
    assert len(triangles) == n - 2
    sides, matrix, opposites = triangulation_data(triangles, boundary)
    assert set(sides) == set(drawn_diagonals)
    path = flip_path(n, sides, opposites, target)
    extended = matrix + (shear_row(sides, opposites, segment),)
    return exchange_polynomial(extended, tuple(step[0] for step in path))


def check_published_examples():
    # Example 4 of arXiv:2508.04396v4. Mutate its displayed matrix in order.
    matrix = (
        (0, -1, 0, 0, 0),
        (1, 0, 1, 0, 0),
        (0, -1, 0, 1, 0),
        (0, 0, -1, 0, 1),
        (0, 0, 0, -1, 0),
        (-1, 1, 0, -1, 0),
    )
    stages = tuple(exchange_polynomial(matrix, tuple(range(k))) for k in range(1, 6))
    assert stages == ((1, 1), (2, 1), (3, 2), (1, 4, 2), (2, 5, 2))
    figure15 = ((0, 2), (2, 7), (3, 7), (4, 7), (5, 7))
    assert figure_polynomial(8, figure15, (0, 4), (1, 6)) == stages[-1]

    # Example 6, labeled clockwise from the left endpoint of the blue arc.
    figure17 = ((1, 11), (2, 11), (3, 10), (3, 11), (4, 8),
                (4, 9), (4, 10), (5, 8), (6, 8))
    assert figure_polynomial(12, figure17, (0, 6), (0, 7)) == (5, 22, 26, 8)


def main():
    check_sector_identities()
    print("All 10 symbolic identities hold.")
    totals = [check_polygon(n) for n in range(4, 9)]
    assert totals == [8, 125, 1134, 8232, 52800]
    for n, total in enumerate(totals, 4):
        print(f"{n} vertices: {total:,} triangulation–lamination–arc triples")
    print(f"{sum(totals):,} total. All coefficients and exact root counts agree with the claims.")
    check_published_examples()
    print("Examples 4 and 6: the values from the displayed matrix and drawings match the note.")


if __name__ == "__main__":
    main()

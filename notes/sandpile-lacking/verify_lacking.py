"""Exact checks for the proof of Alofi and Dukes's Conjecture 13.

Run: python3 verify_lacking.py
Requires Python 3 and SymPy. All computations use integers or symbolic algebra.
"""

from collections import Counter
from itertools import accumulate, combinations_with_replacement, product
from math import factorial, prod

import sympy as sp


def check(condition, message):
    if not condition:
        raise ArithmeticError(message)


def symbolic_check():
    """Check the alternative proof's operator symbol and the main proof's Hessian."""
    i, j, r, s = sp.symbols("i j r s", integer=True, nonnegative=True)
    fac = sp.factorial
    # Write the two coordinate caps as i+r and j+s, including their endpoints.
    actual = (sp.binomial(i + r, i) * sp.binomial(j + s, j)
              * fac(i) * fac(j) / fac(i + j))
    expected = fac(i + r) * fac(j + s) / (fac(i + j) * fac(r) * fac(s))
    check(sp.combsimp(actual / expected) == 1, "operator symbol")
    merge = fac(i) * fac(j) / fac(i + j)
    check(sp.cancel(merge / (fac(i) * fac(j)) - 1 / fac(i + j)) == 0,
          "action on divided powers")

    # Differentiation orders are q=D-k-1 and p=k-1. They are arbitrary.
    p, q = sp.symbols("p q", integer=True, nonnegative=True)
    x, y, left, mid, right = sp.symbols("x y left mid right")
    quadratic = 0
    for offset, coefficient in zip((-1, 0, 1), (left, mid, right)):
        u, v = 1 - offset, 1 + offset
        multiplier = (sp.FallingFactorial(q + u, q) * sp.FallingFactorial(p + v, p)
                      / (fac(q + u) * fac(p + v)))
        quadratic += coefficient * sp.combsimp(multiplier) * x**u * y**v
    hessian = sp.hessian(quadratic, (x, y))
    check(hessian == sp.Matrix([[left, mid], [mid, right]]), "symbolic Hessian")
    check(sp.expand(hessian.det() - (left * right - mid**2)) == 0,
          "symbolic determinant")
    print("Symbolic operator identity, divided powers, Hessian, determinant: PASS")


def orientation_counts(m, n):
    """Enumerate orientations, then enumerate the union of their feasible boxes."""
    # The sink is on the left. Directing all its edges outward can only
    # increase indegrees at the other endpoints. Enumerate all remaining edges.
    top = m - 1
    edges = [(a, top + b) for a in range(top) for b in range(n)]
    maxima = set()
    for directions in product((0, 1), repeat=len(edges)):
        indegree = [0] * top + [1] * n
        for endpoints, direction in zip(edges, directions):
            indegree[endpoints[direction]] += 1
        if min(indegree) > 0:
            maxima.add(tuple(d - 1 for d in indegree))

    # A tuple is a labelled lacking vector. Deduplicate across orientations.
    seen = set(maxima)
    pending = list(maxima)
    while pending:
        state = pending.pop()
        for v, amount in enumerate(state):
            if amount:
                smaller = state[:v] + (amount - 1,) + state[v + 1:]
                if smaller not in seen:
                    seen.add(smaller)
                    pending.append(smaller)
    counts = Counter(map(sum, seen))
    return tuple(counts[k] for k in range(max(counts) + 1))


def orbit_size(heights):
    return factorial(len(heights)) // prod(factorial(c) for c in Counter(heights).values())


def check_assignment_support():
    """Expand the proof's polynomial for K_(3,3) and check each labelled monomial."""
    top_size = 2
    y = sp.Symbol("y")
    vertices = sp.symbols("v:5")
    top, bottom = vertices[:top_size], vertices[top_size:]
    edge_product = prod(y + b for b in bottom)  # sink edges
    edge_product *= prod(y + a + b for a in top for b in bottom)
    differentiated = sp.Poly(edge_product, y, *vertices)
    for v in vertices:
        differentiated = differentiated.diff(v)

    # Independent forbidden-subconfiguration test: every set of left and
    # right vertices must hold at least as many grains as its internal edges.
    independent_support = set()
    for heights in product(range(3), repeat=len(vertices)):
        for mask in range(1 << len(vertices)):
            chosen = [v for v in range(len(vertices)) if (mask >> v) & 1]
            nleft = sum(v < top_size for v in chosen)
            if sum(heights[v] for v in chosen) < nleft * (len(chosen) - nleft):
                break
        else:
            lack = tuple(2 - h for h in heights)
            independent_support.add((4 - sum(lack), *lack))
    check(set(differentiated.monoms()) == independent_support, "assignment support")
    print(f"Exact polynomial support and induced-subgraph test: "
          f"{len(independent_support)} labelled K_(3,3) configurations agree")


def burning_counts(m, n):
    """Apply Selig-Zhu, Theorem 2.2, directly to sorted stable heights."""
    # Their K^0_(m-1,n) is the graph denoted K_(m,n) by Alofi and Dukes.
    top_size = m - 1
    bottom_profiles = [
        (tuple(accumulate(heights)), sum(heights), orbit_size(heights))
        for heights in combinations_with_replacement(range(m), n)
    ]
    counts = Counter()
    maximum_height_sum = top_size * (n - 1) + n * (m - 1)
    for top in combinations_with_replacement(range(n), top_size):
        thresholds = (sum(height < j for height in top) for j in range(1, n + 1))
        required = tuple(accumulate(thresholds))
        top_multiplicity = orbit_size(top)
        for prefixes, bottom_sum, multiplicity in bottom_profiles:
            if all(actual >= bound for actual, bound in zip(prefixes, required)):
                lacking = maximum_height_sum - sum(top) - bottom_sum
                counts[lacking] += top_multiplicity * multiplicity
    return tuple(counts[k] for k in range(max(counts) + 1))


def enumeration_check():
    pairs = [(m, n) for m in range(2, 7) for n in range(2, 7) if m + n <= 8]
    pairs += [(4, 5), (5, 4)]
    total_states = total_inequalities = 0
    for m, n in pairs:
        direct = orientation_counts(m, n)
        independent = burning_counts(m, n)
        check(direct == independent, f"coefficient discrepancy at {(m, n)}")
        check(len(direct) == (m - 1) * (n - 1) + 1, "degree")
        check(all(a > 0 for a in direct), "gap in support")
        for left, mid, right in zip(direct, direct[1:], direct[2:]):
            check(mid * mid >= left * right, f"log-concavity at {(m, n)}")
        total_states += sum(direct)
        total_inequalities += len(direct) - 2
        print(f"K_({m},{n})  {list(direct)}")
    print(f"{len(pairs)} ordered graph sizes, {total_states} recurrent states, "
          f"{total_inequalities} coefficient inequalities: PASS")


if __name__ == "__main__":
    symbolic_check()
    check_assignment_support()
    enumeration_check()

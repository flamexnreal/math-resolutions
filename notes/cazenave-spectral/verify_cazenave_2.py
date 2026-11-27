"""Exact full-matrix check for Cazenave's Conjecture 2 (corpus item 20829).

Run with Python 3. Only the standard library is required. The matrices are in
vertex order 0,...,10, as in the accompanying note.
"""

from fractions import Fraction


ORDER = 11
EDGES = (
    (0, 1), (0, 2), (1, 2), (1, 3), (2, 3),
    (3, 4), (4, 5), (5, 6), (6, 7),
    (7, 8), (7, 9), (8, 9), (8, 10), (9, 10),
)


def graph_matrices():
    adjacency = [[0] * ORDER for _ in range(ORDER)]
    laplacian = [[0] * ORDER for _ in range(ORDER)]
    for u, v in EDGES:
        assert 0 <= u < v < ORDER and adjacency[u][v] == 0
        adjacency[u][v] = adjacency[v][u] = 1
        # Each undirected edge contributes (e_u - e_v)(e_u - e_v)^T.
        laplacian[u][u] += 1
        laplacian[v][v] += 1
        laplacian[u][v] -= 1
        laplacian[v][u] -= 1

    reached = {0}
    pending = [0]
    while pending:
        u = pending.pop()
        for v, linked in enumerate(adjacency[u]):
            if linked and v not in reached:
                reached.add(v)
                pending.append(v)
    assert len(reached) == ORDER

    degrees = [sum(row) for row in adjacency]
    assert sum(degrees) == 2 * len(EDGES)
    for u in range(ORDER):
        for v in range(ORDER):
            assert laplacian[u][v] == (degrees[u] if u == v else -adjacency[u][v])
    return adjacency, laplacian


def shifted_pivots(matrix, shift):
    """Diagonal pivots in a rational congruence of shift*I - 8*matrix."""
    n = len(matrix)
    residual = [
        [Fraction((shift if i == j else 0) - 8 * matrix[i][j]) for j in range(n)]
        for i in range(n)
    ]
    pivots = []
    for k in range(n):
        pivot = residual[k][k]
        if pivot == 0:
            raise ArithmeticError("A zero pivot requires a different elimination order")
        pivots.append(pivot)
        for i in range(k + 1, n):
            multiplier = residual[i][k] / pivot
            for j in range(k + 1, n):
                residual[i][j] -= multiplier * residual[k][j]
    return pivots


def main():
    adjacency, laplacian = graph_matrices()
    print(f"Simple connected undirected graph: {ORDER} vertices, {len(EDGES)} edges")
    for label, matrix, shift, expected_negative in (
        ("21I - 8A", adjacency, 21, 2),
        ("37I - 8L", laplacian, 37, 0),
    ):
        pivots = shifted_pivots(matrix, shift)
        signs = "".join("+" if p > 0 else "-" for p in pivots)
        negative = sum(p < 0 for p in pivots)
        assert negative == expected_negative
        print(f"{label}: pivot signs {signs}; negative eigenvalues = {negative}")
    print("lambda_2(A) > 21/8 and mu_1(L) < 37/8")
    print("Therefore lambda_2(A) > mu_1(L) - 2.")


if __name__ == "__main__":
    main()

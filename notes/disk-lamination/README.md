# Real zeros for a single lamination in a polygon

For any triangulation of an unpunctured marked disk with a single lamination, the specialized cluster polynomial of each arc has positive constant term and all its zeros are real and negative. A sector preserved by the exchange recurrence gives real-rootedness. Newton's inequalities then give the log-concavity asked for in the revised disk conjecture.

[Proof (PDF)](proof.pdf) · [Kang, Lee and Lim, *Unimodality and Cluster Algebras from Surfaces*, v4, §5.1](https://arxiv.org/html/2508.04396v4#S5.SS1)

## Argument

Cutting the polygon along the lamination gives two colors for the boundary vertices. Follow the target arc through the triangulation. During the run of crossed diagonals with differently colored endpoints, write $A$ and $B$ for the values on the arcs from the starting vertex to the red and blue endpoints, respectively. For $q$ in the upper half-plane, the ratio $B/A$ stays in the sector between the positive real axis and $q$. Its opening angle is less than $\pi$, which rules out cancellation.

Version 4 restricts Conjecture 1 to the disk. The earlier version included annuli, where counterexamples are known. [Earlier statement](https://arxiv.org/abs/2508.04396v3) · [Annular counterexamples](https://aixiv.online/abs/2611.00002)

## Reproduce

With Python and SymPy 1.14.0 installed, run `python3 verify.py` from this directory. The script checks the sector identities, compares the recurrence with extended-matrix mutation on all 62,299 labeled cases for polygons with four through eight vertices, and reproduces the calculations for Examples 4 and 6 in the source.

[Exact checker](verify.py) · [Verification guide](../../VERIFICATION.md#coefficient-inequalities)

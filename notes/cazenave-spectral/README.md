# Two diamonds and Cazenave's spectral inequality

Join degree-two tips of two diamonds by a four-edge path. The resulting 11-vertex graph has second-largest adjacency eigenvalue at least $21/8$ and largest Laplacian eigenvalue $(7+\sqrt{5})/2$. These values reverse Cazenave's proposed inequality.

[Proof (PDF)](proof.pdf) · [Tristan Cazenave, *Lemmas and Conjectures in Spectral Graph Theory*, §7, Conjecture 2](https://arxiv.org/html/2611.03879v1#S7)

## Argument

The conjecture asserts $\lambda_2(A)\leq\mu_1(L)-2$ for every connected simple graph with at least two vertices. Two disjointly supported test vectors give the lower bound $21/8$ for $\lambda_2(A)$. An equitable partition in the proof gives $\mu_1(L)-2=(3+\sqrt{5})/2<21/8$.

## Reproduce

Run `python3 verify_cazenave_2.py` from this directory to check the shifted matrices by exact rational elimination. The script uses the Python standard library.

[Exact checker](verify_cazenave_2.py) · [Verification guide](../../VERIFICATION.md#graph-witnesses)

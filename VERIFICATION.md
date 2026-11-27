# Verification guide

Run the commands below from the repository root. The graph counterexamples have finite witnesses. For the two general theorems, the notes give proofs for arbitrary size and the computations check algebraic identities and examples.

## Recorded run

The November 27, 2026 (UTC) run used revision [`9e5df53`](https://github.com/flamexnreal/math-resolutions/tree/9e5df5327b8d62c1b4c78320f0d3c06d367d6588). The following results give a numerical or logical check against which to compare a fresh run.

| Note | Check reproduced |
| --- | --- |
| Davila | The minimum vertex cover has size 2, giving independence number 24. Counting each starting vertex, the computed index is at most $119472707/5000000 < 24$. |
| Cazenave | Rational elimination gives two negative pivots for $21I-8A$ and none for $37I-8L$, with no zero pivots. Hence $\lambda_2(A)>21/8$ and $\mu_1(L)<37/8$. |
| Sombor coindex | Both graphs pass the 2-tree test. The witness exceeds the proposed maximizer by at least $3325912/10^6$. |
| Sandpile | The symbolic Hessian identity holds. Two enumerations agree on 98,708 labeled recurrent states across 17 ordered sizes, with 77 interior coefficient inequalities checked. |
| Single lamination | All ten symbolic identities and all 62,299 labeled cases passed. The additional Lean 4.36.0 certificate described below checked noncancellation for arbitrary finite update sequences. |
| Bichromatic 4-candidate | A clean Lean 4.27.0 build reproduced the 24 axiom reports. The headline theorem uses `propext`, `Classical.choice`, and `Quot.sound`. All seven referee tests passed, and line 56 of the authors’ census decodes to the 21-vertex witness. |

## Graph witnesses

The first three scripts use only the Python standard library. Use Python 3.10 or later for all commands in this guide.

```sh
python3 notes/davila-rga/verify_davila.py &&
python3 notes/cazenave-spectral/verify_cazenave_2.py &&
python3 notes/sombor-coindex/verify_sombor.py
```

| Note | What the script establishes |
| --- | --- |
| [Double star](notes/davila-rga/) | Reconstructs the tree and checks the strict inequality under both conventions for counting vertices within distance two. |
| [Two diamonds](notes/cazenave-spectral/) | Computes the inertia of shifted adjacency and Laplacian matrices by rational elimination. The [proof](notes/cazenave-spectral/proof.pdf) also derives the largest Laplacian eigenvalue in closed form. |
| [Sombor coindex](notes/sombor-coindex/) | Reconstructs both 2-trees and certifies their coindex comparison by rational bounds on the radicals. |

### Bichromatic-forbidding 4-candidate

The [Lean project](notes/bichromatic-candidates/lean/) pins Lean 4.27.0. With Elan and Lake available, run:

```sh
(cd notes/bichromatic-candidates/lean && lake clean && lake build)
```

The headline theorem `census_counterexample_certificate` checks the 21-vertex candidate data, rules out every proper coloring with a bichromatic rim, and excludes order 21 for every permitted order trace. The [certificate note](notes/bichromatic-candidates/RESULTS_lean_certificate.md) gives the two paper arguments connecting these statements to the conjecture. One turns the determinant and area checks into a plane disk embedding. The other maps the moves in Lemmas 27–29 to the order traces.

The general Python referee accepts candidates with a chord on the outer cycle, as required for its diamond control. The 21-vertex witness satisfies the stronger induced-rim property, which Lean checks directly. The authors require inducedness for the inputs to Lemmas 28 and 29. [Definition of a candidate](https://arxiv.org/html/2504.08327v2#S2.p1) · [Move hypotheses](https://arxiv.org/html/2504.08327v2#Thmtheorem28)

To check the census witness and exercise the independent referee, run:

```sh
(
  set -e
  cd notes/bichromatic-candidates
  python3 src/verify_census21.py witnesses/conjecture30-census-21.json
  python3 -m unittest discover -s src/referee -v
  python3 src/referee/verify.py --forbidding witnesses/conjecture30-*.json
)
```

## Coefficient inequalities

Both scripts use SymPy 1.14.0. A virtual environment keeps that version local to the checks.

```sh
python3 -m venv .venv &&
.venv/bin/python -m pip install 'sympy==1.14.0' &&
.venv/bin/python notes/sandpile-lacking/verify_lacking.py &&
.venv/bin/python notes/disk-lamination/verify.py
```

| Note | Scope of the computation | Argument for arbitrary size |
| --- | --- | --- |
| [Sandpile lacking polynomial](notes/sandpile-lacking/) | Checks the symbolic coefficient identities and compares independent enumerations for 17 ordered choices of the part sizes of a complete bipartite graph. | Symmetric exchange and a Lorentzian polynomial give the coefficient inequality on every connected simple graph with at least two vertices and a sink. |
| [Single lamination](notes/disk-lamination/) | Checks ten symbolic identities, compares the recurrence with matrix mutation on 62,299 labeled cases, and recomputes the two examples discussed in the note. | A sector invariant excludes nonreal zeros through any sequence of polygon flips along the arc. |

### Lean certificate for the polygon recurrence

The [proof source](notes/disk-lamination/lean/DiskLamination/Certificate.lean) accompanies the revised polygon note. It was added after the revision used for the Python runs. With Elan and Lake available, run:

```sh
(cd notes/disk-lamination/lean && lake clean && lake build)
```

In Lean 4.36.0, `positive_real_initial_invariant` initializes the two sector inequalities for positive real-coordinate values. Given this invariant and a parameter with positive imaginary coordinate, `update_noncancellation_certificate` proves that both values stay nonzero and the inequalities persist after any finite sequence of the four update rules. The proof works in pair coordinates over an ordered commutative ring. Its axiom report lists `propext`, `Classical.choice`, and `Quot.sound`. The [written proof](notes/disk-lamination/proof.pdf) identifies the polygon flips with these updates, applies the argument to complex polynomial evaluations, and concludes with Newton’s inequalities.

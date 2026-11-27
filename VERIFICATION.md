# Verification guide

Run the commands below from the repository root. The graph counterexamples have finite witnesses. For the two general theorems, the notes give proofs for arbitrary size and the computations check algebraic identities and examples.

## Graph witnesses

The first three scripts use only the Python standard library. Use Python 3.10 or later for all commands in this guide.

```sh
python3 notes/davila-rga/verify_davila.py
python3 notes/cazenave-spectral/verify_cazenave_2.py
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

To check the census witness and exercise the independent referee, run:

```sh
(
  cd notes/bichromatic-candidates
  python3 src/verify_census21.py witnesses/conjecture30-census-21.json
  python3 -m unittest discover -s src/referee -v
  python3 src/referee/verify.py --forbidding witnesses/conjecture30-*.json
)
```

## Coefficient inequalities

Both scripts use SymPy 1.14.0. A virtual environment keeps that version local to the checks.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install 'sympy==1.14.0'
.venv/bin/python notes/sandpile-lacking/verify_lacking.py
.venv/bin/python notes/disk-lamination/verify.py
```

| Note | Scope of the computation | Argument for arbitrary size |
| --- | --- | --- |
| [Sandpile lacking polynomial](notes/sandpile-lacking/) | Checks the symbolic coefficient identities and compares independent enumerations for 17 ordered choices of the part sizes of a complete bipartite graph. | Symmetric exchange and a Lorentzian polynomial give the coefficient inequality on every connected simple graph with at least two vertices and a sink. |
| [Single lamination](notes/disk-lamination/) | Checks ten symbolic identities, compares the recurrence with matrix mutation on 62,299 labeled cases, and recomputes the two examples discussed in the note. | A sector invariant excludes nonreal zeros through any sequence of polygon flips along the arc. |

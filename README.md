# Math Resolutions

Six research notes in graph theory and algebraic combinatorics. Two prove coefficient inequalities for infinite families. Four give explicit graphs that refute proposed bounds or classifications.

[Coefficient inequalities](#coefficient-inequalities) · [Graph counterexamples](#graph-counterexamples) · [Verification guide](VERIFICATION.md)

## Coefficient inequalities

| Conjecture | Result | Proof and checks |
| --- | --- | --- |
| [Alofi and Dukes, Conjecture 13](notes/sandpile-lacking/) | The stochastic sandpile lacking polynomial is log-concave for every connected simple graph with a sink. This gives unimodality as well. | [Proof](notes/sandpile-lacking/proof.pdf) · [Symbolic checks and enumerations](notes/sandpile-lacking/verify_lacking.py) |
| [Kang, Lee and Lim, revised Conjecture 1](notes/disk-lamination/) | For any single lamination on an unpunctured marked disk, the specialized cluster polynomial of every arc has only real negative zeros. Newton’s inequalities give log-concavity. | [Proof](notes/disk-lamination/proof.pdf) · [Exact mutation checks](notes/disk-lamination/verify.py) |

## Graph counterexamples

| Conjecture | Witness | Proof and checks |
| --- | --- | --- |
| [Davila, *Graffiti³*, Conjecture 2](notes/davila-rga/) | A double star with 12 leaves at each center has independence number 24, strictly above its radius-two geometric–arithmetic index. | [Proof](notes/davila-rga/proof.pdf) · [Edge-list check](notes/davila-rga/verify_davila.py) |
| [Cazenave, Conjecture 2, corpus item 20829](notes/cazenave-spectral/) | Two diamonds joined by a four-edge path violate the proposed bound on the second adjacency eigenvalue. | [Proof](notes/cazenave-spectral/proof.pdf) · [Rational matrix check](notes/cazenave-spectral/verify_cazenave_2.py) |
| [Du, You, Liu and Huang, Conjecture 3.1](notes/sombor-coindex/) | A 21-vertex 2-tree exceeds the printed Sombor coindex bound and the coindex of the proposed maximizer. | [Proof](notes/sombor-coindex/proof.pdf) · [Radical comparison](notes/sombor-coindex/verify_sombor.py) |
| [Dvořák, Lidický and Mohar, Conjecture 30](notes/bichromatic-candidates/) | A 21-vertex bichromatic-forbidding 4-candidate in the authors’ census cannot be generated from the diamond by Lemmas 27–29. | [Proof and drawing](notes/bichromatic-candidates/#the-disk) · [Lean certificate and scope](notes/bichromatic-candidates/RESULTS_lean_certificate.md) |

## Reading and citing a note

Each linked note identifies the source and version of its conjecture. To cite a result, give its note title and a permalink to the revision you used. Cite the original authors separately for the conjecture. The [verification guide](VERIFICATION.md) gives the commands and explains which parts of each argument those commands check.

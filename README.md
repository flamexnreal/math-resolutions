# Solved conjectures in graph theory and combinatorics

Mathematical proofs and explicit counterexamples in graph theory and algebraic combinatorics. Includes exact-arithmetic verifiers and Lean 4 certificates.

Curated by [@flamexnreal](https://x.com/flamexnreal) and GPT-6.2 Astra.

[Results](#results) · [Quick run](#quick-run) · [Verification](VERIFICATION.md) · [Layout](#layout)

## Results

| # | Conjecture | Resolution | Lean | Links |
| :---: | :--- | :--- | :---: | :--- |
| **1.** | [Alofi–Dukes, Conjecture 13](notes/sandpile-lacking/) | **Proved** for every finite connected simple graph (log-concavity and unimodality of the stochastic sandpile lacking polynomial) | ⬜ | [PDF](notes/sandpile-lacking/proof.pdf) · [SymPy](notes/sandpile-lacking/verify_lacking.py) |
| **2.** | [Kang–Lee–Lim, revised Conjecture 1](notes/disk-lamination/) | **Proved** for all unpunctured polygons with a single-curve lamination (all zeros are real and negative) | 🟡 | [PDF](notes/disk-lamination/proof.pdf) · [SymPy](notes/disk-lamination/verify.py) · [Lean](notes/disk-lamination/lean/DiskLamination/Certificate.lean) |
| **3.** | [Cazenave, Conjecture 2 (#20829)](notes/cazenave-spectral/) | **Disproved** at 11 vertices: two diamonds joined by a 4-edge path give $\lambda_2(A) \ge 21/8 > (3+\sqrt{5})/2 = \mu_1(L) - 2$ | ⬜ | [PDF](notes/cazenave-spectral/proof.pdf) · [Verify](notes/cazenave-spectral/verify_cazenave_2.py) |
| **4.** | [Du–You–Liu–Huang, Conjecture 3.1](notes/sombor-coindex/) | **Disproved** at 21 vertices: explicit 2-tree beats both the printed bound and Figure 4's maximizer by $> 3.3259$ | ⬜ | [PDF](notes/sombor-coindex/proof.pdf) · [Verify](notes/sombor-coindex/verify_sombor.py) |
| **5.** | [Davila, *Graffiti³*, Conjecture 2](notes/davila-rga/) | **Disproved** at 26 vertices: double star $S_{12,12}$ has $\alpha = 24 > 1 + 12\sqrt{91}/5 = \mathrm{RGA}^{(2)}$ | ⬜ | [PDF](notes/davila-rga/proof.pdf) · [Verify](notes/davila-rga/verify_davila.py) |
| **6.** | [Dvořák–Lidický–Mohar, Conjecture 30](notes/bichromatic-candidates/) | **Disproved** (grammar erratum): 21-vertex witness from the authors' census lies outside Lemmas 27–29 | 🟡 | [Note](notes/bichromatic-candidates/) · [Lean](notes/bichromatic-candidates/RESULTS_lean_certificate.md) |

**Lean status:** ✅ Full end-to-end Lean 4 proof · 🟡 Core theorem / certificate in Lean 4 (zero `sorry`, standard axioms only) · ⬜ Exact Python / SymPy verified, Lean in progress

## Quick run

The three graph counterexample verifiers use only the Python standard library (Python 3.10+):

```sh
python3 notes/cazenave-spectral/verify_cazenave_2.py &&
python3 notes/sombor-coindex/verify_sombor.py &&
python3 notes/davila-rga/verify_davila.py
```

For the SymPy checks, DLM referee, and Lean 4 builds, see the [verification guide](VERIFICATION.md).

## Layout

- `notes/`: one self-contained folder per conjecture (PDF proof, exact verifier, and Lean package where applicable).
- `VERIFICATION.md`: full reproduction commands, pinned versions, and recorded verification output.

## Verification and scope

Every result folder links directly to the original paper and exact conjecture version it addresses. Each Lean certificate documents the exact formalized statement and any written bridge to the paper's notation.

## How to cite

To cite an individual result, reference the note title, its directory path, and the commit hash used, and cite the original conjecture authors separately. These notes are unrefereed preprints and reproducible verification artifacts.

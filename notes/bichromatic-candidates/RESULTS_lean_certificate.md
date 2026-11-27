# Lean certificate: Dvořák–Lidický–Mohar Conjecture 30

**Target.** [arXiv:2504.08327v2, §2, Conjecture 30](https://arxiv.org/html/2504.08327v2#Thmtheorem30):
“Every bichromatic-forbidding 4-candidate can be obtained from the diamond by
a sequence of the operations described in Lemmas 27, 28, and 29.”
This certificate concerns the printed whole-canvas operations, not any broader
grammar. It makes no priority claim.

**Input.** The [independent referee input](witnesses/conjecture30-census-21.json)
is from line 56 of the authors' [census](https://lidicky.name/pub/mindeg5/bernard25.log),
short graph6 `Tl?GWCJ@oB?Jp?AIK?P?@K?C?JoWEG?WySUH`.
Lean's `census_exact` checks the encoding and decodes the same 56 labeled
edges; `census_order` checks that the vertex enumeration is duplicate-free
and has length 21. The standalone verifier can also compare all labels,
edges, and oriented faces to the referee JSON.

## Reproduce

With `lake` on PATH via Elan (the project pins Lean 4.27.0), from the directory containing this report:

```sh
cd lean
lake clean
lake build
cd ..
python3 src/verify_census21.py
python3 src/verify_census21.py witnesses/conjecture30-census-21.json
```

No Mathlib, external package, `sorry`, `native_decide`, or custom axiom.
The 24 `#print axioms` commands in [the root module](lean/DiamondCertificate.lean)
run during the build and include the headline and its constituent lemmas.
The headline and `candidate_data` use exactly `propext`, `Classical.choice`,
and `Quot.sound`; the coloring theorem and both order theorems use only
`propext` and `Quot.sound`. The standalone verifier uses the Python 3.10+
standard library and embedded census and coordinate data; it does not run Lean.

## Kernel-checked statements

```lean
theorem census_counterexample_certificate :
    CandidateData ∧
    (∀ c : Vertex → Color, Proper c → ¬ (c 0 = c 2 ∧ c 1 = c 3)) ∧
    (∀ ms : List Move, ¬ OrderTrace ms vertices.length)

theorem bichromatic_forbidden (c : Vertex → Color) (proper : Proper c) :
    ¬ (c 0 = c 2 ∧ c 1 = c 3)

theorem orderInvariant {ms n} (h : OrderTrace ms n) :
    match ms with
    | [] => n = 4
    | _ :: _ => n = 16 ∨ n = 19 ∨ n = 20 ∨ 22 ≤ n

theorem order21_unreachable (ms : List Move) : ¬ OrderTrace ms 21

theorem rim_induced (u v : Vertex) (hu : u ∈ rim) (hv : v ∈ rim) :
    Adj u v ↔ edgeKey u v ∈ rimEdges
theorem interior_min_degree (v : Vertex) (hv : v ∉ rim) : 5 ≤ degree v
theorem triangles_exact (a b c : Vertex) (hab : a < b) (hbc : b < c) :
    Triangle a b c ↔ ListedFace a b c
```

`Vertex = Fin 21`, `Color = Fin 4`, and `Proper` requires unequal colors on
every edge from the encoded graph. Lean uses actual edge inequalities and
the uniqueness of the remaining color after excluding three distinct colors.
It proves the contradiction for arbitrary color names, without fixing a
particular boundary palette or relying on a colorability search. For the
standalone check only, the rim edge `01` gives distinct colors, and vertex 12
sees both; rename the three colors on `0, 1, 12` to `0, 1, 2`, respectively.
At each subsequent vertex the verifier excludes assigned neighbor colors;
singletons are forced, and vertex 19 has no choice.

`CandidateData` checks the graph is simple, the outer vertices induce
`0–1–2–3–0`, interior graph degrees are at least five, and the listed faces
are exactly all unordered graph triangles with no duplicates. The same
labels have integer coordinates: corners of a square of side 250 in order,
all other vertices strictly inside, all coordinates distinct, no third
vertex on any edge line, and strict separating-line signs for every pair of
nonincident edges. Each of the 36 listed triangles is counterclockwise, has
all three sides in the graph, and strictly excludes every other vertex.
Their doubled areas sum to twice the square's area.

## Paper bridge: finite data to a plane disk

Draw each edge as its real straight segment. For nonincident edges, both
endpoints of one segment are strictly on one side of the other's line.
The determinant is affine along the segment, so it never hits that line.
Incident edges can meet only at their common endpoint because their lines
are distinct; no other vertex is on either edge. The four square sides are
present, and convexity keeps the entire drawing in the square. Nonboundary
edges have relative interiors strictly inside, since the rim is induced.

For a positively oriented triangle, the closed triangle is the intersection
of the three inward closed half-planes. The checked negative determinant
puts every other vertex outside it. No graph edge runs through the open
triangle: it would have to cross a side or pass through a nonendpoint
corner, unless both endpoints are corners, in which case it is a side.
The open triangle is therefore a face, separated from the rest of the
complement by its three edges. Distinct listed triangles give distinct
faces and have disjoint interiors. Their closed union lies in the square
and has the same area. If it missed any interior point of the square, its
closedness would leave a positive-area open ball uncovered. Hence it covers
the square, by closedness also on the boundary. The exterior is the unique
unbounded face and the bounded faces are exactly the listed ones. This is a
plane triangulation of a disk, and the finite triangle and degree theorems
give exactly the candidate conditions in [§2](https://arxiv.org/html/2504.08327v2#S2.p1).

This argument, not Lean's topology library, turns the checked determinant
and area statements into a real plane embedding. The standalone verifier
checks all its finite premises independently of the Lean proof.

## Paper bridge: legal moves to orders

| Source operation | Exact conditions relevant to projection | Change in order |
|---|---|---:|
| [Lemma 27](https://arxiv.org/html/2504.08327v2#Thmtheorem27) | Outer face bounded by a 4-cycle; no inducedness required. Adds eight ring and four outer vertices. | +12 |
| [Lemma 28](https://arxiv.org/html/2504.08327v2#Thmtheorem28) | A 4-candidate with induced outer cycle. Adds the four new outer vertices. | +4 |
| [Lemma 29](https://arxiv.org/html/2504.08327v2#Thmtheorem29) | A 4-candidate with induced outer cycle, face `v₁v₂u₁` at `v₁v₂`, and both endpoint degrees at least five for candidate preservation. Removes only the edge `v₁v₂`, reuses `u₁`, adds `u₂,u₃,u₄`. | +3 |

The diamond starts at order four and has a chord on its outer 4-cycle, so
only Lemma 27 can be first. Map the empty sequence to `OrderTrace.diamond`;
extend the trace by the constructor for each actual operation and its
vertex increment. The other conditions can only restrict later moves, so
none are needed in this necessary projection. Lean's induction covers every
length, with no assumption that its allowed projected traces are realizable.
The standalone verifier uses the same implication with a simpler bound:
after the first move, the target gap is five; two or more later moves add
at least six and no single later move adds five. Relabeling or re-embedding
preserves the order. This paper mapping, not a Lean model of the three
operations, is the second bridge from the kernel-checked facts to the
printed conjecture.

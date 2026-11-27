# Conjecture 30 — alternating patches

**Result:** The literal statement has explicit counterexamples. The
37-vertex construction below is above the reported census. Its 25-vertex
specialization is already present in the authors' public census, which also
supplies a 21-vertex example. The [independent referee](RESULTS_independent_referee.md)
verified all three. No claim of novelty or census error.

[Dvořák–Lidický–Mohar, arXiv:2504.08327v2, Conjecture 30](https://arxiv.org/html/2504.08327v2#Thmtheorem30):
“Every bichromatic-forbidding 4-candidate can be obtained from the diamond by a
sequence of the operations described in Lemmas 27, 28, and 29.” A 4-candidate
is a simple plane graph with a distinguished quadrilateral outer face, all
other faces triangular, every triangle facial, and all internal degrees at
least five. Bichromatic-forbidding means the outer pattern 1212 cannot extend.
The pinned orbit representatives B/X/Y/R are 1212/1213/1232/1234.
Table 1 counts candidates at orders at most 28; the census was not rerun.

## Small source-based cross-check

The diamond has order 4 and its boundary has a chord, so the first move must
be 27, reaching order 16. The three moves then add 12, 4, and 3 vertices,
respectively; no nonnegative sum of these increments is 5. Yet Table 1 and
the authors' [public census log](https://lidicky.name/pub/mindeg5/bernard25.log)
report 29 bichromatic-forbidding 4-candidates of order 21. Line 56 contains
the exact graph6 string `Tl?GWCJ@oB?Jp?AIK?P?@K?C?JoWEG?WySUH`. The graph is
at least 3-connected; its unique nontriangular face has boundary
`(0,1,2,3)` up to reversal, with sorted degrees `(4,4,4,5)`. Direct pinned
counts in orbit order B/X/Y/R are `(0,51,54,105)` with this orientation.

The 25-vertex patch construction below also matches line 7859 exactly up to
isomorphism, sending its boundary onto the unique quadrilateral of the census
graph. Its graph6 string is:

```text
Xl??GCB@oB?J_?A?W?P_Ac?cG`?@QGT?GM?@@De??Yc`_[EW?[@
```

## Two-strip witness and short proof

Take one application of Lemma 27 to the diamond (order 16), or two (order
28). Call its boundary `a,b,c,d` in cyclic order. Add a middle 5-cycle
`p,q,r,s,t` and a new outer 4-cycle `u0,u1,u2,u3`, retaining the core.
Apart from the two new cycles, add precisely these cross edges:

| Middle vertex | Core neighbors | Outer neighbors |
|---|---|---|
| p | a,b,c | u0,u3 |
| q | c,d | u0,u1 |
| r | d | u1,u2 |
| s | d,a | u2 |
| t | a | u2,u3 |

Embed these as nested cycles. In the first strip, traverse the core edges
in order, taking a middle advance of 0,1,2,2 steps immediately after each
core step, starting at `(a,p)`. The second strip starts at `(p,u0)` and
takes 1,1,0,1,1 outer steps after the successive middle steps. In either
strip each step gives a triangle on the current cross edge and the traversed
ring edge. This is a triangulated annulus: the cyclic steps form a strip of
triangles with no repeated cross edge before closure. Checking the table on
consecutive vertices of either ring gives exactly the nine strip faces on
each side; there are no chords in those rings and no core-to-outer edges
that could form extra triangles. The previous core boundary degrees were all
5 and only increase; the middle degrees in order are 7,6,5,5,5.

For the obstruction, suppose `u0,u1,u2,u3` use colors 1,2,1,2. Each of
`p,q,r,t` can use only 3 or 4. The path `r-q-p-t` forces, after swapping
3 and 4 if needed, `p=r=3` and `q=t=4`. Now `s` is adjacent to
`r,t,u2`, so `s=2`. Both `a` (adjacent to `p,s,t`) and `d` (adjacent
to `q,r,s`) must be color 1, contradicting edge `ad`. This argument
does not depend on the core coloring signature.

The ordered outer degrees are 4,4,5,4. Lemma 27 yields 5,5,5,5, and Lemma
28 yields 4,4,4,4. In Lemma 29, the induced input boundary ensures that the
third vertex of the face on the removed edge is internal; it has degree at
least 5 and gains two new neighbors, so the output degrees are 4,4,4,≥7.
These multisets exclude every final move, even after rotation or reflection.

| Order | Edges | Internal faces | Pinned counts B/X/Y/R |
|---:|---:|---:|---|
| 25 | 68 | 44 | 0, 63, 162, 225 |
| 37 | 104 | 68 | 0, 1134, 2916, 4050 |

## Diagnostic scope and verification

- Controls: the diamond and examples of each legal expansion forbidden in B;
  an edge-deleted icosahedron extended all four boundary types. The six
  above-cutoff seeds were pairwise nonisomorphic with boundary marked.
- Paired local flips: 207 valid labeled outcomes across the seeds, 205 with
  noncanonical boundary degrees. All extended B; no rank by exact share was
  available at the per-pattern cap of 129. Zero remained exact.
- Two-strip route: stopped on the 53rd attachment specification (21st
  valid disk) of the first fixed-core pilot. The witness, the unpatched
  Lemma 27 sleeve, and the nearby upper attachment `(0,1,1,1,1)` all had
  dual terminal matching deficiency zero. Their exact outer-B to inner
  type masks were respectively empty, B-only, and Y-only; only the nearby
  variation lets B extend through the fixed core. Thus matching does not
  detect the obstruction even where the exact transfer mask does.
- The validator checks edge incidences and opposite darts, vertex links,
  connectedness, sphere Euler characteristic after adding the outer face,
  triangle completeness and minimum internal degrees. Direct pinned
  coloring searches corroborated the zero obtained from the strip proof.

The original [diagnostic search](https://github.com/flamexnreal/open_math_lab/tree/70d458ce80acf790788be87481303475799b8d9d/problems/diamond-generation/src)
ran under Python 3.10.12 with NetworkX 3.4.2. It stays on its work branch;
the integrated [exact checks](README.md#reproduce) need only Python's
standard library.

[25-vertex disk](witnesses/conjecture30-candidate-25.json) ·
[37-vertex disk](witnesses/conjecture30-candidate-37.json)

# Independent referee: Dvořák–Lidický–Mohar Conjecture 30

**Verdict, conditional on the printed whole-canvas operations:** the 21-, 25-,
and 37-vertex graphs are each counterexamples to Conjecture 30. The strongest
handoff is the 21-vertex graph: it is in the authors' own census, has a short
edge-only coloring contradiction, and its order alone rules out generation.
These are not counterexamples to Conjecture 2; all three admit a rainbow
boundary coloring.

**Source.** [Conjecture 30, v2](https://arxiv.org/html/2504.08327v2#Thmtheorem30):
“Every bichromatic-forbidding 4-candidate can be obtained from the diamond by a
sequence of the operations described in Lemmas 27, 28, and 29.” [v1](https://arxiv.org/html/2504.08327v1#Thmtheorem30)
has the same statement; the [arXiv record](https://arxiv.org/abs/2504.08327)
listed v2 as latest. The target is not a broader grammar allowing arbitrary
substitutions or identifications, which the cited operations do not prescribe.
The audit used the paper, three raw JSONs, and the public census data only;
no discovery code, notes, or branch were consulted.

## Disk and forcing checks

[Section 2](https://arxiv.org/html/2504.08327v2#S2.p1) requires a plane disk
with outer 4-cycle, triangular inner faces, every triangle facial, and every
interior vertex of degree at least five. For each raw input, the verifier checks
the exact simple connected labeled graph, equality of listed faces with all
3-cliques, opposite oriented incidences along interior edges, one directed
incidence along each outer edge, and the link of every vertex. The links are
single cycles in the interior and single paths at the boundary with the
prescribed endpoints. Thus the face complex is a connected orientable compact
surface with one boundary component; Euler characteristic one makes it a disk.

| Order | Edges | Inner faces | Outer cycle | Outer degrees | Min. inner degree |
|---:|---:|---:|---|---|---:|
| 21 | 56 | 36 | 0, 1, 2, 3 | 4, 4, 5, 4 | 5 |
| 25 | 68 | 44 | 21, 22, 23, 24 | 4, 4, 5, 4 | 5 |
| 37 | 104 | 68 | 33, 34, 35, 36 | 4, 4, 5, 4 | 5 |

All three outer cycles are induced, so the alternating pins are individually
proper on the boundary. Under the [§1 color-type definition](https://arxiv.org/html/2504.08327v2#S1.p4),
all bichromatic colorings can be renamed to pin the listed boundary to
`0,1,0,1`. Exact backtracking exhausts all choices under these pins and finds
none, then finds and checks a proper rainbow extension for each graph.

**Edge-only cross-check.** In each row, the first vertex has neighbors of colors
0 and 1, so set it to 2 by swapping unused colors 2 and 3. Read every subsequent
assignment left to right; each vertex has the three already colored neighbors
in parentheses. The last vertex sees all four colors.

| Order | Start | Forced assignments (neighbors) | Blocked vertex (neighbors) |
|---:|---|---|---|
| 21 | 12=2 (0,1) | 14=3 (1,2,12); 20=3 (0,3,12); 16=2 (2,3,20); 15=1 (2,14,16); 17=0 (12,14,15) | 19 (15,16,17,20) |
| 25 | 16=2 (21,24) | 17=3 (16,21,22); 18=2 (17,22,23); 20=3 (16,23,24); 19=1 (18,20,23); 12=0 (16,19,20) | 15 (12,17,18,19) |
| 37 | 28=2 (33,36) | 29=3 (28,33,34); 30=2 (29,34,35); 32=3 (28,35,36); 31=1 (30,32,35); 24=0 (28,31,32) | 27 (24,29,30,31) |

## Complete generation obstruction

The operation descriptions have also been checked against [Figure 4 in the PDF](https://arxiv.org/pdf/2504.08327v2#page=26).

In any 4-canvas embedding of one of these abstract graphs, Euler gives
`E−V+1` triangular faces, exactly the graph's number of triangles. A simple
triangle cannot bound two faces in a connected sphere embedding with more
than three vertices (both complementary disks would be empty of the graph).
Therefore every graph triangle must occur once as a face, even without
assuming the embedding is a candidate. The edges incident with just one
triangle in the graph are exactly the edges of the unique quadrilateral face.
So changing embedding, orientation, outer face, or labels cannot change the
degree multiset on the 4-face of a 4-canvas. The same argument works for any
intermediate 4-candidate, including the diamond.

| Last operation | New vertices | Output outer-degree multiset |
|---|---:|---|
| [Lemma 27](https://arxiv.org/html/2504.08327v2#Thmtheorem27) | 12 | 5, 5, 5, 5: each new outer vertex has two cycle and three inner neighbors. |
| [Lemma 28](https://arxiv.org/html/2504.08327v2#Thmtheorem28) | 4 | 4, 4, 4, 4: each new outer vertex has two cycle and two inner neighbors. |
| [Lemma 29](https://arxiv.org/html/2504.08327v2#Thmtheorem29) | 3 | 4, 4, 4, at least 7: reused `u₁` was interior since its incident triangle on `v₁v₂` and induced `Q` exclude `u₁=v₃,v₄`. Its old degree is at least 5 and it gains two new cycle neighbors. |

No nonempty sequence can end at any of the three graphs, whose invariant
multiset is `4,4,4,5`. This is a necessary property of every possible last
operation, not a failed predecessor search. In Lemma 29, `v₁,v₂` become
interior with their degrees unchanged (each loses their shared edge and gains
one new neighbor). Thus its two endpoint degree conditions are necessary to
remain a candidate; omitting those endpoint conditions would still not weaken
the bound on `u₁` when the predecessor is a candidate. Both Lemmas 28 and 29
require induced `Q`, so the chorded diamond must start with Lemma 27, reaching
16 vertices. From there the only increments are 3, 4 and 12, which cannot add
up to 5. This gives the 21-vertex obstruction without any inverse or even
the extra degree restrictions on the later moves. Independently, in a
candidate sequence each 29 must immediately follow a 27 (only a 27 result
has two outer vertices of degree at least five). For orders 25 and 37,
reduction of the order formula modulo 4 requires at least three uses of 29,
hence at least three uses of 27, already too large.

## Census and reproducibility

[Table 1](https://arxiv.org/html/2504.08327v2#S2.T1) and its [enumeration discussion](https://arxiv.org/html/2504.08327v2#S2.p31)
report 29 bichromatic-forbidding candidates at order 21 and 6,915 at order
25. The 21-vertex graph was reconstructed from the single short-graph6
record on line 56 of the authors' [bernard25.log](https://lidicky.name/pub/mindeg5/bernard25.log).
The exact record is `Tl?GWCJ@oB?Jp?AIK?P?@K?C?JoWEG?WySUH`. Decoding its bits,
enumerating its triangles, and orienting them across shared edges recovered
the same labeled graph and quadrilateral as the supplied 21-vertex JSON.
The apparent conflict is between the census and the printed generation
claim, not between the census and the witnesses being bichromatic-forbidding.

```sh
cd notes/bichromatic-candidates
curl -fsSL https://lidicky.name/pub/mindeg5/bernard25.log -o /tmp/bernard25.log
python3 -m unittest discover -s src/referee -v
python3 src/referee/verify.py --forbidding --census /tmp/bernard25.log witnesses/conjecture30-*.json
```

Python 3.10, standard library only. Controls cover an extendible 4-candidate
(icosahedron minus an edge), the diamond and independently constructed legal
outputs of each operation, an inadmissible Lemma 29 result, a separating
triangle, a wrong outer cycle, a reversed duplicate edge, and a single flipped
face versus consistent global reversal. This is an independent finite exact
check, not a Lean proof or a priority claim.

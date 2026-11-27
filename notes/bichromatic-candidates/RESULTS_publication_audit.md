# Publication and census audit: Dvořák–Lidický–Mohar Conjecture 30

**Checked 2026-11-26 (US Eastern), for Math.** Conjecture 30, as printed in the full preprint, is false: the authors' own public census contains a verified 21-vertex counterexample. No prior source explicitly identifying a counterexample to this exact statement, author withdrawal, or correction was found. The exact conjecture was located only in public preprint versions, not in the accepted EUROCOMB extended abstract or in a verified journal version. No claim about priority or Conjecture 2.

## Which version says what?

| Source | Finding |
|---|---|
| [arXiv record](https://arxiv.org/abs/2504.08327), [v1](https://arxiv.org/html/2504.08327v1#Thmtheorem30), [v2](https://arxiv.org/html/2504.08327v2#Thmtheorem30) | v1 2025-04-11; v2 2025-04-14, latest. The record calls the change an abstract metadata typo fix. Both source bundles extract to byte-identical trees; PDF text differs only in arXiv stamp. No change to numbering, operations, candidate/type conventions, census, or conjecture. |
| [Lidický's author PDF](https://lidicky.name/pub/mindeg5.pdf), also [on the supplement page](https://lidicky.name/pub/mindeg5/) | The two hosted PDFs are byte-identical to each other. The candidate section of the author PDF matches arXiv after whitespace normalization, apart from three sum-sign extraction glyphs. Lidický's [publication list](https://lidicky.name/pub.html) and [CV](https://lidicky.name/bernardcv.pdf) list the full paper under submissions; Dvořák's [personal list](https://iuuk.mff.cuni.cz/~rakdver/index.php?which=res) does not supply a newer copy or status. |
| [EUROCOMB’25 proceedings, pp. 411–416](https://nextcloud.renyi.hu/index.php/s/TdjSmNjDjrQEH2X/download#page=419) | Separate accepted, published extended abstract (Rényi Institute, 2025; [CFP](https://easychair.org/cfp/eurocomb25), [catalog](https://m2.mtmt.hu/api/publication/36432641?labelLang=eng)). Sections 2–3 give the same canvas/candidate and bichromatic conventions, and the same 28-vertex no-rainbow/diamond-only-diagonal finding for **Conjecture 2**. They omit Conjecture 30, its three moves and Table 1. Figure 2 shows the general census reductions, not the three moves. Figure 1 shows yet another set of expansions, for non-4-colorable graphs conditional on Conjecture 2. |
| [Mohar bibliography, November 2026](https://www.sfu.ca/~mohar/BibliographyMohar2026.pdf#page=2) | Separately records the full paper as “submitted to J. Graph Theory, June 2026” (p. 2, item 9), and the EUROCOMB abstract (p. 20, conference item 4). The public proceedings text omits the target; conference acceptance does not substantiate peer review of the target. |
| [arXiv DOI](https://doi.org/10.48550/arXiv.2504.08327), [DataCite](https://api.datacite.org/dois/10.48550/arxiv.2504.08327), [zbMATH](https://zbmath.org/902710802), [Crossref/JGT](https://api.crossref.org/journals/1097-0118/works?query.title=On+a+conjecture+concerning+4-coloring+of+graphs+with+one+crossing) | DataCite labels DOI a preprint (v2, no related IDs); zbMATH gives only that preprint; arXiv has no journal reference. Exact-title/author Crossref and JGT searches produced no matching publisher record or DOI; direct Wiley search was blocked. No independent chapter DOI found for the proceedings item. Public full text is a preprint; acceptance or unpublished revisions cannot be ruled out. |

One terminology difference: the proceedings names the diagonal type for the opposite pair that **differs**, whereas arXiv names it for the pair that **agrees**. This swaps the two diagonal labels, not the aggregate diagonal, rainbow, or bichromatic conditions. The proceedings' “infinitely many counterexamples” refers to the **bichromatic analogue** of the rainbow absence claim, not the omitted three-move classification.

## Exact claim and what the enumeration tested

> Every bichromatic-forbidding 4-candidate can be obtained from the diamond by a sequence of the operations described in Lemmas 27, 28, and 29.

[Section 2](https://arxiv.org/html/2504.08327v2#S2) works with simple plane graphs whose designated outer face is bounded by a 4-cycle, other faces are triangles, every triangle bounds a face, and all internal vertices have degree at least five. The 4-cycle need not be induced (the diamond is a 4-cycle with one chord). [Bichromatic-forbidding](https://arxiv.org/html/2504.08327v2#S1.p4) means no proper 4-coloring with both opposite pairs equal; it imposes no minimality, internal 5-connectivity, or rainbow obstruction requirement.

| Whole-canvas move | Preconditions and vertex change | New outer degrees |
|---|---|---|
| [Lemma 27](https://arxiv.org/html/2504.08327v2#Thmtheorem27) | Any outer 4-cycle; add the inner ring of eight new vertices and outer ring of four. **+12**. | 5,5,5,5 |
| [Lemma 28](https://arxiv.org/html/2504.08327v2#Thmtheorem28) | Induced outer 4-cycle; add four new outer vertices, joined to the old cycle as in the lemma. **+4**. | 4,4,4,4 |
| [Lemma 29](https://arxiv.org/html/2504.08327v2#Thmtheorem29) | Induced outer 4-cycle, with both ends of the chosen edge of degree ≥5 to preserve candidacy. Delete that edge, reuse the interior third vertex of its incident triangle, add three new outer vertices. **+3**. | 4,4,4,≥7: the reused interior vertex gains two edges. |

The seed is chorded, so only Lemma 27 can start: order 4 becomes 16. A further increment of 5 is not a nonnegative sum of 12, 4 and 3, irrespective of relabeling or embedding. At order 25, the verified outer-degree multiset 4,4,4,5 also excludes **every** possible last move. In these graphs the triangular-face count equals the number of graph triangles; a triangle in a connected graph of order greater than 3 cannot bound both faces. Thus in any 4-canvas embedding the edges in exactly one triangle recover the same unique outer 4-cycle. Allowing a reflection or a different abstract labeling does not fix the last-move mismatch.

- [Corollary 25](https://arxiv.org/html/2504.08327v2#Thmtheorem25) proves a generation theorem for **all** candidates by inverses to the general star-contractions, not by Lemmas 27–29. The [supplement](https://lidicky.name/pub/mindeg5/) bundles both programs in [anc.tar.gz](https://lidicky.name/pub/mindeg5/anc.tar.gz). The C++ generation rules use 1-, 2-, 5-, extended-5-, 8- and 10-decontractions. The C++ pipeline filters reflection duplicates, tests boundary extension signatures, and prints restrictive graphs. The Sage code tests the four explicit pins, tallies nonextensions and compares restrictive graph6 lists by abstract graph isomorphism. It is a color-type census, not a reachability test for the three-move grammar.
- [Table 1](https://arxiv.org/html/2504.08327v2#S2.T1) and its accompanying text report all plane 4-candidates through 28 vertices (more than a billion total) and counts of bichromatic-forbidding ones, cross-checked with Sage through 25. At orders 21, 25, 28 the bichromatic counts are 29, 6,915, 346,005. The no-rainbow result verifies **Conjecture 2** through 28 via [Theorem 10](https://arxiv.org/html/2504.08327v2#Thmtheorem10); only the diamond forbids a diagonal type. The authors say their enumeration “supports” Conjecture 30; neither the prose nor the inspected code claims the three-move reachability test was run.
- **Actual mismatch:** a qualifying graph in the listed census fails the literal classification. The census counts/signatures checked here are consistent with the witnesses, not erroneous because of their orders.

## Bounded audit of the authors’ lists

Only [bernard25.log](https://lidicky.name/pub/mindeg5/bernard25.log) and the bundled `anc/md5g-bernard/zdenek25.g6` were used as graph data (9,422 restrictive rows in each). No all-candidate pickles, 28-vertex output, or graph regeneration. Recovered the outer cycle independently by face traversal; compared all triangles with the facial triangles; checked minimum internal degree and exact 4-colorability with each boundary type. In both lists all 29 order-21 rows have outer degrees 4,4,4,5 and signature NYYY (B, both diagonals, rainbow). In the Sage log at order 25, 6,886 of 6,915 rows have that outer profile and were likewise checked to be candidates with signature NYYY.

| Instance (1-based physical line) | Exact result |
|---|---|
| Sage log line 56 | 21 vertices, 56 edges, outer cycle 0–3–2–1 in the recovered rotation, 36 triangular faces, minimum internal degree 5, NYYY. |
| Sage log line 7859 | 25 vertices, 68 edges, outer cycle 0–3–2–1, 44 triangular faces, minimum internal degree 5, NYYY. It is isomorphic preserving the boundary set to Dvořák list line 8287 and to the reported internal 25-vertex lead; the internal referee's 21-vertex instance likewise matches line 56. |

Minimal local check for the two Sage rows (Python + NetworkX 3.4.2); this checks witnesses, not the census completeness:

```sh
curl -fsSLO https://lidicky.name/pub/mindeg5/bernard25.log
python - <<'PY'
from itertools import combinations
from pathlib import Path
import networkx as nx

rows = Path('bernard25.log').read_bytes().splitlines()
for line, n in [(56, 21), (7859, 25)]:
    g = nx.from_graph6_bytes(rows[line - 1])
    planar, rotation = nx.check_planarity(g)
    assert planar and len(g) == n and nx.is_connected(g)
    seen = set()
    faces = [rotation.traverse_face(u, v, seen)
             for u, v in rotation.edges() if (u, v) not in seen]
    outer, = [f for f in faces if len(f) != 3]
    assert len(outer) == len(set(outer)) == 4 and len(faces) == 2*n - 5
    triangles = {frozenset((u,v,w)) for u in g
                 for v,w in combinations(g[u],2) if g.has_edge(v,w)}
    assert {frozenset(f) for f in faces if len(f) == 3} == triangles
    assert len(triangles) == 2*n - 6
    assert min(g.degree(v) for v in g if v not in outer) >= 5
    assert sorted(g.degree(v) for v in outer) == [4,4,4,5]
    assert all(not g.has_edge(outer[i],outer[i+2]) for i in (0,1))

    def extend(colors):
        remaining = [(len(opts), -g.degree(v), v, opts) for v in g
                     if v not in colors
                     for opts in [{0,1,2,3} - {colors[w] for w in g[v] if w in colors}]]
        if not remaining:
            return True
        _, _, v, opts = min(remaining)
        return any(extend(colors | {v: c}) for c in sorted(opts))

    sig = [extend(dict(zip(outer,p))) for p in ((0,1,0,1),(0,1,0,2),(0,1,2,1),(0,1,2,3))]
    assert sig == [False,True,True,True]
    print(line, n, g.number_of_edges(), outer, sig)
PY
```

## Citations and priority coverage

[Semantic Scholar](https://api.semanticscholar.org/graph/v1/paper/ARXIV:2504.08327?fields=title,citationCount,citations) returned one citing document. [Read the note](https://www.cs.umd.edu/~gasarch/open/cross2.pdf), *Four-Coloring Beyond the Plane* (2026, byline Claude Fable 5), §3, §5 and ref. [7]: it discusses the main crossing/colorability conjectures, the conditional K5 grammar and the **Birkhoff diamond** experiment, not Conjecture 30 or its 4-vertex seed. [OpenAlex](https://openalex.org/W4415152100) returned zero and marked both arXiv and the [Iowa State repository location](https://dr.lib.iastate.edu/handle/20.500.12876/qzXBde8v) as submitted versions; the Iowa State record itself blocked direct access. Google Scholar rate-limited and DBLP did not return a usable result. This is incomplete forward-citation coverage, not evidence of zero follow-ups.

The [Graph-theory open-problem index](https://graph-theory-ai.github.io/graph-conjectures/arxiv/AX_one_crossing_bichromatic_forbidding_diamond_generation/) lists the exact claim as open (automated review dated May 2026; not authoritative). Targeted title/ID, quoted claim, variant “diamond generation”/“bichromatic forbidding,” errata and alternate-language queries (notably Czech and Slovene), plus indexed searches of Open Problem Garden, Formal Conjectures and MathOverflow, surfaced neither a corrigendum nor a prior **explicit** refutation. The counterexample *graphs* were already publicly available in the authors' data; that is distinct from finding prior notice that they refute Conjecture 30. No authors contacted, public posts made, or priority asserted.

# A counterexample to the Sombor coindex bound for 2-trees

At order 21, an explicit 2-tree exceeds both the conjectured upper bound as printed and the coindex of the proposed maximizer in Figure 4. The proof counts nonedges by their endpoint degrees and compares the resulting radicals exactly.

[Proof (PDF)](proof.pdf) · [Du, You, Liu and Huang, *The Sombor index and coindex of two-trees*, Conjecture 3.1](https://doi.org/10.3934/math.2023967)

## Argument

The witness starts from the square of a 12-vertex path. Adding nine vertices of degree two leaves all twelve original vertices with degree five. Grouping nonedges by endpoint degrees gives coindex $297\sqrt{2}+90\sqrt{29}$. The proof compares this value with both versions of the proposed extremum.

## Reproduce

Run `python3 verify_sombor.py` from this directory to reconstruct both graphs and certify the comparison. The script uses the Python 3.8+ standard library.

[Graph construction and exact comparison](verify_sombor.py) · [Verification guide](../../VERIFICATION.md#graph-witnesses)

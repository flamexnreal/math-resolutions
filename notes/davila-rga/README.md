# A double-star counterexample to the TxGraffiti independence bound

A tree formed by joining the centers of two stars, each with 12 leaves, has independence number 24 and radius-two geometric–arithmetic index strictly less than 24. The same tree also works when the distance count excludes the starting vertex.

[Proof (PDF)](proof.pdf) · [LaTeX source](proof.tex) · [Randy Davila, *Graffiti³*, §3.1, Conjecture 2](https://doi.org/10.21203/rs.3.rs-8493329/v1)

## Argument

The proposed bound is $\alpha(G)\leq \mathrm{RGA}^{(2)}(G)$ for every nontrivial connected graph. For the double star, the center edge contributes 1 and each of the 24 leaf edges contributes $\sqrt{91}/10$. The strict comparison reduces to $12^2\cdot91<115^2$.

## Reproduce

Run `python3 verify_davila.py` from this directory for an exact check from the edge list. The script uses the Python 3.8+ standard library. Build the PDF with `tectonic proof.tex`.

[Exact checker](verify_davila.py) · [Verification guide](../../VERIFICATION.md#graph-witnesses)

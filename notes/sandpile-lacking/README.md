# Log-concavity of the stochastic sandpile lacking polynomial

For a finite connected simple graph with a designated sink, the coefficients of the lacking polynomial are positive through degree $|E|-|V|+1$ and log-concave. The proof uses symmetric exchange of edge labels and dually Lorentzian polynomials. Applied to complete bipartite graphs, it gives both assertions of Alofi and Dukes's Conjecture 13.

[Proof (PDF)](proof.pdf) · [Alofi and Dukes, *A note on the lacking polynomial of the complete bipartite graph*, Conjecture 13](https://arxiv.org/html/2411.02667v1#Thmtheorem13)

## Argument

Choose a spanning tree rooted at the sink. Label each tree edge by its child. Of the remaining $|E|-|V|+1$ edges, any $k$ can be labeled by a nonsink endpoint and the rest left spare. This realizes every total lack $k$ in the stated range. To prove log-concavity, count distinct label-count vectors and exchange labels along paths between two assignments. The resulting symmetric exchange property is the input to the Lorentzian argument.

## Reproduce

With Python and SymPy 1.14.0 installed, run `python3 verify_lacking.py` from this directory for the symbolic checks and the independent coefficient enumerations.

[Symbolic and enumeration checks](verify_lacking.py) · [Verification guide](../../VERIFICATION.md#coefficient-inequalities)

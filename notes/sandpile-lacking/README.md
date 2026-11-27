# Log-concavity of the stochastic sandpile lacking polynomial

For a finite connected simple graph with a designated sink, the coefficients of the lacking polynomial are positive through degree $|E|-|V|+1$ and log-concave. The proof uses symmetric exchange of edge labels and dually Lorentzian polynomials. Applied to complete bipartite graphs, it gives both assertions of Alofi and Dukes's Conjecture 13.

[Proof (PDF)](proof.pdf) · [Alofi and Dukes, *A note on the lacking polynomial of the complete bipartite graph*, Conjecture 13](https://arxiv.org/html/2411.02667v1#Thmtheorem13)

With Python and SymPy 1.14.0 installed, run `python3 verify_lacking.py` from this directory for the symbolic checks and the independent coefficient enumerations.

# Real zeros for a single lamination in a polygon

For any triangulation of an unpunctured marked disk with a single lamination, the specialized cluster polynomial of each arc has positive constant term and all its zeros are real and negative. A sector preserved by the exchange recurrence gives real-rootedness. Newton's inequalities then give the log-concavity asked for in the revised disk conjecture.

[Proof (PDF)](proof.pdf) · [Kang, Lee and Lim, *Unimodality and Cluster Algebras from Surfaces*, v4, §5.1](https://arxiv.org/html/2508.04396v4#S5.SS1)

With Python and SymPy 1.14.0 installed, run `python3 verify.py` from this directory. The script checks the sector identities, compares the recurrence with extended-matrix mutation on all 62,299 labeled cases for polygons with four through eight vertices, and reproduces the calculations for Examples 4 and 6 in the source.

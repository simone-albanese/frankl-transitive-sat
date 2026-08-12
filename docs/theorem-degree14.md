# Note — Frankl's conjecture for all transitive groups of degree 14

Conventions: points = {0,…,13}; F ⊆ P([14]) union-closed and non-trivial
(F ≠ ∅, F ≠ {∅}); G ≤ S14 transitive; "Frankl margin" = 2·maxfreq − |F|
(integer arithmetic throughout); "14-cycle" = element of cycle type (14)
(NOT the same as "element of order 14", which may have type (2,7,1^5)).

## Theorem

Every non-trivial union-closed family F ⊆ P([14]) invariant under some
transitive permutation group G ≤ S14 satisfies Frankl's conjecture:
some point lies in at least half the sets of F (2·maxfreq ≥ |F|).

This extends beyond prime degrees the corollary that for 13 points followed
from Cauchy's theorem (cyclic cases Z13, Z14 were closed with DRAT
certificates in the companion repository `frankl-cyclic-sat`,
DOI 10.5281/zenodo.21900943).

## Proof structure

**Step 1 (descent of invariance).** If F is G-invariant and H ≤ G, then F
is H-invariant (Lemma 1 in `notes-minimality.md`). Hence non-existence of a
violating H-invariant family implies the same for every overgroup G ≥ H.

**Step 2 (reduction to minimal transitive groups).** Every transitive
G ≤ S14 contains a minimal transitive subgroup M (finite descending chain).
Two cases:

- *G contains a 14-cycle.* Then G ⊇ ⟨that cycle⟩ ≅ Z14, and the Z14 case is
  closed by the DRAT-certified UNSAT of the cyclic repository (sizes ≥ 3;
  sizes ≤ 2 are trivially conforming, Sarvate–Renaud reduction).
- *G has no 14-cycle.* Then M has no 14-cycle either (a 14-cycle in a
  subgroup is a 14-cycle in G — Lemma 2). By the certified minimality scan
  (`results/minimality_scan.json`, criterion of `notes-minimality.md`),
  up to conjugacy in S14 every such M is one of: **14T2, 14T6, 14T10,
  14T30** (minimality certified), with **14T12** added conservatively
  (its 7-elements are not fixed-point-free, so the 2-generation criterion
  does not apply; deciding it directly by SAT was cheaper than classifying
  it, and an UNSAT for it covers its overgroups anyway). Conjugacy in S14
  is a relabeling of points and does not affect the verdict.

**Step 3 (the five instances are UNSAT).** For each of the five groups, the
constraint system "F union-closed, G-invariant, |F| ≥ 3, margin ≤ −1" is
unsatisfiable. Each verdict was obtained by **two independent methods**:

| Group | Name            | Order | Nontrivial orbits | Clauses   | CP-SAT      | cadical | drat-trim  |
|-------|-----------------|-------|-------------------|-----------|-------------|---------|------------|
| 14T2  | D_14(14)=[7]2   | 14    | 1234              | 7,098,740 | INFEASIBLE  | UNSAT   | s VERIFIED |
| 14T6  | [2^3]7          | 56    | 422               | 1,137,222 | INFEASIBLE  | UNSAT   | s VERIFIED |
| 14T10 | L_7(14)         | 168   | 154               | 159,203   | INFEASIBLE  | UNSAT   | s VERIFIED |
| 14T12 | 1/2[D(7)^2]2    | 196   | 170               | 146,706   | INFEASIBLE  | UNSAT   | s VERIFIED |
| 14T30 | L(14)=PSL(2,13) | 1092  | 50                | 10,134    | INFEASIBLE  | UNSAT   | s VERIFIED |

CNF files and DRAT certificates: `results/cnf/` (14T2.drat is 3.3 GB).
Full reverification commands: `results/FOUND.md`.

**Conclusion.** Let F be non-trivial, union-closed, G-invariant, G
transitive of degree 14, and suppose F violates Frankl (margin ≤ −1); note
|F| ≥ 3 since families of size ≤ 2 conform trivially. By Step 2, G contains
either Z14 or a conjugate of one of the five listed groups; by Step 1, F is
invariant under that subgroup; by Step 3 (and the cyclic repository for
Z14) no such F exists. Contradiction. ∎

## Validation of the pipeline

Before production runs, the group encoder was validated on controls with
known outcomes: Z7 and Z11 INFEASIBLE, and the generated DIMACS files are
byte-identical to those of the (published) cyclic encoder
(`results/logs/t5_probe.log`, `results/logs/t7_validate.log`).
The census of the 63 transitive groups of degree 14 (26 without a
14-cycle) was cross-checked against LMFDB (`STATE/census14.json`), with the
14-cycle filter applied on cycle types, never on element orders.

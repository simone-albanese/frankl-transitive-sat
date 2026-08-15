# Note — Frankl's conjecture for all transitive groups of degree 15

Conventions: points = {0,…,14}; F ⊆ P([15]) union-closed and non-trivial
(F ≠ ∅, F ≠ {∅}); G ≤ S15 transitive; "Frankl margin" = 2·maxfreq − |F|
(integer arithmetic throughout); "15-cycle" = element of cycle type (15)
(NOT the same as "element of order 15", which may have type (3,5,1^7)).
Degree-15 warning: a 15-cycle is an **even** permutation, so the parity
shortcut used in the degree-14 census ("all generators even ⇒ no long
cycle") does not exist here and is not used. Instructive example:
15T72 = PSL(4,2) ≅ A8 acting on the 15 points of PG(3,2) **does** contain
15-cycles (Singer cycles of GL(4,2)) although A8 has no order-15 element
in its natural action on 8 letters.

## Theorem

Every non-trivial union-closed family F ⊆ P([15]) invariant under some
transitive permutation group G ≤ S15 satisfies Frankl's conjecture:
some point lies in at least half the sets of F (2·maxfreq ≥ |F|).

Together with the degree-13 corollary (Cauchy) and the degree-14 theorem
(`theorem-degree14.md`), this settles every transitive degree up to 15.

## Proof structure

**Step 0 (size reduction).** WLOG every non-trivial set of F has size ≥ 3:
a union-closed family containing a singleton conforms (that point is in at
least half the sets), and one containing a 2-set conforms by the
Sarvate–Renaud lemma. The trivial family {∅, [15]} conforms. All instances
below therefore carry `min_size = 3` and exclude the trivial family.

**Step 1 (descent of invariance).** If F is G-invariant and H ≤ G, then F
is H-invariant. Hence non-existence of a violating H-invariant family
implies the same for every overgroup G ≥ H.

**Step 2 (census and reduction).** The 104 transitive groups of degree 15
(`STATE/census15.json`, built from the GAP transitive-groups library
`trans15.grp` by A. Hulpke, sha256 `89cd49a6…`; for every enumerable group
the BFS order of the published generators was checked against the order
stated in the library's independent TRANSPROPERTIES section) split as:

- **78 groups contain a 15-cycle** (witness permutation verified, or
  exhaustive enumeration). Each contains ⟨cycle⟩ ≅ Z15 acting regularly,
  conjugate to the standard Z15 — and the Z15 case is closed, with a
  147 GB LRAT certificate verified in streaming, in the companion cyclic
  repository (`frankl-cyclic-sat`, problem 1, closed 2026-08-14).
- **26 groups contain no 15-cycle.** By the arithmetic minimality
  criterion of `notes-minimality-15.md` (order-15/30/45 transitive groups
  cannot be 15-cycle-free or do not exist — Lemma 5 — and the census is
  complete up to S15-conjugacy), every minimal transitive group among
  them is one of **15T5 = A₅(15), 15T9 = [5²]3, 15T26 = [3⁴]5**, each
  *certified* minimal by pure divisibility. The remaining 23 groups all
  contain one of these three as a **literal** subgroup (the smaller census
  entry's generators are elements of the larger group — verified by
  membership in the full enumeration; `results/minimality15_scan.json`).
  Conjugacy in S15 is a relabeling of points and does not affect verdicts.

**Step 3 (the three instances are UNSAT).** For each M ∈ {15T5, 15T9,
15T26}, the constraint system "F union-closed, M-invariant, non-trivial
sets of size ≥ 3, margin ≤ −1" is unsatisfiable. Each verdict was obtained
by **two independent methods plus a machine-checked certificate** — an
upgrade over degree 14, applying the lesson of the Z15 closure (stream-
verifiable LRAT instead of DRAT):

| Group | Name    | Order | Nontrivial orbits | Clauses   | CP-SAT (s) | cadical --lrat (s) | lrat-check |
|-------|---------|-------|-------------------|-----------|------------|--------------------|------------|
| 15T5  | A₅(15)  | 60    | 686               | 4,323,016 | INFEASIBLE, 59.1 | UNSAT (exit 20), 93.2 | c VERIFIED |
| 15T9  | [5²]3   | 75    | 478               | 2,500,889 | INFEASIBLE, 31.7 | UNSAT (exit 20), 28.5 | c VERIFIED |
| 15T26 | [3⁴]5   | 405   | 222               | 257,808   | INFEASIBLE, 2.2  | UNSAT (exit 20), 0.6  | c VERIFIED |

Machines and artifacts: Apple M4, 16 GB; CP-SAT = OR-Tools native model
(margin as a linear integer constraint over orbit variables); CaDiCaL
3.0.1 on frozen CNFs (binary-adder encoding, independent of CP-SAT's;
sha256 in `results/cnf/SHA256-15T-cnf.txt`); text LRAT proofs
(3.9 MB + 54.9 MB + 162.2 MB, sha256 in `results/cnf/SHA256-15T-lrat.txt`)
verified by `lrat-check` (drat-trim repository). Solve + verification of
all three instances took 2 min 26 s wall-clock — the degree-15 SAT phase
is smaller than the single hardest degree-14 instance (14T2, 1234 orbits,
55 min), because the census reduction leaves only groups of order ≥ 60,
hence fewer subset orbits than the regular degree-14 cases.

**Conclusion.** Let F be non-trivial, union-closed, G-invariant, G
transitive of degree 15, and suppose F violates Frankl (margin ≤ −1); by
Step 0 assume its non-trivial sets have size ≥ 3. By Step 2, G contains
either a regular Z15 or a conjugate of one of 15T5, 15T9, 15T26; by
Step 1, F is invariant under that subgroup; by Step 3 (and the certified
cyclic result for Z15) no such F exists. Contradiction. ∎

## Validation of the pipeline

The group encoder is the one validated for the degree-14 theorem (DIMACS
byte-identical to the published cyclic encoder on shared cases). Before
tonight's production runs it was re-checked on the standard controls:
Z7 and Z11 INFEASIBLE with `min_size = 3`
(`results/logs/t9_controls_gauntlet.log`). The census cycle filter acts
on cycle types in the degree-15 action, never on element orders, and the
LRAT chain uses `--no-binary` (lrat-check reads text) with the verdict
taken from the `c VERIFIED` line, never from exit codes alone.

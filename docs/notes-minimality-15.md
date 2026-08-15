# Note — Minimality lemma for degree 15

Goal: reduce the decision "does there exist a union-closed G-invariant F with
margin ≤ −1, for G transitive of degree 15 with no 15-cycle" (26 groups of the
census, `STATE/census15.json`) to a **short list of instance groups**.

Conventions: points = {0,…,14}; F ⊆ P([15]); G ≤ S15 transitive;
"cycle-free" = no element of G has cycle type (15). Lemmas 1–2 of the
degree-14 note (`notes-minimality.md`) hold verbatim: invariance
descends to subgroups, and every subgroup of a cycle-free group is cycle-free.

## Source of the census (different from degree 14, with double verification)

`STATE/trans15.grp` = GAP's transitive groups library (A. Hulpke), copied from
`https://raw.githubusercontent.com/hulpke/transgrp/master/data/trans15.grp`,
sha256 `89cd49a642797ba47f97b6ecd2addd0ca7c3def99b79435a37ccecb57cbcca00`
(on 2026-08-14 the LMFDB API is behind a reCAPTCHA protection; the GAP
library is the primary source of the same classification). The build
(`scripts/census15_build.py`) cross-checks two independent sections of the
file: for every enumerable group the BFS order computed from the generators
(TRANSGRP) must match the declared order (TRANSPROPERTIES), or the build
fails. Outcome: 104 groups, 78 with a 15-cycle (explicit verified witness or
enumeration), 26 without, 0 open cases.

**Warning (degree-15 trap):** a 15-cycle is an *even* permutation,
so the degree-14 parity shortcut ("even generators ⇒
no cycle") does not exist here, and indeed it is not used. Instructive
example: 15T72 = PSL(4,2) ≅ A8 on PG(3,2) **has** a 15-cycle (Singer cycle
of GL(4,2)) despite having no elements of order 15 in the natural action on
8 points — the filter is on the cycle type in the degree-15 action, never
elsewhere.

## Lemma 3 (order of transitive groups)
H transitive of degree 15 ⇒ 15 | |H| (orbit–stabilizer). By Cauchy
H contains elements of order 3 and of order 5. ∎

## Lemma 5 (exclusion of orders 15, 30, 45)
No cycle-free transitive group of degree 15 has order 15 or 30; order 45
does not occur at all among the transitive groups of degree 15.

*Proof.* (15) A transitive group of order 15 is regular; the only group of
order 15 is C15 (Sylow: n₃ = n₅ = 1), and a generator of a regular C15 is a
15-cycle. (30) Every group of order 30 contains a subgroup C15: if
n₅ = 6 and n₃ = 10 simultaneously, the elements of order 5 and 3 alone would
number 6·4 + 10·2 = 44 > 29, absurd; hence one Sylow subgroup (3 or 5) is
normal and the product P₃P₅ is a subgroup of order 15 = C15. In a transitive
H of order 30 the stabilizer has order 2, and C15 ∩ Stab has order dividing
gcd(15,2) = 1: C15 acts with orbits of size 15, that is, regularly — one of
its generators is a 15-cycle, which lies in H (Lemma 2 in the other
direction: H would contain it). (45) A group of order 45 is abelian
(n₃ = n₅ = 1 and groups of order p² are abelian); an abelian transitive
permutation group is regular (the stabilizers, all conjugate and equal, fix
everything), so it would have order 15 ≠ 45. ∎

## Arithmetic minimality criterion (via completeness of the census)
Let G be cycle-free in the census. A hypothetical proper transitive subgroup
H < G would be: cycle-free (Lemma 2), of order a proper divisor of |G|
(Lagrange), and S15-conjugate to a census entry (completeness of the
transitive library) — hence to a **cycle-free** entry with the same
order. If no order from the set

  O = {60, 75, 120, 150, 300, 360, 405, 600, 720, 810, 1620, 2520,
       3240, 4860, 9720, 19440}   (orders of the 26 cycle-free groups)

properly divides |G|, then G is minimally transitive — certified.

It applies to three groups (orders 15, 30, 45 are already excluded by
Lemma 5, and 135 does not appear in the census, so no transitive group of
that order exists):

- **15T5 = A₅(15)**, order 60 (relevant proper divisors: 15, 30 — excluded);
- **15T9 = [5²]3 = C₅²⋊C₃**, order 75 (only candidate: 15 — excluded);
- **15T26 = [3⁴]5 = C₃⁴⋊C₅**, order 405 (candidates 15, 45, 135 — excluded).

## Literal witnesses for the other 23
The GAP library uses incremental generators: for each of the 23 remaining
groups, the generators of a smaller census entry are
**literally elements** of the group (verified by membership in the
complete enumeration) and generate a transitive subgroup of proper
order — an explicit witness, no conjugacy argument needed.
The descent lands on the minimal list in one step:

- → 15T5 (A₅): 15T10 = S₅(15), 15T20 = A₆(15), 15T28 = S₆(15), 15T47 = A₇(15);
- → 15T9: 15T12, 15T13, 15T14, 15T17, 15T18, 15T19, 15T27 ([5²] family);
- → 15T26: 15T33, 15T34, 15T35, 15T41, 15T42, 15T43, 15T52, 15T53,
  15T61, 15T62, 15T63, 15T70 ([3⁴] family).

A cleaner outcome than degree 14: **no UNKNOWN cases** (at degree 14 the
precautionary 14T12 remained). Scan: `scripts/minimality15_scan.py`, output
`results/minimality15_scan.json`.

## Covering theorem (identical to degree 14, with updated MIN)
Let MIN = {15T5, 15T9, 15T26}. If for every M ∈ MIN there is no
union-closed M-invariant F with margin ≤ −1, then there is none for any
of the 26 cycle-free groups. (Same proof as in the degree-14 note:
finite descending chain + conjugation; margins are invariant under
relabeling of the points.) ∎

The groups **with** a 15-cycle (78) contain a regular ⟨σ⟩ ≅ Z15, conjugate
to the standard Z15: they are covered by the certified cyclic result of
2026-08-14 (`results/Z15-CLOSED.md`, UNSAT + verified LRAT).

## Orbit sanity checks (hand computations, reproduced by the scan)
- A₅(15): identity 2¹⁵; 15 involutions with 3 fixed points (2⁹); 20 elements
  of order 3 with no fixed points (2⁵); 24 of order 5 with no fixed points
  (2³). Burnside: (32768 + 15·512 + 20·32 + 24·8)/60 = 41280/60 = **688**.
- [5²]3: (32768 + 12·2⁷ + 12·2³ + 50·2⁵)/75 = 36000/75 = **480**
  (12 elements of order 5 with 5 fixed points, 12 with none, 50 of order 3
  with no fixed points).
If a future scan does not reproduce these numbers, there is a bug in the scan.

## Final instance list (by decreasing orbit count)

| group | order | orbits (Burnside) | status |
|---|---|---|---|
| 15T5 = A₅(15) | 60 | 688 | minimal (arithmetic) |
| 15T9 = [5²]3 | 75 | 480 | minimal (arithmetic) |
| 15T26 = [3⁴]5 | 405 | 224 | minimal (arithmetic) |

All smaller than the worst case already solved at degree 14
(14T2 = D₇, 1236 orbits, CaDiCaL 55 min): the SAT cost of degree 15,
measured in orbits, is lower than that of degree 14.

*Originally written in Italian as the campaign's working record; translated to English on 15 Aug 2026 (the Italian original is preserved in git history).*

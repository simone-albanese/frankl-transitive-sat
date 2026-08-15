# Note — Minimality lemma for degree 14

Goal: reduce the decision "does there exist a union-closed G-invariant F with
margin ≤ −1, for G transitive of degree 14 with no 14-cycle" (26 groups of the
census, `STATE/census14.json`) to a **short list of instance groups**.

Conventions: points = {0,…,13}; F ⊆ P([14]); G ≤ S14 transitive;
"cycle-free" = no element of G has cycle type (14).

## Lemma 1 (descent of invariance)
If F is G-invariant and H ≤ G, then F is H-invariant.
*Proof.* Every h ∈ H lies in G. ∎

## Lemma 2 (heredity of cycle-freeness)
If H ≤ G and H contains a 14-cycle, that 14-cycle lies in G.
Hence every subgroup (in particular every transitive subgroup) of a
cycle-free group is cycle-free. ∎

## Lemma 3 (order of transitive groups)
H transitive of degree 14 ⇒ 14 | |H| (orbit–stabilizer). In particular
H contains an element of order 7 (Cauchy). ∎

## Lemma 4 (2-generation of the minimal groups, fpf case)
Let M ≤ S14 be **minimally transitive** (no proper transitive subgroup)
and let a ∈ M be of order 7 **with no fixed points** (cycle type (7,7)).
Then M = ⟨a, x⟩ for some x ∈ M.
*Proof.* The orbits of ⟨a⟩ are two 7-sets O1, O2. M transitive ⇒ there exists
x ∈ M with x(p) ∈ O2 for some p ∈ O1. The orbit of p under ⟨a,x⟩ contains
O1 (via a) and x(p) ∈ O2, hence all of O2 (via a): ⟨a,x⟩ is transitive.
By minimality M = ⟨a,x⟩. ∎

Note: if EVERY element of order 7 of G is fpf (flag `order7_all_fpf` in the
scan), Lemma 4 applies to every minimally transitive M ≤ G (the order-7
element of M, Lemma 3, is fpf because it is an element of G).

## Computational minimality criterion (complete certificate)
Let G be enumerable with all its 7-elements fpf. Let a_1,…,a_k be
representatives of the G-conjugacy classes of the elements of order 7. Then:

  G has a proper transitive subgroup ⟺
  ∃ i, ∃ x ∈ G such that ⟨a_i, x⟩ is transitive and proper.

*Proof.* (⇐) obvious. (⇒) H < G transitive contains a minimally transitive M
(finite descending chain), M < G. M contains b of order 7 (Lemma 3),
b = g a_i g⁻¹ for some i and g ∈ G. Then g⁻¹Mg is minimally transitive,
contains a_i, and by Lemma 4 g⁻¹Mg = ⟨a_i, x⟩, proper. ∎

Hence the exhaustive loop "for every representative a_i, for every x ∈ G:
⟨a_i,x⟩ transitive ⇒ it must close over all of G" **certifies** minimality.
(Cost trick: if the BFS closure exceeds |G|/2, by Lagrange it equals G.)

## Covering theorem (the reduction)
Let MIN be the set of the cycle-free groups of the census that are minimally
transitive. If for every M ∈ MIN there is no union-closed M-invariant F with
margin ≤ −1, then there is none for ANY of the 26 cycle-free groups.

*Proof.* Let F be a G-invariant counterexample, G cycle-free. G contains a
minimally transitive M₀ (finite chain); M₀ is cycle-free (Lemma 2) and
transitive, hence conjugate in S14 to an M ∈ MIN of the census: M = s M₀ s⁻¹.
F is M₀-invariant (Lemma 1); then F^s = {s(A) : A ∈ F} is M-invariant,
union-closed, with the same |F|, the same frequencies up to a permutation of
the points, the same margin. Contradiction. ∎

**Practical consequence:** it suffices to decide (UNSAT/SAT) only the groups
of MIN.

## Facts already established about the extreme cases
- A regular subgroup of order 14 is C14 or D7. Regular C14 = ⟨14-cycle⟩:
  impossible in the cycle-free groups. Hence "transitive subgroup of order 14"
  ⟺ "regular D7" (every transitive group of order 14 on 14 points is regular).
- In a regular D7 the involutions have type 2^7 (odd!) ⇒ no
  subgroup of A14 contains a regular D7. In particular 14T62 = A14 and
  14T59 ≤ A14 are not covered by D7: witnesses of larger proper transitive
  subgroups are needed (the scan constructs them explicitly:
  for A14 the generators of 14T30 = PSL(2,13), all even; for 14T59 a
  ⟨(7,7)-element, even block-swap⟩ inside (S7≀S2)∩A14).
- 14T2 = D7 is minimally transitive (order 14: the proper subgroups have
  order ≤ 7, not divisible by 14, Lemma 3).
- 14T30 = PSL(2,13): the involutions fix 2 points (q=13 ≡ 1 mod 4), hence
  no regular D7; expected minimal (the scan certifies or refutes it).

## What the scan produces (`scripts/minimality_scan.py`)
For each of the 26: order, number of orbits of P([14]) via Burnside
(1/|G|)·Σ_g 2^{c(g)} (enumerable groups only), flag `order7_all_fpf`,
and exactly one of:
- `minimal_certified: true` (exhaustive criterion above), or
- `witness`: explicit generators of a proper transitive subgroup
  (⇒ not minimal, covered recursively by the descending chain), or
- `UNKNOWN` (large group, sampling inconclusive) ⇒ follow-up task.

The **final list of instance groups** = {certified minimal} ∪ {UNKNOWN
left over after the follow-ups}, ordered by number of orbits (Burnside).

Reference to verify (separate task, non-blocking): arXiv:1701.02374
on minimally transitive groups — useful as external confirmation of the list.

Expected sanity checks: regular D7 ≈ 1236 orbits ((2^14 + 6·2^2 + 7·2^7)/14 = 1236);
PSL(2,13) ≈ 52 orbits (hand computation from the classes). If the scan does
not reproduce these two numbers, there is a bug in the scan.

## OUTCOME (2026-08-12, `results/minimality_scan.json`)
Sanity checks D7=1236 and PSL(2,13)=52 reproduced. Final list of instance
groups (coverage valid for all 26 cycle-free groups — the NOT_MINIMAL ones
all have an explicit verified witness):

| group | order | orbits (Burnside) | status |
|---|---|---|---|
| 14T2 = regular D7 | 14 | 1236 | certified minimal |
| 14T6 = [2^3]7 | 56 | 424 | certified minimal |
| 14T10 = L_7(14) | 168 | 156 | certified minimal |
| 14T12 = 1/2[D(7)^2]2 | 196 | 172 | UNKNOWN (included out of caution)¹ |
| 14T30 = PSL(2,13) | 1092 | 52 | certified minimal |

¹ 14T12 has 7-elements with fixed points: the criterion of Lemma 4 does not
apply. No proper transitive ⟨a,x⟩ exists (checked over ALL x);
it could be minimal, or it could have ≥3-generated transitive subgroups whose
7-elements are all non-fpf. Including it in the list is correct either way
(a superset of MIN); it has only 172 orbits, deciding it via SAT is cheap.
14T46 (fpf, order 5040) resolved by exhaustive post-scan search:
NOT_MINIMAL, witness of order 42 (`results/logs/t46_exhaustive.log`).

*Originally written in Italian as the campaign's working record; translated to English on 15 Aug 2026 (the Italian original is preserved in git history).*

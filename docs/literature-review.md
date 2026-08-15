# Literature review — positioning the results (sweep of 2026-08-14)

**Question.** Are these theorems new, and where do they sit?
(i) cyclic results: no Z13/Z14/Z15-invariant union-closed family violates
Frankl, with verified certificates; (ii) transitive theorems: full degrees
14 and 15.

**Verdict: no overlapping prior work found.** Sweep of arXiv + general web
on 2026-08-14 (queries: transitive/symmetric/invariant union-closed;
cyclic verification; SAT/DRAT/certificates for Frankl; 2023–2026
recency passes). Confidence: high, not absolute — MathSciNet/zbMATH not
directly consulted (paywall), non-English literature not searched.
Everything found nearby is *complementary*, and several finds strengthen
the paper's framing. Details below.

## 1. General exhaustive verification (no symmetry assumption)

- m ≤ 11: Bošnjak–Marković (2008).
- m ≤ 12: Vučković–Živković, *The 12-element case of Frankl's
  conjecture*, IPSI Transactions on Advanced Research, Jan 2017.
- |F| ≤ 50 sets: Roberts–Simpson (Australas. J. Combin. 47, 2010).

⇒ On 13, 14, 15 points the general conjecture is **open**; our invariant
results live exactly beyond the exhaustive frontier. No trace of a
completed m = 13 general verification.

## 2. The constant line (general families)

Gilmer (arXiv 2022): first constant 0.01 → within days improved to
(3−√5)/2 ≈ 0.38197 (Alweiss–Huang–Sellke, Chase–Lovett, Sawin, Pebody,
independently) → best current ≈ **0.38271** (Liu, building on Yu and
Sawin). The full 1/2 is open. Our results give the full 1/2 for
*invariant* families on ≤ 15 points — a different axis (special families,
exact bound vs all families, partial bound). Note: the project's
"ratio < 0.382 ⇒ bug" sanity rule is precisely this constant.

## 3. The invariant/symmetric line (our line)

- **Johnson–Vaughan**, *On union-closed families, I*, JCTA 84 (1998):
  precursor — for translate-generated families yields an element in
  ≥ (|F|−1)/2 of the sets (noted by AEL as "not quite enough").
- **Polymath11** (Gowers' blog, 2016): asked the cyclic-translates
  question.
- **Aaronson–Ellis–Leader**, *A note on transitive union-closed
  families*, Electron. J. Combin. 28(2) (2021), arXiv:2010.08795.
  Theorem 1: for F = {A+R : A ⊆ Z_n} (all unions of cyclic translates of
  ONE fixed set R), average set size ≥ n/2, hence UCC holds. Theorem 2:
  same over any finite Abelian group. **One generating orbit, regular
  abelian action, every n.** Our results are the complementary axis:
  **every** invariant family (any set of generating orbits), **every**
  transitive group (non-abelian included), fixed small degrees, decided
  with certificates.
- **Nived J M**, *Symmetric union closed families*, arXiv:2411.06588
  (Nov 2024, preprint): 1-orbit cyclic case re-proved + cylindrical/torus
  grid graph families. Still one orbit; no whole-degree decisions.
- **Koutsoukou-Argyraki & Paulson**, *Transitive union-closed families*,
  Archive of Formal Proofs, 2025-01-20: Isabelle/HOL formalization of
  the AEL theorem. No computational cases. Shows (a) the subtopic is
  alive in 2025, (b) the formal-methods community touches it — aligning
  with our cake_lpr angle.

Nothing found on: multi-orbit invariant families; non-abelian transitive
groups; complete degrees 14/15; margin-0 uniqueness of the power set.

## 4. Computational-certified tradition on Frankl (method kin)

- **Pulaj**, *Cutting planes for families implying Frankl's conjecture*,
  Math. Comp. 89 (2020), arXiv:1702.05947 (+ thesis; + arXiv:1903.02317
  proving Morris' 3-sets conjecture): exact rational IP with verification
  routines, FC-families. Closest methodological relative on Frankl.
- **Marić–Vučković–Živković**, *Formalizing Frankl's conjecture:
  FC-families* (2012): Isabelle-verified combinatorial search.
- *Fully automatic, verified classification of all FC(6) set families*,
  arXiv:1902.08765 (2019).
- Outside Frankl, the certificate tradition our pipeline follows:
  Ramsey R(3,8)/R(3,9) via SAT + verified certificates (arXiv:2502.06055,
  2025); SAT-modulo-symmetries + Lean graph generation (2025).

**No SAT/DRAT/LRAT-based work on Frankl found at all** — ours appears to
be the first, and the first Frankl computation with formally verified
proof checking of solver certificates (cake_lpr).

## 5. A template cousin in another conjecture

**Tong–Wu–Du**, *On Rivest–Vuillemin conjecture for fourteen variables*,
arXiv:1701.02374: verifies elusiveness of monotone boolean functions
invariant under **transitive groups on 14 points** — the same
census-of-transitive-groups reduction pattern at the same degree.
Useful cross-check for our degree-14 minimal-groups bookkeeping and
precedent that "whole transitive degree n" is a recognized unit of
progress. (NB: `notes-minimality.md` cites this as "minimal transitive
groups paper" — imprecise wording; fix if cited in the paper.)

## 6. Claimed full proofs (monitor, do not cite as settled)

- arXiv:1507.01270 (2015, v3), *Proof of union-closed sets conjecture* —
  not accepted; the 2022–2026 constant-chase implies community consensus
  that the conjecture is open.
- A Jan 2026 preprint (*An algorithmic proof of Frankl's union-closed
  sets conjecture*, ResearchGate) — unreviewed claim. Re-check status
  before submitting the note; if a general proof is ever accepted, our
  results' interest reduces to the certified-methodology story.

## How to state our results for this audience

1. Lead with the **equal-frequency reformulation**: transitivity ⇒ all
   point frequencies equal ⇒ UCC for the family ⟺ average set size
   ≥ m/2. This is the same currency as AEL's theorems ("average ≥ n/2")
   and makes the complementarity exact: AEL prove it for one-orbit
   families over abelian groups for every n; we decide it for **all**
   invariant families over **all** transitive groups for m ≤ 15.
2. State the certificate standard prominently (frozen CNF hashes, LRAT,
   lrat-check + cake_lpr): it matches the strongest current practice in
   SAT-assisted combinatorics (Ramsey 2025) and exceeds what any prior
   Frankl computation shipped.
3. Cite Pulaj + FC-formalizations as the Frankl-computational lineage;
   AFP 2025 as the formal-methods connection; Rivest–Vuillemin-14 as the
   whole-degree precedent.
4. Margin-0 uniqueness (power set) appears unstudied — state as a
   standalone small result.

## Gaps of this review

MathSciNet/zbMATH not searched directly; Polymath11 threads not read
exhaustively; non-English venues unchecked. Residual risk judged low
(the AEL reference list + two surveys — Bruhn–Schaudt 2013
arXiv:1309.3297, *Notes on the UCC* 2022 arXiv:2208.03803 — triangulate
the same map found here).

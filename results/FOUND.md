# FOUND — The degree-14 theorem (a negative result of value)

Date: 2026-08-12 · Status: SUCCESS per GOAL.md ("risultato negativo di
valore, grado 14" — a negative result of value, degree 14), verified with an
independent method (CP-SAT + DRAT).

## Statement

**Theorem.** Every nontrivial union-closed family F ⊆ P([14]) invariant
under ANY transitive permutation group G ≤ S14 satisfies Frankl's
conjecture: there exists an element contained in at least half of the sets
of F (in integers: 2·maxfreq ≥ |F|; no family with margin
2·maxfreq − |F| ≤ −1 exists).

This extends beyond prime degrees the corollary that on 13 points followed
from Cauchy (the cyclic case Z13/Z14 was already closed in the
`frankl-cyclic-sat` repo, DOI 10.5281/zenodo.21900943, with DRAT
certificates).

## Logical chain

1. **Invariance descent** (Lemma 1, `docs/notes-minimality.md`):
   F G-invariant ⟹ F H-invariant for every H ≤ G. Hence an UNSAT on a
   transitive subgroup H implies UNSAT on every overgroup G ≥ H.
2. **Reduction to the minimal groups** (`docs/notes-minimality.md`,
   `results/minimality_scan.json`): every transitive G of degree 14 contains
   a minimal transitive M. Two cases:
   - G contains a 14-cycle ⟹ G ⊇ Z14, a case closed by the cyclic repo
     (Z14 UNSAT for sizes ≥ 3, DRAT certificate, DOI above);
   - G has no 14-cycle ⟹ M has no 14-cycle (Lemma 2) and, up to
     conjugacy in S14, M is one of the 5 groups in the list below
     (certified scan: 14T2/6/10/30 certified minimal; 14T12 included
     conservatively as UNKNOWN — deciding it via SAT costs less than
     classifying it, and an UNSAT on it covers its overgroups anyway).
   Conjugation in S14 does not change the outcome (a relabeling of points).
3. **The 5 groups are all UNSAT** for families of size ≥ 3 (Sarvate–Renaud
   reduction: sizes ≤ 2 conform trivially), with DOUBLE independent
   verification: CP-SAT (OR-Tools, T6) and cadical with a DRAT certificate
   verified by drat-trim (T7).

## Table of the 5 group instances

| Group  | Name            | Order | Nontrivial orbits | Clauses   | CP-SAT (T6)        | cadical (T7) | drat-trim (T7)            |
|--------|-----------------|-------|-------------------|-----------|--------------------|--------------|---------------------------|
| 14T2   | D_14(14)=[7]2   | 14    | 1234              | 7,098,740 | INFEASIBLE, 74.0 s | UNSAT (exit 20) | s VERIFIED, 2,939.8 s  |
| 14T6   | [2^3]7          | 56    | 422               | 1,137,222 | INFEASIBLE, 7.5 s  | UNSAT (exit 20) | s VERIFIED, 4.0 s      |
| 14T10  | L_7(14)         | 168   | 154               | 159,203   | INFEASIBLE, 0.6 s  | UNSAT (exit 20) | s VERIFIED, 0.12 s     |
| 14T12  | 1/2[D(7)^2]2    | 196   | 170               | 146,706   | INFEASIBLE, 0.6 s  | UNSAT (exit 20) | s VERIFIED, 0.21 s     |
| 14T30  | L(14)=PSL(2,13) | 1092  | 50                | 10,134    | INFEASIBLE, 0.1 s  | UNSAT (exit 20) | s VERIFIED, 0.06 s     |

Sources: `results/t6_decide.json`, `results/logs/t7_14T*.log`,
`STATE/census14.json` (63 transitive groups of degree 14, 26 without a
14-cycle), `results/minimality_scan.json`.

## How to re-verify

The CNF files and DRAT certificates are in `results/cnf/` (WARNING:
`14T2.drat` weighs 3.3 GB — do not open it, only feed it to drat-trim).
xz-compressed copies + SHA256SUMS: GitHub release v1.0.0 and permanent
Zenodo archive (DOI 10.5281/zenodo.21920980).

```bash
# 1. Re-verify the existing certificates (no solver needed):
#    exit code 0 and the line "s VERIFIED" = valid certificate.
drat-trim results/cnf/14T30.cnf results/cnf/14T30.drat   # ~0.1 s
drat-trim results/cnf/14T12.cnf results/cnf/14T12.drat   # ~0.2 s
drat-trim results/cnf/14T10.cnf results/cnf/14T10.drat   # ~0.1 s
drat-trim results/cnf/14T6.cnf  results/cnf/14T6.drat    # ~4 s
drat-trim results/cnf/14T2.cnf  results/cnf/14T2.drat    # ~50 min

# 2. Regenerate the CNFs from scratch (the repo's encoder) and rerun:
#    exit 20 = UNSAT (expected). $PY = the venv's python (STATE/hardware.env).
$PY dump_dimacs_group.py <group> 3 results/cnf/<group>.cnf
cadical results/cnf/<group>.cnf results/cnf/<group>.drat  # exit 20

# 3. Independent CP-SAT check:
$PY sat_group.py <group> decide 1200 3        # expected: INFEASIBLE

# 4. Tool sanity (pipeline validated on the controls BEFORE production):
#    Z7 and Z11 INFEASIBLE, DIMACS byte-identical to the cyclic repo's
#    (results/logs/t7_validate.log, results/logs/t5_probe.log).
```

Known caveats: drat-trim's "duplicate literal" WARNINGs are benign; all
verdict arithmetic is over integers (margin = 2·maxfreq − |F|).

## What this result does NOT cover

- Degrees 15 and 16: in the backlog (T9+), not yet started.
- NON-transitive groups: out of scope of GOAL.md.

*Originally written in Italian as the campaign's working record; translated to English on 15 Aug 2026 (the Italian original is preserved in git history).*

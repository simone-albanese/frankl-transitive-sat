# The "margin 0" experiment — characterization of the cyclic extremal families

Date: 2026-08-13 · Status: COMPLETE to the project's standard
(two independent exact methods + a verified LRAT certificate for every
negative outcome).

## Origin

Born from a pattern observed in the data of the cyclic campaign: the power
set hits the threshold of the Frankl conjecture exactly
(integer margin 2·maxfreq − |F| = 0). Question: is it the only one that does?

## Result

**Proposition (m ∈ {7, 11, 13}).** Let F be a union-closed,
Z_m-invariant family with ∅, [m] ∈ F and at least one nontrivial orbit
included. Then:

1. **(Uniqueness of the extremal)** If the margin of F is ≤ 0, then
   F = P([m]) (the full power set), and the margin is exactly 0.
2. **(Gap in the min-3 world)** If moreover every nontrivial set of F has
   size ≥ 3, then the margin of F is ≥ 1: no family even touches the
   threshold.

In other words: under cyclic symmetry not only are there no
counterexamples (margin ≤ −1, already certified by the previous campaign),
but the only way to *touch* the threshold is to take everything, and as
soon as minimum size 3 is imposed, a gap of at least 1 opens up.

## Method (double, with certificates)

Pipeline: `margin_zero.py` — reuses canon_table/build_orbits/build_clauses
from `sat_cyclic.py` (validated) and `pb_adder.py` for the DIMACS.
**Preliminary validation passed**: with rhs=−1 it reproduces INFEASIBLE
on the certified Z7 and Z11 controls.

Experiments for each m ∈ {7, 11, 13}:

| Experiment | Constraints | CP-SAT (method 1) | cadical (method 2) | lrat-check |
|---|---|---|---|---|
| E1a sanity | margin ≤ 0 | FEASIBLE: power set, margin 0 | — (witness) | — |
| E1b uniqueness | margin ≤ 0, ≠ power set | **INFEASIBLE** ×3 | **UNSAT** (exit 20) ×3 | **VERIFIED** ×3 |
| E2 min-3 | margin ≤ 0, sizes ≥ 3 | **INFEASIBLE** ×3 | **UNSAT** (exit 20) ×3 | **VERIFIED** ×3 |

The E1a witness (the power set: |F| = 2^m, margin 0) was verified
for each m by BOTH independent checkers
(`ucs_core.check_family` + `checker2.verify`), integer arithmetic.

CP-SAT timings [M]: Z7 and Z11 < 1 s; Z13 ~16–19 s per experiment.
LRAT certificates: from 5 KB (Z7) to 561 MB (Z13-E1b).

## Artifacts and re-verification

CNF files and certificates in this folder; fingerprints in `SHA256SUMS.txt`.
Encoding: scaled margin Σ r_O(2s_O−m)x_O ≤ 0 (integers; ∅ and [m]
cancel out), non-emptiness Σx ≥ 1, "≠ power set" = clause ∨¬x_O.

```bash
# method 1 (CP-SAT), all three experiments for a given m:
$PY margin_zero.py validate      # first: it must say [OK]
$PY margin_zero.py run 13 900

# method 2 + certificate (example Z13-E1b):
tools/cadical/build/cadical --lrat --no-binary \
    results/margin0/z13_E1b.cnf results/margin0/z13_E1b.lrat   # exit 20
tools/drat-trim/lrat-check results/margin0/z13_E1b.cnf \
    results/margin0/z13_E1b.lrat        # look for "c VERIFIED" in the output
```

Known trap: cadical writes **binary** LRAT by default and the textual
lrat-check answers "NOT VERIFIED" — always use `--no-binary` (or the
lrat-trim in tools/, which reads both). Never trust the exit code alone.

## What this does NOT cover

- Composite m (14, 15): not yet run (feasible: ~1 min CP-SAT for
  Z14; Z15 at the cost of a monolithic decide).
- Non-cyclic transitive groups: the reformulation "margin = m·(average
  size − m/2)·|F|/… " holds for every transitive group; an analogous
  experiment is possible with the group-agnostic pipeline (sat_group.py).
- No direct implication for the general conjecture: this is a
  characterization of the symmetric extremal case.

*Originally written in Italian as the campaign's working record; translated to English on 15 Aug 2026 (the Italian original is preserved in git history).*

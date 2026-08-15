# Degree 15 — CLOSED: transitive theorem with verified certificates (2026-08-14)

**Theorem.** No non-trivial union-closed family F ⊆ P([15])
invariant under a transitive permutation group G ≤ S15 (non-trivial
sets of size ≥ 3, with the Sarvate–Renaud reduction covering the general
case) violates Frankl's conjecture: the integer margin 2·maxfreq − |F| is ≥ 0.

Closed the very evening the blocker fell: the dependency (cyclic Z15, open
problem 1 of the `frankl-cyclic-sat` repo) fell at 19:20 on
2026-08-14 (`Z15-CLOSED.md`); the transitive theorem was closed and
certified at 20:53. Full English statement with proof:
`docs/theorem-degree15.md`; reduction and lemmas: `docs/notes-minimality-15.md`.

## Logical chain

1. **Census** (`scripts/census15_build.py` → `STATE/census15.json`):
   104 transitive groups of degree 15, from Hulpke's GAP library
   `trans15.grp` (sha256 `89cd49a6…`, primary source; the LMFDB API was
   behind reCAPTCHA on 14/08). Two sources for every enumerable group: the
   BFS order of the generators must match the TRANSPROPERTIES section.
   Outcome: **78 with a 15-cycle** (verified witness or enumeration),
   **26 without**, 0 open. Documented trap: the 15-cycle is EVEN
   (no parity shortcut; PSL(4,2) has Singer cycles).
2. **Reduction** (`scripts/minimality15_scan.py` →
   `results/minimality15_scan.json`): the 78 with the cycle contain a
   regular Z15 → covered by this morning's cyclic certificate. Of the 26
   without a cycle, **3 are minimal, certified by pure arithmetic**
   (Lemma 5: orders 15/30/45 impossible; completeness of the census):
   15T5 = A₅(15), 15T9 = [5²]3, 15T26 = [3⁴]5. The other 23 contain
   one of the three as a LITERAL subgroup (the smaller group's census
   generators ∈ the larger group's enumeration, verified). No UNKNOWN
   cases (at degree 14 there was the precautionary 14T12).
3. **Decision — full standard on each of the 3 instances** (two independent
   methods + certificate, LRAT chain inherited from the Z15 lesson):

| instance | orbits | clauses | CP-SAT | cadical --lrat --no-binary | lrat-check | LRAT |
|---|---|---|---|---|---|---|
| 15T5 (A₅) | 686 | 4,323,016 | INFEASIBLE 59.1 s | UNSAT exit 20, 93.2 s, RSS 1.27 GB | **c VERIFIED** | 162.2 MB |
| 15T9 ([5²]3) | 478 | 2,500,889 | INFEASIBLE 31.7 s | UNSAT exit 20, 28.5 s, RSS 1.02 GB | **c VERIFIED** | 54.9 MB |
| 15T26 ([3⁴]5) | 222 | 257,808 | INFEASIBLE 2.2 s | UNSAT exit 20, 0.6 s, RSS 150 MB | **c VERIFIED** | 3.9 MB |

Full SAT phase (solve + verification, driver `scripts/t9_certify.sh`):
**2 min 26 s** of wall-clock time — against the 20h26m of Z15 alone. The
"smart, not harder" reduction did the work: 104 groups → 3 instances, all
smaller than the worst case of degree 14 (14T2: 1234 orbits, 55 min).

## Artifacts (all on disk, to be committed/published)

- Frozen CNFs: `results/cnf/15T{5,9,26}.cnf`,
  sha256 in `results/cnf/SHA256-15T-cnf.txt`
  (15T5: `a5bbb82f…`, 15T9: `8c9ea9ec…`, 15T26: `af711123…`).
- Textual LRAT certificates: `results/cnf/15T{5,9,26}.lrat`,
  sha256 in `results/cnf/SHA256-15T-lrat.txt`; total 221 MB
  (xz-compressible, publishable without size problems).
- Logs: `results/logs/t9_decide_cpsat.log` (method 1),
  `results/logs/t9_certify.log` + `t9_15T*_{cadical,lratcheck}.log`
  (method 2 + verification), `results/logs/t9_controls_gauntlet.log`
  (Z7/Z11 controls), `results/logs/minimality15_scan.log` (reduction).

## How to re-verify

```bash
source STATE/hardware.env
# 1. census and reduction (deterministic, ~4 min):
"$PY" scripts/census15_build.py && "$PY" scripts/minimality15_scan.py
# 2. formulas (deterministic) and fingerprints:
for g in 15T5 15T9 15T26; do "$PY" dump_dimacs_group.py $g /tmp/$g.cnf 3; done
shasum -a 256 /tmp/15T*.cnf   # expected: a5bbb82f… / 8c9ea9ec… / af711123…
# 3. certificates (streaming, ~1 min in total):
for g in 15T5 15T9 15T26; do
  tools/drat-trim/lrat-check results/cnf/$g.cnf results/cnf/$g.lrat | grep VERIFIED
done   # look for "c VERIFIED", never trust the exit code alone
# 4. independent confirmation without certificate (~2 min):
for g in 15T5 15T9 15T26; do "$PY" sat_group.py $g decide 1200 3; done
```

## Consequences and open items

- **Every transitive degree ≤ 15 is now closed** (13 via Cauchy, 14 and 15
  via theorems; degrees ≤ 12 are covered by the unconditional verification
  of the conjecture in the literature).
- Next frontiers, with known prices: monolithic **Z16** remains the wall
  (estimated weeks-months + ~314 GB of proof on this hardware [E]);
  **transitive degree 16** (1954 groups) is blocked by the cyclic anchor
  Z16 for the groups with a 16-cycle; formally verified checking
  (cake_lpr) of the LRAT certificates = a credibility upgrade at low cost.
- To do: commit the new files, update README/FOUND, xz the three
  LRATs, release + new Zenodo version (publication decisions belong to
  the human; Zenodo requires a token).

*Originally written in Italian as the campaign's working record; translated to English on 15 Aug 2026 (the Italian original is preserved in git history).*

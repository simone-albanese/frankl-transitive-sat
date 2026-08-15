# Z15 — CLOSED: UNSAT with a verified certificate (2026-08-14)

**Theorem.** No nontrivial union-closed family F ⊆ P([15]) invariant under
rotation (Z15), with nontrivial sets of size ≥ 3 (Sarvate–Renaud
reduction), violates Frankl's conjecture: the integer margin
2·maxfreq − |F| is always ≥ 0.

This closes **open problem 1** of the `frankl-cyclic-sat` repo
(DOI 10.5281/zenodo.21900943), left open on 2026-08-12 when the run was
stopped by the RAM wall of DRAT verification (an estimated 11–18 GB against
16 physical). The wall was dissolved by switching to the LRAT format, which
is verifiable in streaming.

## Proof standard reached (exceeds the project's criterion)

1. **Method 1 — CP-SAT (OR-Tools 9.15.6755)**, native model (the margin as
   an integer linear constraint, 2,190 orbit variables): INFEASIBLE in 889 s
   (T9a, 2026-08-11; log in the cyclic repo).
2. **Method 2 — CaDiCaL 3.0.1**, independent frozen CNF
   (`results/cnf/z15min3.cnf`, binary-adder encoding, 16,856
   variables / 28,850,111 clauses, sha256
   `e6c732cf30bc619dd4c2706734bdcc2ed99255a422c52c4a8525563785115120`,
   byte-identical to the published formula): **exit 20 = UNSAT** in
   73,544.58 s (20h26m), max RSS 4,793.61 MB, 2026-08-14 18:57:39.
3. **Certificate — a textual LRAT proof** of 158,233,546,333 bytes (147 GB),
   `results/cnf/z15.lrat`, sha256 in `results/cnf/z15.lrat.sha256`.
   Verified by `lrat-check` (drat-trim repo): **"c VERIFIED"** in
   1,358.68 s (22.6 min), 145,241,055 clauses added / 130,164,827
   deleted, max live clauses 28,850,111 — streaming verification uses
   RAM proportional to the formula, not to the proof.

The two methods share only the orbit/closure generator (validated on the
Z7/Z11/P([4]) controls and, downstream, covered by the certificate); the
margin constraint, the encoding and the engines are independent.

## Execution (Route B)

- Driver: `scripts/routeB.sh`, detached launch 2026-08-13 22:31:17,
  no time cap, RAM guard 9 GB / disk 30 GB, hourly heartbeat in
  `results/logs/routeB_driver.log` (full trajectory preserved).
- Proof growth: a constant ~6–8 GB/h. Remaining variables: 51% at 10h, 50%
  until ~17h, 49% at 17h, 48% at 18:30 — **collapse to a verdict in ~27
  minutes** (same pattern as Z14: CDCL refutations end without warning).
- Solver log: `results/logs/routeB_z15.log`; verification:
  `results/logs/routeB_lratcheck.log`.

## How to re-verify

```bash
# 1. Regenerate the formula (deterministic) and check its fingerprint:
$PY dump_dimacs.py 15 z15min3.cnf 3
shasum -a 256 z15min3.cnf   # expected: e6c732cf...

# 2. Verify the certificate (streaming, ~23 min, RAM ~1-2 GB):
tools/drat-trim/lrat-check results/cnf/z15min3.cnf results/cnf/z15.lrat
# look for the line "c VERIFIED" in the output (never trust the exit code alone)

# 3. Independent confirmation without the certificate (about 15 min):
$PY sat_cyclic.py ... # native CP-SAT model, expected INFEASIBLE
```

## Consequences and next steps

- The cyclic corollary now covers m ∈ {13, 14, 15} with a certificate.
- **Green light for the degree-15 transitive theorem** (T9): a census of
  the transitive groups of degree 15 without a 15-cycle + this result ⇒
  "no union-closed family invariant under a transitive group on 15 points
  violates the conjecture" — no longer conditional.
- To do: archival of the certificate (xz), a new Zenodo version of the
  cyclic repo, an update of `docs/open-problems.md` (problem 1 →
  solved), a commit of this record.

**Do NOT delete `results/cnf/z15.lrat`**: it is the certificate. (147 GB;
compressing it with xz will take hours but should bring it below 30 GB.)

*Originally written in Italian as the campaign's working record; translated to English on 15 Aug 2026 (the Italian original is preserved in git history).*

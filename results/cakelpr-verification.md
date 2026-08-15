# Formally verified checking of the LRAT certificates (cake_lpr)

Date: evening of 2026-08-14. Goal: shrink the trusted base of the
results by eliminating the unverified checker (`lrat-check`, hand-written
C) as the weak link: every LRAT certificate in the project is re-verified
with **cake_lpr**, a checker whose correctness is a machine-checked
theorem (HOL4) that covers the *compiled binary* (CakeML compiler, itself
verified). This resolves open problem 5 of the cyclic repo for the LRAT
part — made cheap by the fact that, after the Z15 lesson, new
certificates are born directly in LRAT (no conversion).

## Tool provenance and build

- Repo: `github.com/tanyongkiam/cake_lpr` (cloned into `tools/cake_lpr`),
  which declares the HOL4/CakeML commits used for generation; the
  pre-generated assembly files match the fingerprints declared in the repo
  (`cake_lpr.sha256`): `cake_lpr_arm8.S` sha256 `95b64883…`.
- NATIVE arm64 build on the M4: `make cake_lpr_arm8` (no Rosetta).
- Heap/stack sizes: since July 2026 they are passed on the command line
  (`--CML_HEAP_SIZE=<MB>`), no longer via environment variables.

## Shakedown tests (protocol: never trust an untested tool)

1. Repo example (`example.cnf` + `example.lpr`): `s VERIFIED UNSAT` ✓
2. **Negative control 1** — TRUNCATED 15T26 certificate: rejected
   ("Checking failed … failed to parse line") ✓
3. **Negative control 2** — 15T26 certificate with one literal NEGATED
   mid-file (line 20717, 59 → −59): rejected ("clause index has no
   reduction sequence") ✓
4. **Trap confirmed**: the exit code is 0 even on failures — the
   verdict must be read ONLY from the `s VERIFIED UNSAT` line (same
   hygiene already in use with drat-trim/lrat-check).

## Results (measured on the M4, machine otherwise idle)

| certificate | contents | cake_lpr | time | max RSS |
|---|---|---|---|---|
| 15T26.lrat (3.9 MB) | degree 15, [3⁴]5 | **s VERIFIED UNSAT** | 0.3 s | 0.7 GB |
| 15T9.lrat (55 MB) | degree 15, [5²]3 | **s VERIFIED UNSAT** | 4.0 s | 3.0 GB |
| 15T5.lrat (162 MB) | degree 15, A₅ | **s VERIFIED UNSAT** | 9.1 s | 3.5 GB |
| margin0: z7_E1b, z7_E2, z11_E1b, z11_E2, z13_E1b, z13_E2 | uniqueness of the power set at margin ≤ 0 | **6/6 s VERIFIED UNSAT** | < 1 s each | — |
| z15.lrat (147 GB) | cyclic Z15 | **NOT COMPLETED: heap exhausted** | 3 h 10 m | 6.5 GB RSS (footprint 12.9 GB) |

## Z15 outcome (2026-08-15, 01:05): a resource limit, NOT a negative verdict

Run `scripts/cakelpr_z15.sh` (2026-08-14 21:57 → 2026-08-15 01:05,
CakeML heap 12 GB): terminated with **"CakeML heap space exhausted"**
after 11,393 s, at an estimated [E, from 12 MB/s measured via
proc_pidfdinfo] 80–85% of the file. Honest interpretation:

- **It says nothing against the certificate**: z15.lrat remains VERIFIED
  by the streaming checker `lrat-check` ("c VERIFIED", 22.6 min,
  Z15-CLOSED.md record). The failure is the verified checker's, due to
  memory.
- **Quantified cause [M/E]**: the proof keeps up to 28,850,111
  clauses alive (measured by lrat-check); the CakeML representation costs
  ~4–6× the C one and the copying GC doubles the requirement → some
  ~15–25 GB of heap are needed: a machine with 16 GB of physical RAM is
  below the threshold for the monolithic check. The 9 certificates up to
  162 MB (degree 15 + margin0) do NOT have this problem: 9/10 VERIFIED
  by cake_lpr.
- Tooling lesson: real throughput 12 MB/s = ~10× lrat-check
  (the 2.3× extrapolation from the small certificates was off by 4×).

## Paths to complete the 10/10 (human decision)

1. **A bigger machine** (the route of the cake_lpr project itself: their
   Makefile provides for a 64 GB heap): a 64 GB cloud instance for a
   ~4–6 h run. Cost: a few euros + setup; low risk.
2. **cake_lpr's compositional mode** (intervals i–j + summary + coverage
   `-check`): built precisely for huge proofs on limited RAM; requires
   studying the format and a split script (~half a day of work);
   everything stays on this Mac.
3. **14–15 GB heap on this Mac**: concrete probability of another
   exhaustion (estimated requirement above 15 GB) + swap/crawl.
   Not recommended: high cost, uncertain outcome.
4. **Accept 9/10** and state the limit in the paper: Z15 remains
   covered by lrat-check; the cake_lpr perimeter covers everything else.
   Already scientifically honest and publishable.

## What changes in the trusted base

Before: formula generator (validated with the double method and shakedown
tests) + solver (untrusted: it produces certificates) + **lrat-check
(unverified C, trusted blindly)**.
After: the third link disappears — all that remains to trust is the
formula generator (~60 lines, mitigated by the two independent methods)
and the HOL4 kernel. The degree-14 certificates (DRAT, not LRAT) are not
covered by this step: they would need to be regenerated in LRAT or
converted by drat-trim — a possible extension, cost ~1–2 h [E].

## How to re-verify

```bash
cd tools/cake_lpr && shasum -a 256 -c cake_lpr.sha256 && make cake_lpr_arm8
cd ../.. && for g in 15T5 15T9 15T26; do
  tools/cake_lpr/cake_lpr results/cnf/$g.cnf results/cnf/$g.lrat
done   # expected: "s VERIFIED UNSAT" ×3 (verdict from the line, NOT from the exit code)
tools/cake_lpr/cake_lpr --CML_HEAP_SIZE=12288 --CML_STACK_SIZE=4096 \
  results/cnf/z15min3.cnf results/cnf/z15.lrat   # ~1 h
```

*Originally written in Italian as the campaign's working record; translated to English on 15 Aug 2026 (the Italian original is preserved in git history).*

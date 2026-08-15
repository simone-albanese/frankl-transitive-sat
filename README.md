# Frankl's Conjecture Beyond Cyclic Symmetry

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21920980.svg)](https://doi.org/10.5281/zenodo.21920980)

**Two computer-assisted theorems: no union-closed family that is symmetric
under *any* transitive permutation group on 14 or 15 points violates Frankl's
conjecture. The infinitely-many-groups problem is reduced, by short minimality
lemmas and certified computation, to a handful of SAT instances — each decided
by two independent exact methods, each carrying a machine-checkable proof
certificate, most re-verified by a formally verified checker. Together with
the predecessor's cyclic results and the degree-13 Cauchy corollary, the
transitive case of Frankl's conjecture is closed up to 15 points.**

This is the sequel to
[frankl-cyclic-sat](https://github.com/simone-albanese/frankl-cyclic-sat),
which settled the *rotation*-invariant case of the conjecture on 13 and 14
points. That repository is the on-ramp: its README explains the conjecture,
SAT solvers and proof certificates assuming no prior knowledge, and everything
here inherits its code, its verification standard and its paranoia. This
repository answers the question the predecessor explicitly left open (its open
problem 4): on 14 points, rotations are not the only way to be symmetric —
what about all the other symmetries?

---

## The conjecture, in sixty seconds

Take a finite collection of finite sets with one rule: the union of any two
sets in the collection must also be in the collection ("union-closed"). In
1979 Péter Frankl conjectured:

> **In every union-closed family (with at least one nonempty set), some
> element belongs to at least half of the sets.**

Easy to state to a child, open for over forty-five years. The best general
result (Gilmer 2022 and successors) guarantees an element in ≈ 38.2% of the
sets — not 50%. Exhaustive search has verified the conjecture on universes of
up to 12 points; **13 and 14 points are the frontier**, and the number of
union-closed families there is beyond astronomical. The full story, with
references and worked examples, is in the
[predecessor's README](https://github.com/simone-albanese/frankl-cyclic-sat#readme).

## What "symmetric" means here — and why 14 is the interesting number

A **transitive permutation group** is a set of shuffles of the points, closed
under composition, with the property that any point can be carried to any
other point — no point is special. If a family of sets is invariant under such
a group ("shuffling the points maps the family to itself"), then every element
automatically has the same frequency, and the conjecture reduces to one clean
integer inequality. This is why symmetric families are simultaneously the most
promising hunting ground for a counterexample (a counterexample needs *every*
element to be rare — symmetry gives that wholesale) and a world small enough
to search *completely*.

The predecessor project settled the case of **rotations** (the cyclic group):
no rotation-invariant counterexample exists on 13 or 14 points, with verified
DRAT certificates. On 13 points that was automatically the end of the whole
transitive story: 13 is prime, and a classical theorem of Cauchy forces every
transitive group on a prime number of points to contain a full 13-cycle — so
every transitive symmetry contains rotation, and the cyclic result covers it.

**On 14 points this shortcut disappears.** 14 is not prime, and there are
transitive groups containing no 14-cycle at all — for instance the dihedral
group $D_7$ (the symmetries of a heptagon) acting on its own 14 elements, or
the simple group $\mathrm{PSL}(2,13)$ acting on the 14 points of the
projective line over $\mathbb{F}_{13}$. Families invariant under those
symmetries were untouched by the cyclic result. They are exactly what this
campaign decides.

## The strategy: prove lemmas until only five computations remain

There are **63 transitive groups on 14 points** up to relabeling (census built
from the standard classification, generators cross-checked against the LMFDB:
[STATE/census14.json](STATE/census14.json)). Deciding 63 separate SAT
instances would be wasteful — and the biggest groups give the *smallest*
search spaces, not the biggest, so brute force is not even the danger here;
wasted certification effort is. Three short lemmas
([docs/notes-minimality.md](docs/notes-minimality.md), with proofs) collapse
the problem:

1. **Invariance descends.** If a family is invariant under a group $G$, it is
   invariant under every subgroup of $G$. So an impossibility result for a
   *small* group instantly covers every larger group containing it.
2. **Full cycles are already done.** 37 of the 63 groups contain a 14-cycle —
   they contain the rotation group, and the predecessor's certified Z14 result
   covers them with no new computation.
3. **The cycle-free groups funnel into minimal ones.** Each of the remaining
   26 groups contains a *minimal* transitive subgroup (one with no smaller
   transitive group inside), which is again cycle-free. A computation whose
   exhaustiveness is itself certified
   ([results/minimality_scan.json](results/minimality_scan.json)) shows that,
   up to relabeling, only **five** groups need to be decided: 14T2 (the
   regular $D_7$, order 14), 14T6 (order 56), 14T10 (order 168), 14T12 (order
   196 — not certified minimal, included conservatively: deciding it directly
   was cheaper than classifying it, and its impossibility covers its
   supergroups anyway), and 14T30 ($\mathrm{PSL}(2,13)$, order 1092).

Five instances instead of infinitely many symmetry constraints. Each was then
decided **UNSAT** — no counterexample family exists — for families with member
sets of size ≥ 3, which is all a counterexample could use (a classical result
of Sarvate–Renaud: a counterexample contains no set of size 1 or 2; families
of size ≤ 2 conform trivially).

## The theorem

> **Theorem (degree 14).** Every non-trivial union-closed family
> $F \subseteq \mathcal{P}([14])$ invariant under any transitive permutation
> group $G \le S_{14}$ satisfies Frankl's conjecture: some element belongs to
> at least half of the sets of $F$.

The full statement, the proof chain and the validation protocol are in
[docs/theorem-degree14.md](docs/theorem-degree14.md); the theorem record with
every measured number and re-verification commands is in
[results/FOUND.md](results/FOUND.md).

> **Theorem (degree 15, added 14 Aug 2026).** Every non-trivial union-closed
> family $F \subseteq \mathcal{P}([15])$ invariant under any transitive
> permutation group $G \le S_{15}$ satisfies Frankl's conjecture.

Degree 15 fell in two acts on the same day. First the anchor: the cyclic case
Z15 — the predecessor's open problem 1, stopped at its 16 GB verification
wall — was closed by rerunning CaDiCaL with **streaming-verifiable LRAT**
output: UNSAT in 20 h 26 m, a 147 GB certificate verified in 22.6 minutes
([results/Z15-CLOSED.md](results/Z15-CLOSED.md); certificate archived at
[doi:10.5281/zenodo.21939129](https://doi.org/10.5281/zenodo.21939129)). That
covers the 78 of 104 transitive groups of degree 15 containing a 15-cycle;
the 26 without reduce, by the minimality lemmas
([docs/notes-minimality-15.md](docs/notes-minimality-15.md)), to **three**
instances — 15T5 ($A_5$, 686 orbits), 15T9 ($[5^2]3$, 478) and 15T26
($[3^4]5$, 222) — all three decided UNSAT by CP-SAT + CaDiCaL with LRAT
certificates verified, in **2 minutes 26 seconds total**. Statement:
[docs/theorem-degree15.md](docs/theorem-degree15.md); record:
[results/DEGREE15-CLOSED.md](results/DEGREE15-CLOSED.md); certificates in
[release v1.1.0](https://github.com/simone-albanese/frankl-transitive-sat/releases/tag/v1.1.0)
and archived at
[doi:10.5281/zenodo.21943855](https://doi.org/10.5281/zenodo.21943855). The degree-15
certificates (and the six from the margin-0 characterization) were
additionally re-verified by **cake_lpr**, a checker whose correctness is a
machine-checked theorem
([results/cakelpr-verification.md](results/cakelpr-verification.md)).

## The numbers

Every instance was decided by **two independent exact methods**: Google's
CP-SAT with a native integer margin constraint, and the CaDiCaL SAT solver on
an independently generated CNF encoding, whose refutation is a **DRAT proof
certificate verified by the independent checker drat-trim** — `s VERIFIED` on
all five. Machine: MacBook, Apple M4, 16 GB RAM.

| instance | group | order | orbit variables | CNF clauses | CP-SAT | CaDiCaL | DRAT certificate | drat-trim |
|---|---|---|---|---|---|---|---|---|
| 14T2 | $D_{14}(14) = [7]2$ (regular $D_7$) | 14 | 1,234 | 7,098,740 | INFEASIBLE, 74 s | UNSAT, ~55 min | 3.3 GB | **VERIFIED**, 2,940 s |
| 14T6 | $[2^3]7$ | 56 | 422 | 1,137,222 | INFEASIBLE, 7.5 s | UNSAT | 13 MB | **VERIFIED**, 4.0 s |
| 14T10 | $L_7(14)$ | 168 | 154 | 159,203 | INFEASIBLE, 0.6 s | UNSAT | 0.4 MB | **VERIFIED**, 0.12 s |
| 14T12 | $\tfrac12[D(7)^2]2$ | 196 | 170 | 146,706 | INFEASIBLE, 0.6 s | UNSAT | 1.0 MB | **VERIFIED**, 0.21 s |
| 14T30 | $L(14) = \mathrm{PSL}(2,13)$ | 1092 | 50 | 10,134 | INFEASIBLE, 0.1 s | UNSAT | 26 KB | **VERIFIED**, 0.06 s |

Note the shape of the table: the *smallest* group is the hardest instance. The
fewer symmetries you impose, the more freedom a would-be counterexample has,
and the more work the solver must do — $D_7$ regular, with only 14 shuffles,
generates a 3.3 GB certificate, while the 1092-element
$\mathrm{PSL}(2,13)$ falls in a tenth of a second. Unlike the predecessor's
Z15 attempt, every certificate here verifies comfortably on a laptop (peak
checker memory ≈ 2 GB).

## How the results are protected against error

The protocol is inherited from the predecessor, and it is paranoid by design:

1. **Two independent encodings, two independent solvers**, per instance. A bug
   would have to occur twice, in different formalisms, with identical effect.
2. **Proof certificates.** You do not have to trust CaDiCaL — only the
   independent checker [drat-trim](https://github.com/marijnheule/drat-trim)
   and the short formula generator.
3. **The generalized pipeline was validated before being believed.** Run on
   cyclic groups, the new group encoder must reproduce the *published,
   certified* cyclic pipeline — and it does, byte-identically at the DIMACS
   level on the control instances, and verdict-identically on Z13 and Z14
   (logs: `results/logs/t7_validate.log`, `t4_z13.log`, `t4_z14min3.log`).
4. **The reduction itself is certified.** The minimality scan does not sample:
   it exhaustively applies a criterion (proved in
   [docs/notes-minimality.md](docs/notes-minimality.md)) that certifies a
   group minimal, and any group it cannot certify is included in the instance
   list conservatively (that is what 14T12 is doing there).
5. **Integer-only verdicts.** All margin arithmetic is exact integer
   arithmetic; no floating point touches any verdict.

## Certificates and artifacts

The five CNF instances and five verified DRAT certificates (3.45 GB raw,
~585 MB xz-compressed, SHA-256 anchored in
[results/SHA256SUMS-certificates.txt](results/SHA256SUMS-certificates.txt))
are published in the
[v1.0.0 release](https://github.com/simone-albanese/frankl-transitive-sat/releases/tag/v1.0.0)
and permanently archived at Zenodo:
[doi:10.5281/zenodo.21920980](https://doi.org/10.5281/zenodo.21920980).
Verifying them needs no solver and no trust in this repository:
`unxz`, check the hashes, run `drat-trim instance.cnf instance.drat`, expect
`s VERIFIED`.

## Try it in five minutes

```bash
git clone <this-repository> && cd <this-repository>
python3 -m venv .venv && .venv/bin/python3 -m pip install -r requirements.txt

# 1. The inherited control gauntlet: exact checkers agree on everything known
.venv/bin/python3 controls.py

# 2. Decide the PSL(2,13) instance yourself (~0.1 s)
.venv/bin/python3 sat_group.py 14T30 decide 120 3

# 3. Decide the hardest of the five, the regular D7 (~1-2 min)
.venv/bin/python3 sat_group.py 14T2 decide 1200 3
```

`INFEASIBLE` means: no symmetric counterexample of that kind exists. To
reproduce the full certification chain (CNF export, CaDiCaL, drat-trim), see
[results/FOUND.md](results/FOUND.md) and the predecessor's
[reproducing guide](https://github.com/simone-albanese/frankl-cyclic-sat/blob/main/docs/reproducing.md)
for building the solver toolchain.

## The repository, mapped

| path | what it is |
|---|---|
| [docs/theorem-degree14.md](docs/theorem-degree14.md) | the theorem: statement, proof chain, validation |
| [docs/notes-minimality.md](docs/notes-minimality.md) | the lemmas and the certified minimality criterion, with proofs |
| [docs/playbook.md](docs/playbook.md) | the reusable field guide inherited from the predecessor |
| [STATE/census14.json](STATE/census14.json) | the census: all 63 transitive groups of degree 14, generators and cycle-type flags |
| [results/FOUND.md](results/FOUND.md) | the theorem record: exact numbers, logs, re-verification commands |
| [results/minimality_scan.json](results/minimality_scan.json) | the certified minimality scan |
| [group_orbits.py](group_orbits.py) | orbits of subsets under an arbitrary permutation group |
| [sat_group.py](sat_group.py) | CP-SAT exact decision for any transitive group (method no. 1) |
| [dump_dimacs_group.py](dump_dimacs_group.py) | DIMACS export for the certification chain (method no. 2) |
| [scripts/census14_build.py](scripts/census14_build.py), [scripts/minimality_scan.py](scripts/minimality_scan.py) | census construction and minimality certification |
| [pb_adder.py](pb_adder.py), [controls.py](controls.py), [checker2.py](checker2.py), … | the inherited, already-validated cyclic pipeline, used as controls |
| [scripts/loop.sh](scripts/loop.sh), [scripts/watchdog.sh](scripts/watchdog.sh) | the autonomous agent driver and its resource watchdog |
| [STATE/](STATE/), [CLAUDE.md](CLAUDE.md), [GOAL.md](GOAL.md) | working diary, agent constitution, goal definition (Italian) — primary sources |

## What's next

Degree 15 closed on 14 August 2026 — anchor (Z15) and superstructure (the
three minimal groups) in a single day; see the theorem section above. **This
project's own campaign ends here, by its owner's decision: the results from
13 to 15 points are complete, certified and archived.** What remains open is
left, honestly costed, to anyone who wants it:

- **Degree 16** is the next rung, and it is steep: the cyclic anchor Z16 is
  estimated at weeks-to-months of solver time and ~314 GB of certificate on
  this class of hardware, and the census holds 1,954 transitive groups. The
  predecessor's rule applies: probe before promising.
- **One certificate short of a perfect formal record**: cake_lpr re-verified
  9 of the project's 10 LRAT certificates; the 147 GB Z15 proof exhausted its
  12 GB verified heap at ~85% (a resource limit of the checker, not a verdict
  — Z15 remains lrat-check-verified). A 64 GB machine would finish the job;
  routes in [results/cakelpr-verification.md](results/cakelpr-verification.md).

Exploratory work continues and is recorded, as always, in the working diary
([STATE/](STATE/)) before it is polished into documentation.

## How this was made

Two working modes, both built on
**[Claude Code](https://claude.com/claude-code)** (model pinned to Claude
Fable 5), under the same constitution, resource budgets and
independent-verification protocol as the predecessor (described in detail in
its
[docs/ai-workflow.md](https://github.com/simone-albanese/frankl-cyclic-sat/blob/main/docs/ai-workflow.md)):

- **The degree-14 campaign (12 Aug) ran as an autonomous loop**: census,
  lemmas, pipeline generalization, validation, five decisions, theorem
  write-up — **18 short fresh-context sessions in about two and a half
  hours** of wall-clock time, with the human owner choosing the target and
  supervising.
- **Everything after (13–15 Aug) ran as interactive sessions**: the human
  owner decided at the forks (which route to attempt on Z15, when to stop a
  run, what to publish) and the agent executed — probing decompositions,
  building and validating the LRAT/PB toolchain, launching the detached
  20-hour Route B run that closed Z15 (designed to survive session
  restarts, with watchdogs and automatic verification), closing degree 15,
  re-verifying certificates with cake_lpr, and handling translation,
  archival and publication. At one point two Claude Code sessions worked
  the repository in parallel, coordinating through messages and the shared
  state files.

The raw diary of both modes is preserved verbatim in
[STATE/journal.md](STATE/journal.md) (Italian).

## Contributing

Most valuable right now: **literature pointers** — we believe the multi-orbit
transitive-invariant case decided here is not in the published literature (the
closest work, Aaronson–Ellis–Leader 2021, covers families generated by the
translates of a single set in an abelian group), and we would be glad to be
corrected. Also welcome: independent re-runs of the certificates, bug reports
in the encodings, and ideas for the degree-15 rung. Open an issue; measured
numbers beat opinions.

## License and citation

MIT for everything (code, encodings, documentation). If you build on this,
cite via [CITATION.cff](CITATION.cff).

## References

- J. Aaronson, D. Ellis, I. Leader, *Union-closed families generated by the
  translates of a fixed set in an abelian group* (2021) — the 1-orbit
  transitive case.
- J. H. Conway, A. Hulpke, J. McKay, *On transitive permutation groups*, LMS
  J. Comput. Math. 1 (1998) — the classification and the nTk labels used
  here; group data cross-checked against the [LMFDB](https://www.lmfdb.org/).
- D. G. Sarvate, J.-C. Renaud — a counterexample contains no set of size 1
  or 2.
- A. Biere et al., *CaDiCaL* SAT solver; M. Heule, *drat-trim* proof checker.
- For the conjecture's history and the 2022 breakthrough bounds, see the
  reference list of the
  [predecessor repository](https://github.com/simone-albanese/frankl-cyclic-sat#references).

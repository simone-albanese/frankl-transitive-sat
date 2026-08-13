# Frankl's Conjecture Beyond Cyclic Symmetry

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21920980.svg)](https://doi.org/10.5281/zenodo.21920980)

**Work in progress — campaign started 12 August 2026. Degree 14 is closed
and certified (see below).**

Goal: decide whether any union-closed family invariant under **any transitive
permutation group** on 14 (then 15, 16) points violates Frankl's union-closed
sets conjecture. On 13 points this is settled: every transitive group on a
prime number of points contains a full cycle (Cauchy), so the certified cyclic
result of the predecessor project covers everything. On 14+ points transitive
groups *without* a full cycle exist — for instance the regular action of the
dihedral group $D_7$, or $\mathrm{PSL}(2,13)$ on the projective line — and
they are exactly what this campaign decides, via the reduction to *minimal*
transitive cycle-free groups.

- **Degree-14 theorem** (no union-closed family invariant under any
  transitive group on 14 points violates the conjecture):
  [docs/theorem-degree14.md](docs/theorem-degree14.md) ·
  [results/FOUND.md](results/FOUND.md). Proof artifacts (CNF instances +
  drat-trim–verified DRAT certificates for the five minimal instances) are in
  the [v1.0.0 release](https://github.com/simone-albanese/frankl-transitive-sat/releases/tag/v1.0.0)
  and permanently archived at Zenodo:
  [doi:10.5281/zenodo.21920980](https://doi.org/10.5281/zenodo.21920980).
- Predecessor (methods, certified Z13/Z14 results, proof artifacts):
  [frankl-cyclic-sat](https://github.com/simone-albanese/frankl-cyclic-sat) ·
  artifacts DOI [10.5281/zenodo.21900943](https://doi.org/10.5281/zenodo.21900943)
- Method: [docs/playbook.md](docs/playbook.md) — the field guide distilled
  from the previous campaign (problem selection, resource walls, trust
  architecture, operational traps).
- The research is executed by an autonomous Claude Code agent loop; the live
  diary and task ledger are in [STATE/](STATE/) (Italian), the constitution in
  [CLAUDE.md](CLAUDE.md).

Status: **degree 14 closed and certified** (12 August 2026). The campaign
completed the census of the 63 transitive groups of degree 14 (26 contain no
14-cycle), reduced the theorem to five minimal cycle-free instances, and
decided all five UNSAT with two independent methods (OR-Tools CP-SAT, and
CaDiCaL with DRAT certificates verified by drat-trim — `s VERIFIED` on all
five). Certificates: [v1.0.0 release](https://github.com/simone-albanese/frankl-transitive-sat/releases/tag/v1.0.0)
· [doi:10.5281/zenodo.21920980](https://doi.org/10.5281/zenodo.21920980).
Degrees 15 and 16 are in the backlog and not yet started; degree 15 interacts
with the still-open cyclic case Z15 (open problem 1 of the predecessor
repository).

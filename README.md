# Frankl's Conjecture Beyond Cyclic Symmetry

**Work in progress — campaign started 12 August 2026.**

Goal: decide whether any union-closed family invariant under **any transitive
permutation group** on 14 (then 15, 16) points violates Frankl's union-closed
sets conjecture. On 13 points this is settled: every transitive group on a
prime number of points contains a full cycle (Cauchy), so the certified cyclic
result of the predecessor project covers everything. On 14+ points transitive
groups *without* a full cycle exist — for instance the regular action of the
dihedral group $D_7$, or $\mathrm{PSL}(2,13)$ on the projective line — and
they are exactly what this campaign decides, via the reduction to *minimal*
transitive cycle-free groups.

- Predecessor (methods, certified Z13/Z14 results, proof artifacts):
  [frankl-cyclic-sat](https://github.com/simone-albanese/frankl-cyclic-sat) ·
  artifacts DOI [10.5281/zenodo.21900943](https://doi.org/10.5281/zenodo.21900943)
- Method: [docs/playbook.md](docs/playbook.md) — the field guide distilled
  from the previous campaign (problem selection, resource walls, trust
  architecture, operational traps).
- The research is executed by an autonomous Claude Code agent loop; the live
  diary and task ledger are in [STATE/](STATE/) (Italian), the constitution in
  [CLAUDE.md](CLAUDE.md).

Status: bootstrap — group census and reduction lemma in progress. Everything
here is provisional until it passes the project's two-independent-methods
standard; full English documentation will follow the first decided rung, as in
the predecessor repository.

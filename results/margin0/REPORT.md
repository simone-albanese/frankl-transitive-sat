# Esperimento "margine 0" — caratterizzazione delle famiglie estremali cicliche

Data: 2026-08-13 · Status: COMPLETO allo standard del progetto
(due metodi esatti indipendenti + certificato LRAT verificato per ogni
esito negativo).

## Origine

Nato da un pattern osservato nei dati della campagna ciclica: l'insieme
delle parti tocca esattamente la soglia della congettura di Frankl
(margine intero 2·maxfreq − |F| = 0). Domanda: è l'unico a farlo?

## Risultato

**Proposizione (m ∈ {7, 11, 13}).** Sia F una famiglia union-closed
Z_m-invariante con ∅, [m] ∈ F e almeno un'orbita non banale inclusa.
Allora:

1. **(Unicità dell'estremale)** Se il margine di F è ≤ 0, allora
   F = P([m]) (l'insieme delle parti intero), e il margine è esattamente 0.
2. **(Gap nel mondo min-3)** Se inoltre ogni insieme non banale di F ha
   taglia ≥ 3, allora il margine di F è ≥ 1: nessuna famiglia tocca
   nemmeno la soglia.

In altre parole: sotto simmetria ciclica non solo non esistono
controesempi (margine ≤ −1, già certificato dalla campagna precedente),
ma l'unico modo di *toccare* la soglia è prendere tutto, e appena si
impone la taglia minima 3 si apre un gap di almeno 1.

## Metodo (doppio, con certificati)

Pipeline: `margin_zero.py` — riusa canon_table/build_orbits/build_clauses
di `sat_cyclic.py` (validata) e `pb_adder.py` per il DIMACS.
**Validazione preliminare superata**: con rhs=−1 riproduce INFEASIBLE
sui controlli certificati Z7 e Z11.

Esperimenti per ogni m ∈ {7, 11, 13}:

| Esperimento | Vincoli | CP-SAT (met. 1) | cadical (met. 2) | lrat-check |
|---|---|---|---|---|
| E1a sanity | margine ≤ 0 | FEASIBLE: parti, margine 0 | — (testimone) | — |
| E1b unicità | margine ≤ 0, ≠ parti | **INFEASIBLE** ×3 | **UNSAT** (exit 20) ×3 | **VERIFIED** ×3 |
| E2 min-3 | margine ≤ 0, taglie ≥ 3 | **INFEASIBLE** ×3 | **UNSAT** (exit 20) ×3 | **VERIFIED** ×3 |

Il testimone E1a (insieme delle parti: |F| = 2^m, margine 0) è stato
verificato per ciascun m da ENTRAMBI i checker indipendenti
(`ucs_core.check_family` + `checker2.verify`), aritmetica su interi.

Tempi CP-SAT [M]: Z7 e Z11 < 1 s; Z13 ~16–19 s per esperimento.
Certificati LRAT: da 5 KB (Z7) a 561 MB (Z13-E1b).

## Artefatti e riverifica

CNF e certificati in questa cartella; impronte in `SHA256SUMS.txt`.
Encoding: margine scalato Σ r_O(2s_O−m)x_O ≤ 0 (interi; ∅ e [m]
si cancellano), non-vuotezza Σx ≥ 1, "≠ parti" = clausola ∨¬x_O.

```bash
# metodo 1 (CP-SAT), tutti e tre gli esperimenti per m dato:
$PY margin_zero.py validate      # prima: deve dire [OK]
$PY margin_zero.py run 13 900

# metodo 2 + certificato (esempio Z13-E1b):
tools/cadical/build/cadical --lrat --no-binary \
    results/margin0/z13_E1b.cnf results/margin0/z13_E1b.lrat   # exit 20
tools/drat-trim/lrat-check results/margin0/z13_E1b.cnf \
    results/margin0/z13_E1b.lrat        # cercare "c VERIFIED" nell'output
```

Trappola nota: cadical scrive LRAT **binario** di default e lrat-check
testuale risponde "NOT VERIFIED" — usare sempre `--no-binary` (o il
lrat-trim in tools/ che legge entrambi). Mai fidarsi del solo exit code.

## Cosa NON copre

- m composti (14, 15): non ancora eseguito (fattibile: ~1 min CP-SAT per
  Z14; Z15 al costo di un decide monolitico).
- Gruppi transitivi non ciclici: la riformulazione "margine = m·(taglia
  media − m/2)·|F|/… " vale per ogni transitivo; esperimento analogo
  possibile con la pipeline group-agnostica (sat_group.py).
- Nessuna implicazione diretta sulla congettura generale: è una
  caratterizzazione del caso estremale simmetrico.

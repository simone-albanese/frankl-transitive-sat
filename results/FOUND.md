# FOUND — Teorema di grado 14 (risultato negativo di valore)

Data: 2026-08-12 · Status: SUCCESS secondo GOAL.md ("risultato negativo di
valore, grado 14"), verificato con metodo indipendente (CP-SAT + DRAT).

## Enunciato

**Teorema.** Ogni famiglia union-closed non banale F ⊆ P([14]) invariante
sotto un QUALSIASI gruppo di permutazioni transitivo G ≤ S14 soddisfa la
congettura di Frankl: esiste un elemento contenuto in almeno metà degli
insiemi di F (in interi: 2·maxfreq ≥ |F|; nessuna famiglia con margine
2·maxfreq − |F| ≤ −1 esiste).

Questo estende oltre i gradi primi il corollario che su 13 punti seguiva da
Cauchy (caso ciclico Z13/Z14 già chiuso nel repo `frankl-cyclic-sat`,
DOI 10.5281/zenodo.21900943, con certificati DRAT).

## Catena logica

1. **Discesa dell'invarianza** (Lemma 1, `docs/notes-minimality.md`):
   F G-invariante ⟹ F H-invariante per ogni H ≤ G. Quindi un UNSAT su un
   sottogruppo transitivo H implica UNSAT su ogni sovragruppo G ≥ H.
2. **Riduzione ai minimali** (`docs/notes-minimality.md`,
   `results/minimality_scan.json`): ogni transitivo G di grado 14 contiene
   un transitivo minimale M. Due casi:
   - G contiene un 14-ciclo ⟹ G ⊇ Z14, caso chiuso dal repo ciclico
     (Z14 UNSAT taglie ≥ 3, certificato DRAT, DOI sopra);
   - G senza 14-ciclo ⟹ M è senza 14-ciclo (Lemma 2) e, a meno di
     coniugio in S14, M è uno dei 5 gruppi della lista sotto
     (scan certificato: 14T2/6/10/30 minimali certificati; 14T12 incluso
     conservativamente come UNKNOWN — deciderlo via SAT costa meno che
     classificarlo, e un UNSAT su di lui copre comunque i suoi sovragruppi).
   La coniugazione in S14 non cambia l'esito (rilabeling dei punti).
3. **I 5 gruppi sono tutti UNSAT** per famiglie di taglia ≥ 3 (riduzione
   Sarvate–Renaud: le taglie ≤ 2 sono banalmente conformi), con DOPPIA
   verifica indipendente: CP-SAT (OR-Tools, T6) e cadical con certificato
   DRAT verificato da drat-trim (T7).

## Tabella dei 5 gruppi-istanza

| Gruppo | Nome            | Ordine | Orbite non banali | Clausole  | CP-SAT (T6)        | cadical (T7) | drat-trim (T7)            |
|--------|-----------------|--------|-------------------|-----------|--------------------|--------------|---------------------------|
| 14T2   | D_14(14)=[7]2   | 14     | 1234              | 7 098 740 | INFEASIBLE, 74,0 s | UNSAT (exit 20) | s VERIFIED, 2939,8 s   |
| 14T6   | [2^3]7          | 56     | 422               | 1 137 222 | INFEASIBLE, 7,5 s  | UNSAT (exit 20) | s VERIFIED, 4,0 s      |
| 14T10  | L_7(14)         | 168    | 154               | 159 203   | INFEASIBLE, 0,6 s  | UNSAT (exit 20) | s VERIFIED, 0,12 s     |
| 14T12  | 1/2[D(7)^2]2    | 196    | 170               | 146 706   | INFEASIBLE, 0,6 s  | UNSAT (exit 20) | s VERIFIED, 0,21 s     |
| 14T30  | L(14)=PSL(2,13) | 1092   | 50                | 10 134    | INFEASIBLE, 0,1 s  | UNSAT (exit 20) | s VERIFIED, 0,06 s     |

Fonti: `results/t6_decide.json`, `results/logs/t7_14T*.log`,
`STATE/census14.json` (63 transitivi di grado 14, 26 senza 14-ciclo),
`results/minimality_scan.json`.

## Come riverificare

I file CNF e i certificati DRAT sono in `results/cnf/` (ATTENZIONE:
`14T2.drat` pesa 3,3 GB — non aprirlo, solo darlo in pasto a drat-trim).

```bash
# 1. Riverifica dei certificati esistenti (nessun solver necessario):
#    exit code 0 e riga "s VERIFIED" = certificato valido.
drat-trim results/cnf/14T30.cnf results/cnf/14T30.drat   # ~0,1 s
drat-trim results/cnf/14T12.cnf results/cnf/14T12.drat   # ~0,2 s
drat-trim results/cnf/14T10.cnf results/cnf/14T10.drat   # ~0,1 s
drat-trim results/cnf/14T6.cnf  results/cnf/14T6.drat    # ~4 s
drat-trim results/cnf/14T2.cnf  results/cnf/14T2.drat    # ~50 min

# 2. Rigenerazione da zero dei CNF (encoder del repo) e nuovo run:
#    exit 20 = UNSAT (atteso). $PY = python del venv (STATE/hardware.env).
$PY dump_dimacs_group.py <gruppo> 3 results/cnf/<gruppo>.cnf
cadical results/cnf/<gruppo>.cnf results/cnf/<gruppo>.drat  # exit 20

# 3. Controllo indipendente CP-SAT:
$PY sat_group.py <gruppo> decide 1200 3        # atteso: INFEASIBLE

# 4. Sanity dei tool (pipeline validata sui controlli PRIMA della produzione):
#    Z7 e Z11 INFEASIBLE, DIMACS byte-identici a quelli del repo ciclico
#    (results/logs/t7_validate.log, results/logs/t5_probe.log).
```

Avvertenze note: i WARNING "duplicate literal" di drat-trim sono benigni;
l'aritmetica dei verdetti è tutta su interi (margine = 2·maxfreq − |F|).

## Cosa NON copre questo risultato

- Gradi 15 e 16: nel backlog (T9+), non ancora iniziati.
- Gruppi NON transitivi: fuori scope di GOAL.md.

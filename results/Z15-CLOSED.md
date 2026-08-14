# Z15 — CHIUSO: UNSAT con certificato verificato (2026-08-14)

**Teorema.** Nessuna famiglia union-closed non banale F ⊆ P([15]) invariante
per rotazione (Z15), con insiemi non banali di taglia ≥ 3 (riduzione
Sarvate–Renaud), viola la congettura di Frankl: il margine intero
2·maxfreq − |F| è sempre ≥ 0.

Questo chiude l'**open problem 1** del repo `frankl-cyclic-sat`
(DOI 10.5281/zenodo.21900943), rimasto aperto il 2026-08-12 quando il run
fu fermato per il muro di RAM della verifica DRAT (11–18 GB stimati contro
16 fisici). Il muro è stato dissolto passando al formato LRAT verificabile
in streaming.

## Standard di prova raggiunto (supera il criterio del progetto)

1. **Metodo 1 — CP-SAT (OR-Tools 9.15.6755)**, modello nativo (margine come
   vincolo lineare intero, 2.190 variabili di orbita): INFEASIBLE in 889 s
   (T9a, 2026-08-11; log nel repo ciclico).
2. **Metodo 2 — CaDiCaL 3.0.1**, CNF congelata indipendente
   (`results/cnf/z15min3.cnf`, encoding a sommatore binario, 16.856
   variabili / 28.850.111 clausole, sha256
   `e6c732cf30bc619dd4c2706734bdcc2ed99255a422c52c4a8525563785115120`,
   byte-identica alla formula pubblicata): **exit 20 = UNSAT** in
   73.544,58 s (20h26m), max RSS 4.793,61 MB, 2026-08-14 18:57:39.
3. **Certificato — prova LRAT testuale** di 158.233.546.333 byte (147 GB),
   `results/cnf/z15.lrat`, sha256 in `results/cnf/z15.lrat.sha256`.
   Verificata da `lrat-check` (repo drat-trim): **"c VERIFIED"** in
   1.358,68 s (22,6 min), 145.241.055 clausole aggiunte / 130.164.827
   cancellate, max live clauses 28.850.111 — la verifica in streaming usa
   RAM proporzionale alla formula, non alla prova.

I due metodi condividono solo il generatore di orbite/chiusura (validato
sui controlli Z7/Z11/P([4]) e, a valle, coperto dal certificato); vincolo
di margine, encoding e motori sono indipendenti.

## Esecuzione (Route B)

- Driver: `scripts/routeB.sh`, lancio sganciato 2026-08-13 22:31:17,
  nessun cap di tempo, guardia RAM 9 GB / disco 30 GB, heartbeat orario in
  `results/logs/routeB_driver.log` (traiettoria completa conservata).
- Crescita prova: ~6–8 GB/h costante. Variabili residue: 51% a 10h, 50%
  fino a ~17h, 49% a 17h, 48% alle 18:30 — **crollo a verdetto in ~27
  minuti** (pattern identico a Z14: le confutazioni CDCL finiscono senza
  preavviso).
- Log solver: `results/logs/routeB_z15.log`; verifica:
  `results/logs/routeB_lratcheck.log`.

## Come riverificare

```bash
# 1. Rigenerare la formula (deterministica) e controllare l'impronta:
$PY dump_dimacs.py 15 z15min3.cnf 3
shasum -a 256 z15min3.cnf   # atteso: e6c732cf...

# 2. Verificare il certificato (streaming, ~23 min, RAM ~1-2 GB):
tools/drat-trim/lrat-check results/cnf/z15min3.cnf results/cnf/z15.lrat
# cercare la riga "c VERIFIED" nell'output (mai fidarsi del solo exit code)

# 3. Conferma indipendente senza certificato (15 min circa):
$PY sat_cyclic.py ... # modello CP-SAT nativo, atteso INFEASIBLE
```

## Conseguenze e prossimi passi

- Il corollario ciclico ora copre m ∈ {13, 14, 15} con certificato.
- **Via libera al teorema di grado 15 transitivo** (T9): census dei gruppi
  transitivi di grado 15 senza 15-ciclo + questo risultato ⇒ "nessuna
  famiglia union-closed invariante per un gruppo transitivo su 15 punti
  viola la congettura" — non più condizionale.
- Da fare: archiviazione del certificato (xz), nuova versione Zenodo del
  repo ciclico, aggiornamento di `docs/open-problems.md` (problema 1 →
  risolto), commit di questo verbale.

**NON cancellare `results/cnf/z15.lrat`**: è il certificato. (147 GB;
comprimerlo con xz richiederà ore ma dovrebbe scendere sotto i 30 GB.)

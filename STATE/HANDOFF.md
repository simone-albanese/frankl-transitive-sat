# HANDOFF — 2026-08-12 (pomeriggio) · STATUS: DONE

**Obiettivo (una riga):** decidere se esistono famiglie union-closed
invarianti sotto un gruppo transitivo di grado 14 (poi 15, 16) senza
14-ciclo che violino la congettura di Frankl.

**Dove siamo: OBIETTIVO GRADO 14 RAGGIUNTO.** T1–T8 completati.
Il teorema è scritto in `results/FOUND.md` (enunciato, catena logica,
tabella dei 5 gruppi, comandi di riverifica) e in inglese in
`docs/theorem-degree14.md`. `STATE/status.txt` = DONE: il loop si ferma.

**Esito di questa iterazione (T8):** scritti FOUND.md e la nota inglese;
tutti i numeri presi da results/t6_decide.json e da grep sui log
results/logs/t7_14T*.log (5/5 "s VERIFIED"; 14T2: DRAT_EXIT=0,
verification 2939,8 s). status DONE, SITUAZIONE/html su 🟢, notifica
inviata, backlog spuntato, commit + push su origin.

## PROSSIMO TASK ESATTO (solo se l'umano riparte): T9 — grado 15
1. L'umano deve prima decidere (vedi SITUAZIONE.md): proseguire con 15 o
   fermarsi. Per proseguire: `echo RUN > STATE/status.txt` poi
   `bash scripts/loop.sh`.
2. T9 inizia col census: LMFDB
   `https://www.lmfdb.org/api/gps_transitive/?degree=15&_format=json`
   (stesso schema di scripts/census14_build.py — adattarlo, NON riscrivere).
   Filtro sul cycle type (15), MAI sull'ordine. Nota: 15 = 3·5, Z15 era
   INFEASIBLE per CP-SAT ma NON certificato nel repo ciclico — a grado 15
   il caso ciclico andrà certificato DRAT qui (aggiungere task).
3. Poi replica della catena T2→T7 con gli stessi script generalizzati
   (group_orbits.py, sat_group.py, dump_dimacs_group.py: già group-agnostici).

## Run attivi in background
Nessuno.

## Trappole note
- `python3` nudo SBAGLIATO: usare `$PY` da STATE/hardware.env — e nei
  sotto-shell (`bash -c`) va **esportato** (`export PY`).
- La cwd di Bash PERSISTE tra chiamate: path assoluti nei `cd`.
- results/cnf/14T2.{cnf,drat} pesano 115 MB / 3,3 GB: MAI leggerli. Sono
  ESCLUSI dal commit (troppo grandi per GitHub): restano solo su disco
  locale — non cancellarli, sono i certificati.
- cadical exit 20 = UNSAT (atteso); WARNING "duplicate literal" benigni.
- In zsh `echo ===` fallisce: separatori diversi.
- Aritmetica dei verdetti solo su interi (margine = 2·maxfreq − |F|).
- A grado 15 il filtro è sul cycle type (15); un elemento di ordine 15
  può essere (3,5,1^7).

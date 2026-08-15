# HANDOFF — 2026-08-14 sera · STATUS: DONE (grado 14 E grado 15)

**Obiettivo (una riga):** decidere se esistono famiglie union-closed
invarianti sotto un gruppo transitivo di grado 14 (poi 15, 16) senza
ciclo lungo che violino la congettura di Frankl.

**Dove siamo: GRADO 14 E GRADO 15 ENTRAMBI CHIUSI E CERTIFICATI.**
- Grado 14: T1–T8 (2026-08-12), `results/FOUND.md`,
  `docs/theorem-degree14.md`, pubblicato (release v1.0.0 + Zenodo).
- Z15 ciclico: chiuso 2026-08-14 19:20, `results/Z15-CLOSED.md`
  (LRAT 147 GB verificato; xz in corso, vedi sotto).
- **Grado 15: T9 chiuso 2026-08-14 20:53 in sessione interattiva.**
  Verbale `results/DEGREE15-CLOSED.md`; teorema `docs/theorem-degree15.md`;
  lemmi `docs/notes-minimality-15.md`; census `STATE/census15.json`
  (da `STATE/trans15.grp`, GAP/Hulpke); scan
  `results/minimality15_scan.json`. Tre istanze (15T5/15T9/15T26):
  CP-SAT INFEASIBLE + cadical UNSAT + lrat-check "c VERIFIED".

**Esito di questa sessione (interattiva, 14/08 sera):** vedi journal
20:53. Nuovi file NON ancora committati (decisione umana): scripts/
census15_build.py, minimality15_scan.py, t9_certify.sh; docs/
notes-minimality-15.md, theorem-degree15.md; results/DEGREE15-CLOSED.md,
minimality15_scan.json, cnf/15T*.{cnf,lrat} + SHA256-15T-*.txt,
logs/t9_*; STATE/trans15.grp, census15.json; modifica a group_orbits.py
(load_group sceglie il census dal prefisso dell'etichetta).

## PROSSIMO TASK ESATTO (solo se l'umano riparte): T9b — pubblicazione
1. Attendere fine xz di z15.lrat (log `results/logs/xz_z15.log`,
   notifica macOS a fine corsa; poi esiste z15.lrat.xz con sha nel log).
2. Commit dei file elencati sopra (messaggio suggerito: "Degree 15
   closed: transitive theorem with verified LRAT certificates").
   Push = decisione umana.
3. xz dei tre LRAT di grado 15 (221 MB → ~30-40 MB), release asset
   GitHub + eventuale nuova versione Zenodo (serve token dall'umano).
4. README.md: aggiornare stato (grado 15 chiuso). FOUND.md resta il
   record del grado 14; il grado 15 ha il suo verbale.

## Run attivi in background
NESSUNO (dalle 01:05 del 15/08).
- cake_lpr su z15.lrat (147 GB): TERMINATO 01:05 con **"CakeML heap
  space exhausted"** (heap 12 GB, ~80-85% del file [E]) — limite di
  RISORSE del checker verificato, NON un verdetto sul certificato,
  che resta VERIFICATO da lrat-check. Fabbisogno stimato 15-25 GB >
  16 GB fisici. Bilancio cake_lpr: **9/10 VERIFIED** (3 grado-15 +
  6 margin0, con collaudo e controlli negativi). Quattro strade per il
  10/10 in `results/cakelpr-verification.md` (consigliata: macchina
  64 GB — è la configurazione prevista dal Makefile di cake_lpr;
  alternativa senza cloud: modalità compositiva a intervalli).
- xz di z15.lrat: FINITO (z15.lrat.xz 19 GB, XZ_TEST_OK, sha256 nel
  log xz_z15.log). NON cancellare né z15.lrat né z15.lrat.xz.
- Paper: `paper/ucc-transitive-15.tex` + PDF (8 pagine, ricompilato
  01:15 con l'esito cake_lpr onesto in abstract e sezione dedicata).
  TODO residui nel sorgente: authorship, DOI Zenodo v2, ID arXiv di
  3-4 citazioni della linea Gilmer.

## Trappole note (aggiornate)
- `python3` nudo SBAGLIATO: usare `$PY` da STATE/hardware.env.
- Il 15-ciclo è PARI: mai riusare la scorciatoia di parità del census14
  fuori dai gradi pari; filtro sempre sul cycle type nell'azione giusta.
- LMFDB API dietro reCAPTCHA dal 14/08: fonte primaria = libreria GAP
  transgrp su GitHub (raw), con doppia verifica degli ordini.
- cadical: exit 20 = UNSAT (atteso); LRAT sempre con `--no-binary`;
  verdetto = riga "c VERIFIED" nel log, MAI il solo exit code.
- NON cancellare: results/cnf/z15.lrat (147 GB, certificato ciclico),
  results/cnf/15T*.lrat (certificati grado 15), 14T2.{cnf,drat} ecc.
- Aritmetica dei verdetti solo su interi (margine = 2·maxfreq − |F|).

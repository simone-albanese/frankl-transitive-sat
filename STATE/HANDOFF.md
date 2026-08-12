# HANDOFF — 2026-08-12 11:50 (bootstrap) · STATUS: RUN

**Obiettivo (una riga):** decidere se esistono famiglie union-closed invarianti
sotto un gruppo transitivo su 14 punti (poi 15, 16) che violino la congettura
di Frankl — i gruppi SENZA m-ciclo, ché il caso ciclico è già chiuso
(repo frankl-cyclic-sat: Z13/Z14 certificati, Z15 non confermato).

**Dove siamo:** bootstrap completato dalla sessione interattiva del 12/08:
kit copiato dal repo precedente (costituzione, driver, watchdog, checkers,
pb_adder, playbook, lezioni), GOAL.md nuovo, backlog T1–T10 caricato, venv
creato e controlli superati (vedi journal). Repo GitHub creato e pushato.

## PROSSIMO TASK ESATTO: T1 — census dei gruppi transitivi di grado 14

```bash
# strada A (preferita): GAP
brew install gap          # pesante (~min), una tantum
gap -q -c 'n:=NrTransitiveGroups(14);; Print(n,"\n");'   # atteso 63 (verificare)
# poi script GAP che esporta per ogni gruppo: generatori, ordine,
# has_14_cycle = esiste classe con cycle type [14] — vedi backlog T1.

# strada B (fallback senza GAP): LMFDB API
curl -s "https://www.lmfdb.org/api/gps_transitive/?degree=14&_format=json" | head -c 2000
```

Deliverable: `STATE/census14.json` + conteggi nel journal. Sanity: 14T1 = Z14
con ciclo; D7 regolare e PSL(2,13) senza.

## Run attivi in background
Nessuno.

## Trappole note (ereditate dal repo precedente + nuove)
- `python3` nudo è l'interprete SBAGLIATO: usare `.venv/bin/python3` (o `$PY`
  da `STATE/hardware.env`). Provare l'IMPORT, non la versione.
- **Cycle type, non ordine**: un elemento di ordine 14 può essere (2,7,1^5)
  e NON un 14-ciclo. Il filtro del census va sui cycle type.
- La pipeline generalizzata non ha valore finché non riproduce Z13/Z14
  certificati (T4) — nessun esito nuovo prima di quella validazione.
- I permessi del loop vivono nei flag di `scripts/loop.sh`, non nei settings.
- Log verbosi → `results/logs/`, in conversazione solo `tail`.
- Effort: `medium` di default; scrivere `high` in `STATE/effort.txt` PRIMA
  di T2 (progettazione/lemma).

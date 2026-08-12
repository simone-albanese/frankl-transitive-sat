# Journal — frankl-transitive (append-only)

## 2026-08-12 11:55 — BOOTSTRAP (sessione interattiva, con l'umano)
Campagna scelta dall'umano tra tre candidate verificate su letteratura
(ricerca web del 12/08): gruppi transitivi senza m-ciclo su 14→15→16 punti.
Verifiche di frontiera: solo Aaronson–Ellis–Leader 2021 (caso 1-orbita) in
letteratura; census transitivi ≤ 47 disponibile (GAP TransGrp); nessun lavoro
pubblicato sul caso multi-orbita transitivo oltre il ciclico.
- Kit copiato dal repo frankl-cyclic-sat (costituzione, driver+watchdog,
  ucs_core/checker2/controls/pb_adder + moduli ciclici come riferimento,
  playbook, lezioni). GOAL.md nuovo; backlog T1–T10 caricato.
- venv creato: ortools 9.15.6755, python-sat 1.9.dev13 (identiche ai run
  certificati del repo precedente).
- CONTROLLI SUPERATI in questa sessione: controls.py → "TUTTI I CONTROLLI
  SUPERATI"; sat_cyclic.py controls → Z7 e Z11 INFEASIBLE (teoremi noti
  riprodotti).
- Fatti matematici già fissati in GOAL/backlog: trappola cycle-type≠ordine
  (es. (2,7,1^5) ha ordine 14 ma non è un 14-ciclo); lemma di riduzione ai
  minimali senza ciclo (da scrivere in T2); stime Burnside: D7 regolare
  ~1300 orbite (≈ Z14, dentro l'inviluppo), gruppi grandi → poche orbite.
Prossimo: T1 (census grado 14) — comandi pronti in HANDOFF.

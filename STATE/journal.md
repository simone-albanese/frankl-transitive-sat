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

## 2026-08-12 ~12:30 — T1 census gruppi transitivi grado 14 — SUCCESS
- GAP non installabile via brew (nessuna formula "gap": log results/logs/brew-gap.log). Strada B: LMFDB API (campo `n=14`, non `degree`).
- 63 gruppi (come atteso), salvati grezzi in STATE/census14_lmfdb.json e decisi in STATE/census14.json con scripts/census14_build.py.
- has_14_cycle rigoroso: enumerazione esaustiva per ordine ≤2e6 (57 gruppi, con assert |enum|==ordine LMFDB = cross-check indipendente gens vs ordine); per i 6 grandi: parità (G≤A14 ⇒ nessun 14-ciclo, dispari) per 14T59 e A14, testimone esplicito verificato per gli altri 4.
- Esito: 37 con 14-ciclo, 26 SENZA: t ∈ {2,4,6,10,11,12,16,21,22,23,27,28,30,33,34,35,36,40,41,46,50,53,54,55,59,62}.
- Sanity OK: 14T1=C14 true; 14T2=D7 regolare false; 14T30=PSL(2,13) false.
- Prossimo: T2 (lemma minimalità + lista finale), effort HIGH già scritto in STATE/effort.txt.

## 2026-08-12 ~13:05 — T2: lemma di minimalità + lista finale — SUCCESS
Scritti docs/notes-minimality.md (lemmi 1-4 + criterio computazionale ⟨a_i,x⟩
+ teorema di copertura) e scripts/minimality_scan.py. Run completo in ~10s:
results/minimality_scan.json. Sanity riprodotti (D7=1236 orbite, PSL(2,13)=52,
entrambi confermati da calcolo a mano indipendente). Lista istanze finale:
14T2(1236 orb), 14T6(424), 14T10(156), 14T30(52) certificati minimali +
14T12(172, UNKNOWN conservativo). 14T46 risolto NOT_MINIMAL con esaustivo
mirato (testimone ordine 42). 20 gruppi con testimone esplicito di
non-minimalità; 14T59/14T62 via costruzione (basi in JSON, dipendono
dall'ordine LMFDB per 14T59). Prossimo: T3 (group_orbits.py), effort medium.

## 2026-08-12 ~14:00 — T3: pipeline generalizzata scritta e smoke-testata
Creati group_orbits.py (BFS orbite bitmask, canone=min, assert m|r·s),
sat_group.py (CP-SAT, margine scalato, chiusura rep-fisso con giustificazione
per G arbitrario nel docstring), dump_dimacs_group.py (pb_adder riusato).
Verifiche di questa sessione: 14T2 → 1234 orbite non banali (=1236−2 di T2),
14T30 → 50 (=52−2); Z7 decide INFEASIBLE; DIMACS Z7 e Z11 dalla pipeline
nuova BYTE-IDENTICI a quelli di dump_dimacs.py (cmp ok). Moduli ciclici intatti.
Prossimo: T4 — validazione piena su Z13 (630 orbite, 1.863.311 clausole,
INFEASIBLE) e Z14 min3 (1180 orbite, INFEASIBLE).

## 2026-08-12 ~14:40 — T4: validazione pipeline su Z13 e Z14
Z13 decide: 630 orbite non banali, 1.863.311 clausole, INFEASIBLE in 15,5s
(results/logs/t4_z13.log). Z14 decide min_size=3: 1180 orbite, 7.320.454
clausole, INFEASIBLE in 90,1s (results/logs/t4_z14min3.log). Entrambi i
numeri coincidono ESATTAMENTE con quelli pubblicati (frankl-cyclic-sat).
Pipeline generalizzata validata. Prossimo: T5 (sonda risorse istanze).

## 2026-08-12 ~15:xx — T5: sonda risorse gruppi-istanza
Aggiunto mode "probe" a sat_group.py (build-only, conteggi+RSS). Sanity Z13
riproduce esattamente T4 (630 orbite, 1.863.311 clausole). Sonde (mss=3):
14T30 50orb/10k cl/0.08GB · 14T10 154/159k/0.12 · 14T12 170/147k/0.12 ·
14T6 422/1.14M/0.36 · 14T2 1234/7.10M/1.78GB. Tutto entro budget (cap 9GB).
14T2 ~ Z14 (7.32M cl, solve 90s) ⇒ decide atteso in minuti, niente sharding.
→ results/t5_probe.json, results/logs/t5_probe.log. Prossimo: T6 decide.

## 2026-08-12 ~16:00 — T6: decide CP-SAT per le 5 istanze di grado 14 (mss=3)
Esito: TUTTE INFEASIBLE. 14T30 0,1s · 14T10 0,6s · 14T12 0,6s · 14T6 7,5s ·
14T2 74s (cap 1200s mai avvicinato). Nessun candidato controesempio.
→ results/t6_decide.json · results/logs/t6_decide.log
Nota: verdetti OR-Tools, non ancora certificati (serve T7 DRAT per il SUCCESS
"risultato negativo di valore" di GOAL.md). Prossimo: T7.

## 2026-08-12 ~17:00 — T7 (parti a+b): toolchain DRAT + 4 gruppi certificati
Task: compilare toolchain di certificazione, validarla, certificare i gruppi.
Esito: cadical 3.0.1 e drat-trim compilati ai commit pinnati (tools/).
Gauntlet Z7/Z11: entrambi cadical exit 20 (UNSAT) + drat-trim "s VERIFIED".
Produzione: 14T30, 14T10, 14T12, 14T6 (min_size=3) TUTTI UNSAT + VERIFIED
(results/logs/t7_14T*.log, CNF/DRAT in results/cnf/). Conferma indipendente
dei verdetti CP-SAT di T6 su 4 istanze su 5.
14T2 (7,1M clausole): run in background PID 19098, watchdog cap 120min/9GB,
log results/logs/t7_14T2.log. Prossimo: verificare esito 14T2 al giro dopo.

## 2026-08-12 ~17:25 — T7 (check run 14T2)
Run PID 19098 ancora VIVO: cadical a ~725s di solving, ~1,7M conflitti,
memoria stabile, progresso regolare. Nessuna azione: lasciato lavorare.
Prossimo passo: ricontrollare l'esito al prossimo giro (attesi exit 20 +
s VERIFIED), poi chiudere T7 e passare a T8.

## 2026-08-12 ~17:50 — Controllo run 14T2 (iterazione di sola sorveglianza)
- PID 19098 VIVO, elapsed ~24 min (cap watchdog 120). cadical a ~1423s di
  solving, ~3,83M conflitti, remaining 79%, RAM trascurabile. Progresso regolare.
- Nessun altro task avviato (regola: niente lavoro pesante in parallelo al run).
- Prossimo passo: al giro successivo ricontrollare l'esito (atteso exit 20 + DRAT verified).

## 2026-08-12 13:08 — Controllo run 14T2 (T7)
Run PID 19098 VIVO e in progresso: cadical a ~2144s di solving, ~6,4M
conflitti, remaining sceso 79%→61%, elapsed 36 min su cap 120, RAM ok.
Nessun'altra azione (regola: nessun task pesante in parallelo).
Prossimo passo: ricontrollare 14T2 al giro successivo.

## 2026-08-12 ~13:25 — Controllo run 14T2 (iterazione di sola sorveglianza)
- PID 19098 VIVO, elapsed 48:25 su cap 120 min. cadical a ~2889s di solving,
  ~9,47M conflitti (erano 6,4M al giro scorso), remaining stabile a 61%,
  RSS trascurabile. Progresso reale (conflitti in crescita), nessun stallo.
- Nessun'altra azione: si lascia lavorare. Prossimo giro: stesso controllo,
  se finito verificare CADICAL_EXIT=20 + s VERIFIED + DRAT_EXIT=0.

## 2026-08-12 14:05 — T7: check run 14T2 (iterazione di solo controllo)
- PID 19098 VIVO (elapsed 1:00:48, RSS trascurabile). SVOLTA: cadical ha
  terminato con `s UNSATISFIABLE` + `CADICAL_EXIT=20` — 14T2 è UNSAT.
- Ora gira drat-trim sulla verifica del certificato (log pieno di WARNING
  "duplicate literal": benigni, drat-trim li ripulisce da solo).
- Manca solo `s VERIFIED` + `DRAT_EXIT=0` per dichiarare SUCCESS su T7.
- Prossimo passo: al prossimo giro verificare DRAT_EXIT; se 0 ⇒ T7 chiuso,
  avviare T8 (FOUND.md + status DONE).

## 2026-08-12 ~14:20 — Controllo run 14T2 (T7)
Run PID 19098 vivo (elapsed 1:12:24). drat-trim (PID 24259) al 99% CPU,
RSS ~2,2 GB, proof line ~7,22M. Nessun verdetto ancora nel log. Nessuna
azione: lasciato lavorare. Prossimo passo: rileggere l'esito al prossimo giro
(watchdog scade a ~120 min di elapsed).

## 2026-08-12 13:56 — Controllo run 14T2 (T7)
Run vivo: wrapper PID 19098 elapsed 1:24:05; drat-trim (PID 24259) elapsed
29:16, 98,6% CPU, RSS ~2,1 GB (cap 9 GB ok), proof line ~7,22M, solo WARNING
benigni "duplicate literal", nessun verdetto. Lasciato lavorare.
Prossimo passo: rileggere l'esito al prossimo giro (watchdog 120 min sul
wrapper ⇒ kill atteso verso elapsed 2:00 se non finisce prima).

## 2026-08-12 14:08 — T7 (14T2): controllo run drat-trim
Run vivo: wrapper PID 19098 elapsed 1:36:22; drat-trim PID 24259 elapsed
41:35, 99,3% CPU, RSS ~2,0 GB (cap 9 GB ok). Nessun verdetto ancora, solo
WARNING benigni (duplicate literal), proof line ~7,22M. Lasciato lavorare.
Prossimo passo: ricontrollare; se il watchdog ha ucciso a 120 min, rilanciare
SOLO drat-trim sul .drat esistente oppure confermare con kissat.

## 2026-08-12 14:20 — T7 CHIUSO: drat-trim su 14T2 VERIFIED
Il run in background (PID 19098) è terminato prima del cap watchdog:
`s VERIFIED`, `DRAT_EXIT=0`, verification time 2939,8 s (log
results/logs/t7_14T2.log). Con questo tutti e 5 i gruppi minimali senza
14-ciclo (14T2, 14T6, 14T10, 14T12, 14T30) sono UNSAT (min_size=3) con
certificato DRAT verificato — seconda gamba indipendente rispetto a CP-SAT
(T6). Prossimo passo: T8, scrittura del teorema di grado 14 (FOUND.md,
docs, status DONE).

## 2026-08-12 14:24 — T8 Teorema grado 14: FOUND.md + docs + DONE
Scritti results/FOUND.md (enunciato, catena logica, tabella 5 gruppi, comandi di riverifica) e docs/theorem-degree14.md (nota inglese). Dati da t6_decide.json e grep sui log t7_14T*: 5/5 s VERIFIED, DRAT_EXIT=0 su 14T2. status.txt -> DONE. Criterio SUCCESS di GOAL.md soddisfatto (UNSAT taglie >=3 sui 5 minimali, CP-SAT + DRAT verificato).
Prossimo passo: nessuno automatico; T9 (grado 15) parte solo se l'umano rimette RUN e rilancia il loop.

## 2026-08-13 17:15 — Sessione interattiva: esperimento margine-0 + toolchain PB/LRAT
Esperimento "margine 0" (nuovo, margin_zero.py, validato su Z7/Z11 rhs=-1
prima dell'uso): su Z7, Z11, Z13 CP-SAT dice (a) sanity E1a: insieme delle
parti = testimone margine 0, verificato coi due checker; (b) E1b INFEASIBLE:
NESSUN'ALTRA famiglia ciclica-invariante ha margine <= 0 (unicita'
dell'estremale); (c) E2 INFEASIBLE: con taglie >=3 margine minimo >= 1.
Secondo metodo: cadical+LRAT VERIFIED su 4/6 istanze (Z7/Z11 E1b+E2);
Z13 E1b/E2 in corso. Log: results/logs/margin0_run.log, results/margin0/.
Toolchain nuova in tools/: Exact (build ok, OPB nativo + --proof-log),
VeriPB 3.0.2 (Rust, cargo), lrat-trim 0.2.0, catena cadical --lrat
--no-binary -> lrat-check VALIDATA (trappola: LRAT binario di default,
lrat-check dice NOT VERIFIED; sempre --no-binary col lrat-check testuale).
Gauntlet Exact: Z7/Z11 UNSAT + VeriPB "s VERIFIED UNSATISFIABLE" [M];
Z13/Z14min3 in corso; OPB Z15min3 in generazione preventiva.

## 2026-08-13 ~19:00 — Checkpoint 60min su Exact/Z14 + avvio sonda sharding Z15
Collaudo Exact: Z13 PASSATO (s UNSATISFIABLE, prova 3,8 GB in ~25 min).
Z14min3 senza proof log: oltre 60 min senza verdetto MA progresso misurabile
(4,4M conflitti) => lasciato correre; la catena lancia Z15 da sola su UNSAT.
REPRICING onesto: Exact >60x piu' lento di CP-SAT su Z14min3 => Z15
monolitico via Exact incerto (ore-giorni). Attivata in parallelo Route A:
results/cnf/z15min3.cnf RIGENERATO BYTE-IDENTICO alla formula congelata del
repo pubblicato (sha256 e6c732cf... VERIFICATO); shard_probe.py (8 orbite
s=3 r=15 coeff -9); sonda: 6 shard estremi, cap 30 min/cad, generate-and-
delete. Log: results/logs/shard_probe.log. Lezione: i verdetti Exact si
fanno SENZA proof log (Z14 con proof log: 15,5 GB parziali, interrotto).

## 2026-08-13 ~21:30 — Esito sonde Z15: tutte le porte economiche chiuse
Sonda sharding k=8: 5/6 shard UNSAT in 2-17 s, corner tutto-escluso oltre
cap 30 min (skew da manuale). Sonda 1-orbita-inclusa: cap sfondato. Sonda
min4 (taglie>=4): cap sfondato (RSS 4,4 GB). CONCLUSIONE [M]: niente
decomposizione facile; la durezza e' robusta per CDCL/risoluzione.
Strade rimaste per Z15: (1) Exact monolitico (Z14 collaudo a 2h35m+ e
7,9M conflitti; proiezione Z15 ~40h [E, scala CP-SAT x15] > cap 15h del
watchdog armato); (2) Route B rivisitata: cadical --lrat SENZA cap su piu'
giorni + verifica LRAT in streaming — RIAPERTA dalla toolchain di oggi (il
muro storico era la RAM di drat-trim, dissolto; il disco basta: 313 GB);
(3) cubi profondi con lookahead (march_cu) = infrastruttura futura;
(4) opzione verdetto-senza-certificato: un terzo solver (es. kissat, mai
provato su questa formula) + CP-SAT = standard due-metodi.
NB: NON rilanciare cadical su Z15 con cap breve: stessa versione/opzioni =
stessa traiettoria del run storico morto a 13h; ha senso solo unbounded.
Decisione rimandata al mattino con i numeri di Z14/Exact in mano.

## 2026-08-13 ~22:00 — Stop manuale dei run notturni; stato consolidato
Run Exact Z14min3 terminato dall'esterno dopo 3h09m+ (s UNKNOWN, shutdown
pulito). DATO CHE RESTA [M]: Exact > 3h09m su Z14min3 senza verdetto (CP-SAT:
60 s) => scala Exact su queste istanze ~200x CP-SAT; proiezione Z15
monolitico via Exact: giorni [E]. Z15 mai partito. Nessun processo attivo.
Collaudo Exact: PASSATO su Z7/Z11 (+VeriPB verified) e Z13; Z14min3
INTERROTTO (non fallito). Ripresa: vedi menu' tre strade nel journal delle
21:30 (Route B unbounded con LRAT streaming = favorita; kissat verdetto
rapido; cubi profondi). Tutti gli artefatti a posto: margin0/ (REPORT+
SHA256SUMS+6 LRAT), opb/ (z7/z11/z13 con prove, z15min3.opb sha d38dfc29...),
cnf/ (z15min3.cnf sha e6c732cf... byte-identico al pubblicato, z15min4.cnf).

## 2026-08-13 22:31 — ROUTE B LANCIATA (cadical --lrat unbounded su Z15)
Driver SGANCIATO (nohup+disown, immune ai cleanup di sessione che stasera
hanno ucciso due volte i task in background — diagnosi confermata con la
sessione di pubblicazione, che e' scagionata). scripts/routeB.sh: solver
pid in STATE/routeB.pid, log results/logs/routeB_z15.log, driver log
routeB_driver.log con HEARTBEAT orario (RSS/disco/taglia prova). Guardia:
RAM 9GB, disco min 30GB, NESSUN cap di tempo. A fine corsa: exit 20 =>
lrat-check automatico in streaming + notifiche macOS a ogni evento.
Formula: results/cnf/z15min3.cnf (sha e6c732cf..., byte-identica alla
pubblicata). Prova: TESTO (lrat-trim scartato per la verifica: e' un
trimmer backward IN MEMORIA, muro RAM reincarnato; lrat-check forward
streaming e' la catena validata 6/6 oggi). ATTENZIONE: Mac A BATTERIA al
lancio (97%, ~16h) — SERVE L'ALIMENTATORE per un run multi-giorno.

## 2026-08-14 19:20 — *** Z15 CHIUSO: UNSAT CON CERTIFICATO VERIFICATO ***
Route B completata. cadical 3.0.1 su results/cnf/z15min3.cnf (sha e6c732cf,
byte-identica alla formula pubblicata): exit 20 = UNSAT in 73.544,58 s
(20h26m), max RSS 4,79 GB. Prova LRAT testuale 158.233.546.333 byte (147 GB).
lrat-check (drat-trim repo): "c VERIFIED" in 1.358,68 s (22,6 min),
max live clauses 28.850.111 (streaming: RAM ~ formula, non ~ prova).
STANDARD SUPERATO: CP-SAT INFEASIBLE (modello nativo, 2026-08-11) +
cadical UNSAT (CNF congelata) + certificato verificato = due metodi
indipendenti E certificato. OPEN PROBLEM 1 del repo ciclico: RISOLTO.
Nessuna famiglia union-closed Z15-invariante (taglie>=3) viola Frankl.
Conseguenza: via libera al teorema di grado 15 transitivo (T9).
NON CANCELLARE results/cnf/z15.lrat (147 GB): E' il certificato.
sha256 in calcolo -> results/cnf/z15.lrat.sha256. Da fare: verbale
results/Z15-CLOSED.md, commit, decisioni di pubblicazione (nuova versione
Zenodo repo ciclico + aggiornare open-problems.md), archiviazione xz.

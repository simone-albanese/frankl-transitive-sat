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

## 2026-08-14 20:53 — *** GRADO 15 CHIUSO: teorema transitivo certificato (T9) ***
Sessione interattiva (richiesta umana: "dall'analisi del percorso Z15,
risolvi e proponi soluzioni"). Catena completa in serata:
1. Census 104 gruppi da GAP trans15.grp sha 89cd49a6 (LMFDB dietro
   reCAPTCHA il 14/08 — fonte primaria migliore; ordini incrociati con
   TRANSPROPERTIES per ogni gruppo enumerato). 78 con 15-ciclo (coperti
   da Z15 certificato stamattina), 26 senza, 0 aperti. Trappola nuova
   documentata: il 15-ciclo e' PARI, niente scorciatoia di parita'
   (PSL(4,2) ha cicli di Singer).
2. Riduzione: 3 minimali certificati per ARITMETICA (Lemma 5 ordini
   15/30/45 + completezza census): 15T5=A5 (686 orbite), 15T9=[5^2]3
   (478), 15T26=[3^4]5 (222); gli altri 23 con testimone LETTERALE
   (generatori census-figlio dentro l'enumerazione del padre). Nessun
   UNKNOWN. Sanity a mano 688/480 orbite Burnside riprodotte.
3. Controlli gauntlet Z7/Z11 INFEASIBLE (t9_controls_gauntlet.log).
4. Metodo 1 CP-SAT decide min_size=3: INFEASIBLE 2,2/31,7/59,1 s.
5. Metodo 2+certificati (driver t9_certify.sh, sganciato): cadical
   --lrat --no-binary exit 20 su CNF congelati (sha in
   SHA256-15T-cnf.txt) + lrat-check "c VERIFIED" 3/3; LRAT 3,9/54,9/
   162,2 MB (sha in SHA256-15T-lrat.txt). Totale 2m26s SOTTO carico xz.
Verbale: results/DEGREE15-CLOSED.md. Teorema: docs/theorem-degree15.md.
Lemmi: docs/notes-minimality-15.md. Backlog T9 spuntato, T9b aperto
(pubblicazione: commit/push/README/xz/Zenodo = decisioni umane).
Intanto xz di z15.lrat in corso (11,3 GB output alle 20:50, ETA ~22:15).

## 2026-08-14 ~22:20 — Controllo di letteratura COMPLETO: novita' confermata
Sweep arXiv+web (docs/literature-review.md). Esito: NESSUNA sovrapposizione.
Verifica esaustiva generale ferma a m<=12 (Vuckovic-Zivkovic 2017); linea
invariante = solo famiglie 1-orbita (Johnson-Vaughan 1998; Polymath11;
AEL EJC 2021 arXiv:2010.08795 con "media >= n/2" su gruppi abeliani;
preprint Nived 2024; formalizzazione Isabelle di AEL nell'AFP, gen 2025).
Nessun lavoro SAT/DRAT/LRAT su Frankl: i nostri paiono i primi certificati
SAT sulla congettura, e i primi con checking formalmente verificato.
Costante generale ferma a ~0,38271 (Liu); congettura APERTA (due preprint
che pretendono la dimostrazione completa, 2015 e gen 2026, non accettati:
da rimonitorare prima di sottomettere). Inquadramento per la nota: usare
la riformulazione "transitivo => frequenze uguali => media >= m/2"
(stessa moneta di AEL, complementarita' esatta). Trovato cugino di
template: Rivest-Vuillemin su 14 variabili (arXiv:1701.02374, gruppi
transitivi di grado 14 — la citazione in notes-minimality.md e' imprecisa,
correggerla se usata). cake_lpr su Z15: in corsa (RSS ~3 GB, sano).

## 2026-08-14 22:28 — Bozza nota arXiv scritta e compilata (T9c avviato)
paper/ucc-transitive-15.tex (amsart, file unico, bibliografia inclusa)
+ PDF compilato con tectonic (installato via brew). Contenuto: teorema
principale (transitivi m<=15), riformulazione "frequenze uguali/taglia
media", teorema margine-0, riduzioni con lemmi (incl. Lemma aritmetico
grado 15), tabelle istanze cicliche/14/15, sezione verified
verification, related work dalla literature-review, riproducibilita'
con DOI. TODO nel sorgente: authorship/ringraziamenti (decisione
umana), DOI nuova versione Zenodo, riga cake_lpr-Z15 (run in corso),
ricontrollo ID arXiv della linea Gilmer. cake_lpr Z15: in corsa.

## 2026-08-14 23:30 — cake_lpr su Z15: progresso misurato, ETA rivista
Run sano (RSS 2-4,5 GB, CPU 30-80%). lsof -o su macOS mostra la taglia
(smascherato con sonda a offset noto); offset VERO via proc_pidfdinfo:
39,6% del file alle 23:30, 12 MB/s costanti => fine ~01:45. Fattore
reale vs lrat-check ~10x, non il 2,3x estrapolato dai certificati
piccoli (lezione in lezioni.md). Driver sotto caffeinate: notifica
macOS automatica a fine corsa anche senza sessione attiva.

## 2026-08-15 01:15 — cake_lpr su Z15: HEAP ESAURITO (limite risorse, non verdetto)
Run 21:57->01:05 (3h10m): "CakeML heap space exhausted" con heap 12 GB,
alla stima ~80-85% del file [E da 12 MB/s misurati]. RSS max 6,5 GB,
footprint 12,9 GB. NON dice nulla contro il certificato (che resta
VERIFICATO da lrat-check): e' il fabbisogno del checker verificato —
~28,85 M clausole vive x rappresentazione CakeML (~4-6x C) x GC a copia
(x2) = ~15-25 GB > 16 GB fisici. Bilancio cake_lpr: 9/10 VERIFIED
(3 grado-15 + 6 margin0); Z15 pendente con 4 strade documentate in
results/cakelpr-verification.md (consigliata: macchina 64 GB, e' la
config prevista dal Makefile stesso di cake_lpr). Paper aggiornato
(abstract + sezione verified verification, ricompilato). Nessun
processo residuo nostro; z15.lrat e z15.lrat.xz intatti.

## 2026-08-15 00:30 — ARCHIVIAZIONE E PUBBLICAZIONE Z15 COMPLETATE
xz: 147 GB -> 19 GB (20.293.454.416 byte, sha fcd65ffc..., 1h48m, test ok).
Zenodo v1.1.0 PUBBLICATO: DOI 10.5281/zenodo.21939129 (concept ...21900942),
7 file (3 nuovi: z15.lrat.xz + sha + Z15-RESOLVED.md; 4 ereditati v1.0.0).
Intoppo risolto: PUT metadati HTTP 500 per prereserve_doi ereditato ->
rimosso prereserve_doi/imprint_publisher dal PUT -> 200 -> publish ok.
Repo ciclico: DOI agganciato in Z15-RESOLVED.md e pushato. Token eliminato
dallo scratchpad; CHIEDERE ALL'UTENTE DI REVOCARLO su zenodo.org.
Restano (altra sessione, T9b): commit grado 15 + release/archivio suoi LRAT.

## 2026-08-15 — T9b pubblicazione grado 15 COMPLETATA (sessione Z15)
Commit 0f58000 (39 file: teorema, verbale, census, lemmi, cake_lpr 9/10,
script, log) + README 0ddb264 (due teoremi, DOI Zenodo Z15, stato cake_lpr)
+ release v1.1.0 con 9 asset (3 coppie CNF+LRAT xz ~38 MB + manifesti
SHA256). paper/ NON committato (decisioni umane: authorship, DOI, arXiv).
Restano: eventuale Zenodo v2 del dataset transitive (serve token), revoca
token Zenodo di stanotte, decisioni paper, sonda grado 16.

## 2026-08-15 — Zenodo v1.1.0 transitive + traduzione inglese COMPLETATE
Zenodo v1.1.0 dataset transitive: DOI 10.5281/zenodo.21943855 (concept
...21920979), 10 file (3 coppie CNF+LRAT xz + 3 manifesti + verbale).
DOI agganciato in README e DEGREE15-CLOSED. Traduzione EN di 9 verbali/
note nei due repo (commit 8ffb1b8 + f07bbd3), verificata su ancore hash/
numeri e residui; diario STATE/ e CLAUDE.md restano IT (fonti primarie).
Token eliminato; ricordare all'utente la revoca.

## 2026-08-15 — CHIUSURA DEL PROGETTO (decisione del proprietario)
Il proprietario dichiara CHIUSO il lavoro 13-15 e DECLINA il grado 16.
Bilancio finale: ciclico 13/14/15 certificati; transitivo chiuso fino a
15 punti (Cauchy + 5 istanze grado 14 + Z15 + 3 istanze grado 15);
margine-0 caratterizzato; cake_lpr 9/10. Pubblicato: 2 repo EN coerenti,
release v1.0.0/v1.1.0, Zenodo x4 (DOI 21900943, 21939129, 21920980,
21943855). Aperti PER SCELTA: paper (bozza in paper/, decisioni umane),
cake_lpr 10/10 (macchina 64 GB), grado 16 (lasciato ad altri, costi
prezzati nel README). Il loop NON va riavviato.

## 2026-08-15 — Pulizia disco su richiesta del proprietario: +173 GB
Eliminati (previa verifica md5 byte-identico con Zenodo per z15.lrat.xz):
z15.lrat (147 GB), z15.lrat.xz (19 GB), z15min3/min4.cnf, originali 15T*
non compressi, results/opb/ (5,8 GB Exact). Restano: xz grado 14 e 15,
margin0/ (unica copia locale, rigenerabile), tutte le impronte. Cartella
progetto: 5,8 GB. Disco: 317 GB liberi.

# Backlog — frankl-transitive (grado 14 → 15 → 16)
Ordinati per valore/costo. Un task atomico per iterazione. T2 è di
progettazione: scrivere `high` in STATE/effort.txt PRIMA di iniziarlo.

## [x] T1 — FATTO 2026-08-12 (26 senza 14-ciclo su 63; STATE/census14.json) — Census dei gruppi transitivi di grado 14 + filtro "senza 14-ciclo"
Fonte primaria: GAP, `TransitiveGroups(14)` (attesi 63 gruppi: VERIFICARE il
numero, non fidarsi). Installazione: `brew install gap` (pesante ma una
tantum). Alternativa senza GAP: API LMFDB
`https://www.lmfdb.org/api/gps_transitive/?degree=14&_format=json`.
**Filtro sui cycle type, MAI sugli ordini** (un elemento di ordine 14 può
essere (2,7,1^5) e non un 14-ciclo): un gruppo "ha il 14-ciclo" sse una sua
classe di coniugio ha cycle type (14).
Deliverable: `STATE/census14.json` — per gruppo: etichetta nT, ordine,
generatori (permutazioni 0-based), `has_14_cycle`. Nel journal: quanti con e
senza. Sanity: 14T1 dev'essere Z14 con `has_14_cycle=true`; D7 regolare e
PSL(2,13) devono risultare senza.

## [x] T2 — FATTO 2026-08-12 (lista finale: 14T2/6/10/30 minimali certificati + 14T12 UNKNOWN conservativo; docs/notes-minimality.md + results/minimality_scan.json) — Lemma di minimalità + lista finale dei gruppi-istanza
NOTA: 14T12 lasciato in lista per prudenza (7-elementi non-fpf, criterio L4
non applicabile; solo 172 orbite ⇒ deciderlo via SAT costa meno che
classificarlo). Task opzionale a bassa priorità in coda: T-opz-minimality12.

## [x] T2-originale (testo storico del task, superato — vedi T2 sopra)
Scrivere `docs/notes-minimality.md`: (i) F G-invariante ⟹ H-invariante per
ogni H ≤ G (immediato, ma va scritto); (ii) quindi basta decidere i transitivi
MINIMALI senza 14-ciclo (minimali tra i sottogruppi transitivi, a meno di
coniugio in S14); (iii) attenzione: un minimale-senza-ciclo può contenere
sottogruppi transitivi più piccoli CON ciclo? NO se contiene un sottogruppo
transitivo qualsiasi non è minimale-transitivo — ma un gruppo senza 14-ciclo
può contenere un transitivo con 14-ciclo? Se H ≤ G ha un 14-ciclo, quel ciclo
sta anche in G ⇒ impossibile. Quindi: i minimali-transitivi dentro l'insieme
dei senza-ciclo = i minimali-transitivi tout court che non hanno ciclo.
NOTA 12/08: GAP NON è in Homebrew (brew install gap fallisce). Alternative: lista minimal transitive dalla letteratura (arXiv:1701.02374), calcolo in Python sui 26 gruppi del census (gens disponibili), o GAP via conda/docker se davvero serve. Calcolo in GAP: sottogruppi transitivi minimali di ciascun senza-ciclo
(o lista dei "minimal transitive groups" di grado 14 dalla letteratura,
citata in arXiv:1701.02374). Deliverable: lista breve dei gruppi da decidere
con stima orbite ciascuno (Burnside: (1/|G|)·Σ_g 2^{c(g)}, c = numero di
cicli di g sui punti). Atteso ~O(pochi): D7 regolare (ordine 14, stima ~1300
orbite) è il caso grosso; i gruppi grandi hanno pochissime orbite.

## [x] T3 — FATTO 2026-08-12 (group_orbits.py + sat_group.py + dump_dimacs_group.py; smoke: 14T2=1234 orbite non banali, 14T30=50, Z7 INFEASIBLE, DIMACS Z7/Z11 byte-identici ai moduli ciclici) — Modulo `group_orbits.py` + encoder generalizzati
Chiusura col rappresentante fisso giustificata nel docstring di sat_group
(vale per ogni G: (A',B') = g(A, g⁻¹B')). Moduli ciclici NON toccati.
CLI: `"$PY" sat_group.py <Z13|14T2> [decide|optimize] [cap_s] [min_size]`.

## [x] T4 — FATTO 2026-08-12 (Z13: 630 orbite/1.863.311 clausole/INFEASIBLE 15,5s; Z14 min3: 1180 orbite/INFEASIBLE 90,1s — numeri identici ai pubblicati) — Validazione della pipeline generalizzata sui casi certificati
`group_orbits` con G = ⟨(0 1 … 12)⟩ DEVE dare 630 orbite e 1.863.311 clausole
di chiusura; INFEASIBLE in tempi ~Z13. Con G = Z14, min3: 1180 orbite,
INFEASIBLE. Confronto coi numeri pubblicati (frankl-cyclic-sat,
docs/results.md). Controlli controls.py. Solo dopo: istanze nuove.

## [x] T5 — FATTO 2026-08-12 (mode probe in sat_group.py; tutte le istanze entro budget, max 14T2: 7,10M clausole / 1,78 GB; results/t5_probe.json) — Sonda risorse dei gruppi-istanza (regola 5b)

## [x] T6 — FATTO 2026-08-12 (tutte e 5 INFEASIBLE: 14T30 0,1s · 14T10 0,6s · 14T12 0,6s · 14T6 7,5s · 14T2 74s; results/t6_decide.json) — Decisione CP-SAT per ogni gruppo-istanza (taglie ≥ 3)
Un run per gruppo sotto watchdog, budget hardware.env. INFEASIBLE atteso;
FEASIBLE ⇒ 🔴 doppio checker immediato (candidato controesempio!).

## [x] T7 — FATTO 2026-08-12 (tutti e 5 i minimali UNSAT con certificato DRAT verificato: 14T30/14T10/14T12/14T6 + 14T2 chiuso alle 14:20 con "s VERIFIED", DRAT_EXIT=0, verification time 2939,8 s; log results/logs/t7_14T*.log, CNF+DRAT in results/cnf/) — Toolchain di certificazione + DRAT per ogni gruppo-istanza
Toolchain: tools/cadical 3.0.1 + tools/drat-trim (commit pinnati), validata
su Z7 e Z11 (entrambi exit 20 + "s VERIFIED") prima della produzione.

## [x] T8 — FATTO 2026-08-12 (results/FOUND.md + docs/theorem-degree14.md; status DONE; commit+push) — Scrittura del teorema di grado 14 (FOUND.md + docs inglesi + push)
Enunciato: minimali senza ciclo UNSAT (T6+T7) ∧ Z14 certificato (repo
precedente) ⟹ nessun transitivo di grado 14 ammette controesempio invariante.

## [ ] T9 — Grado 15: census, minimali senza 15-ciclo, e nota sulla
dipendenza da Z15 (il ramo CON 15-ciclo resta condizionale finché Z15 non è
confermato — decisione umana se chiudere prima Z15 via sharding).

## [ ] T10 — Grado 16: census (attesi ~1954 transitivi — verificare), stima
istanze (i 2-gruppi regolari possono superare l'inviluppo: sonda prima).

## [ ] T-opz-minimality12 (OPZIONALE, bassa priorità) — Stato di 14T12
Decidere se 14T12=1/2[D(7)^2]2 (196, 172 orbite) è transitivo-minimale:
serve un argomento per sottogruppi con 7-elementi tutti non-fpf (Lemma 4 non
applicabile). Valore basso: la lista che lo include è già corretta; farlo
solo se il SAT su 14T12 risultasse costoso. Conferma esterna possibile:
arXiv:1701.02374 (minimal transitive groups).

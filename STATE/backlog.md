# Backlog — frankl-transitive (grado 14 → 15 → 16)
Ordinati per valore/costo. Un task atomico per iterazione. T2 è di
progettazione: scrivere `high` in STATE/effort.txt PRIMA di iniziarlo.

## [ ] T1 — Census dei gruppi transitivi di grado 14 + filtro "senza 14-ciclo"
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

## [ ] T2 — Lemma di minimalità + lista finale dei gruppi-istanza · effort HIGH
Scrivere `docs/notes-minimality.md`: (i) F G-invariante ⟹ H-invariante per
ogni H ≤ G (immediato, ma va scritto); (ii) quindi basta decidere i transitivi
MINIMALI senza 14-ciclo (minimali tra i sottogruppi transitivi, a meno di
coniugio in S14); (iii) attenzione: un minimale-senza-ciclo può contenere
sottogruppi transitivi più piccoli CON ciclo? NO se contiene un sottogruppo
transitivo qualsiasi non è minimale-transitivo — ma un gruppo senza 14-ciclo
può contenere un transitivo con 14-ciclo? Se H ≤ G ha un 14-ciclo, quel ciclo
sta anche in G ⇒ impossibile. Quindi: i minimali-transitivi dentro l'insieme
dei senza-ciclo = i minimali-transitivi tout court che non hanno ciclo.
Calcolo in GAP: sottogruppi transitivi minimali di ciascun senza-ciclo
(o lista dei "minimal transitive groups" di grado 14 dalla letteratura,
citata in arXiv:1701.02374). Deliverable: lista breve dei gruppi da decidere
con stima orbite ciascuno (Burnside: (1/|G|)·Σ_g 2^{c(g)}, c = numero di
cicli di g sui punti). Atteso ~O(pochi): D7 regolare (ordine 14, stima ~1300
orbite) è il caso grosso; i gruppi grandi hanno pochissime orbite.

## [ ] T3 — Modulo `group_orbits.py` + encoder generalizzati
Orbite dei sottoinsiemi (bitmask) sotto generatori arbitrari (BFS), canone =
minimo dell'orbita, (r_O, s_O), assert lemma di integrità m | r_O·s_O.
Poi `sat_group.py` (CP-SAT, margine scalato Σ r(2s−m)x ≤ −m) e
`dump_dimacs_group.py` (riusa pb_adder con d_O = r(2s−m)/m interi).
Chiusura: per coppie di orbite, rappresentante A fisso × B su tutta l'orbita
— NB: per gruppi non ciclici verificare che il trucco del rappresentante
resti valido (vale: per G-invarianza ogni coppia è G-immagine di (A, B') con
A rappresentante) — scriverlo nel docstring. NON modificare i moduli ciclici.

## [ ] T4 — Validazione della pipeline generalizzata sui casi certificati
`group_orbits` con G = ⟨(0 1 … 12)⟩ DEVE dare 630 orbite e 1.863.311 clausole
di chiusura; INFEASIBLE in tempi ~Z13. Con G = Z14, min3: 1180 orbite,
INFEASIBLE. Confronto coi numeri pubblicati (frankl-cyclic-sat,
docs/results.md). Controlli controls.py. Solo dopo: istanze nuove.

## [ ] T5 — Sonda risorse dei gruppi-istanza (regola 5b)
Per ciascun gruppo di T2: n_orbite, n_clausole, RSS del modello, SENZA solve.
Confronto con l'inviluppo del playbook (§7). Se qualcosa sfora ⇒ ridisegno
prima di lanciare.

## [ ] T6 — Decisione CP-SAT per ogni gruppo-istanza (taglie ≥ 3)
Un run per gruppo sotto watchdog, budget hardware.env. INFEASIBLE atteso;
FEASIBLE ⇒ 🔴 doppio checker immediato (candidato controesempio!).

## [ ] T7 — Toolchain di certificazione + DRAT per ogni gruppo-istanza
Ricompilare cadical e drat-trim (ricetta: frankl-cyclic-sat
docs/reproducing.md §1, commit pinnati). Validare su Z7/Z11. Poi
dump → CaDiCaL → drat-trim per ciascun gruppo di T6.

## [ ] T8 — Scrittura del teorema di grado 14 (FOUND.md + docs inglesi + push)
Enunciato: minimali senza ciclo UNSAT (T6+T7) ∧ Z14 certificato (repo
precedente) ⟹ nessun transitivo di grado 14 ammette controesempio invariante.

## [ ] T9 — Grado 15: census, minimali senza 15-ciclo, e nota sulla
dipendenza da Z15 (il ramo CON 15-ciclo resta condizionale finché Z15 non è
confermato — decisione umana se chiudere prima Z15 via sharding).

## [ ] T10 — Grado 16: census (attesi ~1954 transitivi — verificare), stima
istanze (i 2-gruppi regolari possono superare l'inviluppo: sonda prima).

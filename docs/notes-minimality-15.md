# Nota — Lemma di minimalità per il grado 15

Obiettivo: ridurre la decisione "esiste F union-closed G-invariante con
margine ≤ −1, per G transitivo di grado 15 senza 15-ciclo" (26 gruppi del
census, `STATE/census15.json`) a una **lista corta di gruppi-istanza**.

Convenzioni: punti = {0,…,14}; F ⊆ P([15]); G ≤ S15 transitivo;
"senza ciclo" = nessun elemento di G ha cycle type (15). I Lemmi 1–2 della
nota di grado 14 (`notes-minimality.md`) valgono verbatim: l'invarianza
scende ai sottogruppi, e ogni sottogruppo di un senza-ciclo è senza-ciclo.

## Fonte del census (diversa dal grado 14, con doppia verifica)

`STATE/trans15.grp` = libreria transitiva di GAP (A. Hulpke), copiata da
`https://raw.githubusercontent.com/hulpke/transgrp/master/data/trans15.grp`,
sha256 `89cd49a642797ba47f97b6ecd2addd0ca7c3def99b79435a37ccecb57cbcca00`
(il 14/08/2026 l'API LMFDB è dietro una protezione reCAPTCHA; la libreria
GAP è la fonte primaria della stessa classificazione). Il build
(`scripts/census15_build.py`) incrocia due sezioni indipendenti del file:
per ogni gruppo enumerabile l'ordine BFS dei generatori (TRANSGRP) deve
coincidere con l'ordine dichiarato (TRANSPROPERTIES), o il build fallisce.
Esito: 104 gruppi, 78 con 15-ciclo (testimone esplicito verificato o
enumerazione), 26 senza, 0 casi aperti.

**Attenzione (trappola di grado 15):** un 15-ciclo è una permutazione
*pari*, quindi la scorciatoia di parità del grado 14 ("generatori pari ⇒
niente ciclo") qui non esiste, e infatti non è usata. Esempio istruttivo:
15T72 = PSL(4,2) ≅ A8 su PG(3,2) **ha** un 15-ciclo (ciclo di Singer di
GL(4,2)) pur non avendo elementi di ordine 15 nell'azione naturale su 8
punti — il filtro è sul cycle type nell'azione di grado 15, mai altrove.

## Lemma 3 (ordine dei transitivi)
H transitivo di grado 15 ⇒ 15 | |H| (orbita-stabilizzatore). Per Cauchy
H contiene elementi di ordine 3 e di ordine 5. ∎

## Lemma 5 (esclusione degli ordini 15, 30, 45)
Nessun transitivo senza-ciclo di grado 15 ha ordine 15 o 30; l'ordine 45
non esiste proprio tra i transitivi di grado 15.

*Dim.* (15) Transitivo di ordine 15 = regolare; l'unico gruppo di ordine
15 è C15 (Sylow: n₃ = n₅ = 1), e un generatore di C15 regolare è un
15-ciclo. (30) Ogni gruppo di ordine 30 contiene un sottogruppo C15: se
n₅ = 6 e n₃ = 10 insieme, i soli elementi di ordine 5 e 3 sarebbero
6·4 + 10·2 = 44 > 29, assurdo; quindi un Sylow (3 o 5) è normale e il
prodotto P₃P₅ è un sottogruppo di ordine 15 = C15. In un transitivo H di
ordine 30 lo stabilizzatore ha ordine 2, e C15 ∩ Stab ha ordine che divide
gcd(15,2) = 1: C15 agisce con orbite di taglia 15, cioè regolarmente — un
suo generatore è un 15-ciclo, che sta in H (Lemma 2 al contrario: H lo
conterrebbe). (45) Un gruppo di ordine 45 è abeliano (n₃ = n₅ = 1 e i
gruppi di ordine p² sono abeliani); un permutazionale abeliano transitivo
è regolare (gli stabilizzatori, tutti coniugati e uguali, fissano tutto),
quindi avrebbe ordine 15 ≠ 45. ∎

## Criterio aritmetico di minimalità (via completezza del census)
Sia G senza-ciclo nel census. Un eventuale sottogruppo transitivo proprio
H < G sarebbe: senza-ciclo (Lemma 2), di ordine divisore proprio di |G|
(Lagrange), e S15-coniugato a una voce del census (completezza della
libreria transitiva) — quindi a una voce **senza-ciclo** con lo stesso
ordine. Se nessun ordine dell'insieme

  O = {60, 75, 120, 150, 300, 360, 405, 600, 720, 810, 1620, 2520,
       3240, 4860, 9720, 19440}   (ordini dei 26 senza-ciclo)

divide propriamente |G|, allora G è transitivo minimale — certificato.

Si applica a tre gruppi (gli ordini 15, 30, 45 sono già esclusi dal
Lemma 5, il 135 non compare nel census quindi non esiste transitivo):

- **15T5 = A₅(15)**, ordine 60 (divisori propri rilevanti: 15, 30 — esclusi);
- **15T9 = [5²]3 = C₅²⋊C₃**, ordine 75 (unico candidato: 15 — escluso);
- **15T26 = [3⁴]5 = C₃⁴⋊C₅**, ordine 405 (candidati 15, 45, 135 — esclusi).

## Testimoni letterali per gli altri 23
La libreria GAP usa generatori incrementali: per ognuno dei 23 gruppi
restanti, i generatori di una voce più piccola del census sono
**letteralmente elementi** del gruppo (verificato per appartenenza
all'enumerazione completa), generano un sottogruppo transitivo di ordine
proprio — testimone esplicito, nessun argomento di coniugio necessario.
La discesa atterra sulla lista minima in un passo:

- → 15T5 (A₅): 15T10 = S₅(15), 15T20 = A₆(15), 15T28 = S₆(15), 15T47 = A₇(15);
- → 15T9: 15T12, 15T13, 15T14, 15T17, 15T18, 15T19, 15T27 (famiglia [5²]);
- → 15T26: 15T33, 15T34, 15T35, 15T41, 15T42, 15T43, 15T52, 15T53,
  15T61, 15T62, 15T63, 15T70 (famiglia [3⁴]).

Esito più pulito del grado 14: **nessun caso UNKNOWN** (al 14 restava il
prudenziale 14T12). Scan: `scripts/minimality15_scan.py`, output
`results/minimality15_scan.json`.

## Teorema di copertura (identico al grado 14, con MIN aggiornato)
Sia MIN = {15T5, 15T9, 15T26}. Se per ogni M ∈ MIN non esiste F
union-closed M-invariante con margine ≤ −1, allora non esiste per nessuno
dei 26 gruppi senza-ciclo. (Stessa dimostrazione della nota di grado 14:
catena discendente finita + coniugio, i margini sono invarianti per
rinominazione dei punti.) ∎

I gruppi **con** 15-ciclo (78) contengono ⟨σ⟩ ≅ Z15 regolare, coniugato
allo Z15 standard: sono coperti dal risultato ciclico certificato del
2026-08-14 (`results/Z15-CLOSED.md`, UNSAT + LRAT verificato).

## Sanity delle orbite (conti a mano, riprodotti dallo scan)
- A₅(15): identità 2¹⁵; 15 involuzioni con 3 punti fissi (2⁹); 20 elementi
  di ordine 3 senza punti fissi (2⁵); 24 di ordine 5 senza punti fissi
  (2³). Burnside: (32768 + 15·512 + 20·32 + 24·8)/60 = 41280/60 = **688**.
- [5²]3: (32768 + 12·2⁷ + 12·2³ + 50·2⁵)/75 = 36000/75 = **480**
  (12 elementi di ordine 5 con 5 punti fissi, 12 senza, 50 di ordine 3
  senza punti fissi).
Se uno scan futuro non riproduce questi numeri, c'è un bug nello scan.

## Lista-istanze finale (per orbite decrescenti)

| gruppo | ordine | orbite (Burnside) | stato |
|---|---|---|---|
| 15T5 = A₅(15) | 60 | 688 | minimale (aritmetica) |
| 15T9 = [5²]3 | 75 | 480 | minimale (aritmetica) |
| 15T26 = [3⁴]5 | 405 | 224 | minimale (aritmetica) |

Tutte più piccole del caso peggiore già risolto al grado 14
(14T2 = D₇, 1236 orbite, CaDiCaL 55 min): il costo SAT del grado 15,
misurato in orbite, è inferiore a quello del grado 14.

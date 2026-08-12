# Nota — Lemma di minimalità per il grado 14

Obiettivo: ridurre la decisione "esiste F union-closed G-invariante con
margine ≤ −1, per G transitivo di grado 14 senza 14-ciclo" (26 gruppi del
census, `STATE/census14.json`) a una **lista corta di gruppi-istanza**.

Convenzioni: punti = {0,…,13}; F ⊆ P([14]); G ≤ S14 transitivo;
"senza ciclo" = nessun elemento di G ha cycle type (14).

## Lemma 1 (discesa dell'invarianza)
Se F è G-invariante e H ≤ G, allora F è H-invariante.
*Dim.* Ogni h ∈ H sta in G. ∎

## Lemma 2 (ereditarietà del no-ciclo)
Se H ≤ G e H contiene un 14-ciclo, quel 14-ciclo sta in G.
Quindi ogni sottogruppo (in particolare ogni sottogruppo transitivo) di un
gruppo senza ciclo è senza ciclo. ∎

## Lemma 3 (ordine dei transitivi)
H transitivo di grado 14 ⇒ 14 | |H| (orbita-stabilizzatore). In particolare
H contiene un elemento di ordine 7 (Cauchy). ∎

## Lemma 4 (2-generazione dei minimali, caso fpf)
Sia M ≤ S14 **transitivo minimale** (nessun sottogruppo proprio transitivo)
e sia a ∈ M di ordine 7 **senza punti fissi** (cycle type (7,7)).
Allora M = ⟨a, x⟩ per qualche x ∈ M.
*Dim.* Le orbite di ⟨a⟩ sono due 7-insiemi O1, O2. M transitivo ⇒ esiste
x ∈ M con x(p) ∈ O2 per qualche p ∈ O1. L'orbita di p sotto ⟨a,x⟩ contiene
O1 (via a) e x(p) ∈ O2, dunque tutta O2 (via a): ⟨a,x⟩ è transitivo.
Per minimalità M = ⟨a,x⟩. ∎

Nota: se OGNI elemento di ordine 7 di G è fpf (flag `order7_all_fpf` nello
scan), il Lemma 4 si applica a ogni transitivo minimale M ≤ G (l'elemento di
ordine 7 di M, Lemma 3, è fpf perché elemento di G).

## Criterio computazionale di minimalità (certificato completo)
Sia G enumerabile con tutti i 7-elementi fpf. Siano a_1,…,a_k rappresentanti
delle classi di G-coniugio degli elementi di ordine 7. Allora:

  G ha un sottogruppo transitivo proprio ⟺
  ∃ i, ∃ x ∈ G tali che ⟨a_i, x⟩ è transitivo e proprio.

*Dim.* (⇐) ovvio. (⇒) H < G transitivo contiene un transitivo minimale M
(catena discendente finita), M < G. M contiene b di ordine 7 (Lemma 3),
b = g a_i g⁻¹ per qualche i e g ∈ G. Allora g⁻¹Mg è transitivo minimale,
contiene a_i, e per Lemma 4 g⁻¹Mg = ⟨a_i, x⟩, proprio. ∎

Quindi il loop esaustivo "per ogni rappresentante a_i, per ogni x ∈ G:
⟨a_i,x⟩ transitivo ⇒ deve chiudere su tutto G" **certifica** la minimalità.
(Trucco di costo: se la chiusura BFS supera |G|/2, per Lagrange è = G.)

## Teorema di copertura (la riduzione)
Sia MIN l'insieme dei gruppi del census senza ciclo che sono transitivi
minimali. Se per ogni M ∈ MIN non esiste F union-closed M-invariante con
margine ≤ −1, allora non esiste per NESSUNO dei 26 gruppi senza ciclo.

*Dim.* Sia F un controesempio G-invariante, G senza ciclo. G contiene un
transitivo minimale M₀ (catena finita); M₀ è senza ciclo (Lemma 2) e
transitivo, quindi coniugato in S14 a un M ∈ MIN del census: M = s M₀ s⁻¹.
F è M₀-invariante (Lemma 1); allora F^s = {s(A) : A ∈ F} è M-invariante,
union-closed, con gli stessi |F|, stesse frequenze a permutazione dei punti,
stesso margine. Contraddizione. ∎

**Conseguenza pratica:** basta decidere (UNSAT/SAT) i soli gruppi di MIN.

## Fatti già acquisiti sui casi estremi
- Un sottogruppo regolare di ordine 14 è C14 o D7. C14 regolare = ⟨14-ciclo⟩:
  impossibile nei senza-ciclo. Quindi "sottogruppo transitivo di ordine 14"
  ⟺ "D7 regolare" (ogni transitivo di ordine 14 su 14 punti è regolare).
- In un D7 regolare le involuzioni hanno tipo 2^7 (dispari!) ⇒ nessun
  sottogruppo di A14 contiene un D7 regolare. In particolare 14T62 = A14 e
  14T59 ≤ A14 non sono coperti da D7: servono testimoni di sottogruppi
  transitivi propri più grandi (lo scan li costruisce esplicitamente:
  per A14 i generatori di 14T30 = PSL(2,13), tutti pari; per 14T59 un
  ⟨(7,7)-elemento, scambio-blocchi pari⟩ dentro (S7≀S2)∩A14).
- 14T2 = D7 è transitivo minimale (ordine 14: i sottogruppi propri hanno
  ordine ≤ 7, non divisibile per 14, Lemma 3).
- 14T30 = PSL(2,13): le involuzioni fissano 2 punti (q=13 ≡ 1 mod 4), quindi
  nessun D7 regolare; atteso minimale (lo scan lo certifica o lo smentisce).

## Cosa produce lo scan (`scripts/minimality_scan.py`)
Per ciascuno dei 26: ordine, n. orbite di P([14]) via Burnside
(1/|G|)·Σ_g 2^{c(g)} (solo enumerabili), flag `order7_all_fpf`,
ed esattamente uno tra:
- `minimal_certified: true` (criterio esaustivo sopra), oppure
- `witness`: generatori espliciti di un sottogruppo transitivo proprio
  (⇒ non minimale, coperto ricorsivamente dalla catena discendente), oppure
- `UNKNOWN` (gruppo grande, campionamento senza esito) ⇒ task di follow-up.

La **lista finale dei gruppi-istanza** = {certificati minimali} ∪ {UNKNOWN
residui dopo i follow-up}, ordinata per numero di orbite (Burnside).

Riferimento da verificare (task separato, non bloccante): arXiv:1701.02374
sui gruppi transitivi minimali — utile come conferma esterna della lista.

Sanity attesi: D7 regolare ≈ 1236 orbite ((2^14 + 6·2^2 + 7·2^7)/14 = 1236);
PSL(2,13) ≈ 52 orbite (calcolo a mano dalle classi). Se lo scan non
riproduce questi due numeri, c'è un bug nello scan.

## ESITO (2026-08-12, `results/minimality_scan.json`)
Sanity D7=1236 e PSL(2,13)=52 riprodotti. Lista finale dei gruppi-istanza
(copertura valida per tutti i 26 senza ciclo — i NOT_MINIMAL hanno tutti
testimone esplicito verificato):

| gruppo | ordine | orbite (Burnside) | stato |
|---|---|---|---|
| 14T2 = D7 regolare | 14 | 1236 | minimale certificato |
| 14T6 = [2^3]7 | 56 | 424 | minimale certificato |
| 14T10 = L_7(14) | 168 | 156 | minimale certificato |
| 14T12 = 1/2[D(7)^2]2 | 196 | 172 | UNKNOWN (incluso per prudenza)¹ |
| 14T30 = PSL(2,13) | 1092 | 52 | minimale certificato |

¹ 14T12 ha 7-elementi con punti fissi: il criterio del Lemma 4 non si
applica. Nessun ⟨a,x⟩ transitivo proprio esiste (verifica su TUTTI gli x);
potrebbe essere minimale oppure avere sottogruppi transitivi ≥3-generati con
7-elementi tutti non-fpf. Includerlo nella lista è comunque corretto
(sovrainsieme di MIN); ha solo 172 orbite, deciderlo via SAT costa poco.
14T46 (fpf, ordine 5040) risolto con ricerca esaustiva post-scan:
NOT_MINIMAL, testimone di ordine 42 (`results/logs/t46_exhaustive.log`).

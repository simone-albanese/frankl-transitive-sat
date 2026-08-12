# Obiettivo
Decidere se esistono famiglie union-closed su m punti (m = 14, poi 15, 16)
invarianti sotto QUALCHE gruppo di permutazioni transitivo, che violino la
congettura di Frankl (margine intero `2*maxfreq - |F| <= -1`), oppure trovare
un controesempio. Il caso ciclico è già chiuso e pubblicato
(repo `frankl-cyclic-sat`, DOI 10.5281/zenodo.21900943: Z13 e Z14 UNSAT
certificati DRAT; Z15 INFEASIBLE per CP-SAT ma NON confermato): restano
ESATTAMENTE i gruppi transitivi **senza m-ciclo**.

**Teorema bersaglio (grado 14):** "nessuna famiglia union-closed invariante
per un gruppo di permutazioni transitivo su 14 punti viola la congettura" —
estende oltre i primi il corollario che su 13 punti seguiva da Cauchy.

# Riduzione chiave (lemma da dimostrare PRIMA di calcolare)
F invariante sotto G ⟹ invariante sotto ogni H ≤ G. Quindi basta decidere i
gruppi transitivi MINIMALI (nell'ordine di inclusione tra sottogruppi
transitivi, a meno di coniugio) senza m-ciclo: UNSAT su questi ⟹ UNSAT per
tutti i sovragruppi; insieme a Z14 già certificato ⟹ teorema bersaglio.

**Trappola già identificata:** "contiene un m-ciclo" NON equivale a "contiene
un elemento di ordine m" quando m è composto: su 14 punti un elemento di
ordine 14 può avere cycle type (2,7,1^5). Il filtro del census va fatto sui
cycle type, mai sugli ordini.

# Criteri di SUCCESS (uno qualunque)
- Candidato controesempio: famiglia che passa ENTRAMBI i checker indipendenti
  (ucs_core.check_family e checker2.verify) con 2*maxfreq < |F| su interi.
- Risultato negativo di valore (grado 14): per OGNI gruppo transitivo minimale
  senza 14-ciclo, UNSAT (taglie ≥ 3, riduzione Sarvate–Renaud) confermato da
  due solver indipendenti o con certificato DRAT verificato da drat-trim.

# Controlli obbligatori (ereditati, non negoziabili)
- `controls.py` (P([4]), validatore, detector, accordo checker1/2) prima di
  ogni run di produzione.
- La pipeline generalizzata (orbite di G qualsiasi) DEVE riprodurre i numeri
  già certificati con G = Z13 (630 orbite, INFEASIBLE) e G = Z14 min3
  (1180 orbite, INFEASIBLE) PRIMA che un suo esito nuovo abbia valore.
- Aritmetica dei verdetti solo su interi; ratio < 0,382 ⇒ bug, fermarsi.
- Lemma di integrità da asserire nel codice: per G transitivo, ogni orbita di
  insiemi O (r insiemi di taglia s) ha frequenza uniforme r·s/m ⇒ m | r·s.

# Non-obiettivi e dipendenze dichiarate
- Grado 15: i gruppi CON 15-ciclo ridurrebbero a Z15, che NON è confermato.
  Prima si decidono i minimali senza 15-ciclo; il teorema pieno di grado 15
  resta condizionale finché Z15 non è chiuso (sharding: open problem 1 del
  repo precedente). La decisione se chiudere prima Z15 spetta all'umano.
- Niente riscritture estetiche del codice ereditato; niente esplorazioni
  fuori scope senza backlog con stima costo/valore.

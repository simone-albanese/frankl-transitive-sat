# Grado 15 — CHIUSO: teorema transitivo con certificati verificati (2026-08-14)

**Teorema.** Nessuna famiglia union-closed non banale F ⊆ P([15])
invariante per un gruppo di permutazioni transitivo G ≤ S15 (insiemi non
banali di taglia ≥ 3, riduzione Sarvate–Renaud che copre il caso generale)
viola la congettura di Frankl: il margine intero 2·maxfreq − |F| è ≥ 0.

Chiuso la sera stessa dello sblocco: la dipendenza (Z15 ciclico, open
problem 1 del repo `frankl-cyclic-sat`) è caduta alle 19:20 del
2026-08-14 (`Z15-CLOSED.md`); il teorema transitivo era chiuso e
certificato alle 20:53. Enunciato inglese completo con dimostrazione:
`docs/theorem-degree15.md`; riduzione e lemmi: `docs/notes-minimality-15.md`.

## Catena logica

1. **Census** (`scripts/census15_build.py` → `STATE/census15.json`):
   104 gruppi transitivi di grado 15, dalla libreria GAP `trans15.grp` di
   Hulpke (sha256 `89cd49a6…`, fonte primaria; l'API LMFDB il 14/08 era
   dietro reCAPTCHA). Doppia fonte per ogni gruppo enumerabile: l'ordine
   BFS dei generatori deve combaciare con la sezione TRANSPROPERTIES.
   Esito: **78 con 15-ciclo** (testimone verificato o enumerazione),
   **26 senza**, 0 aperti. Trappola documentata: il 15-ciclo è PARI
   (niente scorciatoia di parità; PSL(4,2) ha cicli di Singer).
2. **Riduzione** (`scripts/minimality15_scan.py` →
   `results/minimality15_scan.json`): i 78 col ciclo contengono Z15
   regolare → coperti dal certificato ciclico di stamattina. Dei 26
   senza ciclo, **3 sono minimali certificati per pura aritmetica**
   (Lemma 5: ordini 15/30/45 impossibili; completezza del census):
   15T5 = A₅(15), 15T9 = [5²]3, 15T26 = [3⁴]5. Gli altri 23 contengono
   uno dei tre come sottogruppo LETTERALE (generatori del census più
   piccolo ∈ enumerazione del più grande, verificato). Nessun caso
   UNKNOWN (al grado 14 c'era il prudenziale 14T12).
3. **Decisione — standard pieno su ciascuna delle 3 istanze** (due metodi
   indipendenti + certificato, catena LRAT ereditata dalla lezione Z15):

| istanza | orbite | clausole | CP-SAT | cadical --lrat --no-binary | lrat-check | LRAT |
|---|---|---|---|---|---|---|
| 15T5 (A₅) | 686 | 4.323.016 | INFEASIBLE 59,1 s | UNSAT exit 20, 93,2 s, RSS 1,27 GB | **c VERIFIED** | 162,2 MB |
| 15T9 ([5²]3) | 478 | 2.500.889 | INFEASIBLE 31,7 s | UNSAT exit 20, 28,5 s, RSS 1,02 GB | **c VERIFIED** | 54,9 MB |
| 15T26 ([3⁴]5) | 222 | 257.808 | INFEASIBLE 2,2 s | UNSAT exit 20, 0,6 s, RSS 150 MB | **c VERIFIED** | 3,9 MB |

Fase SAT completa (solve + verifica, driver `scripts/t9_certify.sh`):
**2 min 26 s** di orologio — contro le 20h26m del solo Z15. La riduzione
"smart, not harder" ha fatto il lavoro: 104 gruppi → 3 istanze, tutte più
piccole del caso peggiore del grado 14 (14T2: 1234 orbite, 55 min).

## Artefatti (tutti su disco, da committare/pubblicare)

- CNF congelati: `results/cnf/15T{5,9,26}.cnf`,
  sha256 in `results/cnf/SHA256-15T-cnf.txt`
  (15T5: `a5bbb82f…`, 15T9: `8c9ea9ec…`, 15T26: `af711123…`).
- Certificati LRAT testuali: `results/cnf/15T{5,9,26}.lrat`,
  sha256 in `results/cnf/SHA256-15T-lrat.txt`; totale 221 MB
  (comprimibili xz, pubblicabili senza problemi di taglia).
- Log: `results/logs/t9_decide_cpsat.log` (metodo 1),
  `results/logs/t9_certify.log` + `t9_15T*_{cadical,lratcheck}.log`
  (metodo 2 + verifica), `results/logs/t9_controls_gauntlet.log`
  (controlli Z7/Z11), `results/logs/minimality15_scan.log` (riduzione).

## Come riverificare

```bash
source STATE/hardware.env
# 1. census e riduzione (deterministici, ~4 min):
"$PY" scripts/census15_build.py && "$PY" scripts/minimality15_scan.py
# 2. formule (deterministiche) e impronte:
for g in 15T5 15T9 15T26; do "$PY" dump_dimacs_group.py $g /tmp/$g.cnf 3; done
shasum -a 256 /tmp/15T*.cnf   # attese: a5bbb82f… / 8c9ea9ec… / af711123…
# 3. certificati (streaming, ~1 min in tutto):
for g in 15T5 15T9 15T26; do
  tools/drat-trim/lrat-check results/cnf/$g.cnf results/cnf/$g.lrat | grep VERIFIED
done   # cercare "c VERIFIED", mai fidarsi del solo exit code
# 4. conferma indipendente senza certificato (~2 min):
for g in 15T5 15T9 15T26; do "$PY" sat_group.py $g decide 1200 3; done
```

## Conseguenze e pendenze

- **Ogni grado transitivo ≤ 15 è ora chiuso** (13 via Cauchy, 14 e 15 via
  teoremi; i gradi ≤ 12 sono coperti dalla verifica incondizionata della
  congettura in letteratura).
- Frontiere successive, coi prezzi noti: **Z16** monolitico resta il muro
  (stime settimane-mesi + ~314 GB di prova su questo hardware [E]);
  il **grado 16 transitivo** (1954 gruppi) è bloccato dall'ancora ciclica
  Z16 per i gruppi col 16-ciclo; verifica formalmente verificata
  (cake_lpr) dei certificati LRAT = upgrade di credibilità a costo basso.
- Da fare: commit dei nuovi file, aggiornamento README/FOUND, xz dei tre
  LRAT, release + nuova versione Zenodo (decisioni di pubblicazione
  dell'umano; per Zenodo serve un token).

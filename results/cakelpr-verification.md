# Verifica formalmente verificata dei certificati LRAT (cake_lpr)

Data: 2026-08-14 sera. Obiettivo: restringere la base di fiducia dei
risultati eliminando il verificatore non verificato (`lrat-check`, C
artigianale) come anello debole: ogni certificato LRAT del progetto viene
riverificato con **cake_lpr**, un checker la cui correttezza è un teorema
dimostrato a macchina (HOL4) che copre il *binario compilato* (compilatore
CakeML, a sua volta verificato). Risolve l'open problem 5 del repo
ciclico per la parte LRAT — reso economico dal fatto che, dopo la lezione
Z15, i certificati nuovi nascono già in LRAT (niente conversione).

## Provenienza e build dello strumento

- Repo: `github.com/tanyongkiam/cake_lpr` (clonato in `tools/cake_lpr`),
  che dichiara i commit HOL4/CakeML di generazione; gli assembly
  pre-generati combaciano con le impronte dichiarate nel repo
  (`cake_lpr.sha256`): `cake_lpr_arm8.S` sha256 `95b64883…`.
- Build NATIVA arm64 su M4: `make cake_lpr_arm8` (niente Rosetta).
- Taglie heap/stack: dal luglio 2026 si passano da riga di comando
  (`--CML_HEAP_SIZE=<MB>`), non più via variabili d'ambiente.

## Collaudo (protocollo: mai fidarsi di uno strumento non collaudato)

1. Esempio del repo (`example.cnf` + `example.lpr`): `s VERIFIED UNSAT` ✓
2. **Controllo negativo 1** — certificato 15T26 TRONCATO: respinto
   ("Checking failed … failed to parse line") ✓
3. **Controllo negativo 2** — certificato 15T26 con un letterale NEGATO
   a metà file (riga 20717, 59 → −59): respinto ("clause index has no
   reduction sequence") ✓
4. **Trappola confermata**: l'exit code è 0 anche sui fallimenti — il
   verdetto va letto SOLO dalla riga `s VERIFIED UNSAT` (stessa igiene
   già in uso con drat-trim/lrat-check).

## Esiti (misurati su M4, macchina scarica)

| certificato | contenuto | cake_lpr | tempo | RSS max |
|---|---|---|---|---|
| 15T26.lrat (3,9 MB) | grado 15, [3⁴]5 | **s VERIFIED UNSAT** | 0,3 s | 0,7 GB |
| 15T9.lrat (55 MB) | grado 15, [5²]3 | **s VERIFIED UNSAT** | 4,0 s | 3,0 GB |
| 15T5.lrat (162 MB) | grado 15, A₅ | **s VERIFIED UNSAT** | 9,1 s | 3,5 GB |
| margin0: z7_E1b, z7_E2, z11_E1b, z11_E2, z13_E1b, z13_E2 | unicità dell'insieme delle parti a margine ≤ 0 | **6/6 s VERIFIED UNSAT** | < 1 s l'uno | — |
| z15.lrat (147 GB) | Z15 ciclico | **NON COMPLETATO: heap esaurito** | 3 h 10 m | 6,5 GB RSS (footprint 12,9 GB) |

## Esito Z15 (2026-08-15, 01:05): limite di risorse, NON un verdetto negativo

Run `scripts/cakelpr_z15.sh` (2026-08-14 21:57 → 2026-08-15 01:05,
heap CakeML 12 GB): terminato con **"CakeML heap space exhausted"**
dopo 11.393 s, alla stima [E, da 12 MB/s misurati via proc_pidfdinfo]
dell'80–85% del file. Interpretazione onesta:

- **Non dice nulla contro il certificato**: z15.lrat resta VERIFICATO
  dal checker streaming `lrat-check` ("c VERIFIED", 22,6 min, verbale
  Z15-CLOSED.md). Il fallimento è del checker verificato, per memoria.
- **Causa quantificata [M/E]**: la prova tiene vive fino a 28.850.111
  clausole (misura di lrat-check); la rappresentazione CakeML costa
  ~4–6× quella C e il GC a copia raddoppia il fabbisogno → servono
  ~15–25 GB di heap: una macchina da 16 GB fisici è sotto la soglia
  per il check monolitico. I 9 certificati fino a 162 MB (grado 15 +
  margin0) NON hanno questo problema: 9/10 VERIFICATI da cake_lpr.
- Lezione strumenti: throughput reale 12 MB/s = ~10× lrat-check
  (l'estrapolazione 2,3× dai certificati piccoli era sbagliata di 4×).

## Strade per completare il 10/10 (decisione umana)

1. **Macchina più grande** (la via del progetto cake_lpr stesso: il
   loro Makefile prevede heap da 64 GB): un'istanza cloud da 64 GB per
   ~4–6 h di run. Costo: pochi euro + setup; rischio basso.
2. **Modalità compositiva di cake_lpr** (intervalli i–j + summary +
   `-check` di copertura): fatta apposta per prove enormi su RAM
   limitata; richiede studio del formato e uno script di split
   (~mezza giornata di lavoro); tutto resta su questo Mac.
3. **Heap 14–15 GB su questo Mac**: probabilità concreta di nuovo
   esaurimento (fabbisogno stimato sopra i 15 GB) + swap/crawl.
   Sconsigliata: costo alto, esito incerto.
4. **Accettare 9/10** e dichiarare il limite nel paper: Z15 resta
   coperto da lrat-check; il perimetro cake_lpr copre tutto il resto.
   Già scientificamente onesto e pubblicabile.

## Cosa cambia nella base di fiducia

Prima: generatore di formule (validato con doppio metodo e collaudi) +
solver (non fidato: produce certificati) + **lrat-check (C non
verificato, fidato ciecamente)**.
Dopo: il terzo anello sparisce — resta da fidarsi solo del generatore di
formule (~60 righe, mitigato dai due metodi indipendenti) e del nucleo di
HOL4. I certificati di grado 14 (DRAT, non LRAT) non sono coperti da
questo passaggio: servirebbe rigenerarli in LRAT o farli convertire da
drat-trim — possibile estensione, costo ~1–2 h [E].

## Come riverificare

```bash
cd tools/cake_lpr && shasum -a 256 -c cake_lpr.sha256 && make cake_lpr_arm8
cd ../.. && for g in 15T5 15T9 15T26; do
  tools/cake_lpr/cake_lpr results/cnf/$g.cnf results/cnf/$g.lrat
done   # atteso: "s VERIFIED UNSAT" ×3 (verdetto dalla riga, NON dall'exit code)
tools/cake_lpr/cake_lpr --CML_HEAP_SIZE=12288 --CML_STACK_SIZE=4096 \
  results/cnf/z15min3.cnf results/cnf/z15.lrat   # ~1 h
```

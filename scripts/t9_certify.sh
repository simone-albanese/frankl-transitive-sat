#!/bin/bash
# t9_certify.sh — Metodo 2 + certificati per il teorema di grado 15 (T9).
# Per ciascuna delle tre istanze minime {15T26, 15T9, 15T5} (CNF congelati,
# sha256 in results/cnf/SHA256-15T-cnf.txt): cadical --lrat --no-binary
# (trappola nota: senza --no-binary lrat-check risponde NOT VERIFIED),
# poi lrat-check in streaming. MAI fidarsi del solo exit code: si cerca
# la riga VERIFIED nel log. Lancio consigliato (sganciato, sopravvive
# alla sessione):
#   nohup caffeinate -i bash scripts/t9_certify.sh >/dev/null 2>&1 &
#   echo $! > STATE/t9_certify.pid ; disown
cd "$(dirname "$0")/.." || exit 1
LOG=results/logs/t9_certify.log
{
echo "T9_CERTIFY_START $(date)"
for g in 15T26 15T9 15T5; do
  echo "=== $g solve $(date) ==="
  /usr/bin/time -l nice -n 10 tools/cadical/build/cadical --lrat --no-binary \
      "results/cnf/$g.cnf" "results/cnf/$g.lrat" \
      > "results/logs/t9_${g}_cadical.log" 2>&1
  ec=$?
  echo "$g CADICAL_EXIT=$ec (atteso 20=UNSAT)"
  if [ "$ec" -ne 20 ]; then
    echo "$g ESITO INATTESO ($ec): fermo la catena, log da leggere."
    osascript -e 'display notification "Grado 15: esito inatteso, serve un occhio" with title "Progetto Frankl"'
    exit 1
  fi
  echo "=== $g lrat-check $(date) ==="
  nice -n 10 tools/drat-trim/lrat-check \
      "results/cnf/$g.cnf" "results/cnf/$g.lrat" \
      > "results/logs/t9_${g}_lratcheck.log" 2>&1
  echo "$g LRATCHECK_EXIT=$?"
  grep -E "VERIFIED|NOT" "results/logs/t9_${g}_lratcheck.log"
  ls -la "results/cnf/$g.lrat"
done
shasum -a 256 results/cnf/15T26.lrat results/cnf/15T9.lrat results/cnf/15T5.lrat \
    > results/cnf/SHA256-15T-lrat.txt
echo "T9_CERTIFY_DONE $(date)"
osascript -e 'display notification "Certificazione grado 15 completata (3 istanze)" with title "Progetto Frankl"'
} >> "$LOG" 2>&1

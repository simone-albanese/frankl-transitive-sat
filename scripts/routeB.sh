#!/bin/bash
# routeB.sh — Route B su Z15: cadical --lrat SENZA cap di tempo + verifica
# streaming automatica a fine corsa. Progettato per girare SGANCIATO
# (nohup ... & disown): sopravvive ai cleanup di sessione; lo fermano solo
# la guardia (RAM/disco), un riavvio, o un kill esplicito.
# Uso: nohup bash scripts/routeB.sh > results/logs/routeB_driver.log 2>&1 & disown
cd "$(dirname "$0")/.." || exit 1
source STATE/hardware.env

CNF=results/cnf/z15min3.cnf          # sha256 e6c732cf... = formula pubblicata
PRF=results/cnf/z15.lrat             # prova LRAT testuale (streaming-checkable)
LOG=results/logs/routeB_z15.log
DISK_KILL_GB=30                       # sotto questa soglia la guardia ferma tutto

echo "ROUTE_B_START $(date) pid_driver=$$"
caffeinate -i nice -n 10 tools/cadical/build/cadical --lrat --no-binary \
    "$CNF" "$PRF" > "$LOG" 2>&1 &
PID=$!
echo "$PID" > STATE/routeB.pid
echo "solver_pid=$PID"

i=0
while kill -0 "$PID" 2>/dev/null; do
  RSS=$(ps -o rss= -p "$PID" | tr -d ' ')
  FREE=$(df -g . | tail -1 | awk '{print $4}')
  if [ "${RSS:-0}" -gt $(( RAM_JOB_MAX_GB * 1024 * 1024 )) ]; then
    echo "KILL_RAM rss_kb=$RSS $(date)"; kill -TERM "$PID"; break
  fi
  if [ "${FREE:-999}" -lt "$DISK_KILL_GB" ]; then
    echo "KILL_DISK free_gb=$FREE $(date)"; kill -TERM "$PID"; break
  fi
  i=$((i+1))
  if [ $(( i % 60 )) -eq 0 ]; then
    echo "HEARTBEAT $(date) rss_kb=${RSS} free_gb=${FREE} proof=$(du -h "$PRF" 2>/dev/null | cut -f1)"
  fi
  sleep 60
done
wait "$PID"; EX=$?
echo "ROUTE_B_SOLVER_EXIT=$EX $(date) proof=$(du -h "$PRF" 2>/dev/null | cut -f1)"

if [ "$EX" = "20" ]; then
  osascript -e 'display notification "Z15: UNSAT! Verifica del certificato in corso (ore)" with title "Progetto Frankl"'
  tools/drat-trim/lrat-check "$CNF" "$PRF" > results/logs/routeB_lratcheck.log 2>&1
  V=$(grep -c "^c VERIFIED" results/logs/routeB_lratcheck.log)
  echo "ROUTE_B_LRAT_VERIFIED=$V $(date)"
  if [ "$V" = "1" ]; then
    osascript -e 'display notification "Z15 CERTIFICATO VERIFICATO: open problem 1 CHIUSO" with title "Progetto Frankl"'
  else
    osascript -e 'display notification "ATTENZIONE: verifica LRAT non riuscita, servono controlli" with title "Progetto Frankl"'
  fi
elif [ "$EX" = "10" ]; then
  echo "ROUTE_B_SAT_CANDIDATE $(date)"
  osascript -e 'display notification "Z15: SAT?! Candidato controesempio — non toccare i file" with title "Progetto Frankl"'
else
  osascript -e 'display notification "Z15 Route B: run terminato senza verdetto (vedi log)" with title "Progetto Frankl"'
fi
echo "ROUTE_B_END $(date)"

#!/bin/bash
# cakelpr_z15.sh — riverifica del certificato Z15 (147 GB LRAT) col checker
# FORMALMENTE VERIFICATO cake_lpr (build arm64 nativa, tools/cake_lpr).
# Heap CakeML 12 GB (deviazione motivata dal cap 9 GB di hardware.env:
# macchina altrimenti scarica, run unico non spezzabile; guardia di
# sicurezza a 15 GB per evitare la spirale di swap). Trappola nota:
# l'exit code è inaffidabile — verdetto SOLO dalla riga "s VERIFIED UNSAT".
# Lancio: nohup caffeinate -i bash scripts/cakelpr_z15.sh >/dev/null 2>&1 &
#         echo $! > STATE/cakelpr_z15.pid ; disown
cd "$(dirname "$0")/.." || exit 1
LOG=results/logs/cakelpr_z15.log
OUT=results/logs/cakelpr_z15_checker.out
{
echo "CAKELPR_Z15_START $(date)"
nice -n 10 /usr/bin/time -l tools/cake_lpr/cake_lpr \
    --CML_HEAP_SIZE=12288 --CML_STACK_SIZE=4096 \
    results/cnf/z15min3.cnf results/cnf/z15.lrat > "$OUT" 2>&1 &
TPID=$!
# monitor RSS ogni 120 s + guardia 15 GB
while kill -0 "$TPID" 2>/dev/null; do
    CPID=$(pgrep -P "$TPID" -f cake_lpr | head -1)
    [ -z "$CPID" ] && CPID=$TPID
    RSS=$(ps -o rss= -p "$CPID" 2>/dev/null | tr -d ' ')
    echo "HEARTBEAT $(date '+%H:%M:%S') rss_kb=${RSS:-?}"
    if [ -n "$RSS" ] && [ "$RSS" -gt 15728640 ]; then
        echo "GUARDIA RAM: rss ${RSS}KB > 15GB, kill"
        kill -TERM "$CPID"; sleep 5; kill -KILL "$CPID" 2>/dev/null
        break
    fi
    sleep 120
done
wait "$TPID" 2>/dev/null
echo "--- output del checker + time -l ---"
cat "$OUT"
echo "CAKELPR_Z15_DONE $(date)"
if grep -q "s VERIFIED UNSAT" "$OUT"; then
    osascript -e 'display notification "cake_lpr: certificato Z15 VERIFICATO dal checker formalmente verificato" with title "Progetto Frankl"'
else
    osascript -e 'display notification "cake_lpr su Z15: NON verificato, guarda il log" with title "Progetto Frankl"'
fi
} >> "$LOG" 2>&1

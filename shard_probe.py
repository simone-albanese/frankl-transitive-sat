"""shard_probe.py — Sonda di sharding per Z15 (Route A, open problem 1 del
repo ciclico pubblicato).

Idea (correttezza in una riga): fissare k orbite in tutti i 2^k modi
partiziona lo spazio di ricerca; UNSAT su TUTTI gli shard ⟺ UNSAT globale.
La sonda ne decide solo alcuni estremi con cap di tempo, per PREZZARE la
campagna completa prima di lanciarla (regola "smart, not harder").

Selezione orbite (ricetta di docs/open-problems.md del repo ciclico):
le k con coefficiente di margine piu' negativo, a parita' orbita piu'
piccola, tra quelle con taglia >= 3 (le altre sono gia' forzate a 0 nel
modello min3). La numerazione delle variabili coincide con dump_dimacs.py
(stessa build_orbits, stesso ordine).

Uso:
  $PY shard_probe.py select 15 8
  $PY shard_probe.py make 15 8 <pattern01> results/cnf/z15min3.cnf <out.cnf>
"""
import sys, shutil
from sat_cyclic import canon_table, build_orbits


def select(m, k):
    tab = canon_table(m)
    reps, info, idx = build_orbits(m, tab)
    cand = []
    for i, (c, r, s) in enumerate(info):
        if s < 3:
            continue
        assert (2 * r * s) % m == 0
        d = (2 * r * s) // m - r
        cand.append((d, r, i + 1, c, s))  # var 1-based come nel DIMACS
    cand.sort()
    return cand[:k]


def make(m, k, pattern, base_path, out_path):
    assert len(pattern) == k and set(pattern) <= {"0", "1"}
    chosen = select(m, k)
    units = []
    for bit, (d, r, var, c, s) in zip(pattern, chosen):
        units.append(f"{var if bit == '1' else -var} 0")
    with open(base_path) as src, open(out_path, "w") as dst:
        header = src.readline().split()
        assert header[:2] == ["p", "cnf"]
        nv, ncl = int(header[2]), int(header[3])
        dst.write(f"p cnf {nv} {ncl + k}\n")
        dst.write("\n".join(units) + "\n")
        shutil.copyfileobj(src, dst)
    print(f"shard {pattern}: {out_path} (+{k} unit su base {ncl} clausole)")


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "select":
        m, k = int(sys.argv[2]), int(sys.argv[3])
        for d, r, var, c, s in select(m, k):
            print(f"var={var} rep={c} taglia_insieme={s} taglia_orbita={r} coeff={d}")
    elif mode == "make":
        m, k = int(sys.argv[2]), int(sys.argv[3])
        make(m, k, sys.argv[4], sys.argv[5], sys.argv[6])

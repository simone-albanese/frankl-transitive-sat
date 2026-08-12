"""dump_dimacs_group.py — DIMACS della formula 'controesempio G-invariante'.

Generalizza dump_dimacs.py: stesse identiche primitive PB (pb_adder) e stessa
struttura di clausole di sat_group (che riusa canon_table_group/build_orbits):
la formula esportata è per costruzione quella decisa in-process, per il doppio
check con solver esterno / certificato DRAT.
Coefficienti: d_O = r(2s-m)/m interi (lemma m | r·s), vincolo Σ d_O x_O ≤ -1.
Uso: "$PY" dump_dimacs_group.py <spec> <out.cnf> [min_size]
     spec = 'Z13' (ciclico) oppure etichetta census, es. '14T2'.
"""
import sys
from group_orbits import canon_table_group, build_orbits, cyclic_gens, load_group
from pb_adder import Pool, encode_signed_leq


def dump(m, gens, path, min_size=1, label="?"):
    tab = canon_table_group(m, gens)
    reps, info, idx = build_orbits(m, tab)
    n = len(reps)
    full = (1 << m) - 1
    members = {c: [] for c in reps}
    for x in range(1, full):
        members[tab[x]].append(x)
    d = []
    for (_, r, s) in info:
        assert (2 * r * s) % m == 0
        d.append((2 * r * s) // m - r)
    pool = Pool(n + 1)
    pb = encode_signed_leq({i + 1: d[i] for i in range(n) if d[i] != 0}, -1, pool)
    ncl = 0
    body = path + ".body"
    with open(body, "w") as f:
        if min_size > 1:
            for i in range(n):
                if info[i][2] < min_size:
                    f.write(f"{-(i+1)} 0\n"); ncl += 1
        for c in pb:
            f.write(" ".join(map(str, c)) + " 0\n"); ncl += 1
        f.write(" ".join(str(v) for v in range(1, n + 1)) + " 0\n"); ncl += 1
        for i in range(n):
            Ai = reps[i]
            for j in range(i, n):
                seen = set()
                for B in members[reps[j]]:
                    u = Ai | B
                    if u == full:
                        continue
                    t = idx[tab[u]]
                    if t == i or t == j or t in seen:
                        continue
                    seen.add(t)
                    f.write(f"{-(i+1)} {-(j+1)} {t+1} 0\n"); ncl += 1
    with open(path, "w") as f:
        f.write(f"p cnf {pool.next - 1} {ncl}\n")
    import subprocess
    subprocess.run(f"cat {body} >> {path} && rm {body}", shell=True, check=True)
    print(f"DIMACS: {path}  vars={pool.next - 1}  clauses={ncl}  ({label}, m={m}, min_size={min_size})")


if __name__ == "__main__":
    spec = sys.argv[1]; out = sys.argv[2]
    ms = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    if spec.upper().startswith("Z"):
        m = int(spec[1:]); gens = cyclic_gens(m); label = f"Z_{m}"
    else:
        m, gens = load_group(spec); label = spec
    dump(m, gens, out, ms, label)

"""dump_opb.py — Scrive in OPB (pseudo-booleano nativo) la formula
'famiglia Z_m-invariante con margine <= rhs'.

Differenza chiave rispetto a dump_dimacs.py: il vincolo di margine
Σ d_i x_i <= rhs viene dato NATIVO al solver PB (niente adder binario,
niente variabili ausiliarie). Le clausole diventano vincoli lineari:
clausola con positivi P e negati N  ⟺  Σ_P x - Σ_N x >= 1 - |N|.

Riusa ESATTAMENTE canon_table/build_orbits della pipeline validata.
Convenzioni identiche: ∅ e full impliciti (si cancellano nel margine);
non-vuotezza Σx >= 1; d_i = r_i(2s_i - m)/m interi (lemma m | r*s).

VALIDAZIONE OBBLIGATORIA (protocollo): il solver PB su questi OPB deve
riprodurre UNSAT su Z_7 e Z_11 (rhs=-1) prima che un esito nuovo conti.

Uso: $PY dump_opb.py <m> <out.opb> [rhs=-1] [min_size=1] [exclude_full]
"""
import sys
from ucs_core import rot
from sat_cyclic import canon_table, build_orbits


def dump(m, path, rhs=-1, min_size=1, exclude_full=False):
    tab = canon_table(m)
    reps, info, idx = build_orbits(m, tab)
    n = len(reps)
    full = (1 << m) - 1
    orbit_sets = [sorted({rot(c, k, m) for k in range(m)}) for c, _, _ in info]
    d = []
    for (_, r, s) in info:
        assert (2 * r * s) % m == 0
        d.append((2 * r * s) // m - r)
    ncon = 0
    body = path + ".body"
    with open(body, "w") as f:
        # margine: Σ d x <= rhs  ⟺  Σ (-d) x >= -rhs
        f.write(" ".join(f"{-d[i]:+d} x{i+1}" for i in range(n) if d[i] != 0)
                + f" >= {-rhs} ;\n"); ncon += 1
        # non-vuotezza
        f.write(" ".join(f"+1 x{v}" for v in range(1, n + 1)) + " >= 1 ;\n"); ncon += 1
        if exclude_full:
            # almeno un'orbita esclusa: Σ -x >= 1 - n
            f.write(" ".join(f"-1 x{v}" for v in range(1, n + 1))
                    + f" >= {1 - n} ;\n"); ncon += 1
        if min_size > 1:
            for i in range(n):
                if info[i][2] < min_size:
                    f.write(f"+1 x{i+1} = 0 ;\n"); ncon += 1
        # chiusura: ¬xi ∨ ¬xj ∨ xt  ⟺  -xi -xj +xt >= -1
        for i in range(n):
            Ai = reps[i]
            for j in range(i, n):
                seen = set()
                for B in orbit_sets[j]:
                    u = Ai | B
                    if u == full:
                        continue
                    t = idx[tab[u]]
                    if t == i or t == j or t in seen:
                        continue
                    seen.add(t)
                    f.write(f"-1 x{i+1} -1 x{j+1} +1 x{t+1} >= -1 ;\n"); ncon += 1
    import os, shutil
    with open(path, "w") as f:
        f.write(f"* #variable= {n} #constraint= {ncon}\n")
        with open(body) as src:
            shutil.copyfileobj(src, f)
    os.remove(body)
    print(f"OPB: {path} vars={n} constraints={ncon} "
          f"(m={m}, rhs={rhs}, min_size={min_size}, excl_full={exclude_full})")


if __name__ == "__main__":
    m = int(sys.argv[1]); out = sys.argv[2]
    rhs = int(sys.argv[3]) if len(sys.argv) > 3 else -1
    ms = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    excl = len(sys.argv) > 5 and sys.argv[5] == "exclude_full"
    dump(m, out, rhs, ms, excl)

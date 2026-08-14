"""margin_zero.py — Esperimento 'margine 0': famiglie cicliche estremali.

Domanda (nata dal pattern osservato: l'insieme delle parti tocca esattamente
la soglia della congettura, margine 0): oltre all'insieme delle parti,
esistono famiglie union-closed Z_m-invarianti non banali con margine <= 0?

Esperimenti per ogni m:
  E1a (sanity, min_size=1):  margine<=0            -> atteso FEASIBLE (parti).
  E1b (unicita', min_size=1): margine<=0 + ALMENO un'orbita esclusa
                              -> INFEASIBLE = l'insieme delle parti e' UNICO.
  E2  (min_size=3):           margine<=0            -> estremali nel mondo min-3?

Convenzioni ereditate da sat_cyclic.py (pipeline validata, riusata SENZA
riscrivere): ∅ e full sempre inclusi (si cancellano nel margine); margine
scalato m*M = Σ r(2s-m) x  (interi); clausola Σx>=1 esclude {∅, Z_m}.

VALIDAZIONE OBBLIGATORIA: `validate` riproduce con rhs=-1 gli esiti
certificati INFEASIBLE su Z_7 e Z_11 PRIMA che gli esiti nuovi contino.

Uso:
  $PY margin_zero.py validate
  $PY margin_zero.py run <m> [time_cap_s]
  $PY margin_zero.py dump <m> <out.cnf> <margin_rhs> <min_size> [exclude_full]
"""
import sys, time, json
from ortools.sat.python import cp_model
from ucs_core import rot, popcount, check_family, family_to_sets
from checker2 import verify
from sat_cyclic import canon_table, build_orbits, build_clauses
from pb_adder import Pool, encode_signed_leq


def solve_cpsat(m, margin_rhs, min_size=1, exclude_full=False, time_cap=300.0):
    """Decide: esiste famiglia con margine intero M <= margin_rhs?
    (vincolo scalato: Σ r(2s-m) x <= m*margin_rhs)."""
    tab = canon_table(m)
    reps, info, idx = build_orbits(m, tab)
    n = len(reps)
    clauses, _ = build_clauses(m, tab, reps, info, idx)
    model = cp_model.CpModel()
    x = [model.NewBoolVar(f"x{i}") for i in range(n)]
    if min_size > 1:
        for i, (_, r, s) in enumerate(info):
            if s < min_size:
                model.Add(x[i] == 0)
    for i, j, t in clauses:
        model.AddBoolOr([x[i].Not(), x[j].Not(), x[t]])
    coeff = [r * (2 * s - m) for (_, r, s) in info]
    model.Add(sum(c * xi for c, xi in zip(coeff, x)) <= m * margin_rhs)
    model.Add(sum(x) >= 1)  # esclude la famiglia banale {∅, Z_m}
    if exclude_full:
        # famiglia diversa dall'insieme delle parti: almeno un'orbita esclusa
        model.AddBoolOr([xi.Not() for xi in x])
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_cap
    solver.parameters.num_search_workers = 4
    st = solver.Solve(model)
    out = {"m": m, "status": solver.StatusName(st), "margin_rhs": margin_rhs,
           "min_size": min_size, "exclude_full": exclude_full, "n_orbits": n}
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        chosen = [i for i in range(n) if solver.Value(x[i])]
        out["chosen_reps"] = [reps[i] for i in chosen]
        out["scaled_margin"] = sum(coeff[i] for i in chosen)
        out["n_chosen"] = len(chosen)
    return out


def verify_witness(m, chosen_reps):
    """Ricostruisce la famiglia dal testimone e la verifica con ENTRAMBI i
    checker indipendenti (interi). Ritorna il rapporto concordato."""
    fam = {0, (1 << m) - 1}
    for c in chosen_reps:
        fam |= {rot(c, k, m) for k in range(m)}
    r1 = check_family(fam, m)
    r2 = verify(family_to_sets(fam, m))
    assert r1["closed"] and r2["closed"], "testimone NON chiuso: bug!"
    assert r1["margin"] == r2["margin"], "checker in disaccordo: bug!"
    sizes = sorted(popcount(a) for a in fam)
    return {"F": r1["F"], "margin": r1["margin"], "maxf": r1["maxf"],
            "sizes_min_max": (sizes[1], sizes[-2]) if len(sizes) > 2 else None,
            "closed_both": True}


def dump_cnf(m, path, margin_rhs, min_size=1, exclude_full=False):
    """DIMACS del problema (secondo metodo: cadical). Coefficienti NON scalati
    d = r(2s-m)/m (interi per il lemma m | r*s), rhs = margin_rhs."""
    tab = canon_table(m)
    reps, info, idx = build_orbits(m, tab)
    n = len(reps)
    full = (1 << m) - 1
    orbit_sets = [sorted({rot(c, k, m) for k in range(m)}) for c, _, _ in info]
    d = []
    for (_, r, s) in info:
        assert (2 * r * s) % m == 0
        d.append((2 * r * s) // m - r)
    pool = Pool(n + 1)
    pb = encode_signed_leq({i + 1: d[i] for i in range(n) if d[i] != 0},
                           margin_rhs, pool)
    lines = []
    if min_size > 1:
        for i in range(n):
            if info[i][2] < min_size:
                lines.append(f"{-(i+1)} 0")
    for c in pb:
        lines.append(" ".join(map(str, c)) + " 0")
    lines.append(" ".join(str(v) for v in range(1, n + 1)) + " 0")
    if exclude_full:
        lines.append(" ".join(str(-v) for v in range(1, n + 1)) + " 0")
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
                lines.append(f"{-(i+1)} {-(j+1)} {t+1} 0")
    with open(path, "w") as f:
        f.write(f"p cnf {pool.next - 1} {len(lines)}\n")
        f.write("\n".join(lines) + "\n")
    print(f"DIMACS: {path} vars={pool.next-1} clauses={len(lines)} "
          f"(m={m}, rhs={margin_rhs}, min_size={min_size}, excl_full={exclude_full})")


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "validate":
        # DEVE riprodurre gli esiti certificati (margine <= -1 impossibile)
        for mm in (7, 11):
            t0 = time.time()
            r = solve_cpsat(mm, margin_rhs=-1, time_cap=120)
            print(f"VALIDAZIONE Z_{mm} rhs=-1 (atteso INFEASIBLE): "
                  f"{r['status']} [{time.time()-t0:.1f}s]")
            assert r["status"] == "INFEASIBLE", f"BUG pipeline margin_zero su Z_{mm}"
        print("[OK] margin_zero riproduce i risultati certificati: pipeline valida")
    elif mode == "run":
        m = int(sys.argv[2])
        cap = float(sys.argv[3]) if len(sys.argv) > 3 else 300.0
        report = {}
        for label, ms, excl in (("E1a", 1, False), ("E1b", 1, True), ("E2", 3, False)):
            t0 = time.time()
            r = solve_cpsat(m, margin_rhs=0, min_size=ms, exclude_full=excl,
                            time_cap=cap)
            dt = time.time() - t0
            line = f"{label} Z_{m} min_size={ms} excl_full={excl}: {r['status']} [{dt:.1f}s]"
            if "chosen_reps" in r:
                w = verify_witness(m, r["chosen_reps"])
                r["witness_check"] = w
                line += (f"  testimone: |F|={w['F']} margine={w['margin']} "
                         f"orbite={r['n_chosen']}/{r['n_orbits']}")
            print(line)
            report[label] = r
        print("JSON:" + json.dumps(report))
    elif mode == "dump":
        m = int(sys.argv[2]); out = sys.argv[3]
        rhs = int(sys.argv[4]); ms = int(sys.argv[5])
        excl = len(sys.argv) > 6 and sys.argv[6] == "exclude_full"
        dump_cnf(m, out, rhs, ms, excl)

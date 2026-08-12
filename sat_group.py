"""sat_group.py — Decisione esatta: esiste un controesempio G-invariante?
Generalizza sat_cyclic.py a un gruppo transitivo G ≤ S_m arbitrario dato per
generatori (da STATE/census14.json). NON modifica i moduli ciclici.

Modello. Una famiglia union-closed G-invariante è unione di orbite di
sottoinsiemi; WLOG contiene ∅ e (se non banale) l'universo: se un'orbita non
vuota O è inclusa, l'unione dei suoi elementi è G-invariante e non vuota,
quindi (G transitivo) è tutto [m], e la chiusura per unione la contiene.
Variabile x_O per ogni orbita non banale O = (rep c, r_O elementi, taglia s_O).

Conteggi (∅ e full inclusi): |F| = 2 + Σ r_O x_O; per transitività ogni punto
ha la stessa frequenza f = 1 + (Σ r_O s_O x_O)/m. Margine scalato (intero,
lemma m | r_O·s_O in group_orbits):
  m·M = m(2f - |F|) = Σ r_O (2 s_O - m) x_O ;  controesempio ⟺ m·M ≤ -m.

Chiusura con rappresentante fisso — vale per QUALSIASI gruppo G, non solo
ciclico: per ogni coppia di orbite (O1, O2) basta fissare A = rep(O1) e far
variare B su tutta O2. Infatti una coppia generica (A', B') con A' ∈ O1,
B' ∈ O2 si scrive A' = g(A) per qualche g ∈ G, e allora
A' ∪ B' = g(A ∪ g⁻¹(B')) con g⁻¹(B') ∈ O2: quindi orb(A' ∪ B') = orb(A ∪ B)
per un opportuno B ∈ O2, e le clausole ¬x1 ∨ ¬x2 ∨ x_{orb(A∪B)} (B ∈ O2)
impongono già la chiusura su tutte le coppie. Il caso j = i (O1 = O2) è
incluso nel loop.

CONTROLLI PIPELINE (T4): su gens ciclici Z_7/Z_11/Z_13 deve riprodurre gli
esiti della pipeline ciclica validata (INFEASIBLE) prima di ogni run di
produzione sui gruppi del census.
"""
import sys, time
from ortools.sat.python import cp_model
from group_orbits import canon_table_group, build_orbits, cyclic_gens, load_group


def build_clauses(m, tab, reps, info, idx):
    full = (1 << m) - 1
    n = len(reps)
    # orbite come liste, una scansione unica della tabella
    members = {c: [] for c in reps}
    for x in range(1, full):
        members[tab[x]].append(x)
    clauses = []  # (i, j, t) -> ¬xi ∨ ¬xj ∨ xt
    t0 = time.time()
    for i in range(n):
        A = reps[i]
        for j in range(i, n):
            targets = set()
            for B in members[reps[j]]:
                u = A | B
                if u == full:
                    continue
                targets.add(tab[u])
            targets.discard(reps[i])
            targets.discard(reps[j])
            for cu in targets:
                clauses.append((i, j, idx[cu]))
    return clauses, time.time() - t0


def solve(m, gens, mode="decide", time_cap=120, verbose=True, min_set_size=1,
          label="?"):
    tab = canon_table_group(m, gens)
    reps, info, idx = build_orbits(m, tab)
    n = len(reps)
    clauses, tb = build_clauses(m, tab, reps, info, idx)
    if verbose:
        print(f"  {label}: {n} orbite non banali, {len(clauses)} clausole di chiusura (build {tb:.1f}s)")
    model = cp_model.CpModel()
    x = [model.NewBoolVar(f"x{i}") for i in range(n)]
    if min_set_size > 1:
        for i, (_, r, s) in enumerate(info):
            if s < min_set_size:
                model.Add(x[i] == 0)
    for i, j, t in clauses:
        model.AddBoolOr([x[i].Not(), x[j].Not(), x[t]])
    coeff = [r * (2 * s - m) for (_, r, s) in info]
    expr = sum(c * xi for c, xi in zip(coeff, x))
    model.Add(sum(x) >= 1)  # esclude la famiglia banale {∅, [m]}
    if mode == "decide":
        model.Add(expr <= -m)  # M <= -1
    else:
        obj = model.NewIntVar(-sum(abs(c) for c in coeff), sum(abs(c) for c in coeff), "M")
        model.Add(obj == expr)
        model.Minimize(obj)
    if mode == "probe":
        # build-only: conteggi + picco RSS del processo, nessun solve
        import resource
        rss_gb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2**30
        return {"status": "PROBE", "m": m, "label": label, "n_orbits": n,
                "n_clauses": len(clauses), "build_s": round(tb, 1),
                "rss_gb": round(rss_gb, 2)}
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_cap
    solver.parameters.num_search_workers = 4
    st = solver.Solve(model)
    name = solver.StatusName(st)
    out = {"status": name, "m": m, "label": label, "n_orbits": n,
           "n_clauses": len(clauses)}
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        chosen = [i for i in range(n) if solver.Value(x[i])]
        out["chosen_reps"] = [reps[i] for i in chosen]
        out["scaled_margin"] = sum(coeff[i] for i in chosen)
        out["F"] = 2 + sum(info[i][1] for i in chosen)
    return out


def _target(spec):
    """'Z13' -> ciclico; '14T2' -> dal census."""
    if spec.upper().startswith("Z"):
        m = int(spec[1:])
        return m, cyclic_gens(m), f"Z_{m}"
    m, gens = load_group(spec)
    return m, gens, spec


if __name__ == "__main__":
    spec = sys.argv[1] if len(sys.argv) > 1 else "Z7"
    mode = sys.argv[2] if len(sys.argv) > 2 else "decide"
    cap = float(sys.argv[3]) if len(sys.argv) > 3 else 120
    mss = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    m, gens, label = _target(spec)
    t0 = time.time()
    r = solve(m, gens, mode, time_cap=cap, min_set_size=mss, label=label)
    print(f"  {label} mode={mode} min_size={mss}: {r['status']}  [{time.time()-t0:.1f}s]")
    if r["status"] == "PROBE":
        print(f"  probe: {r['n_orbits']} orbite, {r['n_clauses']} clausole, "
              f"build {r['build_s']}s, RSS {r['rss_gb']} GB")
    if r["status"] in ("FEASIBLE", "OPTIMAL"):
        if mode == "decide":
            print("  !!! CANDIDATO TROVATO (da verificare coi due checker):", r)
        else:
            print(f"  margine minimo m*M = {r['scaled_margin']}  |F| = {r['F']}")
            print(f"  orbite scelte: {len(r['chosen_reps'])}  rep: {r['chosen_reps'][:20]}")

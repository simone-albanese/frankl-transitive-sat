#!/usr/bin/env python3
"""Scan dei 26 gruppi transitivi di grado 14 senza 14-ciclo.

Per ogni gruppo: orbite di P([14]) via Burnside (se enumerabile), e
minimalita' transitiva: certificato esaustivo (docs/notes-minimality.md,
criterio ⟨a_i,x⟩) per i piccoli, testimone di sottogruppo transitivo
proprio per i grandi, costruzione esplicita per 14T59 e 14T62=A14.

Output: results/minimality_scan.json ; log su stdout (redirigere).
"""
import json, sys, time
from itertools import combinations

N = 14
CENSUS = 'STATE/census14.json'
OUT = 'results/minimality_scan.json'
ENUM_CAP = 400_000     # enumerazione completa sotto questa taglia
CERT_CAP = 1500        # certificato esaustivo di minimalita' fino a qui
SAMPLE_X = 300         # x campionati (deterministici) per rep nei grandi
BIG_CLOSURE_CAP = 20_000

ID = tuple(range(N))

def compose(p, q):          # (p*q)(i) = p[q[i]]  (prima q, poi p)
    return tuple(p[q[i]] for i in range(N))

def inverse(p):
    r = [0]*N
    for i, v in enumerate(p):
        r[v] = i
    return tuple(r)

def n_cycles(p):
    seen = [False]*N; c = 0
    for i in range(N):
        if not seen[i]:
            c += 1; j = i
            while not seen[j]:
                seen[j] = True; j = p[j]
    return c

def is_even(p):
    return (N - n_cycles(p)) % 2 == 0

def cycle_type(p):
    seen = [False]*N; t = []
    for i in range(N):
        if not seen[i]:
            l = 0; j = i
            while not seen[j]:
                seen[j] = True; j = p[j]; l += 1
            t.append(l)
    return tuple(sorted(t, reverse=True))

def is_order7(p):
    t = cycle_type(p)
    return set(t) <= {7, 1} and 7 in t

def closure(gens, cap=None):
    """BFS deterministica. Se cap e |chiusura| > cap: ritorna None."""
    seen = {ID}; frontier = [ID]; out = [ID]
    while frontier:
        nf = []
        for p in frontier:
            for g in gens:
                q = compose(g, p)
                if q not in seen:
                    seen.add(q); nf.append(q); out.append(q)
                    if cap is not None and len(seen) > cap:
                        return None
        frontier = nf
    return out

def is_transitive(gens):
    seen = {0}; st = [0]
    while st:
        i = st.pop()
        for g in gens:
            j = g[i]
            if j not in seen:
                seen.add(j); st.append(j)
    return len(seen) == N

def order7_class_reps(G, sevens):
    reps = []
    remaining = set(sevens)
    while remaining:
        a = next(iter(remaining)); reps.append(a)
        for g in G:
            remaining.discard(compose(compose(g, a), inverse(g)))
    return reps

def find_witness(G, order, reps, xs, cap):
    """Cerca ⟨a,x⟩ transitivo proprio. Ritorna dict o None."""
    for a in reps:
        for x in xs:
            if not is_transitive([a, x]):
                continue
            H = closure([a, x], cap=cap)
            if H is not None and len(H) < order:
                return {'gens': [list(a), list(x)], 'sub_order': len(H)}
    return None

def scan_group(grp):
    t0 = time.time()
    t, order = grp['t'], grp['order']
    gens = [tuple(g) for g in grp['gens']]
    rec = {'t': t, 'label': grp['label'], 'order': order, 'name': grp['name']}
    print(f"--- 14T{t} ordine {order} ({grp['name']})", flush=True)

    if order > ENUM_CAP:
        rec.update(big_group(grp, gens))
        print(f"    [{time.time()-t0:.1f}s] {rec.get('status')}", flush=True)
        return rec

    G = closure(gens)
    assert len(G) == order, (t, len(G), order)

    s = sum(2**n_cycles(p) for p in G)
    assert s % order == 0, (t, 'Burnside non intero')
    rec['orbits_burnside'] = s // order

    sevens = [p for p in G if is_order7(p)]
    fpf_all = all(cycle_type(p) == (7, 7) for p in sevens)
    rec['n_order7'] = len(sevens)
    rec['order7_all_fpf'] = fpf_all
    reps = order7_class_reps(G, sevens)
    rec['n_order7_classes'] = len(reps)

    if order <= CERT_CAP and fpf_all:
        w = find_witness(G, order, reps, G, cap=order // 2)
        if w is None:
            rec['status'] = 'MINIMAL_CERTIFIED'
        else:
            rec['status'] = 'NOT_MINIMAL'; rec['witness'] = w
    else:
        step = max(1, len(G) // SAMPLE_X)
        xs = G[1::step]
        w = find_witness(G, order, reps, xs,
                         cap=min(order // 2, BIG_CLOSURE_CAP))
        if w is None:
            rec['status'] = 'UNKNOWN'   # campione senza esito: follow-up
        else:
            rec['status'] = 'NOT_MINIMAL'; rec['witness'] = w
    if not fpf_all and order <= CERT_CAP:
        rec['note'] = '7-elementi con punti fissi: certificato L4 non valido'
    print(f"    [{time.time()-t0:.1f}s] {rec['status']} "
          f"orbite={rec['orbits_burnside']}", flush=True)
    return rec

def big_group(grp, gens):
    """14T59 (=(S7wrS2)∩A14, ordine LMFDB) e 14T62=A14: testimoni espliciti."""
    t, order = grp['t'], grp['order']
    if t == 62:
        assert order * 2 == 87178291200, order  # 14!
        assert all(is_even(g) for g in gens), 'A14: gen dispari?'
        census = json.load(open(CENSUS))
        e30 = next(x for x in census if x['t'] == 30)
        g30 = [tuple(g) for g in e30['gens']]
        assert all(is_even(g) for g in g30), '14T30 non ⊆ A14?'
        assert is_transitive(g30)
        H = closure(g30)
        assert len(H) == 1092, len(H)
        return {'status': 'NOT_MINIMAL',
                'witness': {'gens': [list(g) for g in g30],
                            'sub_order': 1092, 'note': '14T30=PSL(2,13)⊆A14'},
                'basis': 'gens census, tutti pari; chiusura verificata =1092'}
    if t == 59:
        # trova la partizione in 2 blocchi da 7 preservata dai generatori
        blocks = None
        for rest in combinations(range(1, N), 6):
            B = frozenset((0,) + rest); C = frozenset(range(N)) - B
            if all(frozenset(g[i] for i in B) in (B, C) for g in gens):
                blocks = (sorted(B), sorted(C)); break
        assert blocks, '14T59: nessun sistema di blocchi 7+7 trovato'
        assert all(is_even(g) for g in gens), '14T59: gen dispari?'
        assert order == 25401600, order   # |S7wrS2|/2: G ≤ E e |G|=|E| ⇒ G=E
        B, C = blocks
        a = [0]*N                          # 7-ciclo su B × 7-ciclo su C
        for i in range(7):
            a[B[i]] = B[(i+1) % 7]; a[C[i]] = C[(i+1) % 7]
        a = tuple(a)
        # x = (swap B_i<->C_i) ∘ (moltiplicatore dispari su B): resta dentro
        # (F42≀2)∩A14, quindi ⟨a,x⟩ ha ordine ≤ 3528 — proprio per forza.
        x = None
        for k in (3, 5, 6):                # μ_k dispari su 7 punti
            cand = [0]*N
            for i in range(7):
                cand[B[i]] = C[(k*i) % 7]; cand[C[i]] = B[i]
            cand = tuple(cand)
            if is_even(cand):
                x = cand; break
        assert x is not None, '14T59: nessun x pari trovato'
        assert cycle_type(a) == (7, 7) and is_even(a)
        for g in (a, x):
            assert frozenset(g[i] for i in B) in (frozenset(B), frozenset(C))
        assert is_transitive([a, x])
        H = closure([a, x], cap=10_000)
        assert H is not None and len(H) < order
        return {'status': 'NOT_MINIMAL',
                'witness': {'gens': [list(a), list(x)], 'sub_order': len(H)},
                'blocks': blocks,
                'basis': ('gens pari e preservano i blocchi ⇒ G ≤ (S7≀S2)∩A14;'
                          ' |G|=25401600=|(S7≀S2)∩A14| (LMFDB) ⇒ uguali;'
                          ' testimone costruito dentro, chiusura propria')}
    raise AssertionError(f'gruppo grande inatteso 14T{t}')

def main():
    census = json.load(open(CENSUS))
    todo = sorted([g for g in census if not g['has_14_cycle']],
                  key=lambda g: g['order'])
    print(f"{len(todo)} gruppi senza 14-ciclo", flush=True)
    results = []
    for g in todo:
        results.append(scan_group(g))
        json.dump(results, open(OUT + '.partial', 'w'))  # checkpoint

    # sanity dalla nota
    d7 = next(r for r in results if r['t'] == 2)
    psl = next(r for r in results if r['t'] == 30)
    assert d7['orbits_burnside'] == 1236, d7
    assert psl['orbits_burnside'] == 52, psl
    assert d7['status'] == 'MINIMAL_CERTIFIED', d7

    minimal = [r for r in results if r['status'] == 'MINIMAL_CERTIFIED']
    unknown = [r for r in results if r['status'] == 'UNKNOWN']
    summary = {
        'minimal_certified': [r['t'] for r in minimal],
        'unknown': [r['t'] for r in unknown],
        'not_minimal': [r['t'] for r in results
                        if r['status'] == 'NOT_MINIMAL'],
    }
    json.dump({'summary': summary, 'groups': results},
              open(OUT, 'w'), indent=1)
    print('\n=== SOMMARIO ===')
    print('MINIMALI CERTIFICATI:',
          [(r['t'], r['order'], r['orbits_burnside']) for r in minimal])
    print('UNKNOWN (follow-up):',
          [(r['t'], r['order']) for r in unknown])
    print('NOT_MINIMAL:', summary['not_minimal'])
    print('scritto', OUT, flush=True)

if __name__ == '__main__':
    main()

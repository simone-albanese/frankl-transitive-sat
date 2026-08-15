#!/usr/bin/env python3
"""Scan dei 26 gruppi transitivi di grado 15 senza 15-ciclo (T9.2).

Per ogni gruppo: enumerazione completa (max ordine 19440), orbite di
P([15]) via Burnside, e riduzione di minimalita' su TRE livelli di rigore:

1. MINIMAL_ARITH — certificato aritmetico: un sottogruppo transitivo
   proprio H avrebbe 15 | |H| (orbita-stabilizzatore), |H| divisore di
   |G|, H senza 15-ciclo (il ciclo starebbe in G), e H coniugato a una
   voce del census (completezza della libreria transitiva). Inoltre
   |H| = 15 e' impossibile (transitivo di ordine 15 = regolare = C15 =
   ha il 15-ciclo) e |H| = 30 pure (ogni gruppo di ordine 30 contiene
   C15; il suo intersecare uno stabilizzatore di ordine 2 e' banale,
   quindi C15 agirebbe regolarmente: 15-ciclo). Se nessun ordine del
   census senza-ciclo divide propriamente |G|: minimale certificato.
2. NOT_MINIMAL con testimone LETTERALE: i generatori della libreria sono
   incrementali, quindi spesso una voce piu' piccola del census e'
   sottoinsieme letterale di G (test di appartenenza, poi verifica
   transitivita' + ordine proprio).
3. NOT_MINIMAL con testimone ⟨a,x⟩ o ⟨a,x,y⟩: sweep sui rappresentanti
   di classe degli elementi di ordine 5 e 3 (pre-filtro O(15) sulla
   partizione in orbite, chiusura BFS solo sui candidati transitivi,
   cap |G|/2: per Lagrange oltre meta' ⇒ tutto G).

Chi resta senza certificato ne' testimone: NO_WITNESS_FOUND — entra
nella lista-istanze per prudenza (soprainsieme di MIN: sempre corretto,
pattern 14T12 di docs/notes-minimality.md).

Output: results/minimality15_scan.json ; log su stdout (redirigere).
"""
import json, time
from itertools import islice

N = 15
CENSUS = 'STATE/census15.json'
OUT = 'results/minimality15_scan.json'
PAIR_SAMPLES = 150          # campioni per classe-coppia nel tentativo 3-gen

ID = tuple(range(N))

def compose(p, q):          # (p*q)(i) = p[q[i]]
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

def perm_order(p):
    q, k = p, 1
    while q != ID:
        q = compose(q, p); k += 1
    return k

def closure(gens, cap=None):
    seen = {ID}; frontier = [ID]
    while frontier:
        nf = []
        for p in frontier:
            for g in gens:
                q = compose(g, p)
                if q not in seen:
                    seen.add(q); nf.append(q)
                    if cap is not None and len(seen) > cap:
                        return None
        frontier = nf
    return seen

def orbit_partition(perms):
    """Componenti connesse del grafo i -> p(i): frozenset di frozenset."""
    parent = list(range(N))
    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]; i = parent[i]
        return i
    for p in perms:
        for i in range(N):
            a, b = find(i), find(p[i])
            if a != b:
                parent[a] = b
    blocks = {}
    for i in range(N):
        blocks.setdefault(find(i), []).append(i)
    return frozenset(frozenset(b) for b in blocks.values())

def is_transitive(perms):
    return len(orbit_partition(perms)) == 1

def class_reps(G_list, elems):
    """Rappresentanti delle classi di G-coniugio (G completo in lista)."""
    reps, remaining = [], set(elems)
    while remaining:
        a = next(iter(remaining)); reps.append(a)
        for g in G_list:
            remaining.discard(compose(compose(g, a), inverse(g)))
    return reps

def proper_or_none(gens, order):
    """Chiusura con cap |G|//2: sopra il cap, per Lagrange, e' tutto G."""
    H = closure(gens, cap=order // 2)
    return H if H is not None and len(H) < order else None


def scan_group(grp, nc_orders, census_by_order, G_sets_cache):
    t0 = time.time()
    t, order, name = grp['t'], grp['order'], grp['name']
    gens = [tuple(g) for g in grp['gens']]
    rec = {'t': t, 'label': grp['label'], 'order': order, 'name': name}
    print(f"--- 15T{t} ordine {order} ({name})", flush=True)

    G = closure(gens)
    assert len(G) == order, (t, len(G), order)
    G_list = list(G)
    G_sets_cache[t] = G

    s = sum(2**n_cycles(p) for p in G)
    assert s % order == 0, (t, 'Burnside non intero')
    rec['orbits_burnside'] = s // order

    # livello 1: certificato aritmetico
    cand = sorted({o for o in nc_orders if o < order and order % o == 0})
    rec['divisor_candidates'] = cand
    if not cand:
        rec['status'] = 'MINIMAL_ARITH'
        rec['basis'] = ('nessun ordine del census senza-ciclo divide '
                        'propriamente |G|; ordini 15 e 30 esclusi dal lemma C15')
        print(f"    [{time.time()-t0:.1f}s] MINIMAL_ARITH "
              f"orbite={rec['orbits_burnside']}", flush=True)
        return rec

    # livello 2: testimone letterale dal census
    for o in cand:
        for k in census_by_order.get(o, []):
            kg = [tuple(g) for g in k['gens']]
            if all(g in G for g in kg) and is_transitive(kg):
                H = closure(kg)
                assert len(H) == k['order'] < order
                rec['status'] = 'NOT_MINIMAL'
                rec['witness'] = {'literal_census': k['label'],
                                  'sub_order': len(H),
                                  'gens': [list(g) for g in kg]}
                print(f"    [{time.time()-t0:.1f}s] NOT_MINIMAL "
                      f"(letterale: {k['label']} ordine {len(H)}) "
                      f"orbite={rec['orbits_burnside']}", flush=True)
                return rec

    # livello 3: sweep ⟨a,x⟩ sui rappresentanti di ordine 5 e 3
    fives = [p for p in G_list if perm_order(p) == 5]
    threes = [p for p in G_list if perm_order(p) == 3]
    reps = class_reps(G_list, fives) + class_reps(G_list, threes)
    rec['n_reps_5_3'] = len(reps)
    for a in reps:
        for x in G_list:
            if len(orbit_partition([a, x])) != 1:
                continue
            H = proper_or_none([a, x], order)
            if H is not None:
                rec['status'] = 'NOT_MINIMAL'
                rec['witness'] = {'gens': [list(a), list(x)],
                                  'sub_order': len(H)}
                print(f"    [{time.time()-t0:.1f}s] NOT_MINIMAL "
                      f"(⟨a,x⟩ ordine {len(H)}) "
                      f"orbite={rec['orbits_burnside']}", flush=True)
                return rec

    # tentativo 3-gen: coppie tra classi di partizione con join pieno
    buckets = {}
    for x in G_list:
        buckets.setdefault(orbit_partition([reps[0], x]), []).append(x)
    a = reps[0]
    keys = list(buckets)
    for i, k1 in enumerate(keys):
        for k2 in keys[i:]:
            if len(orbit_partition([a] +
                   [next(iter(buckets[k1]))] )) == 1:
                continue  # gia' coperto dal 2-gen sopra
            join = orbit_partition([a, next(iter(buckets[k1])),
                                    next(iter(buckets[k2]))])
            if len(join) != 1:
                continue
            for x in islice(buckets[k1], PAIR_SAMPLES):
                for y in islice(buckets[k2], PAIR_SAMPLES):
                    H = proper_or_none([a, x, y], order)
                    if H is not None:
                        rec['status'] = 'NOT_MINIMAL'
                        rec['witness'] = {'gens': [list(a), list(x), list(y)],
                                          'sub_order': len(H)}
                        print(f"    [{time.time()-t0:.1f}s] NOT_MINIMAL "
                              f"(⟨a,x,y⟩ ordine {len(H)}) "
                              f"orbite={rec['orbits_burnside']}", flush=True)
                        return rec

    rec['status'] = 'NO_WITNESS_FOUND'
    print(f"    [{time.time()-t0:.1f}s] NO_WITNESS_FOUND "
          f"orbite={rec['orbits_burnside']}", flush=True)
    return rec


def main():
    census = json.load(open(CENSUS))
    todo = sorted([g for g in census if g['has_15_cycle'] is False],
                  key=lambda g: g['order'])
    nc_orders = sorted({g['order'] for g in todo})
    census_by_order = {}
    for g in todo:
        census_by_order.setdefault(g['order'], []).append(g)
    print(f"{len(todo)} gruppi senza 15-ciclo; ordini {nc_orders}", flush=True)

    results, cache = [], {}
    for g in todo:
        results.append(scan_group(g, nc_orders, census_by_order, cache))
        json.dump(results, open(OUT + '.partial', 'w'))

    # sanity: A5 e [5^2]3 calcolati a mano (688 e 480 orbite), entrambi
    # minimali per aritmetica — se lo scan non li riproduce, c'e' un bug.
    a5 = next(r for r in results if r['t'] == 5)
    v53 = next(r for r in results if r['t'] == 9)
    assert a5['orbits_burnside'] == 688, a5
    assert v53['orbits_burnside'] == 480, v53
    assert a5['status'] == 'MINIMAL_ARITH', a5
    assert v53['status'] == 'MINIMAL_ARITH', v53

    run_list = [r for r in results
                if r['status'] in ('MINIMAL_ARITH', 'NO_WITNESS_FOUND')]
    run_list.sort(key=lambda r: -r['orbits_burnside'])
    summary = {
        'minimal_arith': [r['t'] for r in results
                          if r['status'] == 'MINIMAL_ARITH'],
        'no_witness_found': [r['t'] for r in results
                             if r['status'] == 'NO_WITNESS_FOUND'],
        'not_minimal': [r['t'] for r in results
                        if r['status'] == 'NOT_MINIMAL'],
        'run_list': [{'t': r['t'], 'label': r['label'], 'order': r['order'],
                      'orbits': r['orbits_burnside'], 'name': r['name']}
                     for r in run_list],
    }
    json.dump({'summary': summary, 'groups': results},
              open(OUT, 'w'), indent=1)
    print('\n=== SOMMARIO ===')
    print('MINIMALI (aritmetica):', summary['minimal_arith'])
    print('SENZA TESTIMONE (inclusi per prudenza):',
          summary['no_witness_found'])
    print('NOT_MINIMAL:', summary['not_minimal'])
    print('LISTA-ISTANZE (per orbite decrescenti):')
    for r in summary['run_list']:
        print(f"  15T{r['t']:<3d} ord={r['order']:<6d} "
              f"orbite={r['orbits']:<5d} {r['name']}")
    print('scritto', OUT, flush=True)

if __name__ == '__main__':
    main()

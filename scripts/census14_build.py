#!/usr/bin/env python3
"""T1: costruisce STATE/census14.json da STATE/census14_lmfdb.json.

has_14_cycle deciso rigorosamente:
- ordine <= CAP: enumerazione BFS completa degli elementi (esaustiva);
- ordine >  CAP: (a) se tutti i generatori sono pari -> G <= A14 -> False
  (un 14-ciclo e' una permutazione dispari); (b) altrimenti ricerca random
  di un testimone, verificato esplicitamente -> True; (c) altrimenti
  'needs_proof' (da chiudere con GAP o argomento ad hoc).
Le permutazioni LMFDB sono liste di cicli 1-based; qui immagini 0-based.
"""
import json, random, sys

N = 14
CAP = 2_000_000

def cycles_to_perm(cycles):
    p = list(range(N))
    for cyc in cycles:
        for i, a in enumerate(cyc):
            p[a - 1] = cyc[(i + 1) % len(cyc)] - 1
    return tuple(p)

def compose(a, b):  # a dopo b: (a*b)(x) = a(b(x))
    return tuple(a[b[i]] for i in range(N))

def cycle_lengths(p):
    seen, out = [False] * N, []
    for i in range(N):
        if not seen[i]:
            l, j = 0, i
            while not seen[j]:
                seen[j] = True; j = p[j]; l += 1
            out.append(l)
    return sorted(out)

def is_even(p):
    return (N - len(cycle_lengths(p))) % 2 == 0

def enumerate_group(gens, cap):
    ident = tuple(range(N))
    seen = {ident}
    frontier = [ident]
    while frontier:
        nxt = []
        for x in frontier:
            for g in gens:
                y = compose(x, g)
                if y not in seen:
                    seen.add(y)
                    if len(seen) > cap:
                        return None
                    nxt.append(y)
        frontier = nxt
    return seen

def random_witness(gens, tries=200_000, seed=7):
    rng = random.Random(seed)
    cur = tuple(range(N))
    for _ in range(tries):
        cur = compose(cur, rng.choice(gens))
        if cycle_lengths(cur) == [N]:
            return cur
        if rng.random() < 0.05:  # restart per mescolare
            cur = tuple(range(N))
    return None

def main():
    recs = json.load(open('STATE/census14_lmfdb.json'))
    out = []
    for r in recs:
        gens = [cycles_to_perm(g) for g in r['gens']]
        order = int(r['order'])
        entry = {'label': r['label'], 't': r['t'], 'order': order,
                 'name': r['name'], 'prim': r['prim'], 'solv': r['solv'],
                 'gens': [list(g) for g in gens]}
        if order <= CAP:
            elems = enumerate_group(gens, CAP)
            assert elems is not None and len(elems) == order, \
                f"{r['label']}: enumerati {len(elems) if elems else '>cap'} != {order}"
            entry['has_14_cycle'] = any(cycle_lengths(p) == [N] for p in elems)
            entry['method'] = 'exhaustive'
        elif all(is_even(g) for g in gens):
            entry['has_14_cycle'] = False
            entry['method'] = 'parity(G<=A14)'
        else:
            w = random_witness(gens)
            if w is not None:
                assert cycle_lengths(w) == [N]
                entry['has_14_cycle'] = True
                entry['method'] = 'witness'
                entry['witness'] = list(w)
            else:
                entry['has_14_cycle'] = None
                entry['method'] = 'needs_proof'
        out.append(entry)
        print(f"14T{r['t']:2d} ord={order:<12d} {entry['method']:<16s} "
              f"14cyc={entry['has_14_cycle']} {r['name']}", flush=True)
    json.dump(out, open('STATE/census14.json', 'w'), indent=1)
    with_c = sum(1 for e in out if e['has_14_cycle'] is True)
    without = sum(1 for e in out if e['has_14_cycle'] is False)
    open_q = sum(1 for e in out if e['has_14_cycle'] is None)
    print(f"TOTALE {len(out)}: con 14-ciclo {with_c}, senza {without}, aperti {open_q}")

if __name__ == '__main__':
    main()

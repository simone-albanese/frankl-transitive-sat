#!/usr/bin/env python3
"""T9.1: costruisce STATE/census15.json (104 gruppi transitivi di grado 15).

Fonte: STATE/trans15.grp — libreria GAP "transgrp" di Alexander Hulpke,
copiata il 2026-08-14 da
https://raw.githubusercontent.com/hulpke/transgrp/master/data/trans15.grp
(sha256 89cd49a642797ba47f97b6ecd2addd0ca7c3def99b79435a37ccecb57cbcca00).
È la stessa classificazione servita da LMFDB (l'API LMFDB il 14/08 è dietro
una protezione anti-bot/reCAPTCHA: qui si va alla fonte, che è pure meglio
per la riproducibilità). Il file ha due sezioni: TRANSGRP[15] (generatori
in notazione a cicli + nome) e TRANSPROPERTIES[15] (primo campo = ordine,
secondo = primitività). L'ordine della libreria fa da SECONDA FONTE: per i
gruppi enumerati, |BFS| deve combaciare o il build fallisce.

has_15_cycle deciso rigorosamente:
- ATTENZIONE (diverso dal grado 14): un 15-ciclo è una permutazione PARI,
  quindi la scorciatoia "generatori tutti pari => niente ciclo" NON esiste
  al grado 15. Al suo posto:
- ordine <= ENUM_CAP: enumerazione BFS completa (esaustiva, definitiva);
- ordine >  ENUM_CAP: ricerca random di un testimone, verificato
  esplicitamente -> True; altrimenti 'needs_proof' (da chiudere ad hoc).
Le permutazioni del file sono cicli 1-based; qui immagini 0-based.
"""
import json, random, re, sys

N = 15
SRC = 'STATE/trans15.grp'
OUT = 'STATE/census15.json'
ENUM_CAP = 1_000_000     # BFS completa sotto questa taglia
WITNESS_FIRST = 50_000   # sopra: prova prima il testimone random (economico)


# ---------- parsing del formato GAP ----------

def strip_comments(text):
    return '\n'.join(l for l in text.splitlines() if not l.lstrip().startswith('#'))

def extract_block(text, marker):
    """Il blocco [...] (bilanciato, string-aware) dopo 'marker:='."""
    i = text.index(marker) + len(marker)
    i = text.index('[', i)
    depth, in_str, j = 0, False, i
    while True:
        c = text[j]
        if in_str:
            if c == '"':
                in_str = False
        elif c == '"':
            in_str = True
        elif c == '[':
            depth += 1
        elif c == ']':
            depth -= 1
            if depth == 0:
                return text[i:j + 1]
        j += 1

def split_top(text):
    """Divide sulle virgole a profondità 0 (string-aware, ignora ()[])."""
    parts, depth, in_str, cur = [], 0, False, []
    for c in text:
        if in_str:
            cur.append(c)
            if c == '"':
                in_str = False
            continue
        if c == '"':
            in_str = True; cur.append(c)
        elif c in '([':
            depth += 1; cur.append(c)
        elif c in ')]':
            depth -= 1; cur.append(c)
        elif c == ',' and depth == 0:
            parts.append(''.join(cur).strip()); cur = []
        else:
            cur.append(c)
    if ''.join(cur).strip():
        parts.append(''.join(cur).strip())
    return parts

def parse_perm(token):
    """'(1,2)(3,4)' (eventuali a-capo già rimossi) -> immagini 0-based."""
    p = list(range(N))
    for cyc in re.findall(r'\(([^()]*)\)', token):
        pts = [int(x) for x in cyc.split(',')]
        assert all(1 <= x <= N for x in pts), token
        for i, a in enumerate(pts):
            p[a - 1] = pts[(i + 1) % len(pts)] - 1
    assert sorted(p) == list(range(N)), f'non è una permutazione: {token}'
    return tuple(p)

def parse_source():
    raw = strip_comments(open(SRC).read())
    flat = raw.replace('\n', '')
    groups = []
    body = extract_block(flat, 'TRANSGRP[15]:=')
    for entry in split_top(body[1:-1]):
        assert entry.startswith('[') and entry.endswith(']'), entry[:60]
        gens, name = [], None
        for tok in split_top(entry[1:-1]):
            if tok.startswith('"'):
                name = tok.strip('"')
            elif tok.startswith('('):
                gens.append(parse_perm(tok))
            else:
                raise AssertionError(f'token inatteso: {tok[:60]}')
        assert gens and name, entry[:60]
        groups.append({'gens': gens, 'name': name})
    props = extract_block(flat, 'TRANSPROPERTIES[15]:=')
    orders, prims = [], []
    for entry in split_top(props[1:-1]):
        fields = split_top(entry[1:-1])
        orders.append(int(fields[0]))
        prims.append(int(fields[1]))
    assert len(groups) == len(orders), (len(groups), len(orders))
    for g, o, pr in zip(groups, orders, prims):
        g['order'] = o; g['prim'] = pr
    return groups


# ---------- teoria dei gruppi elementare (come census14) ----------

def compose(a, b):  # a dopo b
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
        if rng.random() < 0.05:   # restart per mescolare
            cur = tuple(range(N))
    return None


# ---------- build ----------

def main():
    groups = parse_source()
    assert len(groups) == 104, f'attesi 104 gruppi transitivi di grado 15, trovati {len(groups)}'
    out = []
    for t0, r in enumerate(groups):
        t = t0 + 1
        gens, order = r['gens'], r['order']
        entry = {'label': f'15T{t}', 't': t, 'order': order,
                 'name': r['name'], 'prim': r['prim'], 'solv': None,
                 'gens': [list(g) for g in gens]}
        w = None
        if order > WITNESS_FIRST:
            w = random_witness(gens)
        if w is not None:
            entry['has_15_cycle'] = True
            entry['method'] = 'witness'
            entry['witness'] = list(w)
        elif order <= ENUM_CAP:
            elems = enumerate_group(gens, ENUM_CAP)
            assert elems is not None and len(elems) == order, \
                f"15T{t}: enumerati {len(elems) if elems else '>cap'} != {order}"
            entry['has_15_cycle'] = any(cycle_lengths(p) == [N] for p in elems)
            entry['method'] = 'exhaustive'
        else:
            entry['has_15_cycle'] = None
            entry['method'] = 'needs_proof'
        out.append(entry)
        print(f"15T{t:<3d} ord={order:<14d} {entry['method']:<12s} "
              f"15cyc={entry['has_15_cycle']} {r['name']}", flush=True)

    # sanity strutturali (falliscono = bug di parsing, non si pubblica niente)
    by_t = {e['t']: e for e in out}
    assert by_t[1]['order'] == 15 and by_t[1]['has_15_cycle'] is True   # C15
    assert by_t[104]['order'] == 1307674368000                          # S15
    assert by_t[103]['order'] == 653837184000                           # A15
    assert by_t[5]['name'].startswith('A_5') and by_t[5]['order'] == 60

    json.dump(out, open(OUT, 'w'), indent=1)
    with_c = sum(1 for e in out if e['has_15_cycle'] is True)
    without = sum(1 for e in out if e['has_15_cycle'] is False)
    open_q = sum(1 for e in out if e['has_15_cycle'] is None)
    print(f"TOTALE {len(out)}: con 15-ciclo {with_c}, senza {without}, aperti {open_q}")
    if open_q:
        print("APERTI:", [e['label'] for e in out if e['has_15_cycle'] is None])

if __name__ == '__main__':
    main()

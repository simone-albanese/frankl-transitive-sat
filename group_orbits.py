"""group_orbits.py — Orbite dei sottoinsiemi di [m] sotto un gruppo di
permutazioni arbitrario (dato per generatori), per la pipeline generalizzata.

Sottoinsiemi come bitmask 0..2^m-1. Una permutazione g (lista images 0-based:
g[p] = immagine del punto p, come in STATE/census14.json campo `gens`) agisce
su una mask S mandando il bit p nel bit g[p]. L'orbita di S si calcola per BFS
sui generatori; il canone di un'orbita è la mask minima.

Lemma di integrità (assert): se G è transitivo su [m] e O è un'orbita di
sottoinsiemi con r_O = |O| elementi tutti di taglia s_O, il conteggio doppio
delle incidenze punto-insieme dà r_O·s_O incidenze distribuite uniformemente
sui m punti (per transitività), quindi m | r_O·s_O. Ne segue che il
coefficiente di margine d_O = r_O(2s_O - m)/m = 2·r_O·s_O/m - r_O è intero.

API compatibile con sat_cyclic: canon_table_group(m, gens) -> tab;
build_orbits(m, tab) riusabile identica (qui ricopiata con l'orbita calcolata
via tab, non via rot).
"""
from ucs_core import popcount


def perm_image(mask, g):
    """Immagine della mask sotto la permutazione g (lista images 0-based)."""
    out = 0
    p = 0
    while mask:
        if mask & 1:
            out |= 1 << g[p]
        mask >>= 1
        p += 1
    return out


def canon_table_group(m, gens):
    """tab[x] = rappresentante canonico (minimo) dell'orbita di x sotto <gens>.
    BFS su ciascuna orbita; costo O(2^m · |gens| · m), fine per m=14."""
    full = (1 << m) - 1
    for g in gens:
        assert sorted(g) == list(range(m)), f"generatore non valido: {g}"
    tab = [-1] * (full + 1)
    for x in range(full + 1):
        if tab[x] >= 0:
            continue
        orb = [x]
        seen = {x}
        c = x
        head = 0
        while head < len(orb):
            y = orb[head]
            head += 1
            for g in gens:
                z = perm_image(y, g)
                if z not in seen:
                    seen.add(z)
                    orb.append(z)
                    if z < c:
                        c = z
        for y in orb:
            tab[y] = c
    return tab


def orbit_of(mask, m, tab):
    """Tutti gli elementi dell'orbita di mask (scansione della tabella)."""
    c = tab[mask]
    return [y for y in range(1 << m) if tab[y] == c]


def build_orbits(m, tab, check_transitive=True):
    """Orbite NON banali (escluse ∅ e full): reps ordinati, info=(c, r, s),
    idx: rep -> indice. Asserisce il lemma m | r·s (vale sse G transitivo)."""
    full = (1 << m) - 1
    counts = {}
    for x in range(1, full):
        counts[tab[x]] = counts.get(tab[x], 0) + 1
    reps = sorted(counts)
    info = []
    idx = {}
    for i, c in enumerate(reps):
        r = counts[c]
        s = popcount(c)
        if check_transitive:
            assert (r * s) % m == 0, f"m∤r·s per rep {c}: G non transitivo?"
        info.append((c, r, s))
        idx[c] = i
    return reps, info, idx


def cyclic_gens(m):
    """Generatore dello shift ciclico su Z_m (per i controlli di validazione)."""
    return [[(p + 1) % m for p in range(m)]]


def load_group(label, path="STATE/census14.json"):
    """Ritorna (m, gens) del gruppo `label` (es. '14T2') dal census."""
    import json
    for g in json.load(open(path)):
        if g["label"] == label:
            return len(g["gens"][0]), g["gens"]
    raise KeyError(label)


if __name__ == "__main__":
    import sys, time
    label = sys.argv[1] if len(sys.argv) > 1 else "14T2"
    t0 = time.time()
    if label.startswith("Z"):
        m = int(label[1:])
        gens = cyclic_gens(m)
    else:
        m, gens = load_group(label)
    tab = canon_table_group(m, gens)
    reps, info, idx = build_orbits(m, tab)
    print(f"{label}: m={m}, {len(reps)} orbite non banali  [{time.time()-t0:.1f}s]")

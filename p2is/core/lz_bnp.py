"""
Conteneurs compressés « 01 02 » (DNGSCN.BNP, P_DEMO.BNP, F01xx.BIN...).

Format : une suite de blocs, sans table d'index (le jeu les lit l'un après l'autre).

  bloc = u8 1 | u8 type (2 = compressé) | u16 0 | u32 taille totale du bloc
         (en-tête de 12 octets compris) | u32 taille décompressée | données

Compression (LZ simple) :
  octet c < 0x80  -> c+1 octets littéraux suivent ;
  octet c >= 0x80 -> copie de (c & 0x7F) + 3 octets, depuis d+1 octets en arrière
                     (d = octet suivant, donc 256 octets de fenêtre au plus).

Pour réinjecter sans rien décaler, chaque bloc garde sa taille compressée
d'origine : on compresse au mieux (découpage optimal), puis on allonge le flux
jusqu'à la taille exacte sans changer ce qu'il produit (voir `ajuster`).
"""

import struct

ENTETE = 12


def lz_decompresser(src: bytes) -> bytes:
    out = bytearray()
    pos = 0
    while pos < len(src):
        c = src[pos]
        pos += 1
        if c < 0x80:
            out += src[pos:pos + c + 1]
            pos += c + 1
        else:
            n = (c & 0x7F) + 3
            dist = src[pos] + 1
            pos += 1
            for _ in range(n):
                out.append(out[-dist] if dist <= len(out) else 0)
    return bytes(out)


def blocs(d: bytes):
    """Liste de (offset, taille totale, type, données décompressées, taille annoncée),
    et la position où s'arrêtent les blocs."""
    res, pos = [], 0
    while pos + ENTETE <= len(d):
        un, typ, zero, tot, ds = struct.unpack_from("<BBHII", d, pos)
        if un != 1 or zero != 0 or tot < ENTETE or pos + tot > len(d):
            break
        brut = d[pos + ENTETE:pos + tot]
        res.append((pos, tot, typ, lz_decompresser(brut) if typ == 2 else brut, ds))
        pos += tot
        while pos < len(d) and pos % 4 and d[pos] == 0:  # blocs alignés sur 4 octets
            pos += 1
    return res, pos


def _correspondances(data: bytes):
    """Pour chaque position : plus longue copie possible (3 à 130 octets, 256 en arrière)."""
    n = len(data)
    best = [(0, 0)] * n
    vus = {}
    for i in range(n):
        if i + 3 > n:
            break
        cle = data[i:i + 3]
        cands = vus.get(cle, [])
        bl = bd = 0
        for j in reversed(cands):
            dist = i - j
            if dist > 256:
                break
            ln = 3
            while ln < 130 and i + ln < n and data[j + ln] == data[i + ln]:
                ln += 1
            if ln > bl:
                bl, bd = ln, dist
                if ln == 130:
                    break
        best[i] = (bl, bd)
        cands.append(i)
        if len(cands) > 300:
            del cands[:100]
        vus[cle] = cands
    return best


def lz_compresser(data: bytes) -> bytes:
    """Flux le plus court possible (programmation dynamique sur les copies et littéraux)."""
    n = len(data)
    m = _correspondances(data)
    inf = 1 << 60
    cout = [inf] * (n + 1)
    choix = [None] * (n + 1)
    cout[n] = 0
    for i in range(n - 1, -1, -1):
        bl, bd = m[i]
        for ln in range(3, bl + 1):
            c = cout[i + ln] + 2
            if c < cout[i]:
                cout[i], choix[i] = c, ("R", ln, bd)
        for ln in range(1, min(128, n - i) + 1):
            c = cout[i + ln] + ln + 1
            if c < cout[i]:
                cout[i], choix[i] = c, ("L", ln)
    out = bytearray()
    i = 0
    while i < n:
        t = choix[i]
        if t[0] == "L":
            out.append(t[1] - 1)
            out += data[i:i + t[1]]
            i += t[1]
        else:
            out.append(0x80 | (t[1] - 3))
            out.append(t[2] - 1)
            i += t[1]
    return bytes(out)


def ajuster(comp: bytes, data: bytes, cible: int) -> bytes:
    """Allonge un flux valide jusqu'à exactement `cible` octets, sans changer ce qu'il
    décompresse : couper une copie en deux ajoute 2 octets, couper une suite de
    littéraux en deux en ajoute 1. ValueError si le flux est déjà trop gros."""
    if len(comp) > cible:
        raise ValueError(f"trop gros : {len(comp)} > {cible} octets")
    toks, pos = [], 0
    while pos < len(comp):
        c = comp[pos]
        if c < 0x80:
            toks.append(["L", bytes(comp[pos + 1:pos + 2 + c])])
            pos += c + 2
        else:
            toks.append(["R", (c & 0x7F) + 3, comp[pos + 1] + 1])
            pos += 2
    manque = cible - len(comp)
    i = 0
    while manque >= 2 and i < len(toks):
        t = toks[i]
        if t[0] == "R" and t[1] >= 6:
            toks[i:i + 1] = [["R", 3, t[2]], ["R", t[1] - 3, t[2]]]
            manque -= 2
        else:
            i += 1
    i = 0
    while manque >= 1 and i < len(toks):
        t = toks[i]
        if t[0] == "L" and len(t[1]) >= 2:
            toks[i:i + 1] = [["L", t[1][:1]], ["L", t[1][1:]]]
            manque -= 1
        else:
            i += 1
    if manque:
        raise ValueError(f"taille exacte impossible (il manque {manque} octets)")
    out = bytearray()
    for t in toks:
        if t[0] == "L":
            out.append(len(t[1]) - 1)
            out += t[1]
        else:
            out.append(0x80 | (t[1] - 3))
            out.append(t[2] - 1)
    assert len(out) == cible and lz_decompresser(bytes(out)) == data
    return bytes(out)


def reconstruire(d: bytes, nouveaux: dict) -> bytes:
    """Remplace les blocs {index: données décompressées} ; chaque bloc garde sa taille
    compressée d'origine, rien ne bouge dans le fichier. ValueError si un bloc ne tient pas."""
    out = bytearray(d)
    bl, _ = blocs(d)
    for k, x in nouveaux.items():
        off, tot, typ, _orig, ds = bl[k]
        if typ != 2 or len(x) != ds:
            raise ValueError(f"bloc {k} : type {typ} ou taille {len(x)} != {ds}")
        out[off + ENTETE:off + tot] = ajuster(lz_compresser(x), x, tot - ENTETE)
    return bytes(out)

"""Encodeur F_BE.BNP / TM_EVE.BNP (répliques de combat et cinématiques in-game).

Format (retrouvé en vérifiant 10 000+ commandes sur les deux fichiers)
----------------------------------------------------------------------
Le texte est découpé en *segments*. Chaque segment est annoncé par la commande

    31 14 81 00  L        ([E4][B_81][B_00] puis un octet de longueur)

  - L < 0x7F  : L-1 octets de texte suivent, puis la commande suivante ;
  - L = 0x7F  : 128 octets de texte, puis un NOUVEL octet de longueur, au milieu
                du texte (chaîne).

Ces octets de longueur intercalés tombent souvent à une adresse impaire : les
anciens outils les lisaient comme du texte (« sins[U+0143][U+7711][B_00]ith »)
et les traducteurs les ont recopiés en fin de réplique. Si une traduction change
la taille d'un segment sans recalculer ces octets, le moteur lit de travers
(crash en combat).

Une réplique du JSON (`offset + _sub_offset`, `_sub_len`) commence au guillemet
du nom, juste après la commande qui ouvre son premier segment. On la découpe en
segments, on remplace le texte de chacun, puis on réécrit les octets de longueur.
La taille totale ne bouge pas (bourrage en [SP] avant les balises de fin).

Garde-fou : reconstruire une réplique à partir de son propre texte anglais doit
redonner l'original à l'octet près ; sinon la réplique est laissée telle quelle.
"""
import json
import re
from collections import Counter
from pathlib import Path

from p2is.core.text import text_to_bytes, decode_text

SEG = b"\x31\x14\x81\x00"
E3 = b"\x03\x11"
CHAINE = 0x7F
BLOC = 128


# ── Lecture / écriture des chaînes de longueur ───────────────────────────────

def _lire_segment(data: bytes, lb: int, limite: int):
    """Lit le segment dont l'octet de longueur est en `lb`.

    Renvoie (texte_sans_longueurs, position_de_fin) ou None si incohérent.
    """
    out = bytearray()
    q = lb
    while q < limite and data[q] == CHAINE:
        out += data[q + 1:q + 1 + BLOC]
        q += 1 + BLOC
    if q >= limite + 1:
        return None
    L = data[q]
    if L == 0:
        return None
    out += data[q + 1:q + L]
    return bytes(out), q + L


def _ecrire_segment(payload: bytes):
    """Octets de longueur + texte, ou None si la taille n'est pas représentable."""
    out = bytearray()
    reste = payload
    while len(reste) >= BLOC:
        out.append(CHAINE)
        out += reste[:BLOC]
        reste = reste[BLOC:]
    if len(reste) + 1 >= CHAINE:
        return None
    out.append(len(reste) + 1)
    out += reste
    return bytes(out)


def decouper(data: bytes, start: int, end: int):
    """Découpe la réplique [start, end) en segments.

    Renvoie (segments, fin) : la liste des textes (sans octets de longueur) et un
    marqueur indiquant si la réplique se termine par une commande dont l'octet
    de longueur appartient à la réplique suivante. None si le format n'est pas
    celui attendu.
    """
    if data[start - 5:start - 1] != SEG:
        return None
    segs = []
    lb = start - 1
    while True:
        lu = _lire_segment(data, lb, end)
        if lu is None:
            return None
        texte, fin = lu
        segs.append(texte)
        if fin == end:
            return segs, "fin"           # la réplique s'arrête pile sur la commande suivante
        if fin == end - 2 and data[fin:end] == E3:
            return segs, "e3"            # fin de scène : le [E3] final n'est pas compté
        if fin > end or data[fin:fin + 4] != SEG:
            return None
        if fin + 5 == end:
            return segs, "commande"      # se termine par [E4] 81 00 + longueur d'autrui
        lb = fin + 4


def assembler(segs, fin_type: str, orig_tail: bytes):
    out = bytearray()
    for k, payload in enumerate(segs):
        enc = _ecrire_segment(payload)
        if enc is None:
            return None
        out += enc
        if k + 1 < len(segs):
            out += SEG
    if fin_type == "commande":
        out += orig_tail  # SEG + octet de longueur de la réplique suivante
    elif fin_type == "e3":
        out += E3
    return bytes(out)


# ── Texte ────────────────────────────────────────────────────────────────────

_TAG = re.compile(r"\[[^\]]+\]")
_CMD = re.compile(r"\[E4\]\[B_81\]\[B_00\]\[B_[0-9A-Fa-f]{2}\]")
_TAIL = re.compile(r"((?:\n|\[[^\]]+\])+)$")


def _tags(text: str) -> Counter:
    return Counter(text_to_bytes(t) for t in _TAG.findall(text) if t not in ("[SP]", "[NL]"))


def _nettoyer_fr(texte_fr: str, texte_orig: str, segs_en_txt) -> str:
    """Retire du FR les commandes de segment et les octets de longueur recopiés."""
    t = _CMD.sub("", texte_fr)
    propres = Counter()
    for s in segs_en_txt:
        propres += _tags(s)
    parasites = _tags(_CMD.sub("", texte_orig)) - propres
    for tag in _TAG.findall(t):
        b = text_to_bytes(tag)
        if parasites.get(b, 0) > 0:
            t = t.replace(tag, "", 1)
            parasites[b] -= 1
    return t


def _couper_fr(texte: str, segs_en_txt):
    """Répartit le texte FR sur autant de segments que l'anglais.

    Chaque segment anglais (après le premier) commence par une balise (ex.
    [0005] ou [0002]) : on coupe le FR juste avant la même balise.
    """
    if len(segs_en_txt) == 1:
        return [texte]
    parts, reste = [], texte
    for s in segs_en_txt[1:]:
        if s.startswith('"') and "\n" in s:
            ancre = s[: s.index("\n") + 1]  # un autre locuteur prend la parole : '"Nom\n'
        else:
            m = _TAG.match(s)
            if not m:
                return None
            ancre = m.group(0)
        i = reste.find(ancre)
        if i < 0:
            return None
        parts.append(reste[:i])
        reste = reste[i:]
    parts.append(reste)
    return parts


def _corps_queue(t: str):
    m = _TAIL.search(t)
    return (t, "") if not m else (t[: m.start()], m.group(1))


_OCTETS_INTERCALES = re.compile(r"\[(?:B_|U\+)[0-9A-Fa-f]+\]")


def _sur_place(data: bytes, start: int, end: int, entry: dict):
    """Réplique qui ne commence pas sur une limite de segment (plusieurs répliques
    dans le même segment) : on remplace son texte à taille identique, sans toucher
    aux octets de longueur. Seulement si la région redonne exactement l'anglais et
    ne contient ni commande de segment ni octet de longueur intercalé."""
    region = bytes(data[start:end])
    nom_o = entry.get("nom_orig") or ""
    en = entry.get("texte_orig") or ""
    if (not nom_o or SEG in region or _OCTETS_INTERCALES.search(nom_o + en)
            or text_to_bytes('"' + nom_o + "\n" + en) != region):
        return None, "format de segments inattendu"
    texte = (entry.get("texte_fr") or "").strip("\r")
    if not texte.strip():
        return None, "pas de traduction"
    corps_en, queue = _corps_queue(en)
    corps, _ = _corps_queue(texte)
    if _tags(corps) != _tags(corps_en):
        return None, "balises de controle differentes de l'original"
    nom = (entry.get("nom_fr") or nom_o).strip()
    fin = text_to_bytes(queue)
    raccourci = False
    while True:
        debut = text_to_bytes('"' + nom + "\n" + corps)
        reste = len(region) - len(debut) - len(fin)
        if reste >= 0 and reste % 2 == 0:
            out = debut + text_to_bytes("[SP]") * (reste // 2) + fin
            return bytes(data[start - 1:start]) + out, ("raccourcie" if raccourci else "ok")
        mots = [m for m in re.split(r"(\[[^\]]+\]|\n)", corps) if m]
        idx = max((i for i, m in enumerate(mots) if not (m.startswith("[") or m == "\n")), default=-1)
        if idx < 0 or not mots[idx]:
            return None, "trop long meme sans texte"
        mots[idx] = mots[idx][:-1]
        corps = "".join(mots)
        raccourci = True


def encoder_bloc(data: bytes, start: int, size: int, entry: dict):
    """Octets FR du bloc (même taille), ou (None, raison)."""
    end = start + size
    dec = decouper(data, start, end)
    if dec is None:
        return _sur_place(data, start, end, entry)
    segs, fin_type = dec
    orig_tail = bytes(data[end - 5:end]) if fin_type == "commande" else b""
    region_orig = bytes(data[start - 1:end])
    if assembler(segs, fin_type, orig_tail) != region_orig:
        return None, "relecture de l'original inexacte"

    segs_txt = [decode_text(s) for s in segs]
    nom = (entry.get("nom_fr") or entry.get("nom_orig") or "").strip()
    texte = (entry.get("texte_fr") or "").strip("\r")
    if not texte.strip():
        return None, "pas de traduction"
    texte = _nettoyer_fr(texte, entry.get("texte_orig", ""), segs_txt)
    if fin_type == "e3":
        # Le [E3] de fin de scene est ecrit hors segment : on le retire du texte.
        texte = re.sub(r"\[E3\]((?:\[[^\]]+\]|\s)*)$", r"\1", texte.rstrip(), count=1)
    parts = _couper_fr(texte, segs_txt)
    if parts is None:
        return None, "segments introuvables dans la traduction"
    parts[0] = '"' + nom + "\n" + parts[0]

    # Contrôle des balises : mêmes balises, segment par segment
    for p, s in zip(parts, segs_txt):
        if _tags(p) != _tags(s):
            return None, "balises de controle differentes de l'original"

    cible = len(region_orig)
    # Le bourrage et les coupes se font dans le segment le plus long (le texte).
    k = max(range(len(parts)), key=lambda i: len(parts[i]))
    corps, queue = _corps_queue(parts[k])
    raccourci = False

    def construire(c, n_sp):
        ps = list(parts)
        ps[k] = c + "[SP]" * n_sp + queue
        segs_fr = [text_to_bytes(p) for p in ps]
        return assembler(segs_fr, fin_type, orig_tail)

    def taille_brute(c):
        # texte + en-têtes, sans les octets de longueur (borne basse)
        ps = list(parts)
        ps[k] = c + queue
        return sum(len(text_to_bytes(p)) for p in ps) + 5 * (len(ps) - 1)

    while True:
        if taille_brute(corps) < cible:
            # Bourrage en [SP] jusqu'à la taille exacte. Certaines longueurs ne
            # s'écrivent pas (segment de 126 ou 127 octets) : on essaie la suivante.
            for n_sp in range(0, (cible - taille_brute(corps)) // 2 + 2):
                out = construire(corps, n_sp)
                if out is not None and len(out) == cible:
                    return out, ("raccourcie" if raccourci else "ok")
        # Trop long (ou taille exacte inatteignable) : on retire un caractère affiché.
        mots = [m for m in re.split(r"(\[[^\]]+\]|\n)", corps) if m]
        idx = max((i for i, m in enumerate(mots) if not (m.startswith("[") or m == "\n")), default=-1)
        if idx < 0 or not mots[idx]:
            return None, "trop long meme sans texte"
        mots[idx] = mots[idx][:-1]
        corps = "".join(mots)
        raccourci = True


def encode_fbe_bnp_from_json(bin_path: str, json_path: str, log_fn, out_path: str = None) -> str:
    data = bytearray(open(bin_path, "rb").read())
    dlgs = json.loads(open(json_path, encoding="utf-8").read(), strict=False)
    stats = Counter()
    for d in sorted(dlgs, key=lambda x: x["offset"] + x["_sub_offset"]):
        start = d["offset"] + d["_sub_offset"]
        size = d["_sub_len"]
        new, raison = encoder_bloc(bytes(data), start, size, d)
        if new is None:
            stats[f"gardee ({raison})"] += 1
            if log_fn and raison != "pas de traduction":
                log_fn(f"  [id {d['id']}] {raison} -> replique d'origine conservee", "warn")
            continue
        data[start - 1:start + size] = new
        stats[raison] += 1
        if raison == "raccourcie" and log_fn:
            log_fn(f"  [!] [DEPASSEMENT] [id {d['id']}] texte FR raccourci pour tenir dans le bloc", "warn")

    if out_path is None:
        out_path = bin_path
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(data)
    if log_fn:
        resume = ", ".join(f"{v} {k}" for k, v in sorted(stats.items()))
        log_fn(f"  [RESUME] {Path(out_path).name} : {resume}", "ok")
    return out_path

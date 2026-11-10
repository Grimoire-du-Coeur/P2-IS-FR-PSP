"""
Messages hors dialogues des scripts (event.bin, DNGSCN.BNP...).

L'extracteur de dialogues (find_dialogs) ne prend que les répliques qui
commencent par « "Nom ». Les autres messages restaient en anglais : profils
des personnages, descriptions « > ... » des objets examinés, messages système,
inscriptions des statues de la forêt...

Un message commence après [1103] (début de message), après [1106][1102]
(page suivante) ou par « > » juste après une zone de données, et s'arrête au
prochain [1106], [1102], [1103], [1208] ou [NULL]. Les balises internes
(couleurs [1431]/[1432] + 3 arguments, noms [1113]/[1112], pauses [1205] + 1
argument) font partie du texte et doivent être gardées telles quelles.

Réinjection : même nombre d'octets que l'anglais, complété par des espaces en
fin de texte ; rien d'autre ne bouge dans le script.
"""

import gzip
import io
import json
import re
import struct
from pathlib import Path

from p2is.core.text import text_to_bytes

SP, NL = 0x1120, 0x1101
FIN = {0x1106, 0x1102, 0x1103, 0x1208, 0x0000}
ARGS = {0x1431: 3, 0x1432: 3, 0x1205: 1}
_BALISE = re.compile(r"\[(?!SP\])(?:NULL|[0-9A-F]{4})\]")


def _lettre(c: int) -> bool:
    return 0x20 <= c <= 0x7E or c in (SP, NL)


def decoder(v) -> str:
    out = []
    for c in v:
        if c == SP:
            out.append("[SP]")
        elif c == NL:
            out.append("\n")
        elif 0x20 <= c <= 0x7E and c not in (0x5B, 0x5D):
            out.append(chr(c))
        else:
            out.append("[NULL]" if c == 0 else f"[{c:04X}]")
    return "".join(out)


def balises(texte: str) -> list:
    """Balises d'un texte, dans l'ordre (les espaces [SP] ne comptent pas)."""
    return _BALISE.findall(texte.replace("[SP]", " "))


def trouver_messages(x: bytes) -> list:
    """(offset en octets, longueur en mots de 16 bits, texte) des messages d'un script."""
    v = struct.unpack(f"<{len(x) // 2}H", x[:len(x) // 2 * 2])
    res = []
    for j in range(len(v) - 1):
        apres_donnees = v[j] == 0 and v[j + 1] == 0x3E and j + 2 < len(v) and v[j + 2] == SP
        if not (v[j] == 0x1103 or (v[j] == 0x1102 and j and v[j - 1] == 0x1106) or apres_donnees):
            continue
        a = k = j + 1
        ok = True
        while k < len(v) and v[k] not in FIN:
            if v[k] in ARGS:
                k += 1 + ARGS[v[k]]
            elif _lettre(v[k]) or v[k] in (0x1113, 0x1112):
                k += 1
            else:
                ok = False  # code inconnu : on ne touche pas
                break
        if not ok or k >= len(v) or v[k] == 0x1208:
            continue  # menu de choix ou structure inconnue
        seg = v[a:k]
        debut = 3 if seg[:3] == (0x1431, 0, 0) else 0  # 3e argument « " » : réplique avec nom
        if sum(0x41 <= c <= 0x7A for c in seg) >= 4 and len(seg) > debut and seg[debut] != 0x22:
            res.append((a * 2, k - a, decoder(seg)))
    return res


def messages_hors_dialogues(x: bytes, dialogues: list) -> list:
    """Messages d'un script qui ne recouvrent aucune réplique déjà extraite."""
    cov = [(d["offset"], d["offset"] + d["slot_size"]) for d in dialogues if "offset" in d]
    return [(o, n, t) for o, n, t in trouver_messages(x)
            if not any(o < b and a < o + 2 * n for a, b in cov)]


def extraire_messages_event(event_bin: str, scripts_json_dir, out_json, log_fn=None) -> int:
    """Crée traduction/event_blocs.json : messages d'event.bin absents des event_scripts.
    Les traductions déjà présentes dans le fichier sont gardées (par texte anglais)."""
    ev = Path(event_bin).read_bytes()
    out_json = Path(out_json)
    ancien, manuels = {}, []
    if out_json.exists():
        for e in json.load(open(out_json, encoding="utf-8")):
            ancien[e["texte_orig"]] = e.get("texte_fr", "")
            if e.get("manuel"):
                manuels.append(e)  # morceaux posés à la main (menus à longueur fixe) : gardés tels quels
    entrees = []
    n_scripts = struct.unpack_from("<I", ev, 0)[0] // 8
    for i in range(n_scripts):
        s, e = struct.unpack_from("<II", ev, i * 8)
        if not s or e <= s or e > len(ev):
            continue
        try:
            x = gzip.GzipFile(fileobj=io.BytesIO(ev[s:e])).read()
        except OSError:
            continue
        p = Path(scripts_json_dir) / f"script_{i:03d}.json"
        dl = json.load(open(p, encoding="utf-8")) if p.exists() else []
        for o, n, t in messages_hors_dialogues(x, dl):
            entrees.append({"script": i, "offset": o, "taille": n, "texte_orig": t,
                            "texte_fr": ancien.get(t, "")})
    deja = {(e["script"], e["offset"]) for e in entrees}
    entrees += [m for m in manuels if (m["script"], m["offset"]) not in deja]
    entrees.sort(key=lambda e: (e["script"], e["offset"]))
    with open(out_json, "w", encoding="utf-8", newline="\r\n") as f:
        json.dump(entrees, f, ensure_ascii=False, indent=2)
        f.write("\n")
    if log_fn:
        log_fn(f"  event.bin : {len(entrees)} messages hors dialogues -> {out_json.name}", "ok")
    return len(entrees)


def appliquer_messages(payload: bytes, orig: bytes, entrees: list, log_fn=None, nom="") -> bytes:
    """Réécrit les messages traduits d'un script déjà encodé, à leur place et à leur taille.
    Un message que l'encodeur a déplacé, ou trop long, reste en anglais."""
    out = bytearray(payload)
    for e in entrees:
        if not e.get("texte_fr"):
            continue
        o, n = e["offset"], 2 * e["taille"]
        if out[o:o + n] != orig[o:o + n]:
            if log_fn:
                log_fn(f"  {nom} message @{o:x} déplacé par l'encodeur -> reste en anglais", "warn")
            continue
        if balises(e["texte_orig"]) != balises(e["texte_fr"]):
            if log_fn:
                log_fn(f"  {nom} message @{o:x} : balises différentes de l'anglais -> reste en anglais", "warn")
            continue
        fr = text_to_bytes(e["texte_fr"])
        if len(fr) > n:
            if log_fn:
                log_fn(f"  {nom} message @{o:x} trop long ({len(fr)} > {n}) -> reste en anglais", "warn")
            continue
        out[o:o + n] = fr + struct.pack("<H", SP) * ((n - len(fr)) // 2)
    return bytes(out)

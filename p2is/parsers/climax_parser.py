"""
Climax Theater (mode Quête) : q00.bin.

Extraction seule, pour préparer la traduction (avec les quêtes DLC, plus tard) ;
la réinjection n'est pas encore écrite.

Format : en-tête de paires (début, fin) u32 pointant sur des flux gzip. Le texte
des flux décompressés utilise les codes de lettres de l'EBOOT (A = 0x00E0,
a = 0x0101, chiffres = 0x00CF..., espace = 0x8140), mais en petit-boutiste.
Les chaînes se terminent par FFFD / FFFE / FFFF.

Sortie : traduction/climax_theater/q00.json, au format de l'EBOOT : [SP] pour
l'espace, <XXXX> pour la ponctuation et les codes (<0004> = point, <0003> =
virgule, <0008> = ?, <0009> = !). `flux` = numéro du flux gzip, `offset` = position
dans le flux décompressé, `taille` = nombre de caractères encodés.
"""

import json
import struct
import zlib
from pathlib import Path

from p2is.parsers.eboot_parser import decode_char

FINS = {0xFFFD, 0xFFFE, 0xFFFF, 0x0000}


def _flux(data: bytes):
    """Flux gzip listés dans l'en-tête (paires début / fin)."""
    res = []
    for k in range(0, 64, 8):
        if k + 8 > len(data):
            break
        s, e = struct.unpack_from("<II", data, k)
        if not s or e <= s or e > len(data) or data[s:s + 2] != b"\x1f\x8b":
            break
        res.append(zlib.decompressobj(31).decompress(data[s:e]))
    return res


def extraire_climax(data: bytes) -> list:
    entrees = []
    for f, x in enumerate(_flux(data)):
        v = struct.unpack(f"<{len(x) // 2}H", x[:len(x) // 2 * 2])
        i = 0
        while i < len(v):
            j, morceaux, lettres = i, [], 0
            while j < len(v) and v[j] not in FINS:
                typ, val = decode_char(v[j])
                if typ != "CHAR" and not (v[j] < 0x0010 or v[j] >> 8 == 0xFF):
                    break
                morceaux.append(val)
                lettres += val.isalpha() and val.isascii()
                j += 1
            if lettres >= 3 and j < len(v) and v[j] in FINS and j > i:
                texte = "".join(morceaux).replace("　", "[SP]")
                entrees.append({"id": len(entrees), "flux": f, "offset": i * 2, "taille": j - i,
                                "texte_orig": texte, "texte_fr": ""})
            i = j + 1
    return entrees


def scan_climax(data: bytes, out_dir: Path, log_fn=None) -> int:
    """Écrit traduction/climax_theater/q00.json (les traductions déjà présentes sont gardées)."""
    dossier = Path(out_dir) / "climax_theater"
    dossier.mkdir(parents=True, exist_ok=True)
    out_path = dossier / "q00.json"
    ancien = {}
    if out_path.exists():
        for e in json.load(open(out_path, encoding="utf-8")):
            ancien[(e["flux"], e["offset"])] = e
    entrees = extraire_climax(data)
    for e in entrees:
        a = ancien.get((e["flux"], e["offset"]))
        if a and a.get("texte_orig") == e["texte_orig"]:
            e["texte_fr"] = a.get("texte_fr", "")
    with open(out_path, "w", encoding="utf-8", newline="\r\n") as fh:
        json.dump(entrees, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    if log_fn:
        log_fn(f"  Climax Theater : {len(entrees)} textes → climax_theater/q00.json (extraction seule)", "ok")
    return len(entrees)

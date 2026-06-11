# -*- coding: utf-8 -*-
"""Propage les traductions DEJA remplies de traduction/event_scripts/ vers les
entrees vides dont le texte_orig est identique (doublons inter-scripts, ex.
boutiques presentes a plusieurs chapitres). Complement de recover.py, dont la
source est l'ancien scripts/ ; ici la source est le nouveau format lui-meme.

Memes garde-fous que recover : jamais d'ecrasement, codes identiques a
texte_orig (hors [SP]/pauses), cout dans le budget. Ecriture atomique.

Usage : python migration/propagate.py [--dry-run]
"""
import os
import sys
import json
import glob

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import texte_nu, extract_codes   # noqa: E402
from byte_budget import cost, budget       # noqa: E402

_PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_EXCL = {"[SP]", "[1205]", "[U+000F]", "[U+000A]", "[001E]", "[U+0008]", "[U+000B]"}


def _codes(s):
    return [c for c in extract_codes(s) if c not in _EXCL]


def propagate(write=True):
    paths = sorted(glob.glob(os.path.join(_PROJ, "traduction",
                                          "event_scripts", "script_*.json")))
    data = {p: json.load(open(p, encoding="utf-8")) for p in paths}

    idx = {}      # texte_nu(orig) -> texte_fr
    names = {}    # nom_orig -> nom_fr
    for p in paths:
        for e in data[p]:
            fr = e.get("texte_fr", "")
            if not fr.strip():
                continue
            to = e.get("texte_orig", "")
            nu = texte_nu(to)
            if nu and texte_nu(fr) != nu:   # jamais de copie anglaise
                idx.setdefault(nu, fr)
            no, nf = e.get("nom_orig", ""), e.get("nom_fr", "").strip()
            if no and nf:
                names.setdefault(no, nf)

    filled = blocked = 0
    for p in paths:
        chg = False
        for e in data[p]:
            if e.get("texte_fr", "").strip():
                continue
            nu = texte_nu(e.get("texte_orig", ""))
            fr = idx.get(nu) if nu else None
            if not fr:
                continue
            nom = e.get("nom_fr", "").strip() or names.get(e.get("nom_orig", ""), "")
            if _codes(e["texte_orig"]) != _codes(fr) or cost(nom, fr) > budget(e):
                blocked += 1
                continue
            e["texte_fr"] = fr
            if nom and not e.get("nom_fr", "").strip():
                e["nom_fr"] = nom
            chg = True
            filled += 1
        if chg and write:
            tmp = p + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(data[p], f, ensure_ascii=False, indent=2)
                f.write("\n")
            json.load(open(tmp, encoding="utf-8"))
            os.replace(tmp, p)
            print(f"{os.path.basename(p)}: rempli(s)")
    return filled, blocked


def main(argv):
    filled, blocked = propagate(write="--dry-run" not in argv)
    print(f"TOTAL propagees: {filled} | bloquees (codes/budget): {blocked}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

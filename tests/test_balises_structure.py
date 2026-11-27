"""Une traduction ne doit jamais perdre une balise de structure (issue #595).

- [1432][NULL][NULL][0014] ouvre/ferme des guillemets : une paire ouverte sans être
  fermée faisait planter le jeu au chargement de la carte (MMAP01, Ramen Shiraishi).
- [E4] au milieu d'un texte est un saut vers une autre réplique.
- [1113] / [1114] sont les noms des héros.

Les menus ([1208]) sont reconstruits par l'encodeur à partir de choix_fr : exclus.
F_BE et TM_EVE ont leur propre encodeur par segments, où [E4] est un marqueur
d'animation géré à part : seuls les noms de héros y sont vérifiés.
"""
import glob
import json
import os

import pytest

TR = os.path.join(os.path.dirname(__file__), "..", "traduction")
BALISES = ("[1432]", "[E4]", "[1113]", "[1114]")


def _entrees():
    fichiers = glob.glob(os.path.join(TR, "*.json")) + glob.glob(os.path.join(TR, "event_scripts", "*.json"))
    for f in fichiers:
        d = json.load(open(f, encoding="utf-8"))
        if not isinstance(d, list):
            continue
        for e in d:
            if not isinstance(e, dict):
                continue
            o, fr = e.get("texte_orig") or "", e.get("texte_fr") or ""
            if fr and "[1208]" not in o and "[U+1208]" not in o:
                yield os.path.relpath(f, TR), e.get("id"), o, fr


def test_balises_de_structure_conservees():
    erreurs = [
        f"{f} id {i} : {b} {o.count(b)} -> {fr.count(b)}"
        for f, i, o, fr in _entrees()
        for b in BALISES
        if o.count(b) != fr.count(b)
        and not (b in ("[E4]", "[1432]") and f in ("F_BE.json", "TM_EVE.json"))
    ]
    if erreurs:
        pytest.fail(f"{len(erreurs)} balise(s) perdue(s) :\n" + "\n".join(erreurs[:40]))

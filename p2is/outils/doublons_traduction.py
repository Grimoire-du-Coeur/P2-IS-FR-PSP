#!/usr/bin/env python3
"""Repere les repliques francaises recopiees sur des originaux differents.

Quand plusieurs repliques vivent dans un meme slot, remplir la premiere et
laisser l'outil propager la valeur aux suivantes donne un resultat qui passe
toutes les verifications existantes : les balises sont intactes, la longueur
tient, `verify_json` est content. En jeu, trois personnages disent la meme
phrase.

Ce controle attrape precisement ce cas : un meme `texte_fr` (balises retirees)
pose sur des `texte_orig` differents. Les vrais doublons du jeu — une phrase
anglaise identique reprise dans deux scripts — ne sont pas signales, puisque
leur original est le meme.

Usage :
    python -m p2is.outils.doublons_traduction            # tout le depot
    python -m p2is.outils.doublons_traduction F_BE.json  # fichiers choisis

Code de sortie : 1 si au moins un groupe suspect est trouve, 0 sinon.
"""

from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
DOSSIER = RACINE / "traduction"

# Longueur en dessous de laquelle une coincidence n'a rien de suspect
# (« Oui. », « Hein? », les libelles de menu courts...).
LONGUEUR_MINIMALE = 18

_BALISES = re.compile(r"\[[^\]]*\]|<[^>]*>")


def dénuder(texte: object) -> str:
    """Retire balises de controle et espaces, pour comparer le texte seul."""
    sans_balises = _BALISES.sub(" ", str(texte or ""))
    return re.sub(r"\s+", " ", sans_balises).strip().lower()


def _entrees(chemin: Path):
    try:
        donnees = json.loads(chemin.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as erreur:
        print(f"  ! illisible : {chemin} ({erreur})", file=sys.stderr)
        return []
    if isinstance(donnees, list):
        return donnees
    valeur = donnees.get("entrees", [])
    return valeur if isinstance(valeur, list) else []


def analyser(fichiers: list[Path]) -> list[tuple]:
    """Renvoie les groupes [(texte_fr, [(fichier, id, texte_orig), ...]), ...]."""
    groupes = defaultdict(list)
    for chemin in fichiers:
        for entree in _entrees(chemin):
            if not isinstance(entree, dict):
                continue
            francais = dénuder(entree.get("texte_fr"))
            original = dénuder(entree.get("texte_orig"))
            if len(francais) < LONGUEUR_MINIMALE or not original:
                continue
            relatif = chemin.relative_to(RACINE).as_posix()
            groupes[francais].append((relatif, entree.get("id"), original))

    suspects = []
    for francais, lignes in groupes.items():
        if len({original for _, _, original in lignes}) > 1:
            suspects.append((francais, lignes))
    return sorted(suspects, key=lambda groupe: -len(groupe[1]))


def main(argv: list[str]) -> int:
    if argv:
        fichiers = [Path(a) if Path(a).is_absolute() else RACINE / a for a in argv]
        fichiers = [f for f in fichiers if f.suffix == ".json" and f.is_file()]
    else:
        fichiers = sorted(DOSSIER.rglob("*.json"))

    if not fichiers:
        print("Aucun fichier JSON a analyser.", file=sys.stderr)
        return 0

    suspects = analyser(fichiers)
    if not suspects:
        print(f"{len(fichiers)} fichier(s) analyse(s) : aucune replique recopiee.")
        return 0

    entrees_touchees = sum(len(lignes) for _, lignes in suspects)
    print(
        f"{len(suspects)} replique(s) francaise(s) posee(s) sur des originaux "
        f"differents, soit {entrees_touchees} entrees :\n"
    )
    for francais, lignes in suspects:
        print(f"  FR  {francais[:88]!r}")
        for fichier, identifiant, original in lignes:
            print(f"      {fichier}  id={identifiant}")
            print(f"          EN  {original[:84]!r}")
        print()
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

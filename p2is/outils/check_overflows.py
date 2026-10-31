#!/usr/bin/env python3
"""Signale les entrees dont la traduction FR depasse son budget d'octets.

Un depassement n'est pas benin : bin_encoder.py tronque automatiquement le
texte trop long, donc la replique part amputee dans le patch.

Remplace les deux versions precedentes (scripts/check_real_overflows.py et
p2is_tool/server/src/check_overflows.py), qui partageaient deux defauts :

  1. des chemins absolus en dur vers C:/Users/nolan/Desktop/..., donc
     inutilisables par quelqu'un d'autre ;
  2. un budget calcule en "data_size - 8", alors que l'encodeur utilise
     "data_size - len(_term) * 2". Beaucoup d'entrees n'ont que trois
     terminateurs : le budget etait sous-estime de 2 octets, ce qui faisait
     remonter des centaines de faux depassements.

Ne couvre que les scripts d'evenement : l'EBOOT a un autre encodeur et un
autre budget, c'est audit_eboot.py qui s'en charge.

Usage :
    python -m p2is.outils.check_overflows
    python -m p2is.outils.check_overflows traduction/event_scripts/script_000.json
"""
import glob
import json
import os
import sys

# Amorce : `python p2is/outils/<outil>.py` ne met pas la racine du depot dans
# sys.path, contrairement a `python -m p2is.outils.<outil>`. Les deux doivent
# marcher, un contributeur tapera l'un ou l'autre.
import os as _os
import sys as _sys

_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))))

from p2is import RACINE as _RACINE  # noqa: E402

RACINE = str(_RACINE)

from p2is.core.text import text_to_bytes, _align_menu_text, _needs_nl_suffix  # noqa: E402
from p2is.parsers.bin_parser import _rebuild_choice_body  # noqa: E402


def budget(d):
    """Octets disponibles, formule exacte de bin_encoder.py (l. 291)."""
    term = d.get("_term") or [0, 0, 0, 0]
    return d.get("data_size", 0) - len(term) * 2


def taille_fr(d):
    """Octets reellement ecrits pour cette entree, terminateur [NL] compris."""
    n_fr = d.get("nom_fr", "").strip() or d.get("nom_orig", "").strip()
    t_fr = d.get("texte_fr", "").strip()

    choix_fr = d.get("choix_fr")
    q_fr = d.get("question_fr", "").strip()
    if choix_fr is not None:
        remplis = [c for c in choix_fr if c.strip()]
        if q_fr and remplis:
            # count_tag preserve : sinon _rebuild_choice_body le devine et se
            # trompe des que le menu a plus de deux options.
            t_fr = _rebuild_choice_body(q_fr, choix_fr, d.get("count_tag"))
        elif not t_fr:
            return None
    elif not n_fr and not t_fr:
        return None
    elif not t_fr:
        t_fr = d.get("texte_orig", "").strip()

    t_fr = _align_menu_text(d.get("nom_orig", ""), d.get("texte_orig", ""), n_fr, t_fr)
    enc = text_to_bytes('"' + n_fr + "\n" + t_fr)
    nl = 2 if _needs_nl_suffix(d.get("_term", []), d.get("texte_orig", "")) else 0

    avail = budget(d)
    if avail > 0 and len(enc) + nl > avail and ("[1208]" in t_fr or "[U+1208]" in t_fr):
        marker = "[U+1208]" if "[U+1208]" in t_fr else "[1208]"
        parts = t_fr.split(marker, 1)
        while parts[0].endswith("[SP]") and (len(text_to_bytes('"' + n_fr + "\n" + parts[0] + marker + parts[1])) + nl > avail):
            parts[0] = parts[0][:-4]
        t_fr = parts[0] + marker + parts[1]
        enc = text_to_bytes('"' + n_fr + "\n" + t_fr)

    return len(enc) + nl


def fichiers(args):
    if args:
        return [a if os.path.isabs(a) else os.path.join(RACINE, a) for a in args]
    # Seulement event_scripts/. Le budget calcule ici est celui de
    # bin_encoder.py, et lui seul :
    #
    #   - EBOOT_decoupe/ n'a pas de bloc `_term` et passe par un autre
    #     encodeur (voir audit_eboot.py) : pres de 6 000 faux depassements ;
    #   - MMAP01-06, F_BE et TM_EVE passent par mmap_encoder et fbe_encoder,
    #     qui ont leur propre budget et rognent deja le texte eux-memes :
    #     741 lignes de bruit, pour 16 vrais depassements dans les scripts.
    #
    # Ces deux familles meritent leur verificateur, pas celui-ci.
    return sorted(glob.glob(os.path.join(RACINE, "traduction", "event_scripts", "*.json")))


def main():
    depassements = []
    examinees = 0
    ignorees = 0

    for chemin in fichiers(sys.argv[1:]):
        if os.path.basename(chemin) == "sys.json":
            continue
        try:
            with open(chemin, encoding="utf-8") as fh:
                data = json.load(fh)
        except (OSError, json.JSONDecodeError) as e:
            print(f"[!] {os.path.basename(chemin)} illisible : {e}", file=sys.stderr)
            continue
        if not isinstance(data, list):
            continue

        for d in data:
            if not isinstance(d, dict):
                continue
            if "_term" not in d:
                ignorees += 1
                continue
            taille = taille_fr(d)
            if taille is None:
                continue
            examinees += 1
            avail = budget(d)
            if avail > 0 and taille > avail:
                depassements.append(
                    (os.path.basename(chemin), d.get("id"), taille, avail))

    for nom, ident, taille, avail in depassements:
        print(f"{nom}|{ident}|{taille}|{avail}|+{taille - avail}")

    print(f"\n{len(depassements)} depassement(s) sur {examinees} entrees traduites",
          file=sys.stderr)
    return 1 if depassements else 0


if __name__ == "__main__":
    sys.exit(main())

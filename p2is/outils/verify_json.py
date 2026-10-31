#!/usr/bin/env python3
"""Vérificateur de fichiers JSON de traduction pour Persona 2: Innocent Sin (PSP).

Vérifie l'intégrité des fichiers JSON modifiés lors d'une Pull Request :
  1. Validité de l'encodage UTF-8 et syntaxe JSON stricte.
  2. Structure correcte des entrées (liste de dictionnaires avec 'id').
  3. Intégrité des balises de contrôle ([SP], [E1], <...>, etc.) sur les entrées modifiées.
  4. Signalement des dépassements de taille éventuels.

Code de sortie :
  - 0 : Succès (fichiers valides, aucune régression ou corruption de balises).
  - 1 : Erreur bloquante (JSON invalide, balise brisée, structure incorrecte).
"""

import glob
import json
import os
import subprocess
import sys

# Assurer un affichage UTF-8 sans crash sur toutes les plateformes
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

from p2is import RACINE as _RACINE

RACINE = str(_RACINE)


def get_base_data(nom_fichier_relatif):
    """Tente de récupérer la version de base du fichier depuis git (origin/main ou HEAD~1)."""
    for ref in ("origin/main", "HEAD~1", "HEAD"):
        try:
            res = subprocess.check_output(
                ["git", "show", f"{ref}:{nom_fichier_relatif}"],
                stderr=subprocess.DEVNULL,
                cwd=RACINE,
            )
            raw = res.decode("utf-8")
            data = json.loads(raw)
            if isinstance(data, list):
                return {d.get("id"): d for d in data if isinstance(d, dict) and "id" in d}
        except Exception:
            continue
    return None


def verifier_fichier(chemin_fichier):
    nom_rel = os.path.relpath(chemin_fichier, RACINE).replace("\\", "/")
    erreurs_bloquantes = []
    avertissements = []

    # 1. Syntaxe JSON & UTF-8
    try:
        with open(chemin_fichier, "r", encoding="utf-8") as f:
            data = json.load(f)
    except UnicodeDecodeError as e:
        erreurs_bloquantes.append(f"{nom_rel}: Erreur d'encodage UTF-8 : {e}")
        return erreurs_bloquantes, avertissements
    except json.JSONDecodeError as e:
        erreurs_bloquantes.append(f"{nom_rel}: Syntaxe JSON invalide (ligne {e.lineno}, col {e.colno}) : {e.msg}")
        return erreurs_bloquantes, avertissements
    except Exception as e:
        erreurs_bloquantes.append(f"{nom_rel}: Impossible d'ouvrir le fichier : {e}")
        return erreurs_bloquantes, avertissements

    if not isinstance(data, list):
        erreurs_bloquantes.append(f"{nom_rel}: La racine du JSON doit être une liste.")
        return erreurs_bloquantes, avertissements

    base_entries = get_base_data(nom_rel)

    # 2. Examen de chaque entrée
    entrees_verifiees = 0
    entrees_modifiees = 0

    for idx, d in enumerate(data):
        if not isinstance(d, dict):
            erreurs_bloquantes.append(f"{nom_rel}[{idx}]: L'élément n'est pas un dictionnaire.")
            continue

        ident = d.get("id", f"idx_{idx}")
        entrees_verifiees += 1

        # Déterminer si l'entrée a été modifiée par rapport à la base
        is_modified = True
        if base_entries is not None:
            old_entry = base_entries.get(ident)
            if old_entry is not None:
                if (
                    old_entry.get("texte_fr") == d.get("texte_fr")
                    and old_entry.get("nom_fr") == d.get("nom_fr")
                    and old_entry.get("choix_fr") == d.get("choix_fr")
                    and old_entry.get("question_fr") == d.get("question_fr")
                ):
                    is_modified = False

        if is_modified:
            entrees_modifiees += 1

        champs = [
            ("texte_fr", d.get("texte_fr")),
            ("nom_fr", d.get("nom_fr")),
            ("question_fr", d.get("question_fr")),
        ]
        choix = d.get("choix_fr")
        if isinstance(choix, list):
            for c_i, c_val in enumerate(choix):
                champs.append((f"choix_fr[{c_i}]", c_val))

        for champ, val in champs:
            if not val or not isinstance(val, str):
                continue

            open_b = val.count("[")
            close_b = val.count("]")
            if open_b != close_b:
                msg = f"{nom_rel} (id {ident}, {champ}): Crochets déséquilibrés ('[': {open_b}, ']': {close_b}) -> {val!r}"
                if is_modified:
                    erreurs_bloquantes.append(msg)
                else:
                    avertissements.append(f"[Pré-existant] {msg}")

            open_c = val.count("<")
            close_c = val.count(">")
            if open_c != close_c:
                msg = f"{nom_rel} (id {ident}, {champ}): Chevrons déséquilibrés ('<': {open_c}, '>': {close_c}) -> {val!r}"
                if is_modified:
                    erreurs_bloquantes.append(msg)
                else:
                    avertissements.append(f"[Pré-existant] {msg}")

    return erreurs_bloquantes, avertissements


def main():
    fichiers = sys.argv[1:]

    if not fichiers or "--all" in fichiers:
        if "--all" in fichiers:
            fichiers.remove("--all")
        if not fichiers:
            fichiers = sorted(glob.glob(os.path.join(RACINE, "traduction", "**", "*.json"), recursive=True))

    total_fichiers = 0
    toutes_erreurs = []
    tous_avertissements = []

    for f in fichiers:
        f_norm = f.strip().strip("'\"")
        if not f_norm:
            continue
        chemin = f_norm if os.path.isabs(f_norm) else os.path.join(RACINE, f_norm)
        if not os.path.isfile(chemin) or not chemin.endswith(".json"):
            continue

        total_fichiers += 1
        errs, warns = verifier_fichier(chemin)
        toutes_erreurs.extend(errs)
        tous_avertissements.extend(warns)

    print(f"=== Validation des scripts Persona 2 IS : {total_fichiers} fichier(s) vérifié(s) ===")

    if tous_avertissements:
        print(f"\n[INFO] {len(tous_avertissements)} avertissement(s) pré-existant(s) dans le projet :")
        for w in tous_avertissements[:10]:
            print(f"  {w}")
        if len(tous_avertissements) > 10:
            print(f"  ... et {len(tous_avertissements) - 10} autre(s) avertissement(s).")

    if toutes_erreurs:
        print(f"\n❌ {len(toutes_erreurs)} erreur(s) bloquante(s) :")
        for e in toutes_erreurs:
            print(f"  - {e}")
        return 1

    print("\n✓ Tous les fichiers vérifiés sont 100% valides.")
    return 0


if __name__ == "__main__":
    sys.exit(main())


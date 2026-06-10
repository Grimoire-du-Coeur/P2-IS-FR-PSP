import os
import sys
import json
import glob
import argparse

sys.path.insert(0, os.path.dirname(__file__))
from byte_budget import cost, budget  # noqa: E402
from core import _KNOWN_RENAMES               # noqa: E402

# Tout code source de la map de renommage qui subsiste dans un FR transfere
# est une erreur de conversion -> avertissement.
_OLD_PLACEHOLDERS = [old for old, _new in _KNOWN_RENAMES]


def _check_1432(texte):
    """Avertit si un [1432] n'est pas suivi de [NULL][NULL][0014]."""
    warns = []
    idx = 0
    while True:
        i = texte.find("[1432]", idx)
        if i == -1:
            break
        if not texte[i:].startswith("[1432][NULL][NULL][0014]"):
            warns.append("structure [1432] incomplete (attendu [1432][NULL][NULL][0014])")
        idx = i + 6
    return warns


def verify_data(data):
    """Verifie une liste d'entrees (nouveau format). Retourne ok/error/skip + listes."""
    res = {
        "ok": 0,
        "error_cnt": 0,
        "skip": 0,
        "errors": [],
        "warnings": [],
    }
    for d in data:
        ident = d.get("id", "?")
        nom = d.get("nom_fr", "").strip()
        texte = d.get("texte_fr", "").strip()
        if not nom or not texte:
            res["skip"] += 1
            continue

        c = cost(nom, texte)
        lim = budget(d)
        if c == -1:
            res["error_cnt"] += 1
            res["errors"].append(f"ID {ident} : crochet '[' non ferme")
        elif c > lim:
            excess = c - lim
            res["error_cnt"] += 1
            res["errors"].append(
                f"ID {ident} : +{excess} octets (+{excess // 2} chars en trop) | Max: ~{lim // 2} chars"
            )
        else:
            res["ok"] += 1

        for ph in _OLD_PLACEHOLDERS:
            if ph in nom or ph in texte:
                res["warnings"].append(
                    f"ID {ident} : ancien placeholder {ph} (attendu sans U+)"
                )
        for w in _check_1432(texte):
            res["warnings"].append(f"ID {ident} : {w}")
    return res


def verify_file(path):
    with open(path, encoding="utf-8") as f:
        return verify_data(json.load(f))


def expand_paths(paths):
    """Remplace chaque dossier par ses fichiers *.json tries ; laisse les fichiers tels quels."""
    out = []
    for p in paths:
        if os.path.isdir(p):
            out.extend(sorted(glob.glob(os.path.join(p, "*.json"))))
        else:
            out.append(p)
    return out


def render(results, errors_only=False, show_warnings=True, markdown=False, summary=False):
    """Formate une liste (path, res) en chaine de caracteres."""
    lines = []
    if markdown:
        lines.append("| Fichier | OK | ERROR | SKIP |")
        lines.append("|---|---|---|---|")
        for path, res in results:
            if errors_only and res["error_cnt"] == 0:
                continue
            lines.append(f"| {path} | {res['ok']} | {res['error_cnt']} | {res['skip']} |")
            for e in res["errors"]:
                lines.append(f"| ⚠ {e} | | | |")
            if show_warnings:
                for w in res["warnings"]:
                    lines.append(f"| warn: {w} | | | |")
    else:
        for path, res in results:
            if errors_only and res["error_cnt"] == 0:
                continue
            lines.append(f"{path}: {res['ok']} OK, {res['error_cnt']} ERROR, {res['skip']} SKIP")
            for e in res["errors"]:
                lines.append(f"  ERREUR  - {e}")
            if show_warnings:
                for w in res["warnings"]:
                    lines.append(f"  warn    - {w}")

    if summary:
        tot_ok = sum(r["ok"] for _, r in results)
        tot_err = sum(r["error_cnt"] for _, r in results)
        tot_skip = sum(r["skip"] for _, r in results)
        tot_warn = sum(len(r["warnings"]) for _, r in results)
        n_err_files = sum(1 for _, r in results if r["error_cnt"] > 0)
        sline = (f"TOTAL: {len(results)} fichier(s) | {tot_ok} OK, {tot_err} ERROR, "
                 f"{tot_skip} SKIP, {tot_warn} warn | {n_err_files} fichier(s) en erreur")
        if markdown:
            lines.append("")
        lines.append(sline)
    return "\n".join(lines)


def main(argv):
    parser = argparse.ArgumentParser(
        prog="verify.py",
        description="Verificateur format event_scripts : limite d'octets (data_size-8) "
                    "+ conventions (codes [U+XXXX] residuels, structure [1432]).",
    )
    parser.add_argument("files", nargs="*", help="fichiers .json ou dossiers a verifier")
    parser.add_argument("--errors-only", action="store_true",
                        help="n'afficher que les fichiers ayant des erreurs")
    parser.add_argument("--no-warnings", action="store_true",
                        help="masquer les avertissements")
    parser.add_argument("--markdown", action="store_true",
                        help="sortie en tableau Markdown")
    parser.add_argument("--summary", action="store_true",
                        help="ajouter une ligne de totaux")
    args = parser.parse_args(argv)

    if not args.files:
        parser.print_help()
        return 1

    paths = expand_paths(args.files)
    results = []
    had_error = False
    for path in paths:
        try:
            res = verify_file(path)
        except FileNotFoundError:
            print(f"{path}: introuvable")
            had_error = True
            continue
        except json.JSONDecodeError as e:
            print(f"{path}: ERREUR JSON - {e}")
            had_error = True
            continue
        results.append((path, res))
        if res["error_cnt"] > 0:
            had_error = True

    out = render(
        results,
        errors_only=args.errors_only,
        show_warnings=not args.no_warnings,
        markdown=args.markdown,
        summary=args.summary,
    )
    if out:
        print(out)
    return 1 if had_error else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

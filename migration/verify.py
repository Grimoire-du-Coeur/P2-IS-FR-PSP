import os
import sys
import json

sys.path.insert(0, os.path.dirname(__file__))
from byte_budget import cost, budget  # noqa: E402

_OLD_PLACEHOLDERS = ["[U+1113]", "[U+1112]"]


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
        nom = d.get("nom_fr", "").strip()
        texte = d.get("texte_fr", "").strip()
        if not nom or not texte:
            res["skip"] += 1
            continue

        c = cost(nom, texte)
        lim = budget(d)
        if c == -1:
            res["error_cnt"] += 1
            res["errors"].append(f"ID {d['id']} : crochet '[' non ferme")
        elif c > lim:
            excess = c - lim
            res["error_cnt"] += 1
            res["errors"].append(
                f"ID {d['id']} : +{excess} octets (+{excess // 2} chars en trop) | Max: ~{lim // 2} chars"
            )
        else:
            res["ok"] += 1

        for ph in _OLD_PLACEHOLDERS:
            if ph in nom or ph in texte:
                res["warnings"].append(
                    f"ID {d['id']} : ancien placeholder {ph} (attendu sans U+)"
                )
        for w in _check_1432(texte):
            res["warnings"].append(f"ID {d['id']} : {w}")
    return res


def verify_file(path):
    with open(path, encoding="utf-8") as f:
        return verify_data(json.load(f))


def main(argv):
    if not argv:
        print("Usage: python migration/verify.py <fichier.json> [...]")
        return 1
    had_error = False
    for path in argv:
        res = verify_file(path)
        print(
            f"{path}: {res['ok']} OK, {res['error_cnt']} ERROR, {res['skip']} SKIP"
        )
        for e in res["errors"]:
            print(f"  ERREUR  - {e}")
        for w in res["warnings"]:
            print(f"  warn    - {w}")
        had_error = had_error or res["error_cnt"] > 0
    return 1 if had_error else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

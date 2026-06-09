# -*- coding: utf-8 -*-
import os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
from core import decide, convert_fr           # noqa: E402
from byte_budget import cost, budget           # noqa: E402


def _load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _save(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def transfer_script(old_path, new_path):
    """Transfere les entrees sures de old_path vers new_path (en place).
    Retourne un rapport {auto, untranslated, pauses:[...]}."""
    old = _load(old_path)
    new = _load(new_path)

    if len(old) != len(new):
        raise ValueError(
            f"Nombre d'entrees different : ancien={len(old)} nouveau={len(new)}"
        )

    old_by_id = {e["id"]: e for e in old}
    if set(old_by_id) != {e["id"] for e in new}:
        raise ValueError("Les ensembles d'id ne correspondent pas")

    report = {"auto": 0, "untranslated": 0, "pauses": []}

    for ne in new:
        oe = old_by_id[ne["id"]]
        status, reason = decide(oe, ne)

        if status == "auto":
            ne["nom_fr"] = convert_fr(oe.get("nom_fr", ""))
            ne["texte_fr"] = convert_fr(oe.get("texte_fr", ""))
            report["auto"] += 1
        elif status == "untranslated":
            report["untranslated"] += 1
        else:  # pause
            reco_nom = convert_fr(oe.get("nom_fr", ""))
            reco_txt = convert_fr(oe.get("texte_fr", ""))
            report["pauses"].append({
                "id": ne["id"],
                "reason": reason,
                "nom_orig": ne.get("nom_orig", ""),
                "texte_orig_new": ne.get("texte_orig", ""),
                "reco_nom_fr": reco_nom,
                "reco_texte_fr": reco_txt,
                "budget": budget(ne),
                "reco_cost": cost(reco_nom, reco_txt),
            })

    _save(new_path, new)
    return report


import re as _re

_PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def resolve_paths(token, base=None):
    """'007' ou 'script_007' -> (old_path, new_path)."""
    base = base or _PROJ
    m = _re.search(r"(\d+)", token)
    if not m:
        raise ValueError(f"Impossible d'extraire un numero de '{token}'")
    num = m.group(1).zfill(3)
    name = f"script_{num}.json"
    return (os.path.join(base, "scripts", name),
            os.path.join(base, "traduction", "event_scripts", name))


def format_report(token, report):
    lines = [f"=== {token} : {report['auto']} auto, "
             f"{len(report['pauses'])} pause, {report['untranslated']} a traduire ==="]
    for p in report["pauses"]:
        over = "" if p["reco_cost"] != -1 and p["reco_cost"] <= p["budget"] else "  ⚠ DEPASSE"
        lines.append(f"\n-- PAUSE id={p['id']} ({p['reason']}){over}")
        lines.append(f"   nom_orig      : {p['nom_orig']}")
        lines.append(f"   texte_orig    : {p['texte_orig_new']}")
        lines.append(f"   RECO nom_fr   : {p['reco_nom_fr']}")
        lines.append(f"   RECO texte_fr : {p['reco_texte_fr']}")
        lines.append(f"   octets        : reco={p['reco_cost']} / budget={p['budget']}")
    return "\n".join(lines)


def main(argv):
    if not argv:
        print("Usage: python migration/transfer.py <numero|script_NNN> [...]")
        return 1
    for token in argv:
        old_path, new_path = resolve_paths(token)
        report = transfer_script(old_path, new_path)
        print(format_report(token, report))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

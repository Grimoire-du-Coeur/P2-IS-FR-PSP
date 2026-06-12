# -*- coding: utf-8 -*-
import os, sys, json, re as _re, difflib
from collections import Counter
sys.path.insert(0, os.path.dirname(__file__))
from core import decide, convert_fr, extract_codes, texte_nu, has_trigger  # noqa: E402
from byte_budget import cost, budget                           # noqa: E402

_PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _save(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def _convert_pair(oe):
    """(nom_fr, texte_fr) convertis depuis une entree ancienne."""
    return convert_fr(oe.get("nom_fr", "")), convert_fr(oe.get("texte_fr", ""))


def _make_pause(oe, ne, reason, report):
    reco_nom, reco_txt = _convert_pair(oe)
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


def _process_pair(oe, ne, report):
    """Paire alignee (texte_nu identique) : applique decide()."""
    status, reason = decide(oe, ne)
    if status == "auto":
        new_nom, new_txt = _convert_pair(oe)
        # Ne jamais ecraser une valeur deja presente cote nouveau par du vide.
        if new_nom or not ne.get("nom_fr", "").strip():
            ne["nom_fr"] = new_nom
        if new_txt or not ne.get("texte_fr", "").strip():
            ne["texte_fr"] = new_txt
        report["auto"] += 1
    elif status == "untranslated":
        report["untranslated"] += 1
    else:
        _make_pause(oe, ne, reason, report)


def _process_replace_pair(oe, ne, report):
    """Paire d'un bloc 'replace' : texte_nu diverge -> pause si l'ancien est traduit."""
    if oe.get("nom_fr", "").strip() or oe.get("texte_fr", "").strip():
        reasons = ["texte divergent"]
        if has_trigger(oe.get("texte_orig", "")) or has_trigger(ne.get("texte_orig", "")):
            reasons.append("menu/Q-R")
        _make_pause(oe, ne, " + ".join(reasons), report)
    else:
        report["untranslated"] += 1


def _add_orphan(oe, report):
    """Entree ancienne traduite sans contrepartie cote nouveau (FR sans destination)."""
    if oe.get("nom_fr", "").strip() or oe.get("texte_fr", "").strip():
        report["orphans"].append({
            "id": oe["id"],
            "nom_fr": oe.get("nom_fr", ""),
            "texte_fr": oe.get("texte_fr", ""),
        })


def _add_new_only(ne, report):
    """Entree nouvelle sans source ancienne (a traduire from scratch)."""
    report["new_only"].append({
        "id": ne["id"],
        "nom_orig": ne.get("nom_orig", ""),
        "texte_orig": ne.get("texte_orig", ""),
    })


def transfer_script(old_path, new_path):
    """Aligne ancien/nouveau par sous-sequence (texte normalise) et transfere
    les entrees sures en place. Retourne un rapport
    {auto, untranslated, pauses, new_only, orphans}."""
    old = _load(old_path)
    new = _load(new_path)

    old_nu = [texte_nu(e.get("texte_orig", "")) for e in old]
    new_nu = [texte_nu(e.get("texte_orig", "")) for e in new]

    report = {"auto": 0, "untranslated": 0, "pauses": [], "new_only": [], "orphans": []}

    sm = difflib.SequenceMatcher(a=old_nu, b=new_nu, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                _process_pair(old[i1 + k], new[j1 + k], report)
        elif tag == "replace":
            n_pair = min(i2 - i1, j2 - j1)
            for k in range(n_pair):
                _process_replace_pair(old[i1 + k], new[j1 + k], report)
            for k in range(i1 + n_pair, i2):
                _add_orphan(old[k], report)
            for k in range(j1 + n_pair, j2):
                _add_new_only(new[k], report)
        elif tag == "delete":
            for k in range(i1, i2):
                _add_orphan(old[k], report)
        elif tag == "insert":
            for k in range(j1, j2):
                _add_new_only(new[k], report)

    _save(new_path, new)
    return report


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
    lines = [f"=== {token} : {report['auto']} auto, {len(report['pauses'])} pause, "
             f"{report['untranslated']} a traduire, {len(report['new_only'])} new-only, "
             f"{len(report['orphans'])} orphelins ==="]
    for p in report["pauses"]:
        over = "" if p["reco_cost"] != -1 and p["reco_cost"] <= p["budget"] else "  ⚠ DEPASSE"
        lines.append(f"\n-- PAUSE id={p['id']} ({p['reason']}){over}")
        lines.append(f"   nom_orig      : {p['nom_orig']}")
        lines.append(f"   texte_orig    : {p['texte_orig_new']}")
        lines.append(f"   RECO nom_fr   : {p['reco_nom_fr']}")
        lines.append(f"   RECO texte_fr : {p['reco_texte_fr']}")
        lines.append(f"   octets        : reco={p['reco_cost']} / budget={p['budget']}")
    if report["new_only"]:
        ids = ", ".join(str(e["id"]) for e in report["new_only"])
        lines.append(f"\n-- {len(report['new_only'])} entrees NOUVELLES a traduire (ids: {ids})")
    if report["orphans"]:
        ids = ", ".join(str(e["id"]) for e in report["orphans"])
        lines.append(f"\n-- {len(report['orphans'])} entrees ANCIENNES orphelines (ids: {ids})")
    if report["new_only"] and report["orphans"]:
        lines.append("\n  ⚠ orphelins ET new-only presents : possible mauvais "
                     "appariement (meme contenu deplace) a reconcilier manuellement.")
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


def detect_code_renames(old, new):
    """Compare les multiset de codes (apres conversion connue) entre ancien et nouveau.
    Retourne {ancien_seul: {code: n}, nouveau_seul: {code: n}}."""
    old_codes = Counter()
    new_codes = Counter()
    new_by_id = {e["id"]: e for e in new}
    for oe in old:
        ne = new_by_id.get(oe["id"])
        if ne is None:
            continue
        old_codes.update(extract_codes(convert_fr(oe.get("texte_orig", ""))))
        new_codes.update(extract_codes(ne.get("texte_orig", "")))
    ancien_seul = {c: old_codes[c] - new_codes[c]
                   for c in old_codes if old_codes[c] > new_codes[c]}
    nouveau_seul = {c: new_codes[c] - old_codes[c]
                    for c in new_codes if new_codes[c] > old_codes[c]}
    return {"ancien_seul": ancien_seul, "nouveau_seul": nouveau_seul}


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

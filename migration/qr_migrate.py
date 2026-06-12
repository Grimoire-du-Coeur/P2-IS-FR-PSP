# -*- coding: utf-8 -*-
"""Remplit question_fr/choix_fr des entrees menu depuis leur texte_fr, via
migrate_choices_in_json() de p2is_tool.py (version upstream corrigee) — garantit
la coherence avec ce que lira l'encodeur. texte_fr est CONSERVE (fallback).

Usage : python migration/qr_migrate.py [--dry-run]
"""
import os
import sys
import json
import glob
import types
import importlib.util

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import extract_codes          # noqa: E402
from byte_budget import cost, budget    # noqa: E402

_PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Codes ignores dans la comparaison de structure ([SP]=espace, pauses libres).
_EXCL = {"[SP]", "[1205]", "[U+000F]", "[U+000A]", "[001E]", "[U+0008]", "[U+000B]"}


def _codes(s):
    return [c for c in extract_codes(s) if c not in _EXCL]


def _load_p2is_tool():
    """Importe p2is_tool.py sans GUI : customtkinter est stubbe (non installe,
    et inutile ici — on ne veut que _parse_choices/migrate_choices_in_json)."""
    if "customtkinter" not in sys.modules:
        stub = types.ModuleType("customtkinter")
        stub.set_appearance_mode = lambda *a, **k: None
        stub.set_default_color_theme = lambda *a, **k: None
        for cls in ("CTk", "CTkButton", "CTkEntry", "CTkFrame", "CTkLabel",
                    "CTkProgressBar", "CTkScrollableFrame", "CTkTabview",
                    "CTkTextbox"):
            setattr(stub, cls, type(cls, (), {}))
        sys.modules["customtkinter"] = stub
    spec = importlib.util.spec_from_file_location(
        "p2is_tool", os.path.join(_PROJ, "p2is_tool.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _rebuild_sur(tool, e):
    """Vrai si l'encodage via _rebuild_choice_body() est SUR pour cette entree :
    structure de codes identique a texte_orig (hors [SP]/pauses) et budget tenu.
    Exclut notamment les menus [1208][U+0003..5] (3-5 options) : _rebuild ecrit
    [0002] en dur, et les menus dont la derniere option est en texte nu. Pour
    les entrees exclues, l'encodeur retombe sur texte_fr (structure fidele)."""
    rebuilt = tool._rebuild_choice_body(e["question_fr"], e["choix_fr"])
    if _codes(rebuilt) != _codes(e.get("texte_orig", "")):
        return False
    return cost(e.get("nom_fr", ""), rebuilt) <= budget(e)


def migrate_dir(write=True):
    tool = _load_p2is_tool()
    stats = {"menus": 0, "remplis": 0, "partiels": [], "sans_texte_fr": 0,
             "deja_remplis": 0, "fichiers": 0, "exclus": []}
    for p in sorted(glob.glob(os.path.join(_PROJ, "traduction",
                                           "event_scripts", "script_*.json"))):
        with open(p, encoding="utf-8") as f:
            entries = json.load(f)
        before = {e["id"]: (e.get("question_fr", ""), list(e.get("choix_fr", [])))
                  for e in entries if "choix_orig" in e}
        stats["menus"] += len(before)
        stats["deja_remplis"] += sum(
            1 for q, c in before.values() if q or any(x.strip() for x in c))
        tool.migrate_choices_in_json(entries)
        changed = []
        for e in entries:
            if "choix_orig" not in e:
                continue
            if (e.get("question_fr", ""), e.get("choix_fr", [])) != before[e["id"]]:
                if not _rebuild_sur(tool, e):
                    # rebuild encodeur non fidele -> on laisse le fallback texte_fr
                    e["question_fr"], e["choix_fr"] = before[e["id"]]
                    stats["exclus"].append((os.path.basename(p), e["id"]))
                    continue
                changed.append(e)
                if "" in e["choix_fr"] or len(e["choix_fr"]) != len(e["choix_orig"]):
                    stats["partiels"].append((os.path.basename(p), e["id"]))
            elif not e.get("texte_fr", "").strip():
                stats["sans_texte_fr"] += 1
        if changed:
            stats["remplis"] += len(changed)
            stats["fichiers"] += 1
            if write:
                with open(p, "w", encoding="utf-8") as f:
                    json.dump(entries, f, ensure_ascii=False, indent=2)
                    f.write("\n")
            print(f"{os.path.basename(p)}: +{len(changed)} menus remplis")
    return stats


def main(argv):
    write = "--dry-run" not in argv
    s = migrate_dir(write=write)
    print(f"\nTOTAL : {s['menus']} menus | {s['remplis']} remplis maintenant | "
          f"{s['deja_remplis']} deja remplis | {s['sans_texte_fr']} sans texte_fr")
    if s["partiels"]:
        print(f"PARTIELS (choix manquants ou en trop, a revoir) : {len(s['partiels'])}")
        for f, i in s["partiels"]:
            print(f"  {f} id={i}")
    if s["exclus"]:
        print(f"EXCLUS (rebuild encodeur non fidele -> fallback texte_fr) : "
              f"{len(s['exclus'])}")
        for f, i in s["exclus"]:
            print(f"  {f} id={i}")
    if not write:
        print("(dry-run : rien ecrit)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

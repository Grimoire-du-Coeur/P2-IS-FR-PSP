"""Scanne TOUS les scripts apparies et agrege les renommages de codes
au-dela des conversions connues. Lecture seule, n'ecrit rien."""
import os, sys, json, glob
sys.path.insert(0, os.path.dirname(__file__))
from transfer import detect_code_renames        # noqa: E402
from collections import Counter

_PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main():
    anc = Counter()
    nouv = Counter()
    for old_path in sorted(glob.glob(os.path.join(_PROJ, "scripts", "script_*.json"))):
        name = os.path.basename(old_path)
        new_path = os.path.join(_PROJ, "traduction", "event_scripts", name)
        if not os.path.exists(new_path):
            continue
        try:
            old = json.load(open(old_path, encoding="utf-8"))
            new = json.load(open(new_path, encoding="utf-8"))
        except Exception as e:
            print(f"SKIP {name}: {e}")
            continue
        if len(old) != len(new):
            print(f"DIVERGE {name}: tailles {len(old)} vs {len(new)}")
            continue
        d = detect_code_renames(old, new)
        anc.update(d["ancien_seul"])
        nouv.update(d["nouveau_seul"])

    print("\n=== Codes presents cote ANCIEN seulement (apres conversion connue) ===")
    for c, n in anc.most_common(40):
        print(f"  {c}: {n}")
    print("\n=== Codes presents cote NOUVEAU seulement ===")
    for c, n in nouv.most_common(40):
        print(f"  {c}: {n}")

if __name__ == "__main__":
    main()

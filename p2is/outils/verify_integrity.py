import json
import glob
import os

repo = r"c:\Users\tasda\Documents\Projets\Perso\Grimoire du Coeur\P2-IS-FR-PSP"
files = sorted(glob.glob(os.path.join(repo, "traduction", "EBOOT_decoupe", "EBOOT_Part*.json")))

total_entries = 0
syntax_errors = 0
unclosed_tags = 0
control_tag_mismatches = 0

for fpath in files:
    fname = os.path.basename(fpath)
    with open(fpath, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except Exception as ex:
            print(f"JSON SYNTAX ERROR in {fname}: {ex}")
            syntax_errors += 1
            continue

    for e in data:
        total_entries += 1
        orig = e['texte_orig']
        fr = e['texte_fr']

        # Check for broken tags like <FF03 or <0004 without closing >
        if ('<' in fr and '>' not in fr) or fr.count('<') != fr.count('>'):
            print(f"[{fname}] ID {e['id']}: Unbalanced angle brackets in FR: {fr!r}")
            unclosed_tags += 1

        # Check for broken square brackets [SP
        if ('[' in fr and ']' not in fr) or fr.count('[') != fr.count(']'):
            print(f"[{fname}] ID {e['id']}: Unbalanced square brackets in FR: {fr!r}")
            unclosed_tags += 1

print(f"Integrity Check: {total_entries} total entries inspected.")
print(f"Syntax errors: {syntax_errors}")
print(f"Tag issues: {unclosed_tags}")


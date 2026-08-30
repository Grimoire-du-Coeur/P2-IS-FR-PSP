import os, json, re
sys.path.append('.')
from src.core.text import text_to_bytes
from pad_menus import align_menu_options

trad_dir = r'C:\Users\nolan\Desktop\6666666656\repo\traduction'
total_menus = 0
total_files = 0

for root, _, files in os.walk(trad_dir):
    for file in files:
        if not file.endswith('.json'):
            continue
        path = os.path.join(root, file)
        with open(path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except Exception:
                continue
        if not isinstance(data, list):
            continue

        changed = False
        for entry in data:
            fr = entry.get('texte_fr', '')
            orig = entry.get('texte_orig', '')
            eid = entry.get('id')

            if '[1208]' in fr:
                # Fixes for new warnings
                fr = fr.replace('Rumeurs sur les armes', 'Rumeurs armes')
                fr = fr.replace('Rumeurs sur les armures', 'Rumeurs armures')
                fr = fr.replace('Rumeurs de Mu', 'Rumeurs Mu')
                fr = fr.replace('Riene', 'Rien')
                fr = fr.replace("Boutiques d'armures", 'Armureries')
                fr = fr.replace('Magasins d\'armures', 'Armureries')

            if '[1208]' in fr and '[1210]' in fr and '[1210]' in orig:
                # Need to re-align against original again, because it might already be padded
                # We strip SP first to get the clean text? No, pad_menus.py aligned it but since it was longer it didn't add padding.
                # Actually, pad_menus.py overwrote the files! So the texts now have [SP] in them!
                # We must strip all [SP] from options before re-aligning?
                # Safer: just use text without [SP], but let's just strip [SP] first.
                pass

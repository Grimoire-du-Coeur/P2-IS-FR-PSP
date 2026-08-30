import os, json
sys.path.append('.')
from src.core.text import text_to_bytes
from pad_menus import align_menu_options

trad_dir = r'C:\Users\nolan\Desktop\6666666656\repo\traduction'

# We map the exact ORIGINAL text to the PERFECT, shortened French text
toro_menus = {
    # ID 32
    'What[SP]can[SP]I[SP]do[SP]for[SP]you[SP]today?\n[1208][0003][1210][U+0475]Ask[SP]about[SP]rumors\nTalk[SP]with[SP]Toro\nNever[SP]mind':
    'Je peux vous aider?\n[1208][0003][1210][0475]Infos rumeurs\nParler à Toro\nRien',
    
    # ID 33
    'What[SP]do[SP]you[SP]want[SP]to[SP]know[SP]about?\n[1208][0004][1210][U+0476]Weapon[SP]shop[SP]rumors\n[1210][U+0477]Armor[SP]shop[SP]rumors\n[1210][U+0478]Other[SP]rumors\nNothing':
    'Sur quoi?\n[1208][0004][1210][0476]Rumeurs armureries\n[1210][0477]Rumeurs armures\n[1210][0478]Autres rumeurs\nRien',
    
    # ID 34
    'For[SP]which[SP]area?\n[1208][0005][1210][U+046A]Rengedai\n[1210][U+046B]Yumezaki\n[1210][U+046C]Aoba\n[1210][U+046D]Kounan\nNone':
    'Secteur?\n[1208][0005][1210][046A]Rengedai\n[1210][046B]Yumezaki\n[1210][046C]Aoba\n[1210][046D]Kounan\nRien',
    
    # ID 35
    'For[SP]which[SP]area?\n[1208][0005][1210][U+046E]Rengedai\n[1210][U+046F]Yumezaki\n[1210][U+0470]Aoba\n[1210][U+0471]Kounan\nNone':
    'Secteur?\n[1208][0005][1210][046E]Rengedai\n[1210][046F]Yumezaki\n[1210][0470]Aoba\n[1210][0471]Kounan\nRien',
    
    # ID 36
    'What[SP]do[SP]you[SP]want[SP]to[SP]know[SP]about?\n[1208][0004][1210][U+0472]Magazine[SP]sweepstakes[SP]rumors\n[1210][U+0473]Mu[SP]rumors\n[1210][U+0474]Legendary[SP]weapon[SP]rumors\nNone[SP]of[SP]them':
    'Sur quoi?\n[1208][0004][1210][0472]Tirages de magazines\n[1210][0473]Rumeurs Mu\n[1210][0474]Armes légendaires\nAucune'
}

chikarin_menus = {
    # script_343.json ID 19
    'What[SP]do[SP]you[SP]want[SP]to[SP]know[SP]about?\n[1208][0003][1210][U+0475]Ask[SP]about[SP]rumors\nTalk[SP]with[SP]Chikarin\nNever[SP]mind':
    'Sur quoi?\n[1208][0003][1210][0475]Infos rumeurs\nParler à Chikarin\nRien',
    
    # ID 20
    'What[SP]do[SP]you[SP]want[SP]to[SP]know[SP]about?\n[1208][0004][1210][U+0476]Weapon[SP]shop[SP]rumors\n[1210][U+0477]Armor[SP]shop[SP]rumors\n[1210][U+0478]Other[SP]rumors\nNothing':
    'Sur quoi?\n[1208][0004][1210][0476]Rumeurs armureries\n[1210][0477]Rumeurs armures\n[1210][0478]Autres rumeurs\nRien',
    
    # ID 21 (For which area) - identical to ID 34
    'For[SP]which[SP]area?\n[1208][0005][1210][U+046A]Rengedai\n[1210][U+046B]Yumezaki\n[1210][U+046C]Aoba\n[1210][U+046D]Kounan\nNone':
    'Secteur?\n[1208][0005][1210][046A]Rengedai\n[1210][046B]Yumezaki\n[1210][046C]Aoba\n[1210][046D]Kounan\nRien',
    
    # ID 22 (For which area) - identical to ID 35
    'For[SP]which[SP]area?\n[1208][0005][1210][U+046E]Rengedai\n[1210][U+046F]Yumezaki\n[1210][U+0470]Aoba\n[1210][U+0471]Kounan\nNone':
    'Secteur?\n[1208][0005][1210][046E]Rengedai\n[1210][046F]Yumezaki\n[1210][0470]Aoba\n[1210][0471]Kounan\nRien',
    
    # ID 23
    'What[SP]rumor[SP]do[SP]you[SP]want[SP]details[SP]on?\n[1208][0004][1210][U+0472]Magazine[SP]sweepstakes\n[1210][U+0473]Mu\n[1210][U+0474]Legendary[SP]weapons\nNone':
    'Laquelle ?\n[1208][0004][1210][0472]Tirages de magazines\n[1210][0473]Mu\n[1210][0474]Armes légendaires\nAucune'
}

all_menus = {**toro_menus, **chikarin_menus}

total_fixes = 0
files_changed = 0

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
            orig = entry.get('texte_orig', '')
            if orig in all_menus:
                new_fr = all_menus[orig]
                padded_fr = align_menu_options(orig, new_fr, entry.get('id'))
                if entry.get('texte_fr') != padded_fr:
                    entry['texte_fr'] = padded_fr
                    changed = True
                    total_fixes += 1

        if changed:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            files_changed += 1

print(f"Fixed {total_fixes} Toro/Chikarin menus across {files_changed} files.")

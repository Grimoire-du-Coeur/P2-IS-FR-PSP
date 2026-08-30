import os, json, re

def get_options(text):
    parts = text.split('[1210]')
    return parts[1:] if len(parts) > 1 else []

def text_to_bytes_dummy(text):
    t = text
    tags = re.findall(r'\[[^\]]+\]', t)
    for tag in tags:
        t = t.replace(tag, '', 1)
    return (len(t) * 2) + (len(tags) * 2)

def align_menu_options(o_text, f_text, eid=None):
    if '[1210]' not in o_text or '[1210]' not in f_text:
        return f_text
    
    o_parts = o_text.split('[1210]')
    f_parts = f_text.split('[1210]')
    
    if len(o_parts) != len(f_parts):
        return f_text
        
    new_f_parts = [f_parts[0]]
    
    for i in range(1, len(o_parts)):
        o_part = o_parts[i]
        f_part = f_parts[i]
        
        o_len = text_to_bytes_dummy(o_part)
        f_len = text_to_bytes_dummy(f_part)
        
        diff = o_len - f_len
        
        if diff > 0:
            n_sp = diff // 2
            padding = '[SP]' * n_sp
            if '\n' in f_part:
                parts_nl = f_part.rsplit('\n', 1)
                f_part = parts_nl[0] + padding + '\n' + parts_nl[1]
            else:
                f_part = f_part + padding
            
        new_f_parts.append(f_part)
        
    return '[1210]'.join(new_f_parts)

trad_dir = r'C:\Users\nolan\Desktop\6666666656\repo\traduction'
total_menus = 0

for root, _, files in os.walk(trad_dir):
    for file in files:
        if not file.endswith('.json'):
            continue
        path = os.path.join(root, file)
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        changed = False
        for entry in data:
            fr = entry.get('texte_fr', '')
            orig = entry.get('texte_orig', '')
            eid = entry.get('id')

            if '[1208]' in fr:
                # Remove SP from menus because we will recalculate it
                fr = fr.replace('[SP]', '')
                # Fix specific overly long menu choices
                replacements = {
                    '[0476]Rumeurs sur les armes': '[0476]Rumeurs: armes',
                    '[0477]Rumeurs sur les armures': '[0477]Rumeurs: armures',
                    '[0473]Rumeurs de Mu': '[0473]Rumeurs Mu',
                    "[0477]Magasins d'armures": '[0477]Mag. armures',
                    '[0475]Demander des rumeurs\nTirer les cartes': '[0475]Infos rumeurs\nTirer cartes',
                    '[046D]Kounan\nRiene': '[046D]Kounan\nRien',
                    '[0471]Kounan\nRiene': '[0471]Kounan\nRien',
                    'Théâtre Climax\nParler\nQuitter le théâtre': 'Climax\nParler\nQuitter',
                    'Armure de jambes': 'Jambes',
                    'Muter Persona\nParler à Igor\nAnnuler\nQuitter': 'Muter Persona\nParler\nAnnuler\nQuitter',
                    'Acheter accessoires\nVendre objets\nParler à la vendeuse\nLaisser tomber\nQuitter la boutique': 'Accessoires\nVendre\nParler\nRien\nQuitter',
                    'Sélection cachée\nATTENTION[E4][NULL][NULL]\nAucun bit actif. Vérifiez ceci.\n-KanadaATTENTION[E4][NULL][NULL]\nAucun bit actif. Vérifiez ceci.\n-Kanada': 'Sél. cachée\nATTENTION\nAucun bit actif.\n-Kanada',
                    'Slection cache': 'Sél. cachée',
                    'Films imports': 'Films',
                    'Films importés': 'Films'
                }
                for old, new in replacements.items():
                    fr = fr.replace(old, new)
                    
            if '[1208]' in fr and '[1210]' in fr and '[1210]' in orig:
                new_fr = align_menu_options(orig, fr, eid)
                
                if new_fr != entry.get('texte_fr', ''):
                    entry['texte_fr'] = new_fr
                    changed = True
                    total_menus += 1

        if changed:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Aligned {total_menus} menus.")

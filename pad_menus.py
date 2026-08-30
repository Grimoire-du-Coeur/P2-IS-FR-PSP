import os, json, re

def get_options(text):
    parts = text.split('[1210]')
    return parts[1:] if len(parts) > 1 else []

def text_to_bytes_dummy(text):
    # Quick approximation for length in P2 (UTF-16 LE)
    # Tags like [XXXX] are 2 bytes. Regular chars are 2 bytes. \n is 2 bytes.
    # Note: this is a precise replica of what text_to_bytes would return in length
    # Remove tags from length, add 2 for each tag
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
        elif diff < 0:
            print(f"WARNING ID {eid}: Option {i} is LONGER by {-diff} bytes! O={o_len} F={f_len}")
            print(f"  F: {f_part.strip()}")
            
        new_f_parts.append(f_part)
        
    return '[1210]'.join(new_f_parts)

# Apply fixes to all translation files
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

            # Manual shortenings to prevent overflow BEFORE aligning
            if '[1208]' in fr:
                if 'Demander des rumeurs\nParler avec Toro' in fr:
                    fr = fr.replace('Demander des rumeurs', 'Infos rumeurs')
                    fr = fr.replace('Parler avec Toro', 'Parler à Toro')
                    fr = fr.replace('Non merci', 'Rien')
                
                if '[046D]Kounan\nAucun' in fr:
                    fr = fr.replace('[046D]Kounan\nAucun', '[046D]Kounan\nRien')
                if '[0471]Kounan\nAucun' in fr:
                    fr = fr.replace('[0471]Kounan\nAucun', '[0471]Kounan\nRien')
                
                if '[0473]Rumeurs sur Mu' in fr:
                    fr = fr.replace('[0473]Rumeurs sur Mu', '[0473]Rumeurs Mu')

            if '[1208]' in fr and '[1210]' in fr and '[1210]' in orig:
                new_fr = align_menu_options(orig, fr, eid)
                if new_fr != entry.get('texte_fr', ''):
                    entry['texte_fr'] = new_fr
                    changed = True
                    total_menus += 1

        if changed:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            total_files += 1

print(f"Aligned {total_menus} menus across {total_files} files.")

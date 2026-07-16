import json
import os
import re
import glob
import math

def get_visual_length(word):
    # Enleve les balises du type [1432][NULL][NULL][0014] etc
    # Mais on donne un poids aux noms des heros pour eviter les debordements !
    word = word.replace('[1113]', 'Tatsuya')
    word = word.replace('[1112]', 'Suou')
    clean_word = re.sub(r'\[[a-zA-Z0-9+\-_]+\]', '', word)
    return len(clean_word)

def balanced_wrap(text, max_len=46):
    text = text.replace('\n', ' ')
    text = re.sub(r'\s+', ' ', text).strip()
    if not text: return []
    words = text.split(' ')
    
    total_len = sum(get_visual_length(w) for w in words) + len(words) - 1
    if total_len <= max_len:
        return [text]
    
    N = math.ceil(total_len / max_len)
    ideal_len = total_len / N
    
    best_lines = []
    
    for target in range(int(ideal_len), max_len + 1):
        lines = []
        current_line = []
        current_len = 0
        
        for w in words:
            vlen = get_visual_length(w)
            if current_len + vlen + (1 if current_line else 0) > target and current_line:
                lines.append(' '.join(current_line))
                current_line = [w]
                current_len = vlen
            else:
                current_line.append(w)
                current_len += vlen + (1 if len(current_line) > 1 else 0)
        if current_line:
            lines.append(' '.join(current_line))
            
        if len(lines) <= N:
            best_lines = lines
            break
            
    if not best_lines:
        best_lines = lines
        
    for i in range(len(best_lines)):
        best_lines[i] = re.sub(r'^(\[[a-zA-Z0-9+\-_]+\](?:\[[a-zA-Z0-9+\-_]+\])*)\s+', r'\1', best_lines[i])
        
    return best_lines

def fix_missing_spaces(text):
    # Ajoute un espace manquant après la ponctuation (.?!) 
    # suivie (éventuellement par des balises) d'une lettre
    pattern = r'([.?!]+(?:\[[a-zA-Z0-9+\-_]+\])*)([A-ZÀ-Ÿa-zà-ÿ])'
    return re.sub(pattern, r'\1 \2', text)

def format_french_text(texte_fr):
    if not texte_fr:
        return texte_fr
        
    # S'il y a deja des balises de menu ou autres trucs speciaux on evite de tout casser
    if '[1208]' in texte_fr or '[U+1208]' in texte_fr:
        return texte_fr # On ne touche pas aux menus de choix
        
    texte_fr = fix_missing_spaces(texte_fr)
    lines = balanced_wrap(texte_fr, 46)
    return '\n'.join(lines)

def process_all_jsons(folder_path):
    files = glob.glob(os.path.join(folder_path, '**', '*.json'), recursive=True)
    count = 0
    for fpath in files:
        with open(fpath, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except:
                continue
                
        changed = False
        for entry in data:
            if 'texte_fr' in entry and entry['texte_fr']:
                old_fr = entry['texte_fr']
                new_fr = format_french_text(old_fr)
                if old_fr != new_fr:
                    entry['texte_fr'] = new_fr
                    changed = True
                    
        if changed:
            with open(fpath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            count += 1
            
    return count

if __name__ == "__main__":
    folder = r"C:\Users\nolan\Desktop\github_repo_temp\traduction"
    c = process_all_jsons(folder)
    print(f"Modifie {c} fichiers JSON.")

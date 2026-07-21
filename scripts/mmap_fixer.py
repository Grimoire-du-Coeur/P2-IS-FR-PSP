import json
import glob
import os
import re
import math

def get_visual_length(word):
    word = word.replace('[1113]', 'Tatsuya')
    word = word.replace('[1112]', 'Suou')
    clean_word = re.sub(r'\[[a-zA-Z0-9+\-_]+\]', '', word)
    return len(clean_word)

def clean_text(text):
    if not text: return text
    text = text.replace('\n', ' ')
    text = text.replace('[E1]', '').replace('[E2]', '').replace('[E3]', '').replace('[E4]', '')
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def balanced_wrap(text, max_len=46):
    text = clean_text(text)
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
    pattern = r'([.?!]+(?:\[[a-zA-Z0-9+\-_]+\])*)([A-ZÀ-Ÿa-zà-ÿ])'
    return re.sub(pattern, r'\1 \2', text)

def format_french_text_mmap(texte_fr):
    if not texte_fr:
        return texte_fr
        
    if '[1208]' in texte_fr or '[U+1208]' in texte_fr:
        return texte_fr 
        
    texte_fr = fix_missing_spaces(texte_fr)
    lines = balanced_wrap(texte_fr, 46)
    
    # Paginate every 3 lines!
    result = ""
    for i, line in enumerate(lines):
        result += line
        if i < len(lines) - 1:
            if (i + 1) % 3 == 0:
                result += "[E1][E2]\n"
            else:
                result += "\n"
    return result

def main():
    folder = "C:/Users/nolan/Desktop/P2IS_FR/traduction"
    for f_path in glob.glob(os.path.join(folder, "MMAP*.json")):
        with open(f_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        changed = False
        for entry in data:
            if 'texte_fr' in entry and entry['texte_fr']:
                old_fr = entry['texte_fr']
                new_fr = format_french_text_mmap(old_fr)
                if old_fr != new_fr:
                    entry['texte_fr'] = new_fr
                    changed = True
                    
        if changed:
            with open(f_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Updated {f_path}")

if __name__ == "__main__":
    main()

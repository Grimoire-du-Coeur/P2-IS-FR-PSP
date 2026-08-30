import os, json, re

def get_visible_length(text):
    clean = re.sub(r'\[[^\]]+\]', '', text)
    return len(clean)

def wrap_chunk(text, max_len=45):
    # Clean up text chunk
    text = text.replace('\n', ' ')
    text = re.sub(r'\s+', ' ', text).strip()
    
    words = text.split(' ')
    lines = []
    current_line = ""
    
    for word in words:
        if not current_line:
            current_line = word
        else:
            test_line = current_line + " " + word
            if get_visible_length(test_line) <= max_len:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
    if current_line:
        lines.append(current_line)
        
    return '\n'.join(lines)

def smart_paginate(text):
    # We must preserve [1205][000A] if it exists
    parts = text.split('[1205][000A]')
    wrapped_parts = [wrap_chunk(p) for p in parts]
    return '[1205][000A]'.join(wrapped_parts)

trad_dir = r'C:\Users\nolan\Desktop\6666666656\repo\traduction'
total_entries = 0

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
            if not fr: continue
            
            if '[1208]' in fr or '[1210]' in fr:
                continue
                
            new_fr = smart_paginate(fr)
            if new_fr != fr:
                entry['texte_fr'] = new_fr
                changed = True
                total_entries += 1

        if changed:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Paginated {total_entries} text entries.")

import os, json, re

def get_visible_length(text):
    # Remove all tags for length calculation
    clean = re.sub(r'\[[^\]]+\]', '', text)
    return len(clean)

def smart_paginate(text, max_len=43):
    # Split text by existing explicit page breaks or pauses if needed? 
    # Actually, let's just strip \n and re-wrap.
    # But preserve [1205][000A] if it exists? 
    # Let's replace [1205][000A] with a space, we will re-insert them naturally!
    # Wait, what if there's a forced pause [1205][000F]? Let's keep it attached to the preceding word.
    
    # Clean up text
    text = text.replace('\n', ' ')
    text = text.replace('[1205][000A]', ' ')
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Tokenize by words, but keep tags attached to words
    # A regex that matches a word (with potential tags inside/around it)
    # Actually, simpler: split by space.
    words = text.split(' ')
    
    lines = []
    current_line = ""
    
    for word in words:
        if not current_line:
            current_line = word
        else:
            # Check length if we add this word
            test_line = current_line + " " + word
            if get_visible_length(test_line) <= max_len:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
    if current_line:
        lines.append(current_line)
        
    # Now assemble the lines, inserting \n and [1205][000A]
    result = ""
    for i, line in enumerate(lines):
        if i > 0:
            if i % 3 == 0:
                # Every 3rd line break is a page break!
                result += "[1205][000A]"
            else:
                result += "\n"
        result += line
        
    return result

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
            
            # Skip menus for now to avoid breaking choices
            if '[1208]' in fr or '[1210]' in fr:
                # We can paginate the part before [1208]
                parts = fr.split('[1208]')
                if len(parts) == 2:
                    q_part = parts[0]
                    # Only paginate if there are no \n in the question? 
                    # Actually, some questions are 1 line, some are 2. 
                    # Let's just leave menus alone, they usually fit because we padded them.
                    continue
                continue
                
            new_fr = smart_paginate(fr)
            if new_fr != fr:
                entry['texte_fr'] = new_fr
                changed = True
                total_entries += 1

        if changed:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

print(f"Paginated {total_entries} text entries.")

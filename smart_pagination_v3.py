import os, json, re, math

def get_visible_length(text):
    clean = re.sub(r'\[[^\]]+\]', '', text)
    return len(clean)

def balanced_wrap(text, max_len=45):
    text = text.replace('\n', ' ')
    text = re.sub(r'\s+', ' ', text).strip()
    words = text.split(' ')
    if not words: return ""
    
    total_len = get_visible_length(text)
    num_lines = math.ceil(total_len / max_len)
    target_len = total_len / num_lines if num_lines > 0 else 0
    
    n = len(words)
    costs = [float('inf')] * (n + 1)
    costs[0] = 0
    breaks = [0] * (n + 1)
    
    for i in range(1, n + 1):
        for j in range(1, i + 1):
            line = ' '.join(words[j-1:i])
            length = get_visible_length(line)
            if length <= max_len:
                diff = abs(target_len - length)
                cost = costs[j-1] + (diff ** 2)
                if cost < costs[i]:
                    costs[i] = cost
                    breaks[i] = j - 1
            else:
                if j == i:
                    cost = costs[j-1] + 1000000
                    if cost < costs[i]:
                        costs[i] = cost
                        breaks[i] = j - 1

    lines = []
    curr = n
    while curr > 0:
        prev = breaks[curr]
        lines.append(' '.join(words[prev:curr]))
        curr = prev
    lines.reverse()
    return '\n'.join(lines)

def smart_paginate(text):
    # Split on original page breaks and preserve them
    parts = text.split('[1205][000A]')
    wrapped_parts = [balanced_wrap(p) for p in parts]
    return '[1205][000A]'.join(wrapped_parts)

trad_dir = r'C:\Users\nolan\Desktop\6666666656\repo\traduction\event_scripts'
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

print(f"Paginated {total_entries} text entries in event_scripts.")

import os, json

for root, _, files in os.walk('traduction'):
    for file in files:
        if file.endswith('.json'):
            path = os.path.join(root, file)
            changed = False
            with open(path, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                except:
                    continue
            
            if isinstance(data, list):
                for entry in data:
                    text = entry.get('texte_fr', '')
                    if '>' in text:
                        entry['texte_fr'] = text.replace('>', ' ')
                        changed = True
            
            if changed:
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)

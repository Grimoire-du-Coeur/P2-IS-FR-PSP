import json
import glob

files = glob.glob('C:/Users/nolan/Desktop/6666666656/repo/traduction/**/*.json', recursive=True)
count = 0

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        data = json.load(file)
        
    changed = False
    for entry in data:
        if 'texte_fr' in entry:
            original = entry['texte_fr']
            text = original
            text = text.replace('.[000F]..', '...')
            text = text.replace('.[1205].[000F].', '...[1205][000F]')
            text = text.replace('.[1205][000F]..', '...[1205][000F]')
            text = text.replace('[1205][000F]..', '...[1205][000F]')
            text = text.replace('[000F]Il ', 'Il ')
            text = text.replace('.[000F].', '..')
            text = text.replace('[1205].[000F].', '[1205][000F]')
            text = text.replace('Ëtes-vous', 'Êtes-vous')
            
            if text != original:
                entry['texte_fr'] = text
                changed = True
                count += 1
                
    if changed:
        with open(f, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

print(f'Fixed {count} text entries with mangled tags.')

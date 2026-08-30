import json
import glob
import re

files = glob.glob('C:/Users/nolan/Desktop/6666666656/repo/traduction/**/*.json', recursive=True)
count = 0

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        data = json.load(file)
        
    changed = False
    for entry in data:
        fr = entry.get('texte_fr', '')
        if not fr:
            continue
            
        original = fr
        
        # Fix [E1][E2] [E3][E4] replacing space with \n
        fr = fr.replace('[E1][E2] [E3][E4]', '[E1][E2]\n[E3][E4]')
        # In case there are other variations
        fr = fr.replace('[E1][E2] \n[E3][E4]', '[E1][E2]\n[E3][E4]')
        
        # Remove any [000F] that is NOT preceded by [1205]
        # Regex: find [000F] not preceded by [1205]
        # Wait, Python regex doesn't support variable length lookbehind, but we can just use a simple sub
        # We find all [000F]
        # We can split the string by [000F]
        # Or better: regex replacement
        # Find anything that is NOT `[1205]` followed by `[000F]`
        # We can just replace `[1205][000F]` with a temporary marker, then remove all remaining `[000F]`, then restore.
        fr = fr.replace('[1205][000F]', '%%VALID_000F%%')
        
        # Also, sometimes it's `[1205][000A]` we don't care about 000A, only 000F.
        
        # Wait, what if there are other valid tags before [000F]? Like [color][000F]?
        # Usually [000F] is just reset color.
        # But let's just remove orphaned [000F].
        fr = fr.replace('[000F]', '')
        fr = fr.replace('%%VALID_000F%%', '[1205][000F]')
        
        # Also clean up "chansonssont" typo from screenshot
        fr = fr.replace('chansonssont', 'chansons sont')
        
        if fr != original:
            entry['texte_fr'] = fr
            changed = True
            count += 1
            
    if changed:
        with open(f, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

print(f'Fixed {count} text entries.')

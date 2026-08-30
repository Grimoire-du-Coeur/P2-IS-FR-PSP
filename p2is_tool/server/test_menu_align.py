import sys, json, re
sys.path.append('.')
from src.core.text import text_to_bytes

def align_menu_options(o_text, f_text):
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
        
        o_len = len(text_to_bytes(o_part))
        f_len = len(text_to_bytes(f_part))
        
        diff = o_len - f_len
        
        if diff > 0:
            # Need to pad with [SP]. Each [SP] is 2 bytes.
            # But [SP] must be inserted BEFORE the \n if there is one, or at the end.
            n_sp = diff // 2
            padding = '[SP]' * n_sp
            
            if '\n' in f_part:
                # Insert before the newline of the NEXT option
                # Actually, the \n belongs to the CURRENT option if it's separating it from the NEXT option
                # Example: Opt1\n (next is [1210]Opt2)
                # We should insert [SP] before the \n
                parts_nl = f_part.rsplit('\n', 1)
                f_part = parts_nl[0] + padding + '\n' + parts_nl[1]
            else:
                f_part = f_part + padding
                
        elif diff < 0:
            # F is longer! We can't align it perfectly without truncating text.
            # We must warn and maybe truncate manually.
            print(f"WARNING: Option {i} is LONGER than original by {-diff} bytes! '{f_part.strip()}'")
            # For now, do not modify
            
        new_f_parts.append(f_part)
        
    return '[1210]'.join(new_f_parts)

with open(r'C:\Users\nolan\Desktop\6666666656\repo\traduction\event_scripts\script_382.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for e in data:
    if e['id'] in [32, 33, 34, 35, 36]:
        print(f"--- ID {e['id']} ---")
        new_fr = align_menu_options(e['texte_orig'], e['texte_fr'])
        print("OLD:", repr(e['texte_fr']))
        print("NEW:", repr(new_fr))

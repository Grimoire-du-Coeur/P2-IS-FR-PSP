import sys, json, os, glob
sys.path.append('C:/Users/nolan/Desktop/p2is_tool_to_push')
from src.core.text import text_to_bytes, _align_menu_text, _needs_nl_suffix
from src.parsers.bin_parser import _rebuild_choice_body

for f in glob.glob('C:/Users/nolan/Desktop/traduction/event_scripts/*.json') + glob.glob('C:/Users/nolan/Desktop/traduction/*.json'):
    if os.path.basename(f) == 'sys.json': continue
    try:
        data = json.load(open(f, encoding='utf-8'))
    except:
        continue
    if not isinstance(data, list): continue
    for d in data:
        n_fr_input = d.get('nom_fr', '').strip()
        t_fr_input = d.get('texte_fr', '').strip()
        choix_fr = d.get('choix_fr')
        q_fr = d.get('question_fr', '').strip()
        if choix_fr is not None:
            filled = [c for c in choix_fr if c.strip()]
            if q_fr and filled: t_fr = _rebuild_choice_body(q_fr, choix_fr)
            elif not t_fr_input: continue
            else: t_fr = t_fr_input
        elif not n_fr_input and not t_fr_input: continue
        else: t_fr = t_fr_input or d.get('texte_orig', '').strip()
        n_fr = n_fr_input or d.get('nom_orig', '').strip()
        t_fr = _align_menu_text(d.get('nom_orig', ''), d.get('texte_orig', ''), n_fr, t_fr)
        enc = text_to_bytes('"' + n_fr + '\n' + t_fr)
        nl_sfx = 2 if _needs_nl_suffix(d.get('_term', []), d.get('texte_orig', '')) else 0
        avail = d.get('data_size', 0) - 8
        if avail > 0 and len(enc) + nl_sfx > avail:
            print(f"{os.path.basename(f)}|{d['id']}|{len(enc)+nl_sfx}|{avail}")

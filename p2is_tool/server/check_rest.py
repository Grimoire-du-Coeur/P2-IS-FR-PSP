import sys
sys.path.append('.')
from src.core.text import text_to_bytes

orig_rest = '[1208][0003][1210][U+0475]Ask[SP]about[SP]rumors\nTalk[SP]with[SP]Toro\nNever[SP]mind'
fr_rest = '[1208][0003][1210][0475]Demander des rumeurs\nParler avec Toro\nNon merci'
print('ORIG rest:', len(text_to_bytes(orig_rest)))
print('FR rest:', len(text_to_bytes(fr_rest)))

orig_rest33 = '[1208][0004][1210][U+0476]Weapon[SP]shop[SP]rumors\n[1210][U+0477]Armor[SP]shop[SP]rumors\n[1210][U+0478]Other[SP]rumors\nNothing'
fr_rest33 = '[1208][0004][1210][0476]Rumeurs armureries\n[1210][0477]Rumeurs armures\n[1210][0478]Autres rumeurs\nRien'
print('ORIG rest 33:', len(text_to_bytes(orig_rest33)))
print('FR rest 33:', len(text_to_bytes(fr_rest33)))

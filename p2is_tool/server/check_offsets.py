import sys
sys.path.append('.')
from src.core.text import text_to_bytes

nom_orig_32 = 'Rumormonger Toro'
nom_fr_32 = "Toro l'informateur"

o = '"' + nom_orig_32 + '\nWhat[SP]can[SP]I[SP]do[SP]for[SP]you[SP]today?\n'
f = '"' + nom_fr_32 + '\nJe peux vous aider?\n'
print('ID 32 orig len:', len(text_to_bytes(o)))
print('ID 32 fr len:', len(text_to_bytes(f)))

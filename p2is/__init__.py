"""Le paquet P2IS : formats, parseurs, encodeurs et outils.

Rien ici n'importe tkinter. Les reglages d'interface sont dans
`labs/tool/ui_config.py`, et les tables du format dans `p2is.tables`.
"""

from pathlib import Path

# La racine du depot, calculee une fois. Chaque module la recalculait a sa
# facon, en empilant des dirname() dont le compte changeait a chaque
# deplacement de fichier.
RACINE = Path(__file__).resolve().parent.parent

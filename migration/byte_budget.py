import os
import sys

# Reutilise l'estimateur d'octets valide existant (DRY)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "json_verify"))
from utils import estimate_bytes  # noqa: E402


def cost(nom_fr, texte_fr):
    """Cout en octets d'une entree, identique a json_verify/cli.py. -1 si crochet non ferme."""
    return estimate_bytes('"' + nom_fr + "\n" + texte_fr + "\n")


def budget(entry):
    """Budget d'octets disponible pour une entree."""
    return entry.get("data_size", 8) - 8


def fits(entry, nom_fr, texte_fr):
    """Vrai si (nom_fr, texte_fr) tient dans le budget de l'entree."""
    c = cost(nom_fr, texte_fr)
    return c != -1 and c <= budget(entry)

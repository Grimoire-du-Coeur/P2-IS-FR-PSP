# -*- coding: utf-8 -*-
import re

_CODE_RE = re.compile(r"\[[^\]]*\]")
_WS_RE = re.compile(r"\s+")

def texte_nu(s):
    """Texte 'nu' pour comparaison : sans codes, [SP] et sauts de ligne -> espace."""
    s = s.replace("[SP]", " ")
    s = _CODE_RE.sub("", s)
    s = s.replace("\n", " ")
    s = _WS_RE.sub(" ", s).strip()
    return s

TRIGGERS = ["[1432]", "[1208]", "[E1]", "[E2]", "[E3]", "[E4]"]

_KNOWN_RENAMES = [("[U+1113]", "[1113]"), ("[U+1112]", "[1112]")]

def has_trigger(s):
    """Vrai si s contient un code menu / question-reponse."""
    return any(t in s for t in TRIGGERS)

def convert_fr(s):
    """Convertit les codes de l'ancien format FR vers le nouveau."""
    for old, new in _KNOWN_RENAMES:
        s = s.replace(old, new)
    return s

def extract_codes(s):
    """Liste ordonnee des codes [...] presents dans s."""
    return _CODE_RE.findall(s)

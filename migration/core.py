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

# Renommages connus ancien -> nouveau (map data-driven validee : le nouveau
# format retire U+ sur cette famille de codes, qui apparait aussi dans les texte_fr).
# Ordonner du plus long au plus court si la liste grandit (un prefixe pourrait
# corrompre un code plus long).
_KNOWN_RENAMES = [
    ("[U+0002]", "[0002]"),
    ("[U+1107]", "[1107]"),
    ("[U+1109]", "[1109]"),
    ("[U+1112]", "[1112]"),
    ("[U+1113]", "[1113]"),
    ("[U+1114]", "[1114]"),
    ("[U+111F]", "[111F]"),
    ("[U+1121]", "[1121]"),
    ("[U+1208]", "[1208]"),
    ("[U+120E]", "[120E]"),
    ("[U+1210]", "[1210]"),
    ("[U+121D]", "[121D]"),
]

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

def decide(old_e, new_e):
    """Retourne (status, reason) : 'auto' | 'pause' | 'untranslated'."""
    nom = old_e.get("nom_fr", "").strip()
    txt = old_e.get("texte_fr", "").strip()
    if not nom and not txt:
        return ("untranslated", "ancien non traduit")

    nu_match = texte_nu(old_e["texte_orig"]) == texte_nu(new_e["texte_orig"])
    trig = has_trigger(old_e["texte_orig"]) or has_trigger(new_e["texte_orig"])

    if nu_match and not trig:
        return ("auto", "")

    reasons = []
    if not nu_match:
        reasons.append("texte divergent")
    if trig:
        reasons.append("menu/Q-R")
    return ("pause", " + ".join(reasons))

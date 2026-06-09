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

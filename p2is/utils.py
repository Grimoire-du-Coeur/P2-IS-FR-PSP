#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P2IS FR Tool  ·  Persona 2 Innocent Sin PSP (EUR ULES01557)
============================================================
Outil de traduction fan-made : extraction, décodage, traduction, rebuild ISO.

Pipeline complet :
  ISO → P2PT_ALL.cpk → event.bin → scripts (0-398) → JSON à traduire
  JSON traduits → scripts encodés → event.bin patché → ISO finale

Fichiers supplémentaires : CD_SHOP.BIN · F_BE.BNP · TM_EVE.BNP · MMAP01-06.BNP

Auteurs : chenetulipe & GarloulouLeAsriel
GitHub  : https://github.com/chenetulipe/P2-FR-IS-PSP
"""

import json
from pathlib import Path
# Chemin du fichier d'offsets, pose par l'application qui ouvre un dossier de
# travail. C'etait une globale de `config.py`, le module d'INTERFACE : le
# decodeur lisait donc un reglage de fenetre pour savoir ou ecrire.
_fichier_offsets = ""


def set_offsets_file(chemin) -> None:
    """Declare ou vivent les offsets du dossier de travail courant."""
    global _fichier_offsets
    _fichier_offsets = str(chemin) if chemin else ""


def _offsets_path():
    return _fichier_offsets


def save_offsets(data: dict):
    # Convert any Path objects to strings before saving
    clean_data = {}
    for k, v in data.items():
        if hasattr(k, "__fspath__"):
            k = str(k)
        if hasattr(v, "__fspath__"):
            v = str(v)
        elif isinstance(v, dict):
            new_v = {}
            for k2, v2 in v.items():
                if hasattr(k2, "__fspath__"):
                    k2 = str(k2)
                if hasattr(v2, "__fspath__"):
                    v2 = str(v2)
                new_v[k2] = v2
            v = new_v
        clean_data[k] = v

    with open(_offsets_path(), "w", encoding="utf-8") as f:
        json.dump(clean_data, f, indent=2)


def load_offsets() -> dict:
    """Charge les offsets sauvegardés, ou retourne des valeurs par défaut."""
    p = _offsets_path()
    if p and Path(p).exists():
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"iso_path": "", "cpk_offset_in_iso": -1}


# ── Constantes Atlus PSP ──────────────────────────────────────────────────────
SP = 0x1120  # espace
NL = 0x1101  # saut de ligne
E1 = 0x1106  # terminateur partiel 1
E2 = 0x1102  # terminateur partiel 2
E3 = 0x1103  # terminateur partiel 3
E4 = 0x1431  # terminateur partiel 4 / marqueur animation F_BE
CHAIN_E1 = 0x1109  # variante E1

CTRL = {
    SP: "[SP]",
    NL: "\n",
    E1: "[E1]",
    E2: "[E2]",
    E3: "[E3]",
    E4: "[E4]",
    CHAIN_E1: "[1109]",
    0x1205: "[1205]",
    0x001E: "[001E]",
    0x1432: "[1432]",
    0x0014: "[0014]",
    0x0002: "[0002]",
    0x0010: "[0010]",
    0x0000: "[NULL]",
    0x1107: "[1107]",
    0x1108: "[1108]",
    0x120C: "[120C]",
    0x120D: "[120D]",
    0x120E: "[120E]",
    0x120F: "[120F]",
    0x1208: "[1208]",
    0x1210: "[1210]",
    0x1112: "[1112]",
    0x1113: "[1113]",
    0x121E: "[121E]",
}

# Correspondances accents FR → glyphes japonais disponibles dans la police du jeu
ACCENT_MAP = [
    ("é", "Ğ"),
    ("è", "ò"),
    ("ê", "¿"),
    ("ô", "Æ"),
    ("É", "Ņ"),
    ("È", "Ũ"),
    ("Î", "£"),
    ("Ô", "ō"),
    ("Û", "ĵ"),
    ("œ", "ë"),
    ("Œ", "Ǩ"),
    ("ü", "Ȗ"),
    ("ï", "ˠ"),
]

# Magic bytes de fichiers binaires non-dialogue
BINARY_MAGICS = (
    b"MIG.",
    b"VAGp",
    b"SGXD",
    b"RIFF",
    b"PMF\x00",
    b"PSMF",
    b"\x89PNG",
    b"BM\x00\x00",
)

# Fichiers à scanner dans cpk_files/
SCAN_TARGETS = {
    "cd_shop.bin",
    "f_be.bnp",
    "tm_eve.bnp",
    "mmap*.bnp",
    "f*.bin",
    "dun*.bnp",
    "shop*.bnp",
}

# ── Décodeur F_BE / TM_EVE ────────────────────────────────────────────────────
#
# Format animation Atlus PSP :
#   [E4](2 octets) + 5 octets de paramètres d'animation → sauter +7 au total
#   Timing marks inline (1 octet isolé, ex: 0x3B, 0x7F) → sauter +1
#   [1107] → fin de slot
#   Plusieurs prises de parole par slot → split sur '"'

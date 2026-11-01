#!/usr/bin/env python3
"""Les tables du format Atlus : opcodes, accents, magics.

Rien ici ne depend de l'interface. C'est volontaire : ce module etait
auparavant la moitie de `config.py`, qui importait tkinter et customtkinter et
posait le theme a l'import. Un simple verificateur de depassements ne pouvait
donc pas tourner sans une bibliotheque de fenetres installee, et la CI ne
pouvait rien verifier du tout.

Les balises decodees ici ne doivent jamais disparaitre d'une traduction :
`[NULL]` decale un pointeur, `[E4]` termine un dialogue, `[1432]` place le
curseur d'un menu. Voir docs/DEVELOPER.md.
"""

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
    0x0001: "[0001]",
    0x0002: "[0002]",
    0x0003: "[0003]",
    0x0004: "[0004]",
    0x0005: "[0005]",
    0x0006: "[0006]",
    0x0007: "[0007]",
    0x0008: "[0008]",
    0x0009: "[0009]",
    0x000A: "[000A]",
    0x000B: "[000B]",
    0x000C: "[000C]",
    0x000D: "[000D]",
    0x000F: "[000F]",
    0x0010: "[0010]",
    0x0014: "[0014]",
    0x0159: "[0159]",
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
    ("È", "Ņ"),
    ("Î", "£"),
    ("Ô", "ō"),
    ("Û", "ĵ"),
    ("œ", "ë"),
    ("Œ", "Ǩ"),
    ("ü", "ˠ"),
    ("ï", "Ȗ"),
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

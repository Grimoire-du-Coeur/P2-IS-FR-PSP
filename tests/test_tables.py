"""Les tables du format Atlus : ce qui doit rester vrai.

Une balise qui disparait d'ici, c'est un opcode qui ne se decode plus et qui
ressort en `[U+XXXX]` -- ou pire, qui se perd au reencodage.
"""

from p2is.tables import (
    ACCENT_MAP,
    BINARY_MAGICS,
    CHAIN_E1,
    CTRL,
    E1,
    E2,
    E3,
    E4,
    NL,
    SP,
)

# Ce que docs/DEVELOPER.md classe comme cassant si la balise se perd.
CRITIQUES = {
    0x0000: "[NULL]",   # decale un pointeur
    0x1431: "[E4]",     # terminateur de dialogue
    0x1432: "[1432]",   # position du curseur de menu
    0x0014: "[0014]",   # fin de chaine d'une option de choix
    0x1208: "[1208]",   # ouverture d'un menu de choix
    0x1113: "[1113]",   # prenom du heros
}


def test_les_balises_critiques_sont_toutes_dans_la_table():
    for code, balise in CRITIQUES.items():
        assert code in CTRL, f"{balise} ({code:#06x}) a disparu de CTRL"
        assert CTRL[code] == balise, f"{code:#06x} rend {CTRL[code]!r}, attendu {balise!r}"


def test_aucune_balise_ne_sort_deux_fois_du_decodeur():
    """Deux opcodes qui rendent le meme texte rendent le reencodage ambigu."""
    vus = {}
    for code, balise in CTRL.items():
        assert balise not in vus, (
            f"{balise!r} est rendu par {code:#06x} et par {vus[balise]:#06x}"
        )
        vus[balise] = code


def test_les_terminateurs_sont_distincts():
    termes = [SP, NL, E1, E2, E3, E4, CHAIN_E1]
    assert len(set(termes)) == len(termes), "deux terminateurs partagent un code"


def test_la_table_d_accents_est_bijective():
    """Deux accents sur le meme glyphe rendraient la relecture impossible."""
    gauche = [a for a, _ in ACCENT_MAP]
    droite = [g for _, g in ACCENT_MAP]
    assert len(set(gauche)) == len(gauche), "un accent est declare deux fois"
    doublons = {g for g in droite if droite.count(g) > 1}
    # E et E accent grave partagent volontairement un glyphe : la police du jeu
    # n'en a qu'un. Toute autre collision est une erreur.
    assert doublons <= {"Ņ"}, f"glyphes partages inattendus : {doublons}"


def test_les_magics_binaires_sont_des_octets():
    assert BINARY_MAGICS, "la liste est vide : tout fichier passerait pour du dialogue"
    for m in BINARY_MAGICS:
        assert isinstance(m, bytes), f"{m!r} n'est pas des octets"

"""Le codec de texte : ce qu'il garantit, et ce qu'il ne garantit pas.

Le cycle n'est pas symetrique : une espace s'encode comme `SP` et se relit
`[SP]`, un accent passe par le glyphe japonais de la police du jeu et se relit
`[U+XXXX]`. L'invariant qui compte n'est donc pas `decode(encode(t)) == t`,
c'est la STABILITE : un deuxieme tour ne doit plus rien changer aux octets.
Sans elle, reouvrir un JSON pour corriger une virgule suffirait a faire deriver
le patch.
"""

import pytest

from p2is.core.text import decode_text, text_to_bytes

ECHANTILLONS = [
    "Bonjour[SP]Maya",
    "Attends ![E1][E2][E3]",
    "Oui[SP]ou[SP]non ?[1205]",
    "Eikichi\nLe Roi du Casino",
    "[NULL]",
    "Tu[SP]viens ?[1208][0014]",
    "",
]


@pytest.mark.parametrize("texte", ECHANTILLONS)
def test_le_deuxieme_tour_ne_change_plus_les_octets(texte):
    premier = text_to_bytes(texte)
    relu = decode_text(premier)
    assert text_to_bytes(relu) == premier


@pytest.mark.parametrize("texte", ECHANTILLONS)
def test_relire_deux_fois_donne_le_meme_texte(texte):
    relu = decode_text(text_to_bytes(texte))
    assert decode_text(text_to_bytes(relu)) == relu


def test_les_balises_de_controle_traversent_l_encodeur():
    """Une balise perdue ici, c'est un dialogue casse dans le jeu."""
    for balise in ("[NULL]", "[E4]", "[1432]", "[0014]", "[1208]", "[1113]"):
        assert balise in decode_text(text_to_bytes(f"a{balise}b")), f"{balise} perdue"


def test_une_espace_devient_SP():
    assert decode_text(text_to_bytes("a b")) == "a[SP]b"


def test_le_saut_de_ligne_survit():
    assert "\n" in decode_text(text_to_bytes("a\nb"))

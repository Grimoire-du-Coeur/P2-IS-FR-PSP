"""Chaque encodeur doit reellement modifier les octets qu'il ecrit.

Le bug de `fbe_encoder` a survecu des mois parce qu'aucun test ne verifiait
cette evidence : il travaillait sur une copie du slot, le fichier sortait
intact, et le resume annoncait « N injectes ». Les balises etaient en place,
les longueurs tenaient, `verify_json` ne regarde que le JSON. Rien ne pouvait
le voir.

Ces tests ferment le trou pour les trois encodeurs que `pipeline.encode_all`
utilise reellement :

    encode_bin_from_json   -> CD_SHOP.BIN et les scripts d'evenement
    encode_bnp_from_json   -> MMAP01-06 (entrees sans bloc gzip)
    encode_fbe_bnp_from_json -> F_BE.BNP et TM_EVE.BNP (couvert en detail
                                dans test_fbe_encoder.py)

Le controle est un aller-retour : on encode, puis on relit avec le parseur du
projet et on compare le texte decode. Comparer des octets bruts ne marcherait
pas, l'espace devenant la balise [SP] et non 0x0020.
"""

import json
import struct

import pytest

from p2is.encoders.bin_encoder import encode_bin_from_json, encode_bnp_from_json
from p2is.parsers.bin_parser import find_dialogs
from p2is.tables import E1, E2, E3, E4, NL

GUILLEMET = 0x0022  # ouvre un dialogue dans le format Atlus


def _mot(valeur: int) -> bytes:
    return struct.pack("<H", valeur)


def _texte(chaine: str) -> bytes:
    return b"".join(_mot(ord(c)) for c in chaine)


def dialogue(nom: str, corps: str) -> bytes:
    """Un dialogue minimal que `find_dialogs` reconnait.

    Structure : guillemet, nom, saut de ligne, texte, terminateur en quatre
    mots. Les zeros autour simulent le remplissage du fichier reel.
    """
    return (
        _mot(GUILLEMET)
        + _texte(nom)
        + _mot(NL)
        + _texte(corps)
        + _mot(E1) + _mot(E2) + _mot(E3) + _mot(E4)
    )


def fichier_test(tmp_path, nom="Maya", corps="Hello everyone, how are you?"):
    chemin = tmp_path / "source.BIN"
    chemin.write_bytes(b"\x00" * 16 + dialogue(nom, corps) + b"\x00" * 16)
    return chemin


def ecrire_json(tmp_path, source, nom_fr, texte_fr):
    """Produit le JSON comme le fait le pipeline : on relit le binaire.

    `encode_bnp_from_json` travaille sur les entrees telles quelles et a besoin
    de leur offset, de leur taille de slot et de leur terminateur. Les fabriquer
    a la main figerait ici des details de format ; les demander au parseur, qui
    est la source de verite, reproduit le vrai trajet extraction -> traduction
    -> reinjection.
    """
    entrees = find_dialogs(source.read_bytes())
    assert entrees, "le binaire de test n'est pas reconnu par le parseur"
    entrees[0]["nom_fr"] = nom_fr
    entrees[0]["texte_fr"] = texte_fr

    chemin = tmp_path / "trad.json"
    chemin.write_text(json.dumps(entrees, ensure_ascii=False), encoding="utf-8")
    return chemin


def texte_relu(octets: bytes) -> str:
    """Texte du premier dialogue, balises [SP] ramenees a des espaces.

    Le remplissage de fin est retire : un slot a une taille fixe, et les
    encodeurs completent la place restante avec des espaces. C'est voulu, et
    ce n'est pas ce que ces tests surveillent.
    """
    trouves = find_dialogs(octets)
    assert trouves, "le parseur ne retrouve plus aucun dialogue apres encodage"
    return trouves[0]["texte_orig"].replace("[SP]", " ").rstrip()


# Les deux encodeurs partagent la meme signature et la meme logique pour une
# entree sans bloc gzip : on leur fait passer les memes epreuves.
ENCODEURS = [
    pytest.param(encode_bin_from_json, id="bin_CD_SHOP_et_scripts"),
    pytest.param(encode_bnp_from_json, id="bnp_MMAP"),
]


@pytest.mark.parametrize("encodeur", ENCODEURS)
def test_la_traduction_atteint_le_fichier(tmp_path, encodeur):
    """L'invariant qui manquait : les octets ecrits changent vraiment."""
    source = fichier_test(tmp_path)
    carte = ecrire_json(tmp_path, source, "Maya", "Salut tout le monde, ca va?")
    sortie = tmp_path / "sortie.BIN"

    encodeur(str(source), str(carte), log_fn=None, out_path=str(sortie))
    octets = sortie.read_bytes()

    assert octets != source.read_bytes(), "le fichier ecrit est reste identique"
    assert texte_relu(octets) == "Salut tout le monde, ca va?"


@pytest.mark.parametrize("encodeur", ENCODEURS)
def test_la_taille_du_fichier_ne_bouge_pas(tmp_path, encodeur):
    """Les pointeurs du jeu sont absolus : rien ne doit se decaler."""
    source = fichier_test(tmp_path)
    carte = ecrire_json(tmp_path, source, "Maya", "Salut tout le monde, ca va?")
    sortie = tmp_path / "sortie.BIN"

    encodeur(str(source), str(carte), log_fn=None, out_path=str(sortie))

    assert len(sortie.read_bytes()) == len(source.read_bytes())


@pytest.mark.parametrize("encodeur", ENCODEURS)
def test_entree_non_traduite_laissee_intacte(tmp_path, encodeur):
    """Sans texte_fr, l'original doit survivre tel quel."""
    source = fichier_test(tmp_path)
    carte = ecrire_json(tmp_path, source, "", "")
    sortie = tmp_path / "sortie.BIN"

    encodeur(str(source), str(carte), log_fn=None, out_path=str(sortie))

    assert texte_relu(sortie.read_bytes()) == "Hello everyone, how are you?"


@pytest.mark.parametrize("encodeur", ENCODEURS)
def test_les_balises_de_controle_survivent(tmp_path, encodeur):
    """[1205] decale un pointeur : le perdre casse l'affichage en jeu."""
    source = fichier_test(tmp_path)
    carte = ecrire_json(tmp_path, source, "Maya", "Tiens...[1205] te voila.")
    sortie = tmp_path / "sortie.BIN"

    encodeur(str(source), str(carte), log_fn=None, out_path=str(sortie))

    assert "[1205]" in texte_relu(sortie.read_bytes())


@pytest.mark.parametrize("encodeur", ENCODEURS)
def test_un_texte_trop_long_ne_deborde_pas(tmp_path, encodeur):
    """Un depassement doit etre tronque, jamais ecrase sur le voisin."""
    source = fichier_test(tmp_path)
    carte = ecrire_json(tmp_path, source, "Maya", "Z" * 400)
    sortie = tmp_path / "sortie.BIN"

    encodeur(str(source), str(carte), log_fn=None, out_path=str(sortie))

    assert len(sortie.read_bytes()) == len(source.read_bytes())

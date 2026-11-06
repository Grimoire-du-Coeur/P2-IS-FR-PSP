"""Garde-fou sur l'injection des repliques de combat (F_BE / TM_EVE).

L'encodeur a longtemps annonce « N injectes » en reecrivant le fichier
d'origine octet pour octet : il travaillait sur une copie du slot, obtenue par
tranchage d'un bytearray, et ne la reinjectait jamais dans le tampon final.
Il a ensuite fait planter les combats en ignorant les octets de longueur des
segments ([E4] 81 00 L, voir fbe_encoder.py).

Les fichiers de test reproduisent le vrai format : chaque replique est
precedee d'une commande de segment, et suivie de la commande suivante.
"""

import json

from p2is.core.text import text_to_bytes
from p2is.encoders.fbe_encoder import SEG, encode_fbe_bnp_from_json, encoder_bloc

NL = b"\x01\x11"
TAILLE_SLOT = 48


def _texte_complet(nom: str, texte: str) -> str:
    """Texte d'origine complete en [SP] pour que le bloc fasse TAILLE_SLOT octets."""
    corps = text_to_bytes('"' + nom) + NL + text_to_bytes(texte)
    assert len(corps) <= TAILLE_SLOT
    return texte + "[SP]" * ((TAILLE_SLOT - len(corps)) // 2)


def _bloc(nom: str, texte: str) -> bytes:
    octets = text_to_bytes('"' + nom + "\n" + _texte_complet(nom, texte))
    assert len(octets) == TAILLE_SLOT
    return octets


def _fichier(*blocs: bytes) -> bytes:
    """Commande de segment + bloc, pour chaque bloc, puis une commande finale."""
    out = b""
    for b in blocs:
        out += SEG + bytes([len(b) + 1]) + b
    return out + SEG + b"\x01"


def _entree(**extra):
    base = {
        "id": 1,
        "offset": 5,
        "data_size": TAILLE_SLOT,
        "slot_size": TAILLE_SLOT,
        "_sub_offset": 0,
        "_sub_len": TAILLE_SLOT,
        "nom_orig": "AA",
        "texte_orig": _texte_complet("AA", "BBBB"),
        "nom_fr": "",
        "texte_fr": "",
    }
    base.update(extra)
    return base


def _preparer(tmp_path, entrees, source_octets=None):
    source = tmp_path / "F_BE.BIN"
    sortie = tmp_path / "out.BIN"
    carte = tmp_path / "f.json"
    source.write_bytes(source_octets or _fichier(_bloc("AA", "BBBB")))
    carte.write_text(json.dumps(entrees, ensure_ascii=False), encoding="utf-8")
    encode_fbe_bnp_from_json(str(source), str(carte), log_fn=None, out_path=str(sortie))
    return source.read_bytes(), sortie.read_bytes()


def test_la_traduction_atteint_le_fichier(tmp_path):
    """Le bug historique : la sortie etait identique a l'entree."""
    avant, apres = _preparer(tmp_path, [_entree(nom_fr="ZZ", texte_fr="WWWW")])

    assert apres != avant, "le fichier ecrit est reste identique a l'original"
    assert text_to_bytes("ZZ") in apres, "le nom traduit est absent des octets"
    assert text_to_bytes("WWWW") in apres, "le texte traduit est absent des octets"


def test_la_taille_du_fichier_ne_bouge_pas(tmp_path):
    """Un slot a une taille fixe : la reinjection ne doit rien decaler."""
    avant, apres = _preparer(tmp_path, [_entree(nom_fr="ZZ", texte_fr="WWWW")])

    assert len(apres) == len(avant)
    assert apres[-5:] == avant[-5:], "la commande suivante a ete deplacee"


def test_entree_non_traduite_laissee_intacte(tmp_path):
    """Sans nom_fr ni texte_fr, l'original doit survivre."""
    avant, apres = _preparer(tmp_path, [_entree()])

    assert apres == avant


def test_plusieurs_repliques_a_la_suite(tmp_path):
    """Chaque replique ecrit a son propre decalage, sans ecraser la voisine."""
    source = _fichier(_bloc("AA", "BB"), _bloc("CC", "DD"))
    entrees = [
        _entree(id=1, offset=5, texte_orig=_texte_complet("AA", "BB"),
                nom_fr="ZZ", texte_fr="WW"),
        _entree(id=2, offset=5 + TAILLE_SLOT + 5, nom_orig="CC",
                texte_orig=_texte_complet("CC", "DD"), nom_fr="YY", texte_fr="VV"),
    ]
    _, octets = _preparer(tmp_path, entrees, source)

    assert text_to_bytes("ZZ") in octets
    assert text_to_bytes("YY") in octets, "la seconde replique a ete perdue"
    assert len(octets) == len(source)


def test_long_segment_avec_octet_de_longueur_intercale():
    """Au-dela de 128 octets, un octet de longueur est intercale dans le texte.

    Reconstruire la replique a partir de son propre texte doit redonner
    l'original a l'octet pres, octet intercale compris.
    """
    texte = "Lorem ipsum dolor sit amet, consectetur adipiscing elit sed do eiusmod tempor"
    corps = text_to_bytes('"AA\n' + texte)  # > 128 octets
    assert len(corps) > 128
    bloc = bytes([0x7F]) + corps[:128] + bytes([len(corps) - 128 + 1]) + corps[128:]
    source = SEG + bloc + SEG + b"\x01"
    entree = {"nom_orig": "AA", "texte_orig": texte, "nom_fr": "AA", "texte_fr": texte}

    nouveau, raison = encoder_bloc(source, 5, len(bloc) - 1, entree)

    assert raison == "ok"
    assert nouveau == source[4:5 + len(bloc) - 1]

"""Garde-fou sur l'injection des repliques de combat (F_BE).

L'encodeur a longtemps annonce « N injectes » en reecrivant le fichier
d'origine octet pour octet : il travaillait sur une copie du slot, obtenue par
tranchage d'un bytearray, et ne la reinjectait jamais dans le tampon final.
Rien ne le signalait, ni le resume, ni la CI.

Ces tests verifient le seul invariant qui compte : ce qui est demande finit
dans les octets ecrits.
"""

import json

from p2is.core.text import text_to_bytes
from p2is.encoders.fbe_encoder import encode_fbe_bnp_from_json

NL = b"\x01\x11"
REMPLISSAGE = b"\x20\x11"
TAILLE_SLOT = 48


def _slot(nom: str, texte: str) -> bytes:
    """Fabrique un slot <nom> NL <texte>, complete a TAILLE_SLOT octets."""
    corps = text_to_bytes(nom) + NL + text_to_bytes(texte)
    assert len(corps) <= TAILLE_SLOT
    return bytes(corps + REMPLISSAGE * ((TAILLE_SLOT - len(corps)) // 2))


def _preparer(tmp_path, entrees, nom: str = "AA", texte: str = "BBBB"):
    source = tmp_path / "F_BE.BIN"
    sortie = tmp_path / "out.BIN"
    carte = tmp_path / "f.json"
    source.write_bytes(_slot(nom, texte))
    carte.write_text(json.dumps(entrees, ensure_ascii=False), encoding="utf-8")
    encode_fbe_bnp_from_json(str(source), str(carte), log_fn=None, out_path=str(sortie))
    return source.read_bytes(), sortie.read_bytes()


def _entree(**extra):
    base = {
        "id": 1,
        "offset": 0,
        "data_size": TAILLE_SLOT,
        "slot_size": TAILLE_SLOT,
        "_sub_offset": 0,
        "_sub_len": TAILLE_SLOT,
        "nom_orig": "AA",
        "texte_orig": "BBBB",
        "nom_fr": "",
        "texte_fr": "",
    }
    base.update(extra)
    return base


def test_la_traduction_atteint_le_fichier(tmp_path):
    """Le bug historique : la sortie etait identique a l'entree."""
    avant, apres = _preparer(tmp_path, [_entree(nom_fr="ZZ", texte_fr="WWWW")])

    assert apres != avant, "le fichier ecrit est reste identique a l'original"
    assert text_to_bytes("ZZ") in apres, "le nom traduit est absent des octets"
    assert text_to_bytes("WWWW") in apres, "le texte traduit est absent des octets"


def test_la_taille_du_fichier_ne_bouge_pas(tmp_path):
    """Un slot a une taille fixe : la reinjection ne doit rien decaler."""
    avant, apres = _preparer(tmp_path, [_entree(nom_fr="ZZ", texte_fr="WWWW")])

    assert len(apres) == len(avant) == TAILLE_SLOT


def test_entree_non_traduite_laissee_intacte(tmp_path):
    """Sans nom_fr ni texte_fr, l'original japonais doit survivre."""
    avant, apres = _preparer(tmp_path, [_entree()])

    assert apres == avant


def test_plusieurs_sous_entrees_dans_un_meme_slot(tmp_path):
    """Chaque sous-entree ecrit a son propre decalage, sans ecraser la voisine."""
    source = tmp_path / "F_BE.BIN"
    sortie = tmp_path / "out.BIN"
    carte = tmp_path / "f.json"
    source.write_bytes(_slot("AA", "BB") + _slot("CC", "DD"))

    entrees = [
        _entree(id=1, _sub_offset=0, _sub_len=TAILLE_SLOT,
                nom_fr="ZZ", texte_fr="WW"),
        _entree(id=2, _sub_offset=TAILLE_SLOT, _sub_len=TAILLE_SLOT,
                nom_fr="YY", texte_fr="VV"),
    ]
    for entree in entrees:
        entree["data_size"] = TAILLE_SLOT * 2
        entree["slot_size"] = TAILLE_SLOT * 2
    carte.write_text(json.dumps(entrees, ensure_ascii=False), encoding="utf-8")

    encode_fbe_bnp_from_json(str(source), str(carte), log_fn=None, out_path=str(sortie))
    octets = sortie.read_bytes()

    assert text_to_bytes("ZZ") in octets
    assert text_to_bytes("YY") in octets, "la seconde sous-entree a ete perdue"
    assert len(octets) == TAILLE_SLOT * 2

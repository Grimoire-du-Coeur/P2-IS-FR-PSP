"""Garde-fous des formats de texte ajoutés en v0.3.1 :
conteneurs compressés « 01 02 » (DNGSCN, P_DEMO), messages hors dialogues des
scripts (profils, descriptions « > ») et Climax Theater (q00.bin, extraction)."""

import gzip
import struct

import pytest

from p2is.core.lz_bnp import ENTETE, ajuster, blocs, lz_compresser, lz_decompresser, reconstruire
from p2is.parsers.climax_parser import extraire_climax
from p2is.parsers.messages_parser import appliquer_messages, balises, trouver_messages

SP, NL = 0x1120, 0x1101


def _u16(*mots) -> bytes:
    return struct.pack(f"<{len(mots)}H", *mots)


def _texte(t: str) -> list:
    return [SP if c == " " else (NL if c == "\n" else ord(c)) for c in t]


def _conteneur(*donnees: bytes, marge: int = 0) -> bytes:
    out = bytearray()
    for x in donnees:
        comp = ajuster(lz_compresser(x), x, len(lz_compresser(x)) + marge)
        out += struct.pack("<BBHII", 1, 2, 0, ENTETE + len(comp), len(x)) + comp
        while len(out) % 4:
            out.append(0)
    return bytes(out)


TEXTE = ("Yeah, I saw her go upstairs a moment ago. Maybe she's on the third floor? " * 4).encode("utf-16-le")


def test_lz_aller_retour():
    comp = lz_compresser(TEXTE)
    assert len(comp) < len(TEXTE)
    assert lz_decompresser(comp) == TEXTE


@pytest.mark.parametrize("ajout", [0, 1, 2, 7, 30])
def test_ajuster_taille_exacte(ajout):
    comp = lz_compresser(TEXTE)
    long = ajuster(comp, TEXTE, len(comp) + ajout)
    assert len(long) == len(comp) + ajout
    assert lz_decompresser(long) == TEXTE


def test_ajuster_refuse_trop_gros():
    comp = lz_compresser(TEXTE)
    with pytest.raises(ValueError):
        ajuster(comp, TEXTE, len(comp) - 1)


def test_reconstruire_garde_les_positions():
    a, b = TEXTE, "Second block of text, a little different.".encode("utf-16-le") * 3
    d = _conteneur(a, b, marge=40)
    bl, _ = blocs(d)
    assert [x[3] for x in bl] == [a, b]
    nouveau = "Oui, je l'ai vue monter il y a un instant. Elle est peut-être au 3e.".encode("utf-16-le")
    nouveau = (nouveau * 10)[:len(a)]
    r = reconstruire(d, {0: nouveau})
    assert len(r) == len(d)
    bl2, _ = blocs(r)
    assert bl2[0][3] == nouveau and bl2[1][3] == b
    assert [x[:2] for x in bl2] == [x[:2] for x in bl]  # mêmes positions et tailles


def test_messages_trouves_et_reinjectes():
    script = _u16(0x1103, *_texte("> The door is tightly sealed."), 0x1106, 0x1102, 0x1103,
                  0x1431, 0, 0, 0x0010, *_texte("Takashi Hanya\n The new principal."), 0x1431, 0, 0, 0x0002,
                  0x1106, 0x1102)
    msgs = trouver_messages(script)
    textes = [t for _, _, t in msgs]
    assert "> The door is tightly sealed." in [t.replace("[SP]", " ") for t in textes]
    o, n, t = msgs[0]
    entree = {"offset": o, "taille": n, "texte_orig": t, "texte_fr": "> La porte est scellée."}
    out = appliquer_messages(script, script, [entree])
    assert len(out) == len(script)
    assert out[o:o + 4] == _u16(ord(">"), SP)
    # un texte trop long ou aux balises changées reste en anglais
    trop = dict(entree, texte_fr="> " + "x" * 200)
    assert appliquer_messages(script, script, [trop]) == script
    profil = [m for m in msgs if "Takashi" in m[2]][0]
    assert balises(profil[2]) == ["[1431]", "[NULL]", "[NULL]", "[0010]", "[1431]", "[NULL]", "[NULL]", "[0002]"]


def test_climax_extraction():
    def code(c):
        if c == " ":
            return 0x8140
        if c.isupper():
            return 0x00E0 + ord(c) - 65
        if c.islower():
            return 0x0101 + ord(c) - 97
        return {".": 0x0004, "?": 0x0008}[c]

    corps = _u16(0x1001, 0x0001, 0) + _u16(*[code(c) for c in "Maya"]) + _u16(0xFFFD, 0xFFFE, 0xFFFF, 0)
    corps += _u16(*[code(c) for c in "Where is this?"]) + _u16(0xFFFD, 0xFFFE, 0xFFFF)
    flux = gzip.compress(corps)
    data = struct.pack("<II", 64, 64 + len(flux)) + bytes(56) + flux
    textes = [e["texte_orig"] for e in extraire_climax(data)]
    assert "Maya" in textes
    assert "Where[SP]is[SP]this<0008>" in textes

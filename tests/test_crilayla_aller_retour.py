"""Compression CRILAYLA puis décompression : on doit retrouver le fichier exact (issue #595).

Quand la dernière copie de l'encodeur déborde dans l'en-tête non compressé de 256 octets,
l'ancien décodeur écrivait à un indice négatif, donc à la fin du fichier en Python :
les deux derniers octets ressortaient faux (0x3e3e au lieu de 0x0000 sur MMAP01.BNP).
"""
import random

import pytest

from p2is.core.compression import crilayla_compress
from p2is.core.cpk import decompress_crilayla
from p2is.core.cpk_image import decompress_crilayla as decompress_image

random.seed(595)
CAS = {
    "zeros": bytes(256) + bytes(40),
    "repetitif": bytes(256) + b"ABCDEFGH" * 64 + b"\x00\x00",
    "aleatoire": bytes(256) + bytes(random.getrandbits(8) for _ in range(3000)),
    "en_tete_repetee": b"P2IS" * 64 + b"P2IS" * 200 + b"\x00\x00\x00\x00",
    "court": bytes(256) + b"xyz\x00\x00",
}


@pytest.mark.parametrize("nom", CAS)
@pytest.mark.parametrize("decode", [decompress_crilayla, decompress_image])
def test_aller_retour(nom, decode):
    data = CAS[nom]
    assert decode(crilayla_compress(data, header_size=256)) == data

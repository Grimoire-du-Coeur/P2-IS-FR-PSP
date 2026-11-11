"""Garde-fou : l'injection de l'EBOOT ne doit jamais écrire au-delà du texte d'origine.

En v0.3.1, les 2 octets qui suivent le terminateur FFFF étaient pris pour du
bourrage et passés à FFFF. Dans les tables de l'EBOOT, ce sont des champs de
l'enregistrement (valeur 0 -> -1) : le jeu plantait (sortie du parc d'Aoba,
Velvet Room...)."""

import json
import struct

from p2is.parsers.eboot_parser import encode_string, inject_eboot


def test_rien_n_est_ecrit_apres_le_texte(tmp_path):
    texte = encode_string("No")
    champ = struct.pack(">H", 0x0000) + struct.pack(">H", 0x0012)  # champs de l'enregistrement
    data = bytearray(64) + texte + b"\xff\xff" + champ + bytearray(32)
    off = 64
    (tmp_path / "eboot.bin").write_bytes(bytes(data))
    entrees = [{"id": 0, "offset": off, "data_size": len(texte), "slot_size": len(texte),
                "texte_orig": "No", "texte_fr": "Non"}]
    (tmp_path / "e.json").write_text(json.dumps(entrees), encoding="utf-8")
    inject_eboot(str(tmp_path / "eboot.bin"), str(tmp_path / "e.json"), str(tmp_path / "out.bin"), lambda m: None)
    out = (tmp_path / "out.bin").read_bytes()
    fin = off + len(texte)
    assert out[:off] == bytes(data[:off])
    assert out[fin:] == bytes(data[fin:])  # terminateur et champs intacts
    assert len(out) == len(data)

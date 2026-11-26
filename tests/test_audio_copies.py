"""Issue #505 : une piste stockée en double (offsets différents) doit être
remplacée partout, sinon le jeu continue de jouer l'ancienne copie."""
import struct

from labs.audio.server.core.audio_format import inject_wav_into_bin, parse_bin_toc


def _bin(tmp_path):
    # TOC de 4 entrées (16 octets), puis 3 pistes de 16 octets : A, B, A (copie)
    a, b = b"A" * 16, b"B" * 16
    toc = struct.pack("<4I", 16, 32, 48, 0)
    p = tmp_path / "BGMALL.BIN"
    p.write_bytes(toc + a + b + a)
    return p


def test_copies_identiques_remplacees(tmp_path):
    src = _bin(tmp_path)
    out = tmp_path / "BGMALL_MOD.BIN"
    entries, toc_end = parse_bin_toc(str(src))
    assert inject_wav_into_bin(str(src), 0, b"N" * 16, entries, toc_end, str(out))
    data = out.read_bytes()
    assert data[16:32] == b"N" * 16  # piste 0
    assert data[32:48] == b"B" * 16  # piste 1 : intacte
    assert data[48:64] == b"N" * 16  # piste 2 : copie de la 0, remplacée aussi
    assert len(data) == src.stat().st_size


def test_piste_unique_seule(tmp_path):
    src = _bin(tmp_path)
    out = tmp_path / "BGMALL_MOD.BIN"
    entries, toc_end = parse_bin_toc(str(src))
    assert inject_wav_into_bin(str(src), 1, b"N" * 16, entries, toc_end, str(out))
    data = out.read_bytes()
    assert data[16:32] == b"A" * 16 and data[48:64] == b"A" * 16
    assert data[32:48] == b"N" * 16

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P2IS FR Tool  ·  Persona 2 Innocent Sin PSP (EUR ULES01557)
============================================================
Outil de traduction fan-made : extraction, décodage, traduction, rebuild ISO.

Pipeline complet :
  ISO → P2PT_ALL.cpk → event.bin → scripts (0-398) → JSON à traduire
  JSON traduits → scripts encodés → event.bin patché → ISO finale

Fichiers supplémentaires : CD_SHOP.BIN · F_BE.BNP · TM_EVE.BNP · MMAP01-06.BNP

Auteurs : chenetulipe & GarloulouLeAsriel
GitHub  : https://github.com/chenetulipe/P2-FR-IS-PSP
"""

import struct
def crilayla_decompress(data: bytes):
    """Décompresse un bloc CRILAYLA (compression propriétaire CRI Middleware)."""
    if len(data) >= 16 and data[0:8] == b"CRILAYLA":
        # Standard CRILAYLA header at the beginning
        unc = struct.unpack_from("<I", data, 8)[0]
        # Skip to payload
        header_sz = struct.unpack_from("<I", data, 12)[0]
        # In standard CRILAYLA, there is a 0x100 (256) byte header after the 16 byte header.
        # So payload starts at 16 + 256 = 272.
        start_offset = 272 if len(data) >= 272 + header_sz else 16
        payload = data[start_offset:start_offset+header_sz]
        csz = len(payload)
        rev = bytearray(payload[::-1])
    elif len(data) >= 16 and data[-16:-8] == b"CRILAYLA":
        # Padded CRILAYLA at the end
        unc = struct.unpack_from("<I", data, len(data) - 8)[0]
        csz = struct.unpack_from("<I", data, len(data) - 4)[0]
        cs = len(data) - 16 - csz
        if cs < 0 or csz == 0:
            return None
        rev = bytearray(data[cs : cs + csz][::-1])
    else:
        return None

    try:
        out = bytearray(unc)
        wp = unc
        rp = pool = left = 0

        def nb():
            nonlocal rp, pool, left
            if left == 0:
                if rp >= len(rev):
                    return 0
                pool = rev[rp]
                rp += 1
                left = 8
            left -= 1
            return (pool >> left) & 1

        def rn(n):
            v = 0
            for _ in range(n):
                v = (v << 1) | nb()
            return v

        while wp > 0 and rp < len(rev):
            if nb() == 0:
                if rp >= len(rev):
                    break
                wp -= 1
                out[wp] = rev[rp]
                rp += 1
            else:
                b2 = rn(2)
                if b2 == 3:
                    b3 = rn(3)
                    length = (b3 + 3) if b3 < 7 else (rn(8) + 10)
                else:
                    length = b2 + 2
                offset = rn(13) + 3
                for _ in range(length):
                    if wp <= 0:
                        break
                    wp -= 1
                    ref = wp + offset
                    out[wp] = out[ref] if ref < unc else 0
        return bytes(out)
    except:
        return None


def crilayla_compress(
    data: bytes,
    header_size: int = 0,
    max_offset: int = 8191,
    target_size: int = 0,
    max_chain: int = 128,
) -> bytes:
    """
    Compresse des données au format CRILAYLA. Supporte les en-têtes non compressés
    exigés par certains moteurs de jeu (ex: 256 octets pour les MMAP de Persona 2).
    """
    if header_size > len(data):
        header_size = len(data)
    HEADER = header_size
    n = len(data)

    class BitWriter:
        """Émule l'ordre exact de consommation de crilayla_decompress."""

        def __init__(self):
            self.out = bytearray()
            self.pool = 0
            self.nbits = 0
            self.pending_literals = []

        def _flush_pending(self):
            while self.pending_literals:
                self.out.append(self.pending_literals.pop(0))

        def write_bit(self, b):
            self.pool = (self.pool << 1) | b
            self.nbits += 1
            if self.nbits == 8:
                self.out.append(self.pool)
                self.pool = 0
                self.nbits = 0

        def write_bits(self, val, width):
            for i in range(width - 1, -1, -1):
                self.write_bit((val >> i) & 1)

        def finish(self):
            if self.nbits > 0:
                self.out.append(self.pool << (8 - self.nbits))
                self.nbits = 0
            return bytes(self.out)

    bw = BitWriter()
    wp = n
    MAX_CHAIN = max_chain
    hash_table = [[] for _ in range(65536)]

    def key_at(pos):
        if pos < 3:
            return None
        return (data[pos - 1] << 8) | data[pos - 2]

    def record_position(pos):
        k = key_at(pos)
        if k is not None:
            bucket = hash_table[k]
            bucket.append(pos)
            if len(bucket) > MAX_CHAIN:
                del bucket[0]

    def find_best_match(pos):
        best_len = 0
        best_off = 0
        k = key_at(pos)
        if k is not None:
            tested = 0
            for ref in reversed(hash_table[k]):
                if ref <= pos:
                    continue
                offset = ref - pos
                if offset < 3 or offset - 3 > max_offset:
                    continue
                max_search_len = min(265, pos, ref)
                if max_search_len < 2:
                    continue
                length = 0
                while (
                    length < max_search_len
                    and data[pos - 1 - length] == data[ref - 1 - length]
                ):
                    length += 1
                if length > best_len:
                    best_len = length
                    best_off = offset - 3
                    if best_len >= 265:
                        break
                tested += 1
                if tested >= MAX_CHAIN:
                    break
        return best_len, best_off

    while wp > HEADER:
        best_len, best_off = find_best_match(wp)
        if best_len >= 3 and wp - 1 > HEADER:
            next_len, next_off = find_best_match(wp - 1)
            if next_len > best_len + 1:
                best_len = 0
            elif best_len <= 9 and wp - 2 > HEADER:
                next2_len, _ = find_best_match(wp - 2)
                if next2_len > best_len + 2:
                    best_len = 0
        if best_len == 3 and wp - 1 > HEADER:
            next_len, _ = find_best_match(wp - 1)
            if next_len >= 3:
                best_len = 0
        positions_covered = max(best_len, 1) if best_len >= 3 else 1
        for offset_back in range(positions_covered):
            record_position(wp - offset_back)
        if best_len >= 3:
            bw.write_bit(1)
            bw.write_bits(best_off, 13)

            rem = best_len - 3
            vle_lens = [2, 3, 5, 8]
            for vle_level in vle_lens:
                max_val = (1 << vle_level) - 1
                if rem < max_val:
                    bw.write_bits(rem, vle_level)
                    break
                else:
                    bw.write_bits(max_val, vle_level)
                    rem -= max_val
            else:
                while True:
                    if rem < 255:
                        bw.write_bits(rem, 8)
                        break
                    else:
                        bw.write_bits(255, 8)
                        rem -= 255

            wp -= best_len
        else:
            bw.write_bit(0)
            wp -= 1
            bw.write_bits(data[wp], 8)

    compressed = bw.finish()
    stored = compressed[::-1]
    header_bytes = data[:HEADER]

    pad = b""
    csz = len(stored)
    if target_size > 0:
        current_size = 16 + len(stored) + len(header_bytes)
        if current_size < target_size:
            pad = b"\x00" * (target_size - current_size)
            csz += len(pad)

    # Format CRI PSP : CRILAYLA + unc + csz + pad + stored (bitstream) + header_bytes
    return (
        b"CRILAYLA"
        + struct.pack("<I", n - HEADER)
        + struct.pack("<I", csz)
        + pad
        + stored
        + header_bytes
    )


# ── Extraction CPK depuis ISO ─────────────────────────────────────────────────

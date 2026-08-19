"""
Script de décryptage de EBOOT.BIN (PSP PRXType2) - Python pur, sans pspdecrypt.exe
Reproduit fidèlement la logique de pspdecrypt / libkirk pour PRXType2.
"""
import struct
import hashlib
import sys
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# ─────────────────────────────────────────────────────────────────────────────
# Clés internes libkirk (hardcodées dans la ROM du Kirk ME)
# ─────────────────────────────────────────────────────────────────────────────

KIRK7_KEY = bytes.fromhex("115A5D20D53A8DD39CC5AF410F0F186F")
KIRK1_KEY = bytes.fromhex("98C940975C1D10E87FE60EA3FD03A8BA")

TAG_TABLE = {
    0xD91613F0: (bytes.fromhex("EBFF40D8B41AE166913B8F64B6FCB712"), 0x5D),
    0x0CF3D6B6: (bytes.fromhex("37C0A9B09ACF3358D0ECF03D8A0E59A7"), 0x5C),
    0x457B6E2A: (bytes.fromhex("ADB900EDDB3E4543EA0F62B974E7E4B2"), 0x5E),
    0x423BD600: (bytes.fromhex("4E1CEDC5B3DE7B168D0F7EF7B56D73F1"), 0x42),
    0x8B8B5B68: (bytes.fromhex("EAE6F20F25E6C6A66CDA99D6D1063CFF"), 0x4B),
    0xEBF5A5CE: (bytes.fromhex("EB44FB27C42C271E83D14F8F5C1ECC90"), 0x5F),
    0x5372ADC7: (bytes.fromhex("17C4EB62D0F8AE0B8E33E1BDD8B34F98"), 0x60),
    0xB7C01C89: (bytes.fromhex("FADA5E66E0EB0F38B97A5CCCB5B72FAB"), 0x61),
    0x3D7E63C4: (bytes.fromhex("40F76B03DEE67F45BBF09B45EEE3D9A0"), 0x62),
}

def aes_decrypt_ecb(key: bytes, ct: bytes) -> bytes:
    c = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    d = c.decryptor()
    return d.update(ct) + d.finalize()

def aes_decrypt_cbc_null_iv(key: bytes, data: bytes) -> bytes:
    result = bytearray()
    prev_ct = None
    for i in range(0, len(data), 16):
        block = data[i:i+16]
        if len(block) < 16:
            result.extend(block)
            break
        pt = aes_decrypt_ecb(key, block)
        if prev_ct is None:
            result.extend(pt)
        else:
            result.extend(bytes(a ^ b for a, b in zip(pt, prev_ct)))
        prev_ct = block
    return bytes(result)

def aes_decrypt_cbc_with_iv(key: bytes, iv: bytes, data: bytes) -> bytes:
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    d = cipher.decryptor()
    return d.update(data) + d.finalize()

def kirk7(data: bytes) -> bytes:
    return aes_decrypt_cbc_null_iv(KIRK7_KEY, data)

def expand_seed(seed: bytes, key_id: int) -> bytes:
    buf = bytearray(0x90)
    for i in range(0, 0x90, 0x10):
        buf[i:i+0x10] = seed
        buf[i] = i // 0x10
    return kirk7(bytes(buf))

def build_prxtype2(prx: bytes) -> bytearray:
    buf = bytearray(0x150)
    buf[0x000:0x004] = prx[0xD0:0xD4]
    buf[0x05C:0x06C] = prx[0x140:0x150]
    buf[0x06C:0x080] = prx[0x12C:0x140]
    buf[0x080:0x0B0] = prx[0x080:0x0B0]
    buf[0x0B0:0x0C0] = prx[0x0C0:0x0D0]
    buf[0x0C0:0x0D0] = prx[0x0B0:0x0C0]
    buf[0x0D0:0x150] = prx[0x000:0x080]
    return buf

def decrypt_prx_type2(prx: bytes) -> bytes:
    tag = struct.unpack_from("<I", prx, 0xD0)[0]
    print(f"[*] Tag détecté : {tag:08X}")
    if tag not in TAG_TABLE:
        raise ValueError(f"Tag {tag:08X} non reconnu dans la table des clés.")
    pti_key, pti_code = TAG_TABLE[tag]
    print(f"[*] Code Kirk : {pti_code:02X}")
    xorbuf = bytearray(expand_seed(pti_key, pti_code))
    type2 = build_prxtype2(prx)
    type2[0x5C:0x5C+0x60] = kirk7(bytes(type2[0x5C:0x5C+0x60]))
    sha_ctx = hashlib.sha1()
    sha_ctx.update(bytes(type2[0x000:0x004]))
    sha_ctx.update(bytes(xorbuf[0x000:0x010]))
    sha_ctx.update(bytes(type2[0x004:0x05C]))
    sha_ctx.update(bytes(type2[0x05C:0x06C]))
    sha_ctx.update(bytes(type2[0x080:0x0C0]))
    sha_ctx.update(bytes(type2[0x0C0:0x0D0]))
    sha_ctx.update(bytes(type2[0x0D0:0x150]))
    computed_sha1 = sha_ctx.digest()
    stored_sha1   = bytes(type2[0x06C:0x080])
    if computed_sha1 != stored_sha1:
        print(f"[!] SHA-1 mismatch – computed: {computed_sha1.hex()} / stored: {stored_sha1.hex()}")
        print("[!] Poursuite malgré la divergence…")
    else:
        print("[+] SHA-1 verifie OK")
    kh = bytearray(type2[0x080:0x0C0])
    for i in range(0x40):
        kh[i] ^= xorbuf[0x10 + i]
    kh = bytearray(kirk7(bytes(kh)))
    for i in range(0x40):
        kh[i] ^= xorbuf[0x50 + i]
    keys = aes_decrypt_cbc_null_iv(KIRK1_KEY, bytes(kh[:32]))
    aes_key = keys[0:16]
    aes_iv  = keys[16:32]
    print(f"[*] AES Key : {aes_key.hex().upper()}")
    print(f"[*] AES IV  : {aes_iv.hex().upper()}")
    data_size   = struct.unpack_from("<I", prx, 0xB0)[0]
    data_offset = struct.unpack_from("<I", prx, 0xB4)[0]
    print(f"[*] data_size   : {data_size} octets")
    print(f"[*] data_offset : {data_offset} octets")
    prx_header = prx[0x000:0x080]
    payload_ct = prx[0x150:]
    total_plain_size = data_offset + data_size
    padded_size = ((total_plain_size + 15) // 16) * 16
    full_input = prx_header + payload_ct
    full_input = full_input[:padded_size]
    decrypted_full = aes_decrypt_cbc_with_iv(aes_key, aes_iv, bytes(full_input))
    elf_data = bytearray(decrypted_full[data_offset:data_offset + data_size])
    if elf_data[:4] == b"\x7f\x45\x4c\x46" and len(elf_data) >= 13:
        elf_data[8:13] = b"\x00" * 5
    print(f"[+] Dechiffrement termine. Taille ELF : {len(elf_data)} octets")
    return bytes(elf_data)

if __name__ == "__main__":
    import os
    if len(sys.argv) < 2:
        print("Usage: python decrypt_eboot.py <EBOOT.BIN> [sortie.bin]")
        sys.exit(1)
    in_path  = sys.argv[1]
    out_path = sys.argv[2] if len(sys.argv) > 2 else in_path + ".dec"
    print(f"[*] Lecture de {in_path} …")
    with open(in_path, "rb") as f:
        data = f.read()
    magic = data[:4]
    if magic == b"\x7e\x50\x53\x50":
        elf = decrypt_prx_type2(data)
    elif magic == b"\x7f\x45\x4c\x46":
        print("[*] Fichier déjà en clair (ELF), copie directe.")
        elf = data
    else:
        print(f"[!] Magic inconnu : {magic.hex()} – tentative de déchiffrement PRXType2…")
        elf = decrypt_prx_type2(data)
    with open(out_path, "wb") as f:
        f.write(elf)
    import hashlib
    sha1 = hashlib.sha1(elf).hexdigest()
    print(f"[+] Écrit dans {out_path}")
    print(f"[+] SHA-1 de la sortie : {sha1}")

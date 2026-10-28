import glob
import json
import os
import re
import struct
import unicodedata

def encode_char(c):
    if c == '\n': return 0x000A
    if c in (' ', '\xA0', '\u3000'): return 0x8140
    punct_map = {
        '.': 0x0004, ',': 0x0003, '?': 0x0008, '!': 0x0009, '-': 0x003C,
        "'": 0x0026, '"': 0x0028, ':': 0x0006, ';': 0x0007, '/': 0x002F,
        '(': 0x0028, ')': 0x0029, '[': 0x005B, ']': 0x005D,
    }
    if c in punct_map:
        return punct_map[c]
    if c.isupper() and 'A' <= c <= 'Z':
        return 0x00E0 + (ord(c) - 0x41)
    if c.islower() and 'a' <= c <= 'z':
        return 0x0101 + (ord(c) - 0x61)
    if c.isdigit():
        return 0x00CF + int(c)
    if 0x20 <= ord(c) <= 0x7E:
        return ord(c)
    return 0x8140

def encode_string(text):
    tokens = re.split(r'(<[0-9A-Fa-f]{4}>|<S[0-9A-Fa-f]{4}>)', text)
    out_bytes = bytearray()
    for token in tokens:
        if not token:
            continue
        if token.startswith('<S') and token.endswith('>'):
            val = int(token[2:6], 16)
            out_bytes.extend(struct.pack('>H', val))
        elif token.startswith('<') and token.endswith('>'):
            val = int(token[1:5], 16)
            out_bytes.extend(struct.pack('>H', val))
        else:
            token = ''.join(x for x in unicodedata.normalize('NFKD', token) if unicodedata.category(x) != 'Mn')
            for char in token:
                val = encode_char(char)
                out_bytes.extend(struct.pack('>H', val))
    return bytes(out_bytes)

def audit():
    repo_dir = r"c:\Users\tasda\Documents\Projets\Perso\Grimoire du Coeur\P2-IS-FR-PSP"
    pattern = os.path.join(repo_dir, "traduction", "EBOOT_decoupe", "EBOOT_Part*.json")
    files = sorted(glob.glob(pattern))
    
    total_entries = 0
    empty_entries = 0
    translated_entries = 0
    current_overflows = 0
    
    for fpath in files:
        fname = os.path.basename(fpath)
        with open(fpath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        f_empty = 0
        f_trans = 0
        f_ovf = 0
        for entry in data:
            total_entries += 1
            orig = entry.get('texte_orig', '')
            fr = entry.get('texte_fr', '')
            slot = entry.get('slot_size', 0)
            if not fr.strip():
                empty_entries += 1
                f_empty += 1
            else:
                translated_entries += 1
                f_trans += 1
                enc_len = len(encode_string(fr.replace('[SP]', '\u3000')))
                if enc_len > slot:
                    current_overflows += 1
                    f_ovf += 1
                    print(f"[{fname}] ID {entry['id']} OVERFLOW: {enc_len} > {slot}")
                    print(f"   Orig: {orig}")
                    print(f"   FR  : {fr}")
        print(f"{fname}: {len(data)} total, {f_trans} translated, {f_empty} empty, {f_ovf} overflows")
        
    print("=" * 60)
    print(f"TOTAL: {total_entries} entries, {translated_entries} translated, {empty_entries} empty, {current_overflows} overflows")

if __name__ == '__main__':
    audit()


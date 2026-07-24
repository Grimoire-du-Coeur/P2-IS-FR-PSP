#!/usr/bin/env python3
"""
p2_eboot_tool.py
Universal tool to extract and inject ENGBIN-encoded text in Persona 2 Innocent Sin (PSP) EBOOT.BIN
"""

import struct
import json
import os
import argparse
import re

def decode_char(v):
    hb = v >> 8
    lb = v & 0xFF
    if v in (0xFFFF, 0x0000): return ('END', '')
    if hb == 0x00:
        if 0xE0 <= lb <= 0xF9: return ('CHAR', chr(0x41 + (lb - 0xE0)))
        elif 0xCF <= lb <= 0xD8: return ('CHAR', str(lb - 0xCF))
        elif 0x20 <= lb <= 0x7E: return ('CHAR', chr(lb))
        else: return ('CTRL', f'<{v:04X}>')
    if hb == 0x01:
        if 0x01 <= lb <= 0x1A: return ('CHAR', chr(0x61 + (lb - 0x01)))
        return ('CHAR', chr(0x60 + lb)) # Fallback
    
    if hb in (0x81, 0x82) or (0x83 <= hb <= 0x9F) or (0xE0 <= hb <= 0xEF):
        try:
            c = struct.pack('>H', v).decode('shift-jis')
            return ('CHAR', c)
        except:
            return ('CTRL', f'<S{v:04X}>')
    
    return ('CTRL', f'<{v:04X}>')

import unicodedata

def encode_char(c):
    # c is guaranteed to be a single character now
    if c == '\n':
        return 0x000A
    if c == '\xA0':
        return 0x0020
    
    if c.isupper() and 'A' <= c <= 'Z':
        return 0x00E0 + (ord(c) - 0x41)
    if c.islower() and 'a' <= c <= 'z':
        return 0x0101 + (ord(c) - 0x61)
    if c.isdigit():
        return 0x00CF + int(c)
    if 0x20 <= ord(c) <= 0x7E:
        return ord(c)
    return 0x0020 # Space fallback for unknown characters (0x1120 is the event.bin space, in EBOOT it causes a tilde)

def encode_string(text):
    # This regex finds <XXXX> tags and literal text
    tokens = re.split(r'(<[0-9A-Fa-f]{4}>|<S[0-9A-Fa-f]{4}>)', text)
    out_bytes = bytearray()
    
    for token in tokens:
        if not token: continue
        if token.startswith('<S') and token.endswith('>'):
            val = int(token[2:6], 16)
            out_bytes.extend(struct.pack('>H', val))
        elif token.startswith('<') and token.endswith('>'):
            val = int(token[1:5], 16)
            out_bytes.extend(struct.pack('>H', val))
        else:
            # Normalize to decompose ligatures and remove accents
            token = ''.join(x for x in unicodedata.normalize('NFKD', token) if unicodedata.category(x) != 'Mn')
            for char in token:
                val = encode_char(char)
                out_bytes.extend(struct.pack('>H', val))
    return bytes(out_bytes)

def extract_eboot(eboot_path, json_path, logger=print):
    logger(f"Extracting texts from {eboot_path}...")
    with open(eboot_path, 'rb') as f:
        data = f.read()

    entries = []
    i = 0
    # On limite la recherche aux zones probables pour eviter les faux positifs
    start_offset = 0x3D0000
    end_offset = 0x4A0000
    i = start_offset
    
    while i < end_offset - 1:
        v = struct.unpack_from('>H', data, i)[0]
        typ, val = decode_char(v)
        if typ == 'CHAR':
            j = i
            chars = []
            while j < end_offset - 1:
                v2 = struct.unpack_from('>H', data, j)[0]
                typ2, val2 = decode_char(v2)
                if typ2 == 'END':
                    break
                chars.append(val2)
                j += 2
            
            text = ''.join(chars)
            # Filter garbage
            clean_text = re.sub(r'<[^>]+>', '', text)
            alphas = len([c for c in clean_text if c.isalpha() and ord(c) < 128])
            
            if alphas >= 2:
                # Rejet si trop de kanji/caracteres etranges (hors espace 8140)
                kanjis = len([c for c in text if ord(c) > 0xFF and c != '\u3000'])
                if kanjis > alphas:
                    pass # ignore
                elif '<S' in text: # Shift-JIS erroné
                    pass # ignore
                else:
                    # Rejet si trop de balises binaires inconnues
                    ctrl_tags = re.findall(r'<([0-9A-Fa-f]{4})>', text)
                    bad_tags = [t for t in ctrl_tags if not t.startswith('FF') and not t.startswith('00')]
                    
                    # Verifier s'il y a des vrais mots (au moins 3 lettres)
                    words = re.findall(r'[A-Za-z]{3,}', clean_text)
                    
                    # Rejet si on a des bad tags mais aucun mot de 3 lettres
                    if len(bad_tags) > 0 and len(words) == 0:
                        pass
                    # Rejet des patterns repetitifs type 'a<1401>a<0800>'
                    elif clean_text.count('a') == len(clean_text) and len(clean_text) > 0:
                        pass
                    elif len(bad_tags) <= alphas:
                        # Conversion format DreamMMap
                        formatted_text = text.replace('\u3000', '[SP]')
                        entries.append({
                            "id": len(entries),
                            "offset": i,
                            "data_size": j - i,
                            "slot_size": j - i,
                            "_term": [],
                            "nom_orig": "",
                            "texte_orig": formatted_text,
                            "nom_fr": "",
                            "texte_fr": ""
                        })
            i = j + 2
        else:
            i += 2

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(entries, f, indent=4, ensure_ascii=False)
    
    logger(f"Extraction complete: {len(entries)} strings written to EBOOT_Translation.json")

def inject_eboot(eboot_path, json_path, out_path, logger=print):
    logger(f"Injecting translations from {json_path} into {eboot_path}...")
    with open(eboot_path, 'rb') as f:
        data = bytearray(f.read())
        
    with open(json_path, 'r', encoding='utf-8') as f:
        entries = json.load(f)
        
    injected_count = 0
    
    for entry in entries:
        if not entry.get("texte_fr"):
            continue
            
        offset = entry["offset"]
        orig_len = entry["slot_size"]
        trans_text = entry["texte_fr"].replace('[SP]', '\u3000')
        
        encoded_bytes = encode_string(trans_text)
        
        # Determine available space (we can safely overwrite until the next string, 
        # so we rely on original_length)
        if len(encoded_bytes) > orig_len:
            logger(f"WARNING: Translated text at 0x{offset:X} is too long! "
                  f"({len(encoded_bytes)} > {orig_len} bytes). Truncating.")
            encoded_bytes = encoded_bytes[:orig_len]
        
        # Write translated bytes
        data[offset : offset + len(encoded_bytes)] = encoded_bytes
        
        # Fill the remaining space with 0xFFFF (END marker) to prevent garbage
        padding_start = offset + len(encoded_bytes)
        padding_len = orig_len - len(encoded_bytes)
        
        for p in range(padding_start, padding_start + padding_len, 2):
            if p + 1 < len(data):
                data[p] = 0xFF
                data[p+1] = 0xFF
        
        injected_count += 1
        
    with open(out_path, 'wb') as f:
        f.write(data)
        
    logger(f"Injection complete: {injected_count} strings translated. Saved to EBOOT_MODIFIED.BIN")

#!/usr/bin/env python3
"""
p2_eboot_tool.py
Universal tool to extract and inject ENGBIN-encoded text in Persona 2 Innocent Sin (PSP) EBOOT.BIN
"""

import struct
import json
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
    if c == '\n': return 0x000A
    if c in (' ', '\xA0', '\u3000'): return 0x8140
    
    # Mapping de la ponctuation vers Shift-JIS Full-Width 
    # pour eviter les problemes de font corrompue/decalee dans l'EBOOT
    punct_map = {
        '.': 0x0004,
        ',': 0x0003,
        '?': 0x0008,
        '!': 0x0009,
        '-': 0x003C,
        # Codes relevés dans les textes anglais d'origine de l'EBOOT : la police
        # des menus est décalée (0x28 = guillemet, 0x29 = « ( », 0x2A = « ) »,
        # 0x3B = « / »). Les anciennes valeurs affichaient « "Nostalgie( ».
        "'": 0x0026,
        '"': 0x0028,
        ':': 0x0006,
        ';': 0x0007,
        '/': 0x003B,
        '(': 0x0029,
        ')': 0x002A,
        '[': 0x005B,
        ']': 0x005D,
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
    # Caractères japonais (préfixes de tables, ex. CD Shop) : on les réécrit tels quels.
    try:
        b = c.encode('shift-jis')
        if len(b) == 2:
            return struct.unpack('>H', b)[0]
    except UnicodeEncodeError:
        pass
    return 0x8140

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
            # La police des menus n'a ni accents ni ligatures : œ ne se décompose
            # pas (il devenait une espace), on l'écrit « oe ». Guillemets et
            # apostrophes typographiques -> codes de la police.
            for a, b in (('œ', 'oe'), ('Œ', 'OE'), ('æ', 'ae'), ('Æ', 'AE'),
                         ('«', '"'), ('»', '"'), ('“', '"'), ('”', '"'),
                         ('’', "'"), ('‘', "'"), ('…', '...')):
                token = token.replace(a, b)
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
                            "texte_orig": formatted_text,
                            "texte_fr": ""
                        })
            i = j + 2
        else:
            i += 2

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(entries, f, indent=4, ensure_ascii=False)
    
    logger(f"Extraction complete: {len(entries)} strings written to EBOOT_Translation.json")

def encode_brut(text):
    """Réencode un texte tel que le décodeur l'a lu (caractères 0x20-0x7E tels
    quels). Sert à vérifier qu'une entrée est bien du texte : si son anglais ne
    redonne pas les octets d'origine, c'est une table de données, à ne pas écraser."""
    out = bytearray()
    for tok in re.split(r'(<[0-9A-Fa-f]{4}>|<S[0-9A-Fa-f]{4}>)', text.replace('[SP]', '　')):
        if not tok:
            continue
        if tok.startswith('<S'):
            out += struct.pack('>H', int(tok[2:6], 16))
            continue
        if tok.startswith('<'):
            out += struct.pack('>H', int(tok[1:5], 16))
            continue
        for c in tok:
            if c == '　':
                v = 0x8140
            elif 'A' <= c <= 'Z':
                v = 0x00E0 + ord(c) - 0x41
            elif 'a' <= c <= 'z':
                v = 0x0101 + ord(c) - 0x61
            elif c.isdigit():
                v = 0x00CF + int(c)
            elif 0x20 <= ord(c) <= 0x7E:
                v = ord(c)
            else:
                try:
                    v = struct.unpack('>H', c.encode('shift-jis'))[0]
                except Exception:
                    return None
            out += struct.pack('>H', v)
    return bytes(out)


def _sans_balises(t):
    return re.sub(r'<[^>]+>', '', t.replace('[SP]', ' ')).strip()


def raison_de_ne_pas_injecter(entry, data):
    """None si la traduction peut être écrite, sinon la raison de garder l'original."""
    fr = entry.get("texte_fr") or ""
    en = entry.get("texte_orig") or ""
    if not fr:
        return "vide"
    if fr.replace(' ', '[SP]') == en or fr == en:
        return "identique a l'anglais"
    # L'anglais doit être ce que le décodeur lit à cet endroit, sinon c'est une table
    # de données. On compare au décodage (et non à un réencodage) : certains codes
    # ASCII bruts sont des symboles (0x44 = flèche « > », 0x53 = « % »...) que le
    # décodeur affiche comme des lettres.
    lu, off = [], entry["offset"]
    for k in range(off, min(off + entry["slot_size"], len(data) - 1), 2):
        typ, val = decode_char(struct.unpack_from('>H', data, k)[0])
        if typ == 'END':
            break
        lu.append(val)
    if ''.join(lu).replace('　', '[SP]') != en:
        return "pas du texte (donnees)"
    f, e = _sans_balises(fr), _sans_balises(en)
    if f and len(f) < 0.6 * len(e) and e.endswith(f) and ' ' not in f.strip():
        return "fragment de l'anglais (traduction tronquee)"
    return None


def inject_eboot(eboot_path, json_path, out_path, logger=print):
    logger(f"Injecting translations from {json_path} into {eboot_path}...")
    with open(eboot_path, 'rb') as f:
        data = bytearray(f.read())

    with open(json_path, 'r', encoding='utf-8') as f:
        entries = json.load(f)

    injected_count = 0
    gardees = {}

    # Place réelle : les chaînes sont alignées sur 4 octets. Après le terminateur
    # FFFF, les octets à 00 jusqu'à la chaîne suivante sont libres (« No » a la
    # place d'écrire « Non »).
    suivants = sorted(e["offset"] for e in entries)
    import bisect

    def place(entry):
        o, n = entry["offset"], entry["slot_size"]
        k = bisect.bisect_right(suivants, o)
        fin = suivants[k] if k < len(suivants) else o + n + 2
        fin = min(fin, o + n + 4)  # seulement l'alignement (2 octets) : au-delà, ce peut être une table de données
        bourrage = bytes(data[o + n:fin])
        if fin - o - n >= 4 and bourrage[:2] == b"\xff\xff" and not any(bourrage[2:]):
            return fin - o - 2
        return n

    for entry in entries:
        raison = raison_de_ne_pas_injecter(entry, data)
        if raison:
            if raison != "vide":
                gardees[raison] = gardees.get(raison, 0) + 1
            continue

        offset = entry["offset"]
        orig_len = place(entry)
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
        
        # Fill the remaining space with 0xFFFF (END marker) to prevent garbage,
        # terminator included (+2): orig_len may now reach into the alignment padding.
        padding_start = offset + len(encoded_bytes)
        padding_len = orig_len + 2 - len(encoded_bytes)
        
        for p in range(padding_start, padding_start + padding_len, 2):
            if p + 1 < len(data):
                data[p] = 0xFF
                data[p+1] = 0xFF
        
        injected_count += 1
        
    with open(out_path, 'wb') as f:
        f.write(data)
        
    for raison, n in sorted(gardees.items()):
        logger(f"Original kept ({raison}): {n}")
    logger(f"Injection complete: {injected_count} strings translated. Saved to EBOOT_MODIFIED.BIN")

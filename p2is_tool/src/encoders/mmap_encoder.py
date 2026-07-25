#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P2IS FR Tool  ·  Persona 2 Innocent Sin PSP (EUR ULES01557)
============================================================
Module spécialisé pour le parsing et l'encodage des fichiers MMAP01-06.BNP.

Les fichiers MMAP (carte du monde, dialogues de PNJ par zone) utilisent un
format binaire propre différent de l'event.bin :

  - Format conteneur : MIG.00.1PSP (format propriétaire Atlus)
  - Terminateur de dialogue MMAP : [0x1106][0x1102][0x1103][0x1431][0x0000][0x0000]
    (12 octets) — différent de l'event.bin qui utilise [E1][E2][E3][E4]
  - Pas de zéros de padding entre dialogues : slot_size == data_size
  - Les dialogues sont contigus dans la zone de données du BNP

IMPORTANT : Le 'nettoyage' effectué par find_dialogs() de bin_parser.py
supprime des codes de contrôle critiques ([0x1106], [0x1431]) qui font partie
du terminateur MMAP, cassant ainsi l'encodage.

Ce module contourne ce problème avec une logique dédiée.
"""

import struct, json, re
from pathlib import Path
from src.config import *
from src.core.text import decode_text, text_to_bytes, _align_menu_text

# ── Terminateur spécifique MMAP ───────────────────────────────────────────────
# [0x1106][E2=0x1102][E3=0x1103][0x1431][NULL=0x0000][NULL=0x0000]
MMAP_TERM = [0x1106, 0x1102, 0x1103, 0x1431, 0x0000, 0x0000]
MMAP_TERM_BYTES = b''.join(struct.pack('<H', w) for w in MMAP_TERM)
MMAP_TERM_SIZE = len(MMAP_TERM_BYTES)  # 12 octets

# Codes de contrôle à nettoyer du texte extrait (sans toucher au terminateur)
_CTRL_MMAP = {
    0x1101: '[NL]', 0x1102: '[E2]', 0x1103: '[E3]', 0x1104: '[E4]',
    0x1106: '[1106]', 0x1109: '[1109]', 0x1120: '[SP]',
    0x1113: '[1113]', 0x1112: '[1112]', 0x1208: '[1208]', 0x1205: '[1205]',
    0x1431: '[1431]',
}


def _valid_mmap_name(data: bytes, offset: int) -> bool:
    """
    Vérifie qu'un guillemet ouvrant 0x0022 est suivi d'un nom de personnage valide
    dans le contexte MMAP (même logique que bin_parser._valid_name).
    """
    j = offset + 2
    if j + 1 >= len(data):
        return False
    first = struct.unpack_from('<H', data, j)[0]
    if first == SP:
        return False
    chars = []
    pr = al = uk = 0
    while j < len(data) - 1:
        cp = struct.unpack_from('<H', data, j)[0]
        if cp == NL:  # 0x1101 = fin du nom
            n = len(chars)
            if not (1 <= n <= 40):
                return False
            return al >= 1 and (pr / max(1, n)) >= 0.6
        if 0x20 <= cp <= 0x7E:
            pr += 1
            al += 0x41 <= cp <= 0x7A
        elif cp == SP:
            pr += 1
        else:
            uk += 1
        if uk > 2:
            return False
        chars.append(cp)
        if len(chars) > 40:
            return False
        j += 2
    return False


def _decode_mmap_text(raw: bytes) -> str:
    """Décode le texte binaire Atlus MMAP en texte lisible, en excluant le terminateur."""
    out = ""
    for i in range(0, len(raw) - 1, 2):
        cp = struct.unpack_from('<H', raw, i)[0]
        if cp in _CTRL_MMAP:
            out += _CTRL_MMAP[cp]
        elif 0x20 <= cp <= 0x7E:
            out += chr(cp)
        elif 0x80 <= cp <= 0xFF:
            out += chr(cp)
        else:
            out += f'[U+{cp:04X}]'
    return out


def scan_mmap_bnp(data: bytes, stem: str, out_dir: Path, log_fn) -> int:
    """
    Parse un fichier MMAP.BNP et extrait tous les dialogues dans un JSON.

    Contrairement à scan_bnp_bin(), cette fonction utilise le terminateur
    propre aux MMAP et ne cherche pas de blocs gzip embeddés.

    Returns: nombre de dialogues extraits.
    """
    dialogs = []
    i = 0

    while i < len(data) - 1:
        w = struct.unpack_from('<H', data, i)[0]
        if w != 0x0022 or not _valid_mmap_name(data, i):
            i += 2
            continue

        start = i
        # Chercher le terminateur MMAP à partir de start
        term_idx = data.find(MMAP_TERM_BYTES, start + 2)
        if term_idx == -1 or term_idx > start + 4000:
            # Pas de terminateur MMAP dans la fenêtre → pas un dialogue valide
            i += 2
            continue

        end = term_idx + MMAP_TERM_SIZE  # inclut le terminateur

        # Décoder le texte (sans le terminateur final)
        raw_text = data[start:term_idx]
        full_text = _decode_mmap_text(raw_text)

        lines = full_text.split('[NL]')
        nom = lines[0].lstrip('"') if lines else ''
        body = '[NL]'.join(lines[1:]) if len(lines) > 1 else ''
        body_clean = body.strip()

        entry = {
            'id': len(dialogs),
            'offset': start,
            'data_size': end - start,   # inclut le terminateur
            'slot_size': end - start,   # = data_size (pas de padding dans MMAP)
            '_term': MMAP_TERM,
            'nom_orig': nom,
            'texte_orig': body_clean,
            'nom_fr': '',
            'texte_fr': '',
        }
        dialogs.append(entry)
        i = end

    if not dialogs:
        if log_fn:
            log_fn(f'  {stem.upper()}: aucun dialogue trouvé', 'warn')
        return 0

    out_path = out_dir / f'{stem.upper()}.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(dialogs, f, ensure_ascii=False, indent=2)

    if log_fn:
        log_fn(f'  {stem.upper()}: {len(dialogs)} dialogues -> {out_path.name}', 'ok')
    return len(dialogs)


def encode_mmap_bnp_from_json(
    bin_path: str, json_path: str, log_fn, out_path: str = None
) -> str:
    data = bytearray(open(bin_path, 'rb').read())
    dlgs = json.loads(open(json_path, encoding='utf-8').read(), strict=False)

    ok = skip = kept = 0
    nl_bytes = struct.pack('<H', NL)
    
    dlgs.sort(key=lambda x: x['offset'])
    
    new_data = bytearray()
    last_offset = 0

    for d in dlgs:
        n_fr = d.get('nom_fr', '').strip()
        t_fr = d.get('texte_fr', '').strip()

        if not n_fr and not t_fr:
            kept += 1
            continue

        n_fr = n_fr or d.get('nom_orig', '').replace('[SP]', ' ').strip()
        t_fr = t_fr or d.get('texte_orig', '').strip()
        n_orig = d.get('nom_orig', '')
        t_orig = d.get('texte_orig', '')

        # Alignement des menus de choix pour éviter les crashs
        t_fr = _align_menu_text(n_orig, t_orig, n_fr, t_fr)

        enc = text_to_bytes('"' + n_fr + '\n' + t_fr)

        # Terminateur exact du JSON
        term_seq = d.get('_term', MMAP_TERM)
        term_bytes = b''.join(struct.pack('<H', w) for w in term_seq)
        
        orig_offset = d['offset']
        orig_size = d['slot_size']

        avail = orig_size - len(term_bytes)

        if len(enc) > avail:
            depassement = len(enc) - avail
            if log_fn:
                log_fn(
                    f'  [!] [MMAP] [id {d["id"]}] Texte FR trop long de {depassement} '
                    f'octets. Troncature automatique.',
                    'warn'
                )
            tokens = re.split(r'(\[[a-zA-Z0-9+\-_]+\]|\s|\[SP\])', t_fr)
            tokens = [t for t in tokens if t]
            while tokens and len(text_to_bytes('"' + n_fr + '\n' + ''.join(tokens))) > avail:
                tokens.pop()
            t_fr = ''.join(tokens)
            enc = text_to_bytes('"' + n_fr + '\n' + t_fr)

        # Pad avec des espaces pour maintenir la taille exacte du slot
        pad_len = avail - len(enc)
        if pad_len > 0:
            enc += struct.pack('<H', 0x1120) * (pad_len // 2)

        # Construire la séquence stricte
        full = enc + term_bytes
        
        # Sécurité maximale : on force la taille
        if len(full) != orig_size:
            if log_fn: log_fn(f'  [!] Erreur fatale de taille pour {d["id"]}: {len(full)} != {orig_size}', 'err')
            full = full[:orig_size].ljust(orig_size, b'\x00')

        # On copie l'original jusqu'a l'offset de ce dialogue
        new_data += data[last_offset : orig_offset]
        # On ajoute le nouveau dialogue
        new_data += full
        
        last_offset = orig_offset + orig_size
        ok += 1

    # On ajoute le reste du fichier
    new_data += data[last_offset:]
    
    # Combien de bytes avons-nous gagne ?
    total_delta = len(data) - len(new_data)
    
    # On met a jour la taille du chunk 0x08000001 (qui contient les dialogues)
    idx = 0
    while idx < len(new_data):
        if idx + 8 > len(new_data): break
        ctype, csize = struct.unpack_from('<II', new_data, idx)
        if ctype == 0x08000001:
            new_csize = csize - total_delta
            struct.pack_into('<I', new_data, idx + 4, new_csize)
            break
        idx += 8 + csize
        idx = (idx + 0x7FF) & ~0x7FF
        
    # On pad la fin du fichier avec des zeros pour conserver la meme taille globale
    if total_delta > 0:
        new_data += b'\x00' * total_delta
        
    out = Path(out_path) if out_path else Path(bin_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, 'wb') as f:
        f.write(new_data)

    if log_fn:
        log_fn(f'  [OK]   [MMAP] {ok} traduits | {skip} ignores | {kept} conserves -> {out.name}', 'ok')
    return str(out)

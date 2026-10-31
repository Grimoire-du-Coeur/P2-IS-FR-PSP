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

import json
import struct
from pathlib import Path

from p2is.tables import E1, E2, E3, E4, NL
from p2is.core.text import decode_text
from p2is.parsers.bin_parser import find_dialogs
def scan_fbe_bnp(data: bytes, stem: str, out_dir: Path, log_fn) -> int:
    """Extrait les dialogues d'un F_BE.BNP ou TM_EVE.BNP avec le décodeur animation."""
    
    raw = find_dialogs(data)
    if not raw:
        return 0
    output = []
    eid = 0
    for e in raw:
        off, sz = e["offset"], e["data_size"]
        slot_data = data[off : off + sz]
        
        # Identifier chaque sous-dialogue dans le slot
        i = 0
        while i < len(slot_data) - 1:
            w = struct.unpack_from('<H', slot_data, i)[0]
            if w == 0x0022:
                # Trouver la fin de ce sous-dialogue (le prochain 0x0022)
                j = i + 2
                while j < len(slot_data) - 1:
                    w2 = struct.unpack_from('<H', slot_data, j)[0]
                    if w2 == 0x0022:
                        break
                    j += 2
                
                sub_chunk = slot_data[i:j]
                
                # Extraire le nom et le texte
                nl_idx = sub_chunk.find(struct.pack('<H', NL))
                if nl_idx != -1:
                    name_bytes = sub_chunk[2:nl_idx]
                    text_and_ctrl = sub_chunk[nl_idx+2:]
                else:
                    name_bytes = b''
                    text_and_ctrl = sub_chunk[2:]
                    
                # Nettoyer les codes de controle finaux pour avoir un texte propre pour la trad
                # (On garde sub_chunk intact pour référence binaire si besoin, mais encode_fbe_slot va tout réassembler)
                text_str = decode_text(text_and_ctrl)
                name_str = decode_text(name_bytes)
                
                # Pour éviter d'exposer trop de codes binaires au traducteur à la fin, on peut nettoyer les tags [1102] etc.
                # Mais pour la fidélité, decode_text les garde. On les laissera ainsi, ou bien l'encodeur s'en moquera.
                # Dans F_BE, l'encodeur va devoir ré-injecter les bons codes.
                # L'approche la plus sûre est de ne PAS changer l'encodeur original qui ignore la fin, 
                # MAIS de donner à l'encodeur la possibilité de remplacer UNIQUEMENT la partie texte de ce sub_chunk !
                
                # On sauvegarde donc le pre_bytes, le texte original, et on donnera tout à l'encodeur.
                output.append(
                    {
                        "id": eid,
                        "offset": off,
                        "data_size": sz,
                        "slot_size": e["slot_size"],
                        "_sub_offset": i, # Offset interne au slot
                        "_sub_len": j - i, # Taille du sous-dialogue
                        "_term": e.get("_term", [E1, E2, E3, E4]),
                        "nom_orig": name_str.strip(),
                        "texte_orig": text_str.strip(),
                        "nom_fr": "",
                        "texte_fr": "",
                    }
                )
                eid += 1
                i = j
            else:
                i += 2

    out_path = out_dir / f"{stem.upper()}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    if log_fn:
        log_fn(f"  {stem.upper()}: {len(output)} dialogues → {out_path.name}", "ok")
    return len(output)


# ── Encodage / décodage texte Atlus ──────────────────────────────────────────

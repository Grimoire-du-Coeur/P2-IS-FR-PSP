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

from p2is.tables import ACCENT_MAP, BINARY_MAGICS, CTRL, NL, SP
def decode_text(raw: bytes) -> str:
    """Binaire Atlus → texte lisible avec balises de contrôle."""
    out = ""
    i = 0
    while i < len(raw):
        if i + 1 < len(raw):
            b0 = raw[i]
            b1 = raw[i+1]
            cp = b0 | (b1 << 8)
            if cp in CTRL:
                out += CTRL[cp]
                i += 2
                continue
            if 0x20 <= cp <= 0x7E:
                out += chr(cp)
                i += 2
                continue
            if 0x1100 <= cp <= 0x12FF:
                out += f"[{cp:04X}]"
                i += 2
                continue
            
            # Treat unknown as 1-byte if it's in our known buggy set to resync alignment
            if b0 in (0x7b, 0x7f, 0x81, 0x0d, 0x00, 0x1b, 0x05, 0x27, 0x09, 0x0b):
                out += f"[B_{b0:02X}]"
                i += 1
                continue
                
            out += f"[U+{cp:04X}]"
            i += 2
        else:
            out += f"[B_{raw[i]:02X}]"
            i += 1
    return out


def text_to_bytes(text: str) -> bytes:
    text = text.replace("…", "...").replace("«", "\"").replace("»", "\"")
    """Texte FR (avec balises et accents) → octets binaires Atlus."""
    for fr, jp in ACCENT_MAP:
        text = text.replace(fr, jp)
    out = []
    i = 0
    while i < len(text):
        ch = text[i]
        if ch == "[":
            try:
                closing = text.index("]", i)
            except ValueError:
                out.append(struct.pack("<H", ord(ch)))
                i += 1
                continue
            tag = text[i : closing + 1]
            i = closing + 1
            if tag == "[NULL]":
                out.append(b"\x00\x00")
                continue
            matched = False
            for code, name in CTRL.items():
                if name == tag:
                    out.append(struct.pack("<H", code))
                    matched = True
                    break
            if matched:
                continue
            if tag.startswith("[B_") and len(tag) == 6:
                try:
                    out.append(bytes([int(tag[3:5], 16)]))
                    continue
                except ValueError:
                    pass
            if tag.startswith("[U+") and len(tag) == 8:
                try:
                    out.append(struct.pack("<H", int(tag[3:7], 16)))
                    continue
                except ValueError:
                    pass
            if len(tag) == 6:
                try:
                    out.append(struct.pack("<H", int(tag[1:5], 16)))
                    continue
                except ValueError:
                    pass
            for c in tag[1:-1]:
                out.append(struct.pack("<H", ord(c)))
        elif ch == "\n":
            out.append(struct.pack("<H", NL))
            i += 1
        elif ch == " ":
            out.append(struct.pack("<H", SP))
            i += 1
        else:
            out.append(struct.pack("<H", ord(ch)))
            i += 1
    res = b"".join(out)
    if len(res) % 2 != 0:
        res += b"\x00"
    return res


# ── Détection de format ───────────────────────────────────────────────────────


def detect(data: bytes) -> str:
    if len(data) < 4:
        return "UNKNOWN"
    for m in BINARY_MAGICS:
        if data[: len(m)] == m:
            return "BINARY"
    if data[:2] == b"\x1f\x8b":
        return "GZIP"
    if len(data) >= 8 and data[0:8] == b"CRILAYLA":
        return "CRILAYLA"
    if len(data) >= 16 and data[-16:-8] == b"CRILAYLA":
        return "CRILAYLA"
    if len(data) >= 8:
        s0 = struct.unpack_from("<I", data, 0)[0]
        e0 = struct.unpack_from("<I", data, 4)[0]
        if 0x800 <= s0 < e0 < len(data) and data[s0 : s0 + 2] == b"\x1f\x8b":
            return "EVENT_BIN"
    return "UNKNOWN"


def _valid_name(data: bytes, offset: int) -> bool:
    """Vérifie qu'un guillemet ouvrant est suivi d'un nom de personnage valide."""
    j = offset + 2
    if j + 1 >= len(data):
        return False
    first = struct.unpack_from("<H", data, j)[0]
    if first == SP or (first in CTRL and first not in (0x1113, 0x1112)):
        return False
    chars = []
    pr = al = uk = 0
    while j < len(data) - 1:
        cp = struct.unpack_from("<H", data, j)[0]
        if cp == NL:
            n = len(chars)
            if not (1 <= n <= 40):
                return False
            if n <= 3 and all(chr(c) in "?." for c in chars):
                return True
            return al >= 1 and (pr / max(1, n)) >= 0.6
        if 0x20 <= cp <= 0x7E:
            pr += 1
            al += 0x41 <= cp <= 0x7A
        elif cp == SP:
            pr += 1
        elif cp in CTRL:
            pr += 1
        elif 0x1100 <= cp <= 0x11FF:
            pass
        else:
            uk += 1
        if uk > 2:
            return False
        chars.append(cp)
        if len(chars) > 40:
            return False
        j += 2
    return False


def _needs_nl_suffix(term: list, texte_orig: str) -> bool:
    """
    Détermine si un dialogue a besoin d'un [NL] (0x1101) final avant le terminateur.
    Tous les dialogues du jeu (menus, standards, boutiques, combats)
    se terminent par 0x1101 juste avant le terminateur (E1 E2 E3 E4, etc).
    Si le 0x1101 est manquant, le jeu ne s'arrête pas de lire et affiche ΓΓΓ (0x0000).
    """
    return True


# ── Encodage bin depuis JSON ──────────────────────────────────────────────────


def _align_menu_text(nom_orig: str, texte_orig: str, nom_fr: str, t_fr: str) -> str:
    """
    Pour les slots qui contiennent un menu de choix [1208], insère du padding SP
    AVANT [1208] dans t_fr pour que les options restent aux mêmes offsets relatifs
    que dans l'original. Le moteur PSP Atlus stocke des pointeurs absolus vers
    les options de menu — si les options bougent, le jeu lit les mauvaises données
    et n'affiche qu'une seule option (ou aucune).

    Retourne t_fr avec padding ajusté. Si la question FR est trop longue,
    retourne t_fr inchangé (l'encodeur avertira via la vérification de taille).
    """
    marker_fr = (
        "[U+1208]" if "[U+1208]" in t_fr else ("[1208]" if "[1208]" in t_fr else None)
    )
    if marker_fr is None:
        return t_fr  # pas un slot de menu

    # Calculer l'offset du 1er [0014] (= début opt1) dans l'original encodé
    # Structure : [1208](2)+[0002](2)+[1432](2)+[NULL](2)+[NULL](2)+[0014](2) = 12 bytes
    nom_orig_clean = nom_orig.replace("[SP]", " ")
    marker_orig = "[U+1208]" if "[U+1208]" in texte_orig else ("[1208]" if "[1208]" in texte_orig else None)
    pre_orig = texte_orig.split(marker_orig)[0] if marker_orig else texte_orig
    enc_pre_orig = text_to_bytes('"' + nom_orig_clean + "\n" + pre_orig)
    opt1_offset_orig = len(enc_pre_orig) + 12  # 6 mots × 2 bytes

    # Calculer la taille de la question FR encodée (avant [1208])
    pre_fr = t_fr.split(marker_fr)[0]
    enc_pre_fr = text_to_bytes('"' + nom_fr + "\n" + pre_fr)
    current_opt1_offset = len(enc_pre_fr) + 12

    diff = opt1_offset_orig - current_opt1_offset  # bytes manquants
    if diff <= 0:
        return t_fr  # déjà aligné ou trop long → laisser tel quel

    # diff doit être pair (mots de 2 bytes)
    n_sp = diff // 2
    return t_fr.replace(marker_fr, "[SP]" * n_sp + marker_fr, 1)

def _align_mid_text(nom_orig: str, texte_orig: str, nom_fr: str, t_fr: str) -> str:
    """
    Pour les slots qui contiennent un changement de dialogue mid-text via [NULL][NULL]",
    insère du padding SP pour réaligner le pointeur interne du jeu.
    """
    if '[NULL][NULL]"' not in t_fr or '[NULL][NULL]"' not in texte_orig:
        return t_fr

    nom_orig_clean = nom_orig.replace("[SP]", " ")
    
    parts_orig = texte_orig.split('[NULL][NULL]"')
    parts_fr = t_fr.split('[NULL][NULL]"')
    
    out_fr = parts_fr[0]
    
    for i in range(1, len(parts_orig)):
        if i >= len(parts_fr): break
        
        pre_orig = '[NULL][NULL]"'.join(parts_orig[:i])
        pre_fr = '[NULL][NULL]"'.join(parts_fr[:i])
        
        orig_off = len(text_to_bytes('"' + nom_orig_clean + "\n" + pre_orig))
        fr_off = len(text_to_bytes('"' + nom_fr + "\n" + out_fr))
        
        diff = orig_off - fr_off
        if diff > 0:
            n_sp = diff // 2
            # Insérer avant [E1] ou [E3] pour préserver intacte la séquence [E4][NULL][NULL]"
            if "[E1]" in out_fr:
                out_fr = out_fr.replace("[E1]", "[SP]" * n_sp + "[E1]", 1)
            elif "[E3]" in out_fr:
                out_fr = out_fr.replace("[E3]", "[SP]" * n_sp + "[E3]", 1)
            else:
                out_fr += "[SP]" * n_sp
        elif diff < 0:
            # Si le texte FR est trop long, raccourcir proprement avant les balises de contrôle
            excess = (-diff) // 2
            for tag in ("[E1]", "[E3]", "[E4]"):
                if tag in out_fr:
                    body, rest = out_fr.split(tag, 1)
                    if len(body) >= excess:
                        body = body[:-excess]
                        out_fr = body + tag + rest
                        break
            fr_off = len(text_to_bytes('"' + nom_fr + "\n" + out_fr))
            diff = orig_off - fr_off
            if diff > 0:
                n_sp = diff // 2
                if "[E1]" in out_fr:
                    out_fr = out_fr.replace("[E1]", "[SP]" * n_sp + "[E1]", 1)
                else:
                    out_fr += "[SP]" * n_sp

        out_fr += '[NULL][NULL]"' + parts_fr[i]
        
    return out_fr

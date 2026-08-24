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

import struct, json, gzip, io, os, re, shutil, threading, subprocess, platform, concurrent.futures, zlib
from pathlib import Path
import tkinter as tk
from src.config import *
from src.config import _lang, _theme_name


from tkinter import filedialog, messagebox
import customtkinter as ctk

# ── Thème ─────────────────────────────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
C_DARK = "#1a1a2e"
C_PANEL = "#16213e"
C_CARD = "#0f3460"
C_ACCENT = "#3a7ebf"
C_OK = "#2ecc71"
C_ERR = "#e74c3c"
C_WARN = "#f39c12"
C_MUTED = "#8892a4"
C_WHITE = "#ffffff"

# ── Traductions FR / EN ───────────────────────────────────────────────────────
STRINGS = {
    "fr": {
        "app_sub": "Outil de traduction  ·  Persona 2 IS PSP  ·  EUR ULES01557",
        "work_lbl": "Dossier de travail :",
        "lang_btn": "🌐 EN",
        "tab_extract": "① Extraction",
        "tab_scan": "② Traduction",
        "tab_encode": "③ Encodage",
        "tab_rebuild": "④ Rebuild ISO",
        # Onglet Extraction
        "a_title": "A — Extraire le CPK",
        "a_iso": "Fichier ISO :",
        "a_note": "Sortie : <travail>/P2PT_ALL.cpk",
        "a_tip": "💡 Sélectionne ton fichier .iso original (ULES01557).",
        "a_btn": "⬇  Extraire P2PT_ALL.cpk",
        "b_title": "B — Extraire les fichiers du jeu",
        "b_exe": "CriFsLib.GUI.exe :",
        "b_dl_btn": "⬇  Télécharger CriFsLib",
        "b_instr": "  1. Télécharge CriFsLib si besoin (bouton ci-dessus)\n  2. Clique « Ouvrir CriFsLib »\n  3. Glisse P2PT_ALL.cpk dans la fenêtre\n  4. Clic droit → Extract All\n  5. Extrais vers : <travail>/cpk_files/",
        "b_tip": "💡 CriFsLib est requis pour cette étape.",
        "b_btn": "🔧  Ouvrir CriFsLib",
        "c_title": "C — Extraire les scripts du jeu",
        "c_cpk": "P2PT_ALL.cpk :",
        "c_note": "Sortie : <travail>/event.bin",
        "c_tip": "💡 event.bin contient tous les scripts de dialogue du jeu.",
        "c_btn": "⬇  Extraire event.bin",
        "d_title": "D — Séparer les scripts",
        "d_event": "event.bin :",
        "d_note": "Sortie : <travail>/scripts_bin/  (399 fichiers)",
        "d_tip": "💡 Chaque script = une scène ou un lieu du jeu.",
        "d_btn": "⬇  Extraire les 399 scripts",
        # Onglet Scan
        "e_title": "E — Générer les fichiers à traduire",
        "e_src": "Dossier scripts_bin/ :",
        "e_out": "Sortie JSON :",
        "e_tip": "💡 Remplis nom_fr et texte_fr dans les JSON pour traduire.",
        "e_btn": "📝  Décoder tous les scripts en JSON",
        "v_title": "G — Vérifier la cohérence des menus",
        "v_src": "Dossier event_scripts/ :",
        "v_tip": "💡 Vérifie que les dialogues d'intro s'alignent bien avec leurs menus de choix.",
        "v_btn": "🔍  Vérifier les menus de choix",
        "v_ok": "Tous les menus sont cohérents !",
        "v_warn": "{n} incohérence(s) dans {f} fichier(s) — voir le journal.",
        "f_title": "F — Extraire les dialogues annexes",
        "f_src": "cpk_files/ :",
        "f_out": "Sortie JSON :",
        "f_f1": "Dialogues boutique CDs",
        "f_f2": "F_BE — dialogues de combat (Personas, ennemis, répliques en bataille)",
        "f_f3": "TM_EVE — dialogues de scènes narratives (hors combat)",
        "f_f4": "Dialogues NPC par zone",
        "f_tip": "💡 Ces fichiers contiennent PNJ, boutiques et cinématiques.",
        "f_btn": "🔍  Scanner CD_SHOP + F_BE + TM_EVE + MMAP01-06",
        # Onglet Encodage
        "enc_info": "Comment ça marche :\n  • Les JSON avec nom_fr / texte_fr remplis sont encodés en binaire.\n  • Les accents français sont convertis en glyphes japonais (ACCENT_MAP).\n  • Le terminateur _term de chaque dialogue est préservé.\n  • Les scripts event.bin sont recompressés en gzip avant injection.",
        "enc_title": "Encoder la traduction",
        "enc_trad": "Dossier traduction/ :",
        "enc_cpk": "cpk_files/ (fichiers originaux) :",
        "enc_out": "Sortie encoded/ :",
        "enc_tip": "💡 Seuls les dialogues traduits sont modifiés. Les autres restent en anglais.",
        "enc_btn": "🔄  Encoder tous les JSON traduits",
        # Onglet Rebuild
        "rb_info": "Cette étape patche event.bin traduit dans une copie de l'ISO.\nL'offset est mémorisé automatiquement à l'étape C.\n\nPrérequis : avoir complété les onglets ① ② ③.",
        "rb_title": "Créer l'ISO traduite",
        "rb_iso": "ISO originale :",
        "rb_enc": "Dossier encoded/ :",
        "rb_out": "ISO de sortie :",
        "rb_tip": "💡 L'ISO originale n'est jamais modifiée — une copie est créée.",
        "rb_btn": "🏗️  Créer l'ISO traduite",
        # Log
        "log_title": "Journal",
        "log_clear": "Effacer",
        # Statuts
        "running": "En cours…",
        "done_s": "OK",
        # Alertes
        "w_title": "Attention",
        "e_title": "Erreur",
        "ok_title": "Terminé",
        "w_no_iso": "Sélectionne un fichier ISO valide d'abord.",
        "w_no_cpk": "Sélectionne le fichier P2PT_ALL.cpk.",
        "w_no_event": "Sélectionne le fichier event.bin.",
        "w_no_scripts": "Sélectionne le dossier scripts_bin/.",
        "w_no_cpkfiles": "Le dossier cpk_files/ est introuvable.\nComplète l'étape B (CriFsLib) avant.",
        "w_no_crifsl": "CriFsLib.GUI.exe introuvable :\n{p}\nVérifie le chemin ci-dessus.",
        "w_fill_all": "Remplis tous les champs avant de continuer.",
        "w_no_iso2": "ISO originale introuvable :\n{p}",
        "w_no_encoded": "Dossier encoded/ introuvable :\n{p}\nComplète l'onglet ③ d'abord.",
        "w_no_eventbin": "event.bin absent de encoded/.\nComplète l'encodage (onglet ③) d'abord.",
        # Messages de fin
        "ok_cpk": "CPK extrait ({s} MB) :\n{p}\n\n→ Étape suivante : ouvrir CriFsLib (B).",
        "ok_crifsl": "CriFsLib est ouvert.\n→ Glisse P2PT_ALL.cpk, extrais vers cpk_files/.",
        "ok_event": "event.bin extrait :\n{p}\n\n→ Étape suivante : extraire les scripts (D).",
        "ok_scripts": "{n} scripts extraits dans :\n{p}\n\n→ Passe à l'onglet ②.",
        "ok_decode": "Scripts décodés dans :\n{p}\n\n→ Traduis les JSON, puis onglet ③.",
        "ok_scan": "✓ {n} dialogues extraits.\nJSON dans : {p}\n\n→ Traduis, puis onglet ③.",
        "ok_encode": "✓ {n} fichier(s) encodé(s) : {f}\n{e}Sortie : {p}\n\n→ Passe à l'onglet ④.",
        "ok_rebuild": "✓ ISO traduite créée ({s} MB) :\n{p}\n\nLance-la dans PPSSPP !",
        "log_crifsl1": "CriFsLib ouvert.",
        "log_crifsl2": "  → Glisse P2PT_ALL.cpk dans la fenêtre",
        "log_crifsl3": "  → Extraire vers : {p}",
    },
    "en": {
        "app_sub": "Fan translation tool  ·  Persona 2 IS PSP  ·  EUR ULES01557",
        "work_lbl": "Working folder:",
        "lang_btn": "🌐 FR",
        "tab_extract": "① Extract",
        "tab_scan": "② Translation",
        "tab_encode": "③ Encode",
        "tab_rebuild": "④ Rebuild ISO",
        "a_title": "A — Extract the CPK",
        "a_iso": "ISO file:",
        "a_note": "Output: <workdir>/P2PT_ALL.cpk",
        "a_tip": "💡 Select your original .iso file (ULES01557).",
        "a_btn": "⬇  Extract P2PT_ALL.cpk",
        "b_title": "B — Extract game files",
        "b_exe": "CriFsLib.GUI.exe:",
        "b_dl_btn": "⬇  Download CriFsLib",
        "b_instr": "  1. Download CriFsLib if needed (button above)\n  2. Click 'Open CriFsLib'\n  3. Drag P2PT_ALL.cpk into the window\n  4. Right-click → Extract All\n  5. Extract to: <workdir>/cpk_files/",
        "b_tip": "💡 CriFsLib is required for this step.",
        "b_btn": "🔧  Open CriFsLib",
        "c_title": "C — Extract game scripts",
        "c_cpk": "P2PT_ALL.cpk:",
        "c_note": "Output: <workdir>/event.bin",
        "c_tip": "💡 event.bin holds all the game's dialogue scripts.",
        "c_btn": "⬇  Extract event.bin",
        "d_title": "D — Split scripts",
        "d_event": "event.bin:",
        "d_note": "Output: <workdir>/scripts_bin/  (399 files)",
        "d_tip": "💡 Each script = one scene or location in the game.",
        "d_btn": "⬇  Extract all 399 scripts",
        "e_title": "E — Generate translation files",
        "e_src": "scripts_bin/ folder:",
        "e_out": "JSON output:",
        "e_tip": "💡 Fill in nom_fr and texte_fr in the JSON files to translate.",
        "e_btn": "📝  Decode all scripts to JSON",
        "v_title": "G — Check menu consistency",
        "v_src": "event_scripts/ folder:",
        "v_tip": "💡 Checks that intro dialogues align with their choice menus.",
        "v_btn": "🔍  Check choice menus",
        "v_ok": "All menus are consistent!",
        "v_warn": "{n} issue(s) in {f} file(s) — see the log.",
        "f_title": "F — Extract side dialogues",
        "f_src": "cpk_files/ folder:",
        "f_out": "JSON output:",
        "f_f1": "CD Shop dialogues",
        "f_f2": "F_BE — battle dialogues (Personas, enemies, character lines)",
        "f_f3": "TM_EVE — narrative scene dialogues (outside combat)",
        "f_f4": "NPC dialogues per game zone",
        "f_tip": "💡 These files contain NPC text, shop text and cutscene subtitles.",
        "f_btn": "🔍  Scan CD_SHOP + F_BE + TM_EVE + MMAP01-06",
        "enc_info": "How it works:\n  • JSON entries with nom_fr / texte_fr filled in are encoded to binary.\n  • French accents are mapped to Japanese glyphs (ACCENT_MAP).\n  • Each dialogue's _term terminator is preserved as-is.\n  • event.bin scripts are gzip-recompressed before injection.",
        "enc_title": "Encode the translation",
        "enc_trad": "translation/ folder:",
        "enc_cpk": "cpk_files/ (original files):",
        "enc_out": "encoded/ output:",
        "enc_tip": "💡 Only translated entries are modified. Everything else stays in English.",
        "enc_btn": "🔄  Encode all translated JSON files",
        "rb_info": "This step patches the translated event.bin into a copy of the ISO.\nThe offset is saved automatically at step C.\n\nPrerequisites: complete tabs ① ② ③ first.",
        "rb_title": "Build the translated ISO",
        "rb_iso": "Original ISO:",
        "rb_enc": "encoded/ folder:",
        "rb_out": "Output ISO:",
        "rb_tip": "💡 The original ISO is never modified — a copy is created.",
        "rb_btn": "🏗️  Build translated ISO",
        "log_title": "Log",
        "log_clear": "Clear",
        "running": "Running…",
        "done_s": "Done",
        "w_title": "Warning",
        "e_title": "Error",
        "ok_title": "Done",
        "w_no_iso": "Please select a valid ISO file first.",
        "w_no_cpk": "Please select the P2PT_ALL.cpk file.",
        "w_no_event": "Please select the event.bin file.",
        "w_no_scripts": "Please select the scripts_bin/ folder.",
        "w_no_cpkfiles": "The cpk_files/ folder was not found.\nComplete step B (CriFsLib) first.",
        "w_no_crifsl": "CriFsLib.GUI.exe not found:\n{p}\nCheck the path above.",
        "w_fill_all": "Please fill in all fields before continuing.",
        "w_no_iso2": "Original ISO not found:\n{p}",
        "w_no_encoded": "encoded/ folder not found:\n{p}\nComplete tab ③ first.",
        "w_no_eventbin": "event.bin missing from encoded/.\nComplete encoding (tab ③) first.",
        "ok_cpk": "CPK extracted ({s} MB):\n{p}\n\n→ Next: open CriFsLib (B).",
        "ok_crifsl": "CriFsLib is open.\n→ Drag P2PT_ALL.cpk in, extract to cpk_files/.",
        "ok_event": "event.bin extracted:\n{p}\n\n→ Next: extract scripts (D).",
        "ok_scripts": "{n} scripts extracted to:\n{p}\n\n→ Move to tab ②.",
        "ok_decode": "Scripts decoded to:\n{p}\n\n→ Translate the JSON files, then go to tab ③.",
        "ok_scan": "✓ {n} dialogues extracted.\nJSON in: {p}\n\n→ Translate, then go to tab ③.",
        "ok_encode": "✓ {n} file(s) encoded: {f}\n{e}Output: {p}\n\n→ Move to tab ④.",
        "ok_rebuild": "✓ Translated ISO created ({s} MB):\n{p}\n\nLaunch it in PPSSPP!",
        "log_crifsl1": "CriFsLib opened.",
        "log_crifsl2": "  → Drag P2PT_ALL.cpk into the window",
        "log_crifsl3": "  → Extract to: {p}",
    },
}

_lang = "fr"


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
    Aligne la question ET chaque option de menu pour correspondre exactement 
    à la taille binaire de l'original. Empêche les dépassements de mémoire 
    et préserve les pointeurs absolus du moteur vers chaque option.
    """
    marker_fr = (
        "[U+1208]" if "[U+1208]" in t_fr else ("[1208]" if "[1208]" in t_fr else None)
    )
    if marker_fr is None:
        return t_fr

    marker_orig = "[U+1208]" if "[U+1208]" in texte_orig else ("[1208]" if "[1208]" in texte_orig else None)
    if not marker_orig:
        return t_fr

    nom_orig_clean = nom_orig.replace("[SP]", " ")
    
    pre_orig, post_orig = texte_orig.split(marker_orig, 1)
    pre_fr, post_fr = t_fr.split(marker_fr, 1)

    enc_pre_orig = text_to_bytes('"' + nom_orig_clean + "\n" + pre_orig)
    enc_pre_fr = text_to_bytes('"' + nom_fr + "\n" + pre_fr)
    
    diff_q = len(enc_pre_orig) - len(enc_pre_fr)
    
    if diff_q > 0:
        pre_fr += "[SP]" * (diff_q // 2)
    elif diff_q < 0:
        import re
        while len(text_to_bytes('"' + nom_fr + "\n" + pre_fr)) > len(enc_pre_orig):
            tokens = re.split(r'(\[[a-zA-Z0-9+\-_]+\])', pre_fr)
            tokens = [t for t in tokens if t]
            if not tokens: break
            if tokens[-1].startswith('['):
                tokens.pop()
            else:
                tokens[-1] = tokens[-1][:-1]
            pre_fr = ''.join(tokens)
    
    orig_lines = post_orig.split('\n')
    fr_lines = post_fr.split('\n')
    aligned_fr_lines = []
    
    for i in range(len(fr_lines)):
        if i >= len(orig_lines):
            aligned_fr_lines.append(fr_lines[i])
            continue
            
        orig_line = orig_lines[i]
        fr_line = fr_lines[i]
        
        orig_len = len(text_to_bytes(orig_line.replace("[SP]", " ")))
        fr_len = len(text_to_bytes(fr_line))
        
        diff_opt = orig_len - fr_len
        if diff_opt > 0:
            fr_line += "[SP]" * (diff_opt // 2)
        elif diff_opt < 0:
            import re
            while len(text_to_bytes(fr_line)) > orig_len:
                tokens = re.split(r'(\[[a-zA-Z0-9+\-_]+\])', fr_line)
                tokens = [t for t in tokens if t]
                if not tokens: break
                if tokens[-1].startswith('['):
                    tokens.pop()
                else:
                    tokens[-1] = tokens[-1][:-1]
                fr_line = ''.join(tokens)
        
        aligned_fr_lines.append(fr_line)

    return pre_fr + marker_fr + '\n'.join(aligned_fr_lines)

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
            out_fr += "[SP]" * n_sp
        elif diff < 0:
            while diff < 0 and len(out_fr) > 0:
                out_fr = out_fr[:-1]
                fr_off = len(text_to_bytes('"' + nom_fr + "\n" + out_fr))
                diff = orig_off - fr_off
            
        out_fr += '[NULL][NULL]"' + parts_fr[i]
        
    return out_fr

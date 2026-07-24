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

import pycdlib
import struct, json, gzip, io, os, re, shutil, threading, subprocess, platform, concurrent.futures, zlib
from pathlib import Path
import tkinter as tk
from src.config import *
from src.config import _lang, _theme_name
from src.utils import SCAN_TARGETS
from src.utils import _offsets_path, save_offsets, load_offsets, SCAN_TARGETS
from src.core.text import _valid_name
from src.parsers.bin_parser import scan_bnp_bin
from src.parsers.fbe_parser import scan_fbe_bnp


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


def extract_cpk_from_iso(iso_path: str, out_dir: Path, log_fn, pspdecrypt_path: str = "") -> str:
    """Localise et extrait P2PT_ALL.cpk depuis l'ISO (ou le dossier extrait), ainsi que l'EBOOT.BIN."""
    iso_p = Path(iso_path)
    
    # --- Cas 1 : L'utilisateur a fourni un dossier (ISO decompressé) ---
    if iso_p.is_dir():
        if log_fn:
            log_fn(f"Lecture du dossier ISO : {iso_path}", "info")
            
        cpk_src = iso_p / "PSP_GAME" / "USRDIR" / "pack" / "P2PT_ALL.cpk"
        eboot_src = iso_p / "PSP_GAME" / "SYSDIR" / "EBOOT.BIN"
        
        out_dir.mkdir(parents=True, exist_ok=True)
        out_cpk = out_dir / "P2PT_ALL.cpk"
        out_eboot = out_dir / "EBOOT.BIN"
        
        if cpk_src.exists():
            shutil.copy2(cpk_src, out_cpk)
            if log_fn: log_fn(f"  P2PT_ALL.cpk copié depuis le dossier.", "ok")
        else:
            raise Exception("P2PT_ALL.cpk introuvable dans le dossier fourni.")
            
        if eboot_src.exists():
            shutil.copy2(eboot_src, out_eboot)
            if log_fn: log_fn("  EBOOT.BIN copié depuis le dossier.", "ok")
            
    # --- Cas 2 : L'utilisateur a fourni un fichier .iso ---
    else:
        if log_fn:
            log_fn("Lecture de l'ISO...", "info")
        iso = open(iso_path, "rb").read()
        if log_fn:
            log_fn(f"  Taille globale : {len(iso)//1024//1024} MB", "info")
            
        # 1. Extraction du CPK (Methode historique)
        pos = iso.find(b"CPK ")
        if pos == -1:
            raise Exception(
                "Fichier CPK introuvable dans l'ISO.\nVérifie qu'il s'agit bien d'une ISO ULES01557."
            )
        if log_fn:
            log_fn(f"  CPK trouvé à l'offset 0x{pos:08X}", "info")
            
        offs = load_offsets()
        offs["iso_path"] = iso_path
        offs["cpk_offset_in_iso"] = pos
        save_offsets(offs)
        
        out_dir.mkdir(parents=True, exist_ok=True)
        out_cpk = out_dir / "P2PT_ALL.cpk"
        with open(out_cpk, "wb") as f:
            f.write(iso[pos:])
        if log_fn:
            log_fn(f"  P2PT_ALL.cpk sauvegardé ({len(iso[pos:])//1024//1024} MB)", "ok")
            
        # 2. Extraction de l'EBOOT avec pycdlib
        try:
            cd = pycdlib.PyCdlib()
            cd.open(iso_path)
            out_eboot = out_dir / "EBOOT.BIN"
            try:
                cd.get_file_from_iso(str(out_eboot), iso_path='/PSP_GAME/SYSDIR/EBOOT.BIN;1')
            except Exception:
                cd.get_file_from_iso(str(out_eboot), iso_path='/PSP_GAME/SYSDIR/EBOOT.BIN')
            cd.close()
            if log_fn:
                log_fn("  EBOOT.BIN extrait avec succès de l'ISO.", "ok")
        except Exception as e:
            if log_fn:
                log_fn(f"  Erreur lors de l'extraction de l'EBOOT : {e}", "error")

    # --- Decryptage EBOOT (Commun aux deux cas) ---
    out_eboot = out_dir / "EBOOT.BIN"
    if out_eboot.exists():
        if pspdecrypt_path and Path(pspdecrypt_path).exists():
            if log_fn:
                log_fn("  Décryptage de l'EBOOT avec pspdecrypt...", "info")
            eboot_dec_out = out_dir / "EBOOT_DECRYPTED.BIN"
            try:
                subprocess.run([pspdecrypt_path, str(out_eboot)], cwd=str(out_dir), check=True, creationflags=subprocess.CREATE_NO_WINDOW)
                dec_file = out_dir / "EBOOT.BIN.dec"
                if dec_file.exists():
                    dec_file.rename(eboot_dec_out)
                    if log_fn:
                        log_fn("  EBOOT décrypté avec succès en EBOOT_DECRYPTED.BIN.", "ok")
                else:
                    if log_fn:
                        log_fn("  Erreur: EBOOT.BIN.dec introuvable après décryptage.", "error")
            except Exception as e:
                if log_fn: log_fn(f"  Erreur pspdecrypt: {e}", "error")
        else:
            if log_fn:
                log_fn("  Attention: pspdecrypt_path non fourni, l'EBOOT n'est pas décrypté.", "warning")

    return str(out_cpk)


# ── Extraction event.bin depuis CPK ──────────────────────────────────────────


def extract_event_from_cpk(cpk_path: str, out_dir: Path, log_fn) -> str:
    """Localise event.bin dans le CPK par recherche de TOC gzip. Mémorise l'offset."""
    if log_fn:
        log_fn("Lecture du CPK…", "info")
    cpk = open(cpk_path, "rb").read()
    if log_fn:
        log_fn(f"  Taille CPK : {len(cpk)//1024//1024} MB", "info")
    if log_fn:
        log_fn("  Recherche du TOC event.bin…", "info")
    best = -1
    idx = 0
    while idx < len(cpk) - 40:
        found = cpk.find(b"\x00\x10\x00\x00", idx)
        if found == -1:
            break
        if found % 4 != 0:
            idx = found + 1
            continue
        e0 = struct.unpack_from("<I", cpk, found + 4)[0]
        if not (0x20000 <= e0 <= 0x40000):
            idx = found + 1
            continue
        if found + e0 + 8 >= len(cpk):
            idx = found + 1
            continue
        gp = found + 0x1000
        if gp + 2 < len(cpk) and cpk[gp : gp + 2] == b"\x1f\x8b":
            best = found
            break
        valid = True
        pe = e0
        for k in range(1, 5):
            s = struct.unpack_from("<I", cpk, found + k * 8)[0]
            e = struct.unpack_from("<I", cpk, found + k * 8 + 4)[0]
            if s == 0:
                break
            if not (pe <= s <= pe + 0x100000) or not (s < e <= s + 0x100000):
                valid = False
                break
            pe = e
        if valid:
            best = found
            break
        idx = found + 1
    if best == -1:
        raise Exception(
            "Impossible de localiser event.bin dans le CPK automatiquement.\n→ Extrais event.bin manuellement avec CriFsLib puis charge-le à l'étape D."
        )
    entries = []
    i = best
    while i + 8 <= len(cpk):
        s = struct.unpack_from("<I", cpk, i)[0]
        e = struct.unpack_from("<I", cpk, i + 4)[0]
        if s == 0:
            break
        if entries and s < entries[-1][1]:
            break
        if e > s + 0x500000:
            break
        entries.append((s, e))
        i += 8
    if not entries:
        raise Exception("TOC vide après parsing.")
    ev_size = entries[-1][1]
    if log_fn:
        log_fn(f"  {len(entries)} entrées TOC · taille = {ev_size} octets", "info")
    offs = load_offsets()
    offs["event_offset_in_cpk"] = best
    cii = offs.get("cpk_offset_in_iso", 0)
    offs["event_offset_in_iso"] = cii + best
    offs["event_size"] = ev_size
    save_offsets(offs)
    if log_fn:
        log_fn(f"  Offset dans l'ISO : 0x{cii+best:08X}", "info")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "event.bin"
    with open(out_path, "wb") as f:
        f.write(cpk[best : best + ev_size])
    if log_fn:
        log_fn(f"  event.bin sauvegardé ({ev_size} octets)", "ok")
    return str(out_path)


# ── Extraction scripts depuis event.bin ──────────────────────────────────────


def extract_scripts_from_event(event_path: str, out_dir: Path, log_fn) -> int:
    """Découpe event.bin en 399 scripts individuels (script_000.bin … script_398.bin)."""
    data = open(event_path, "rb").read()
    out_dir.mkdir(parents=True, exist_ok=True)
    if log_fn:
        log_fn(f"  event.bin : {len(data)} octets", "info")
    entries = []
    i = 0
    while i + 8 <= len(data):
        s = struct.unpack_from("<I", data, i)[0]
        e = struct.unpack_from("<I", data, i + 4)[0]
        if s == 0:
            break
        entries.append((s, e))
        i += 8
    entries = entries[:399]
    if log_fn:
        log_fn(f"  Extraction de {len(entries)} scripts…", "info")
    ok = skip = 0
    for idx, (start, end) in enumerate(entries):
        if end > len(data) or start >= end:
            skip += 1
            continue
        chunk = data[start:end]
        if chunk[:2] == b"\x1f\x8b":
            try:
                with gzip.open(io.BytesIO(chunk)) as gz:
                    chunk = gz.read()
            except Exception as eg:
                if log_fn:
                    log_fn(f"  script_{idx:03d} : erreur gzip ({eg})", "warn")
        with open(out_dir / f"script_{idx:03d}.bin", "wb") as f:
            f.write(chunk)
        ok += 1
        if idx % 50 == 0 and log_fn:
            log_fn(f"  script_{idx:03d}.bin ({len(chunk)} octets)", "info")
    if log_fn:
        log_fn(f"  {ok} scripts extraits, {skip} ignorés → {out_dir}", "ok")
    return ok


# ── Détection des dialogues ───────────────────────────────────────────────────


def scan_cpk_files(
    cpk_dir_str: str, out_dir: Path, log_fn=None, progress_fn=None
) -> dict:
    """Scanne les fichiers cibles dans cpk_files/ et extrait leurs dialogues en JSON."""
    cpk_dir = Path(cpk_dir_str)
    out_dir.mkdir(parents=True, exist_ok=True)
    targets = sorted(SCAN_TARGETS)
    fmap = {f.name.lower(): f for f in Path(cpk_dir_str).rglob("*") if f.is_file()}
    if log_fn:
        log_fn("Scan des fichiers de jeu…", "head")
    total = []
    done = []
    offs = load_offsets()
    cpk_offset_in_iso = offs.get("cpk_offset_in_iso", 0)
    if not _bnp_offsets_look_valid(offs.get("bnp_offsets", {})):
        offs.pop("bnp_offsets", None)

    # FORCE RECALCULATION DU CACHE POUR CORRIGER LE BUG DES 12KB
    offs.pop("bnp_offsets", None)

    bnp_offsets = {}
    cpk_candidates2 = [
        cpk_dir.parent / "P2PT_ALL.cpk",
        cpk_dir / "P2PT_ALL.cpk",
    ]
    cpk_path = next((p for p in cpk_candidates2 if p.exists()), None)
    if cpk_path:
        bnp_offsets = _find_bnp_offsets_in_cpk(
            cpk_path, set(targets), cpk_offset_in_iso
        )
    if not bnp_offsets:
        iso_path_str = offs.get("iso_path", "")
        bnp_offsets = _find_bnp_offsets_in_iso(
            iso_path_str, cpk_dir, set(targets), cpk_offset_in_iso
        )
    for i, tname in enumerate(targets):
        if progress_fn:
            progress_fn((i + 1) / len(targets))
        fp = fmap.get(tname)
        if not fp:
            continue
        try:
            raw = open(fp, "rb").read()
        except:
            continue
        n = scan_bnp_bin(raw, fp.stem, out_dir, log_fn)
        total.append(n)
        if n > 0:
            done.append(tname)
    if bnp_offsets:
        offs["bnp_offsets"] = bnp_offsets
        save_offsets(offs)
    if log_fn:
        log_fn(f"  Total : {sum(total)} dialogues dans {len(done)} fichiers", "ok")
    return {"total": sum(total), "files": done}


# ── Rebuild event.bin ─────────────────────────────────────────────────────────


def _parse_cpk_utf(data: bytes, offset: int) -> list:
    """Parse une table @UTF du CPK CRI (big-endian, header 32 bytes)."""
    if len(data) < offset + 32 or data[offset : offset + 4] != b"@UTF":
        return []
    try:
        base = offset + 8  # base pour rows/strings/data offsets
        rows_off = struct.unpack_from(">I", data, offset + 0x08)[0]
        strings_off = struct.unpack_from(">I", data, offset + 0x0C)[0]
        data_off = struct.unpack_from(">I", data, offset + 0x10)[0]
        num_cols = struct.unpack_from(">H", data, offset + 0x18)[0]
        row_stride = struct.unpack_from(">H", data, offset + 0x1A)[0]
        num_rows = struct.unpack_from(">I", data, offset + 0x1C)[0]
        str_base = base + strings_off
        data_base = base + data_off

        def read_str(pos):
            s = b""
            while pos < len(data) and data[pos]:
                s += bytes([data[pos]])
                pos += 1
            return s.decode("utf-8", "replace")

        def read_val(p, ftype):
            if ftype == 0x00:
                return data[p] if p < len(data) else 0, p + 1
            if ftype == 0x01:
                return struct.unpack_from(">b", data, p)[0], p + 1
            if ftype == 0x02:
                return struct.unpack_from(">H", data, p)[0], p + 2
            if ftype == 0x03:
                return struct.unpack_from(">h", data, p)[0], p + 2
            if ftype == 0x04:
                return struct.unpack_from(">I", data, p)[0], p + 4
            if ftype == 0x05:
                return struct.unpack_from(">i", data, p)[0], p + 4
            if ftype == 0x06:
                return struct.unpack_from(">Q", data, p)[0], p + 8
            if ftype == 0x07:
                return struct.unpack_from(">q", data, p)[0], p + 8
            if ftype == 0x08:
                return struct.unpack_from(">f", data, p)[0], p + 4
            if ftype == 0x0A:
                soff = struct.unpack_from(">I", data, p)[0]
                p += 4
                return read_str(str_base + soff), p
            if ftype == 0x0B:
                doff = struct.unpack_from(">I", data, p)[0]
                dsize = struct.unpack_from(">I", data, p + 4)[0]
                return None, p + 8
            return None, p

        fields = []
        fp = offset + 0x20
        for _ in range(num_cols):
            if fp + 5 > len(data):
                break
            flags = data[fp]
            fp += 1
            name_soff = struct.unpack_from(">I", data, fp)[0]
            fp += 4
            name = read_str(str_base + name_soff)
            ftype = flags & 0x0F
            storage = (flags >> 4) & 0x0F
            default = None
            if storage == 1:  # valeur constante (pas de données dans la row)
                default, fp = read_val(fp, ftype)
            fields.append((name, ftype, storage, default))

        rows = []
        rows_start = base + rows_off
        for i in range(num_rows):
            rp = rows_start + i * row_stride if row_stride else rows_start
            row = {}
            for name, ftype, storage, default in fields:
                if storage == 1:
                    row[name] = default
                elif storage in (3, 5):
                    val, rp = read_val(rp, ftype)
                    row[name] = val
            rows.append(row)
        return rows
    except Exception:
        return []


def _read_cpk_header(data: bytes, cpk_off: int = 0) -> dict:
    """Lit ContentOffset, TocOffset, TocSize depuis le CpkHeader @UTF."""
    if len(data) < cpk_off + 0x30 or data[cpk_off : cpk_off + 4] != b"CPK ":
        return {}
    utf_off = cpk_off + 0x10
    if data[utf_off : utf_off + 4] != b"@UTF":
        return {}
    try:
        base = utf_off + 8
        rows_off = struct.unpack_from(">I", data, utf_off + 0x08)[0]
        row_base = base + rows_off
        if row_base + 40 > len(data):
            return {}
        content_off = struct.unpack_from(">Q", data, row_base + 8)[0]
        content_sz = struct.unpack_from(">Q", data, row_base + 16)[0]
        toc_off = struct.unpack_from(">Q", data, row_base + 24)[0]
        toc_sz = struct.unpack_from(">Q", data, row_base + 32)[0]
        return {
            "ContentOffset": content_off,
            "ContentSize": content_sz,
            "TocOffset": toc_off,
            "TocSize": toc_sz,
        }
    except Exception:
        return {}


def _find_bnp_offsets_in_iso(
    iso_path: str, cpk_dir: Path, targets: set, cpk_offset_in_iso: int
) -> dict:
    """Cherche chaque BNP dans l'ISO directement par ses bytes caractéristiques."""
    if not iso_path or not Path(iso_path).exists():
        return {}
    result = {}
    fmap = {f.name.lower(): f for f in cpk_dir.rglob("*") if f.is_file()}
    try:
        with open(iso_path, "rb") as iso_f:
            iso_f.seek(0, 2)
            iso_size = iso_f.tell()
            search_start = cpk_offset_in_iso
            search_end = iso_size
            iso_f.seek(search_start)
            cpk_data = iso_f.read(search_end - search_start)
    except Exception:
        return {}
    used_positions = set()
    for tname in targets:
        fp = fmap.get(tname)
        if not fp:
            continue
        try:
            raw = open(fp, "rb").read()
        except Exception:
            continue
        signature = raw[:128]
        check_off = min(4096, len(raw) - 64)
        check_sig = raw[check_off : check_off + 64] if check_off > 0 else b""
        pos = -1
        search_from = 0
        while True:
            candidate = cpk_data.find(signature, search_from)
            if candidate == -1:
                break
            if candidate not in used_positions:
                if check_sig and check_off > 0:
                    if (
                        cpk_data[candidate + check_off : candidate + check_off + 64]
                        == check_sig
                    ):
                        pos = candidate
                        break
                    search_from = candidate + 1
                    continue
                else:
                    pos = candidate
                    break
            search_from = candidate + 1
        if pos == -1:
            pos = cpk_data.find(raw[:32])
        if pos == -1 or pos in used_positions:
            continue
        used_positions.add(pos)
        result[tname] = {
            "offset_in_cpk": pos,
            "offset_in_iso": search_start + pos,
            "size": len(raw),
        }
    return result


def _parse_cpk_toc_rows(toc_data: bytes, toc_utf_off: int) -> list:
    """Parse la table TOC réelle de ce CPK Atlus PSP."""
    if (
        len(toc_data) < toc_utf_off + 0x20
        or toc_data[toc_utf_off : toc_utf_off + 4] != b"@UTF"
    ):
        return []
    try:
        base = toc_utf_off + 8
        rows_off = struct.unpack_from(">I", toc_data, toc_utf_off + 0x08)[0]
        strings_off = struct.unpack_from(">I", toc_data, toc_utf_off + 0x0C)[0]
        row_stride = struct.unpack_from(">H", toc_data, toc_utf_off + 0x1A)[0]
        num_rows = struct.unpack_from(">I", toc_data, toc_utf_off + 0x1C)[0]
        str_base = base + strings_off
        rows_start = base + rows_off

        def read_str(pos):
            s = b""
            while pos < len(toc_data) and toc_data[pos]:
                s += bytes([toc_data[pos]])
                pos += 1
            return s.decode("utf-8", "replace")

        results = []
        for i in range(num_rows):
            rp = rows_start + i * row_stride
            if rp + 20 > len(toc_data):
                break
            name_off = struct.unpack_from(">I", toc_data, rp)[0]
            file_size = struct.unpack_from(">I", toc_data, rp + 4)[0]
            ext_size = struct.unpack_from(">I", toc_data, rp + 8)[0]
            file_off = struct.unpack_from(">I", toc_data, rp + 16)[0]
            fname = read_str(str_base + name_off)
            results.append(
                {
                    "FileName": fname,
                    "FileOffset": file_off,
                    "FileSize": file_size,
                    "ExtractSize": ext_size,
                    "RowOffset": rp,
                }
            )
        return results
    except Exception:
        return []


def _find_bnp_offsets_in_cpk(
    cpk_path: Path, targets: set, cpk_offset_in_iso: int
) -> dict:
    """Parse la table TOC du CPK pour trouver les offsets des BNP."""
    if not cpk_path.exists():
        return {}
    try:
        with open(cpk_path, "rb") as f:
            header = f.read(512)
        if header[:4] != b"CPK ":
            return {}
        hdr_info = _read_cpk_header(header, 0)
        toc_off = hdr_info.get("TocOffset")
        toc_size = hdr_info.get("TocSize")
        content_off = hdr_info.get("ContentOffset", 0) or 0
        if not toc_off or not toc_size:
            return {}
        with open(cpk_path, "rb") as f:
            f.seek(int(toc_off))
            toc_data = f.read(int(toc_size) + 64)
        toc_utf_off = None
        for probe in (16, 0, 8):
            if len(toc_data) > probe + 4 and toc_data[probe : probe + 4] == b"@UTF":
                toc_utf_off = probe
                break
        if toc_utf_off is None:
            return {}
        toc_rows = _parse_cpk_toc_rows(toc_data, toc_utf_off)
        result = {}
        for row in toc_rows:
            fname = (row.get("FileName") or "").lower()
            if fname in targets:
                file_off = row.get("FileOffset")
                file_size = row.get("FileSize")
                ext_size = row.get("ExtractSize")
                rp = row.get("RowOffset")
                if file_off is None or file_size is None or ext_size is None:
                    continue
                abs_iso_off = cpk_offset_in_iso + 0x3800 + file_off
                result[fname] = {
                    "offset_in_cpk": 0x3800 + file_off,
                    "offset_in_iso": abs_iso_off,
                    "size": ext_size,
                    "stored_size": file_size,
                    "toc_row_iso_off": cpk_offset_in_iso + int(toc_off) + rp,
                }
        return result
    except Exception:
        return {}


def _bnp_offsets_look_valid(bnp_offsets: dict) -> bool:
    """Détecte un cache corrompu."""
    if not bnp_offsets:
        return False
    seen = {}
    for tname, meta in bnp_offsets.items():
        off = meta.get("offset_in_iso")
        if off in seen:
            return False
        seen[off] = tname
    return True


def rebuild_event_bin(
    orig_event: bytes, scripts_fr_dir: Path, log_fn, scripts_bin_dir: Path = None
) -> bytes:
    """Réinjecte les scripts traduits dans event.bin."""
    event = bytearray(orig_event)
    toc = []
    i = 0
    while i + 8 <= len(event):
        s = struct.unpack_from("<I", event, i)[0]
        e = struct.unpack_from("<I", event, i + 4)[0]
        if s == 0:
            break
        toc.append((s, e, i))
        i += 8
    patched = kept_orig = 0
    for idx, (start, end, tp) in enumerate(toc):
        fr = scripts_fr_dir / f"script_{idx:03d}_fr.bin"
        if not fr.exists():
            fr = scripts_fr_dir / f"script_{idx}_fr.bin"
        if fr.exists():
            sc = open(fr, "rb").read()
        elif scripts_bin_dir is not None:
            orig = scripts_bin_dir / f"script_{idx:03d}.bin"
            if not orig.exists():
                orig = scripts_bin_dir / f"script_{idx}.bin"
            if orig.exists():
                sc = open(orig, "rb").read()
                kept_orig += 1
            else:
                continue
        else:
            continue
        gz_buf = io.BytesIO()
        with gzip.GzipFile(
            filename=b"e0000.bin", mode="wb", fileobj=gz_buf, mtime=0
        ) as gz:
            gz.write(sc)
        new_gz = gz_buf.getvalue()
        if len(new_gz) > end - start:
            continue
        event[start : start + len(new_gz)] = new_gz
        event[start + len(new_gz) : end] = bytes((end - start) - len(new_gz))
        # Ne PAS modifier l'index de fin (tp+4) ! Le jeu a besoin que end - start
        # corresponde exactement à l'espace mémoire alloué, même s'il y a du padding !
        patched += 1
    return bytes(event)


# ── Rebuild ISO ───────────────────────────────────────────────────────────────


def update_iso_metadata(f, cpk_offset, new_end_offset, log_fn):
    """
    Hack de la taille de l'ISO et du CPK pour autoriser la lecture au-delà de la limite officielle.
    """
    if log_fn:
        log_fn("  [HACK] Application du hack ISO9660 et CPK Header...", "info")
    import struct

    try:
        new_size = new_end_offset - cpk_offset

        # 1. Le CPK Header n'a PAS besoin d'etre patche !
        # Le jeu lit sans probleme au-dela de sa propre ContentSize.
        # Patch ContentSize, EnabledPackedSize, ou EnabledDataSize fait saturer la RAM de la PSP et freeze au logo !

        # 2. Update Primary Volume Descriptor (PVD)
        f.seek(16 * 2048)
        pvd = bytearray(f.read(2048))
        if pvd[:7] == b"\x01CD001\x01":
            sectors = (new_end_offset + 2047) // 2048
            pvd[80:88] = struct.pack("<I", sectors) + struct.pack(">I", sectors)
            f.seek(16 * 2048)
            f.write(pvd)
        else:
            if log_fn:
                log_fn("  [ERREUR] PVD ISO9660 introuvable.", "err")

        # 3. Update Directory Entry for P2PT_ALL.CPK
        f.seek(0)
        iso_start = bytearray(f.read(2 * 1024 * 1024))
        iso_start_lower = bytearray(iso_start).lower()
        pos = 0
        found = 0
        while True:
            pos = iso_start_lower.find(b"p2pt_all.cpk", pos)
            if pos == -1:
                break
            rec_start = pos - 33
            if rec_start >= 0:
                rec_len = iso_start[rec_start]
                if rec_len >= 34:
                    f.seek(rec_start + 10)
                    f.write(struct.pack("<I", new_size))
                    f.write(struct.pack(">I", new_size))
                    found += 1
            pos += 1
        if found > 0:
            if log_fn:
                log_fn(
                    f"  [TOC PATCH] Limites ISO/CPK etendues virtuellement a {new_size//1024//1024} MB ({found} entrees) avec succes !",
                    "ok",
                )
        else:
            if log_fn:
                log_fn("  [ERREUR] Entree ISO9660 P2PT_ALL.CPK introuvable.", "err")

    except Exception as e:
        if log_fn:
            log_fn(f"  [ERREUR CRITIQUE] Echec du hack ISO9660: {e}", "err")


def rebuild_iso(
    iso_orig: str, event_data: bytes, out_iso: str, log_fn, enc_dir: str = None
) -> bool:
    import pathlib
    import shutil
    iso_p = pathlib.Path(iso_orig)
    offs = load_offsets()
    
    # --- Mode Dossier ---
    if iso_p.is_dir():
        if log_fn: log_fn("Reconstruction dans un dossier...", "info")
        cpk_path = iso_p / "PSP_GAME" / "USRDIR" / "pack" / "P2PT_ALL.cpk"
        if not cpk_path.exists():
            raise Exception("P2PT_ALL.cpk introuvable dans le dossier original.")
        
        shutil.copy(str(cpk_path), out_iso)
        
        cpk_off_in_iso = 0
        event_pos = offs.get("event_offset_in_cpk", -1)
        if event_pos == -1:
            raise Exception("Offset event.bin dans le CPK inconnu. Relance l'extraction.")
            
        with open(out_iso, "r+b") as f:
            if log_fn: log_fn(f"  Patch event.bin a l'offset 0x{event_pos:08X} du CPK", "info")
            f.seek(event_pos)
            f.write(event_data)
            
            bnp_offsets = offs.get("bnp_offsets", {})
            if enc_dir and pathlib.Path(enc_dir).exists() and bnp_offsets:
                for bnp_name, offset_in_cpk in bnp_offsets.items():
                    src_bnp = pathlib.Path(enc_dir) / bnp_name
                    if src_bnp.exists():
                        data = src_bnp.read_bytes()
                        f.seek(offset_in_cpk)
                        f.write(data)
                        if log_fn: log_fn(f"  Injecte {bnp_name} a 0x{offset_in_cpk:08X}", "info")
        
        if log_fn: log_fn("Le fichier .cpk patche a ete cree a la place de l'ISO de sortie. Veuillez le renommer et le placer manuellement dans le jeu.", "warn")
        return True

    # --- Mode ISO ---
    pos = offs.get("event_offset_in_iso", -1)
    if pos != -1:
        with open(iso_orig, "rb") as f:
            f.seek(pos)
            import struct
            chk = struct.unpack("<I", f.read(4))[0]
        if chk != 0x1000:
            if log_fn:
                log_fn(
                    f"  Offset memorise invalide (0x{chk:x}), re-extraction necessaire.",
                    "warn",
                )
            pos = -1
    if pos == -1:
        raise Exception(
            "Offset event.bin inconnu. Relance l'Extraction du CPK (Etape A) pour le recalculer."
        )
    max_iso_offset = 0
    shutil.copy(iso_orig, out_iso)
    with open(out_iso, "r+b") as f:
        if log_fn:
            log_fn(f"  event.bin → offset 0x{pos:08X}", "info")
        f.seek(pos)
        f.write(event_data)
        cpk_off_in_iso = offs.get("cpk_offset_in_iso", 0)

        # FORCE RECALCULATION DU CACHE
        offs.pop("bnp_offsets", None)

        bnp_offsets = offs.get("bnp_offsets", {})
        if not bnp_offsets and enc_dir:
            work_dir = Path(enc_dir).parent
            iso_orig_path = offs.get("iso_path", "")
            cpk_candidates = [
                work_dir / "P2PT_ALL.cpk",
                Path(enc_dir) / "P2PT_ALL.cpk",
                (
                    Path(iso_orig_path).parent / "P2PT_ALL.cpk"
                    if iso_orig_path
                    else Path("nonexistent")
                ),
            ]
            cpk_path = next((p for p in cpk_candidates if p.exists()), None)
            if cpk_path:
                bnp_offsets = _find_bnp_offsets_in_cpk(
                    cpk_path, set(SCAN_TARGETS), cpk_off_in_iso
                )
            if not bnp_offsets:
                cpk_files_dir = next(
                    (
                        p
                        for p in [work_dir / "cpk_files", Path(enc_dir) / "cpk_files"]
                        if p.exists()
                    ),
                    work_dir,
                )
                bnp_offsets = _find_bnp_offsets_in_iso(
                    iso_orig_path, cpk_files_dir, set(SCAN_TARGETS), cpk_off_in_iso
                )
        if bnp_offsets:
            offs["bnp_offsets"] = bnp_offsets
            save_offsets(offs)
            if log_fn:
                log_fn(f"  {len(bnp_offsets)} BNP localisés ✓", "info")
        else:
            if log_fn:
                log_fn(
                    "  ⚠ BNP introuvables dans l'ISO — MMAP/F_BE non injectés", "warn"
                )
        if enc_dir and bnp_offsets:
            enc = Path(enc_dir)
            bnp_files = [
                ("CD_SHOP.BIN", "cd_shop.bin"),
                ("F_BE.BNP", "f_be.bnp"),
                ("TM_EVE.BNP", "tm_eve.bnp"),
                ("MMAP01.BNP", "mmap01.bnp"),
                ("MMAP02.BNP", "mmap02.bnp"),
                ("MMAP03.BNP", "mmap03.bnp"),
                ("MMAP04.BNP", "mmap04.bnp"),
                ("MMAP05.BNP", "mmap05.bnp"),
                ("MMAP06.BNP", "mmap06.bnp"),
            ]
            for fn_enc, fn_key in bnp_files:
                enc_path = enc / fn_enc
                if not enc_path.exists():
                    continue
                meta = bnp_offsets.get(fn_key) or bnp_offsets.get(fn_key.upper())
                if not meta:
                    if log_fn:
                        log_fn(f"  ⚠ {fn_enc} : offset introuvable dans la TOC", "warn")
                    continue
                iso_off = meta["offset_in_iso"]
                extract_size = meta["size"]  # taille réelle décompressée attendue
                stored_size = meta.get(
                    "stored_size", extract_size
                )  # espace réellement alloué dans le CPK
                new_data = open(enc_path, "rb").read()

                # HACK SALVATEUR : On désactive la recompression CRILAYLA expérimentale qui corrompt le jeu.
                # Si le fichier original était compressé, on va forcer le moteur du jeu (CRI) à le lire
                # en format non-compressé (BRUT) en écrivant FileSize == ExtractSize dans la TOC.
                needs_compression = stored_size < extract_size
                if needs_compression:
                    if len(new_data) != extract_size:
                        if log_fn:
                            log_fn(
                                f"  ⚠ {fn_enc} : taille décodée ({len(new_data)}) ≠ "
                                f"taille attendue ({extract_size}), ignoré",
                                "warn",
                            )
                        continue
                    if log_fn:
                        log_fn(
                            f"  [INFO] Traitement de {fn_enc} sans recompression...",
                            "info",
                        )

                    compressed = (
                        new_data  # Pas de compression ! On garde les données brutes.
                    )

                    if len(compressed) > stored_size:
                        if fn_enc.upper() == "F_BE.BNP":
                            if log_fn:
                                log_fn(f"  [+] [INTERDIT] {fn_enc} est trop volumineux et le LBA hack est INTERDIT pour ce fichier. Crash Philémon evité !", "err")
                            continue
                            
                        if log_fn:
                            log_fn(
                                f"  [+] [TOC PATCH] {fn_enc} est trop volumineux ({len(compressed)} > {stored_size}), deplacement a la FIN de l'ISO !",
                                "ok",
                            )
                        f.seek(0, 2)  # EOF
                        padding = (2048 - (f.tell() % 2048)) % 2048
                        if padding:
                            f.write(b"\x00" * padding)

                        iso_off = f.tell()  # NOUVEL OFFSET DE FIN
                        new_file_off = iso_off - (cpk_off_in_iso + 0x3800)

                        # Met a jour FileOffset dans la TOC (U32 a toc_row_off + 16 ! PAS U64 a +12 !)
                        toc_row_off = meta.get("toc_row_iso_off")
                        if toc_row_off:
                            f.seek(toc_row_off + 16)
                            f.write(struct.pack(">I", new_file_off))

                            # PATCH MAJEUR : On met à jour la limite de lecture du CPK (ContentSize)
                            # Sinon, le jeu refuse de lire les fichiers au-delà de 254 Mo (écran noir)
                            new_content_size = new_file_off + len(compressed)
                            f.seek(cpk_off_in_iso)
                            cpk_header = f.read(512)
                            utf_off = 0x10
                            base = utf_off + 8
                            rows_off = struct.unpack_from(
                                ">I", cpk_header, utf_off + 0x08
                            )[0]
                            row_base = base + rows_off
                            old_content_size = struct.unpack_from(
                                ">Q", cpk_header, row_base + 16
                            )[0]

                            if new_content_size > old_content_size:
                                f.seek(cpk_off_in_iso + row_base + 16)
                                f.write(struct.pack(">Q", new_content_size))
                                if log_fn:
                                    log_fn(
                                        f"  [+] [TOC PATCH] ContentSize reculé de {old_content_size//1024//1024}MB à {new_content_size//1024//1024}MB",
                                        "ok",
                                    )

                        stored_size = len(
                            compressed
                        )  # On leve la limite pour la suite du script
                        max_iso_offset = max(max_iso_offset, iso_off + stored_size)

                    # IMPORTANT: On ne padde plus ! On écrit le flux compressé nu.
                    # Le padding causait un crash sur console à cause du bounds check strict.
                    write_data = compressed
                else:
                    if len(new_data) > stored_size:
                        if log_fn:
                            log_fn(
                                f"  ⚠ {fn_enc} trop grand ({len(new_data)} > {stored_size}), ignoré",
                                "warn",
                            )
                        continue
                    write_data = new_data

                f.seek(iso_off)
                f.write(write_data)

                # Fichiers non compressés ou trop courts : on nettoie les restes avec des zéros
                # (uniquement derrière le fichier, là où le jeu ne les lira pas)
                if len(write_data) < stored_size:
                    f.write(b"\x00" * (stored_size - len(write_data)))

                # MAGIE NOIRE : Mise à jour de la TOC de l'ISO en direct
                # Si on a l'offset exact de la taille du fichier dans la TOC
                toc_row_off = meta.get("toc_row_iso_off")
                if toc_row_off:
                    f.seek(toc_row_off + 4)  # FileSize
                    f.write(struct.pack(">I", len(write_data)))
                    f.seek(toc_row_off + 8)  # ExtractSize
                    f.write(struct.pack(">I", len(new_data)))

                    if log_fn:
                        log_fn(
                            f"  [TOC] Mise a jour de la table a l'adresse 0x{toc_row_off:08X} (Nouveau FileSize: {len(write_data)}, ExtractSize: {len(new_data)})",
                            "info",
                        )
                if log_fn:
                    log_fn(
                        f"  [>] INJECTION de {fn_enc} -> offset 0x{iso_off:08X} ({len(write_data)} / {stored_size} bytes) terminee.",
                        "info",
                    )

        if max_iso_offset > 0:
            f.seek(0, 2)
            rem = f.tell() % 2048
            if rem != 0:
                f.write(b"\x00" * (2048 - rem))
            update_iso_metadata(f, cpk_off_in_iso, f.tell(), log_fn)

        # --- Injection EBOOT_MODIFIED.BIN ---
        if enc_dir:
            eboot_mod = Path(enc_dir).parent / "EBOOT_MODIFIED.BIN"
            if eboot_mod.exists():
                try:
                    import pycdlib
                    cd = pycdlib.PyCdlib()
                    cd.open(iso_orig)
                    try:
                        r = cd.get_record(iso_path='/PSP_GAME/SYSDIR/EBOOT.BIN;1')
                    except:
                        r = cd.get_record(iso_path='/PSP_GAME/SYSDIR/EBOOT.BIN')
                    
                    # Ensure compatibility with different versions of pycdlib
                    loc = None
                    if hasattr(r, 'extent_location'):
                        if callable(r.extent_location):
                            loc = r.extent_location()
                        else:
                            loc = r.extent_location
                            
                    eboot_offset = loc * 2048 if loc else 0
                    eboot_size = r.get_data_length()
                    cd.close()
                    
                    if eboot_offset > 0:
                        f.seek(eboot_offset)
                        data = eboot_mod.read_bytes()
                        # Pad data to original eboot_size to prevent garbage at end
                        if len(data) < eboot_size:
                            data += b'\0' * (eboot_size - len(data))
                        elif len(data) > eboot_size:
                            data = data[:eboot_size]
                        f.write(data)
                        if log_fn: log_fn(f"  [>] INJECTION de EBOOT.BIN -> offset 0x{eboot_offset:08X} ({len(data)} bytes) terminee.", "ok")
                except Exception as e:
                    if log_fn: log_fn(f"  [!] Erreur lors de l'injection de l'EBOOT : {e}", "err")

    sz = Path(out_iso).stat().st_size // 1024 // 1024
    if log_fn:
        log_fn(f"  [V] ISO modifiee generee avec succes : {out_iso} ({sz} MB)", "ok")
    return True


# ── Encodage BNP (MMAP01-06, CD_SHOP) ────────────────────────────────────────

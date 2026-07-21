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
from src.core.text import _needs_nl_suffix, _align_menu_text
from src.config import _lang, _theme_name
from src.core.text import text_to_bytes
from src.parsers.bin_parser import find_dialogs, _rebuild_choice_body


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


def encode_bin_from_json(
    bin_path: str, json_path: str, log_fn, out_path: str = None
) -> str:
    """Réécrit les dialogues traduits dans le fichier .bin. Préserve le _term et le slot_size."""
    data = bytearray(open(bin_path, "rb").read())
    dlgs = json.loads(open(json_path, encoding="utf-8").read(), strict=False)
    ok = skip = kept = 0
    for d in dlgs:
        n_fr_input = d.get("nom_fr", "").strip()
        t_fr_input = d.get("texte_fr", "").strip()
        # Si c'est un menu de choix avec les champs dédiés, reconstruire texte_fr
        choix_fr = d.get("choix_fr")
        q_fr = d.get("question_fr", "").strip()
        if choix_fr is not None:
            # Utiliser question_fr/choix_fr si remplis, sinon fallback sur texte_fr
            filled_choices = [c for c in choix_fr if c.strip()]
            if q_fr and filled_choices:
                t_fr = _rebuild_choice_body(q_fr, choix_fr)
            elif not t_fr_input:
                # Rien de traduit du tout → skip
                kept += 1
                continue
            else:
                t_fr = t_fr_input
        elif not n_fr_input and not t_fr_input:
            kept += 1
            continue
        else:
            t_fr = t_fr_input or d.get("texte_orig", "").strip()

        n_fr = n_fr_input or d.get("nom_orig", "").strip()

        term = d.get("_term", [E1, E2, E3, E4])
        avail = d["data_size"] - (len(term) * 2)
        # NL avant terminateur : règle binaire universelle (event + MMAP + autres)
        nl_suffix = (
            struct.pack("<H", NL)
            if _needs_nl_suffix(term, d.get("texte_orig", ""))
            else b""
        )
        # Aligner AVANT d'encoder (on a besoin d'avail pour le test d'alignement)
        enc_pre = text_to_bytes('"' + n_fr + "\n" + t_fr)
        t_fr_aligned = _align_menu_text(
            d.get("nom_orig", ""), d.get("texte_orig", ""), n_fr, t_fr
        )
        enc_aligned = text_to_bytes('"' + n_fr + "\n" + t_fr_aligned)
        if len(enc_aligned) + len(nl_suffix) <= avail:
            enc = enc_aligned
        else:
            # Alignement impossible → garder sans align, warn si menu
            enc = enc_pre
            if "[1208]" in t_fr or "[U+1208]" in t_fr:
                marker = "[U+1208]" if "[U+1208]" in t_fr else "[1208]"
                pre_fr = text_to_bytes('"' + n_fr + "\n" + t_fr.split(marker)[0])
                pre_or = text_to_bytes(
                    '"'
                    + d.get("nom_orig", "").replace("[SP]", " ")
                    + "\n"
                    + d.get("texte_orig", "").split("[1208]")[0]
                )
                if len(pre_fr) > len(pre_or) and log_fn:
                    log_fn(
                        f"  ⚠ [id {d['id']}] question FR trop longue de {(len(pre_fr)-len(pre_or))//2} mot(s) → alignement désactivé.",
                        "warn",
                    )
        if len(enc) + len(nl_suffix) > avail:
            depassement = len(enc) + len(nl_suffix) - avail
            if log_fn:
                log_fn(
                    f"  [!] [DEPASSEMENT] [id {d['id']}] Texte FR trop long de {depassement} octets ({len(enc)} > {avail}). Troncature automatique.",
                    "warn",
                )
            import re
            tokens = re.split(r'(\[[a-zA-Z0-9+\-_]+\]|\s)', t_fr)
            tokens = [t for t in tokens if t]
            
            while tokens and len(text_to_bytes('"' + n_fr + "\n" + ''.join(tokens))) > avail - len(nl_suffix):
                tokens.pop()
                
            t_fr = ''.join(tokens)
            enc = text_to_bytes('"' + n_fr + "\n" + t_fr)
            
        pad_len = avail - len(enc) - len(nl_suffix)
        if pad_len < 0:
            pad_len = 0

        end_c = b"".join(struct.pack("<H", t) for t in term)
        null_gap_orig = data[
            d["offset"] + d["data_size"] : d["offset"] + d["slot_size"]
        ]

        # PAD AVANT LE TERMINATEUR avec des espaces (0x1120) pour que le texte soit juste plus long
        # et que le moteur de script atterrisse sur le bon opcode suivant !
        # Le padding après le terminateur (0x0000) plantait le jeu car exécuté comme opcode par le moteur.
        null_pad = struct.pack("<H", 0x1120) * (pad_len // 2)
        full = enc + null_pad + nl_suffix + end_c + null_gap_orig

        if len(full) != d["slot_size"]:
            skip += 1
            continue
        data[d["offset"] : d["offset"] + d["slot_size"]] = full
        ok += 1
    if out_path is None:
        out_path = bin_path
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(data)
    if log_fn:
        log_fn(
            f"  [RESUME] {Path(out_path).name} : {ok} injectes avec succes, {skip} rejetes (trop longs), {kept} laisses en japonais.",
            "ok",
        )
    return out_path


# ── Scan fichiers BNP/BIN ─────────────────────────────────────────────────────


def encode_bnp_from_json(
    bin_path: str, json_path: str, log_fn, out_path: str = None
) -> str:
    """
    Réécrit les dialogues traduits dans un fichier BNP/BIN qui peut contenir
    des blocs gzip embeddés (MMAP01-06).

    Stratégie :
    - Entrées sans _source (dialogues dans le BNP brut) → même logique que encode_bin_from_json
    - Entrées avec _source="gz@0xOFFSET" → décompresser le bloc gzip à cet offset,
      patcher le dialogue dedans, recompresser, réinjecter dans le BNP
    """
    data = bytearray(open(bin_path, "rb").read())
    dlgs = json.loads(open(json_path, encoding="utf-8").read(), strict=False)

    # Grouper les entrées par source
    direct = []  # pas de _source : offset direct dans BNP
    by_gz = {}  # "gz@0xXXXX" → liste d'entrées

    for d in dlgs:
        src = d.get("_source", "")
        if src.startswith("gz@"):
            by_gz.setdefault(src, []).append(d)
        else:
            direct.append(d)

    ok = skip = kept = 0

    # ── 1. Entrées directes (même logique que encode_bin_from_json) ───────────
    for d in direct:
        n_fr_input = d.get("nom_fr", "").strip()
        t_fr_input = d.get("texte_fr", "").strip()
        choix_fr = d.get("choix_fr")
        q_fr = d.get("question_fr", "").strip()
        if choix_fr is not None:
            filled = [c for c in choix_fr if c.strip()]
            if q_fr and filled:
                t_fr = _rebuild_choice_body(q_fr, choix_fr)
            elif not t_fr_input:
                kept += 1
                continue
            else:
                t_fr = t_fr_input
        elif not n_fr_input and not t_fr_input:
            kept += 1
            continue
        else:
            t_fr = t_fr_input or d.get("texte_orig", "").strip()

        n_fr = n_fr_input or d.get("nom_orig", "").strip()
        t_fr = _align_menu_text(
            d.get("nom_orig", ""), d.get("texte_orig", ""), n_fr, t_fr
        )
        enc = text_to_bytes('"' + n_fr + "\n" + t_fr)
        term = d.get("_term", [E1, E2, E3, E4])
        avail = d["data_size"] - (len(term) * 2)
        is_menu = "[1208]" in d.get("texte_orig", "") or "[U+1208]" in d.get(
            "texte_orig", ""
        )
        nl_sfx = struct.pack("<H", NL) if is_menu else b""

        # TRONCATURE AUTOMATIQUE SÉCURISÉE si le texte FR est trop long
        if len(enc) > avail - len(nl_sfx):
            depassement = len(enc) - (avail - len(nl_sfx))
            if log_fn:
                log_fn(
                    f"  [!] [DEPASSEMENT] [id {d['id']}] Texte FR trop long de {depassement//2} caracteres.",
                    "warn",
                )
            
            import re
            tokens = re.split(r'(\[[a-zA-Z0-9+\-_]+\]|\s)', t_fr)
            tokens = [t for t in tokens if t]
            
            while tokens and len(text_to_bytes('"' + n_fr + "\n" + ''.join(tokens))) > avail - len(nl_sfx):
                tokens.pop()
                
            t_fr = ''.join(tokens)
            enc = text_to_bytes('"' + n_fr + "\n" + t_fr)

        pad_len = avail - len(enc) - len(nl_sfx)
        end_c = b"".join(struct.pack("<H", t) for t in term)
        null_gap_orig = data[
            d["offset"] + d["data_size"] : d["offset"] + d["slot_size"]
        ]
        null_pad = struct.pack("<H", 0x1120) * (pad_len // 2)
        full = enc + null_pad + nl_sfx + end_c + null_gap_orig
        if len(full) != d["slot_size"]:
            skip += 1
            continue
        data[d["offset"] : d["offset"] + d["slot_size"]] = full
        ok += 1

    # ── 2. Entrées dans des blocs gzip embeddés ───────────────────────────────
    for src, entries in by_gz.items():
        # Parser l'offset du bloc gzip dans le BNP : "gz@0x1A3F" → 0x1A3F
        try:
            gz_off = int(src.split("@")[1], 16)
        except (IndexError, ValueError):
            if log_fn:
                log_fn(f"  _source invalide : {src}", "err")
            skip += len(entries)
            continue

        # Trouver la fin du bloc gzip (gzip.decompress lit jusqu'à la fin naturelle)
        try:
            dec = bytearray(gzip.decompress(data[gz_off:]))
        except Exception as e:
            if log_fn:
                log_fn(f"  Erreur décompression {src} : {e}", "err")
            skip += len(entries)
            continue

        # Patcher chaque entrée dans le binaire décompressé
        patched_in_gz = 0
        for d in entries:
            n_fr_input = d.get("nom_fr", "").strip()
            t_fr_input = d.get("texte_fr", "").strip()
            choix_fr = d.get("choix_fr")
            q_fr = d.get("question_fr", "").strip()
            if choix_fr is not None:
                filled = [c for c in choix_fr if c.strip()]
                if q_fr and filled:
                    t_fr = _rebuild_choice_body(q_fr, choix_fr)
                elif not t_fr_input:
                    kept += 1
                    continue
                else:
                    t_fr = t_fr_input
            elif not n_fr_input and not t_fr_input:
                kept += 1
                continue
            else:
                t_fr = t_fr_input or d.get("texte_orig", "").strip()

            n_fr = n_fr_input or d.get("nom_orig", "").strip()
            t_fr = _align_menu_text(
                d.get("nom_orig", ""), d.get("texte_orig", ""), n_fr, t_fr
            )
            enc = text_to_bytes('"' + n_fr + "\n" + t_fr)
            term = d.get("_term", [E1, E2, E3, E4])
            avail = d["data_size"] - (len(term) * 2)
            nl_sfx = (
                struct.pack("<H", NL)
                if _needs_nl_suffix(
                    d.get("_term", [E1, E2, E3, E4]), d.get("texte_orig", "")
                )
                else b""
            )
            if len(enc) + len(nl_sfx) > avail:
                if log_fn:
                    log_fn(f"  [id {d['id']}] trop long, troncature automatique", "warn")
                
                import re
                tokens = re.split(r'(\[[a-zA-Z0-9+\-_]+\]|\s)', t_fr)
                tokens = [t for t in tokens if t]
                
                while tokens and len(text_to_bytes('"' + n_fr + "\n" + ''.join(tokens))) > avail - len(nl_sfx):
                    tokens.pop()
                    
                t_fr = ''.join(tokens)
                enc = text_to_bytes('"' + n_fr + "\n" + t_fr)
                
            pad_len = avail - len(enc) - len(nl_sfx)
            if pad_len < 0:
                pad_len = 0
            term = d.get("_term", [E1, E2, E3, E4])
            end_c = b"".join(struct.pack("<H", t) for t in term)
            null_gap_orig = dec[
                d["offset"] + d["data_size"] : d["offset"] + d["slot_size"]
            ]
            null_pad = struct.pack("<H", 0x1120) * (pad_len // 2)
            full = enc + null_pad + nl_sfx + end_c + null_gap_orig
            if len(full) != d["slot_size"]:
                skip += 1
                continue
            dec[d["offset"] : d["offset"] + d["slot_size"]] = full
            patched_in_gz += 1
            ok += 1

        if patched_in_gz == 0:
            continue  # rien à réécrire dans ce bloc

        # Recompresser et calculer la taille du bloc original dans le BNP
        gz_buf = io.BytesIO()
        with gzip.GzipFile(filename=b"", mode="wb", fileobj=gz_buf, mtime=0) as gz:
            gz.write(bytes(dec))
        new_gz = gz_buf.getvalue()

        # Trouver la taille du bloc gzip original (lire jusqu'au prochain magic ou fin)
        orig_end = gz_off + 10  # gzip header minimum
        # Avancer jusqu'à trouver la fin du stream gzip original
        try:
            import io as _io

            tmp = _io.BytesIO(data[gz_off:])
            with gzip.GzipFile(fileobj=tmp) as _gz:
                _gz.read()
            orig_gz_size = tmp.tell()
        except Exception:
            orig_gz_size = len(new_gz)  # fallback

        if len(new_gz) > orig_gz_size:
            if log_fn:
                log_fn(
                    f"  ⚠ {src} : bloc gzip FR trop grand ({len(new_gz)} > {orig_gz_size}), ignoré",
                    "warn",
                )
            ok -= patched_in_gz
            skip += patched_in_gz
            continue

        # Z_SYNC_FLUSH Split Padding pour atteindre orig_gz_size exactement.
        def _pad_gz(dec_data, target_size):
            base_comp = zlib.compressobj(level=9, wbits=-15)
            base_stream = base_comp.compress(dec_data) + base_comp.flush()
            header = b"\x1f\x8b\x08\x00\x00\x00\x00\x00\x02\xff"
            crc = struct.pack("<I", zlib.crc32(dec_data) & 0xFFFFFFFF)
            isize = struct.pack("<I", len(dec_data) & 0xFFFFFFFF)
            base_sz = len(header) + len(base_stream) + len(crc) + len(isize)
            if base_sz == target_size:
                return header + base_stream + crc + isize
            if base_sz > target_size:
                return None

            split_points = [len(dec_data) * i // 5 for i in range(1, 5)]
            for mask in range(1 << 4):
                comp = zlib.compressobj(level=9, wbits=-15)
                stream = b""
                last = 0
                for i in range(4):
                    if mask & (1 << i):
                        stream += comp.compress(
                            dec_data[last : split_points[i]]
                        ) + comp.flush(zlib.Z_SYNC_FLUSH)
                        last = split_points[i]
                stream += comp.compress(dec_data[last:]) + comp.flush(zlib.Z_SYNC_FLUSH)
                cur = len(header) + len(stream) + len(crc) + len(isize)
                diff = target_size - cur
                if diff >= 5 and diff % 5 == 0:
                    pad_stream = (
                        b"\x00\x00\x00\xff\xff" * ((diff // 5) - 1)
                        + b"\x01\x00\x00\xff\xff"
                    )
                    return header + stream + pad_stream + crc + isize

            # Fallback to random splits if mod 5 didn't hit
            import random

            for _ in range(500):
                comp = zlib.compressobj(level=9, wbits=-15)
                splits = sorted(
                    random.sample(range(1, len(dec_data)), random.randint(1, 5))
                )
                stream = b""
                last = 0
                for sp in splits:
                    stream += comp.compress(dec_data[last:sp]) + comp.flush(
                        zlib.Z_SYNC_FLUSH
                    )
                    last = sp
                stream += comp.compress(dec_data[last:]) + comp.flush(zlib.Z_SYNC_FLUSH)
                cur = len(header) + len(stream) + len(crc) + len(isize)
                diff = target_size - cur
                if diff >= 5 and diff % 5 == 0:
                    pad_stream = (
                        b"\x00\x00\x00\xff\xff" * ((diff // 5) - 1)
                        + b"\x01\x00\x00\xff\xff"
                    )
                    return header + stream + pad_stream + crc + isize

            return None

        res_gz = _pad_gz(dec, orig_gz_size)
        if res_gz is None:
            if log_fn:
                log_fn(
                    f"  [!] {src} : Impossible d'atteindre exactement la taille gzip ({orig_gz_size})",
                    "warn",
                )
            ok -= patched_in_gz
            skip += patched_in_gz
            continue
        data[gz_off : gz_off + orig_gz_size] = res_gz

    if out_path is None:
        out_path = bin_path
    from pathlib import Path

    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(data)
    if log_fn:
        log_fn(
            f"  {ok} traduits | {skip} ignores | {kept} conserves -> {Path(out_path).name}",
            "ok",
        )
    return out_path

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
from src.core.text import (
    decode_text,
    text_to_bytes,
    detect,
    _valid_name,
    _needs_nl_suffix,
    _align_menu_text,
)


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


def find_dialogs(data: bytes) -> list:
    """Scanne un buffer binaire et extrait tous les dialogues valides."""
    dialogs = []
    i = 0
    while i < len(data) - 1:
        w = struct.unpack_from("<H", data, i)[0]
        if w != 0x0022 or not _valid_name(data, i):
            i += 2
            continue
        start = i
        chars = []
        j = i
        found = False
        term = None
        while j < len(data) - 1:
            c = struct.unpack_from("<H", data, j)[0]
            chars.append(c)
            if len(chars) > 2000:
                break
            t4 = chars[-4:]
            t3 = chars[-3:]
            if t4 in ([E1, E2, E3, E4], [CHAIN_E1, E2, E3, E4]):
                end = j + 2
                term = t4
                found = True
                break
            if t3 in ([E1, E2, E4], [CHAIN_E1, E2, E4]):
                end = j + 2
                term = t3
                found = True
                break
            j += 2
        if not found:
            i += 2
            continue
        k = end
        while k + 1 < len(data) and struct.unpack_from("<H", data, k)[0] == 0:
            k += 2
        raw_b = data[start:end]
        ac = tc = 0
        pnl = False
        for bi in range(0, len(raw_b) - 1, 2):
            bv = struct.unpack_from("<H", raw_b, bi)[0]
            if bv == NL:
                pnl = True
                continue
            if not pnl:
                continue
            if bv in {E1, E2, E3, E4, SP, CHAIN_E1}:
                continue
            tc += 1
            if 0x20 <= bv <= 0x7E:
                ac += 1
        if tc > 5 and (ac / tc) < 0.25:
            i += 2
            continue
        txt = decode_text(raw_b)
        lns = txt.split("\n")
        nom = lns[0].lstrip('"') if lns else ""
        body = "\n".join(lns[1:])
        for seq in (
            "[E1][E2][E3][E4]",
            "[1109][E2][E3][E4]",
            "[E1][E2][E4]",
            "[1109][E2][E4]",
        ):
            body = body.replace(seq, "")
        body_clean = body.strip()
        question, choices = _parse_choices(body_clean)
        entry = {
            "id": len(dialogs),
            "offset": start,
            "data_size": end - start,
            "slot_size": k - start,
            "_term": term,
            "nom_orig": nom,
            "texte_orig": body_clean,
            "nom_fr": "",
            "texte_fr": "",
        }
        if choices is not None:
            entry["question_orig"] = question
            entry["choix_orig"] = choices
            entry["question_fr"] = ""
            entry["choix_fr"] = [""] * len(choices)
        dialogs.append(entry)
        i = k
    return dialogs


def _parse_choices(body: str) -> tuple:
    """
    Si body contient un menu de choix (marqueur [1208] ou [U+1208]),
    retourne (question, [option1, option2, ...]) avec les balises de contrôle préservées.
    Sinon retourne (body, None).

    Format binaire Atlus PSP pour les menus :
      Question\n[1208][0002][1432][NULL][NULL][0014]Option1[1432][NULL][NULL][0014]\n[1432][NULL][NULL][0014]Option2...
    Le [0014] sépare les options, [1208][0002] ouvre le menu.
    """
    marker = None
    for m in ("[1208]", "[U+1208]"):
        if m in body:
            marker = m
            break
    if marker is None:
        return body, None

    # Séparer la question du bloc de choix
    parts = body.split(marker, 1)
    question = parts[0].rstrip("\n").strip()
    choice_block = marker + parts[1]

    # Extraire les options : elles sont délimitées par [0014]
    # Structure : [1208][0002][1432][NULL][NULL][0014]OPT1[1432][NULL][NULL][0014]\n[1432][NULL][NULL][0014]OPT2...
    # On split sur [0014] et on garde les parties non-vides qui ne sont que des balises ctrl
    raw_opts = re.split(r"\[0014\]", choice_block)
    options = []
    for o in raw_opts:
        # Retirer les balises de structure [1208][0002][1432][NULL][NULL] etc.
        # Nettoyer tous les codes de contrôle y compris [U+00XX] (ex: [U+0002], [U+0003])
        cleaned = (
            re.sub(
                r"\[1208\]|\[U\+1208\]|\[U\+[0-9A-Fa-f]{4}\]|\[0002\]|\[1432\]|\[NULL\]",
                "",
                o,
            )
            .strip("\n")
            .strip()
        )
        # Un segment valide = texte non vide sans \n interne (le \n sépare les options)
        if cleaned and "\n" not in cleaned:
            options.append(cleaned)

    if not options:
        return body, None
    return question, options


def _rebuild_choice_body(question: str, options: list) -> str:
    """
    Reconstruit le texte complet du menu de choix à partir de la question
    et de la liste d'options, avec les balises de contrôle Atlus PSP.
    """
    sep = "[1432][NULL][NULL][0014]"
    header = "\n[1208][0002]"
    opt_str = sep
    opt_str += (sep + "\n" + sep).join(options)
    opt_str += sep
    return question + header + opt_str


def check_menu_consistency(json_path: str, log_fn=None) -> list:
    """
    Vérifie qu'un fichier JSON de script est cohérent pour les menus de choix.

    Le moteur Atlus PSP affiche toujours deux slots consécutifs pour un menu :
      slot N   = texte d'intro qui SE TERMINE par la question
      slot N+1 = même question répétée + menu [1208][0002]...[0014]...

    Si la fin de l'intro (texte_fr de N) ne correspond pas à la question
    du menu (texte_fr de N+1), le joueur voit deux formulations différentes.

    Retourne la liste des problèmes trouvés :
      [{"intro_id": int, "menu_id": int, "q_menu": str, "intro_end": str}, ...]
    """
    try:
        data = json.load(open(json_path, encoding="utf-8"))
    except Exception as e:
        if log_fn:
            log_fn(f"  Impossible de lire {json_path} : {e}", "err")
        return []

    by_id = {e["id"]: e for e in data}
    problems = []

    # Identifier les slots avec menu de choix
    menu_slots = [
        e
        for e in data
        if "[1208]" in e.get("texte_orig", "") or "[0002]" in e.get("texte_orig", "")
    ]

    for menu_entry in menu_slots:
        intro_entry = by_id.get(menu_entry["id"] - 1)
        if not intro_entry:
            continue

        # Ne vérifier que si les deux ont une traduction
        q_fr_raw = menu_entry.get("texte_fr", "")
        i_fr_raw = intro_entry.get("texte_fr", "")
        if not q_fr_raw or not i_fr_raw:
            continue

        # Extraire la question du menu = tout avant [1208] / [0002]
        q_fr = (
            q_fr_raw.split("[U+1208]")[0].split("[1208]")[0].split("[0002]")[0].strip()
        )

        # Normaliser pour comparaison souple (ignorer espaces/ponctuation finale)
        def norm(s):
            return s.strip().rstrip("?! ").replace(" ", "").replace("\n", "").lower()

        q_norm = norm(q_fr)
        i_norm = norm(i_fr_raw)

        # La fin de l'intro doit correspondre à la question (sur les 20 derniers chars)
        tail = max(15, len(q_norm) - 3)
        if not i_norm.endswith(q_norm[-tail:]):
            problems.append(
                {
                    "intro_id": intro_entry["id"],
                    "menu_id": menu_entry["id"],
                    "q_menu": q_fr,
                    "intro_end": i_fr_raw,
                }
            )
            if log_fn:
                log_fn(
                    f"  ⚠ Incohérence menu : id={intro_entry['id']} (intro) "
                    f"ne se termine pas par la question de id={menu_entry['id']}",
                    "warn",
                )

    return problems


def validate_all_scripts(scripts_json_dir: str, log_fn=None, progress_fn=None) -> dict:
    """
    Parcourt tous les script_XXX.json traduits et vérifie la cohérence
    des menus de choix dans chaque fichier.

    Retourne {"total_files": int, "files_with_issues": int, "problems": list}
    """
    jdir = Path(scripts_json_dir)
    files = sorted(jdir.glob("script_*.json"))
    if not files:
        if log_fn:
            log_fn("  Aucun fichier JSON trouvé.", "warn")
        return {"total_files": 0, "files_with_issues": 0, "problems": []}

    all_problems = []
    files_with_issues = 0

    for i, jf in enumerate(files):
        if progress_fn:
            progress_fn((i + 1) / len(files))
        probs = check_menu_consistency(str(jf), log_fn=None)
        if probs:
            files_with_issues += 1
            for p in probs:
                p["file"] = jf.name
            all_problems.extend(probs)
            if log_fn:
                log_fn(f"  {jf.name} : {len(probs)} incohérence(s) détectée(s)", "warn")

    if log_fn:
        if all_problems:
            log_fn(
                f"  {files_with_issues}/{len(files)} fichiers avec incohérences "
                f"({len(all_problems)} total)",
                "warn",
            )
        else:
            log_fn(f"  Tous les menus sont cohérents ({len(files)} fichiers).", "ok")

    return {
        "total_files": len(files),
        "files_with_issues": files_with_issues,
        "problems": all_problems,
    }


def scan_bnp_bin(data: bytes, stem: str, out_dir: Path, log_fn) -> int:
    from src.parsers.fbe_parser import scan_fbe_bnp

    """Extrait les dialogues d'un BNP/BIN (route vers le décodeur spécial si F_BE/TM_EVE)."""
    if stem.lower() in ("f_be", "tm_eve"):
        return scan_fbe_bnp(data, stem, out_dir, log_fn)
    all_dlgs = find_dialogs(data)
    pos = gz_n = 0
    while gz_n < 200:
        idx = data.find(b"\x1f\x8b", pos)
        if idx == -1:
            break
        try:
            dec = gzip.decompress(data[idx:])
            if len(dec) > 64:
                for d in find_dialogs(dec):
                    d["_source"] = f"gz@0x{idx:X}"
                    all_dlgs.append(d)
                gz_n += 1
        except:
            pass
        pos = idx + 2
    if detect(data) == "CRILAYLA":
        dec = crilayla_decompress(data)
        if dec:
            for d in find_dialogs(dec):
                d["_source"] = "crilayla"
                all_dlgs.append(d)
    seen = set()
    unique = []
    for d in all_dlgs:
        k = (d["offset"], d["data_size"])
        if k not in seen:
            seen.add(k)
            unique.append(d)
    for k, d in enumerate(unique):
        d["id"] = k
    if not unique:
        return 0
    out_path = out_dir / f"{stem.upper()}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(unique, f, ensure_ascii=False, indent=2)
    if log_fn:
        log_fn(f"  {stem.upper()}: {len(unique)} dialogues → {out_path.name}", "ok")
    return len(unique)


def _decode_single_script(idx, scripts_dir, output_dir):
    bf = scripts_dir / f"script_{idx:03d}.bin"
    if not bf.exists():
        bf = scripts_dir / f"script_{idx}.bin"
    if not bf.exists():
        return None

    raw = open(bf, "rb").read()
    if raw[:2] == b"\x1f\x8b":
        try:
            raw = gzip.decompress(raw)
        except:
            pass

    dlgs = find_dialogs(raw)
    out_json = output_dir / f"script_{idx:03d}.json"

    # Si un JSON traduit existe déjà, préserver les traductions
    if out_json.exists():
        try:
            existing = json.load(open(out_json, encoding="utf-8"))
            by_offset = {e["offset"]: e for e in existing}
            for d in dlgs:
                prev = by_offset.get(d["offset"])
                if prev:
                    d["nom_fr"] = prev.get("nom_fr", "")
                    d["texte_fr"] = prev.get("texte_fr", "")
                    if "choix_orig" in d:
                        d["question_fr"] = prev.get("question_fr", "")
                        # Récupérer choix_fr depuis prev si disponible, sinon depuis texte_fr
                        prev_choix = prev.get("choix_fr")
                        if prev_choix and len(prev_choix) == len(d["choix_orig"]):
                            d["choix_fr"] = prev_choix
        except Exception:
            pass

    migrate_choices_in_json(dlgs)
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(dlgs, f, ensure_ascii=False, indent=2)

    return len(dlgs)


def decode_all_scripts(
    scripts_dir: Path, output_dir: Path, log_fn=None, progress_fn=None
):
    """Décode tous les scripts_bin/*.bin en fichiers JSON prêts à traduire."""
    output_dir.mkdir(parents=True, exist_ok=True)
    total = vides = 0
    total_scripts = 399
    completed = 0

    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [
            executor.submit(_decode_single_script, idx, scripts_dir, output_dir)
            for idx in range(total_scripts)
        ]

        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            completed += 1
            if progress_fn:
                progress_fn(completed / total_scripts)
            if res is not None:
                total += 1
                if res == 0:
                    vides += 1

    if log_fn:
        log_fn(f"  {total} scripts décodés ({vides} vides) via ProcessPool", "ok")


# ── Validation cohérence menus de choix ───────────────────────────────────────


def migrate_choices_in_json(entries: list) -> list:
    """
    Migration : pour les entrées déjà traduites (texte_fr rempli) qui contiennent
    un menu de choix, peuple question_fr/choix_fr à partir du texte_fr existant.
    Les entrées sans texte_fr gardent question_fr="" et choix_fr=["","..."].
    """
    for e in entries:
        if "choix_orig" not in e:
            continue  # pas un menu de choix
        # Si question_fr/choix_fr déjà remplis, ne pas écraser
        if e.get("question_fr") or any(c.strip() for c in e.get("choix_fr", [])):
            continue
        t_fr = e.get("texte_fr", "").strip()
        if not t_fr:
            continue
        q_fr, opts_fr = _parse_choices(t_fr)
        if opts_fr is not None and len(opts_fr) == len(e["choix_orig"]):
            e["question_fr"] = q_fr
            e["choix_fr"] = opts_fr
        elif opts_fr is not None:
            # Nombre d'options différent — on met quand même ce qu'on a
            e["question_fr"] = q_fr
            e["choix_fr"] = opts_fr + [""] * max(0, len(e["choix_orig"]) - len(opts_fr))
    return entries

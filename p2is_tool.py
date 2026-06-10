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

import struct, json, gzip, io, os, re, shutil, threading, subprocess, platform
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk

# ── Thème ─────────────────────────────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
C_DARK   = "#1a1a2e"
C_PANEL  = "#16213e"
C_CARD   = "#0f3460"
C_ACCENT = "#3a7ebf"
C_OK     = "#2ecc71"
C_ERR    = "#e74c3c"
C_WARN   = "#f39c12"
C_MUTED  = "#8892a4"
C_WHITE  = "#ffffff"

# ── Traductions FR / EN ───────────────────────────────────────────────────────
STRINGS = {
"fr": {
    "app_sub":      "Outil de traduction  ·  Persona 2 IS PSP  ·  EUR ULES01557",
    "work_lbl":     "Dossier de travail :",
    "lang_btn":     "🌐 EN",
    "tab_extract":  "① Extraction",
    "tab_scan":     "② Traduction",
    "tab_encode":   "③ Encodage",
    "tab_rebuild":  "④ Rebuild ISO",
    # Onglet Extraction
    "a_title":"A — Extraire le CPK",
    "a_iso":"Fichier ISO :",
    "a_note":"Sortie : <travail>/P2PT_ALL.cpk",
    "a_tip":"💡 Sélectionne ton fichier .iso original (ULES01557).",
    "a_btn":"⬇  Extraire P2PT_ALL.cpk",
    "b_title":"B — Extraire les fichiers du jeu",
    "b_exe":"CriFsLib.GUI.exe :",
    "b_dl_btn":"⬇  Télécharger CriFsLib",
    "b_instr":"  1. Télécharge CriFsLib si besoin (bouton ci-dessus)\n  2. Clique « Ouvrir CriFsLib »\n  3. Glisse P2PT_ALL.cpk dans la fenêtre\n  4. Clic droit → Extract All\n  5. Extrais vers : <travail>/cpk_files/",
    "b_tip":"💡 CriFsLib est requis pour cette étape.",
    "b_btn":"🔧  Ouvrir CriFsLib",
    "c_title":"C — Extraire les scripts du jeu",
    "c_cpk":"P2PT_ALL.cpk :",
    "c_note":"Sortie : <travail>/event.bin",
    "c_tip":"💡 event.bin contient tous les scripts de dialogue du jeu.",
    "c_btn":"⬇  Extraire event.bin",
    "d_title":"D — Séparer les scripts",
    "d_event":"event.bin :",
    "d_note":"Sortie : <travail>/scripts_bin/  (399 fichiers)",
    "d_tip":"💡 Chaque script = une scène ou un lieu du jeu.",
    "d_btn":"⬇  Extraire les 399 scripts",
    # Onglet Scan
    "e_title":"E — Générer les fichiers à traduire",
    "e_src":"Dossier scripts_bin/ :",
    "e_out":"Sortie JSON :",
    "e_tip":"💡 Remplis nom_fr et texte_fr dans les JSON pour traduire.",
    "e_btn":"📝  Décoder tous les scripts en JSON",
    "v_title":"G — Vérifier la cohérence des menus",
    "v_src":"Dossier event_scripts/ :",
    "v_tip":"💡 Vérifie que les dialogues d\'intro s\'alignent bien avec leurs menus de choix.",
    "v_btn":"🔍  Vérifier les menus de choix",
    "v_ok":"Tous les menus sont cohérents !",
    "v_warn":"{n} incohérence(s) dans {f} fichier(s) — voir le journal.",
    "f_title":"F — Extraire les dialogues annexes",
    "f_src":"cpk_files/ :",
    "f_out":"Sortie JSON :",
    "f_f1":"Dialogues boutique CDs",
    "f_f2":"F_BE — dialogues de combat (Personas, ennemis, répliques en bataille)",
    "f_f3":"TM_EVE — dialogues de scènes narratives (hors combat)",
    "f_f4":"Dialogues NPC par zone",
    "f_tip":"💡 Ces fichiers contiennent PNJ, boutiques et cinématiques.",
    "f_btn":"🔍  Scanner CD_SHOP + F_BE + TM_EVE + MMAP01-06",
    # Onglet Encodage
    "enc_info":"Comment ça marche :\n  • Les JSON avec nom_fr / texte_fr remplis sont encodés en binaire.\n  • Les accents français sont convertis en glyphes japonais (ACCENT_MAP).\n  • Le terminateur _term de chaque dialogue est préservé.\n  • Les scripts event.bin sont recompressés en gzip avant injection.",
    "enc_title":"Encoder la traduction",
    "enc_trad":"Dossier traduction/ :",
    "enc_cpk":"cpk_files/ (fichiers originaux) :",
    "enc_out":"Sortie encoded/ :",
    "enc_tip":"💡 Seuls les dialogues traduits sont modifiés. Les autres restent en anglais.",
    "enc_btn":"🔄  Encoder tous les JSON traduits",
    # Onglet Rebuild
    "rb_info":"Cette étape patche event.bin traduit dans une copie de l'ISO.\nL'offset est mémorisé automatiquement à l'étape C.\n\nPrérequis : avoir complété les onglets ① ② ③.",
    "rb_title":"Créer l'ISO traduite",
    "rb_iso":"ISO originale :",
    "rb_enc":"Dossier encoded/ :",
    "rb_out":"ISO de sortie :",
    "rb_tip":"💡 L'ISO originale n'est jamais modifiée — une copie est créée.",
    "rb_btn":"🏗️  Créer l'ISO traduite",
    # Log
    "log_title":"Journal",
    "log_clear":"Effacer",
    # Statuts
    "running":"En cours…",
    "done_s":"OK",
    # Alertes
    "w_title":"Attention",
    "e_title":"Erreur",
    "ok_title":"Terminé",
    "w_no_iso":"Sélectionne un fichier ISO valide d'abord.",
    "w_no_cpk":"Sélectionne le fichier P2PT_ALL.cpk.",
    "w_no_event":"Sélectionne le fichier event.bin.",
    "w_no_scripts":"Sélectionne le dossier scripts_bin/.",
    "w_no_cpkfiles":"Le dossier cpk_files/ est introuvable.\nComplète l'étape B (CriFsLib) avant.",
    "w_no_crifsl":"CriFsLib.GUI.exe introuvable :\n{p}\nVérifie le chemin ci-dessus.",
    "w_fill_all":"Remplis tous les champs avant de continuer.",
    "w_no_iso2":"ISO originale introuvable :\n{p}",
    "w_no_encoded":"Dossier encoded/ introuvable :\n{p}\nComplète l'onglet ③ d'abord.",
    "w_no_eventbin":"event.bin absent de encoded/.\nComplète l'encodage (onglet ③) d'abord.",
    # Messages de fin
    "ok_cpk":"CPK extrait ({s} MB) :\n{p}\n\n→ Étape suivante : ouvrir CriFsLib (B).",
    "ok_crifsl":"CriFsLib est ouvert.\n→ Glisse P2PT_ALL.cpk, extrais vers cpk_files/.",
    "ok_event":"event.bin extrait :\n{p}\n\n→ Étape suivante : extraire les scripts (D).",
    "ok_scripts":"{n} scripts extraits dans :\n{p}\n\n→ Passe à l'onglet ②.",
    "ok_decode":"Scripts décodés dans :\n{p}\n\n→ Traduis les JSON, puis onglet ③.",
    "ok_scan":"✓ {n} dialogues extraits.\nJSON dans : {p}\n\n→ Traduis, puis onglet ③.",
    "ok_encode":"✓ {n} fichier(s) encodé(s) : {f}\n{e}Sortie : {p}\n\n→ Passe à l'onglet ④.",
    "ok_rebuild":"✓ ISO traduite créée ({s} MB) :\n{p}\n\nLance-la dans PPSSPP !",
    "log_crifsl1":"CriFsLib ouvert.",
    "log_crifsl2":"  → Glisse P2PT_ALL.cpk dans la fenêtre",
    "log_crifsl3":"  → Extraire vers : {p}",
},
"en": {
    "app_sub":      "Fan translation tool  ·  Persona 2 IS PSP  ·  EUR ULES01557",
    "work_lbl":     "Working folder:",
    "lang_btn":     "🌐 FR",
    "tab_extract":  "① Extract",
    "tab_scan":     "② Translation",
    "tab_encode":   "③ Encode",
    "tab_rebuild":  "④ Rebuild ISO",
    "a_title":"A — Extract the CPK",
    "a_iso":"ISO file:",
    "a_note":"Output: <workdir>/P2PT_ALL.cpk",
    "a_tip":"💡 Select your original .iso file (ULES01557).",
    "a_btn":"⬇  Extract P2PT_ALL.cpk",
    "b_title":"B — Extract game files",
    "b_exe":"CriFsLib.GUI.exe:",
    "b_dl_btn":"⬇  Download CriFsLib",
    "b_instr":"  1. Download CriFsLib if needed (button above)\n  2. Click 'Open CriFsLib'\n  3. Drag P2PT_ALL.cpk into the window\n  4. Right-click → Extract All\n  5. Extract to: <workdir>/cpk_files/",
    "b_tip":"💡 CriFsLib is required for this step.",
    "b_btn":"🔧  Open CriFsLib",
    "c_title":"C — Extract game scripts",
    "c_cpk":"P2PT_ALL.cpk:",
    "c_note":"Output: <workdir>/event.bin",
    "c_tip":"💡 event.bin holds all the game's dialogue scripts.",
    "c_btn":"⬇  Extract event.bin",
    "d_title":"D — Split scripts",
    "d_event":"event.bin:",
    "d_note":"Output: <workdir>/scripts_bin/  (399 files)",
    "d_tip":"💡 Each script = one scene or location in the game.",
    "d_btn":"⬇  Extract all 399 scripts",
    "e_title":"E — Generate translation files",
    "e_src":"scripts_bin/ folder:",
    "e_out":"JSON output:",
    "e_tip":"💡 Fill in nom_fr and texte_fr in the JSON files to translate.",
    "e_btn":"📝  Decode all scripts to JSON",
    "v_title":"G — Check menu consistency",
    "v_src":"event_scripts/ folder:",
    "v_tip":"💡 Checks that intro dialogues align with their choice menus.",
    "v_btn":"🔍  Check choice menus",
    "v_ok":"All menus are consistent!",
    "v_warn":"{n} issue(s) in {f} file(s) — see the log.",
    "f_title":"F — Extract side dialogues",
    "f_src":"cpk_files/ folder:",
    "f_out":"JSON output:",
    "f_f1":"CD Shop dialogues",
    "f_f2":"F_BE — battle dialogues (Personas, enemies, character lines)",
    "f_f3":"TM_EVE — narrative scene dialogues (outside combat)",
    "f_f4":"NPC dialogues per game zone",
    "f_tip":"💡 These files contain NPC text, shop text and cutscene subtitles.",
    "f_btn":"🔍  Scan CD_SHOP + F_BE + TM_EVE + MMAP01-06",
    "enc_info":"How it works:\n  • JSON entries with nom_fr / texte_fr filled in are encoded to binary.\n  • French accents are mapped to Japanese glyphs (ACCENT_MAP).\n  • Each dialogue's _term terminator is preserved as-is.\n  • event.bin scripts are gzip-recompressed before injection.",
    "enc_title":"Encode the translation",
    "enc_trad":"translation/ folder:",
    "enc_cpk":"cpk_files/ (original files):",
    "enc_out":"encoded/ output:",
    "enc_tip":"💡 Only translated entries are modified. Everything else stays in English.",
    "enc_btn":"🔄  Encode all translated JSON files",
    "rb_info":"This step patches the translated event.bin into a copy of the ISO.\nThe offset is saved automatically at step C.\n\nPrerequisites: complete tabs ① ② ③ first.",
    "rb_title":"Build the translated ISO",
    "rb_iso":"Original ISO:",
    "rb_enc":"encoded/ folder:",
    "rb_out":"Output ISO:",
    "rb_tip":"💡 The original ISO is never modified — a copy is created.",
    "rb_btn":"🏗️  Build translated ISO",
    "log_title":"Log",
    "log_clear":"Clear",
    "running":"Running…",
    "done_s":"Done",
    "w_title":"Warning",
    "e_title":"Error",
    "ok_title":"Done",
    "w_no_iso":"Please select a valid ISO file first.",
    "w_no_cpk":"Please select the P2PT_ALL.cpk file.",
    "w_no_event":"Please select the event.bin file.",
    "w_no_scripts":"Please select the scripts_bin/ folder.",
    "w_no_cpkfiles":"The cpk_files/ folder was not found.\nComplete step B (CriFsLib) first.",
    "w_no_crifsl":"CriFsLib.GUI.exe not found:\n{p}\nCheck the path above.",
    "w_fill_all":"Please fill in all fields before continuing.",
    "w_no_iso2":"Original ISO not found:\n{p}",
    "w_no_encoded":"encoded/ folder not found:\n{p}\nComplete tab ③ first.",
    "w_no_eventbin":"event.bin missing from encoded/.\nComplete encoding (tab ③) first.",
    "ok_cpk":"CPK extracted ({s} MB):\n{p}\n\n→ Next: open CriFsLib (B).",
    "ok_crifsl":"CriFsLib is open.\n→ Drag P2PT_ALL.cpk in, extract to cpk_files/.",
    "ok_event":"event.bin extracted:\n{p}\n\n→ Next: extract scripts (D).",
    "ok_scripts":"{n} scripts extracted to:\n{p}\n\n→ Move to tab ②.",
    "ok_decode":"Scripts decoded to:\n{p}\n\n→ Translate the JSON files, then go to tab ③.",
    "ok_scan":"✓ {n} dialogues extracted.\nJSON in: {p}\n\n→ Translate, then go to tab ③.",
    "ok_encode":"✓ {n} file(s) encoded: {f}\n{e}Output: {p}\n\n→ Move to tab ④.",
    "ok_rebuild":"✓ Translated ISO created ({s} MB):\n{p}\n\nLaunch it in PPSSPP!",
    "log_crifsl1":"CriFsLib opened.",
    "log_crifsl2":"  → Drag P2PT_ALL.cpk into the window",
    "log_crifsl3":"  → Extract to: {p}",
},
}

_lang = "fr"

def T(key, **kw):
    """Retourne la chaîne traduite pour la langue active."""
    s = STRINGS[_lang].get(key, STRINGS["fr"].get(key, key))
    return s.format(**kw) if kw else s

# ── Dossier de travail multiplateforme ────────────────────────────────────────
def _default_work() -> Path:
    s = platform.system()
    if s == "Windows":
        return Path(os.environ.get("USERPROFILE", Path.home())) / "Desktop" / "P2IS_FR"
    elif s == "Darwin":
        return Path.home() / "Documents" / "P2IS_FR"
    return Path.home() / "P2IS_FR"

def _default_crifsl() -> str:
    if platform.system() == "Windows":
        return str(Path(os.environ.get("USERPROFILE", Path.home())) / "Desktop" / "CriFsLib" / "CriFsLib.GUI.exe")
    return ""

DEFAULT_WORK   = _default_work()
DEFAULT_CRIFSL = _default_crifsl()

# Créer les dossiers de base au démarrage
for _d in [DEFAULT_WORK, DEFAULT_WORK / "cpk_files"]:
    _d.mkdir(parents=True, exist_ok=True)

OFFSETS_FILE = ""

def _offsets_path():
    return OFFSETS_FILE or ""

def save_offsets(data: dict):
    """Persiste les offsets ISO/CPK/event.bin entre les sessions."""
    p = _offsets_path()
    if p:
        Path(p).parent.mkdir(parents=True, exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

def load_offsets() -> dict:
    """Charge les offsets sauvegardés, ou retourne des valeurs par défaut."""
    p = _offsets_path()
    if p and Path(p).exists():
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"iso_path": "", "cpk_offset_in_iso": -1}


# ── Constantes Atlus PSP ──────────────────────────────────────────────────────
SP = 0x1120   # espace
NL = 0x1101   # saut de ligne
E1 = 0x1106   # terminateur partiel 1
E2 = 0x1102   # terminateur partiel 2
E3 = 0x1103   # terminateur partiel 3
E4 = 0x1431   # terminateur partiel 4 / marqueur animation F_BE
CHAIN_E1 = 0x1109  # variante E1

CTRL = {
    SP:"[SP]", NL:"\n", E1:"[E1]", E2:"[E2]", E3:"[E3]", E4:"[E4]",
    CHAIN_E1:"[1109]",
    0x1205:"[1205]",0x001E:"[001E]",0x1432:"[1432]",0x0014:"[0014]",
    0x0002:"[0002]",0x0010:"[0010]",0x0000:"[NULL]",
    0x1107:"[1107]",0x1108:"[1108]",0x120C:"[120C]",0x120D:"[120D]",
    0x120E:"[120E]",0x120F:"[120F]",0x1208:"[1208]",0x1210:"[1210]",
    0x1112:"[1112]",0x1113:"[1113]",0x121E:"[121E]",
}

# Correspondances accents FR → glyphes japonais disponibles dans la police du jeu
ACCENT_MAP = [
    ('é','Ğ'),('è','ò'),('ê','¿'),('ô','Æ'),('É','Ņ'),('È','Ũ'),
    ('Î','£'),('Ô','ō'),('Û','ĵ'),('œ','ë'),('Œ','Ǩ'),('ü','ˠ'),('ï','Ȗ'),
]

# Magic bytes de fichiers binaires non-dialogue
BINARY_MAGICS = (b'MIG.',b'VAGp',b'SGXD',b'RIFF',b'PMF\x00',b'PSMF',b'\x89PNG',b'BM\x00\x00')

# Fichiers à scanner dans cpk_files/
SCAN_TARGETS = {
    'cd_shop.bin',
    'f_be.bnp','tm_eve.bnp',
    'mmap01.bnp','mmap02.bnp','mmap03.bnp',
    'mmap04.bnp','mmap05.bnp','mmap06.bnp',
}

# ── Décodeur F_BE / TM_EVE ────────────────────────────────────────────────────
#
# Format animation Atlus PSP :
#   [E4](2 octets) + 5 octets de paramètres d'animation → sauter +7 au total
#   Timing marks inline (1 octet isolé, ex: 0x3B, 0x7F) → sauter +1
#   [1107] → fin de slot
#   Plusieurs prises de parole par slot → split sur '"'

def decode_fbe_slot(data: bytes, start: int, data_size: int) -> str:
    """Lit un slot F_BE/TM_EVE octet par octet, gère les escapes animation."""
    end = min(start + data_size, len(data))
    out = []; i = start
    while i < end:
        if i + 1 >= end: break
        b0, b1 = data[i], data[i+1]
        w = b0 | (b1 << 8)
        if w == 0x1431:   i += 7; continue          # [E4] + 5 bytes anim
        if w == 0x1107:   break                      # fin de slot
        if b1 in (0x11, 0x14):                       # code ctrl Atlus
            if w == SP:  out.append(' ')
            elif w == NL: out.append('\n')
            i += 2; continue
        if 0x20 <= b0 <= 0x7E and b1 == 0x00:        # ASCII UTF-16 LE
            out.append('"' if b0 == 0x22 else chr(b0))
            i += 2; continue
        if b0 != 0x00 and b1 != 0x00:               # timing mark 1 octet
            i += 1; continue
        i += 2
    return ''.join(out)

def parse_fbe_text(text: str) -> list:
    """Parse le texte brut d'un slot en [{nom, texte}], garde le plus long par perso."""
    order = []; best = {}
    for seg in re.split(r'"', text):
        seg = seg.strip()
        if not seg: continue
        nl = seg.find('\n')
        if nl == -1: continue
        nom = seg[:nl].strip()
        texte = seg[nl+1:].strip()
        if not nom or not re.match(r'^[A-Za-z0-9 #&\'\[\]\.\-]+$', nom): continue
        if nom not in best:
            best[nom] = texte; order.append(nom)
        elif len(texte) > len(best[nom]):
            best[nom] = texte
    return [{"nom": n, "texte": best[n]} for n in order if best[n]]

def scan_fbe_bnp(data: bytes, stem: str, out_dir: Path, log_fn) -> int:
    """Extrait les dialogues d'un F_BE.BNP ou TM_EVE.BNP avec le décodeur animation."""
    raw = find_dialogs(data)
    if not raw: return 0
    output = []; eid = 0
    for e in raw:
        off, sz = e["offset"], e["data_size"]
        dlgs = parse_fbe_text(decode_fbe_slot(data, off, sz))
        if not dlgs:
            output.append({**e, "id": eid, "nom_orig": e.get("nom_orig",""),
                           "texte_orig":"", "nom_fr":"", "texte_fr":""}); eid += 1; continue
        for d in dlgs:
            output.append({"id":eid,"offset":off,"data_size":sz,"slot_size":e["slot_size"],
                           "_term":e.get("_term",[E1,E2,E3,E4]),
                           "nom_orig":d["nom"],"texte_orig":d["texte"],"nom_fr":"","texte_fr":""})
            eid += 1
    out_path = out_dir / f"{stem.upper()}.json"
    with open(out_path,"w",encoding="utf-8") as f: json.dump(output,f,ensure_ascii=False,indent=2)
    if log_fn: log_fn(f"  {stem.upper()}: {len(output)} dialogues → {out_path.name}","ok")
    return len(output)


# ── Encodage / décodage texte Atlus ──────────────────────────────────────────

def decode_text(raw: bytes) -> str:
    """Binaire Atlus → texte lisible avec balises de contrôle."""
    out = ""
    for i in range(0, len(raw)-1, 2):
        cp = struct.unpack_from("<H", raw, i)[0]
        if cp in CTRL:           out += CTRL[cp]
        elif 0x20 <= cp <= 0x7E: out += chr(cp)
        elif 0x80 <= cp <= 0xFF: out += chr(cp)
        elif 0x1100 <= cp <= 0x12FF: out += f"[{cp:04X}]"
        else:                    out += f"[U+{cp:04X}]"
    return out

def text_to_bytes(text: str) -> bytes:
    """Texte FR (avec balises et accents) → octets binaires Atlus."""
    for fr, jp in ACCENT_MAP:
        text = text.replace(fr, jp)
    out = []; i = 0
    while i < len(text):
        ch = text[i]
        if ch == '[':
            try:   closing = text.index(']', i)
            except ValueError:
                out.append(struct.pack("<H", ord(ch))); i += 1; continue
            tag = text[i:closing+1]; i = closing+1
            if tag == "[NULL]":   out.append(b'\x00\x00'); continue
            matched = False
            for code, name in CTRL.items():
                if name == tag:
                    out.append(struct.pack("<H", code)); matched = True; break
            if matched: continue
            if tag.startswith("[U+") and len(tag) == 8:
                try: out.append(struct.pack("<H", int(tag[3:7],16))); continue
                except ValueError: pass
            if len(tag) == 6:
                try: out.append(struct.pack("<H", int(tag[1:5],16))); continue
                except ValueError: pass
            for c in tag[1:-1]: out.append(struct.pack("<H", ord(c)))
        elif ch == '\n': out.append(struct.pack("<H", NL)); i += 1
        elif ch == ' ':  out.append(struct.pack("<H", SP)); i += 1
        else:            out.append(struct.pack("<H", ord(ch))); i += 1
    return b"".join(out)


# ── Détection de format ───────────────────────────────────────────────────────

def detect(data: bytes) -> str:
    if len(data) < 4: return "UNKNOWN"
    for m in BINARY_MAGICS:
        if data[:len(m)] == m: return "BINARY"
    if data[:2] == b'\x1f\x8b': return "GZIP"
    if len(data) >= 16 and data[-16:-8] == b'CRILAYLA': return "CRILAYLA"
    if len(data) >= 8:
        s0 = struct.unpack_from("<I", data, 0)[0]
        e0 = struct.unpack_from("<I", data, 4)[0]
        if 0x800 <= s0 < e0 < len(data) and data[s0:s0+2] == b'\x1f\x8b': return "EVENT_BIN"
    return "UNKNOWN"

def crilayla_decompress(data: bytes):
    """Décompresse un bloc CRILAYLA (compression propriétaire CRI Middleware)."""
    if len(data) < 16 or data[-16:-8] != b'CRILAYLA': return None
    try:
        unc = struct.unpack_from("<I", data, len(data)-8)[0]
        csz = struct.unpack_from("<I", data, len(data)-4)[0]
        cs  = len(data) - 16 - csz
        if cs < 0 or csz == 0: return None
        rev = bytearray(data[cs:cs+csz][::-1])
        out = bytearray(unc)
        wp = unc; rp = pool = left = 0
        def nb():
            nonlocal rp, pool, left
            if left == 0:
                if rp >= len(rev): return 0
                pool = rev[rp]; rp += 1; left = 8
            left -= 1; return (pool >> left) & 1
        def rn(n):
            v = 0
            for _ in range(n): v = (v << 1) | nb()
            return v
        while wp > 0 and rp < len(rev):
            if nb() == 0:
                if rp >= len(rev): break
                wp -= 1; out[wp] = rev[rp]; rp += 1
            else:
                b2 = rn(2)
                if b2 == 3:
                    b3 = rn(3); length = (b3+3) if b3 < 7 else (rn(8)+10)
                else: length = b2+2
                offset = rn(13)+3
                for _ in range(length):
                    if wp <= 0: break
                    wp -= 1; ref = wp+offset
                    out[wp] = out[ref] if ref < unc else 0
        return bytes(out)
    except: return None

# ── Extraction CPK depuis ISO ─────────────────────────────────────────────────

def extract_cpk_from_iso(iso_path: str, out_dir: Path, log_fn) -> str:
    """Localise et extrait P2PT_ALL.cpk depuis l'ISO. Mémorise l'offset."""
    if log_fn: log_fn("Lecture de l'ISO…", "info")
    iso = open(iso_path, "rb").read()
    if log_fn: log_fn(f"  Taille : {len(iso)//1024//1024} MB", "info")
    pos = iso.find(b"CPK ")
    if pos == -1:
        raise Exception("Fichier CPK introuvable dans l'ISO.\nVérifie qu'il s'agit bien d'une ISO ULES01557.")
    if log_fn: log_fn(f"  CPK trouvé à l'offset 0x{pos:08X}", "info")
    offs = load_offsets(); offs["iso_path"] = iso_path; offs["cpk_offset_in_iso"] = pos
    save_offsets(offs)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "P2PT_ALL.cpk"
    with open(out_path, "wb") as f: f.write(iso[pos:])
    if log_fn: log_fn(f"  P2PT_ALL.cpk sauvegardé ({len(iso[pos:])//1024//1024} MB)", "ok")
    return str(out_path)


# ── Extraction event.bin depuis CPK ──────────────────────────────────────────

def extract_event_from_cpk(cpk_path: str, out_dir: Path, log_fn) -> str:
    """Localise event.bin dans le CPK par recherche de TOC gzip. Mémorise l'offset."""
    if log_fn: log_fn("Lecture du CPK…", "info")
    cpk = open(cpk_path, "rb").read()
    if log_fn: log_fn(f"  Taille CPK : {len(cpk)//1024//1024} MB", "info")
    if log_fn: log_fn("  Recherche du TOC event.bin…", "info")
    best = -1; idx = 0
    while idx < len(cpk) - 40:
        found = cpk.find(b"\x00\x10\x00\x00", idx)
        if found == -1: break
        if found % 4 != 0: idx = found+1; continue
        e0 = struct.unpack_from("<I", cpk, found+4)[0]
        if not (0x20000 <= e0 <= 0x40000): idx = found+1; continue
        if found+e0+8 >= len(cpk): idx = found+1; continue
        gp = found + 0x1000
        if gp+2 < len(cpk) and cpk[gp:gp+2] == b"\x1f\x8b":
            best = found; break
        valid = True; pe = e0
        for k in range(1,5):
            s = struct.unpack_from("<I", cpk, found+k*8)[0]
            e = struct.unpack_from("<I", cpk, found+k*8+4)[0]
            if s == 0: break
            if not (pe <= s <= pe+0x100000) or not (s < e <= s+0x100000): valid=False; break
            pe = e
        if valid: best = found; break
        idx = found+1
    if best == -1:
        raise Exception("Impossible de localiser event.bin dans le CPK automatiquement.\n→ Extrais event.bin manuellement avec CriFsLib puis charge-le à l'étape D.")
    entries = []; i = best
    while i+8 <= len(cpk):
        s = struct.unpack_from("<I", cpk, i)[0]; e = struct.unpack_from("<I", cpk, i+4)[0]
        if s == 0: break
        if entries and s < entries[-1][1]: break
        if e > s + 0x500000: break
        entries.append((s, e)); i += 8
    if not entries: raise Exception("TOC vide après parsing.")
    ev_size = entries[-1][1]
    if log_fn: log_fn(f"  {len(entries)} entrées TOC · taille = {ev_size} octets", "info")
    offs = load_offsets(); offs["event_offset_in_cpk"] = best
    cii  = offs.get("cpk_offset_in_iso", 0)
    offs["event_offset_in_iso"] = cii + best; offs["event_size"] = ev_size
    save_offsets(offs)
    if log_fn: log_fn(f"  Offset dans l'ISO : 0x{cii+best:08X}", "info")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "event.bin"
    with open(out_path, "wb") as f: f.write(cpk[best:best+ev_size])
    if log_fn: log_fn(f"  event.bin sauvegardé ({ev_size} octets)", "ok")
    return str(out_path)


# ── Extraction scripts depuis event.bin ──────────────────────────────────────

def extract_scripts_from_event(event_path: str, out_dir: Path, log_fn) -> int:
    """Découpe event.bin en 399 scripts individuels (script_000.bin … script_398.bin)."""
    data = open(event_path, "rb").read()
    out_dir.mkdir(parents=True, exist_ok=True)
    if log_fn: log_fn(f"  event.bin : {len(data)} octets", "info")
    entries = []; i = 0
    while i+8 <= len(data):
        s = struct.unpack_from("<I", data, i)[0]; e = struct.unpack_from("<I", data, i+4)[0]
        if s == 0: break
        entries.append((s, e)); i += 8
    entries = entries[:399]
    if log_fn: log_fn(f"  Extraction de {len(entries)} scripts…", "info")
    ok = skip = 0
    for idx, (start, end) in enumerate(entries):
        if end > len(data) or start >= end: skip += 1; continue
        chunk = data[start:end]
        if chunk[:2] == b"\x1f\x8b":
            try:
                with gzip.open(io.BytesIO(chunk)) as gz: chunk = gz.read()
            except Exception as eg:
                if log_fn: log_fn(f"  script_{idx:03d} : erreur gzip ({eg})", "warn")
        with open(out_dir / f"script_{idx:03d}.bin", "wb") as f: f.write(chunk)
        ok += 1
        if idx % 50 == 0 and log_fn: log_fn(f"  script_{idx:03d}.bin ({len(chunk)} octets)", "info")
    if log_fn: log_fn(f"  {ok} scripts extraits, {skip} ignorés → {out_dir}", "ok")
    return ok


# ── Détection des dialogues ───────────────────────────────────────────────────

def _valid_name(data: bytes, offset: int) -> bool:
    """Vérifie qu'un guillemet ouvrant est suivi d'un nom de personnage valide."""
    j = offset + 2
    if j+1 >= len(data): return False
    first = struct.unpack_from("<H", data, j)[0]
    if first == SP or (first in CTRL and first not in (0x1113, 0x1112)): return False
    chars = []; pr = al = uk = 0
    while j < len(data)-1:
        cp = struct.unpack_from("<H", data, j)[0]
        if cp == NL:
            n = len(chars)
            if not (1 <= n <= 40): return False
            if n <= 3 and all(chr(c) in '?.' for c in chars): return True
            return al >= 1 and (pr / max(1, n)) >= 0.6
        if 0x20 <= cp <= 0x7E:     pr += 1; al += (0x41 <= cp <= 0x7A)
        elif cp == SP:              pr += 1
        elif cp in CTRL:            pr += 1
        elif 0x1100 <= cp <= 0x11FF: pass
        else:                       uk += 1
        if uk > 2: return False
        chars.append(cp)
        if len(chars) > 40: return False
        j += 2
    return False

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
            marker = m; break
    if marker is None:
        return body, None

    # Séparer la question du bloc de choix
    parts = body.split(marker, 1)
    question = parts[0].rstrip("\n").strip()
    choice_block = marker + parts[1]

    # Extraire les options : elles sont délimitées par [0014]
    # Structure : [1208][0002][1432][NULL][NULL][0014]OPT1[1432][NULL][NULL][0014]\n[1432][NULL][NULL][0014]OPT2...
    # On split sur [0014] et on garde les parties non-vides qui ne sont que des balises ctrl
    raw_opts = re.split(r'\[0014\]', choice_block)
    options = []
    for o in raw_opts:
        # Retirer les balises de structure [1208][0002][1432][NULL][NULL] etc.
        # Nettoyer tous les codes de contrôle y compris [U+00XX] (ex: [U+0002], [U+0003])
        cleaned = re.sub(
            r'\[1208\]|\[U\+1208\]|\[U\+[0-9A-Fa-f]{4}\]|\[0002\]|\[1432\]|\[NULL\]',
            '', o
        ).strip('\n').strip()
        # Un segment valide = texte non vide sans \n interne (le \n sépare les options)
        if cleaned and '\n' not in cleaned:
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


def find_dialogs(data: bytes) -> list:
    """Scanne un buffer binaire et extrait tous les dialogues valides."""
    dialogs = []; i = 0
    while i < len(data)-1:
        w = struct.unpack_from("<H", data, i)[0]
        if w != 0x0022 or not _valid_name(data, i): i += 2; continue
        start = i; chars = []; j = i; found = False; term = None
        while j < len(data)-1:
            c = struct.unpack_from("<H", data, j)[0]; chars.append(c)
            if len(chars) > 2000: break
            t4 = chars[-4:]; t3 = chars[-3:]
            if t4 in ([E1,E2,E3,E4],[CHAIN_E1,E2,E3,E4]):
                end = j+2; term = t4; found = True; break
            if t3 in ([E1,E2,E4],[CHAIN_E1,E2,E4]):
                end = j+2; term = t3; found = True; break
            j += 2
        if not found: i += 2; continue
        k = end
        while k+1 < len(data) and struct.unpack_from("<H", data, k)[0] == 0: k += 2
        raw_b = data[start:end]; ac = tc = 0; pnl = False
        for bi in range(0, len(raw_b)-1, 2):
            bv = struct.unpack_from("<H", raw_b, bi)[0]
            if bv == NL: pnl = True; continue
            if not pnl: continue
            if bv in {E1,E2,E3,E4,SP,CHAIN_E1}: continue
            tc += 1
            if 0x20 <= bv <= 0x7E: ac += 1
        if tc > 5 and (ac/tc) < 0.25: i += 2; continue
        txt = decode_text(raw_b); lns = txt.split("\n")
        nom = lns[0].lstrip('"') if lns else ""
        body = "\n".join(lns[1:])
        for seq in ("[E1][E2][E3][E4]","[1109][E2][E3][E4]","[E1][E2][E4]","[1109][E2][E4]"):
            body = body.replace(seq, "")
        body_clean = body.strip()
        question, choices = _parse_choices(body_clean)
        entry = {
            "id": len(dialogs), "offset": start,
            "data_size": end-start, "slot_size": k-start, "_term": term,
            "nom_orig": nom, "texte_orig": body_clean, "nom_fr": "", "texte_fr": ""
        }
        if choices is not None:
            entry["question_orig"] = question
            entry["choix_orig"] = choices
            entry["question_fr"] = ""
            entry["choix_fr"] = [""] * len(choices)
        dialogs.append(entry)
        i = k
    return dialogs

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



def decode_all_scripts(scripts_dir: Path, output_dir: Path, log_fn):
    """Décode tous les scripts_bin/*.bin en fichiers JSON prêts à traduire."""
    output_dir.mkdir(parents=True, exist_ok=True)
    total = vides = 0
    for idx in range(399):
        bf = scripts_dir / f"script_{idx:03d}.bin"
        if not bf.exists(): bf = scripts_dir / f"script_{idx}.bin"
        if not bf.exists(): continue
        raw = open(bf, "rb").read()
        if raw[:2] == b'\x1f\x8b':
            try: raw = gzip.decompress(raw)
            except: pass
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
                        d["nom_fr"]   = prev.get("nom_fr", "")
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
        total += 1
        if not dlgs: vides += 1
        if idx % 50 == 0 and log_fn: log_fn(f"  script_{idx:03d} → {len(dlgs)} dialogues", "info")
    if log_fn: log_fn(f"  {total} scripts décodés ({vides} vides)", "ok")



# ── Validation cohérence menus de choix ───────────────────────────────────────

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
        if log_fn: log_fn(f"  Impossible de lire {json_path} : {e}", "err")
        return []

    by_id = {e["id"]: e for e in data}
    problems = []

    # Identifier les slots avec menu de choix
    menu_slots = [
        e for e in data
        if "[1208]" in e.get("texte_orig","") or "[0002]" in e.get("texte_orig","")
    ]

    for menu_entry in menu_slots:
        intro_entry = by_id.get(menu_entry["id"] - 1)
        if not intro_entry:
            continue

        # Ne vérifier que si les deux ont une traduction
        q_fr_raw  = menu_entry.get("texte_fr","")
        i_fr_raw  = intro_entry.get("texte_fr","")
        if not q_fr_raw or not i_fr_raw:
            continue

        # Extraire la question du menu = tout avant [1208] / [0002]
        q_fr = q_fr_raw.split("[U+1208]")[0].split("[1208]")[0].split("[0002]")[0].strip()

        # Normaliser pour comparaison souple (ignorer espaces/ponctuation finale)
        def norm(s):
            return s.strip().rstrip("?! ").replace(" ", "").replace("\n", "").lower()

        q_norm = norm(q_fr)
        i_norm = norm(i_fr_raw)

        # La fin de l'intro doit correspondre à la question (sur les 20 derniers chars)
        tail = max(15, len(q_norm) - 3)
        if not i_norm.endswith(q_norm[-tail:]):
            problems.append({
                "intro_id":  intro_entry["id"],
                "menu_id":   menu_entry["id"],
                "q_menu":    q_fr,
                "intro_end": i_fr_raw,
            })
            if log_fn:
                log_fn(
                    f"  ⚠ Incohérence menu : id={intro_entry['id']} (intro) "
                    f"ne se termine pas par la question de id={menu_entry['id']}",
                    "warn"
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
        if log_fn: log_fn("  Aucun fichier JSON trouvé.", "warn")
        return {"total_files": 0, "files_with_issues": 0, "problems": []}

    all_problems = []
    files_with_issues = 0

    for i, jf in enumerate(files):
        if progress_fn: progress_fn((i + 1) / len(files))
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
                f"({len(all_problems)} total)", "warn"
            )
        else:
            log_fn(f"  Tous les menus sont cohérents ({len(files)} fichiers).", "ok")

    return {
        "total_files":      len(files),
        "files_with_issues": files_with_issues,
        "problems":         all_problems,
    }

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
    marker_fr = '[U+1208]' if '[U+1208]' in t_fr else ('[1208]' if '[1208]' in t_fr else None)
    if marker_fr is None:
        return t_fr  # pas un slot de menu

    # Calculer l'offset du 1er [0014] (= début opt1) dans l'original encodé
    # Structure : [1208](2)+[0002](2)+[1432](2)+[NULL](2)+[NULL](2)+[0014](2) = 12 bytes
    nom_orig_clean = nom_orig.replace('[SP]', ' ')
    pre_orig = texte_orig.split('[1208]')[0]
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
    return t_fr.replace(marker_fr, '[SP]' * n_sp + '[1208]', 1)


def encode_bin_from_json(bin_path: str, json_path: str, log_fn, out_path: str = None) -> str:
    """Réécrit les dialogues traduits dans le fichier .bin. Préserve le _term et le slot_size."""
    data  = bytearray(open(bin_path,"rb").read())
    dlgs  = json.load(open(json_path, encoding="utf-8"))
    ok = skip = kept = 0
    for d in dlgs:
        n_fr = d.get("nom_fr","").strip(); t_fr = d.get("texte_fr","").strip()
        # Si c'est un menu de choix avec les champs dédiés, reconstruire texte_fr
        choix_fr = d.get("choix_fr")
        q_fr = d.get("question_fr","").strip()
        if choix_fr is not None:
            # Utiliser question_fr/choix_fr si remplis, sinon fallback sur texte_fr
            filled_choices = [c for c in choix_fr if c.strip()]
            if q_fr and filled_choices:
                t_fr = _rebuild_choice_body(q_fr, choix_fr)
            elif not t_fr:
                # Rien de traduit du tout → skip
                kept += 1; continue
        elif not n_fr and not t_fr: kept += 1; continue

        # Aligner les options de menu à leur offset original (fix pointeurs PSP absolus)
        t_fr_aligned = _align_menu_text(
            d.get("nom_orig", ""), d.get("texte_orig", ""),
            n_fr, t_fr
        )
        if t_fr_aligned == t_fr and ('[1208]' in t_fr or '[U+1208]' in t_fr):
            # Vérifier si c'est parce que la question FR est trop longue
            import re as _re
            marker = '[U+1208]' if '[U+1208]' in t_fr else '[1208]'
            pre_fr_enc = text_to_bytes('"' + n_fr + "\n" + t_fr.split(marker)[0])
            pre_orig_enc = text_to_bytes('"' + d.get("nom_orig","").replace('[SP]',' ') + "\n" + d.get("texte_orig","").split('[1208]')[0])
            if len(pre_fr_enc) > len(pre_orig_enc):
                if log_fn: log_fn(
                    f"  ⚠ [id {d['id']}] question FR trop longue de "
                    f"{(len(pre_fr_enc)-len(pre_orig_enc))//2} mot(s) → "
                    f"les choix seront décalés ! Raccourcir la question.", "warn"
                )
        t_fr = t_fr_aligned

        enc = text_to_bytes('"' + n_fr + "\n" + t_fr)
        avail = d["data_size"] - 8
        # Pour les slots de menu, le moteur PSP exige un NL (0x1101) juste
        # avant le terminateur (il est dans le binaire original mais absent de texte_orig).
        # On réserve ce NL dans le padding au lieu de mettre un SP.
        is_menu = '[1208]' in d.get("texte_orig","") or '[U+1208]' in d.get("texte_orig","")
        nl_suffix = struct.pack("<H", NL) if is_menu else b""
        avail_for_enc = avail - len(nl_suffix) // 2
        if len(enc) > avail - (1 if is_menu else 0) * 2:
            if log_fn: log_fn(f"  [id {d['id']}] trop long ({len(enc)}>{avail}), ignoré","warn")
            skip += 1; continue
        sp_count = (avail - len(enc) - (1 if is_menu else 0) * 2) // 2
        sp_pad = struct.pack("<H", SP) * sp_count
        term = d.get("_term", [E1,E2,E3,E4])
        end_c = struct.pack("<HHHH",*term) if len(term)==4 else struct.pack("<HHH",*term) if len(term)==3 else struct.pack("<HHHH",E1,E2,E3,E4)
        null_gap = bytes(d["slot_size"] - d["data_size"])
        full = enc + sp_pad + nl_suffix + end_c + null_gap
        if len(full) != d["slot_size"]: skip += 1; continue
        data[d["offset"]:d["offset"]+d["slot_size"]] = full
        ok += 1
    if out_path is None: out_path = bin_path
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    with open(out_path,"wb") as f: f.write(data)
    if log_fn: log_fn(f"  {ok} traduits · {skip} ignorés · {kept} conservés → {Path(out_path).name}","ok")
    return out_path


# ── Scan fichiers BNP/BIN ─────────────────────────────────────────────────────

def scan_bnp_bin(data: bytes, stem: str, out_dir: Path, log_fn) -> int:
    """Extrait les dialogues d'un BNP/BIN (route vers le décodeur spécial si F_BE/TM_EVE)."""
    if stem.lower() in ("f_be","tm_eve"):
        return scan_fbe_bnp(data, stem, out_dir, log_fn)
    all_dlgs = find_dialogs(data)
    pos = gz_n = 0
    while gz_n < 200:
        idx = data.find(b'\x1f\x8b', pos)
        if idx == -1: break
        try:
            dec = gzip.decompress(data[idx:])
            if len(dec) > 64:
                for d in find_dialogs(dec): d["_source"] = f"gz@0x{idx:X}"; all_dlgs.append(d)
                gz_n += 1
        except: pass
        pos = idx + 2
    if detect(data) == "CRILAYLA":
        dec = crilayla_decompress(data)
        if dec:
            for d in find_dialogs(dec): d["_source"] = "crilayla"; all_dlgs.append(d)
    seen = set(); unique = []
    for d in all_dlgs:
        k = (d["offset"], d["data_size"])
        if k not in seen: seen.add(k); unique.append(d)
    for k, d in enumerate(unique): d["id"] = k
    if not unique: return 0
    out_path = out_dir / f"{stem.upper()}.json"
    with open(out_path,"w",encoding="utf-8") as f: json.dump(unique,f,ensure_ascii=False,indent=2)
    if log_fn: log_fn(f"  {stem.upper()}: {len(unique)} dialogues → {out_path.name}","ok")
    return len(unique)

def scan_cpk_files(cpk_dir_str: str, out_dir: Path, log_fn=None, progress_fn=None) -> dict:
    """Scanne les fichiers cibles dans cpk_files/ et extrait leurs dialogues en JSON."""
    cpk_dir = Path(cpk_dir_str); out_dir.mkdir(parents=True, exist_ok=True)
    targets = sorted(SCAN_TARGETS)
    fmap = {f.name.lower(): f for f in Path(cpk_dir_str).rglob("*") if f.is_file()}
    if log_fn: log_fn("Scan des fichiers de jeu…","head")
    total = []; done = []
    for i, tname in enumerate(targets):
        if progress_fn: progress_fn((i+1)/len(targets))
        fp = fmap.get(tname)
        if not fp:
            if log_fn: log_fn(f"  ✗ {tname} — introuvable","warn"); continue
        try: raw = open(fp,"rb").read()
        except Exception as e:
            if log_fn: log_fn(f"  ✗ {tname} — erreur : {e}","err"); continue
        n = scan_bnp_bin(raw, fp.stem, out_dir, log_fn)
        total.append(n)
        if n > 0: done.append(tname)
    if log_fn: log_fn(f"  Total : {sum(total)} dialogues dans {len(done)} fichiers","ok")
    return {"total": sum(total), "files": done}


# ── Rebuild event.bin ─────────────────────────────────────────────────────────

def rebuild_event_bin(orig_event: bytes, scripts_fr_dir: Path, log_fn) -> bytes:
    """Réinjecte les scripts traduits dans event.bin (recompresse en gzip)."""
    event = bytearray(orig_event); toc = []; i = 0
    while i+8 <= len(event):
        s = struct.unpack_from("<I",event,i)[0]; e = struct.unpack_from("<I",event,i+4)[0]
        if s == 0: break
        toc.append((s,e,i)); i += 8
    patched = 0
    for idx,(start,end,tp) in enumerate(toc):
        fr = scripts_fr_dir / f"script_{idx:03d}_fr.bin"
        if not fr.exists(): fr = scripts_fr_dir / f"script_{idx}_fr.bin"
        if not fr.exists(): continue
        sc = open(fr,"rb").read()
        gz_buf = io.BytesIO()
        with gzip.GzipFile(filename=b"e0000.bin",mode="wb",fileobj=gz_buf,mtime=0) as gz: gz.write(sc)
        new_gz = gz_buf.getvalue()
        if len(new_gz) > end-start:
            if log_fn: log_fn(f"  [ignoré] script_{idx:03d} : trop grand","warn"); continue
        event[start:start+len(new_gz)] = new_gz
        event[start+len(new_gz):end]   = bytes((end-start)-len(new_gz))
        struct.pack_into("<I",event,tp+4,start+len(new_gz))
        patched += 1
    if log_fn: log_fn(f"  {patched}/{len(toc)} scripts réinjectés","ok")
    return bytes(event)


# ── Rebuild ISO ───────────────────────────────────────────────────────────────

def rebuild_iso(iso_orig: str, event_data: bytes, out_iso: str, log_fn) -> bool:
    """Patche event.bin dans une copie de l'ISO. L'original n'est jamais touché."""
    if log_fn: log_fn("Préparation du rebuild ISO…","info")
    offs = load_offsets(); pos = offs.get("event_offset_in_iso",-1)
    if pos != -1:
        with open(iso_orig,"rb") as f:
            f.seek(pos); chk = struct.unpack("<I",f.read(4))[0]
        if chk != 0x1000:
            if log_fn: log_fn(f"  Offset mémorisé invalide (0x{chk:x}), re-extraction nécessaire.","warn")
            pos = -1
    if pos == -1:
        raise Exception("Offset event.bin inconnu.\n→ Relance les étapes A, B, C pour le recalculer.")
    if log_fn: log_fn(f"  Injection à l'offset 0x{pos:08X}","info")
    shutil.copy(iso_orig, out_iso)
    with open(out_iso,"r+b") as f: f.seek(pos); f.write(event_data)
    sz = Path(out_iso).stat().st_size // 1024 // 1024
    if log_fn: log_fn(f"  ISO générée : {out_iso} ({sz} MB)","ok")
    return True


# ── Encodage complet ──────────────────────────────────────────────────────────

def encode_all(trad_dir: str, cpk_dir: str, enc_dir: str, log_fn, progress_fn=None) -> dict:
    """Encode tous les JSON traduits en une seule passe (BNP/BIN + event.bin)."""
    jdir = Path(trad_dir); cpk = Path(cpk_dir); out = Path(enc_dir)
    out.mkdir(parents=True, exist_ok=True)
    cmap = {f.name.lower(): f for f in cpk.rglob("*") if f.is_file()}
    ok_f = []; err_f = []
    steps = [
        ("CD_SHOP.json","cd_shop.bin","CD_SHOP.BIN"),
        ("F_BE.json","f_be.bnp","F_BE.BNP"),
        ("TM_EVE.json","tm_eve.bnp","TM_EVE.BNP"),
        ("MMAP01.json","mmap01.bnp","MMAP01.BNP"),
        ("MMAP02.json","mmap02.bnp","MMAP02.BNP"),
        ("MMAP03.json","mmap03.bnp","MMAP03.BNP"),
        ("MMAP04.json","mmap04.bnp","MMAP04.BNP"),
        ("MMAP05.json","mmap05.bnp","MMAP05.BNP"),
        ("MMAP06.json","mmap06.bnp","MMAP06.BNP"),
    ]
    n = len(steps)+1
    for i,(jn,on,fn) in enumerate(steps):
        if progress_fn: progress_fn((i+1)/n)
        jp = jdir/jn
        if not jp.exists():
            if log_fn: log_fn(f"  {jn} absent → ignoré","info"); continue
        op = cmap.get(on)
        if not op:
            if log_fn: log_fn(f"  ✗ {on} introuvable dans cpk_files/","warn"); err_f.append(fn); continue
        try:
            if log_fn: log_fn(f"  Encodage {jn}…","info")
            encode_bin_from_json(str(op),str(jp),log_fn,out_path=str(out/fn))
            ok_f.append(fn)
        except Exception as e:
            if log_fn: log_fn(f"  ✗ {fn} : {e}","err"); err_f.append(fn)
    sj = jdir/"event_scripts"; ep = cmap.get("event.bin")
    if progress_fn: progress_fn((n-1)/n)
    if ep and sj.exists():
        if log_fn: log_fn("  Encodage scripts event.bin…","info")
        try:
            ev = open(ep,"rb").read(); tmp = out/"_ev_tmp"; tmp.mkdir(parents=True,exist_ok=True)
            extract_scripts_from_event(str(ep), tmp, None)
            sc_ok = 0
            for js in sorted(sj.glob("script_*.json")):
                si = js.stem.split("_")[-1].lstrip("0") or "0"
                try: si = int(si)
                except: continue
                bs = tmp/f"script_{si:03d}.bin"
                if not bs.exists(): bs = tmp/f"script_{si}.bin"
                if not bs.exists(): continue
                try:
                    encode_bin_from_json(str(bs),str(js),None,out_path=str(tmp/f"script_{si:03d}_fr.bin"))
                    sc_ok += 1
                except: pass
            if log_fn: log_fn(f"  {sc_ok} scripts encodés","info")
            new_ev = rebuild_event_bin(ev, tmp, log_fn)
            with open(out/"event.bin","wb") as f: f.write(new_ev)
            ok_f.append("event.bin")
            if log_fn: log_fn("  ✓ event.bin reconstruit","ok")
            shutil.rmtree(str(tmp),ignore_errors=True)
        except Exception as e:
            if log_fn: log_fn(f"  ✗ event.bin : {e}","err"); err_f.append("event.bin")
    else:
        if log_fn: log_fn("  event_scripts/ ou event.bin absent → ignoré","info")
    if progress_fn: progress_fn(1.0)
    if log_fn:
        log_fn(f"\n  Encodés : {', '.join(ok_f) or 'aucun'}","ok")
        if err_f: log_fn(f"  Erreurs : {', '.join(err_f)}","err")
    return {"ok": ok_f, "err": err_f}

# ═════════════════════════════════════════════════════════════════════════════

# ═════════════════════════════════════════════════════════════════════════════
#  INTERFACE GRAPHIQUE — Redesign moderne (inspiration VS Code / macOS)
# ═════════════════════════════════════════════════════════════════════════════

# ── Palette claire / sombre ───────────────────────────────────────────────────
THEMES = {
    "light": {
        "bg":        "#f5f5f7",   # fond principal
        "panel":     "#ffffff",   # panneaux / cartes
        "border":    "#e5e5ea",   # bordures fines
        "accent":    "#0066cc",   # bleu sobre
        "accent_hov":"#0055aa",
        "ok":        "#34c759",
        "warn":      "#ff9500",
        "err":       "#ff3b30",
        "txt":       "#1d1d1f",   # texte principal
        "txt2":      "#6e6e73",   # texte secondaire
        "txt3":      "#aeaeb2",   # placeholder / muted
        "step_bg":   "#e8f0fb",   # badge étape fond
        "step_fg":   "#0066cc",
        "log_bg":    "#fafafa",
        "btn_sec":   "#e5e5ea",   # bouton secondaire fond
        "btn_sec_hov":"#d5d5da",
        "scroll":    "#c7c7cc",
    },
    "dark": {
        "bg":        "#1c1c1e",
        "panel":     "#2c2c2e",
        "border":    "#3a3a3c",
        "accent":    "#0a84ff",
        "accent_hov":"#409cff",
        "ok":        "#30d158",
        "warn":      "#ff9f0a",
        "err":       "#ff453a",
        "txt":       "#f5f5f7",
        "txt2":      "#98989d",
        "txt3":      "#636366",
        "step_bg":   "#1c3260",
        "step_fg":   "#5ac8fa",
        "log_bg":    "#1c1c1e",
        "btn_sec":   "#3a3a3c",
        "btn_sec_hov":"#4a4a4e",
        "scroll":    "#48484a",
    },
}

_theme_name = "dark"

def TH(key):
    """Retourne la couleur du thème actif."""
    return THEMES[_theme_name][key]


# ── Tooltip simple ────────────────────────────────────────────────────────────
class Tooltip:
    """Info-bulle légère qui apparaît après un court délai au survol d'un widget."""
    def __init__(self, widget, text: str):
        self.widget = widget
        self.text   = text
        self._tip   = None
        self._job   = None
        widget.bind("<Enter>", self._schedule)
        widget.bind("<Leave>", self._cancel)

    def _schedule(self, _=None):
        self._cancel()
        self._job = self.widget.after(600, self._show)

    def _cancel(self, _=None):
        if self._job:
            self.widget.after_cancel(self._job)
            self._job = None
        if self._tip:
            self._tip.destroy()
            self._tip = None

    def _show(self):
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 4
        self._tip = tk.Toplevel(self.widget)
        self._tip.wm_overrideredirect(True)
        self._tip.wm_geometry(f"+{x}+{y}")
        bg = "#1d1d1f" if _theme_name == "light" else "#f5f5f7"
        fg = "#f5f5f7" if _theme_name == "light" else "#1d1d1f"
        tk.Label(self._tip, text=self.text, bg=bg, fg=fg,
                 font=("SF Pro Display", 9) if platform.system() == "Darwin" else ("Segoe UI", 9),
                 padx=8, pady=4, relief="flat", bd=0, wraplength=300
                 ).pack()


# ── Classe principale ─────────────────────────────────────────────────────────
class P2ISFRTool(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("P2IS FR Tool")
        self.geometry("900x980")
        self.minsize(740, 780)
        self.resizable(True, True)

        self._wdir   = tk.StringVar(value=str(DEFAULT_WORK))
        self._crifsl = tk.StringVar(value=DEFAULT_CRIFSL)
        self._wdir.trace_add("write", lambda *_: self._sync_offsets())
        self._sync_offsets()

        self._apply_theme()
        self._build()

    # ── Thème ──────────────────────────────────────────────────────────────────

    def _apply_theme(self):
        ctk.set_appearance_mode("dark" if _theme_name == "dark" else "light")
        self.configure(fg_color=TH("bg"))

    def _toggle_theme(self):
        global _theme_name
        _theme_name = "light" if _theme_name == "dark" else "dark"
        # Sauvegarder les valeurs
        saved = {a: getattr(self, a, tk.StringVar()).get() for a in (
            "_wdir","_crifsl","_v_iso","_v_cpk","_v_event","_v_sbin","_v_sjson",
            "_v_cpkf","_v_scan","_v_trad","_v_cpkenc","_v_enc",
            "_v_iso2","_v_encin","_v_outiso"
        )}
        for w in self.winfo_children(): w.destroy()
        self._wdir   = tk.StringVar(value=saved["_wdir"])
        self._crifsl = tk.StringVar(value=saved["_crifsl"])
        self._wdir.trace_add("write", lambda *_: self._sync_offsets())
        self._sync_offsets()
        self._apply_theme()
        self._build()
        for attr, val in saved.items():
            if hasattr(self, attr) and val:
                getattr(self, attr).set(val)

    # ── Langue ────────────────────────────────────────────────────────────────

    def _toggle_lang(self):
        global _lang
        _lang = "en" if _lang == "fr" else "fr"
        saved = {a: getattr(self, a, tk.StringVar()).get() for a in (
            "_wdir","_crifsl","_v_iso","_v_cpk","_v_event","_v_sbin","_v_sjson",
            "_v_cpkf","_v_scan","_v_trad","_v_cpkenc","_v_enc",
            "_v_iso2","_v_encin","_v_outiso"
        )}
        for w in self.winfo_children(): w.destroy()
        self._wdir   = tk.StringVar(value=saved["_wdir"])
        self._crifsl = tk.StringVar(value=saved["_crifsl"])
        self._wdir.trace_add("write", lambda *_: self._sync_offsets())
        self._sync_offsets()
        self._apply_theme()
        self._build()
        for attr, val in saved.items():
            if hasattr(self, attr) and val:
                getattr(self, attr).set(val)

    def _sync_offsets(self):
        global OFFSETS_FILE
        OFFSETS_FILE = str(Path(self._wdir.get()) / "offsets.json")

    @property
    def W(self) -> Path:
        return Path(self._wdir.get())

    # ── Polices ────────────────────────────────────────────────────────────────

    @staticmethod
    def _font(size=11, weight="normal", mono=False):
        if platform.system() == "Darwin":
            fam = "SF Mono" if mono else "SF Pro Display"
        elif platform.system() == "Windows":
            fam = "Consolas" if mono else "Segoe UI"
        else:
            fam = "DejaVu Sans Mono" if mono else "Ubuntu"
        return (fam, size, weight)

    # ── Construction principale ────────────────────────────────────────────────

    def _build(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self._build_topbar()
        self._build_workdir_bar()
        self._build_tabs()
        self._build_log_panel()

    # ── Topbar ────────────────────────────────────────────────────────────────

    def _build_topbar(self):
        bar = ctk.CTkFrame(self, fg_color=TH("panel"), corner_radius=0, height=60)
        bar.grid(row=0, column=0, sticky="ew")
        bar.grid_columnconfigure(1, weight=1)
        bar.grid_propagate(False)

        # Titre + sous-titre
        title_frame = ctk.CTkFrame(bar, fg_color="transparent")
        title_frame.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        ctk.CTkLabel(title_frame, text="P2IS FR Tool",
                     font=self._font(15, "bold"),
                     text_color=TH("txt")).pack(side="left", padx=(0, 10))
        ctk.CTkLabel(title_frame, text="Persona 2 IS PSP · ULES01557",
                     font=self._font(10),
                     text_color=TH("txt3")).pack(side="left", pady=(2, 0))

        # Boutons topbar droite
        btn_frame = ctk.CTkFrame(bar, fg_color="transparent")
        btn_frame.grid(row=0, column=2, padx=16, sticky="e")

        self._lang_btn = ctk.CTkButton(
            btn_frame, text=T("lang_btn"),
            width=56, height=28, corner_radius=8,
            font=self._font(10, "bold"),
            fg_color=TH("btn_sec"), hover_color=TH("btn_sec_hov"),
            text_color=TH("txt"), border_width=0,
            command=self._toggle_lang)
        self._lang_btn.pack(side="left", padx=(0, 6))

        theme_icon = "☀️" if _theme_name == "dark" else "🌙"
        self._theme_btn = ctk.CTkButton(
            btn_frame, text=theme_icon,
            width=36, height=28, corner_radius=8,
            font=self._font(13),
            fg_color=TH("btn_sec"), hover_color=TH("btn_sec_hov"),
            text_color=TH("txt"), border_width=0,
            command=self._toggle_theme)
        self._theme_btn.pack(side="left")

        # Séparateur fin
        sep = ctk.CTkFrame(self, fg_color=TH("border"), height=1, corner_radius=0)
        sep.grid(row=0, column=0, sticky="ews")

    # ── Barre dossier de travail ───────────────────────────────────────────────

    def _build_workdir_bar(self):
        bar = ctk.CTkFrame(self, fg_color=TH("panel"), corner_radius=0)
        bar.grid(row=1, column=0, sticky="ew")
        bar.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(bar, text=T("work_lbl"),
                     font=self._font(10), text_color=TH("txt2"), width=150, anchor="w"
                     ).grid(row=0, column=0, padx=(18, 6), pady=8)

        ctk.CTkEntry(bar,
                     textvariable=self._wdir,
                     font=self._font(10, mono=True),
                     fg_color=TH("bg"), text_color=TH("txt"),
                     border_color=TH("border"), border_width=1, corner_radius=6,
                     height=30
                     ).grid(row=0, column=1, sticky="ew", padx=(0, 4), pady=8)

        ctk.CTkButton(bar, text="📂", width=34, height=30, corner_radius=6,
                      font=self._font(13),
                      fg_color=TH("btn_sec"), hover_color=TH("btn_sec_hov"),
                      text_color=TH("txt"), border_width=0,
                      command=lambda: self._wdir.set(
                          filedialog.askdirectory() or self._wdir.get())
                      ).grid(row=0, column=2, padx=(0, 16), pady=8)

        # Séparateur
        ctk.CTkFrame(self, fg_color=TH("border"), height=1, corner_radius=0).grid(
            row=1, column=0, sticky="ews")

    # ── Onglets ────────────────────────────────────────────────────────────────

    def _build_tabs(self):
        self._tabs = ctk.CTkTabview(
            self,
            fg_color=TH("bg"),
            segmented_button_fg_color=TH("panel"),
            segmented_button_selected_color=TH("accent"),
            segmented_button_selected_hover_color=TH("accent_hov"),
            segmented_button_unselected_color=TH("panel"),
            segmented_button_unselected_hover_color=TH("btn_sec"),
            text_color=TH("txt2"),
            text_color_disabled=TH("txt3"),
        )
        self._tabs.grid(row=2, column=0, padx=0, pady=0, sticky="nsew")
        for k in ("tab_extract","tab_scan","tab_encode","tab_rebuild"):
            self._tabs.add(T(k))
        self._build_tab_extract()
        self._build_tab_scan()
        self._build_tab_encode()
        self._build_tab_rebuild()

    # ── Zone de log ───────────────────────────────────────────────────────────

    def _build_log_panel(self):
        panel = ctk.CTkFrame(self, fg_color=TH("panel"), corner_radius=0)
        panel.grid(row=3, column=0, sticky="ew")
        panel.grid_columnconfigure(0, weight=1)

        # Séparateur haut
        ctk.CTkFrame(panel, fg_color=TH("border"), height=1, corner_radius=0
                     ).grid(row=0, column=0, columnspan=3, sticky="ew")

        # En-tête
        hdr = ctk.CTkFrame(panel, fg_color="transparent")
        hdr.grid(row=1, column=0, sticky="ew", padx=16, pady=(8, 2))
        hdr.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(hdr, text=T("log_title"),
                     font=self._font(10, "bold"), text_color=TH("txt2")
                     ).grid(row=0, column=0, sticky="w")

        btns = ctk.CTkFrame(hdr, fg_color="transparent")
        btns.grid(row=0, column=1, sticky="e")

        ctk.CTkButton(btns, text="⎘ " + ("Copier" if _lang == "fr" else "Copy"),
                      width=72, height=22, corner_radius=6,
                      font=self._font(9), fg_color=TH("btn_sec"),
                      hover_color=TH("btn_sec_hov"), text_color=TH("txt2"),
                      border_width=0, command=self._copy_log
                      ).pack(side="left", padx=(0, 6))

        ctk.CTkButton(btns, text=T("log_clear"),
                      width=64, height=22, corner_radius=6,
                      font=self._font(9), fg_color=TH("btn_sec"),
                      hover_color=TH("btn_sec_hov"), text_color=TH("txt2"),
                      border_width=0, command=self._clear_log
                      ).pack(side="left")

        # Zone texte
        self._log_box = ctk.CTkTextbox(
            panel,
            font=self._font(10, mono=True),
            height=120,
            fg_color=TH("log_bg"),
            text_color=TH("txt2"),
            border_width=0,
            corner_radius=0,
            activate_scrollbars=True,
            scrollbar_button_color=TH("scroll"),
            scrollbar_button_hover_color=TH("txt3"),
        )
        self._log_box.grid(row=2, column=0, sticky="ew", padx=0, pady=(2, 0))
        self._log_box.configure(state="disabled")

        for tag, col in [
            ("ok",   TH("ok")),
            ("warn", TH("warn")),
            ("err",  TH("err")),
            ("info", TH("txt2")),
            ("head", TH("accent")),
        ]:
            self._log_box.tag_config(tag, foreground=col)

    # ── Helpers constructeurs ─────────────────────────────────────────────────

    def _scroll_frame(self, parent):
        """Crée un CTkScrollableFrame avec le thème actif."""
        return ctk.CTkScrollableFrame(
            parent, fg_color="transparent",
            scrollbar_button_color=TH("scroll"),
            scrollbar_button_hover_color=TH("txt3"),
        )

    def _card(self, parent, title: str, row: int, step: str = None) -> ctk.CTkFrame:
        """Carte avec fond panel, bordure subtile, titre + badge étape optionnel."""
        outer = ctk.CTkFrame(parent, fg_color=TH("border"), corner_radius=10)
        outer.grid(row=row, column=0, sticky="ew", padx=12, pady=(0, 10))
        outer.grid_columnconfigure(0, weight=1)

        inner = ctk.CTkFrame(outer, fg_color=TH("panel"), corner_radius=9)
        inner.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
        inner.grid_columnconfigure(0, weight=1)

        # En-tête de la carte
        hdr = ctk.CTkFrame(inner, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="ew", padx=16, pady=(14, 6))

        if step:
            badge = ctk.CTkLabel(
                hdr, text=step,
                font=self._font(9, "bold"),
                fg_color=TH("step_bg"), text_color=TH("step_fg"),
                corner_radius=6, width=24, height=20,
            )
            badge.pack(side="left", padx=(0, 10))

        ctk.CTkLabel(hdr, text=title,
                     font=self._font(12, "bold"),
                     text_color=TH("txt")
                     ).pack(side="left")

        return inner

    def _path_row(self, parent, label: str, var: tk.StringVar, pick_fn, row: int,
                  tooltip: str = None):
        """Ligne label + champ + bouton 📂."""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=row, column=0, sticky="ew", padx=16, pady=(2, 6))
        frame.grid_columnconfigure(1, weight=1)

        lbl = ctk.CTkLabel(frame, text=label, width=175, anchor="w",
                           font=self._font(10), text_color=TH("txt2"))
        lbl.grid(row=0, column=0, padx=(0, 8))

        entry = ctk.CTkEntry(frame, textvariable=var,
                             font=self._font(10, mono=True),
                             fg_color=TH("bg"), text_color=TH("txt"),
                             border_color=TH("border"), border_width=1,
                             corner_radius=6, height=30)
        entry.grid(row=0, column=1, sticky="ew", padx=(0, 6))

        btn = ctk.CTkButton(frame, text="📂", width=34, height=30, corner_radius=6,
                            font=self._font(13),
                            fg_color=TH("btn_sec"), hover_color=TH("btn_sec_hov"),
                            text_color=TH("txt"), border_width=0,
                            command=pick_fn)
        btn.grid(row=0, column=2)

        if tooltip:
            Tooltip(lbl, tooltip)
            Tooltip(entry, tooltip)

    def _action_btn(self, parent, label: str, cmd, row: int,
                    tooltip: str = None) -> tuple:
        """Bouton d'action principal + badge de statut."""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=row, column=0, sticky="ew", padx=16, pady=(6, 14))
        frame.grid_columnconfigure(0, weight=1)

        inner = ctk.CTkFrame(frame, fg_color="transparent")
        inner.pack(side="left")

        btn = ctk.CTkButton(
            inner, text=label,
            font=self._font(11, "bold"),
            fg_color=TH("accent"), hover_color=TH("accent_hov"),
            text_color="#ffffff",
            height=38, corner_radius=8, border_width=0,
            command=cmd,
        )
        btn.pack(side="left")

        badge = ctk.CTkLabel(
            inner, text="",
            font=self._font(10, mono=True),
            text_color=TH("txt3"), width=160,
        )
        badge.pack(side="left", padx=(12, 0))

        if tooltip:
            Tooltip(btn, tooltip)

        return btn, badge

    def _progress(self, parent, row: int) -> ctk.CTkProgressBar:
        pb = ctk.CTkProgressBar(
            parent, mode="determinate",
            fg_color=TH("border"), progress_color=TH("accent"),
            height=4, corner_radius=2,
        )
        pb.grid(row=row, column=0, sticky="ew", padx=16, pady=(0, 4))
        pb.set(0)
        return pb

    def _tip(self, parent, text: str, row: int):
        ctk.CTkLabel(
            parent, text=text,
            font=self._font(9), text_color=TH("txt3"),
            justify="left", anchor="w", wraplength=680,
        ).grid(row=row, column=0, sticky="w", padx=16, pady=(0, 6))

    def _note(self, parent, text: str, row: int):
        ctk.CTkLabel(
            parent, text=f"→ {text}",
            font=self._font(9), text_color=TH("txt3"),
            justify="left", anchor="w",
        ).grid(row=row, column=0, sticky="w", padx=16, pady=(0, 2))

    def _instr_box(self, parent, text: str, row: int):
        box = ctk.CTkFrame(parent, fg_color=TH("bg"), corner_radius=8)
        box.grid(row=row, column=0, sticky="ew", padx=16, pady=(0, 6))
        ctk.CTkLabel(
            box, text=text,
            font=self._font(10, mono=True), text_color=TH("txt2"),
            justify="left", anchor="w",
        ).pack(padx=12, pady=10, fill="x")

    def _info_box(self, parent, text: str, row: int):
        """Bloc d'info gris clair (remplace les vieilles cartes 'comment ça marche')."""
        box = ctk.CTkFrame(parent, fg_color=TH("bg"), corner_radius=8)
        box.grid(row=row, column=0, sticky="ew", padx=16, pady=(4, 10))
        ctk.CTkLabel(
            box, text=text,
            font=self._font(10), text_color=TH("txt2"),
            justify="left", anchor="w", wraplength=700,
        ).pack(padx=14, pady=10, fill="x")

    def _set_badge(self, badge, state: str, msg: str = ""):
        colors = {"ok": TH("ok"), "err": TH("err"), "run": TH("accent"),
                  "warn": TH("warn"), "idle": TH("txt3")}
        icons  = {"ok": "✓", "err": "✗", "run": "⟳", "warn": "⚠", "idle": ""}
        badge.configure(
            text=f"{icons.get(state,'')}  {msg}".strip() if msg else icons.get(state,""),
            text_color=colors.get(state, TH("txt3")),
        )

    # ── Log ───────────────────────────────────────────────────────────────────

    def log(self, msg: str, level: str = "info"):
        self._log_box.configure(state="normal")
        self._log_box.insert("end", msg + "\n", level)
        self._log_box.see("end")
        self._log_box.configure(state="disabled")
        self._log_box.update_idletasks()

    def _clear_log(self):
        self._log_box.configure(state="normal")
        self._log_box.delete("1.0", "end")
        self._log_box.configure(state="disabled")

    def _copy_log(self):
        content = self._log_box.get("1.0", "end").strip()
        self.clipboard_clear()
        self.clipboard_append(content)

    # ── Thread ────────────────────────────────────────────────────────────────

    def _run(self, fn):
        def wrapper():
            try:
                fn()
            except Exception as e:
                import traceback
                self.log(f"Erreur inattendue : {e}", "err")
                self.log(traceback.format_exc(), "err")
                self.after(0, lambda: messagebox.showerror(T("e_title"), str(e)))
        threading.Thread(target=wrapper, daemon=True).start()

    # ═════════════════════════════════════════════════════════════════════════
    #  ONGLETS
    # ═════════════════════════════════════════════════════════════════════════

    # ── ① Extraction ──────────────────────────────────────────────────────────

    def _build_tab_extract(self):
        tab = self._tabs.tab(T("tab_extract"))
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(0, weight=1)
        sc = self._scroll_frame(tab)
        sc.grid(row=0, column=0, sticky="nsew", padx=0, pady=8)
        sc.grid_columnconfigure(0, weight=1)

        # A ─ ISO → CPK
        cA = self._card(sc, T("a_title"), 0, "A")
        self._v_iso = tk.StringVar()
        self._path_row(cA, T("a_iso"), self._v_iso,
            lambda: self._v_iso.set(
                filedialog.askopenfilename(filetypes=[("ISO","*.iso *.ISO"),("Tous","*.*")])
                or self._v_iso.get()),
            row=1, tooltip=T("a_tip"))
        self._note(cA, T("a_note"), 2)
        _, self._b_cpk = self._action_btn(cA, T("a_btn"), self._do_cpk, row=3)

        # B ─ CriFsLib
        cB = self._card(sc, T("b_title"), 1, "B")

        # Chemin exe
        row_exe = ctk.CTkFrame(cB, fg_color="transparent")
        row_exe.grid(row=1, column=0, sticky="ew", padx=16, pady=(2, 4))
        row_exe.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(row_exe, text=T("b_exe"), width=175, anchor="w",
                     font=self._font(10), text_color=TH("txt2")).grid(row=0, column=0, padx=(0,8))
        ctk.CTkEntry(row_exe, textvariable=self._crifsl,
                     font=self._font(10, mono=True),
                     fg_color=TH("bg"), text_color=TH("txt"),
                     border_color=TH("border"), border_width=1,
                     corner_radius=6, height=30
                     ).grid(row=0, column=1, sticky="ew", padx=(0,6))
        ctk.CTkButton(row_exe, text="📂", width=34, height=30, corner_radius=6,
                      font=self._font(13),
                      fg_color=TH("btn_sec"), hover_color=TH("btn_sec_hov"),
                      text_color=TH("txt"), border_width=0,
                      command=lambda: self._crifsl.set(
                          filedialog.askopenfilename(filetypes=[("EXE","*.exe"),("Tous","*.*")])
                          or self._crifsl.get())
                      ).grid(row=0, column=2)

        # Bouton téléchargement CriFsLib
        dl_row = ctk.CTkFrame(cB, fg_color="transparent")
        dl_row.grid(row=2, column=0, sticky="w", padx=16, pady=(0, 4))
        dl_btn = ctk.CTkButton(
            dl_row, text=T("b_dl_btn"),
            width=200, height=28, corner_radius=6,
            font=self._font(10),
            fg_color=TH("btn_sec"), hover_color=TH("btn_sec_hov"),
            text_color=TH("accent"), border_width=0,
            command=self._do_dl_crifsl,
        )
        dl_btn.pack(side="left")
        Tooltip(dl_btn, "https://github.com/Sewer56/CriFsV2Lib/releases/tag/2.1.2")

        self._instr_box(cB, T("b_instr"), 3)

        # Bouton ouvrir + bouton "Ouvrir cpk_files/"
        btn_row = ctk.CTkFrame(cB, fg_color="transparent")
        btn_row.grid(row=4, column=0, sticky="w", padx=16, pady=(6, 14))

        self._b_crifsl_btn, self._b_crifsl = ctk.CTkButton(
            btn_row, text=T("b_btn"),
            font=self._font(11, "bold"),
            fg_color=TH("accent"), hover_color=TH("accent_hov"),
            text_color="#ffffff", height=38, corner_radius=8,
            command=self._do_crifsl,
        ), ctk.CTkLabel(btn_row, text="", font=self._font(10, mono=True),
                        text_color=TH("txt3"), width=140)
        self._b_crifsl_btn.pack(side="left")
        self._b_crifsl.pack(side="left", padx=(12,0))

        open_cpk_btn = ctk.CTkButton(
            btn_row, text="📁 cpk_files/",
            width=130, height=38, corner_radius=8,
            font=self._font(10),
            fg_color=TH("btn_sec"), hover_color=TH("btn_sec_hov"),
            text_color=TH("txt2"), border_width=0,
            command=self._open_cpk_files_dir,
        )
        open_cpk_btn.pack(side="left", padx=(10, 0))
        Tooltip(open_cpk_btn, "Ouvrir le dossier cpk_files/ dans l'explorateur" if _lang == "fr"
                else "Open cpk_files/ folder in file explorer")

        # C ─ CPK → event.bin
        cC = self._card(sc, T("c_title"), 2, "C")
        self._v_cpk = tk.StringVar(value=str(self.W / "P2PT_ALL.cpk"))
        self._path_row(cC, T("c_cpk"), self._v_cpk,
            lambda: self._v_cpk.set(
                filedialog.askopenfilename(filetypes=[("CPK","*.cpk"),("Tous","*.*")])
                or self._v_cpk.get()),
            row=1, tooltip=T("c_tip"))
        self._note(cC, T("c_note"), 2)
        _, self._b_event = self._action_btn(cC, T("c_btn"), self._do_event, row=3,
                                             tooltip=T("c_tip"))

        # D ─ event.bin → scripts
        cD = self._card(sc, T("d_title"), 3, "D")
        self._v_event = tk.StringVar(value=str(self.W / "event.bin"))
        self._path_row(cD, T("d_event"), self._v_event,
            lambda: self._v_event.set(
                filedialog.askopenfilename(filetypes=[("BIN","*.bin"),("Tous","*.*")])
                or self._v_event.get()),
            row=1, tooltip=T("d_tip"))
        self._note(cD, T("d_note"), 2)
        _, self._b_scripts = self._action_btn(cD, T("d_btn"), self._do_scripts, row=3,
                                               tooltip=T("d_tip"))

    # ── ② JSON + Scan ─────────────────────────────────────────────────────────

    def _build_tab_scan(self):
        tab = self._tabs.tab(T("tab_scan"))
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(0, weight=1)
        sc = self._scroll_frame(tab)
        sc.grid(row=0, column=0, sticky="nsew", padx=0, pady=8)
        sc.grid_columnconfigure(0, weight=1)

        # E ─ scripts → JSON
        cE = self._card(sc, T("e_title"), 0, "E")
        self._v_sbin  = tk.StringVar(value=str(self.W / "scripts_bin"))
        self._v_sjson = tk.StringVar(value=str(self.W / "traduction" / "event_scripts"))
        self._path_row(cE, T("e_src"), self._v_sbin,
            lambda: self._v_sbin.set(filedialog.askdirectory() or self._v_sbin.get()),
            row=1, tooltip=T("e_tip"))
        self._path_row(cE, T("e_out"), self._v_sjson,
            lambda: self._v_sjson.set(filedialog.askdirectory() or self._v_sjson.get()),
            row=2)
        self._tip(cE, T("e_tip"), 3)
        _, self._b_decode = self._action_btn(cE, T("e_btn"), self._do_decode, row=4,
                                              tooltip=T("e_tip"))

        # F ─ Scan BNP
        cF = self._card(sc, T("f_title"), 1, "F")
        self._v_cpkf = tk.StringVar(value=str(self.W / "cpk_files"))
        self._v_scan = tk.StringVar(value=str(self.W / "traduction"))
        self._path_row(cF, T("f_src"), self._v_cpkf,
            lambda: self._v_cpkf.set(filedialog.askdirectory() or self._v_cpkf.get()),
            row=1)
        self._path_row(cF, T("f_out"), self._v_scan,
            lambda: self._v_scan.set(filedialog.askdirectory() or self._v_scan.get()),
            row=2)

        # Légende fichiers
        leg = ctk.CTkFrame(cF, fg_color=TH("bg"), corner_radius=8)
        leg.grid(row=3, column=0, sticky="ew", padx=16, pady=(0, 6))
        for col_key, name, desc in [
            ("accent", "CD_SHOP.BIN",   T("f_f1")),
            ("warn",   "F_BE.BNP",      T("f_f2")),
            ("warn",   "TM_EVE.BNP",    T("f_f3")),
            ("accent", "MMAP01–06.BNP", T("f_f4")),
        ]:
            r = ctk.CTkFrame(leg, fg_color="transparent")
            r.pack(fill="x", padx=10, pady=3)
            ctk.CTkLabel(r, text="▸", font=self._font(10), text_color=TH(col_key),
                         width=16).pack(side="left")
            ctk.CTkLabel(r, text=name, font=self._font(10, "bold"),
                         text_color=TH("txt"), width=140, anchor="w"
                         ).pack(side="left", padx=(4, 6))
            ctk.CTkLabel(r, text=desc, font=self._font(9),
                         text_color=TH("txt2"), anchor="w", wraplength=420,
                         justify="left").pack(side="left")
        ctk.CTkLabel(leg, text="", height=4, fg_color="transparent").pack()

        self._pb_scan = self._progress(cF, 4)
        self._tip(cF, T("f_tip"), 5)
        _, self._b_scan = self._action_btn(cF, T("f_btn"), self._do_scan, row=6,
                                            tooltip=T("f_tip"))

        # G ─ Validation menus de choix
        cG = self._card(sc, T("v_title"), 2, "G")
        self._v_valid = tk.StringVar(value=str(self.W / "traduction" / "event_scripts"))
        self._path_row(cG, T("v_src"), self._v_valid,
            lambda: self._v_valid.set(filedialog.askdirectory() or self._v_valid.get()),
            row=1, tooltip=T("v_tip"))
        self._tip(cG, T("v_tip"), 2)
        self._pb_valid = self._progress(cG, 3)
        _, self._b_valid = self._action_btn(cG, T("v_btn"), self._do_validate, row=4,
                                             tooltip=T("v_tip"))

    # ── ③ Encodage ────────────────────────────────────────────────────────────

    def _build_tab_encode(self):
        tab = self._tabs.tab(T("tab_encode"))
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(0, weight=1)
        sc = self._scroll_frame(tab)
        sc.grid(row=0, column=0, sticky="nsew", padx=0, pady=8)
        sc.grid_columnconfigure(0, weight=1)

        cE = self._card(sc, T("enc_title"), 0)
        self._info_box(cE, T("enc_info"), 1)
        self._v_trad   = tk.StringVar(value=str(self.W / "traduction"))
        self._v_cpkenc = tk.StringVar(value=str(self.W / "cpk_files"))
        self._v_enc    = tk.StringVar(value=str(self.W / "encoded"))
        self._path_row(cE, T("enc_trad"), self._v_trad,
            lambda: self._v_trad.set(filedialog.askdirectory() or self._v_trad.get()), row=2)
        self._path_row(cE, T("enc_cpk"), self._v_cpkenc,
            lambda: self._v_cpkenc.set(filedialog.askdirectory() or self._v_cpkenc.get()), row=3)
        self._path_row(cE, T("enc_out"), self._v_enc,
            lambda: self._v_enc.set(filedialog.askdirectory() or self._v_enc.get()), row=4)
        self._pb_enc = self._progress(cE, 5)
        self._tip(cE, T("enc_tip"), 6)
        _, self._b_enc = self._action_btn(cE, T("enc_btn"), self._do_encode, row=7,
                                           tooltip=T("enc_tip"))

    # ── ④ Rebuild ISO ─────────────────────────────────────────────────────────

    def _build_tab_rebuild(self):
        tab = self._tabs.tab(T("tab_rebuild"))
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(0, weight=1)
        sc = self._scroll_frame(tab)
        sc.grid(row=0, column=0, sticky="nsew", padx=0, pady=8)
        sc.grid_columnconfigure(0, weight=1)

        cR = self._card(sc, T("rb_title"), 0)
        self._info_box(cR, T("rb_info"), 1)
        self._v_iso2   = tk.StringVar()
        self._v_encin  = tk.StringVar(value=str(self.W / "encoded"))
        self._v_outiso = tk.StringVar(value=str(self.W / "P2IS_FR.iso"))
        self._path_row(cR, T("rb_iso"), self._v_iso2,
            lambda: self._v_iso2.set(
                filedialog.askopenfilename(filetypes=[("ISO","*.iso *.ISO"),("Tous","*.*")])
                or self._v_iso2.get()),
            row=2, tooltip=T("rb_tip"))
        self._path_row(cR, T("rb_enc"), self._v_encin,
            lambda: self._v_encin.set(filedialog.askdirectory() or self._v_encin.get()), row=3)
        self._path_row(cR, T("rb_out"), self._v_outiso,
            lambda: self._v_outiso.set(
                filedialog.asksaveasfilename(
                    defaultextension=".iso", initialfile="P2IS_FR.iso",
                    filetypes=[("ISO","*.iso")])
                or self._v_outiso.get()),
            row=4)
        self._pb_rb = self._progress(cR, 5)
        self._tip(cR, T("rb_tip"), 6)
        _, self._b_rebuild = self._action_btn(cR, T("rb_btn"), self._do_rebuild, row=7,
                                               tooltip=T("rb_tip"))

    # ═════════════════════════════════════════════════════════════════════════
    #  CALLBACKS
    # ═════════════════════════════════════════════════════════════════════════

    def _open_cpk_files_dir(self):
        """Ouvre le dossier cpk_files/ dans l'explorateur de fichiers."""
        d = self.W / "cpk_files"
        d.mkdir(parents=True, exist_ok=True)
        if platform.system() == "Windows":
            os.startfile(str(d))
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", str(d)])
        else:
            subprocess.Popen(["xdg-open", str(d)])

    def _do_dl_crifsl(self):
        import webbrowser
        url = "https://github.com/Sewer56/CriFsV2Lib/releases/download/2.1.2/CriFsLib.GUI.zip"
        webbrowser.open(url)
        self.log(f"Téléchargement CriFsLib → {url}", "info")

    def _do_cpk(self):
        iso = self._v_iso.get()
        if not iso or not Path(iso).exists():
            messagebox.showwarning(T("w_title"), T("w_no_iso")); return
        def _w():
            self.after(0, lambda: self._set_badge(self._b_cpk, "run", T("running")))
            r = extract_cpk_from_iso(iso, self.W, self.log)
            self.after(0, lambda: self._v_cpk.set(r))
            sz = Path(r).stat().st_size // 1024 // 1024
            self.after(0, lambda: self._set_badge(self._b_cpk, "ok", f"{sz} MB"))
            self.after(0, lambda: messagebox.showinfo(T("ok_title"), T("ok_cpk", s=sz, p=r)))
        self._run(_w)

    def _do_crifsl(self):
        exe = self._crifsl.get()
        if not exe or not Path(exe).exists():
            messagebox.showwarning(T("w_title"), T("w_no_crifsl", p=exe)); return
        try:
            subprocess.Popen([exe])
            self._set_badge(self._b_crifsl, "ok", T("done_s"))
            self.log(T("log_crifsl1"), "ok")
            self.log(T("log_crifsl2"), "info")
            self.log(T("log_crifsl3", p=str(self.W / "cpk_files")), "info")
            messagebox.showinfo(T("ok_title"), T("ok_crifsl"))
        except Exception as e:
            messagebox.showerror(T("e_title"), str(e))
            self._set_badge(self._b_crifsl, "err", str(e)[:40])

    def _do_event(self):
        cpk = self._v_cpk.get()
        if not cpk or not Path(cpk).exists():
            messagebox.showwarning(T("w_title"), T("w_no_cpk")); return
        def _w():
            self.after(0, lambda: self._set_badge(self._b_event, "run", T("running")))
            self.W.mkdir(parents=True, exist_ok=True)
            r = extract_event_from_cpk(cpk, self.W, self.log)
            self.after(0, lambda: self._v_event.set(r))
            self.after(0, lambda: self._set_badge(self._b_event, "ok", T("done_s")))
            self.after(0, lambda: messagebox.showinfo(T("ok_title"), T("ok_event", p=r)))
        self._run(_w)

    def _do_scripts(self):
        ev = self._v_event.get()
        if not ev or not Path(ev).exists():
            messagebox.showwarning(T("w_title"), T("w_no_event")); return
        def _w():
            self.after(0, lambda: self._set_badge(self._b_scripts, "run", T("running")))
            out = self.W / "scripts_bin"
            out.mkdir(parents=True, exist_ok=True)
            n = extract_scripts_from_event(ev, out, self.log)
            self.after(0, lambda: self._v_sbin.set(str(out)))
            self.after(0, lambda: self._set_badge(self._b_scripts, "ok", f"{n} scripts"))
            self.after(0, lambda: messagebox.showinfo(T("ok_title"), T("ok_scripts", n=n, p=str(out))))
        self._run(_w)

    def _do_decode(self):
        src = self._v_sbin.get()
        dst = self._v_sjson.get()
        # Créer le dossier source s'il n'existe pas encore (évite le faux "Erreur")
        src_path = Path(src)
        if not src_path.exists():
            messagebox.showwarning(
                T("w_title"),
                (f"Le dossier scripts_bin/ est introuvable :\n{src}\n\n"
                 "Complète l'étape D d'abord.")
                if _lang == "fr" else
                (f"scripts_bin/ folder not found:\n{src}\n\n"
                 "Complete step D first.")
            ); return
        def _w():
            self.after(0, lambda: self._set_badge(self._b_decode, "run", T("running")))
            out = Path(dst)
            out.mkdir(parents=True, exist_ok=True)
            decode_all_scripts(src_path, out, self.log)
            self.after(0, lambda: self._set_badge(self._b_decode, "ok", T("done_s")))
            self.after(0, lambda: messagebox.showinfo(T("ok_title"), T("ok_decode", p=str(out))))
        self._run(_w)

    def _do_scan(self):
        cpkd = self._v_cpkf.get()
        if not Path(cpkd).is_dir():
            messagebox.showwarning(T("w_title"), T("w_no_cpkfiles")); return
        out = Path(self._v_scan.get())
        out.mkdir(parents=True, exist_ok=True)
        def _w():
            self.after(0, lambda: self._set_badge(self._b_scan, "run", T("running")))
            self.after(0, lambda: self._pb_scan.set(0))
            rep = scan_cpk_files(cpkd, out, self.log,
                                  lambda v: self.after(0, lambda v=v: self._pb_scan.set(v)))
            self.after(0, lambda: self._pb_scan.set(1.0))
            n = rep.get("total", 0)
            self.after(0, lambda: self._set_badge(self._b_scan, "ok", f"{n} dialogues"))
            self.after(0, lambda: messagebox.showinfo(T("ok_title"), T("ok_scan", n=n, p=str(out))))
        self._run(_w)

    def _do_validate(self):
        src = self._v_valid.get()
        src_path = Path(src)
        if not src_path.is_dir():
            messagebox.showwarning(
                T("w_title"),
                (f"Dossier event_scripts/ introuvable :\n{src}\n\nComplète l\'étape E d\'abord.")
                if _lang == "fr" else
                (f"event_scripts/ folder not found:\n{src}\n\nComplete step E first.")
            ); return
        def _w():
            self.after(0, lambda: self._set_badge(self._b_valid, "run", T("running")))
            self.after(0, lambda: self._pb_valid.set(0))
            result = validate_all_scripts(
                src,
                log_fn=self.log,
                progress_fn=lambda v: self.after(0, lambda v=v: self._pb_valid.set(v))
            )
            self.after(0, lambda: self._pb_valid.set(1.0))
            n = len(result.get("problems", []))
            f = result.get("files_with_issues", 0)
            if n == 0:
                self.after(0, lambda: self._set_badge(self._b_valid, "ok", T("v_ok")))
                self.after(0, lambda: messagebox.showinfo(T("ok_title"), T("v_ok")))
            else:
                self.after(0, lambda: self._set_badge(self._b_valid, "warn",
                    T("v_warn", n=n, f=f)))
                self.after(0, lambda: messagebox.showwarning(
                    T("w_title"), T("v_warn", n=n, f=f)))
        self._run(_w)

    def _do_encode(self):
        trad = self._v_trad.get(); cpk = self._v_cpkenc.get(); enc = self._v_enc.get()
        if not trad or not cpk or not enc:
            messagebox.showwarning(T("w_title"), T("w_fill_all")); return
        def _w():
            self.after(0, lambda: self._set_badge(self._b_enc, "run", T("running")))
            self.after(0, lambda: self._pb_enc.set(0))
            Path(enc).mkdir(parents=True, exist_ok=True)
            res = encode_all(trad, cpk, enc, self.log,
                              lambda v: self.after(0, lambda v=v: self._pb_enc.set(v)))
            self.after(0, lambda: self._pb_enc.set(1.0))
            ok_l = res.get("ok", []); err_l = res.get("err", [])
            self.after(0, lambda: self._set_badge(self._b_enc,
                "ok" if not err_l else "warn", f"{len(ok_l)} ok · {len(err_l)} err"))
            err_s = f"⚠ Erreurs : {', '.join(err_l)}\n\n" if err_l else ""
            self.after(0, lambda: messagebox.showinfo(
                T("ok_title"), T("ok_encode", n=len(ok_l), f=', '.join(ok_l), e=err_s, p=enc)))
        self._run(_w)

    def _do_rebuild(self):
        iso = self._v_iso2.get(); enc = self._v_encin.get(); out = self._v_outiso.get()
        if not iso or not enc or not out:
            messagebox.showwarning(T("w_title"), T("w_fill_all")); return
        if not Path(iso).exists():
            messagebox.showwarning(T("w_title"), T("w_no_iso2", p=iso)); return
        if not Path(enc).is_dir():
            messagebox.showwarning(T("w_title"), T("w_no_encoded", p=enc)); return
        ev_fr = Path(enc) / "event.bin"
        if not ev_fr.exists():
            messagebox.showwarning(T("w_title"), T("w_no_eventbin")); return
        def _w():
            self.after(0, lambda: self._set_badge(self._b_rebuild, "run", T("running")))
            self.after(0, lambda: self._pb_rb.set(0))
            ev_data = open(ev_fr, "rb").read()
            Path(out).parent.mkdir(parents=True, exist_ok=True)
            rebuild_iso(iso, ev_data, out, self.log)
            self.after(0, lambda: self._pb_rb.set(1.0))
            sz = Path(out).stat().st_size // 1024 // 1024
            self.after(0, lambda: self._set_badge(self._b_rebuild, "ok", f"{sz} MB"))
            self.after(0, lambda: messagebox.showinfo(
                T("ok_title"), T("ok_rebuild", s=sz, p=out)))
        self._run(_w)


# ── Point d'entrée ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = P2ISFRTool()
    app.mainloop()

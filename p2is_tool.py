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

import struct, json, gzip, io, os, re, shutil, threading, subprocess, platform, concurrent.futures
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


def crilayla_compress(data: bytes, header_size: int = 0, max_offset: int = 8191, target_size: int = 0, max_chain: int = 128) -> bytes:
    """
    Compresse des données au format CRILAYLA. Supporte les en-têtes non compressés
    exigés par certains moteurs de jeu (ex: 256 octets pour les MMAP de Persona 2).
    """
    if header_size > len(data): header_size = len(data)
    HEADER = header_size
    n = len(data)

    class BitWriter:
        """Émule l'ordre exact de consommation de crilayla_decompress."""
        def __init__(self):
            self.out = bytearray()
            self.pool = 0
            self.nbits = 0
            self.pending_literals = []

        def _flush_pending(self):
            while self.pending_literals:
                self.out.append(self.pending_literals.pop(0))

        def write_bit(self, b):
            self.pool = (self.pool << 1) | b
            self.nbits += 1
            if self.nbits == 8:
                self.out.append(self.pool)
                self.pool = 0; self.nbits = 0

        def write_bits(self, val, width):
            for i in range(width - 1, -1, -1):
                self.write_bit((val >> i) & 1)

        def finish(self):
            if self.nbits > 0:
                self.out.append(self.pool << (8 - self.nbits))
                self.nbits = 0
            return bytes(self.out)

    bw = BitWriter()
    wp = n
    MAX_CHAIN = max_chain
    hash_table = [[] for _ in range(65536)]

    def key_at(pos):
        if pos < 3: return None
        return (data[pos-1] << 8) | data[pos-2]

    def record_position(pos):
        k = key_at(pos)
        if k is not None:
            bucket = hash_table[k]
            bucket.append(pos)
            if len(bucket) > MAX_CHAIN: del bucket[0]

    def find_best_match(pos):
        best_len = 0; best_off = 0
        k = key_at(pos)
        if k is not None:
            tested = 0
            for ref in reversed(hash_table[k]):
                if ref <= pos: continue
                offset = ref - pos
                if offset < 3 or offset - 3 > max_offset: continue
                max_search_len = min(265, pos, ref)
                if max_search_len < 2: continue
                length = 0
                while (length < max_search_len and
                       data[pos - 1 - length] == data[ref - 1 - length]):
                    length += 1
                if length > best_len:
                    best_len = length; best_off = offset - 3
                    if best_len >= 265: break
                tested += 1
                if tested >= MAX_CHAIN: break
        return best_len, best_off

    while wp > HEADER:
        best_len, best_off = find_best_match(wp)
        if best_len >= 3 and wp - 1 > HEADER:
            next_len, next_off = find_best_match(wp - 1)
            if next_len > best_len + 1: best_len = 0
            elif best_len <= 9 and wp - 2 > HEADER:
                next2_len, _ = find_best_match(wp - 2)
                if next2_len > best_len + 2: best_len = 0
        if best_len == 3 and wp - 1 > HEADER:
            next_len, _ = find_best_match(wp - 1)
            if next_len >= 3: best_len = 0
        positions_covered = max(best_len, 1) if best_len >= 3 else 1
        for offset_back in range(positions_covered): record_position(wp - offset_back)
        if best_len >= 3:
            bw.write_bit(1)
            bw.write_bits(best_off, 13)
            
            rem = best_len - 3
            vle_lens = [2, 3, 5, 8]
            for vle_level in vle_lens:
                max_val = (1 << vle_level) - 1
                if rem < max_val:
                    bw.write_bits(rem, vle_level)
                    break
                else:
                    bw.write_bits(max_val, vle_level)
                    rem -= max_val
            else:
                while True:
                    if rem < 255:
                        bw.write_bits(rem, 8)
                        break
                    else:
                        bw.write_bits(255, 8)
                        rem -= 255
                        
            wp -= best_len
        else:
            bw.write_bit(0)
            wp -= 1
            bw.write_bits(data[wp], 8)

    compressed = bw.finish()
    stored = compressed[::-1]
    header_bytes = data[:HEADER]
    
    pad = b''
    csz = len(stored)
    if target_size > 0:
        current_size = 16 + len(stored) + len(header_bytes)
        if current_size < target_size:
            pad = b'\x00' * (target_size - current_size)
            csz += len(pad)

    # Format CRI PSP : CRILAYLA + unc + csz + pad + stored (bitstream) + header_bytes
    return b'CRILAYLA' + struct.pack("<I", n - HEADER) + struct.pack("<I", csz) + pad + stored + header_bytes




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



def _decode_single_script(idx, scripts_dir, output_dir, log_fn):
    bf = scripts_dir / f"script_{idx:03d}.bin"
    if not bf.exists(): bf = scripts_dir / f"script_{idx}.bin"
    if not bf.exists(): return None
    
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
        
    if idx % 50 == 0 and log_fn:
        log_fn(f"  script_{idx:03d} → {len(dlgs)} dialogues", "info")
        
    return len(dlgs)


def decode_all_scripts(scripts_dir: Path, output_dir: Path, log_fn):
    """Décode tous les scripts_bin/*.bin en fichiers JSON prêts à traduire."""
    output_dir.mkdir(parents=True, exist_ok=True)
    total = vides = 0
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(_decode_single_script, idx, scripts_dir, output_dir, log_fn) for idx in range(399)]
        
        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            if res is not None:
                total += 1
                if res == 0:
                    vides += 1

    if log_fn: log_fn(f"  {total} scripts décodés ({vides} vides) via ThreadPool", "ok")



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


def _needs_nl_suffix(term: list, texte_orig: str) -> bool:
    """
    Détermine si un NL (0x1101) doit être inséré entre le texte encodé
    et le terminateur dans le slot binaire.

    Règle observée sur event scripts et MMAP01-06 :
    - E3 (0x1103) absent du terminateur → NL requis  (slots narratifs courts)
    - Menu de choix [1208] → NL requis  (sentinel de fin de menu)
    - E3 présent ET pas de menu → pas de NL  (slots avec E1 E2 E3 E4)
    """
    E3 = 0x1103
    is_menu = '[1208]' in texte_orig or '[U+1208]' in texte_orig
    return E3 not in term or is_menu


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
    dlgs  = json.loads(open(json_path, encoding="utf-8").read(), strict=False)
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

        avail = d["data_size"] - 8
        # NL avant terminateur : règle binaire universelle (event + MMAP + autres)
        term = d.get("_term", [E1,E2,E3,E4])
        nl_suffix = struct.pack("<H", NL) if _needs_nl_suffix(
            term, d.get("texte_orig","")
        ) else b""
        # Aligner AVANT d'encoder (on a besoin d'avail pour le test d'alignement)
        enc_pre = text_to_bytes('"' + n_fr + "\n" + t_fr)
        t_fr_aligned = _align_menu_text(
            d.get("nom_orig", ""), d.get("texte_orig", ""),
            n_fr, t_fr
        )
        enc_aligned = text_to_bytes('"' + n_fr + "\n" + t_fr_aligned)
        if len(enc_aligned) + len(nl_suffix) <= avail:
            enc = enc_aligned
        else:
            # Alignement impossible → garder sans align, warn si menu
            enc = enc_pre
            if '[1208]' in t_fr or '[U+1208]' in t_fr:
                marker = '[U+1208]' if '[U+1208]' in t_fr else '[1208]'
                pre_fr = text_to_bytes('"' + n_fr + "\n" + t_fr.split(marker)[0])
                pre_or = text_to_bytes('"' + d.get("nom_orig","").replace('[SP]',' ') + "\n" + d.get("texte_orig","").split('[1208]')[0])
                if len(pre_fr) > len(pre_or) and log_fn:
                    log_fn(f"  ⚠ [id {d['id']}] question FR trop longue de {(len(pre_fr)-len(pre_or))//2} mot(s) → alignement désactivé.", "warn")
        if len(enc) + len(nl_suffix) > avail:
            depassement = len(enc) + len(nl_suffix) - avail
            if log_fn: log_fn(f"  [!] [DEPASSEMENT] [id {d['id']}] Texte FR trop long de {depassement} octets ({len(enc)} > {avail}). Texte ignore et version originale restauree.","warn")
            skip += 1; continue
        pad_count = (avail - len(enc) - len(nl_suffix)) // 2
        
        # RETOUR AUX SOURCES : PADDING ESPACES INVISIBLES
        # C'est la seule méthode qui ne casse ni le jeu, ni les choix (pas de ").
        # Le moteur de script ne le verra jamais.
        ghost_pad = b'\x20\x11' * pad_count
        
        end_c = b"".join(struct.pack("<H", t) for t in term)
        null_gap_orig = data[d["offset"]+d["data_size"] : d["offset"]+d["slot_size"]]
        
        full = enc + ghost_pad + nl_suffix + end_c + null_gap_orig
        
        if len(full) != d["slot_size"]: skip += 1; continue
        data[d["offset"]:d["offset"]+d["slot_size"]] = full
        ok += 1
    if out_path is None: out_path = bin_path
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    with open(out_path,"wb") as f: f.write(data)
    if log_fn: log_fn(f"  [RESUME] {Path(out_path).name} : {ok} injectes avec succes, {skip} rejetes (trop longs), {kept} laisses en japonais.","ok")
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

def _parse_cpk_utf(data: bytes, offset: int) -> list:
    """Parse une table @UTF du CPK CRI (big-endian, header 32 bytes)."""
    if len(data) < offset + 32 or data[offset:offset+4] != b'@UTF':
        return []
    try:
        base        = offset + 8  # base pour rows/strings/data offsets
        rows_off    = struct.unpack_from('>I', data, offset+0x08)[0]
        strings_off = struct.unpack_from('>I', data, offset+0x0C)[0]
        data_off    = struct.unpack_from('>I', data, offset+0x10)[0]
        num_cols    = struct.unpack_from('>H', data, offset+0x18)[0]
        row_stride  = struct.unpack_from('>H', data, offset+0x1A)[0]
        num_rows    = struct.unpack_from('>I', data, offset+0x1C)[0]
        str_base    = base + strings_off
        data_base   = base + data_off

        def read_str(pos):
            s = b''
            while pos < len(data) and data[pos]: s += bytes([data[pos]]); pos += 1
            return s.decode('utf-8', 'replace')

        def read_val(p, ftype):
            if ftype == 0x00: return data[p] if p < len(data) else 0, p+1
            if ftype == 0x01: return struct.unpack_from('>b', data, p)[0], p+1
            if ftype == 0x02: return struct.unpack_from('>H', data, p)[0], p+2
            if ftype == 0x03: return struct.unpack_from('>h', data, p)[0], p+2
            if ftype == 0x04: return struct.unpack_from('>I', data, p)[0], p+4
            if ftype == 0x05: return struct.unpack_from('>i', data, p)[0], p+4
            if ftype == 0x06: return struct.unpack_from('>Q', data, p)[0], p+8
            if ftype == 0x07: return struct.unpack_from('>q', data, p)[0], p+8
            if ftype == 0x08: return struct.unpack_from('>f', data, p)[0], p+4
            if ftype == 0x0A:
                soff = struct.unpack_from('>I', data, p)[0]; p += 4
                return read_str(str_base + soff), p
            if ftype == 0x0B:
                doff  = struct.unpack_from('>I', data, p)[0]
                dsize = struct.unpack_from('>I', data, p+4)[0]
                return None, p+8
            return None, p

        fields = []; fp = offset + 0x20
        for _ in range(num_cols):
            if fp + 5 > len(data): break
            flags = data[fp]; fp += 1
            name_soff = struct.unpack_from('>I', data, fp)[0]; fp += 4
            name  = read_str(str_base + name_soff)
            ftype   = flags & 0x0F
            storage = (flags >> 4) & 0x0F
            default = None
            if storage == 1:  # valeur constante (pas de données dans la row)
                default, fp = read_val(fp, ftype)
            fields.append((name, ftype, storage, default))

        rows = []; rows_start = base + rows_off
        for i in range(num_rows):
            rp = rows_start + i * row_stride if row_stride else rows_start
            row = {}
            for name, ftype, storage, default in fields:
                if storage == 1:   row[name] = default
                elif storage in (3, 5):
                    val, rp = read_val(rp, ftype)
                    row[name] = val
            rows.append(row)
        return rows
    except Exception:
        return []


def _read_cpk_header(data: bytes, cpk_off: int = 0) -> dict:
    """Lit ContentOffset, TocOffset, TocSize depuis le CpkHeader @UTF."""
    if len(data) < cpk_off + 0x30 or data[cpk_off:cpk_off+4] != b'CPK ':
        return {}
    utf_off = cpk_off + 0x10
    if data[utf_off:utf_off+4] != b'@UTF':
        return {}
    try:
        base     = utf_off + 8
        rows_off = struct.unpack_from('>I', data, utf_off + 0x08)[0]
        row_base = base + rows_off
        if row_base + 40 > len(data):
            return {}
        content_off = struct.unpack_from('>Q', data, row_base + 8)[0]
        content_sz  = struct.unpack_from('>Q', data, row_base + 16)[0]
        toc_off     = struct.unpack_from('>Q', data, row_base + 24)[0]
        toc_sz      = struct.unpack_from('>Q', data, row_base + 32)[0]
        return {
            'ContentOffset': content_off,
            'ContentSize':   content_sz,
            'TocOffset':     toc_off,
            'TocSize':       toc_sz,
        }
    except Exception:
        return {}


def _find_bnp_offsets_in_iso(iso_path: str, cpk_dir: Path, targets: set,
                              cpk_offset_in_iso: int) -> dict:
    """Cherche chaque BNP dans l'ISO directement par ses bytes caractéristiques."""
    if not iso_path or not Path(iso_path).exists():
        return {}
    result = {}
    fmap = {f.name.lower(): f for f in cpk_dir.rglob("*") if f.is_file()}
    try:
        with open(iso_path, "rb") as iso_f:
            iso_f.seek(0, 2); iso_size = iso_f.tell()
            search_start = cpk_offset_in_iso
            search_end   = iso_size
            iso_f.seek(search_start)
            cpk_data = iso_f.read(search_end - search_start)
    except Exception:
        return {}
    used_positions = set()
    for tname in targets:
        fp = fmap.get(tname)
        if not fp: continue
        try:
            raw = open(fp, "rb").read()
        except Exception:
            continue
        signature = raw[:128]
        check_off = min(4096, len(raw) - 64)
        check_sig = raw[check_off:check_off+64] if check_off > 0 else b""
        pos = -1
        search_from = 0
        while True:
            candidate = cpk_data.find(signature, search_from)
            if candidate == -1:
                break
            if candidate not in used_positions:
                if check_sig and check_off > 0:
                    if cpk_data[candidate+check_off:candidate+check_off+64] == check_sig:
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
    if len(toc_data) < toc_utf_off + 0x20 or toc_data[toc_utf_off:toc_utf_off+4] != b'@UTF':
        return []
    try:
        base        = toc_utf_off + 8
        rows_off    = struct.unpack_from('>I', toc_data, toc_utf_off+0x08)[0]
        strings_off = struct.unpack_from('>I', toc_data, toc_utf_off+0x0C)[0]
        row_stride  = struct.unpack_from('>H', toc_data, toc_utf_off+0x1A)[0]
        num_rows    = struct.unpack_from('>I', toc_data, toc_utf_off+0x1C)[0]
        str_base    = base + strings_off
        rows_start  = base + rows_off

        def read_str(pos):
            s = b''
            while pos < len(toc_data) and toc_data[pos]:
                s += bytes([toc_data[pos]]); pos += 1
            return s.decode('utf-8', 'replace')

        results = []
        for i in range(num_rows):
            rp = rows_start + i * row_stride
            if rp + 20 > len(toc_data):
                break
            name_off  = struct.unpack_from('>I', toc_data, rp)[0]
            file_size = struct.unpack_from('>I', toc_data, rp+4)[0]
            ext_size  = struct.unpack_from('>I', toc_data, rp+8)[0]
            file_off  = struct.unpack_from('>I', toc_data, rp+16)[0]
            fname = read_str(str_base + name_off)
            results.append({
                'FileName': fname,
                'FileOffset': file_off,
                'FileSize': file_size,
                'ExtractSize': ext_size,
                'RowOffset': rp,
            })
        return results
    except Exception:
        return []


def _find_bnp_offsets_in_cpk(cpk_path: Path, targets: set, cpk_offset_in_iso: int) -> dict:
    """Parse la table TOC du CPK pour trouver les offsets des BNP."""
    if not cpk_path.exists():
        return {}
    try:
        with open(cpk_path, "rb") as f:
            header = f.read(512)
        if header[:4] != b'CPK ':
            return {}
        hdr_info = _read_cpk_header(header, 0)
        toc_off = hdr_info.get('TocOffset')
        toc_size = hdr_info.get('TocSize')
        content_off = hdr_info.get('ContentOffset', 0) or 0
        if not toc_off or not toc_size:
            return {}
        with open(cpk_path, "rb") as f:
            f.seek(int(toc_off))
            toc_data = f.read(int(toc_size) + 64)
        toc_utf_off = None
        for probe in (16, 0, 8):
            if len(toc_data) > probe + 4 and toc_data[probe:probe+4] == b'@UTF':
                toc_utf_off = probe; break
        if toc_utf_off is None:
            return {}
        toc_rows = _parse_cpk_toc_rows(toc_data, toc_utf_off)
        result = {}
        for row in toc_rows:
            fname = (row.get('FileName') or '').lower()
            if fname in targets:
                file_off  = row.get('FileOffset')
                file_size = row.get('FileSize')
                ext_size  = row.get('ExtractSize')
                rp        = row.get('RowOffset')
                if file_off is None or file_size is None or ext_size is None:
                    continue
                abs_iso_off = cpk_offset_in_iso + 0x3800 + file_off
                result[fname] = {
                    "offset_in_cpk": 0x3800 + file_off,
                    "offset_in_iso": abs_iso_off,
                    "size": ext_size,
                    "stored_size": file_size,
                    "toc_row_iso_off": cpk_offset_in_iso + int(toc_off) + rp
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


def scan_cpk_files(cpk_dir_str: str, out_dir: Path, log_fn=None, progress_fn=None) -> dict:
    """Scanne les fichiers cibles dans cpk_files/ et extrait leurs dialogues en JSON."""
    cpk_dir = Path(cpk_dir_str); out_dir.mkdir(parents=True, exist_ok=True)
    targets = sorted(SCAN_TARGETS)
    fmap = {f.name.lower(): f for f in Path(cpk_dir_str).rglob("*") if f.is_file()}
    if log_fn: log_fn("Scan des fichiers de jeu…","head")
    total = []; done = []
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
        bnp_offsets = _find_bnp_offsets_in_cpk(cpk_path, set(targets), cpk_offset_in_iso)
    if not bnp_offsets:
        iso_path_str = offs.get("iso_path", "")
        bnp_offsets = _find_bnp_offsets_in_iso(iso_path_str, cpk_dir, set(targets), cpk_offset_in_iso)
    for i, tname in enumerate(targets):
        if progress_fn: progress_fn((i+1)/len(targets))
        fp = fmap.get(tname)
        if not fp: continue
        try: raw = open(fp,"rb").read()
        except: continue
        n = scan_bnp_bin(raw, fp.stem, out_dir, log_fn)
        total.append(n)
        if n > 0: done.append(tname)
    if bnp_offsets:
        offs["bnp_offsets"] = bnp_offsets
        save_offsets(offs)
    if log_fn: log_fn(f"  Total : {sum(total)} dialogues dans {len(done)} fichiers","ok")
    return {"total": sum(total), "files": done}


# ── Rebuild event.bin ─────────────────────────────────────────────────────────

def rebuild_event_bin(orig_event: bytes, scripts_fr_dir: Path, log_fn,
                      scripts_bin_dir: Path = None) -> bytes:
    """Réinjecte les scripts traduits dans event.bin."""
    event = bytearray(orig_event); toc = []; i = 0
    while i+8 <= len(event):
        s = struct.unpack_from("<I",event,i)[0]; e = struct.unpack_from("<I",event,i+4)[0]
        if s == 0: break
        toc.append((s,e,i)); i += 8
    patched = kept_orig = 0
    for idx,(start,end,tp) in enumerate(toc):
        fr = scripts_fr_dir / f"script_{idx:03d}_fr.bin"
        if not fr.exists(): fr = scripts_fr_dir / f"script_{idx}_fr.bin"
        if fr.exists():
            sc = open(fr,"rb").read()
        elif scripts_bin_dir is not None:
            orig = scripts_bin_dir / f"script_{idx:03d}.bin"
            if not orig.exists(): orig = scripts_bin_dir / f"script_{idx}.bin"
            if orig.exists():
                sc = open(orig,"rb").read()
                kept_orig += 1
            else: continue
        else: continue
        gz_buf = io.BytesIO()
        with gzip.GzipFile(filename=b"e0000.bin",mode="wb",fileobj=gz_buf,mtime=0) as gz: gz.write(sc)
        new_gz = gz_buf.getvalue()
        if len(new_gz) > end-start: continue
        event[start:start+len(new_gz)] = new_gz
        event[start+len(new_gz):end]   = bytes((end-start)-len(new_gz))
        # Ne PAS modifier l'index de fin (tp+4) ! Le jeu a besoin que end - start
        # corresponde exactement à l'espace mémoire alloué, même s'il y a du padding !
        patched += 1
    return bytes(event)


# ── Rebuild ISO ───────────────────────────────────────────────────────────────


def update_iso_metadata(f, cpk_offset, new_end_offset, log_fn):
    """
    Hack de la taille de l'ISO et du CPK pour autoriser la lecture au-delà de la limite officielle.
    """
    if log_fn: log_fn("  [HACK] Application du hack ISO9660 et CPK Header...", "info")
    import struct
    try:
        new_size = new_end_offset - cpk_offset
        
        # 1. Le CPK Header n'a PAS besoin d'etre patche !
        # Le jeu lit sans probleme au-dela de sa propre ContentSize.
        # Patch ContentSize, EnabledPackedSize, ou EnabledDataSize fait saturer la RAM de la PSP et freeze au logo !

        # 2. Update Primary Volume Descriptor (PVD)
        f.seek(16 * 2048)
        pvd = bytearray(f.read(2048))
        if pvd[:7] == b'\x01CD001\x01':
            sectors = (new_end_offset + 2047) // 2048
            pvd[80:88] = struct.pack('<I', sectors) + struct.pack('>I', sectors)
            f.seek(16 * 2048)
            f.write(pvd)
        else:
            if log_fn: log_fn("  [ERREUR] PVD ISO9660 introuvable.", "err")

        # 3. Update Directory Entry for P2PT_ALL.CPK
        f.seek(0)
        iso_start = bytearray(f.read(2 * 1024 * 1024))
        iso_start_lower = bytearray(iso_start).lower()
        pos = 0
        found = 0
        while True:
            pos = iso_start_lower.find(b'p2pt_all.cpk', pos)
            if pos == -1: break
            rec_start = pos - 33
            if rec_start >= 0:
                rec_len = iso_start[rec_start]
                if rec_len >= 34:
                    f.seek(rec_start + 10)
                    f.write(struct.pack('<I', new_size))
                    f.write(struct.pack('>I', new_size))
                    found += 1
            pos += 1
        if found > 0:
            if log_fn: log_fn(f"  [TOC PATCH] Limites ISO/CPK etendues virtuellement a {new_size//1024//1024} MB ({found} entrees) avec succes !", "ok")
        else:
            if log_fn: log_fn("  [ERREUR] Entree ISO9660 P2PT_ALL.CPK introuvable.", "err")

    except Exception as e:
        if log_fn: log_fn(f"  [ERREUR CRITIQUE] Echec du hack ISO9660: {e}", "err")

def rebuild_iso(iso_orig: str, event_data: bytes, out_iso: str, log_fn,
                enc_dir: str = None) -> bool:
    """Patche event.bin ET les BNP traduits."""
    offs = load_offsets(); pos = offs.get("event_offset_in_iso",-1)
    if pos != -1:
        with open(iso_orig,"rb") as f:
            f.seek(pos); chk = struct.unpack("<I",f.read(4))[0]
        if chk != 0x1000:
            if log_fn: log_fn(f"  Offset mémorisé invalide (0x{chk:x}), re-extraction nécessaire.","warn")
            pos = -1
    if pos == -1:
        raise Exception("Offset event.bin inconnu.\n→ Relance les étapes A, B, C pour le recalculer.")
    max_iso_offset = 0
    shutil.copy(iso_orig, out_iso)
    with open(out_iso,"r+b") as f:
        if log_fn: log_fn(f"  event.bin → offset 0x{pos:08X}","info")
        f.seek(pos); f.write(event_data)
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
                Path(iso_orig_path).parent / "P2PT_ALL.cpk" if iso_orig_path else Path("nonexistent"),
            ]
            cpk_path = next((p for p in cpk_candidates if p.exists()), None)
            if cpk_path:
                bnp_offsets = _find_bnp_offsets_in_cpk(cpk_path, set(SCAN_TARGETS), cpk_off_in_iso)
            if not bnp_offsets:
                cpk_files_dir = next((p for p in [work_dir / "cpk_files", Path(enc_dir) / "cpk_files"] if p.exists()), work_dir)
                bnp_offsets = _find_bnp_offsets_in_iso(iso_orig_path, cpk_files_dir, set(SCAN_TARGETS), cpk_off_in_iso)
        if bnp_offsets:
            offs["bnp_offsets"] = bnp_offsets
            save_offsets(offs)
            if log_fn: log_fn(f"  {len(bnp_offsets)} BNP localisés ✓","info")
        else:
            if log_fn: log_fn("  ⚠ BNP introuvables dans l'ISO — MMAP/F_BE non injectés","warn")
        if enc_dir and bnp_offsets:
            enc = Path(enc_dir)
            bnp_files = [
                ("CD_SHOP.BIN", "cd_shop.bin"),
                ("F_BE.BNP",    "f_be.bnp"),
                ("TM_EVE.BNP",  "tm_eve.bnp"),
                ("MMAP01.BNP",  "mmap01.bnp"),
                ("MMAP02.BNP",  "mmap02.bnp"),
                ("MMAP03.BNP",  "mmap03.bnp"),
                ("MMAP04.BNP",  "mmap04.bnp"),
                ("MMAP05.BNP",  "mmap05.bnp"),
                ("MMAP06.BNP",  "mmap06.bnp"),
            ]
            for fn_enc, fn_key in bnp_files:
                enc_path = enc / fn_enc
                if not enc_path.exists():
                    continue
                meta = bnp_offsets.get(fn_key) or bnp_offsets.get(fn_key.upper())
                if not meta:
                    if log_fn: log_fn(f"  ⚠ {fn_enc} : offset introuvable dans la TOC","warn")
                    continue
                iso_off = meta["offset_in_iso"]
                extract_size = meta["size"]          # taille réelle décompressée attendue
                stored_size  = meta.get("stored_size", extract_size)  # espace réellement alloué dans le CPK
                new_data = open(enc_path,"rb").read()

                # HACK SALVATEUR : On désactive la recompression CRILAYLA expérimentale qui corrompt le jeu.
                # Si le fichier original était compressé, on va forcer le moteur du jeu (CRI) à le lire 
                # en format non-compressé (BRUT) en écrivant FileSize == ExtractSize dans la TOC.
                needs_compression = stored_size < extract_size
                if needs_compression:
                    if len(new_data) != extract_size:
                        if log_fn: log_fn(
                            f"  ⚠ {fn_enc} : taille décodée ({len(new_data)}) ≠ "
                            f"taille attendue ({extract_size}), ignoré","warn")
                        continue
                    if log_fn: log_fn(f"  [INFO] Traitement de {fn_enc} sans recompression...","info")
                    
                    compressed = new_data  # Pas de compression ! On garde les données brutes.
                    
                    if len(compressed) > stored_size:
                        if log_fn: log_fn(f"  [+] [TOC PATCH] {fn_enc} est trop volumineux ({len(compressed)} > {stored_size}), deplacement a la FIN de l'ISO !", "ok")
                        f.seek(0, 2) # EOF
                        padding = (2048 - (f.tell() % 2048)) % 2048
                        if padding: f.write(b'\x00' * padding)
                        
                        iso_off = f.tell() # NOUVEL OFFSET DE FIN
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
                            rows_off = struct.unpack_from('>I', cpk_header, utf_off + 0x08)[0]
                            row_base = base + rows_off
                            old_content_size = struct.unpack_from('>Q', cpk_header, row_base + 16)[0]
                            
                            if new_content_size > old_content_size:
                                f.seek(cpk_off_in_iso + row_base + 16)
                                f.write(struct.pack(">Q", new_content_size))
                                if log_fn: log_fn(f"  [+] [TOC PATCH] ContentSize reculé de {old_content_size//1024//1024}MB à {new_content_size//1024//1024}MB", "ok")

                        stored_size = len(compressed) # On leve la limite pour la suite du script
                        max_iso_offset = max(max_iso_offset, iso_off + stored_size)
                        
                    # IMPORTANT: On ne padde plus ! On écrit le flux compressé nu.
                    # Le padding causait un crash sur console à cause du bounds check strict.
                    write_data = compressed
                else:
                    if len(new_data) > stored_size:
                        if log_fn: log_fn(
                            f"  ⚠ {fn_enc} trop grand ({len(new_data)} > {stored_size}), ignoré","warn")
                        continue
                    write_data = new_data

                f.seek(iso_off)
                f.write(write_data)
                
                # Fichiers non compressés ou trop courts : on nettoie les restes avec des zéros
                # (uniquement derrière le fichier, là où le jeu ne les lira pas)
                if len(write_data) < stored_size:
                    f.write(b'\x00' * (stored_size - len(write_data)))

                # MAGIE NOIRE : Mise à jour de la TOC de l'ISO en direct
                # Si on a l'offset exact de la taille du fichier dans la TOC
                toc_row_off = meta.get("toc_row_iso_off")
                if toc_row_off:
                    f.seek(toc_row_off + 4)  # FileSize
                    f.write(struct.pack(">I", len(write_data)))
                    f.seek(toc_row_off + 8)  # ExtractSize
                    f.write(struct.pack(">I", len(new_data)))
                    
                    if log_fn: log_fn(f"  [TOC] Mise a jour de la table a l'adresse 0x{toc_row_off:08X} (Nouveau FileSize: {len(write_data)}, ExtractSize: {len(new_data)})", "info")
                if log_fn: log_fn(f"  [>] INJECTION de {fn_enc} -> offset 0x{iso_off:08X} ({len(write_data)} / {stored_size} bytes) terminee.","info")
                
        if max_iso_offset > 0:
            f.seek(0, 2)
            rem = f.tell() % 2048
            if rem != 0:
                f.write(b'\x00' * (2048 - rem))
            update_iso_metadata(f, cpk_off_in_iso, f.tell(), log_fn)

    sz = Path(out_iso).stat().st_size // 1024 // 1024
    if log_fn: log_fn(f"  [V] ISO modifiee generee avec succes : {out_iso} ({sz} MB)","ok")
    return True



# ── Encodage BNP (MMAP01-06, CD_SHOP) ────────────────────────────────────────

def encode_bnp_from_json(bin_path: str, json_path: str, log_fn, out_path: str = None) -> str:
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
    direct = []   # pas de _source : offset direct dans BNP
    by_gz  = {}   # "gz@0xXXXX" → liste d'entrées

    for d in dlgs:
        src = d.get("_source", "")
        if src.startswith("gz@"):
            by_gz.setdefault(src, []).append(d)
        else:
            direct.append(d)

    ok = skip = kept = 0

    # ── 1. Entrées directes (même logique que encode_bin_from_json) ───────────
    for d in direct:
        n_fr = d.get("nom_fr","").strip(); t_fr = d.get("texte_fr","").strip()
        choix_fr = d.get("choix_fr"); q_fr = d.get("question_fr","").strip()
        if choix_fr is not None:
            filled = [c for c in choix_fr if c.strip()]
            if q_fr and filled:
                t_fr = _rebuild_choice_body(q_fr, choix_fr)
            elif not t_fr:
                kept += 1; continue
        elif not n_fr and not t_fr:
            kept += 1; continue
        t_fr = _align_menu_text(d.get("nom_orig",""), d.get("texte_orig",""), n_fr, t_fr)
        enc = text_to_bytes('"' + n_fr + "\n" + t_fr)
        avail = d["data_size"] - 8
        is_menu = '[1208]' in d.get("texte_orig","") or '[U+1208]' in d.get("texte_orig","")
        nl_sfx = struct.pack("<H", NL) if is_menu else b""
        
        # TRONCATURE AUTOMATIQUE si le texte FR est trop long
        if len(enc) > avail - len(nl_sfx):
            depassement = len(enc) - (avail - len(nl_sfx))
            if log_fn: log_fn(f"  [!] [DEPASSEMENT] [id {d['id']}] Texte FR tronque de {depassement//2} caracteres.", "warn")
            # On coupe le texte FR en retirant les caractères en trop à la fin
            t_fr = t_fr[:-(depassement//2)]
            enc = text_to_bytes('"' + n_fr + "\n" + t_fr)
            
            # Recalcul de sécurité au cas où (si des balises complexes ont été coupées)
            while len(enc) > avail - len(nl_sfx) and len(t_fr) > 0:
                t_fr = t_fr[:-1]
                enc = text_to_bytes('"' + n_fr + "\n" + t_fr)

        sp_pad = struct.pack("<H", SP) * ((avail - len(enc) - len(nl_sfx)) // 2)
        term = d.get("_term", [E1,E2,E3,E4])
        end_c = b"".join(struct.pack("<H", t) for t in term)
        null_gap_orig = data[d["offset"]+d["data_size"] : d["offset"]+d["slot_size"]]
        full = enc + sp_pad + nl_sfx + end_c + null_gap_orig
        if len(full) != d["slot_size"]: skip += 1; continue
        data[d["offset"]:d["offset"]+d["slot_size"]] = full
        ok += 1

    # ── 2. Entrées dans des blocs gzip embeddés ───────────────────────────────
    for src, entries in by_gz.items():
        # Parser l'offset du bloc gzip dans le BNP : "gz@0x1A3F" → 0x1A3F
        try:
            gz_off = int(src.split("@")[1], 16)
        except (IndexError, ValueError):
            if log_fn: log_fn(f"  _source invalide : {src}", "err")
            skip += len(entries); continue

        # Trouver la fin du bloc gzip (gzip.decompress lit jusqu'à la fin naturelle)
        try:
            dec = bytearray(gzip.decompress(data[gz_off:]))
        except Exception as e:
            if log_fn: log_fn(f"  Erreur décompression {src} : {e}", "err")
            skip += len(entries); continue

        # Patcher chaque entrée dans le binaire décompressé
        patched_in_gz = 0
        for d in entries:
            n_fr = d.get("nom_fr","").strip(); t_fr = d.get("texte_fr","").strip()
            choix_fr = d.get("choix_fr"); q_fr = d.get("question_fr","").strip()
            if choix_fr is not None:
                filled = [c for c in choix_fr if c.strip()]
                if q_fr and filled:
                    t_fr = _rebuild_choice_body(q_fr, choix_fr)
                elif not t_fr:
                    kept += 1; continue
            elif not n_fr and not t_fr:
                kept += 1; continue
            t_fr = _align_menu_text(d.get("nom_orig",""), d.get("texte_orig",""), n_fr, t_fr)
            enc = text_to_bytes('"' + n_fr + "\n" + t_fr)
            avail = d["data_size"] - 8
            nl_sfx = struct.pack("<H", NL) if _needs_nl_suffix(
                d.get("_term", [E1,E2,E3,E4]), d.get("texte_orig","")
            ) else b""
            if len(enc) + len(nl_sfx) > avail:
                if log_fn: log_fn(f"  [id {d['id']}] trop long, ignoré", "warn")
                skip += 1; continue
            sp_pad = struct.pack("<H", SP) * ((avail - len(enc) - len(nl_sfx)) // 2)
            term = d.get("_term", [E1,E2,E3,E4])
            end_c = b"".join(struct.pack("<H", t) for t in term)
            null_gap_orig = dec[d["offset"]+d["data_size"] : d["offset"]+d["slot_size"]]
            full = enc + sp_pad + nl_sfx + end_c + null_gap_orig
            if len(full) != d["slot_size"]: skip += 1; continue
            dec[d["offset"]:d["offset"]+d["slot_size"]] = full
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
            if log_fn: log_fn(f"  ⚠ {src} : bloc gzip FR trop grand ({len(new_gz)} > {orig_gz_size}), ignoré", "warn")
            ok -= patched_in_gz; skip += patched_in_gz; continue

        # Réinjecter : écrire new_gz + padding nul jusqu'à orig_gz_size
        data[gz_off:gz_off+orig_gz_size] = new_gz + bytes(orig_gz_size - len(new_gz))

    if out_path is None:
        out_path = bin_path
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(data)
    if log_fn: log_fn(f"  {ok} traduits · {skip} ignorés · {kept} conservés → {Path(out_path).name}", "ok")
    return out_path


# ── Encodage F_BE / TM_EVE ────────────────────────────────────────────────────

def encode_fbe_slot(data: bytearray, offset: int, data_size: int, n_fr: str, t_fr: str, term_list: list, log_fn=None, dlg_id=None) -> bool:
    # 1. Trouver la fin EXACTE du dialogue d'origine dans la zone allouee
    # Le dialogue s'arrete au premier 0x1107.
    orig_end = offset
    max_search = min(offset + data_size, len(data) - 1)
    # L'espace total alloue pour ce dialogue est EXACTEMENT data_size
    real_budget = data_size

    # Extraction de tail_bytes (tout ce qui vient après [1107])
    # ET récupération des animations [1431] perdues dans le texte !
    tail_start = offset + data_size
    idx = offset
    lost_anims = b''
    while idx < offset + data_size:
        if idx + 1 >= offset + data_size: break
        b0, b1 = data[idx], data[idx+1]
        w = b0 | (b1 << 8)
        if w == 0x1431:
            lost_anims += data[idx:idx+7]
            idx += 7; continue
        if w == 0x1107:
            tail_start = idx + 2
            break
        # Saut des tags texte normaux pour avancer
        if b1 in (0x11, 0x14):
            idx += 2; continue
        if 0x20 <= b0 <= 0x7E and b1 == 0x00:
            idx += 2; continue
        idx += 2

    # On cherche le End Event (31 14) dans la suite du buffer pour couper tail_bytes en deux !
    # tail_part1 = la fin logique du script courant (ex: 06 11 02 11 03 11 31 14)
    # tail_part2 = les scripts suivants caches dans le meme bloc (ex: Shadow Eikichi)
    end_event_idx = -1
    idx_search = tail_start
    while idx_search < offset + data_size:
        if idx_search + 1 >= offset + data_size: break
        w = data[idx_search] | (data[idx_search+1] << 8)
        if w == 0x1431:
            end_event_idx = idx_search
            break
        idx_search += 2

    if end_event_idx != -1:
        tail_part1 = data[tail_start : end_event_idx + 2]
        tail_part2 = data[end_event_idx + 2 : offset + data_size]
    else:
        tail_part1 = data[tail_start : offset + data_size]
        tail_part2 = b''

    header_bytes = struct.pack("<H", 0x0022) + text_to_bytes(n_fr) + struct.pack("<H", NL)
    trailer_bytes = struct.pack("<H", NL) + struct.pack("<H", 0x1107)
    
    overhead = len(header_bytes) + len(trailer_bytes) + len(tail_part1) + len(tail_part2) + len(lost_anims)
    text_budget = real_budget - overhead
    
    if text_budget < 2: return False, 0

    t_bytes = text_to_bytes(t_fr)
    if len(t_bytes) > text_budget:
        depassement = len(t_bytes) - text_budget
        if log_fn: log_fn(f"  [!] [TEXTE TRONQUE] [id {dlg_id}] Menu FR tronque de {depassement//2} caracteres.", "warn")
        t_bytes = text_to_bytes(t_fr[:text_budget//2])

    # AUCUN PADDING ! 
    # Le moteur de script de F_BE génère ses pointeurs en scannant séquentiellement 
    # les opcodes `31 14`. Si on insère le moindre octet de padding (même `00`), 
    # le scanner va l'interpréter comme le début d'un nouveau dialogue, ce qui 
    # causera le fameux crash "Invalid Memory Access" quand un Ennemi parlera !
    
    enc = header_bytes + t_bytes + lost_anims + trailer_bytes + tail_part1 + tail_part2
    
    # On remplace la portion d'origine par la nouvelle portion (qui sera plus petite)
    data[offset:offset + data_size] = enc
    
    return True, len(enc)


def encode_fbe_bnp_from_json(bin_path: str, json_path: str, log_fn, out_path: str = None) -> str:
    """Récrit les dialogues traduits dans un fichier F_BE.BNP ou TM_EVE.BNP."""
    data = bytearray(open(bin_path, "rb").read())
    import json
    dlgs = json.loads(open(json_path, encoding="utf-8").read(), strict=False)
    ok = skip = kept = 0
    done_slots = set()
    
    # TRI IMPÉRATIF PAR OFFSET POUR GÉRER LE DELTA
    dlgs.sort(key=lambda d: d["offset"])
    delta = 0
    
    for d in dlgs:
        n_fr = d.get("nom_fr","").strip(); t_fr = d.get("texte_fr","").strip()
        if not n_fr and not t_fr: kept += 1; continue
        key = (d["offset"], d["data_size"])
        if key in done_slots: continue
        term_list = d.get("_term", [])
        
        current_offset = d["offset"] + delta
        success, new_size = encode_fbe_slot(data, current_offset, d["data_size"], n_fr, t_fr, term_list, log_fn, d.get("id"))
        
        if success:
            done_slots.add(key)
            ok += 1
            delta += (new_size - d["data_size"])
        else:
            if log_fn: log_fn(f"  [!] [ERREUR F_BE] [id {d.get('id')}] Espace alloue insuffisant meme pour le nom ({d['data_size']} octets), ignore", "err")
            skip += 1
            
    if out_path is None:
        out_path = bin_path
    from pathlib import Path
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(data)
    if log_fn: log_fn(f"  [RESUME] {Path(out_path).name} : {ok} injectes, {skip} rejetes, {kept} laisses en japonais.", "ok")
    return out_path


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
            stem = Path(on).stem.lower()
            if stem in ("f_be","tm_eve"):
                # Format spécial F_BE/TM_EVE : bytes d'animation intercalés
                encode_fbe_bnp_from_json(str(op),str(jp),log_fn,out_path=str(out/fn))
            elif on.endswith(".bnp"):
                # BNP avec blocs gzip embeddés (MMAP01-06)
                encode_bnp_from_json(str(op),str(jp),log_fn,out_path=str(out/fn))
            else:
                # BIN direct (CD_SHOP.bin)
                encode_bin_from_json(str(op),str(jp),log_fn,out_path=str(out/fn))
            ok_f.append(fn)
        except Exception as e:
            if log_fn: log_fn(f"  [ERREUR CRITIQUE] Echec de l'encodage pour {fn} : {str(e)}","err"); err_f.append(fn)
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
            new_ev = rebuild_event_bin(ev, tmp, log_fn, scripts_bin_dir=tmp)
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
        try:
            # Toujours ecrire dans le dossier de travail
            log_file = self.W / "logs.txt"
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(msg + "\n")
        except: pass

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
            # FALLBACK : utiliser le event.bin original si le traduit n'existe pas
            ev_orig = self.W / "event.bin"
            if not ev_orig.exists():
                messagebox.showwarning(T("w_title"), "Impossible de trouver event.bin (ni le traduit, ni l'original extrait à l'étape C)."); return
            self.log("event.bin traduit absent, utilisation de l'original pour l'ISO...", "warn")
            ev_fr = ev_orig

        def _w():
            self.after(0, lambda: self._set_badge(self._b_rebuild, "run", T("running")))
            self.after(0, lambda: self._pb_rb.set(0))
            ev_data = open(ev_fr, "rb").read()
            Path(out).parent.mkdir(parents=True, exist_ok=True)
            
            # Auto-logging list
            def logged_log_fn(msg, type="info"):
                self.log(msg, type)
                
            rebuild_iso(iso, ev_data, out, logged_log_fn, enc_dir=self._v_encin.get())
            
            # Plus de sauvegarde différée des logs car self.log le fait en direct

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

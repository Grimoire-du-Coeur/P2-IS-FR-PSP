import threading
import struct
import json
import gzip
import io
import os
import shutil
from pathlib import Path

SP = 0x1120; NL = 0x1101
E1 = 0x1106; E2 = 0x1102; E3 = 0x1103; E4 = 0x1431
CTRL = {
    SP:"[SP]", NL:"\n", E1:"[E1]", E2:"[E2]", E3:"[E3]", E4:"[E4]",
    0x1205:"[1205]", 0x001E:"[001E]", 0x1432:"[1432]", 0x0014:"[0014]",
    0x0002:"[0002]", 0x0010:"[0010]", 0x0000:"[NULL]",
}

OFFSETS_FILE = None  # chemin vers offsets.json, set au demarrage

def save_offsets(data):
    if OFFSETS_FILE:
        json.dump(data, open(OFFSETS_FILE,"w"), indent=2)

def load_offsets():
    if OFFSETS_FILE and Path(OFFSETS_FILE).exists():
        return json.load(open(OFFSETS_FILE))
    return {}

def extract_cpk_from_iso(iso_path, out_dir, log):
    """Cherche P2PT_ALL.cpk dans l'ISO et l'extrait."""
    log("Lecture ISO...")
    iso = open(iso_path, "rb").read()
    SECTOR = 2048
    target = b"P2PT_ALL.CPK"
    log(f"Recherche de P2PT_ALL.CPK dans l'ISO ({len(iso)//1024//1024} MB)...")
    for sector in range(16, 500):
        off = sector * SECTOR
        block = iso[off:off+SECTOR]
        if target in block.upper():
            log(f"  Reference trouvee au secteur {sector}")
            break
    CPK_MAGIC = b"CPK "
    pos = iso.find(CPK_MAGIC)
    if pos == -1:
        raise Exception("P2PT_ALL.CPK introuvable dans l'ISO")
    log(f"  CPK trouve a l'offset 0x{pos:08x}")
    # Sauvegarder l'offset du CPK dans l'ISO
    offs = load_offsets()
    offs["iso_path"]  = iso_path
    offs["cpk_offset_in_iso"] = pos
    save_offsets(offs)

    cpk_data = iso[pos:]
    out_path = Path(out_dir) / "P2PT_ALL.cpk"
    open(out_path, "wb").write(cpk_data)
    log(f"  P2PT_ALL.cpk extrait ({len(cpk_data)//1024//1024} MB)")
    return str(out_path)

def extract_event_from_cpk(cpk_path, out_dir, log):
    """
    Cherche event.bin dans le CPK et l'extrait proprement.
    Strategie: chercher le TOC d'event.bin en cherchant une sequence de paires
    (start, end) valides correspondant a des blocs gzip (magic 1f 8b).
    """
    log("Lecture CPK...")
    cpk = open(cpk_path, "rb").read()
    log(f"Taille CPK: {len(cpk)//1024//1024} MB")

    GZIP_MAGIC = b"\x1f\x8b"

    log("  Recherche du TOC d'event.bin (sequence de blocs gzip)...")

    # Chercher une zone avec au moins 5 paires (start, end) consecutives
    # ou le premier bloc pointe vers un magic gzip
    # Le TOC est aligne sur 4 bytes, les starts/ends sont relatifs au debut d'event.bin
    # start[0] est toujours ~ 0x1000 (apres le TOC lui-meme)

    best_pos = -1
    idx = 0
    while idx < len(cpk) - 40:
        # Chercher 0x1000 suivi d'un end raisonnable
        found = cpk.find(b"\x00\x10\x00\x00", idx)
        if found == -1:
            break

        # Verifier alignement 4 bytes
        if found % 4 != 0:
            idx = found + 1
            continue

        end0 = struct.unpack_from("<I", cpk, found + 4)[0]
        # end du script 0 doit etre entre 0x20000 et 0x40000 (128KB-256KB)
        if not (0x20000 <= end0 <= 0x40000):
            idx = found + 1
            continue

        # Verifier que le debut du premier bloc gzip est bien la
        if found + end0 + 8 >= len(cpk):
            idx = found + 1
            continue

        # Le premier script gzip doit commencer a found + 0x1000
        gzip_pos = found + 0x1000
        if gzip_pos + 2 < len(cpk) and cpk[gzip_pos:gzip_pos+2] == GZIP_MAGIC:
            log(f"  TOC valide trouve a 0x{found:x} (end0=0x{end0:x}, gzip confirme)")
            best_pos = found
            break

        # Ou verifier avec au moins 3 entrees consecutives coherentes
        valid = True
        prev_end = end0
        for k in range(1, 5):
            s = struct.unpack_from("<I", cpk, found + k*8)[0]
            e = struct.unpack_from("<I", cpk, found + k*8 + 4)[0]
            if s == 0: break
            if not (prev_end <= s <= prev_end + 0x100000):
                valid = False; break
            if not (s < e <= s + 0x100000):
                valid = False; break
            prev_end = e
        if valid:
            log(f"  TOC valide trouve a 0x{found:x} (end0=0x{end0:x})")
            best_pos = found
            break

        idx = found + 1

    if best_pos == -1:
        raise Exception(
            "Impossible de localiser event.bin dans le CPK automatiquement.\n"
            "Conseil: extrais event.bin manuellement avec CriFsLib et utilise\n"
            "le bouton 'Parcourir' de l'etape 3."
        )

    toc_start = best_pos

    # Lire le TOC pour trouver le nombre exact de scripts et la taille totale
    entries = []
    i = toc_start
    while i + 8 <= len(cpk):
        s = struct.unpack_from("<I", cpk, i)[0]
        e = struct.unpack_from("<I", cpk, i+4)[0]
        if s == 0:
            break
        # Sanite: start et end doivent etre croissants et raisonnables
        if entries and s < entries[-1][1]:
            break
        if e > s + 0x500000:  # max ~5MB par script
            break
        entries.append((s, e))
        i += 8

    if not entries:
        raise Exception("TOC vide apres parsing")

    last_end = entries[-1][1]
    event_size = last_end
    log(f"  {len(entries)} entrees dans le TOC, taille event.bin = {event_size//1024//1024} MB ({event_size} octets)")

    event_data = cpk[toc_start:toc_start + event_size]
    if len(event_data) < event_size:
        log(f"  Attention: donnees tronquees ({len(event_data)} < {event_size})")

    # Sauvegarder l'offset event dans le CPK et dans l'ISO
    offs = load_offsets()
    offs["event_offset_in_cpk"] = toc_start
    cpk_in_iso = offs.get("cpk_offset_in_iso", 0)
    offs["event_offset_in_iso"] = cpk_in_iso + toc_start
    offs["event_size"] = event_size
    save_offsets(offs)
    log(f"  Offset event.bin dans l ISO: 0x{cpk_in_iso + toc_start:08x}")

    out_path = Path(out_dir) / "event.bin"
    open(out_path, "wb").write(event_data)
    log(f"  event.bin extrait ({len(event_data)} octets)")
    return str(out_path)

def extract_scripts_from_event(event_path, out_dir, log):
    """
    Extrait exactement les scripts 0-398 depuis event.bin.
    Lit le TOC pour avoir les vrais offsets, limite a 399 scripts max.
    """
    data = open(event_path, "rb").read()
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    log(f"event.bin: {len(data)} octets")

    # Lire le TOC
    entries = []
    i = 0
    while i + 8 <= len(data):
        s = struct.unpack_from("<I", data, i)[0]
        e = struct.unpack_from("<I", data, i+4)[0]
        if s == 0:
            break
        entries.append((s, e))
        i += 8

    log(f"  TOC: {len(entries)} entrees")

    # Limiter a 399 scripts (0 a 398)
    MAX_SCRIPTS = 399
    entries = entries[:MAX_SCRIPTS]
    log(f"  Extraction de {len(entries)} scripts (0 a {len(entries)-1})...")

    ok = 0; errors = 0
    for idx, (start, end) in enumerate(entries):
        if end > len(data) or start >= end:
            log(f"  [SKIP] script_{idx}: offset invalide (start=0x{start:x} end=0x{end:x})")
            errors += 1
            continue

        chunk = data[start:end]

        # Verifier magic gzip
        if chunk[:2] != b"\x1f\x8b":
            # Sauvegarder quand meme le chunk brut (certains scripts ne sont pas gzip)
            fname = Path(out_dir) / f"script_{idx}.bin"
            open(fname, "wb").write(chunk)
            if idx % 50 == 0:
                log(f"  script_{idx}.bin (brut, {len(chunk)} octets)")
            ok += 1
            continue

        try:
            with gzip.open(io.BytesIO(chunk)) as f:
                content = f.read()
            fname = Path(out_dir) / f"script_{idx}.bin"
            open(fname, "wb").write(content)
            if idx % 50 == 0:
                log(f"  script_{idx}.bin ({len(content)} octets)")
            ok += 1
        except Exception as e:
            # Sauvegarder le chunk brut en cas d'erreur de decompression
            fname = Path(out_dir) / f"script_{idx}.bin"
            open(fname, "wb").write(chunk)
            log(f"  script_{idx}.bin (erreur gzip, sauvegarde brut: {e})")
            ok += 1

    log(f"  {ok} scripts extraits, {errors} skips -> {out_dir}")
    return ok

def is_valid_dialogue(data, start):
    j = start + 2
    nom_chars = []
    nom_printable = 0
    while j < len(data) - 1:
        cp = struct.unpack_from("<H", data, j)[0]
        if cp == NL:
            if len(nom_chars) == 0 or len(nom_chars) > 80:
                return False
            return (nom_printable / len(nom_chars)) >= 0.6
        if 0x0020 <= cp < 0x0200:
            nom_printable += 1
        elif cp == SP:
            nom_printable += 1
        nom_chars.append(cp)
        if len(nom_chars) > 100:
            return False
        j += 2
    return False

def decode_text(raw):
    out = ""
    for i in range(0, len(raw), 2):
        cp = struct.unpack_from("<H", raw, i)[0]
        if cp in CTRL: out += CTRL[cp]
        elif 0x20 <= cp < 0x200: out += chr(cp)
        else: out += f"[U+{cp:04X}]"
    return out

def find_dialogues_dynamic(data):
    dialogues = []
    i = 0
    while i < len(data) - 1:
        cp = struct.unpack_from("<H", data, i)[0]
        if cp == 0x0022:
            if not is_valid_dialogue(data, i):
                i += 2; continue
            start = i; chars = []; j = i; valid = True
            while j < len(data) - 1:
                c = struct.unpack_from("<H", data, j)[0]
                chars.append(c)
                if len(chars) > 2000: valid = False; break
                if len(chars) >= 4 and chars[-4:] == [E1, E2, E3, E4]:
                    end = j + 2
                    dialogues.append({"id": len(dialogues), "offset": start,
                        "data_size": end-start, "slot_size": end-start+4})
                    break
                j += 2
            if valid and dialogues and dialogues[-1]["offset"] == start:
                i = dialogues[-1]["offset"] + dialogues[-1]["slot_size"]; continue
        i += 2
    return dialogues

def decode_all_scripts(scripts_dir, output_dir, log):
    """Decode les scripts 0-398 en JSON."""
    scripts_dir = Path(scripts_dir)
    output_dir  = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    total = 0; vides = []
    for i in range(0, 399):
        bin_file = scripts_dir / f"script_{i}.bin"
        if not bin_file.exists(): continue
        raw = open(bin_file, "rb").read()
        if raw[:2] == b'\x1f\x8b':
            try: raw = gzip.decompress(raw)
            except: pass
        dialogues = find_dialogues_dynamic(raw)
        result = []
        for d in dialogues:
            chunk = raw[d["offset"]:d["offset"]+d["data_size"]]
            text  = decode_text(chunk)
            lines = text.split("\n")
            nom     = lines[0].lstrip('"') if lines else ""
            contenu = "\n".join(lines[1:]).replace("[E1][E2][E3][E4]","").rstrip() if len(lines)>1 else ""
            result.append({"id":d["id"],"offset":d["offset"],"slot_size":d["slot_size"],
                "data_size":d["data_size"],"nom_orig":nom,"texte_orig":contenu,"nom_fr":"","texte_fr":""})
        json.dump(result, open(output_dir/f"script_{i}.json","w",encoding="utf-8"), ensure_ascii=False, indent=2)
        total += 1
        if not result: vides.append(i)
        if i % 50 == 0: log(f"  script_{i} -> {len(result)} dialogues")
    log(f"  {total} scripts decodes, {len(vides)} vides")

def text_to_bytes(text):
    # Mapping custom accents FR → caractères japonais modifiés dans syscg.bin
    text = text.replace('é', 'Ğ')
    text = text.replace('è', 'ò')
    text = text.replace('ê', '¿')
    text = text.replace('ô', 'Æ')
    text = text.replace('É', 'Ņ')
    text = text.replace('È', 'Ũ')
    text = text.replace('Î', '£')
    text = text.replace('Ô', 'ō')
    text = text.replace('Û', 'ĵ')
    text = text.replace('œ', 'ë')
    text = text.replace('Œ', 'Ǩ')
    text = text.replace('ü', 'ˠ')
    text = text.replace('ï', 'Ȗ')
    out = []; i = 0
    while i < len(text):
        if text[i] == '[':
            end = text.index(']', i); tag = text[i:end+1]
            if tag == "[NULL]":out.append(b'\x00\x00');i = end+1; continue
            found = False
            for code, name in CTRL.items():
                if name == tag: out.append(struct.pack("<H", code)); found=True; break
            if not found and tag.startswith("[U+") and len(tag)==8:
                try: out.append(struct.pack("<H", int(tag[3:7],16))); found=True
                except: pass
            if not found and len(tag)==6:
                try: out.append(struct.pack("<H", int(tag[1:5],16))); found=True
                except: pass
            if not found:
                for c in tag[1:-1]: out.append(struct.pack("<H",ord(c)))
            i = end+1
        elif text[i] == '\n': out.append(struct.pack("<H",NL)); i+=1
        elif text[i] == ' ':  out.append(struct.pack("<H",SP)); i+=1
        else: out.append(struct.pack("<H",ord(text[i]))); i+=1
    return b"".join(out)

def encode_script(bin_path, json_path, log, out_dir=None):
    """Re-encode un JSON traduit en .bin, sorti dans out_dir si fourni."""
    data      = bytearray(open(bin_path,"rb").read())
    dialogues = json.load(open(json_path, encoding="utf-8"))
    ok = skip = kept = 0
    for d in dialogues:
        nom_fr   = d.get("nom_fr","").strip()
        texte_fr = d.get("texte_fr","").strip()
        if not nom_fr or not texte_fr: kept+=1; continue
        text_bytes = text_to_bytes('"'+nom_fr+"\n"+texte_fr+"\n")
        target = d["data_size"] - 8
        if len(text_bytes) > target:
            log(f"  SKIP [{d['id']}] trop long ({len(text_bytes)} > {target})")
            skip+=1; continue
        sp_count = (target - len(text_bytes)) // 2
        sp_pad   = struct.pack("<H", SP) * sp_count
        end_codes = struct.pack("<HHHH", E1, E2, E3, E4)
        null_gap  = bytes(d["slot_size"] - d["data_size"])
        full = text_bytes + sp_pad + end_codes + null_gap
        if len(full) != d["slot_size"]:
            skip+=1; continue
        data[d["offset"]:d["offset"]+d["slot_size"]] = full
        ok+=1

    # Nom du fichier de sortie = script_XX_fr.bin
    stem = Path(bin_path).stem  # ex: script_0
    out_name = f"{stem}_fr.bin"
    if out_dir:
        Path(out_dir).mkdir(parents=True, exist_ok=True)
        out = str(Path(out_dir) / out_name)
    else:
        out = str(Path(bin_path).parent / out_name)

    open(out,"wb").write(data)
    log(f"  {ok} traduits, {skip} skips, {kept} gardes -> {out_name}")
    return out

def rebuild_iso(iso_orig, event_bin, scripts_dir, out_iso, log):
    """Reinjecte tous les scripts traduits dans l'ISO."""
    log("Lecture event.bin...")
    event = bytearray(open(event_bin,"rb").read())
    scripts_dir = Path(scripts_dir)

    # Lire le TOC
    toc = []
    i = 0
    while True:
        s = struct.unpack_from("<I", event, i)[0]
        e = struct.unpack_from("<I", event, i+4)[0]
        if s == 0: break
        toc.append((s, e, i))
        i += 8
    log(f"  TOC: {len(toc)} entrees")

    # Patcher les scripts traduits
    patched = 0
    for idx, (start, end, toc_off) in enumerate(toc):
        fr_bin = scripts_dir / f"script_{idx}_fr.bin"
        if not fr_bin.exists(): continue
        script_data = open(fr_bin,"rb").read()
        gz_buf = io.BytesIO()
        with gzip.GzipFile(filename=b"e0000.bin", mode="wb", fileobj=gz_buf, mtime=0) as gz:
            gz.write(script_data)
        new_gz = gz_buf.getvalue()
        if len(new_gz) > end - start:
            log(f"  SKIP script_{idx}: trop grand")
            continue
        event[start:start+len(new_gz)] = new_gz
        event[start+len(new_gz):end]   = bytes((end-start)-len(new_gz))
        struct.pack_into("<I", event, toc_off+4, start+len(new_gz))
        patched += 1
    log(f"  {patched} scripts reinjectes dans event.bin")

    # Trouver l'offset d'event.bin dans l'ISO
    # Methode fiable: utiliser l'offset memorise pendant l'extraction
    log("Recherche de l'offset event.bin dans l'ISO...")
    offs = load_offsets()
    pos = offs.get("event_offset_in_iso", -1)
    if pos != -1:
        log(f"  Offset memorise: 0x{pos:08x}")
        # Verification rapide: lire 4 bytes a cet offset et verifier TOC
        with open(iso_orig, "rb") as f:
            f.seek(pos)
            check = struct.unpack("<I", f.read(4))[0]
        if check == 0x1000:
            log(f"  Verification OK (TOC start = 0x{check:x})")
        else:
            log(f"  Attention: valeur inattendue 0x{check:x} a l offset memorise")
            pos = -1

    if pos == -1:
        raise Exception(
            "Offset event.bin inconnu.\n"
            "Relance d'abord les etapes 1 et 2 (extraction CPK et event.bin)\n"
            "pour que l'outil memorise l'offset correct."
        )
    iso = bytearray(open(iso_orig,"rb").read())

    shutil.copy(iso_orig, out_iso)
    with open(out_iso,"r+b") as f:
        f.seek(pos)
        f.write(bytes(event))
    log(f"  ISO creee: {Path(out_iso).name}")


import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import sys

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

P5_RED="#c0000a";P5_RED_HOV="#e8001a";P5_RED_DARK="#5a0003";P5_BG_CARD="#0e0000"
P4_YELLOW="#f5c400";P4_YELLOW_HOV="#ffd740";P4_YELLOW_DRK="#7a6200";P4_BG_CARD="#0e0b00"
P3_BLUE="#4a90d9";P3_BLUE_HOV="#6aabf0";P3_BLUE_DARK="#1a3d6a";P3_BG_CARD="#000a14"
COL_BG="#080808";COL_MED="#0f0f0f";COL_CARD="#141414";COL_BORDER="#242424"
COL_WHITE="#e8e8e8";COL_MUTED="#404040";COL_MUTED2="#686868";COL_GREEN="#1D9E75";COL_GRN_BG="#071a0e"
_WIN=sys.platform.startswith("win")
FONT_DISPLAY=("Arial Black",20) if _WIN else ("Arial",20,"bold")
FONT_TITLE=("Arial",15,"bold");FONT_LABEL_B=("Arial",12,"bold");FONT_LABEL=("Arial",12)
FONT_MONO=("Consolas",12);FONT_MONO_S=("Consolas",11);FONT_BADGE=("Consolas",11,"bold")
FONT_STEP_N=("Impact",24) if _WIN else ("Arial Black",22,"bold")

class StatusBadge(ctk.CTkFrame):
    _S={"wait":("#1e1e1e",COL_MUTED2,"◌  EN ATTENTE"),"run":("#1a1600",P4_YELLOW,"◉  EN COURS..."),
        "ok":(COL_GRN_BG,COL_GREEN,"✔  TERMINÉ"),"err":("#1a0000","#ff4444","✘  ERREUR")}
    def __init__(self,parent,**kw):
        super().__init__(parent,fg_color="transparent",**kw)
        self._lbl=ctk.CTkLabel(self,text="◌  EN ATTENTE",font=FONT_BADGE,text_color=COL_MUTED2,
            fg_color="#1e1e1e",corner_radius=3,padx=10,pady=4)
        self._lbl.pack()
        self._state="wait";self._job=None;self._phase=False
    def set_state(self,s):
        if self._job: self.after_cancel(self._job);self._job=None
        self._state=s
        if s in self._S:
            bg,fg,txt=self._S[s];self._lbl.configure(fg_color=bg,text_color=fg,text=txt)
        if s=="run": self._pulse()
    def _pulse(self):
        if self._state!="run": return
        self._phase=not self._phase
        self._lbl.configure(text_color=P4_YELLOW if self._phase else "#907500")
        self._job=self.after(480,self._pulse)

class FileCard(ctk.CTkFrame):
    def __init__(self,parent,label,filetypes,callback=None,accent=P5_RED,**kw):
        super().__init__(parent,fg_color=COL_CARD,border_color=COL_BORDER,border_width=1,corner_radius=5,**kw)
        self.filetypes=filetypes;self.callback=callback;self.accent=accent;self.path=None
        self._bar=ctk.CTkFrame(self,width=3,fg_color=accent,corner_radius=0)
        self._bar.pack(side="left",fill="y");self._bar.pack_propagate(False)
        inn=ctk.CTkFrame(self,fg_color="transparent")
        inn.pack(side="left",fill="both",expand=True,padx=14,pady=10)
        ctk.CTkLabel(inn,text=label.upper(),font=FONT_LABEL_B,text_color=COL_WHITE).pack(anchor="w")
        self._lbl=ctk.CTkLabel(inn,text="Aucun fichier sélectionné",font=FONT_MONO_S,
            text_color=COL_MUTED2,anchor="w",wraplength=420)
        self._lbl.pack(fill="x",pady=(3,7))
        ctk.CTkButton(inn,text="  PARCOURIR...",width=150,height=28,fg_color=accent,
            hover_color=self._br(accent),text_color="white",font=FONT_BADGE,corner_radius=3,
            command=self._browse).pack(anchor="w")
    @staticmethod
    def _br(h):
        try: return "#{:02x}{:02x}{:02x}".format(min(255,int(h[1:3],16)+45),min(255,int(h[3:5],16)+45),min(255,int(h[5:7],16)+45))
        except: return h
    def _browse(self):
        p=filedialog.askopenfilename(filetypes=self.filetypes)
        if p: self.set_path(p)
    def set_path(self,path):
        self.path=path;self._lbl.configure(text=Path(path).name,text_color=COL_GREEN)
        self._bar.configure(fg_color=COL_GREEN)
        if self.callback: self.callback(path)

class LogConsole(ctk.CTkFrame):
    def __init__(self,parent,**kw):
        super().__init__(parent,fg_color="#050505",border_color="#1a1a1a",border_width=1,corner_radius=0,**kw)
        hdr=ctk.CTkFrame(self,fg_color="#0a0a0a",height=30,corner_radius=0)
        hdr.pack(fill="x");hdr.pack_propagate(False)
        self._dot=ctk.CTkLabel(hdr,text="●",font=("Arial",9),text_color=COL_GREEN)
        self._dot.pack(side="left",padx=(12,4),pady=5)
        ctk.CTkLabel(hdr,text="CONSOLE",font=FONT_BADGE,text_color=COL_GREEN).pack(side="left",pady=5)
        ctk.CTkButton(hdr,text="EFFACER",width=72,height=20,fg_color="#181818",hover_color="#2a2a2a",
            text_color=COL_MUTED2,font=FONT_BADGE,corner_radius=3,command=self.clear).pack(side="right",padx=10,pady=5)
        wrap=ctk.CTkFrame(self,fg_color="#030303",corner_radius=0);wrap.pack(fill="both",expand=True)
        self._txt=tk.Text(wrap,font=FONT_MONO,bg="#030303",fg="#00e060",insertbackground=COL_GREEN,
            selectbackground=COL_GRN_BG,selectforeground=COL_GREEN,bd=0,highlightthickness=0,
            wrap="word",state="disabled",padx=12,pady=8,relief="flat")
        self._txt.pack(fill="both",expand=True,side="left")
        self._txt.tag_config("err",foreground="#ff4444");self._txt.tag_config("ok",foreground=COL_GREEN)
        self._txt.tag_config("sep",foreground=P3_BLUE);self._txt.tag_config("warn",foreground=P4_YELLOW)
        self._txt.tag_config("info",foreground=COL_MUTED2)
        sb=tk.Scrollbar(wrap,orient="vertical",command=self._txt.yview,bg="#0c0c0c",
            troughcolor="#060606",activebackground="#1a1a1a",width=5,borderwidth=0,highlightthickness=0)
        sb.pack(side="right",fill="y");self._txt.configure(yscrollcommand=sb.set)
        self._txt.bind("<MouseWheel>",lambda e:self._txt.yview_scroll(int(-1*(e.delta/120)),"units"))
        self._txt.bind("<Button-4>",lambda e:self._txt.yview_scroll(-1,"units"))
        self._txt.bind("<Button-5>",lambda e:self._txt.yview_scroll(1,"units"))
        self._dot_on=True;self._blink()
    def _blink(self):
        self._dot_on=not self._dot_on
        self._dot.configure(text_color=COL_GREEN if self._dot_on else "#003318")
        self.after(1400,self._blink)
    def _tag(self,msg):
        m=msg.lower()
        if any(x in m for x in ("erreur","error","skip","[err")): return "err"
        if "===" in msg: return "sep"
        if any(x in m for x in ("ok","termine","extrait","traduit","cree")): return "ok"
        if "attention" in m: return "warn"
        if m.startswith("  ") or m.startswith("lecture"): return "info"
        return ""
    def log(self,msg):
        self._txt.configure(state="normal");self._txt.insert("end",msg+"\n",self._tag(msg))
        self._txt.see("end");self._txt.configure(state="disabled");self._txt.update_idletasks()
    def clear(self):
        self._txt.configure(state="normal");self._txt.delete("1.0","end");self._txt.configure(state="disabled")

def _snc(parent,num,color):
    S,CUT=46,13
    c=tk.Canvas(parent,width=S,height=S,bg=COL_BG,highlightthickness=0)
    c.create_polygon([CUT,0,S,0,S,S,0,S,0,CUT],fill=color,outline="")
    c.create_text(S//2+1,S//2+1,text=num,fill="white",font=FONT_STEP_N)
    return c

def _hsep(parent,color=COL_BORDER,pady=10):
    ctk.CTkFrame(parent,height=1,fg_color=color,corner_radius=0).pack(fill="x",pady=pady,padx=4)

def _p5b(p,t,c,w=230): return ctk.CTkButton(p,text=t,command=c,width=w,height=34,fg_color=P5_RED,hover_color=P5_RED_HOV,text_color="white",font=FONT_LABEL_B,corner_radius=4)
def _p4b(p,t,c,w=230): return ctk.CTkButton(p,text=t,command=c,width=w,height=34,fg_color=P4_YELLOW,hover_color=P4_YELLOW_HOV,text_color="#110d00",font=FONT_LABEL_B,corner_radius=4)
def _p3b(p,t,c,w=230): return ctk.CTkButton(p,text=t,command=c,width=w,height=34,fg_color=P3_BLUE,hover_color=P3_BLUE_HOV,text_color="white",font=FONT_LABEL_B,corner_radius=4)
def _gb(p,t,c,w=110):  return ctk.CTkButton(p,text=t,command=c,width=w,height=26,fg_color=COL_CARD,hover_color=COL_BORDER,text_color=COL_MUTED2,font=FONT_BADGE,border_color=COL_BORDER,border_width=1,corner_radius=3)

def _frow(parent,label,var,cmd,w=300):
    row=ctk.CTkFrame(parent,fg_color="transparent");row.pack(fill="x",pady=3)
    ctk.CTkLabel(row,text=label,font=FONT_BADGE,text_color=COL_MUTED2,width=175,anchor="w").pack(side="left")
    ent=ctk.CTkEntry(row,textvariable=var,width=w,height=26,font=FONT_MONO_S,
        fg_color=COL_CARD,border_color=COL_BORDER,border_width=1,text_color=COL_WHITE,corner_radius=3)
    ent.pack(side="left",padx=(0,6))
    _gb(row,"...",cmd,38).pack(side="left")
    return ent

def _step_card(parent,num,title,color,body_fn):
    row=ctk.CTkFrame(parent,fg_color="transparent");row.pack(fill="x",padx=22,pady=7)
    _snc(row,num,color).pack(side="left",padx=(0,10),pady=4)
    card=ctk.CTkFrame(row,fg_color=COL_CARD,border_color=COL_BORDER,border_width=1,corner_radius=5)
    card.pack(side="left",fill="both",expand=True)
    ctk.CTkFrame(card,width=3,fg_color=color,corner_radius=0).pack(side="left",fill="y")
    inn=ctk.CTkFrame(card,fg_color="transparent")
    inn.pack(side="left",fill="both",expand=True,padx=14,pady=10)
    ctk.CTkLabel(inn,text=title.upper(),font=FONT_LABEL_B,text_color=COL_WHITE).pack(anchor="w")
    body_fn(inn)

class P2ISApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Persona 2: Innocent Sin FR — Outil de traduction")
        self.geometry("900x960");self.minsize(800,820);self.configure(fg_color=COL_BG)
        self.iso_path=tk.StringVar();self.cpk_path=tk.StringVar();self.event_path=tk.StringVar()
        self.scripts_dir=tk.StringVar();self.json_dir=tk.StringVar()
        self.work_dir=tk.StringVar(value=str(Path.home()/"Desktop"/"P2IS_FR"))
        self._mod=sys.modules[__name__]
        def _ow(*_): self._mod.OFFSETS_FILE=str(Path(self.work_dir.get())/"offsets.json")
        self.work_dir.trace_add("write",_ow);_ow()
        self._iso_for_rebuild=None;self._event_for_rebuild=None
        self._json_to_encode=None;self._bin_orig=None
        self._fr_bin_dir=tk.StringVar()
        self._out_iso=tk.StringVar(value=str(Path.home()/"Desktop"/"P2IS_FR.iso"))
        self._bin_dir_all=tk.StringVar()
        self._panels=[];self._tab_btns=[]
        self._build_ui()

    def _build_ui(self):
        self._build_header()
        self._build_workdir_bar()
        self._build_tabbar()    # barre d'onglets EN BAS (pack side=bottom avant le paned)
        self._init_paned()      # crée le PanedWindow + _content
        self._fill_tabs()       # remplit _content avec les panels
        self._build_console()   # ajoute la console dans le paned
        self._switch_tab(0)

    def _init_paned(self):
        # PanedWindow vertical natif — les deux volets s'ajustent au drag
        self._paned = tk.PanedWindow(self, orient="vertical",
            bg="#1a1a1a", sashwidth=6, sashpad=0,
            sashrelief="flat", handlesize=0,
            showhandle=False, opaqueresize=True)
        self._paned.pack(fill="both", expand=True)
        # _content est enfant direct du paned (obligatoire pour reparenting)
        self._content = ctk.CTkFrame(self._paned, fg_color=COL_BG, corner_radius=0)
        self._paned.add(self._content, stretch="always", minsize=200)

    def _build_header(self):
        hdr=ctk.CTkFrame(self,height=66,fg_color="#0c0000",corner_radius=0)
        hdr.pack(fill="x");hdr.pack_propagate(False)
        ctk.CTkFrame(hdr,height=2,fg_color=P5_RED,corner_radius=0).pack(side="bottom",fill="x")
        c=ctk.CTkFrame(hdr,fg_color="transparent");c.pack(expand=True)
        ctk.CTkLabel(c,text="PERSONA 2: INNOCENT SIN",font=FONT_DISPLAY,text_color=COL_WHITE).pack()
        ctk.CTkLabel(c,text="Fan Translation Tool  ·  PSP EUR (ULES01557)",font=("Consolas",10),text_color="#bb5555").pack()

    def _build_workdir_bar(self):
        bar=ctk.CTkFrame(self,height=40,fg_color="#0c0c0c",corner_radius=0)
        bar.pack(fill="x");bar.pack_propagate(False)
        inn=ctk.CTkFrame(bar,fg_color="transparent");inn.pack(side="left",padx=16,pady=6)
        ctk.CTkLabel(inn,text="DOSSIER :",font=FONT_BADGE,text_color=COL_MUTED2).pack(side="left",padx=(0,8))
        ctk.CTkEntry(inn,textvariable=self.work_dir,width=360,height=26,font=FONT_MONO_S,
            fg_color=COL_CARD,border_color=COL_BORDER,border_width=1,text_color=COL_WHITE,corner_radius=3).pack(side="left",padx=(0,8))
        _gb(inn,"CHANGER",self._pick_workdir,78).pack(side="left")

    def _build_tabbar(self):
        # Barre d'onglets packée en bas AVANT le PanedWindow → toujours visible
        tb=ctk.CTkFrame(self,height=46,fg_color="#0c0c0c",corner_radius=0)
        tb.pack(fill="x",side="bottom");tb.pack_propagate(False)
        # Ligne de séparation en haut de la barre
        ctk.CTkFrame(tb,height=1,fg_color=COL_BORDER,corner_radius=0).pack(fill="x",side="top")
        defs=[("  ◆  01 — PIPELINE EXTRACTION  ",P5_RED),("  ◆  02 — TRADUCTION  ",P4_YELLOW),("  ◆  03 — REBUILD ISO  ",P3_BLUE)]
        for i,(label,color) in enumerate(defs):
            btn=ctk.CTkButton(tb,text=label,font=FONT_BADGE,fg_color="transparent",hover_color=COL_CARD,
                text_color=COL_MUTED2,border_width=0,corner_radius=0,height=46,
                command=lambda idx=i:self._switch_tab(idx))
            btn.pack(side="left");self._tab_btns.append((btn,color))

    def _fill_tabs(self):
        # Remplit _content (déjà dans le paned) avec les 3 panels
        for fn in [self._build_p5,self._build_p4,self._build_p3]:
            panel=ctk.CTkScrollableFrame(self._content,fg_color=COL_BG,corner_radius=0,
                scrollbar_button_color=COL_BORDER,scrollbar_button_hover_color=COL_MUTED)
            fn(panel);self._panels.append(panel)

    def _switch_tab(self,idx):
        for p in self._panels: p.pack_forget()
        self._panels[idx].pack(fill="both",expand=True)
        for i,(btn,color) in enumerate(self._tab_btns):
            btn.configure(text_color=color if i==idx else COL_MUTED2)

    def _build_console(self):
        # Volet bas : console (ajoutée dans le paned déjà créé)
        self.log_box = LogConsole(self._paned)
        self._paned.add(self.log_box, stretch="never", minsize=80)
        # Placer le sash après que la fenêtre soit dessinée
        self.after(150, self._place_sash)

    def _place_sash(self):
        h = self.winfo_height()
        if h > 300:
            self._paned.sash_place(0, 0, h - 230)
        else:
            self.after(100, self._place_sash)

    # ── PANEL P5 (rouge) ──────────────────────────────────────────────────────
    def _build_p5(self,parent):
        PAD={"padx":22,"pady":7}
        t=ctk.CTkFrame(parent,fg_color=P5_BG_CARD,border_color=P5_RED_DARK,border_width=1,corner_radius=5)
        t.pack(fill="x",**PAD)
        ctk.CTkLabel(t,text="  PIPELINE EXTRACTION — 4 ÉTAPES",font=FONT_TITLE,text_color=P5_RED).pack(anchor="w",padx=14,pady=9)

        _step_card(parent,"1","ISO PSP  →  P2PT_ALL.cpk",P5_RED,self._s1body)
        _hsep(parent,P5_RED_DARK)
        _step_card(parent,"2","P2PT_ALL.cpk  →  event.bin",P5_RED,self._s2body)
        _hsep(parent,P5_RED_DARK)
        _step_card(parent,"3","event.bin  →  scripts 0–398",P5_RED,self._s3body)
        _hsep(parent,P5_RED_DARK)
        _step_card(parent,"4","Scripts .bin  →  JSON décodés",P5_RED,self._s4body)
        ctk.CTkFrame(parent,height=18,fg_color="transparent").pack()

    def _s1body(self,inn):
        self.dz_iso=FileCard(inn,"ISO PSP Européenne",[("ISO PSP","*.iso"),("Tous","*.*")],self._on_iso_selected,P5_RED)
        self.dz_iso.pack(fill="x",pady=(6,0))
        row=ctk.CTkFrame(inn,fg_color="transparent");row.pack(fill="x",pady=(8,0))
        _p5b(row,"  EXTRAIRE P2PT_ALL.CPK",lambda:self._run(self._do_extract_cpk),240).pack(side="left")
        self._badge_s1=StatusBadge(row);self._badge_s1.pack(side="left",padx=12)

    def _s2body(self,inn):
        self.dz_cpk=FileCard(inn,"P2PT_ALL.cpk",[("CPK","*.cpk"),("Tous","*.*")],self._on_cpk_selected,P5_RED)
        self.dz_cpk.pack(fill="x",pady=(6,0))
        row=ctk.CTkFrame(inn,fg_color="transparent");row.pack(fill="x",pady=(8,0))
        _p5b(row,"  EXTRAIRE EVENT.BIN",lambda:self._run(self._do_extract_event),220).pack(side="left")
        self._badge_s2=StatusBadge(row);self._badge_s2.pack(side="left",padx=12)

    def _s3body(self,inn):
        self.dz_event=FileCard(inn,"event.bin",[("BIN","*.bin"),("Tous","*.*")],self._on_event_selected,P5_RED)
        self.dz_event.pack(fill="x",pady=(6,0))
        fr=ctk.CTkFrame(inn,fg_color="transparent");fr.pack(fill="x",pady=(6,0))
        ctk.CTkLabel(fr,text="Sortie :",font=FONT_BADGE,text_color=COL_MUTED2).pack(side="left",padx=(0,8))
        self.ent_scripts=ctk.CTkEntry(fr,textvariable=self.scripts_dir,width=310,height=24,font=FONT_MONO_S,
            fg_color=COL_CARD,border_color=COL_BORDER,border_width=1,text_color=COL_WHITE,corner_radius=3)
        self.ent_scripts.pack(side="left",padx=(0,6))
        _gb(fr,"...",self._pick_scripts_dir,38).pack(side="left")
        row=ctk.CTkFrame(inn,fg_color="transparent");row.pack(fill="x",pady=(8,0))
        _p5b(row,"  EXTRAIRE LES 399 SCRIPTS",lambda:self._run(self._do_extract_scripts),260).pack(side="left")
        self._badge_s3=StatusBadge(row);self._badge_s3.pack(side="left",padx=12)

    def _s4body(self,inn):
        fr=ctk.CTkFrame(inn,fg_color="transparent");fr.pack(fill="x",pady=(4,0))
        ctk.CTkLabel(fr,text="Dossier scripts .bin :",font=FONT_BADGE,text_color=COL_MUTED2).pack(side="left",padx=(0,8))
        ctk.CTkEntry(fr,textvariable=self.scripts_dir,width=290,height=24,font=FONT_MONO_S,
            fg_color=COL_CARD,border_color=COL_BORDER,border_width=1,text_color=COL_WHITE,corner_radius=3).pack(side="left",padx=(0,6))
        _gb(fr,"...",self._pick_scripts_dir,38).pack(side="left")
        row=ctk.CTkFrame(inn,fg_color="transparent");row.pack(fill="x",pady=(8,0))
        _p5b(row,"  DÉCODER TOUT EN JSON",lambda:self._run(self._do_decode_all),230).pack(side="left")
        self._badge_s4=StatusBadge(row);self._badge_s4.pack(side="left",padx=12)

    # ── PANEL P4 (jaune) ──────────────────────────────────────────────────────
    def _build_p4(self,parent):
        PAD={"padx":22,"pady":8}
        t=ctk.CTkFrame(parent,fg_color=P4_BG_CARD,border_color=P4_YELLOW_DRK,border_width=1,corner_radius=5)
        t.pack(fill="x",**PAD)
        ctk.CTkLabel(t,text="  TRADUCTION — ENCODER LES SCRIPTS",font=FONT_TITLE,text_color=P4_YELLOW).pack(anchor="w",padx=14,pady=9)

        # Section encoder UN script
        s1=ctk.CTkFrame(parent,fg_color=COL_CARD,border_color=COL_BORDER,border_width=1,corner_radius=5)
        s1.pack(fill="x",**PAD)
        ctk.CTkFrame(s1,height=3,fg_color=P4_YELLOW,corner_radius=0).pack(fill="x",side="top")
        i1=ctk.CTkFrame(s1,fg_color="transparent");i1.pack(fill="x",padx=16,pady=12)
        ctk.CTkLabel(i1,text="ENCODER UN SEUL SCRIPT",font=FONT_LABEL_B,text_color=P4_YELLOW).pack(anchor="w",pady=(0,6))
        ctk.CTkLabel(i1,text="Sélectionne le JSON traduit ET le .bin original.",font=FONT_BADGE,text_color=COL_MUTED2).pack(anchor="w",pady=(0,8))
        two=ctk.CTkFrame(i1,fg_color="transparent");two.pack(fill="x")
        self.dz_json=FileCard(two,"JSON traduit",[("JSON","*.json"),("Tous","*.*")],lambda p:setattr(self,"_json_to_encode",p),P4_YELLOW)
        self.dz_json.pack(side="left",fill="both",expand=True,padx=(0,8))
        self.dz_bin_orig=FileCard(two,".bin original",[("BIN","*.bin"),("Tous","*.*")],lambda p:setattr(self,"_bin_orig",p),P4_YELLOW)
        self.dz_bin_orig.pack(side="left",fill="both",expand=True)
        r1=ctk.CTkFrame(i1,fg_color="transparent");r1.pack(fill="x",pady=(10,0))
        _p4b(r1,"  ENCODER → script_XX_fr.bin",lambda:self._run(self._do_encode_one),280).pack(side="left")
        self._badge_enc1=StatusBadge(r1);self._badge_enc1.pack(side="left",padx=12)

        _hsep(parent,P4_YELLOW_DRK)

        # Section encoder TOUS
        s2=ctk.CTkFrame(parent,fg_color=COL_CARD,border_color=COL_BORDER,border_width=1,corner_radius=5)
        s2.pack(fill="x",**PAD)
        ctk.CTkFrame(s2,height=3,fg_color=P4_YELLOW,corner_radius=0).pack(fill="x",side="top")
        i2=ctk.CTkFrame(s2,fg_color="transparent");i2.pack(fill="x",padx=16,pady=12)
        ctk.CTkLabel(i2,text="ENCODER TOUS LES JSON D'UN DOSSIER",font=FONT_LABEL_B,text_color=P4_YELLOW).pack(anchor="w",pady=(0,10))
        self.ent_json_dir=_frow(i2,"Dossier JSON :",self.json_dir,self._pick_json_dir,300)
        _frow(i2,"Dossier .bin originaux :",self._bin_dir_all,lambda:self._bin_dir_all.set(filedialog.askdirectory() or self._bin_dir_all.get()),300)
        r2=ctk.CTkFrame(i2,fg_color="transparent");r2.pack(fill="x",pady=(10,0))
        _p4b(r2,"  ENCODER TOUS LES JSON",lambda:self._run(self._do_encode_all),240).pack(side="left")
        self._badge_enc_all=StatusBadge(r2);self._badge_enc_all.pack(side="left",padx=12)
        ctk.CTkFrame(parent,height=18,fg_color="transparent").pack()

    # ── PANEL P3 (bleu) ───────────────────────────────────────────────────────
    def _build_p3(self,parent):
        PAD={"padx":22,"pady":8}
        t=ctk.CTkFrame(parent,fg_color=P3_BG_CARD,border_color=P3_BLUE_DARK,border_width=1,corner_radius=5)
        t.pack(fill="x",**PAD)
        ctk.CTkLabel(t,text="  REBUILD ISO — RÉINJECTION DES SCRIPTS",font=FONT_TITLE,text_color=P3_BLUE).pack(anchor="w",padx=14,pady=9)
        main=ctk.CTkFrame(parent,fg_color=COL_CARD,border_color=COL_BORDER,border_width=1,corner_radius=5)
        main.pack(fill="x",**PAD)
        ctk.CTkFrame(main,height=3,fg_color=P3_BLUE,corner_radius=0).pack(fill="x",side="top")
        inn=ctk.CTkFrame(main,fg_color="transparent");inn.pack(fill="x",padx=16,pady=14)
        self.dz_iso_rebuild=FileCard(inn,"ISO originale",[("ISO","*.iso"),("Tous","*.*")],lambda p:setattr(self,"_iso_for_rebuild",p),P3_BLUE)
        self.dz_iso_rebuild.pack(fill="x",pady=(0,8))
        self.dz_event_rebuild=FileCard(inn,"event.bin original",[("BIN","*.bin"),("Tous","*.*")],lambda p:setattr(self,"_event_for_rebuild",p),P3_BLUE)
        self.dz_event_rebuild.pack(fill="x",pady=(0,12))
        _frow(inn,"Dossier script_XX_fr.bin :",self._fr_bin_dir,lambda:self._fr_bin_dir.set(filedialog.askdirectory() or self._fr_bin_dir.get()),290)
        _frow(inn,"ISO de sortie :",self._out_iso,self._pick_out_iso,290)
        ctk.CTkLabel(inn,text="PROGRESSION",font=FONT_BADGE,text_color=COL_MUTED2).pack(anchor="w",pady=(12,4))
        self._rebuild_progress=ctk.CTkProgressBar(inn,height=7,fg_color=COL_BORDER,progress_color=P3_BLUE,corner_radius=3)
        self._rebuild_progress.set(0);self._rebuild_progress.pack(fill="x",pady=(0,12))
        row=ctk.CTkFrame(inn,fg_color="transparent");row.pack(fill="x")
        _p3b(row,"  CRÉER L'ISO TRADUITE",lambda:self._run(self._do_rebuild_iso),240).pack(side="left")
        self._badge_rebuild=StatusBadge(row);self._badge_rebuild.pack(side="left",padx=12)
        ctk.CTkFrame(parent,height=18,fg_color="transparent").pack()

    # ── CALLBACKS ─────────────────────────────────────────────────────────────
    def _pick_workdir(self):
        d=filedialog.askdirectory()
        if d: self.work_dir.set(d)
    def _pick_scripts_dir(self):
        d=filedialog.askdirectory()
        if d: self.scripts_dir.set(d)
    def _pick_json_dir(self):
        d=filedialog.askdirectory()
        if d: self.json_dir.set(d)
    def _pick_out_iso(self):
        p=filedialog.asksaveasfilename(defaultextension=".iso",filetypes=[("ISO","*.iso")])
        if p: self._out_iso.set(p)
    def _on_iso_selected(self,path): self.iso_path.set(path);self.log(f"ISO: {path}")
    def _on_cpk_selected(self,path): self.cpk_path.set(path);self.log(f"CPK: {path}")
    def _on_event_selected(self,path): self.event_path.set(path);self.log(f"event.bin: {path}")
    def log(self,msg): self.log_box.log(msg)
    def _run(self,func):
        def w():
            try: func()
            except Exception as e: self.log(f"ERREUR: {e}");messagebox.showerror("Erreur",str(e))
        threading.Thread(target=w,daemon=True).start()
    def _workdir(self):
        d=Path(self.work_dir.get());d.mkdir(parents=True,exist_ok=True);return d

    # ── ACTIONS ───────────────────────────────────────────────────────────────
    def _do_extract_cpk(self):
        iso=self.iso_path.get()
        if not iso: messagebox.showwarning("Attention","Sélectionne d'abord une ISO");return
        self._badge_s1.set_state("run");out=self._workdir();self.log("=== Extraction P2PT_ALL.cpk ===")
        try:
            result=extract_cpk_from_iso(iso,out,self.log);self.cpk_path.set(result);self.dz_cpk.set_path(result)
            self.log(f"Termine: {result}");self._badge_s1.set_state("ok")
        except Exception: self._badge_s1.set_state("err");raise

    def _do_extract_event(self):
        cpk=self.cpk_path.get()
        if not cpk: messagebox.showwarning("Attention","Sélectionne d'abord un CPK");return
        self._badge_s2.set_state("run");out=self._workdir();self.log("=== Extraction event.bin ===")
        try:
            result=extract_event_from_cpk(cpk,out,self.log);self.event_path.set(result);self.dz_event.set_path(result)
            self.log(f"Termine: {result}");self._badge_s2.set_state("ok")
        except Exception: self._badge_s2.set_state("err");raise

    def _do_extract_scripts(self):
        ev=self.event_path.get()
        if not ev: messagebox.showwarning("Attention","Sélectionne d'abord event.bin");return
        self._badge_s3.set_state("run");out=self._workdir()/"scripts_bin";self.log("=== Extraction scripts 0-398 ===")
        try:
            count=extract_scripts_from_event(ev,out,self.log);self.scripts_dir.set(str(out))
            self.ent_scripts.delete(0,"end");self.ent_scripts.insert(0,str(out))
            self.log(f"Termine: {count} scripts dans {out}");self._badge_s3.set_state("ok")
        except Exception: self._badge_s3.set_state("err");raise

    def _do_decode_all(self):
        sd=self.scripts_dir.get()
        if not sd: messagebox.showwarning("Attention","Sélectionne le dossier des scripts .bin");return
        self._badge_s4.set_state("run");out=self._workdir()/"scripts_json";self.log("=== Decodage 0-398 en JSON ===")
        try:
            decode_all_scripts(sd,out,self.log);self.json_dir.set(str(out))
            self.ent_json_dir.delete(0,"end");self.ent_json_dir.insert(0,str(out))
            self.log(f"Termine: JSON dans {out}");self._badge_s4.set_state("ok")
            messagebox.showinfo("Terminé",f"JSON générés dans:\n{out}")
        except Exception: self._badge_s4.set_state("err");raise

    def _fr_bin_out_dir(self):
        d=self._workdir()/"scripts_bin_fr";d.mkdir(parents=True,exist_ok=True);return str(d)

    def _do_encode_one(self):
        if not self._json_to_encode or not self._bin_orig:
            messagebox.showwarning("Attention","Sélectionne le JSON et le .bin original");return
        self._badge_enc1.set_state("run");out_dir=self._fr_bin_out_dir()
        self.log(f"=== Encodage {Path(self._json_to_encode).name} ===")
        try:
            result=encode_script(self._bin_orig,self._json_to_encode,self.log,out_dir=out_dir)
            self.log(f"Termine: {result}");self._fr_bin_dir.set(out_dir);self._badge_enc1.set_state("ok")
            messagebox.showinfo("Terminé",f"Fichier créé:\n{result}")
        except Exception: self._badge_enc1.set_state("err");raise


    def _do_encode_all(self):
        json_path = self.json_dir.get()
        base_bin_path = self._bin_dir_all.get()

        if not json_path or not base_bin_path:
            messagebox.showwarning("Attention", "Sélectionnez les deux dossiers.")
            return

        self._badge_enc_all.set_state("run")
        output_dir = self._fr_bin_out_dir()
        self.log(f"=== Encodage : JSON (00x) -> BIN (x) ===")

        try:
            json_dir = Path(json_path)
            bin_dir = Path(base_bin_path)
            success_count = 0

            for json_file in sorted(json_dir.glob("script_*.json")):
                raw_num = json_file.stem.replace("script_", "").replace("_fr", "")       
                try:
                    clean_num = str(int(raw_num))
                    original_bin = bin_dir / f"script_{clean_num}.bin"
                except ValueError:
                    self.log(f"  [SKIP] {json_file.name} : Format de numéro invalide")
                    continue
                if not original_bin.exists():
                    self.log(f"  [SKIP] {json_file.name} : {original_bin.name} introuvable")
                    continue
                try:
                    encode_script(str(original_bin), str(json_file), self.log, out_dir=output_dir)
                    success_count += 1
                except Exception as e:
                    self.log(f"  [ERR] {json_file.name}: {e}")

            self.log(f"Terminé : {success_count} fichiers encodés.")
            self._fr_bin_dir.set(output_dir)
            self._badge_enc_all.set_state("ok")
            messagebox.showinfo("Succès", f"{success_count} scripts encodés.")

        except Exception as e:
            self._badge_enc_all.set_state("err")
            self.log(f"Erreur fatale : {e}")
            raise


    def _do_rebuild_iso(self):
        iso=self._iso_for_rebuild;ev=self._event_for_rebuild;fbd=self._fr_bin_dir.get();out=self._out_iso.get()
        if not iso or not ev or not fbd or not out:
            messagebox.showwarning("Attention","Remplis tous les champs");return
        self._badge_rebuild.set_state("run");self._rebuild_progress.set(0);self._anim_progress()
        self.log("=== Rebuild ISO ===")
        try:
            rebuild_iso(iso,ev,fbd,out,self.log);self.log(f"Termine: {out}")
            self._rebuild_progress.set(1.0);self._badge_rebuild.set_state("ok")
            messagebox.showinfo("Terminé",f"ISO créée:\n{out}")
        except Exception: self._badge_rebuild.set_state("err");raise

    def _anim_progress(self,v=0.0):
        if self._badge_rebuild._state=="run":
            nv=v+0.012
            if nv>0.94: nv=0.0
            self._rebuild_progress.set(nv)
            self.after(70,lambda:self._anim_progress(nv))

if __name__=="__main__":
    app=P2ISApp();app.mainloop()

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

import shutil
from pathlib import Path
from p2is.core.iso import (
    extract_scripts_from_event,
    rebuild_event_bin,
)
from p2is.encoders.bin_encoder import encode_bin_from_json, encode_bnp_from_json
from p2is.encoders.fbe_encoder import encode_fbe_bnp_from_json
def encode_all(
    trad_dir: str, cpk_dir: str, enc_dir: str, log_fn, progress_fn=None, targets=None
) -> dict:
    """Encode tous les JSON traduits en une seule passe (BNP/BIN + event.bin)."""
    jdir = Path(trad_dir)
    cpk = Path(cpk_dir)
    out = Path(enc_dir)
    out.mkdir(parents=True, exist_ok=True)
    cmap = {f.name.lower(): f for f in cpk.rglob("*") if f.is_file()}
    ok_f = []
    err_f = []
    steps = []
    for json_file in jdir.glob("*.json"):
        if json_file.name == "event.json" or json_file.name == "EBOOT_Translation.json":
            continue
        
        # We need to find the matching original file in cpk_files/
        json_name = json_file.name
        # Typically the original file is the json name without .json, but the extension was .BIN or .BNP
        # Let's search in cmap for matching stem
        stem = json_file.stem.lower()
        
        matched_orig = None
        for orig_name, orig_path in cmap.items():
            if orig_path.stem.lower() == stem:
                matched_orig = orig_name
                break
                
        if matched_orig:
            steps.append((json_name, matched_orig, matched_orig.upper()))
            
    if targets:
        steps = [s for s in steps if s[0].replace(".json", "").lower() in [t.lower() for t in targets]]
    
    n = len(steps) + 1
    for i, (jn, on, fn) in enumerate(steps):
        if progress_fn:
            progress_fn((i + 1) / n)
        jp = jdir / jn
        if not jp.exists():
            if log_fn:
                log_fn(f"  {jn} absent → ignoré", "info")
                continue
        op = cmap.get(on)
        if not op:
            if log_fn:
                log_fn(f"  ✗ {on} introuvable dans cpk_files/", "warn")
                err_f.append(fn)
                continue
        try:
            if log_fn:
                log_fn(f"  Encodage {jn}…", "info")
            stem = Path(on).stem.lower()
            if stem in ("f_be", "tm_eve"):
                # Format spécial F_BE/TM_EVE : bytes d'animation intercalés
                encode_fbe_bnp_from_json(
                    str(op), str(jp), log_fn, out_path=str(out / fn)
                )
            elif on.endswith(".bnp"):
                # BNP avec blocs gzip embeddés (MMAP01-06)
                encode_bnp_from_json(str(op), str(jp), log_fn, out_path=str(out / fn))
            else:
                # BIN direct (CD_SHOP.bin)
                encode_bin_from_json(str(op), str(jp), log_fn, out_path=str(out / fn))
            ok_f.append(fn)
        except Exception as e:
            if log_fn:
                log_fn(
                    f"  [ERREUR CRITIQUE] Echec de l'encodage pour {fn} : {str(e)}",
                    "err",
                )
                err_f.append(fn)
    sj = jdir / "event_scripts"
    ep = cmap.get("event.bin")
    if progress_fn:
        progress_fn((n - 1) / n)
        
    do_event = not targets or "event" in [t.lower() for t in targets]
    
    if do_event and ep and sj.exists():
        if log_fn:
            log_fn("  Encodage scripts event.bin…", "info")
        try:
            ev = open(ep, "rb").read()
            tmp = out / "_ev_tmp"
            tmp.mkdir(parents=True, exist_ok=True)
            extract_scripts_from_event(str(ep), tmp, None)
            sc_ok = 0
            for js in sorted(sj.glob("script_*.json")):
                si = js.stem.split("_")[-1].lstrip("0") or "0"
                try:
                    si = int(si)
                except:
                    continue
                bs = tmp / f"script_{si:03d}.bin"
                if not bs.exists():
                    bs = tmp / f"script_{si}.bin"
                if not bs.exists():
                    continue
                try:
                    encode_bin_from_json(
                        str(bs),
                        str(js),
                        None,
                        out_path=str(tmp / f"script_{si:03d}_fr.bin"),
                    )
                    sc_ok += 1
                except:
                    pass
            if log_fn:
                log_fn(f"  {sc_ok} scripts encodés", "info")
            new_ev = rebuild_event_bin(ev, tmp, log_fn, scripts_bin_dir=tmp)
            with open(out / "event.bin", "wb") as f:
                f.write(new_ev)
            ok_f.append("event.bin")
            if log_fn:
                log_fn("  ✓ event.bin reconstruit", "ok")
            shutil.rmtree(str(tmp), ignore_errors=True)
        except Exception as e:
            if log_fn:
                log_fn(f"  ✗ event.bin : {e}", "err")
                err_f.append("event.bin")
    else:
        if log_fn:
            log_fn("  event_scripts/ ou event.bin absent → ignoré", "info")
    if progress_fn:
        progress_fn(1.0)
    if log_fn:
        log_fn(f"\n  Encodés : {', '.join(ok_f) or 'aucun'}", "ok")
        if err_f:
            log_fn(f"  Erreurs : {', '.join(err_f)}", "err")
    return {"ok": ok_f, "err": err_f}

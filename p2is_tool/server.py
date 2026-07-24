import os
import sys
import json
import subprocess
import threading
from pathlib import Path
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import tkinter as tk
from tkinter import filedialog

app = FastAPI(title="P2IS Tool Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.core.iso import (
    extract_cpk_from_iso,
    rebuild_iso,
    scan_cpk_files,
    extract_event_from_cpk,
    extract_scripts_from_event,
)
from src.parsers.bin_parser import decode_all_scripts, validate_all_scripts
from src.parsers.eboot_parser import extract_eboot, inject_eboot
from src.encoders.pipeline import encode_all

# État global pour la progression
progress_state = {"current": 0, "task": ""}
progress_lock = threading.Lock()


def update_progress(percent: float):
    with progress_lock:
        progress_state["current"] = int(percent * 100)


@app.get("/api/progress")
async def get_progress():
    with progress_lock:
        return progress_state


def reset_progress(task_name: str):
    with progress_lock:
        progress_state["task"] = task_name
        progress_state["current"] = 0


class GenericRequest(BaseModel):
    work_dir: str
    pspdecrypt_path: str = ""
    targets: Optional[List[str]] = None

class IsoRequest(BaseModel):
    iso_path: str
    work_dir: str
    pspdecrypt_path: str = ""


class BrowseRequest(BaseModel):
    type: str  # "dir" or "file"
    ext: str = ""  # e.g. ".iso"


class CrifsRequest(BaseModel):
    crifs_path: str


import src.config


def set_work_dir(work_dir: str):
    if work_dir:
        Path(work_dir).mkdir(parents=True, exist_ok=True)
    src.config.OFFSETS_FILE = str(Path(work_dir) / "offsets.json")


def get_logger(work_dir=None):
    def dummy_log(msg, level="info"):
        try:
            print(
                f"[{level.upper()}] {msg}".encode(
                    sys.stdout.encoding, errors="replace"
                ).decode(sys.stdout.encoding)
            )
        except Exception:
            pass
        try:
            if work_dir:
                log_dir = os.path.join(work_dir, "logs")
                os.makedirs(log_dir, exist_ok=True)
                with open(
                    os.path.join(log_dir, "server.log"), "a", encoding="utf-8"
                ) as f:
                    f.write(f"[{level.upper()}] {msg}\n")
        except Exception:
            pass

    return dummy_log


@app.post("/api/browse")
async def api_browse(req: BrowseRequest):
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    path = ""
    if req.type == "dir":
        path = filedialog.askdirectory(title="Sélectionner un dossier")
    else:
        filetypes = (
            [("Fichiers", f"*{req.ext}")] if req.ext else [("Tous les fichiers", "*.*")]
        )
        path = filedialog.askopenfilename(
            title="Sélectionner un fichier", filetypes=filetypes
        )

    root.destroy()
    return {"path": path.replace("/", "\\")}


@app.post("/api/open-folder")
def api_open_folder(req: GenericRequest):
    w = Path(req.work_dir)
    if w.exists():
        os.startfile(str(w))
    return {"status": "ok"}

@app.get("/api/default-paths")
def api_default_paths():
    return {"work_dir": r"C:\Users\user\Desktop\P2IS_FR"}


@app.post("/api/extract-cpk")
def api_extract_cpk(req: IsoRequest):
    set_work_dir(req.work_dir)
    iso = Path(req.iso_path)
    if not iso.exists():
        raise HTTPException(status_code=400, detail="ISO introuvable")
    w = Path(req.work_dir)
    w.mkdir(parents=True, exist_ok=True)
    res = extract_cpk_from_iso(str(iso), w, get_logger(req.work_dir), req.pspdecrypt_path)
    if not res:
        raise HTTPException(status_code=500, detail="Erreur lors de l'extraction CPK")
    return {"status": "ok", "msg": f"CPK et EBOOT extraits : {res}"}


@app.post("/api/open-crifslib")
def api_open_crifslib(req: CrifsRequest):
    exe_path = Path(req.crifs_path)
    if not exe_path.exists():
        raise HTTPException(
            status_code=400, detail=f"CriFsLib introuvable dans {exe_path.absolute()}"
        )
    subprocess.Popen([str(exe_path)])
    return {"status": "ok", "msg": "CriFsLib ouvert"}


@app.post("/api/extract-event")
def api_extract_event(req: GenericRequest):
    set_work_dir(req.work_dir)
    cpk = Path(req.work_dir) / "P2PT_ALL.cpk"
    if not cpk.exists():
        raise HTTPException(
            status_code=400,
            detail="P2PT_ALL.cpk introuvable. Avez-vous fait l'étape A ?",
        )
    res = extract_event_from_cpk(str(cpk), Path(req.work_dir), get_logger(req.work_dir))
    if not res:
        raise HTTPException(
            status_code=500, detail="Erreur lors de l'extraction event.bin"
        )
    return {"status": "ok", "msg": f"event.bin extrait : {res}"}


@app.post("/api/split-scripts")
def api_split_scripts(req: GenericRequest):
    ev = Path(req.work_dir) / "event.bin"
    if not ev.exists():
        raise HTTPException(
            status_code=400, detail="event.bin introuvable. Avez-vous fait l'étape C ?"
        )
    out = Path(req.work_dir) / "scripts_bin"
    out.mkdir(parents=True, exist_ok=True)
    extract_scripts_from_event(str(ev), out, get_logger(req.work_dir))
    return {"status": "ok", "msg": "Scripts séparés avec succès."}


@app.post("/api/decode-eboot")
def api_decode_eboot(req: GenericRequest):
    try:
        w = Path(req.work_dir)
        eboot_dec = w / "EBOOT_DECRYPTED.BIN"
        out_dir = w / "traduction"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_json = out_dir / "EBOOT_Translation.json"
        
        if not eboot_dec.exists():
            raise HTTPException(status_code=400, detail="EBOOT_DECRYPTED.BIN introuvable. Extraire l'ISO d'abord.")
        
        reset_progress("decode-eboot")
        extract_eboot(str(eboot_dec), str(out_json), get_logger(req.work_dir))
        return {"status": "ok", "msg": "EBOOT décodé avec succès !"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/decode-scripts")
def api_decode_scripts(req: GenericRequest):
    try:
        w = Path(req.work_dir)
        scripts_dir = w / "scripts_bin"
        out_dir = w / "traduction" / "event_scripts"
        if not scripts_dir.exists():
            raise HTTPException(status_code=400, detail="scripts_bin introuvable.")
        reset_progress("decode-scripts")
        decode_all_scripts(
            scripts_dir, out_dir, get_logger(req.work_dir), progress_fn=update_progress
        )
        update_progress(1.0)
        return {"status": "ok", "msg": "Scripts décodés (JSON)."}
    except Exception as e:
        import traceback

        err_msg = traceback.format_exc()
        logger = get_logger(req.work_dir)
        logger(f"CRASH in decode_scripts: {err_msg}", "error")
        raise HTTPException(status_code=500, detail=f"Erreur interne : {str(e)}")


@app.post("/api/scan-secondary")
def api_scan_secondary(req: GenericRequest):
    try:
        set_work_dir(req.work_dir)
        w = Path(req.work_dir)
        cpk_dir = w / "cpk_files"
        out_dir = w / "traduction"
        if not cpk_dir.exists():
            raise HTTPException(
                status_code=400,
                detail="cpk_files introuvable. Avez-vous fait l'étape B ?",
            )
        reset_progress("scan-secondary")
        scan_cpk_files(
            str(cpk_dir), out_dir, get_logger(req.work_dir), progress_fn=update_progress
        )
        update_progress(1.0)
        return {"status": "ok", "msg": "Fichiers annexes extraits (JSON)."}
    except Exception as e:
        import traceback

        logger = get_logger(req.work_dir)
        logger(f"CRASH in scan_secondary: {traceback.format_exc()}", "error")
        raise HTTPException(status_code=500, detail=f"Erreur interne : {str(e)}")


@app.post("/api/validate")
def api_validate(req: GenericRequest):
    src = Path(req.work_dir) / "traduction" / "event_scripts"
    if not src.exists():
        raise HTTPException(
            status_code=400, detail="Dossier event_scripts introuvable."
        )
    res = validate_all_scripts(str(src), get_logger(req.work_dir))
    return {
        "status": "ok",
        "msg": f"Validation terminée. Problèmes détectés : {len(res.get('problems', []))}",
    }


@app.post("/api/encode")
def api_encode(req: GenericRequest):
    try:
        w = Path(req.work_dir)
        trad_dir = w / "traduction"
        cpk_dir = w / "cpk_files"
        enc_dir = w / "encoded"
        if not trad_dir.exists() or not cpk_dir.exists():
            raise HTTPException(
                status_code=400, detail="Dossiers de traduction ou cpk_files manquants."
            )
        reset_progress("encode")
        res = encode_all(
            str(trad_dir),
            str(cpk_dir),
            str(enc_dir),
            get_logger(req.work_dir),
            progress_fn=update_progress,
            targets=req.targets,
        )
        update_progress(1.0)
        
        # Encodage de l'EBOOT (seulement si cible 'eboot' ou toutes)
        if not req.targets or "eboot" in req.targets:
            eboot_dec = w / "EBOOT_DECRYPTED.BIN"
            eboot_json = trad_dir / "EBOOT_Translation.json"
            eboot_out = w / "EBOOT_MODIFIED.BIN"
            if eboot_dec.exists() and eboot_json.exists():
                get_logger(req.work_dir)("Encodage de l'EBOOT en cours...", "info")
                inject_eboot(str(eboot_dec), str(eboot_json), str(eboot_out), get_logger(req.work_dir))
            
        return {"status": "ok", "msg": "Encodage terminé !", "result": res}
    except Exception as e:
        import traceback

        logger = get_logger(req.work_dir)
        logger(f"CRASH in encode: {traceback.format_exc()}", "error")
        raise HTTPException(status_code=500, detail=f"Erreur interne : {str(e)}")


@app.post("/api/rebuild")
def api_rebuild(req: IsoRequest):
    try:
        set_work_dir(req.work_dir)
        iso_orig = Path(req.iso_path)
        w = Path(req.work_dir)
        enc_dir = w / "encoded"
        out_iso = w / "P2IS_FR.iso"
        if not iso_orig.exists() or not enc_dir.exists():
            raise HTTPException(
                status_code=400,
                detail="ISO originale ou dossiers d'encodage manquants.",
            )
        event_bin_path = enc_dir / "event.bin"
        if not event_bin_path.exists():
            raise HTTPException(
                status_code=400, detail="event.bin manquant dans le dossier encoded."
            )

        reset_progress("rebuild")
        # Fake progress since rebuild_iso doesn't support it
        update_progress(0.5)

        with open(event_bin_path, "rb") as f:
            event_data = f.read()

        rebuild_iso(
            str(iso_orig),
            event_data,
            str(out_iso),
            get_logger(req.work_dir),
            enc_dir=str(enc_dir),
        )
        update_progress(1.0)
        return {"status": "ok", "out_iso": str(out_iso)}
    except Exception as e:
        import traceback

        logger = get_logger(req.work_dir)
        logger(f"CRASH in rebuild: {traceback.format_exc()}", "error")
        raise HTTPException(status_code=500, detail=f"Erreur interne : {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)

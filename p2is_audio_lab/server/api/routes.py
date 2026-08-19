from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pathlib import Path
from core.audio_format import parse_bin_toc, extract_entry, inject_wav_into_bin
from core.ffmpeg import prepare_wav_for_injection
import tkinter as tk
from tkinter import filedialog
import os
import traceback
from core.iso_builder import patch_iso

router = APIRouter()

class InfoRequest(BaseModel):
    bin_path: str

class ExtractRequest(BaseModel):
    bin_path: str
    out_dir: str
    start_idx: int = 0
    end_idx: int = -1

class InjectRequest(BaseModel):
    bin_path: str
    wav_path: str
    out_bin_path: str
    voice_index: int
    at3tool_path: str = None

class BrowseRequest(BaseModel):
    type: str
    ext: str = ""

@router.post("/browse")
async def browse(req: BrowseRequest):
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    path = ""
    if req.type == "dir":
        path = filedialog.askdirectory()
    else:
        ft = [(f"{req.ext} files", f"*{req.ext}")] if req.ext else [("All files", "*.*")]
        path = filedialog.askopenfilename(filetypes=ft)
    root.destroy()
    return {"path": path.replace("/", "\\")}

@router.post("/audio/info")
async def audio_info(req: InfoRequest):
    if not os.path.exists(req.bin_path):
        raise HTTPException(404, "Fichier introuvable.")
    try:
        entries, toc_end = parse_bin_toc(req.bin_path)
        total = sum(1 for e in entries if e is not None)
        return {"status": "ok", "total": total, "toc_end": toc_end}
    except Exception as e:
        raise HTTPException(500, str(e))

from core.logger import get_logger
import tempfile
import subprocess
from core.ffmpeg import find_ffmpeg

logger = get_logger()

@router.post("/audio/extract")
async def audio_extract(req: ExtractRequest):
    logger.info(f"DÃ©but de l'extraction pour {req.bin_path} vers {req.out_dir}")
    if not os.path.exists(req.bin_path):
        logger.error(f"Fichier introuvable: {req.bin_path}")
        raise HTTPException(404, "Fichier introuvable.")
    out_dir = Path(req.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    
    entries, _ = parse_bin_toc(req.bin_path)
    start = req.start_idx
    end = req.end_idx if req.end_idx >= 0 else len(entries) - 1
    
    count = 0
    ffmpeg_exe = find_ffmpeg()
    
    for i in range(start, min(end + 1, len(entries))):
        if entries[i] is None:
            continue
        offset, size = entries[i]
        data = extract_entry(req.bin_path, offset, size)
        ext = ".wav" if data[:4] == b"RIFF" else ".bin"
        
        # Convertir en PCM lisible (pour Audacity) si c'est un WAV ATRAC3
        if ext == ".wav" and ffmpeg_exe:
            try:
                fd_in, tmp_in_name = tempfile.mkstemp(suffix=".wav")
                with os.fdopen(fd_in, 'wb') as f:
                    f.write(data)
                
                fd_out, tmp_out_name = tempfile.mkstemp(suffix=".wav")
                os.close(fd_out)
                
                res = subprocess.run([
                    ffmpeg_exe, "-y", "-i", tmp_in_name,
                    "-acodec", "pcm_s16le", "-ar", "44100", "-ac", "2",
                    "-map_metadata", "-1", "-fflags", "+bitexact",
                    tmp_out_name
                ], capture_output=True)
                
                if res.returncode == 0 and os.path.getsize(tmp_out_name) > 0:
                    with open(tmp_out_name, "rb") as f:
                        data = f.read()
                    logger.debug(f"Piste {i} convertie en PCM standard avec succÃ¨s.")
                else:
                    logger.warning(f"Ã‰chec conversion piste {i}: {res.stderr.decode('utf-8', errors='ignore')}")
                
                try:
                    os.unlink(tmp_in_name)
                    os.unlink(tmp_out_name)
                except:
                    pass
            except Exception as e:
                logger.error(f"Erreur ffmpeg sur piste {i}: {e}")
                
        out_file = out_dir / f"track_{i:05d}{ext}"
        with open(out_file, "wb") as f:
            f.write(data)
        logger.debug(f"Piste {i} sauvegardÃ©e dans {out_file} (Taille: {len(data)} octets)")
        count += 1
        
    logger.info(f"Extraction terminÃ©e : {count} fichiers extraits.")
    return {"status": "ok", "msg": f"{count} fichiers extraits avec succÃ¨s !"}

@router.post("/audio/inject")
async def audio_inject(req: InjectRequest):
    if not os.path.exists(req.bin_path):
        raise HTTPException(404, "BIN introuvable.")
    if not os.path.exists(req.wav_path):
        raise HTTPException(404, "WAV introuvable.")
        
    actual_bin_path = req.bin_path
    if os.path.exists(req.out_bin_path):
        actual_bin_path = req.out_bin_path
        logger.info(f"Chaining: utilisation du fichier existant {req.out_bin_path}")
        
    entries, toc_end = parse_bin_toc(actual_bin_path)
    if req.voice_index < 0 or req.voice_index >= len(entries):
        raise HTTPException(400, "Index invalide.")
        
    try:
        # Lire les mÃ©tadonnÃ©es de la piste originale pour respecter son format (Mono/StÃ©rÃ©o)
        offset, size = entries[req.voice_index]
        orig_data = extract_entry(actual_bin_path, offset, size)
        
        target_channels = 1
        target_sr = 44100
        if orig_data.startswith(b'RIFF') and len(orig_data) > 36:
            import struct
            target_channels = struct.unpack('<H', orig_data[22:24])[0]
            target_sr = struct.unpack('<I', orig_data[24:28])[0]
            logger.info(f"Piste originale dÃ©tectÃ©e : {target_channels} canaux, {target_sr} Hz")
            
        new_wav_data = prepare_wav_for_injection(req.wav_path, req.at3tool_path, target_channels, target_sr)
        def log(msg, lvl):
            logger.info(f"[{lvl}] {msg}")
            
        temp_out_path = req.out_bin_path + ".tmp"
        ok = inject_wav_into_bin(actual_bin_path, req.voice_index, new_wav_data,
                                 entries, toc_end, temp_out_path, log_fn=log)
        if not ok:
            if os.path.exists(temp_out_path):
                os.unlink(temp_out_path)
            raise HTTPException(500, "Taille trop grande ou Ã©chec de l'injection.")
            
        # Remplacer le fichier out_bin_path
        if os.path.exists(req.out_bin_path):
            os.remove(req.out_bin_path)
        os.rename(temp_out_path, req.out_bin_path)
            
        return {"status": "ok", "msg": f"Voix {req.voice_index} injectÃ©e avec succÃ¨s !"}
    except Exception as e:
        logger.error(f"Erreur d'injection: {e}")
        raise HTTPException(500, str(e))

from fastapi.responses import Response
import json

@router.get("/audio/stream")
async def audio_stream(bin_path: str, index: int):
    if not os.path.exists(bin_path):
        raise HTTPException(404, "Fichier introuvable.")
    entries, _ = parse_bin_toc(bin_path)
    if index < 0 or index >= len(entries) or entries[index] is None:
        raise HTTPException(404, "Index invalide ou piste vide.")
    
    offset, size = entries[index]
    data = extract_entry(bin_path, offset, size)
    
    # On convertit Ã  la volÃ©e en PCM standard (les navigateurs ne lisent pas le ATRAC3)
    if data[:4] == b"RIFF":
        import tempfile, subprocess
        from core.ffmpeg import find_ffmpeg
        
        ffmpeg_exe = find_ffmpeg()
        if ffmpeg_exe:
            import tempfile
            fd_in, tmp_in_name = tempfile.mkstemp(suffix=".wav")
            with os.fdopen(fd_in, 'wb') as f:
                f.write(data)
            
            fd_out, tmp_out_name = tempfile.mkstemp(suffix=".wav")
            os.close(fd_out) # Fermer pour que ffmpeg puisse Ã©crire
                
            # Convertir
            subprocess.run([
                ffmpeg_exe, "-y", "-i", tmp_in_name,
                "-acodec", "pcm_s16le", "-ar", "22050", "-ac", "1",
                tmp_out_name
            ], capture_output=True)
            
            if os.path.exists(tmp_out_name) and os.path.getsize(tmp_out_name) > 0:
                with open(tmp_out_name, "rb") as f:
                    data = f.read()
            
            try:
                os.unlink(tmp_in_name)
                os.unlink(tmp_out_name)
            except:
                pass
                
        content_type = "audio/wav"
    else:
        content_type = "application/octet-stream"
    
    return Response(content=data, media_type=content_type)

class NotesRequest(BaseModel):
    bin_path: str
    notes: dict

@router.post("/audio/notes/save")
async def save_notes(req: NotesRequest):
    bin_name = os.path.basename(req.bin_path)
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    notes_dir = os.path.join(base_dir, "notes")
    os.makedirs(notes_dir, exist_ok=True)
    notes_file = os.path.join(notes_dir, f"{bin_name}_notes.json")
    with open(notes_file, 'w', encoding='utf-8') as f:
        json.dump(req.notes, f, ensure_ascii=False, indent=2)
    return {"status": "ok"}

@router.post("/audio/notes/load")
async def load_notes(req: InfoRequest):
    bin_name = os.path.basename(req.bin_path)
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    notes_dir = os.path.join(base_dir, "notes")
    notes_file = os.path.join(notes_dir, f"{bin_name}_notes.json")
    if os.path.exists(notes_file):
        try:
            with open(notes_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            return {}
    return {}

class PatchIsoRequest(BaseModel):
    iso_path: str
    bin_path: str
    internal_path: str
    out_iso_path: str

@router.post("/iso/patch")
async def patch_iso_route(req: PatchIsoRequest):
    if not os.path.exists(req.iso_path):
        raise HTTPException(404, "Fichier ISO original introuvable.")
    if not os.path.exists(req.bin_path):
        raise HTTPException(404, "Fichier BIN modifiÃ© introuvable.")
        
    ok = patch_iso(req.iso_path, req.bin_path, req.internal_path, req.out_iso_path)
    if ok != True:
        err_msg = ok if isinstance(ok, str) else "Erreur inconnue."
        raise HTTPException(500, f"Erreur lors de la reconstruction de l'ISO: {err_msg}")
        
    return {"status": "ok", "msg": "Nouvel ISO gÃ©nÃ©rÃ© avec succÃ¨s !"}

from pydantic import BaseModel

class ExtractReq(BaseModel):
    iso_path: str
    out_dir: str

@router.post("/iso/extract")
def extract_iso(req: ExtractReq):
    from core.iso_builder import extract_audio_from_iso
    result = extract_audio_from_iso(req.iso_path, req.out_dir)
    if "error" in result:
        raise HTTPException(500, detail=result["error"])
    return {"msg": "Extraction terminee", "details": result.get("details", {})}

@router.get("/desktop")
async def get_desktop():
    import os
    return {"path": os.path.join(os.path.expanduser("~"), "Desktop", "P2IS_FR_audio")}



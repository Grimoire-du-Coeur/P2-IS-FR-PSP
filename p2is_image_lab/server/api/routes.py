from fastapi import APIRouter, HTTPException, File, UploadFile, Form
from pydantic import BaseModel
from pathlib import Path
from core.image_format import scan_bin_for_gims, extract_gim_entry, parse_gim, render_gim, inject_gim_into_bin
from core.iso_builder import extract_cpk_from_iso
from core.cpk_tool import extract_cpk
import tkinter as tk
from tkinter import filedialog
import os
import io
import json
import shutil
from fastapi.responses import Response
from core.logger import get_logger

router = APIRouter()
logger = get_logger()

class InitProjectRequest(BaseModel):
    iso_path: str
    workspace_dir: str

@router.post("/project/init")
async def project_init(req: InitProjectRequest):
    iso_path = req.iso_path
    workspace_dir = req.workspace_dir
    
    if not os.path.exists(iso_path):
        raise HTTPException(404, "Le fichier ISO est introuvable.")
        
    try:
        os.makedirs(workspace_dir, exist_ok=True)
        
        orig_cpk_path = os.path.join(workspace_dir, "_original.cpk")
        extracted_cpk_dir = os.path.join(workspace_dir, "extracted_cpk")
        
        # 1. Extraire le CPK original depuis l'ISO
        logger.info(f"Extraction du CPK depuis {iso_path}...")
        extract_cpk_from_iso(iso_path, orig_cpk_path)
        
        # 2. Extraire les fichiers bin/bnp du CPK
        logger.info(f"Extraction des fichiers du CPK vers {extracted_cpk_dir}...")
        extract_cpk(orig_cpk_path, extracted_cpk_dir)
        
        return {"status": "ok", "cpk_dir": extracted_cpk_dir}
    except Exception as e:
        logger.error(f"Erreur init_project: {e}")
        raise HTTPException(500, f"Erreur lors de l'initialisation du projet: {e}")

STAGING_DIR = Path("staging")
STAGING_DIR.mkdir(exist_ok=True)
STAGING_JSON = STAGING_DIR / "queue.json"

def get_queue():
    if STAGING_JSON.exists():
        try:
            with open(STAGING_JSON, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def save_queue(q):
    with open(STAGING_JSON, "w") as f:
        json.dump(q, f, indent=2)

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

class InfoRequest(BaseModel):
    bin_path: str
    ignore_atlus: bool = True

@router.post("/image/info")
async def image_info(req: InfoRequest):
    if not os.path.exists(req.bin_path):
        raise HTTPException(404, "Fichier introuvable.")
    try:
        gims = scan_bin_for_gims(req.bin_path, req.ignore_atlus)
        return {"status": "ok", "total": len(gims), "gims": gims}
    except Exception as e:
        logger.error(f"Erreur scan_bin: {e}")
        raise HTTPException(500, str(e))

class ScanFolderRequest(BaseModel):
    folder_path: str
    ignore_atlus: bool = True

@router.post("/image/scan_folder")
async def scan_folder(req: ScanFolderRequest):
    if not os.path.exists(req.folder_path) or not os.path.isdir(req.folder_path):
        raise HTTPException(404, "Dossier introuvable.")
    
    files_with_images = []
    try:
        for root, _, files in os.walk(req.folder_path):
            for file in files:
                ext = file.lower()
                if ext.endswith('.bin') or ext.endswith('.bnp') or ext.endswith('.gim'):
                    full_path = os.path.join(root, file)
                    try:
                        with open(full_path, 'rb') as f:
                            import mmap
                            try:
                                with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                                    if mm.find(b'MIG.00.1PSP') != -1:
                                        rel_path = os.path.relpath(full_path, req.folder_path)
                                        files_with_images.append({
                                            "name": file,
                                            "rel_path": rel_path,
                                            "full_path": full_path
                                        })
                            except ValueError:
                                pass
                    except:
                        pass
        return {"status": "ok", "files": files_with_images}
    except Exception as e:
        logger.error(f"Erreur scan_folder: {e}")
        raise HTTPException(500, str(e))

@router.get("/image/preview")
async def image_preview(bin_path: str, offset: int, size: int, is_archive: bool = False, archive_type: str = "", chunk_index: int = -1, chunk_offset: int = 0, chunk_size: int = 0, is_compressed: bool = False, inner_offset: int = 0):
    if not os.path.exists(bin_path):
        raise HTTPException(404, "Fichier introuvable.")
    
    try:
        data = extract_gim_entry(bin_path, offset, size, is_archive, archive_type, chunk_index, chunk_offset, chunk_size, is_compressed, inner_offset)
        imgs, pal, _ = parse_gim(data, 0)
        
        if not imgs:
            raise HTTPException(500, "Impossible de parser le GIM (ou format inconnu).")
            
        img = render_gim(data, imgs[0], pal)
        if not img:
            raise HTTPException(500, "Erreur lors du rendu du GIM.")
            
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return Response(content=buf.getvalue(), media_type="image/png")
    except Exception as e:
        logger.error(f"Erreur preview: {e}")
        raise HTTPException(500, str(e))

class ExtractRequest(BaseModel):
    is_archive: bool = False
    archive_type: str = ""
    chunk_index: int = -1
    chunk_offset: int = 0
    chunk_size: int = 0
    is_compressed: bool = False
    inner_offset: int = 0
    bin_path: str
    out_dir: str
    index: int
    offset: int
    size: int
    format: str # 'gim' or 'png'

class ExtractAllRequest(BaseModel):
    bin_path: str
    out_dir: str
    format: str = "png" # "png" ou "gim"
    ignore_atlus: bool = True

@router.post("/image/extract_all")
async def extract_all(req: ExtractAllRequest):
    if not os.path.exists(req.bin_path):
        raise HTTPException(404, "Fichier introuvable.")
        
    out_dir = Path(req.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        from core.image_format import scan_bin_for_gims
        gims = scan_bin_for_gims(req.bin_path, req.ignore_atlus)
        
        extracted = 0
        for gim in gims:
            try:
                data = extract_gim_entry(req.bin_path, gim['offset'], gim['size'], gim.get('is_archive', False), gim.get('archive_type', ''), gim.get('chunk_index', -1), gim.get('chunk_offset', 0), gim.get('chunk_size', 0), gim.get('is_compressed', False), gim.get('inner_offset', 0))
                base_name = f"image_{gim['index']:03d}_{gim['offset']:x}"
                
                if req.format == "png":
                    imgs, pal, _ = parse_gim(data, 0)
                    if imgs:
                        img = render_gim(data, imgs[0], pal)
                        if img:
                            out_file = out_dir / f"{base_name}.png"
                            img.save(out_file, format="PNG")
                            extracted += 1
                else:
                    out_file = out_dir / f"{base_name}.gim"
                    with open(out_file, "wb") as f:
                        f.write(data)
                    extracted += 1
            except:
                pass
                
        return {"status": "ok", "msg": f"{extracted} images extraites dans {req.out_dir}"}
    except Exception as e:
        logger.error(f"Erreur extract_all: {e}")
        raise HTTPException(500, str(e))

class ExtractAllGlobalRequest(BaseModel):
    folder_path: str
    format: str = "png"
    ignore_atlus: bool = True

@router.post("/image/extract_all_global")
async def extract_all_global(req: ExtractAllGlobalRequest):
    if not os.path.exists(req.folder_path):
        raise HTTPException(404, "Dossier introuvable.")
        
    out_dir = Path(req.folder_path) / "Export_All"
    out_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        from core.image_format import scan_bin_for_gims
        
        extracted = 0
        total_files = 0
        for root, _, files in os.walk(req.folder_path):
            if "Export_All" in root: continue
            for file in files:
                ext = file.lower()
                if ext.endswith('.bin') or ext.endswith('.bnp') or ext.endswith('.gim'):
                    full_path = os.path.join(root, file)
                    total_files += 1
                    try:
                        gims = scan_bin_for_gims(full_path, req.ignore_atlus)
                        for gim in gims:
                            try:
                                data = extract_gim_entry(full_path, gim['offset'], gim['size'], gim.get('is_archive', False), gim.get('archive_type', ''), gim.get('chunk_index', -1), gim.get('chunk_offset', 0), gim.get('chunk_size', 0), gim.get('is_compressed', False), gim.get('inner_offset', 0))
                                base_name = f"{file}_image_{gim['index']:03d}_{gim['offset']:x}"
                                
                                if req.format == "png":
                                    imgs, pal, _ = parse_gim(data, 0)
                                    if imgs:
                                        img = render_gim(data, imgs[0], pal)
                                        if img:
                                            out_file = out_dir / f"{base_name}.png"
                                            img.save(out_file, format="PNG")
                                            extracted += 1
                                else:
                                    out_file = out_dir / f"{base_name}.gim"
                                    with open(out_file, "wb") as f:
                                        f.write(data)
                                    extracted += 1
                            except:
                                pass
                    except:
                        pass
                
        return {"status": "ok", "msg": f"{extracted} images extraites de {total_files} fichiers dans {out_dir.name}"}
    except Exception as e:
        logger.error(f"Erreur extract_all_global: {e}")
        raise HTTPException(500, str(e))


@router.post("/image/extract")
async def image_extract(req: ExtractRequest):
    if not os.path.exists(req.bin_path):
        raise HTTPException(404, "Fichier introuvable.")
        
    out_dir = Path(req.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        data = extract_gim_entry(req.bin_path, req.offset, req.size, req.is_archive, req.archive_type, req.chunk_index, req.chunk_offset, req.chunk_size, req.is_compressed, req.inner_offset)
        base_name = f"image_{req.index:03d}_{req.offset:x}"
        
        if req.format == "png":
            imgs, pal, _ = parse_gim(data, 0)
            if not imgs:
                raise HTTPException(500, "Impossible de parser le GIM.")
            img = render_gim(data, imgs[0], pal)
            out_file = out_dir / f"{base_name}.png"
            img.save(out_file, format="PNG")
        else:
            out_file = out_dir / f"{base_name}.gim"
            with open(out_file, "wb") as f:
                f.write(data)
                
        return {"status": "ok", "msg": f"Image extraite : {out_file.name}"}
    except Exception as e:
        logger.error(f"Erreur extraction: {e}")
        raise HTTPException(500, str(e))

class InjectRequest(BaseModel):
    is_archive: bool = False
    archive_type: str = ""
    chunk_index: int = -1
    chunk_offset: int = 0
    chunk_size: int = 0
    is_compressed: bool = False
    inner_offset: int = 0
    bin_path: str
    gim_path: str
    out_bin_path: str
    target_offset: int
    target_size: int

@router.post("/image/inject")
async def image_inject(req: InjectRequest):
    if not os.path.exists(req.bin_path):
        raise HTTPException(404, "Fichier BIN introuvable.")
    if not os.path.exists(req.gim_path):
        raise HTTPException(404, "Fichier GIM de remplacement introuvable.")
        
    actual_bin_path = req.bin_path
    if os.path.exists(req.out_bin_path):
        actual_bin_path = req.out_bin_path
        
    try:
        with open(req.gim_path, "rb") as f:
            new_gim_data = f.read()
            
        temp_out = req.out_bin_path + ".tmp"
        
        def log_fn(msg, lvl):
            logger.info(f"[{lvl}] {msg}")
            
        inject_gim_into_bin(actual_bin_path, req.target_offset, req.target_size, new_gim_data, temp_out, req.is_archive, req.archive_type, req.chunk_index, req.chunk_offset, req.chunk_size, req.is_compressed, req.inner_offset, log_fn=log_fn)
        
        if os.path.exists(req.out_bin_path):
            os.remove(req.out_bin_path)
        os.rename(temp_out, req.out_bin_path)
        
        return {"status": "ok", "msg": "Texture injectée avec succès !"}
    except Exception as e:
        logger.error(f"Erreur injection: {e}")
        raise HTTPException(500, str(e))

@router.get("/queue/list")
async def queue_list():
    return {"queue": get_queue()}

@router.post("/queue/clear")
async def queue_clear():
    save_queue([])
    for f in STAGING_DIR.glob("*"):
        if f.is_file() and f.name != "queue.json":
            f.unlink()
    return {"status": "ok"}

@router.post("/queue/add")
async def queue_add(
    bin_path: str = Form(...),
    target_offset: int = Form(...),
    target_size: int = Form(...),
    index: int = Form(...),
    is_archive: bool = Form(False),
    archive_type: str = Form(""),
    chunk_index: int = Form(-1),
    chunk_offset: int = Form(0),
    chunk_size: int = Form(0),
    is_compressed: bool = Form(False),
    inner_offset: int = Form(0),
    file: UploadFile = File(...)
):
    q = get_queue()
    bin_name = Path(bin_path).name
    ext = Path(file.filename).suffix.lower()
    
    new_filename = f"{bin_name}_0x{target_offset:x}{ext}"
    dest_path = STAGING_DIR / new_filename
    
    with open(dest_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
        
    item = {
        "bin_path": bin_path,
        "bin_name": bin_name,
        "offset": target_offset,
        "size": target_size,
        "index": index,
        "filename": new_filename,
        "staging_path": str(dest_path.absolute())
    }
    
    q = [x for x in q if x["bin_path"] != bin_path or x["offset"] != target_offset]
    q.append(item)
    save_queue(q)
    
    return {"status": "ok", "msg": "Ajouté à la file d'attente"}

from core.gim_encoder import encode_png_to_gim_in_place

@router.post("/build/apply")
async def build_apply():
    q = get_queue()
    if not q:
        return {"status": "ok", "success_count": 0, "errors": []}
        
    errors = []
    success = 0
    
    for item in q:
        try:
            bin_path = item["bin_path"]
            staging_path = item["staging_path"]
            offset = item["offset"]
            size = item["size"]
            
            # Read original GIM chunk
            orig_chunk = extract_gim_entry(bin_path, offset, size, item.get("is_archive", False), item.get("archive_type", ""), item.get("chunk_index", -1), item.get("chunk_offset", 0), item.get("chunk_size", 0), item.get("is_compressed", False), item.get("inner_offset", 0))
            
            # If user uploaded a PNG, encode it. If it's already a GIM, use it directly.
            if staging_path.lower().endswith('.png'):
                new_chunk = encode_png_to_gim_in_place(staging_path, orig_chunk)
            else:
                with open(staging_path, "rb") as f:
                    new_chunk = f.read()
                    
            if len(new_chunk) > size:
                errors.append(f"{item['filename']}: GIM généré trop grand ({len(new_chunk)} > {size})")
                continue
                
            # Inject into BIN
            temp_out = bin_path + ".tmp"
            inject_gim_into_bin(bin_path, offset, size, new_chunk, temp_out, item.get("is_archive", False), item.get("archive_type", ""), item.get("chunk_index", -1), item.get("chunk_offset", 0), item.get("chunk_size", 0), item.get("is_compressed", False), item.get("inner_offset", 0))
            
            if os.path.exists(bin_path):
                os.remove(bin_path)
            os.rename(temp_out, bin_path)
            
            success += 1
        except Exception as e:
            errors.append(f"{item['filename']}: {str(e)}")
            logger.error(f"Erreur apply {item['filename']}: {e}")
            
    # Clear queue after apply
    save_queue([])
    for f in STAGING_DIR.glob("*"):
        if f.is_file() and f.name != "queue.json":
            try: f.unlink()
            except: pass
            
    return {"status": "ok", "success_count": success, "errors": errors}

import pycdlib
import subprocess

class IsoBuildRequest(BaseModel):
    base_folder: str
    iso_orig: str = ""

@router.post("/build/iso")
async def build_iso(req: IsoBuildRequest):
    base_folder = req.base_folder
    if not os.path.exists(base_folder):
        return Response(status_code=400, content=f'{{"detail": "Dossier {base_folder} introuvable."}}')
        
    try:
        from core.iso_builder import rebuild_iso_images
        
        iso_orig = req.iso_orig
        if not iso_orig or not os.path.exists(iso_orig):
            raise HTTPException(400, "Le fichier ISO original specifie est introuvable.")
            
        out_iso = os.path.join(base_folder, "..", "P2IS_MOD.iso")
        
        rebuild_iso_images(iso_orig, out_iso, base_folder)
        
        return {"status": "ok", "out_iso": out_iso}
    except Exception as e:
        logger.error(f"Erreur build iso: {e}")
        raise HTTPException(500, f"Erreur lors de la construction de l'ISO: {e}")

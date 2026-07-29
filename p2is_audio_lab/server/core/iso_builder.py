import logging
import shutil
import struct
import os

logger = logging.getLogger(__name__)

def patch_iso(iso_path: str, bin_path: str, internal_path: str, out_iso_path: str = None) -> bool:
    if not os.path.exists(iso_path):
        logger.error(f"Fichier ISO original introuvable : {iso_path}")
        return False
        
    if not os.path.exists(bin_path):
        logger.error(f"Fichier BIN modifie introuvable : {bin_path}")
        return False

    target_filename = internal_path.split('/')[-1]
    
    if not out_iso_path:
        base, ext = os.path.splitext(iso_path)
        out_iso_path = f"{base}_MOD{ext}"
    
    try:
        logger.info(f"PrÃ©paration de la copie de l'ISO...")
        shutil.copy(iso_path, out_iso_path)
        
        with open(out_iso_path, "r+b") as iso_f:
            iso_f.seek(0)
            header_data = iso_f.read(10 * 1024 * 1024)
            
            target_bytes = (target_filename + ";1").encode('ascii')
            target_bytes_no_ver = target_filename.encode('ascii')
            
            idx = header_data.find(target_bytes)
            if idx == -1:
                idx = header_data.find(target_bytes_no_ver)
                
            if idx == -1:
                logger.error("Impossible de trouver le fichier dans l'ISO.")
                return False
                
            rec_start = idx - 33
            orig_lba = struct.unpack('<I', header_data[rec_start+2:rec_start+6])[0]
            orig_size = struct.unpack('<I', header_data[rec_start+10:rec_start+14])[0]
            
            new_size = os.path.getsize(bin_path)
            
            if new_size == orig_size:
                logger.info(f"Tailles identiques ({orig_size} octets). Injection IN-PLACE au LBA {orig_lba} ! Le jeu ne verra aucune difference de structure.")
                iso_f.seek(orig_lba * 2048)
                with open(bin_path, "rb") as bin_f:
                    iso_f.write(bin_f.read())
                return True
            else:
                msg = f"ECHEC IN-PLACE: Taille {new_size} au lieu de {orig_size} ! Le script audio aurait du corriger la taille !"
                logger.error(msg)
                return msg
                
    except Exception as e:
        logger.error(f"Erreur lors de la reconstruction de l'ISO: {e}")
        return str(e)



def extract_audio_from_iso(iso_path: str, out_dir: str) -> dict:
    results = {}
    if not os.path.exists(iso_path):
        return {"error": f"Fichier ISO introuvable : {iso_path}"}
    if not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)
        
    try:
        with open(iso_path, "rb") as iso_f:
            header_data = iso_f.read(10 * 1024 * 1024)
            
            for target_filename in ["VOICEALL.BIN", "BGMALL.BIN"]:
                target_bytes = (target_filename + ";1").encode('ascii')
                target_bytes_no_ver = target_filename.encode('ascii')
                
                idx = header_data.find(target_bytes)
                if idx == -1:
                    idx = header_data.find(target_bytes_no_ver)
                    
                if idx == -1:
                    logger.warning(f"Impossible de trouver {target_filename} dans l'ISO.")
                    results[target_filename] = False
                    continue
                    
                rec_start = idx - 33
                orig_lba = struct.unpack('<I', header_data[rec_start+2:rec_start+6])[0]
                orig_size = struct.unpack('<I', header_data[rec_start+10:rec_start+14])[0]
                
                iso_f.seek(orig_lba * 2048)
                file_data = iso_f.read(orig_size)
                
                out_path = os.path.join(out_dir, target_filename)
                with open(out_path, "wb") as out_f:
                    out_f.write(file_data)
                    
                logger.info(f"{target_filename} extrait avec succes ({orig_size} octets).")
                results[target_filename] = True
                
        return {"success": True, "details": results}
    except Exception as e:
        logger.error(f"Erreur lors de l'extraction: {e}")
        return {"error": str(e)}

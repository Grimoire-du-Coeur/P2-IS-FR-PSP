import os
import shutil
import struct
import logging
from pathlib import Path

# Importer cpk_tool (qui doit se trouver dans le meme dossier)
from .cpk_tool import extract_cpk, build_cpk

logger = logging.getLogger("api")

def extract_cpk_from_iso(iso_path: str, out_cpk_path: str):
    """
    Extrait l'archive P2PT_ALL.CPK depuis l'ISO vers le chemin specifie.
    """
    if not os.path.exists(iso_path):
        raise FileNotFoundError(f"ISO introuvable : {iso_path}")
        
    logger.info(f"Recherche de l'archive P2PT_ALL.CPK dans {iso_path}...")
    with open(iso_path, "rb") as f:
        # On lit les premiers Mo pour trouver le P2PT_ALL.CPK Directory Record
        data = f.read(10 * 1024 * 1024)
        pos = data.upper().find(b'P2PT_ALL')
        if pos == -1:
            raise ValueError("Directory Record P2PT_ALL.CPK introuvable dans l'ISO.")
            
        dir_record_offset = pos - 33
        lba_le = struct.unpack("<I", data[dir_record_offset+2:dir_record_offset+6])[0]
        size_le = struct.unpack("<I", data[dir_record_offset+10:dir_record_offset+14])[0]
        cpk_offset_in_iso = lba_le * 2048
        
        logger.info(f"Directory Record de P2PT_ALL trouve a 0x{dir_record_offset:X}. LBA={lba_le}, Size={size_le}")
        logger.info(f"Extraction du CPK original depuis 0x{cpk_offset_in_iso:X} vers {out_cpk_path}...")
        
        f.seek(cpk_offset_in_iso)
        with open(out_cpk_path, "wb") as out_f:
            bytes_left = size_le
            chunk_size = 1024 * 1024 * 16 # 16 MB chunks
            while bytes_left > 0:
                chunk = f.read(min(bytes_left, chunk_size))
                if not chunk:
                    break
                out_f.write(chunk)
                bytes_left -= len(chunk)

def rebuild_iso_images(iso_orig_path: str, out_iso_path: str, cpk_dir: str):
    """
    Construit un nouveau CPK valide avec cpk_tool.py, l'ajoute a la fin de l'ISO, 
    et met a jour la table des matieres ISO9660 (Directory Record) pour pointer vers le nouveau CPK.
    """
    if not os.path.exists(iso_orig_path):
        raise FileNotFoundError("ISO original introuvable.")
        
    logger.info(f"Copie de {iso_orig_path} vers {out_iso_path}...")
    shutil.copyfile(iso_orig_path, out_iso_path)
    
    # 1. Trouver le nom de l'archive CPK et sa position
    logger.info("Recherche de l'archive P2PT_ALL.CPK dans l'ISO...")
    cpk_offset_in_iso = -1
    dir_record_offset = -1
    
    with open(out_iso_path, "r+b") as f:
        # On lit les premiers Mo pour trouver le P2PT_ALL.CPK Directory Record
        f.seek(0)
        data = f.read(10 * 1024 * 1024)
        pos = data.upper().find(b'P2PT_ALL')
        if pos == -1:
            raise ValueError("Directory Record P2PT_ALL.CPK introuvable dans l'ISO.")
            
        # Trouver le debut du directory record (pos est l'index du nom de fichier)
        # La longueur du file ID est a pos-33 (si le length indicator est 33 octets avant)
        dir_record_offset = pos - 33
        
        # Verification que c'est bien un Directory Record
        rec_len = data[dir_record_offset]
        if rec_len == 0 or rec_len > 255:
            raise ValueError("Directory Record P2PT_ALL invalide.")
            
        lba_le = struct.unpack("<I", data[dir_record_offset+2:dir_record_offset+6])[0]
        size_le = struct.unpack("<I", data[dir_record_offset+10:dir_record_offset+14])[0]
        cpk_offset_in_iso = lba_le * 2048
        
        logger.info(f"Directory Record de P2PT_ALL trouve a 0x{dir_record_offset:X}. LBA={lba_le}, Size={size_le}")
        logger.info(f"Extraction du CPK original depuis 0x{cpk_offset_in_iso:X}...")
        
        # 2. Extraire le CPK original vers un fichier temporaire
        f.seek(cpk_offset_in_iso)
        original_cpk_data = f.read(size_le)
        
    # Ecrire le cpk original temporaire
    temp_orig_cpk = os.path.join(cpk_dir, "_original.cpk")
    temp_new_cpk = os.path.join(cpk_dir, "_rebuilt.cpk")
    
    with open(temp_orig_cpk, "wb") as f:
        f.write(original_cpk_data)
        
    # 3. Construire le nouveau CPK en injectant les images
    logger.info("Reconstruction du nouveau CPK avec vos fichiers modifies...")
    # On passe le dossier de travail (in_dir), le chemin de sortie, et le CPK d'origine
    build_cpk(cpk_dir, temp_new_cpk, temp_orig_cpk)
    
    new_cpk_size = os.path.getsize(temp_new_cpk)
    logger.info(f"Nouveau CPK construit : {new_cpk_size} octets.")
    
    # 4. Injecter le nouveau CPK a la fin de l'ISO
    with open(out_iso_path, "r+b") as f:
        f.seek(0, 2) # fin du fichier
        padding = (2048 - (f.tell() % 2048)) % 2048
        if padding:
            f.write(b'\x00' * padding)
            
        new_iso_offset = f.tell()
        new_lba = new_iso_offset // 2048
        
        logger.info(f"Ecriture du nouveau CPK a la fin de l'ISO (LBA={new_lba})...")
        with open(temp_new_cpk, "rb") as new_f:
            # Copier en gros blocs pour eviter la RAM excessive
            while True:
                chunk = new_f.read(16 * 1024 * 1024)
                if not chunk:
                    break
                f.write(chunk)
            
        final_iso_size = f.tell()
        
        # 5. Mettre a jour le Directory Record
        logger.info(f"Mise a jour du Directory Record P2PT_ALL (LBA: {lba_le} -> {new_lba}, Size: {size_le} -> {new_cpk_size})...")
        f.seek(dir_record_offset + 2)
        f.write(struct.pack("<I", new_lba) + struct.pack(">I", new_lba))
        f.seek(dir_record_offset + 10)
        f.write(struct.pack("<I", new_cpk_size) + struct.pack(">I", new_cpk_size))
        
        # 6. Mettre a jour le Volume Space Size (PVD)
        logger.info("Mise a jour de la taille globale de l'ISO (PVD)...")
        f.seek(16 * 2048)
        pvd = bytearray(f.read(2048))
        if pvd[:7] == b"\x01CD001\x01":
            sectors = (final_iso_size + 2047) // 2048
            pvd[80:88] = struct.pack("<I", sectors) + struct.pack(">I", sectors)
            f.seek(16 * 2048)
            f.write(pvd)
        else:
            logger.warning("PVD ISO9660 introuvable au secteur 16, la taille du volume n'a pas ete mise a jour.")
            
    # Nettoyage
    try:
        os.remove(temp_orig_cpk)
        os.remove(temp_new_cpk)
    except:
        pass
        
    logger.info("Magie Noire CPK (Reconstruction Complete) terminee avec succes !")

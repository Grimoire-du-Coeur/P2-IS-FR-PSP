import os
import struct
import shutil

def parse_bin_toc(filepath: str):
    """
    Parse la Table des Matières d'un VOICEALL.BIN ou BGMALL.BIN.
    La TOC s'arrête physiquement avant l'offset minimum non-nul.
    """
    filesize = os.path.getsize(filepath)
    with open(filepath, "rb") as f:
        toc_limit = None
        offsets = []
        pos = 0
        while True:
            # Si on a atteint la limite dynamique
            if toc_limit is not None and pos >= toc_limit:
                break
                
            val = struct.unpack('<I', f.read(4))[0]
            offsets.append(val)
            pos += 4
            
            if val > 0:
                if toc_limit is None or val < toc_limit:
                    toc_limit = val
                    
        toc_end = toc_limit
        num_entries = len(offsets)
        raw_offsets = offsets

    # Construire la liste (offset, size) en triant et calculant les tailles
    indexed = [(i, o) for i, o in enumerate(raw_offsets) if o > 0]
    sorted_by_offset = sorted(indexed, key=lambda x: x[1])

    entries_by_index = [None] * num_entries
    for rank, (idx, offset) in enumerate(sorted_by_offset):
        # Trouver le PROCHAIN offset strictement supérieur pour calculer la vraie taille
        next_offset = filesize
        for next_rank in range(rank + 1, len(sorted_by_offset)):
            if sorted_by_offset[next_rank][1] > offset:
                next_offset = sorted_by_offset[next_rank][1]
                break
                
        size = next_offset - offset
        if size > 0:
            entries_by_index[idx] = (offset, size)

    return entries_by_index, toc_end

def extract_entry(filepath: str, offset: int, size: int) -> bytes:
    """Extrait une entrée audio brute du BIN."""
    with open(filepath, "rb") as f:
        f.seek(offset)
        return f.read(size)

def detect_audio_format(data: bytes) -> str:
    if data[:4] == b"RIFF":
        return ".wav"
    if data[:4] == b"VAGp":
        return ".vag"
    if data[:4] == b"OggS":
        return ".ogg"
    return ".bin"

def inject_wav_into_bin(bin_path: str, entry_idx: int, new_wav_data: bytes,
                         toc_entries: list, toc_end: int,
                         out_bin_path: str, log_fn=None) -> bool:
    """
    Remplace une entrée audio dans le BIN par les données WAV converties (new_wav_data).
    Injection IN-PLACE stricte pour conserver la taille et la TOC d'origine.
    """
    if entry_idx < 0 or entry_idx >= len(toc_entries):
        if log_fn: log_fn(f"[ERREUR] Index {entry_idx} hors limite.", "ERROR")
        return False
        
    entry = toc_entries[entry_idx]
    if entry is None:
        if log_fn: log_fn(f"[ERREUR] Entrée {entry_idx} vide ou invalide.", "ERROR")
        return False

    orig_offset, orig_size = entry
    
    if log_fn: log_fn(f"Injection In-Place stricte de {len(new_wav_data)} octets dans {orig_size} octets...", "INFO")
    
    import shutil
    import struct
    
    try:
        # 1. Copier le fichier de base s'il n'est pas déjà à l'emplacement de destination
        if os.path.abspath(bin_path) != os.path.abspath(out_bin_path):
            shutil.copy2(bin_path, out_bin_path)
            
        # 2. Préparer les nouvelles données pour qu'elles fassent EXACTEMENT la taille d'origine
        if len(new_wav_data) <= orig_size:
            padded_wav = new_wav_data + b'\x00' * (orig_size - len(new_wav_data))
        else:
            if log_fn: log_fn(f"Avertissement : La piste est plus grande, troncature de {len(new_wav_data) - orig_size} octets !", "WARNING")
            truncated = bytearray(new_wav_data[:orig_size])
            if truncated.startswith(b'RIFF'):
                # Corriger la taille RIFF
                struct.pack_into('<I', truncated, 4, orig_size - 8)
                # Corriger la taille DATA si possible
                idx = 12
                while idx < len(truncated) - 8:
                    chunk_id = truncated[idx:idx+4]
                    chunk_size = struct.unpack('<I', truncated[idx+4:idx+8])[0]
                    if chunk_id == b'data':
                        new_data_size = orig_size - (idx + 8)
                        struct.pack_into('<I', truncated, idx+4, new_data_size)
                        break
                    idx += 8 + chunk_size
            padded_wav = bytes(truncated)
            
        # 3. Ecrire par-dessus l'ancienne piste
        with open(out_bin_path, "r+b") as f_out:
            # Remplacer TOUTES les occurrences de cet offset si la piste est dupliquée (ex: 2 et 146)
            # En in-place, si on modifie l'offset physique, on modifie automatiquement TOUTES les pistes qui pointent dessus !
            f_out.seek(orig_offset)
            f_out.write(padded_wav)
            
        if log_fn: log_fn(f"Injection réussie à l'offset {orig_offset}.", "INFO")
        return True
        
    except Exception as e:
        if log_fn: log_fn(f"Erreur d'injection : {e}", "ERROR")
        return False

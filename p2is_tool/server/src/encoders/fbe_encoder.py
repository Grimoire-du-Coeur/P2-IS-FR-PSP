def encode_fbe_sub_chunk(
    data: bytearray,
    n_fr: str,
    t_fr: str,
    log_fn=None,
    dlg_id=None,
) -> None:
    from src.core.text import text_to_bytes
    from src.config import SP, NL
    import re
    
    end = len(data)
    i = 0
    
    # 1. Remplacer le nom
    n_bytes_fr = text_to_bytes(n_fr) if n_fr else b""
    n_len = len(n_bytes_fr)
    n_idx = 0
    
    while i < end - 1:
        w = data[i] | (data[i+1] << 8)
        if w == NL:
            i += 2
            break
            
        if n_idx < n_len:
            data[i] = n_bytes_fr[n_idx]
            data[i+1] = n_bytes_fr[n_idx+1]
            n_idx += 2
        else:
            if n_fr:
                data[i] = 0x20
                data[i+1] = 0x11
        i += 2
        
    text_start = i
    avail_space = end - text_start
    
    # 2. Remplacer le texte avec preservation des tags binaires (ex: [E4], [B_81], etc.)
    if not t_fr:
        data[text_start:end] = b"  " * (avail_space // 2)
        return
        
    parts = re.split(r'(\[[a-zA-Z0-9_+]+\]|\
)', t_fr)
    tokens = []
    for p in parts:
        if not p: continue
        if (p.startswith('[') and p.endswith(']')) or p == '\n':
            tokens.append((True, text_to_bytes(p)))
        else:
            for ch in p:
                tokens.append((False, text_to_bytes(ch)))
                
    total_len = sum(len(b) for _, b in tokens)
    
    if total_len > avail_space:
        if log_fn:
            log_fn(f"  [!] [DEPASSEMENT] [id {dlg_id}] Texte FR trop long de {total_len - avail_space} octets. Troncature securisee.", "warn")
        excess = total_len - avail_space
        # On supprime d'abord les caracteres textuels depuis la fin pour preserver les codes binaires (tags)
        for j in range(len(tokens)-1, -1, -1):
            if excess <= 0: break
            is_tag, b = tokens[j]
            if not is_tag and len(b) > 0:
                excess -= len(b)
                tokens[j] = (False, b"")
        # Si on depasse toujours (impossible sauf si les tags sont plus gros que la place d'origine), on tronque les tags
        for j in range(len(tokens)-1, -1, -1):
            if excess <= 0: break
            is_tag, b = tokens[j]
            if is_tag and len(b) > 0:
                excess -= len(b)
                tokens[j] = (True, b"")
                
    out = bytearray()
    for _, b in tokens:
        out.extend(b)
        
    if len(out) < avail_space:
        padding = (avail_space - len(out)) // 2
        out.extend(b"  " * padding)
        
    data[text_start:end] = out[:avail_space]

def encode_fbe_bnp_from_json(
    bin_path: str, json_path: str, log_fn, out_path: str = None
) -> str:
    data = bytearray(open(bin_path, "rb").read())
    import json
    from pathlib import Path

    dlgs = json.loads(open(json_path, encoding="utf-8").read(), strict=False)
    ok = skip = kept = 0
    
    from collections import defaultdict
    slots_map = defaultdict(list)
    for d in dlgs:
        slots_map[d["offset"]].append(d)

    for offset, subs in slots_map.items():
        slot_size = subs[0]["data_size"]
        slot_data = data[offset : offset + slot_size]
        
        for d in subs:
            n_fr = d.get("nom_fr", "").strip()
            t_fr = d.get("texte_fr", "").strip()
            
            if not n_fr and not t_fr:
                kept += 1
                continue
                
            sub_off = d.get("_sub_offset")
            sub_len = d.get("_sub_len")
            
            if sub_off is None or sub_len is None:
                continue
                
            sub_chunk = slot_data[sub_off : sub_off + sub_len]
            encode_fbe_sub_chunk(sub_chunk, n_fr, t_fr, log_fn, d.get("id"))
            
            slot_data[sub_off : sub_off + sub_len] = sub_chunk
            ok += 1
            
    if out_path is None:
        out_path = bin_path
        
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(data)
        
    if log_fn:
        log_fn(
            f"  [RESUME] {Path(out_path).name} : {ok} injectes, {skip} rejetes, {kept} laisses en japonais.",
            "ok",
        )
    return out_path

import struct
import io
import gzip
import re
from typing import List, Dict, Tuple
from PIL import Image

def decompress_atlus_lz77(data: bytes) -> bytes:
    if not data.startswith(b'MIG.00.1PSP\x82'):
        return None
    try:
        dict_size = struct.unpack_from(">I", data, 12)[0]
        nxt = data.find(b'MIG.00.1PSP\x82', 16)
        if nxt == -1: nxt = len(data)
        chunk = data[:nxt]
        out = bytearray(chunk[16:16+dict_size])
        pos = 16 + dict_size
        while pos < len(chunk):
            b1 = chunk[pos]
            if b1 < 0x80: 
                out.append(b1)
                pos += 1
            else:
                if pos+1 >= len(chunk): break
                b2 = chunk[pos+1]
                pos += 2
                word = ((b1&0x7F)<<8)|b2
                offset = word>>4
                length = (word&0xF)+3
                sc = len(out)-offset-1
                if sc >= 0 and sc + length <= len(out):
                    out.extend(out[sc:sc+length])
                else:
                    for _ in range(length):
                        out.append(out[sc] if 0<=sc<len(out) else 0)
                        sc += 1
        return bytes(out)
    except Exception as e:
        print(f"LZ77 Decompress error: {e}")
        return None

def compress_atlus_lzss(uncompressed: bytes, original_compressed: bytes) -> bytes:
    dict_size = struct.unpack_from(">I", original_compressed, 12)[0]
    dictionary = uncompressed[:dict_size]
    n = len(uncompressed)
    cost = [float('inf')] * (n + 1)
    link = [None] * (n + 1)
    cost[dict_size] = 0
    
    for i in range(dict_size, n):
        if cost[i] == float('inf'): continue
        b = uncompressed[i]
        if b < 0x80:
            if cost[i] + 1 < cost[i+1]:
                cost[i+1] = cost[i] + 1
                link[i+1] = (i, ('L', b))
        
        max_lookbehind = min(i, 2048)
        best_len_for_offset = {}
        for lb in range(1, max_lookbehind + 1):
            l = 0
            while l < 18 and i + l < n and uncompressed[i - lb + l] == uncompressed[i + l]:
                l += 1
            if l >= 3:
                if l not in best_len_for_offset:
                    best_len_for_offset[l] = lb
                    
        for l in range(3, 19):
            if l in best_len_for_offset:
                lb = best_len_for_offset[l]
                if cost[i] + 2 < cost[i+l]:
                    cost[i+l] = cost[i] + 2
                    link[i+l] = (i, ('M', lb, l))
                    
    if cost[n] == float('inf'): return None
    path = []
    curr = n
    while curr > dict_size:
        prev, info = link[curr]
        path.append(info)
        curr = prev
    path.reverse()
    
    out = bytearray(b'MIG.00.1PSP\x82')
    out.extend(struct.pack(">I", dict_size))
    out.extend(dictionary)
    for info in path:
        if info[0] == 'L':
            out.append(info[1])
        else:
            _, lb, l = info
            word = ((lb - 1) << 4) | (l - 3)
            out.append((word >> 8) | 0x80)
            out.append(word & 0xFF)
    return bytes(out)

def create_fake_gim_from_atlus(dec: bytes) -> bytes:
    # Heuristics for Atlus sprite
    pal_off = None
    bpp = 4 # default to 4bpp, try to guess
    
    # Parse Atlus sprite header (Big-Endian 16-byte records)
    pal_off = 0x0380
    pix_off = 0x1080
    w = 256
    
    if len(dec) >= 16:
        import struct
        try:
            # First record
            vals = struct.unpack_from(">HHHHHHHH", dec, 0)
            if vals[5] > 0 and vals[5] < len(dec):
                pix_off = vals[5]
            if vals[7] > 0 and vals[7] < len(dec):
                pal_off = vals[7]
            if vals[2] > 0 and vals[2] <= 4096:
                w = vals[2]
        except Exception:
            pass
            
    # Try 8bpp if the file is large enough
    if len(dec) >= 66560:
        bpp = 8
        
    pix_size = len(dec) - pix_off
    if bpp == 4:
        h = (pix_size * 2) // w
    else:
        h = pix_size // w
        
    w = max(0, min(65535, w))
    h = max(0, min(65535, h))
        
    # Ensure palette is RGBA8888 by swapping bytes (BGRA -> RGBA) and fixing alpha (0-128 -> 0-255)
    palette_data = bytearray(dec[pal_off : pal_off + (16 * 4 if bpp == 4 else 256 * 4)])
    pixel_data = dec[pix_off:]
    for i in range(0, len(palette_data), 4):
        b = palette_data[i]
        g = palette_data[i+1]
        r = palette_data[i+2]
        a = palette_data[i+3]
        palette_data[i] = r
        palette_data[i+1] = g
        palette_data[i+2] = b
        palette_data[i+3] = min(255, a * 2)
    
    gim = bytearray(b'MIG.00.1PSP\x00' + struct.pack("<I", 0x10))
    psize = len(pixel_data)
    palsize = len(palette_data)
    
    # Chunk sizes must include their 16-byte headers!
    img_sz = 16 + 48 + psize
    pal_sz = 16 + 48 + palsize
    
    # Frame chunk contains Image chunk and Palette chunk
    frm_sz = 16 + img_sz + pal_sz
    rt_sz = 16 + frm_sz
    
    gim.extend(struct.pack("<HHIIII", 0x0002, 16, rt_sz, rt_sz, 16, 0)) # Root
    gim = gim[:len(gim)-4] # struct packing alignment fix
    
    gim.extend(struct.pack("<HHIIII", 0x0003, 16, frm_sz, frm_sz, 16, 0))
    gim = gim[:len(gim)-4]
    
    gim.extend(struct.pack("<HHIIII", 0x0004, 16, img_sz, img_sz+pal_sz, 16, 0))
    gim = gim[:len(gim)-4]
    
    # Image Header (48 bytes)
    # 0: size(48), 2: unused(0), 4: fmt, 6: order, 8: w, 10: h, 12: bpp, 14: pitch
    # 16: align, 18-27: unused
    # 28: offset to pixels (usually 48 if pixel data follows immediately)
    gim.extend(struct.pack("<HHHHHHHH", 48, 0, 0x04 if bpp==4 else 0x05, 0, w, h, bpp, w))
    gim.extend(b'\x00' * 12) # bytes 16-27
    gim.extend(struct.pack("<IIIII", 48, 0, 0, 0, 0)) # bytes 28-47 (48 is offset to pixels relative to bd)
    
    gim.extend(pixel_data)
    
    gim.extend(struct.pack("<HHIIII", 0x0005, 16, pal_sz, pal_sz, 16, 0))
    gim = gim[:len(gim)-4]
    
    # Palette Header (48 bytes)
    # 0: size(48), 2: 0, 4: fmt(3), 6: 0, 8: pw, 10: ph, 12: bpp(32), 14: pitch
    gim.extend(struct.pack("<HHHHHHHH", 48, 0, 0x03, 0, palsize//4, 1, 32, palsize//4))
    gim.extend(b'\x00' * 12)
    gim.extend(struct.pack("<IIIII", 48, 0, 0, 0, 0))
    
    gim.extend(palette_data)
    
    return bytes(gim)

def detect_archive(data: bytes) -> str:
    if len(data) >= 8:
        s0 = struct.unpack_from("<I", data, 0)[0]
        e0 = struct.unpack_from("<I", data, 4)[0]
        if 0 < s0 < e0 < len(data) and data[s0:s0+2] == b'\x1f\x8b':
            return "EVENT_BIN"
            
    if len(data) >= 12:
        n = struct.unpack_from("<I", data, 0)[0]
        if 1 <= n <= 200:
            offs, valid = [], True
            for i in range(min(n, 8)):
                o = struct.unpack_from("<I", data, 4+i*4)[0]
                if o == 0 or o >= len(data): valid = False; break
                offs.append(o)
            if valid and offs:
                hits = sum(1 for o in offs if b'MIG.' in data[o:o+8] or data[o:o+2]==b'\x1f\x8b' or data[o:o+4]==b'VAGp')
                if hits > 0: return "ATLUS_ARCHIVE"
                if (len(offs) >= 2 and all(offs[i] < offs[i+1] for i in range(len(offs)-1)) and min(offs) > 0x100 and max(offs) < len(data) * 0.9):
                    return "ATLUS_ARCHIVE"
    return "UNKNOWN"

def unswizzle_psp(raw: bytes, w: int, h: int, bpp_bits: int) -> bytes:
    row_bytes = (w * bpp_bits + 7) // 8
    pitch = (row_bytes + 15) & ~15
    aligned_h = (h + 7) & ~7
    bw, bh = 16, 8

    aligned_out = bytearray(aligned_h * pitch)
    src = 0
    for by in range(0, aligned_h, bh):
        for bx in range(0, pitch, bw):
            for row in range(bh):
                for col in range(bw):
                    dst = (by + row) * pitch + (bx + col)
                    if src < len(raw) and dst < len(aligned_out):
                        aligned_out[dst] = raw[src]
                    src += 1

    out = bytearray(h * row_bytes)
    for row in range(h):
        s = row * pitch
        d = row * row_bytes
        out[d:d + row_bytes] = aligned_out[s:s + row_bytes]

    return bytes(out)

def _swz_read_size(w: int, h: int, bpp_bits: int) -> int:
    row_bytes = (w * bpp_bits + 7) // 8
    pitch = (row_bytes + 15) & ~15
    aligned_h = (h + 7) & ~7
    return pitch * aligned_h

def parse_gim(data: bytes, base: int = 0) -> Tuple[List[Dict], Dict, int]:
    if len(data) < base + 4 or data[base:base+4] != b'MIG.':
        return [], None, 0
    
    pos = base + 16
    images = []
    palette = None
    visited = set()
    total_size = 0
    
    while pos + 16 <= len(data) and pos not in visited:
        visited.add(pos)
        btype = struct.unpack_from("<H", data, pos)[0]
        bsize = struct.unpack_from("<I", data, pos+4)[0]
        next_off = struct.unpack_from("<I", data, pos+8)[0]
        data_off = struct.unpack_from("<I", data, pos+12)[0]
        
        if bsize == 0 or bsize > 0x4000000: break
        bd = pos + data_off
        
        if btype in (0x0002, 0x0003):
            pos += data_off
            continue
        elif btype == 0x0004 and bd + 2 <= len(data):
            ssz = struct.unpack_from("<H", data, bd)[0]
            if ssz >= 16 and bd + ssz <= len(data):
                fmt = struct.unpack_from("<H", data, bd+4)[0]
                order = struct.unpack_from("<H", data, bd+6)[0]
                w = struct.unpack_from("<H", data, bd+8)[0]
                h = struct.unpack_from("<H", data, bd+10)[0]
                fst = struct.unpack_from("<I", data, bd+28)[0] if ssz >= 32 else 0
                if 0 < w <= 4096 and 0 < h <= 4096 and bd+fst < len(data):
                    images.append({'fmt': fmt, 'order': order, 'w': w, 'h': h, 'pix_abs': bd+fst})
        elif btype == 0x0005 and bd + 2 <= len(data):
            ssz = struct.unpack_from("<H", data, bd)[0]
            if ssz >= 16 and bd + ssz <= len(data):
                pfmt = struct.unpack_from("<H", data, bd+4)[0]
                pw = struct.unpack_from("<H", data, bd+8)[0]
                ph = struct.unpack_from("<H", data, bd+10)[0]
                pfst = struct.unpack_from("<I", data, bd+28)[0] if ssz >= 32 else 0
                nc = pw * ph
                palette = {'fmt': pfmt, 'abs': bd+pfst, 'n': nc}
        elif btype == 0x0006:
            total_size = (pos - base) + bsize
            break
            
        if next_off > 0 and next_off <= bsize:
            pos = pos + next_off
        elif bsize > 0:
            pos += bsize
        else:
            break
            
    if total_size == 0:
        total_size = pos - base # Fallback if no 0006 found
        
    return images, palette, total_size

def read_palette(data: bytes, palette: Dict) -> List[Tuple[int, int, int, int]]:
    n = palette['n']
    pfmt = palette['fmt']
    abs_off = palette['abs']
    pal = []
    
    if pfmt == 0x03: # RGBA8888
        pb = data[abs_off : abs_off + n*4]
        for i in range(0, min(len(pb), n*4), 4):
            pal.append((pb[i], pb[i+1], pb[i+2], pb[i+3]))
    elif pfmt == 0x02: # RGBA4444
        pb = data[abs_off : abs_off + n*2]
        for i in range(0, min(len(pb), n*2), 2):
            v = struct.unpack_from("<H", pb, i)[0]
            pal.append(((v & 0xF)*17, ((v >> 4) & 0xF)*17, ((v >> 8) & 0xF)*17, ((v >> 12) & 0xF)*17))
    elif pfmt == 0x00 or pfmt == 0x01: # RGB565 or RGBA5551
        pb = data[abs_off : abs_off + n*2]
        for i in range(0, min(len(pb), n*2), 2):
            v = struct.unpack_from("<H", pb, i)[0]
            if pfmt == 0x01: # RGBA5551
                r = (v & 0x1F) * 8
                g = ((v >> 5) & 0x1F) * 8
                b = ((v >> 10) & 0x1F) * 8
                a = 255 if (v >> 15) else 0
                pal.append((r, g, b, a))
            else: # RGB565
                r = (v & 0x1F) * 8
                g = ((v >> 5) & 0x3F) * 4
                b = ((v >> 11) & 0x1F) * 8
                pal.append((r, g, b, 255))
    else:
        # Fallback to RGBA8888 if unknown
        pb = data[abs_off : abs_off + n*4]
        for i in range(0, min(len(pb), n*4), 4):
            pal.append((pb[i], pb[i+1], pb[i+2], pb[i+3]))
            
    # Pad palette if needed
    while len(pal) < n:
        pal.append((0, 0, 0, 255))
        
    return pal

def render_gim(data: bytes, img_info: Dict, palette: Dict) -> Image.Image:
    fmt = img_info['fmt']
    w = img_info['w']
    h = img_info['h']
    pa = img_info['pix_abs']
    order = img_info['order']
    
    if w <= 0 or h <= 0 or pa >= len(data):
        raise ValueError(f"Dimensions invalides: {w}x{h}")
        
    def read_raw(bpp):
        sz = _swz_read_size(w, h, bpp)
        return data[pa:pa+sz]

    if fmt == 0x05: # INDEX8
        raw = read_raw(8)
        if order == 1: 
            raw = unswizzle_psp(raw, w, h, 8)
            row_bytes = w
        else:
            row_bytes = (w * 8 + 7) // 8
            row_bytes = (row_bytes + 15) & ~15
            
        pal = read_palette(data, palette) if palette else [(i, i, i, 255) for i in range(256)]
        
        px = []
        for r in range(h):
            for c in range(w):
                off = r * row_bytes + c
                if off < len(raw):
                    b = raw[off]
                else:
                    b = 0
                px.extend(pal[b] if b < len(pal) else (0,0,0,255))
        return Image.frombytes("RGBA", (w, h), bytes(px))
        
    elif fmt == 0x04: # INDEX4
        raw = read_raw(4)
        if order == 1: 
            raw = unswizzle_psp(raw, w, h, 4)
            row_bytes = (w + 1) // 2
        else:
            row_bytes = (w * 4 + 7) // 8
            row_bytes = (row_bytes + 15) & ~15
            
        pal = read_palette(data, palette) if palette else [(i*17, i*17, i*17, 255) for i in range(16)]
        
        px = []
        for r in range(h):
            for c in range(w):
                off = r * row_bytes + c // 2
                if off < len(raw):
                    b = raw[off]
                    nib = b & 0xF if c % 2 == 0 else (b >> 4) & 0xF
                else:
                    nib = 0
                px.extend(pal[nib] if nib < len(pal) else (0,0,0,255))
        return Image.frombytes("RGBA", (w, h), bytes(px))
        
    elif fmt == 0x03: # RGBA8888
        raw = read_raw(32)
        if order == 1: raw = unswizzle_psp(raw, w, h, 32)
        return Image.frombytes("RGBA", (w, h), raw[:w*h*4])
        
    elif fmt == 0x02: # RGBA4444
        raw = read_raw(16)
        if order == 1: raw = unswizzle_psp(raw, w, h, 16)
        px = []
        for i in range(0, w*h*2, 2):
            v = struct.unpack_from("<H", raw, i)[0]
            px += [(v & 0xF)*17, ((v >> 4) & 0xF)*17, ((v >> 8) & 0xF)*17, ((v >> 12) & 0xF)*17]
        return Image.frombytes("RGBA", (w, h), bytes(px[:w*h*4]))
        
    elif fmt == 0x01: # RGBA5551
        raw = read_raw(16)
        if order == 1: raw = unswizzle_psp(raw, w, h, 16)
        px = []
        for i in range(0, w*h*2, 2):
            v = struct.unpack_from("<H", raw, i)[0]
            r = (v & 0x1F) * 8
            g = ((v >> 5) & 0x1F) * 8
            b = ((v >> 10) & 0x1F) * 8
            a = 255 if (v >> 15) else 0
            px += [r, g, b, a]
        return Image.frombytes("RGBA", (w, h), bytes(px[:w*h*4]))
        
    elif fmt == 0x00: # RGB565
        raw = read_raw(16)
        if order == 1: raw = unswizzle_psp(raw, w, h, 16)
        px = []
        for i in range(0, w*h*2, 2):
            v = struct.unpack_from("<H", raw, i)[0]
            px += [(v >> 11 & 0x1F)*8, (v >> 5 & 0x3F)*4, (v & 0x1F)*8]
        return Image.frombytes("RGB", (w, h), bytes(px[:w*h*3]))

    raise ValueError(f"Format GIM {fmt:#x} non supporté")

def _try_force_decode_gim_metadata(data: bytes, base: int) -> dict:
    for off in range(16, min(len(data)-32, 512), 2):
        try:
            ssz  = struct.unpack_from('<H', data, base + off)[0]
            if not (32 <= ssz <= 128): continue
            fmt  = struct.unpack_from('<H', data, base + off + 4)[0]
            if fmt > 5: continue
            order = struct.unpack_from('<H', data, base + off + 6)[0]
            w    = struct.unpack_from('<H', data, base + off + 8)[0]
            h    = struct.unpack_from('<H', data, base + off + 10)[0]
            if not (4 <= w <= 1024 and 4 <= h <= 1024): continue
            fst  = struct.unpack_from('<I', data, base + off + 28)[0]
            pix_abs = base + off + fst
            if pix_abs >= len(data): continue
            return [{'fmt':fmt,'order':order,'w':w,'h':h,'pix_abs':pix_abs}]
        except: continue
    return None

def _scan_chunk_for_gims(data: bytes, is_archive: bool, archive_type: str, chunk_index: int, chunk_offset: int, chunk_size: int, is_compressed: bool, next_index: int, ignore_atlus: bool = False) -> List[Dict]:
    gims = []
    matches = [m.start() for m in re.finditer(rb'MIG\.00\.1PSP', data)]
    for mp in matches:
        if mp + 11 < len(data) and data[mp+11] == 0x82:
            if ignore_atlus:
                continue
            # Handle Atlus Sprite
            dec = decompress_atlus_lz77(data[mp:])
            if dec:
                fake_gim = create_fake_gim_from_atlus(dec)
                if fake_gim:
                    imgs, pal, _ = parse_gim(fake_gim, 0)
                    if imgs:
                        fmt_name = {0: 'RGB565', 1: 'RGBA5551', 2: 'RGBA4444', 3: 'RGBA8888', 4: 'INDEX4', 5: 'INDEX8'}.get(imgs[0]['fmt'], 'UNK')
                        info_str = f"{imgs[0]['w']}x{imgs[0]['h']} (Atlus Sprite) | Format: {fmt_name}"
                        
                        nxt = data.find(b'MIG.00.1PSP', mp + 4)
                        total_size = nxt - mp if nxt != -1 else len(data) - mp
                        
                        gims.append({
                            'index': next_index + len(gims),
                            'offset': mp if is_compressed else (chunk_offset + mp),
                            'size': total_size,
                            'info': info_str,
                            'has_palette': pal is not None,
                            'is_archive': is_archive,
                            'archive_type': archive_type,
                            'chunk_index': chunk_index,
                            'inner_offset': mp,
                            'chunk_offset': chunk_offset,
                            'chunk_size': chunk_size,
                            'is_compressed': is_compressed,
                            'is_atlus': True
                        })
            continue

        imgs, pal, total_size = parse_gim(data, mp)
        if total_size <= 0:
            nxt = data.find(b'MIG.00.1PSP', mp + 4)
            if nxt != -1:
                total_size = nxt - mp
            else:
                total_size = len(data) - mp
                
        if imgs:
            fmt = imgs[0]['fmt']
            fmt_name = {0: 'RGB565', 1: 'RGBA5551', 2: 'RGBA4444', 3: 'RGBA8888', 4: 'INDEX4', 5: 'INDEX8'}.get(fmt, f'UNK({fmt})')
            info_str = f"{imgs[0]['w']}x{imgs[0]['h']} ({'swz' if imgs[0]['order'] else 'norm'}) | Format: {fmt_name}"
            
            gims.append({
                'index': next_index + len(gims),
                'offset': mp if is_compressed else (chunk_offset + mp),
                'size': total_size,
                'info': info_str,
                'has_palette': pal is not None,
                'is_archive': is_archive,
                'archive_type': archive_type,
                'chunk_index': chunk_index,
                'inner_offset': mp,
                'chunk_offset': chunk_offset,
                'chunk_size': chunk_size,
                'is_compressed': is_compressed
            })
    return gims

def scan_bin_for_gims(bin_path: str, ignore_atlus: bool = False) -> List[Dict]:
    print(f"[DEBUG] scan_bin_for_gims called for: {bin_path}")
    with open(bin_path, 'rb') as f:
        data = f.read()
    print(f"[DEBUG] Read {len(data)} bytes")
    
    archive_type = detect_archive(data)
    print(f"[DEBUG] detect_archive returned: {archive_type}")
    
    gims = []
    
    if archive_type == "EVENT_BIN":
        i = 0
        entries = []
        while i+8 <= len(data):
            s = struct.unpack_from("<I", data, i)[0]
            e = struct.unpack_from("<I", data, i+4)[0]
            if s == 0 or s >= len(data) or e > len(data): break
            if 0 < s < e <= len(data) and (e-s) > 16:
                entries.append((s, e))
            else: break
            i += 8
            
        print(f"[DEBUG] EVENT_BIN entries found: {len(entries)}")
        for idx, (s, e) in enumerate(entries):
            chunk = data[s:e]
            is_compressed = chunk[:2] == b'\x1f\x8b'
            
            try:
                inner_data = gzip.decompress(chunk) if is_compressed else chunk
                gims.extend(_scan_chunk_for_gims(inner_data, True, "EVENT_BIN", idx, s, e-s, is_compressed, len(gims), ignore_atlus))
            except Exception as ex:
                print(f"[DEBUG] Exception in EVENT_BIN chunk: {ex}")
                pass
                
    elif archive_type == "ATLUS_ARCHIVE":
        n = struct.unpack_from("<I", data, 0)[0]
        offs = []
        for i in range(n):
            o = struct.unpack_from("<I", data, 4 + i*4)[0]
            offs.append(o)
            
        print(f"[DEBUG] ATLUS_ARCHIVE entries found: {n}")
        for idx in range(n):
            s = offs[idx]
            e = offs[idx+1] if idx+1 < n else len(data)
            if s >= len(data) or s >= e: continue
            chunk = data[s:e]
            is_compressed = chunk[:2] == b'\x1f\x8b'
            
            try:
                inner_data = gzip.decompress(chunk) if is_compressed else chunk
                gims.extend(_scan_chunk_for_gims(inner_data, True, "ATLUS_ARCHIVE", idx, s, e-s, is_compressed, len(gims), ignore_atlus))
            except Exception as ex:
                print(f"[DEBUG] Exception in ATLUS chunk: {ex}")
                pass
    else:
        # Normal scan
        print(f"[DEBUG] Running normal scan on entire file")
        gims.extend(_scan_chunk_for_gims(data, False, "", -1, 0, len(data), False, 0, ignore_atlus))
        
    print(f"[DEBUG] scan_bin_for_gims returning {len(gims)} items")
    return gims

def extract_gim_entry(bin_path: str, offset: int, size: int, is_archive: bool = False, archive_type: str = "", chunk_index: int = -1, chunk_offset: int = 0, chunk_size: int = 0, is_compressed: bool = False, inner_offset: int = 0, is_atlus: bool = False) -> bytes:
    with open(bin_path, 'rb') as f:
        if is_archive:
            f.seek(chunk_offset)
            chunk = f.read(chunk_size)
            if is_compressed:
                try:
                    inner_data = gzip.decompress(chunk)
                    raw_extracted = inner_data[inner_offset : inner_offset + size]
                except Exception as e:
                    raise ValueError(f"Erreur de décompression GZIP: {e}")
            else:
                raw_extracted = chunk[inner_offset : inner_offset + size]
        else:
            f.seek(offset)
            raw_extracted = f.read(size)
        
    # Check if it's a standard GIM or an Atlus LZ77 stream
    if raw_extracted.startswith(b'MIG.00.1PSP'):
        if len(raw_extracted) > 11 and raw_extracted[11] == 0x82:
            # It's an Atlus LZ77 stream!
            try:
                dec = decompress_atlus_lz77(raw_extracted)
                if dec:
                    return create_fake_gim_from_atlus(dec)
            except Exception as e:
                print(f"[DEBUG] Error decompressing Atlus: {e}")
                pass
        else:
            # Standard GIM
            return raw_extracted
        
    return raw_extracted

def rebuild_event_bin(data: bytes, chunk_index: int, new_chunk: bytes) -> bytes:
    i = 0
    entries = []
    while i+8 <= len(data):
        s = struct.unpack_from("<I", data, i)[0]
        e = struct.unpack_from("<I", data, i+4)[0]
        if s == 0 or s >= len(data) or e > len(data): break
        if 0 < s < e <= len(data) and (e-s) > 16:
            entries.append((s, e))
        else: break
        i += 8
        
    if chunk_index < 0 or chunk_index >= len(entries):
        raise ValueError(f"chunk_index {chunk_index} invalide pour EVENT_BIN (max {len(entries)-1})")
        
    header_size = entries[0][0] if entries else 0
    new_data = bytearray(data[:header_size])
    current_offset = header_size
    
    for idx, (s, e) in enumerate(entries):
        if idx == chunk_index:
            chunk = new_chunk
        else:
            chunk = data[s:e]
            
        new_start = current_offset
        new_end = current_offset + len(chunk)
        
        struct.pack_into("<I", new_data, idx*8, new_start)
        struct.pack_into("<I", new_data, idx*8 + 4, new_end)
        
        new_data.extend(chunk)
        current_offset = new_end
        
    return bytes(new_data)

def rebuild_atlus_archive(data: bytes, chunk_index: int, new_chunk: bytes) -> bytes:
    n = struct.unpack_from("<I", data, 0)[0]
    offs = [struct.unpack_from("<I", data, 4 + i*4)[0] for i in range(n)]
    
    if chunk_index < 0 or chunk_index >= n:
        raise ValueError(f"chunk_index {chunk_index} invalide pour ATLUS_ARCHIVE (max {n-1})")
        
    first_off = offs[0]
    new_data = bytearray(data[:first_off])
    current_offset = first_off
    
    for idx in range(n):
        s = offs[idx]
        e = offs[idx+1] if idx+1 < n else len(data)
        
        if idx == chunk_index:
            chunk = new_chunk
        else:
            chunk = data[s:e]
            
        struct.pack_into("<I", new_data, 4 + idx*4, current_offset)
        new_data.extend(chunk)
        current_offset += len(chunk)
        
    return bytes(new_data)

def inject_gim_into_bin(bin_path: str, target_offset: int, target_size: int, new_gim_data: bytes, out_bin_path: str, is_archive: bool = False, archive_type: str = "", chunk_index: int = -1, chunk_offset: int = 0, chunk_size: int = 0, is_compressed: bool = False, inner_offset: int = 0, is_atlus: bool = False, log_fn=print) -> bool:
    new_size = len(new_gim_data)
    
    if not is_archive and not is_compressed and not is_atlus:
        if new_size > target_size:
            raise ValueError(f"Taille stricte violée: Le nouveau GIM est plus grand ({new_size} bytes) que l'original ({target_size} bytes).")
            
        with open(bin_path, 'rb') as f:
            data = bytearray(f.read())
            
        for i in range(new_size):
            if target_offset + i < len(data):
                data[target_offset + i] = new_gim_data[i]
                
        if new_size < target_size:
            for i in range(new_size, target_size):
                if target_offset + i < len(data):
                    data[target_offset + i] = 0

        with open(out_bin_path, 'wb') as f:
            f.write(data)
            
        return True
        
    # Archive Logic
    with open(bin_path, 'rb') as f:
        data = f.read()
        
    chunk = data[chunk_offset : chunk_offset + chunk_size]
    
    if is_compressed:
        inner_data = bytearray(gzip.decompress(chunk))
        if new_size > target_size:
            raise ValueError(f"Le nouveau GIM est plus grand que l'original, ce qui déborderait dans les données non-compressées adjacentes.")
            
        for i in range(new_size):
            if inner_offset + i < len(inner_data):
                inner_data[inner_offset + i] = new_gim_data[i]
                
        if new_size < target_size:
            for i in range(new_size, target_size):
                if inner_offset + i < len(inner_data):
                    inner_data[inner_offset + i] = 0
                    
        new_chunk = gzip.compress(bytes(inner_data))
    else:
        if is_atlus:
            # new_gim_data is a GIM. We extract its pixels and palette, 
            # and inject them into the uncompressed Atlus sprite table.
            dec = decompress_atlus_lz77(chunk)
            if not dec: raise ValueError("Failed to decompress Atlus chunk")
            dec_bytes = bytearray(dec)
            
            # parse the new GIM to get its pixels/palette
            imgs, pal, _ = parse_gim(new_gim_data, 0)
            if not imgs or not pal:
                raise ValueError("New GIM data is invalid")
            
            new_pix_size = (imgs[0]['w'] * imgs[0]['h'] * (4 if imgs[0]['fmt'] == 0x04 else 8)) // 8
            new_pix_data = new_gim_data[imgs[0]['pix_abs'] : imgs[0]['pix_abs'] + new_pix_size]
            
            new_pal_size = pal['n'] * 4
            new_pal_data = new_gim_data[pal['abs'] : pal['abs'] + new_pal_size]
            
            # Find original offsets in dec
            pal_off = None
            pix_off = None
            for i in range(0, min(256, len(dec)-4), 4):
                val = struct.unpack_from(">I", dec, i)[0]
                if 0 < val < len(dec) and val % 16 == 0:
                    if 0x300 <= val < 0x1000 and pal_off is None: pal_off = val
                    if val >= 0x1000: pix_off = val
            if pal_off is None: pal_off = 0x380
            if pix_off is None: pix_off = 0x1080
            
            # Overwrite in-place
            dec_bytes[pal_off : pal_off + new_pal_size] = new_pal_data
            
            # Pixels might overflow if user changed dimensions... but usually not
            copy_size = min(new_pix_size, len(dec_bytes) - pix_off)
            dec_bytes[pix_off : pix_off + copy_size] = new_pix_data[:copy_size]
            
            new_chunk = compress_atlus_lzss(bytes(dec_bytes), chunk)
            if not new_chunk:
                raise ValueError("Failed to recompress Atlus LZSS")
        else:
            inner_data = bytearray(chunk)
            if new_size > target_size:
                raise ValueError(f"Le nouveau GIM est plus grand que l'original dans l'archive.")
                
            for i in range(new_size):
                if inner_offset + i < len(inner_data):
                    inner_data[inner_offset + i] = new_gim_data[i]
                    
            if new_size < target_size:
                for i in range(new_size, target_size):
                    if inner_offset + i < len(inner_data):
                        inner_data[inner_offset + i] = 0
                        
            new_chunk = bytes(inner_data)
        
    # Rebuild archive
    if archive_type == "EVENT_BIN":
        rebuilt = rebuild_event_bin(data, chunk_index, new_chunk)
    elif archive_type == "ATLUS_ARCHIVE":
        rebuilt = rebuild_atlus_archive(data, chunk_index, new_chunk)
    else:
        raise ValueError(f"Type d'archive inconnu: {archive_type}")
        
    with open(out_bin_path, 'wb') as f:
        f.write(rebuilt)
        
    return True

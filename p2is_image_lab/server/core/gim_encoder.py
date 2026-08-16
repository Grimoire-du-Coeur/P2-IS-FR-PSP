"""
P2IS GIM Encoder - Encodage PNG → GIM en remplacement in-place.

Bugs corrigés :
  - Ajout des formats manquants : RGB565 (0x00), RGBA5551 (0x01), RGBA4444 (0x02)
    Avant, ces formats retournaient silencieusement le GIM original non modifié.
"""
import struct
from typing import List, Dict, Tuple
from PIL import Image
import io
from core.image_format import parse_gim, extract_gim_entry


def swizzle_psp(linear_data: bytes, w: int, h: int, bpp_bits: int) -> bytes:
    """Applique le swizzle PSP à des données linéaires."""
    row_bytes = (w * bpp_bits + 7) // 8
    pitch     = (row_bytes + 15) & ~15
    aligned_h = (h + 7) & ~7
    bw, bh    = 16, 8

    aligned_in = bytearray(aligned_h * pitch)
    for row in range(h):
        s = row * row_bytes
        d = row * pitch
        chunk = linear_data[s:s + row_bytes]
        aligned_in[d:d + len(chunk)] = chunk

    out = bytearray(aligned_h * pitch)
    dst = 0
    for by in range(0, aligned_h, bh):
        for bx in range(0, pitch, bw):
            for row in range(bh):
                for col in range(bw):
                    src = (by + row) * pitch + (bx + col)
                    if dst < len(out) and src < len(aligned_in):
                        out[dst] = aligned_in[src]
                    dst += 1
    return bytes(out)


def _encode_16bpp(pixels_rgba, w: int, h: int, order: int, fmt: int) -> bytes:
    """Encode des pixels RGBA en format 16bpp (RGB565, RGBA5551, RGBA4444) avec swizzle optionnel."""
    row_bytes = w * 2
    linear    = bytearray(h * row_bytes)

    for row in range(h):
        for col in range(w):
            pixel = pixels_rgba[row * w + col]
            r, g, b = pixel[0], pixel[1], pixel[2]
            a = pixel[3] if len(pixel) == 4 else 255
            offset = row * row_bytes + col * 2

            if fmt == 0x00:   # RGB565
                val = ((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3)
            elif fmt == 0x01:  # RGBA5551
                val = (r >> 3) | ((g >> 3) << 5) | ((b >> 3) << 10) | ((1 if a > 127 else 0) << 15)
            elif fmt == 0x02:  # RGBA4444
                val = (r >> 4) | ((g >> 4) << 4) | ((b >> 4) << 8) | ((a >> 4) << 12)
            else:
                val = 0

            struct.pack_into("<H", linear, offset, val)

    if order == 1:
        return swizzle_psp(bytes(linear), w, h, 16)
    return bytes(linear)


from .image_format import read_palette

def custom_rgba_quantize(img_rgba, original_gim, pal, max_colors):
    """
    Quantifies an RGBA image to a palette using 4D Euclidean distance (R, G, B, A),
    preventing transparency loss for palettes that rely on the alpha channel.
    """
    orig_pal_rgba = read_palette(original_gim, pal)
    if len(orig_pal_rgba) > max_colors:
        orig_pal_rgba = orig_pal_rgba[:max_colors]
        
    px_rgba = list(img_rgba.getdata())
    px_indexed = []
    color_cache = {}
    
    for p in px_rgba:
        if len(p) == 3: p = (p[0], p[1], p[2], 255)
        if p not in color_cache:
            best_idx = 0
            best_dist = float('inf')
            for i, c in enumerate(orig_pal_rgba):
                dist = (p[0]-c[0])**2 + (p[1]-c[1])**2 + (p[2]-c[2])**2 + (p[3]-c[3])**2
                if dist < best_dist:
                    best_dist = dist
                    best_idx = i
            color_cache[p] = best_idx
        px_indexed.append(color_cache[p])
        
    return px_indexed

def encode_png_to_gim_in_place(png_path: str, original_gim: bytes) -> bytes:
    """
    Encode un fichier PNG dans le format GIM de l'original (in-place).
    Tous les formats PSP GIM sont supportés :
        0x00 RGB565 | 0x01 RGBA5551 | 0x02 RGBA4444 | 0x03 RGBA8888
        0x04 INDEX4 | 0x05 INDEX8

    BUG CORRIGÉ : les formats RGB565, RGBA5551 et RGBA4444 n'étaient pas gérés
    → la fonction renvoyait le GIM original sans modification (injection silencieusement ratée).
    """
    imgs, pal, _ = parse_gim(original_gim, 0)
    if not imgs:
        raise ValueError("Impossible de parser le GIM original.")

    img_info   = imgs[0]
    w          = img_info['w']
    h          = img_info['h']
    fmt        = img_info['fmt']
    order      = img_info['order']
    img_offset = img_info['pix_abs']

    img = Image.open(png_path)
    if img.size != (w, h):
        img = img.resize((w, h), Image.Resampling.LANCZOS)

    out_gim = bytearray(original_gim)

    # ── Formats non-indexés 16bpp ─────────────────────────────────────────────
    if fmt in (0x00, 0x01, 0x02):
        img_rgba   = img.convert("RGBA")
        pixels     = list(img_rgba.getdata())
        final_pix  = _encode_16bpp(pixels, w, h, order, fmt)
        sz         = len(final_pix)
        out_gim[img_offset:img_offset + sz] = final_pix

    # ── RGBA8888 ──────────────────────────────────────────────────────────────
    elif fmt == 0x03:
        img_rgba = img.convert("RGBA")
        if order == 1:
            linear    = bytearray(img_rgba.tobytes())
            final_pix = swizzle_psp(linear, w, h, 32)
        else:
            # Write with 16-byte row pitch padding
            raw_row   = w * 4
            pitch     = (raw_row + 15) & ~15
            linear    = bytearray(h * pitch)
            src_bytes = img_rgba.tobytes()
            for row in range(h):
                linear[row*pitch:row*pitch+raw_row] = src_bytes[row*raw_row:(row+1)*raw_row]
            final_pix = bytes(linear)
        sz = len(final_pix)
        out_gim[img_offset:img_offset + sz] = final_pix

    # ── INDEX4 ────────────────────────────────────────────────────────────────
    elif fmt == 0x04:
        img_rgba = img.convert("RGBA")

        # Build original palette from GIM and remap pixels to it using custom 4D distance
        if pal:
            px = custom_rgba_quantize(img_rgba, original_gim, pal, 16)
        else:
            img_p = img_rgba.quantize(colors=16)
            px = list(img_p.getdata())

        # Encoder en 4bpp avec pitch padded à 16 bytes
        raw_row  = (w * 4 + 7) // 8          # bytes actifs par ligne
        pitch    = (raw_row + 15) & ~15       # pitch paddé
        if order == 1:
            linear_compact = bytearray(h * raw_row)
            for r in range(h):
                for c in range(0, w, 2):
                    p0 = px[r * w + c] & 0x0F
                    p1 = px[r * w + c + 1] & 0x0F if c + 1 < w else 0
                    linear_compact[r * raw_row + c // 2] = p0 | (p1 << 4)
            final_pix = swizzle_psp(bytes(linear_compact), w, h, 4)
        else:
            linear = bytearray(h * pitch)
            for r in range(h):
                for c in range(0, w, 2):
                    p0 = px[r * w + c] & 0x0F
                    p1 = px[r * w + c + 1] & 0x0F if c + 1 < w else 0
                    linear[r * pitch + c // 2] = p0 | (p1 << 4)
            final_pix = bytes(linear)
        sz = len(final_pix)
        out_gim[img_offset:img_offset + sz] = final_pix
        # Palette data left unchanged (pixels remapped to original palette)

    # ── INDEX8 ────────────────────────────────────────────────────────────────
    elif fmt == 0x05:
        img_rgba = img.convert("RGBA")

        # Build original palette from GIM and remap pixels to it using custom 4D distance
        if pal:
            px = custom_rgba_quantize(img_rgba, original_gim, pal, 256)
        else:
            img_p = img_rgba.quantize(colors=256)
            px = list(img_p.getdata())

        if order == 1:
            # Swizzle: pas de pitch padding (swizzle_psp gère l'alignement)
            final_pix = swizzle_psp(bytes(px), w, h, 8)
        else:
            # Linear: rows padded to 16-byte pitch
            pitch = (w + 15) & ~15
            linear = bytearray(h * pitch)
            for r in range(h):
                linear[r*pitch:r*pitch+w] = bytes(px[r*w:(r+1)*w])
            final_pix = bytes(linear)
        sz = len(final_pix)
        out_gim[img_offset:img_offset + sz] = final_pix
        # Palette data left unchanged (pixels remapped to original palette)

    else:
        raise ValueError(f"Format GIM {fmt:#x} non supporté pour l'encodage.")

    return bytes(out_gim)

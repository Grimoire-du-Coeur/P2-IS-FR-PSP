import struct
from typing import List, Dict, Tuple
from PIL import Image
import io
import math
from core.image_format import parse_gim, extract_gim_entry

def swizzle_psp(linear_data: bytes, w: int, h: int, bpp_bits: int) -> bytes:
    row_bytes = (w * bpp_bits + 7) // 8
    pitch = (row_bytes + 15) & ~15
    aligned_h = (h + 7) & ~7
    bw, bh = 16, 8

    aligned_in = bytearray(aligned_h * pitch)
    for row in range(h):
        s = row * row_bytes
        d = row * pitch
        # pad with zeros if needed
        data_to_copy = linear_data[s:s + row_bytes]
        aligned_in[d:d + len(data_to_copy)] = data_to_copy

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

def encode_png_to_gim_in_place(png_path: str, original_gim: bytes) -> bytes:
    # 1. Parse original GIM to get offsets and formats
    imgs, pal, _ = parse_gim(original_gim, 0)
    if not imgs:
        raise ValueError("Impossible de parser le GIM original.")
    
    img_info = imgs[0]
    w = img_info['w']
    h = img_info['h']
    fmt = img_info['fmt']
    order = img_info['order']
    img_offset = img_info['pix_abs']
    
    img = Image.open(png_path)
    if img.size != (w, h):
        # Resize or pad, but user was warned. We will resize for safety
        img = img.resize((w, h), Image.Resampling.LANCZOS)
        
    out_gim = bytearray(original_gim)
    
    if fmt == 0x04: # INDEX4
        # Convert to 16 colors
        img_p = img.convert("RGBA").convert('P', palette=Image.ADAPTIVE, colors=16)
        px = list(img_p.getdata())
        pal_data = img_p.getpalette() # RGB RGB RGB...
        
        # We need RGBA8888 palette. PIL palette doesn't have alpha if converted this way, so we assume alpha=255.
        # Actually, for transparency, we should properly quantize with alpha.
        # Simple workaround: just assume first color is transparent if needed, or build RGBA palette.
        # PIL palette is 768 bytes (256 * 3).
        new_pal = bytearray(16 * 4)
        for i in range(16):
            r = pal_data[i*3] if i*3 < len(pal_data) else 0
            g = pal_data[i*3+1] if i*3+1 < len(pal_data) else 0
            b = pal_data[i*3+2] if i*3+2 < len(pal_data) else 0
            new_pal[i*4 : i*4+4] = bytes([r, g, b, 255])
            
        # Pack 4-bit (little endian nibbles usually for PSP: pixel 0 in lower nibble)
        row_bytes = (w * 4 + 7) // 8
        linear = bytearray(h * row_bytes)
        for r in range(h):
            for c in range(0, w, 2):
                p0 = px[r * w + c] & 0x0F
                p1 = px[r * w + c + 1] & 0x0F if c + 1 < w else 0
                linear[r * row_bytes + c // 2] = p0 | (p1 << 4)
                
        final_pixels = swizzle_psp(linear, w, h, 4) if order == 1 else bytes(linear)
        
        # Replace image payload
        sz = len(final_pixels)
        out_gim[img_offset:img_offset+sz] = final_pixels
        
        # Replace palette payload
        if pal:
            pal_offset = pal['abs']
            pal_fmt = pal['fmt']
            # We assume palette is RGBA8888 (fmt=3). If it's something else, we should convert.
            # Usually INDEX4 uses RGBA8888 or RGBA4444.
            # We will just write the 64 bytes. If original was smaller, we only write what fits.
            if pal_fmt == 3: # RGBA8888
                out_gim[pal_offset:pal_offset+64] = new_pal[:min(64, len(out_gim)-pal_offset)]
            elif pal_fmt == 2: # RGBA4444
                # Convert new_pal to RGBA4444
                pal4444 = bytearray(16 * 2)
                for i in range(16):
                    r, g, b, a = new_pal[i*4], new_pal[i*4+1], new_pal[i*4+2], new_pal[i*4+3]
                    val = ((r >> 4) << 0) | ((g >> 4) << 4) | ((b >> 4) << 8) | ((a >> 4) << 12)
                    pal4444[i*2:i*2+2] = struct.pack("<H", val)
                out_gim[pal_offset:pal_offset+32] = pal4444[:min(32, len(out_gim)-pal_offset)]
            
    elif fmt == 0x05: # INDEX8
        img_p = img.convert("RGBA").convert('P', palette=Image.ADAPTIVE, colors=256)
        px = list(img_p.getdata())
        pal_data = img_p.getpalette()
        
        new_pal = bytearray(256 * 4)
        for i in range(256):
            if i*3+2 < len(pal_data):
                new_pal[i*4 : i*4+4] = bytes([pal_data[i*3], pal_data[i*3+1], pal_data[i*3+2], 255])
            else:
                new_pal[i*4 : i*4+4] = b'\x00\x00\x00\xff'
                
        linear = bytearray(px)
        final_pixels = swizzle_psp(linear, w, h, 8) if order == 1 else bytes(linear)
        
        sz = len(final_pixels)
        out_gim[img_offset:img_offset+sz] = final_pixels
        
        if pal:
            pal_offset = pal['abs']
            pal_fmt = pal['fmt']
            if pal_fmt == 3:
                out_gim[pal_offset:pal_offset+1024] = new_pal[:min(1024, len(out_gim)-pal_offset)]
            elif pal_fmt == 2:
                pal4444 = bytearray(256 * 2)
                for i in range(256):
                    r, g, b, a = new_pal[i*4], new_pal[i*4+1], new_pal[i*4+2], new_pal[i*4+3]
                    val = ((r >> 4) << 0) | ((g >> 4) << 4) | ((b >> 4) << 8) | ((a >> 4) << 12)
                    pal4444[i*2:i*2+2] = struct.pack("<H", val)
                out_gim[pal_offset:pal_offset+512] = pal4444[:min(512, len(out_gim)-pal_offset)]

    elif fmt == 3: # RGBA8888
        img = img.convert("RGBA")
        linear = bytearray(img.tobytes())
        final_pixels = swizzle_psp(linear, w, h, 32) if order == 1 else bytes(linear)
        sz = len(final_pixels)
        out_gim[img_offset:img_offset+sz] = final_pixels

    return bytes(out_gim)

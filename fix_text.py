import sys

path = 'p2is_tool/server/src/core/text.py'
with open(path, 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace('("\xc8", "\u0168")', '("\xc8", "\u0145")')

code = code.replace('def text_to_bytes(text: str) -> bytes:', 'def text_to_bytes(text: str) -> bytes:\n    text = text.replace("\u2026", "...").replace("\xab", "\\"").replace("\xbb", "\\"")')

old_return = 'return b"".join(out)'
new_return = 'res = b"".join(out)\n    if len(res) % 2 != 0:\n        res += b"\\x00"\n    return res'
code = code.replace(old_return, new_return)

align_mid_old = '''        diff = orig_off - fr_off
        if diff > 0:
            n_sp = diff // 2
            out_fr += "[SP]" * n_sp
            
        out_fr += '[NULL][NULL]"' + parts_fr[i]'''

align_mid_new = '''        diff = orig_off - fr_off
        if diff > 0:
            n_sp = diff // 2
            out_fr += "[SP]" * n_sp
        elif diff < 0:
            while diff < 0 and len(out_fr) > 0:
                out_fr = out_fr[:-1]
                fr_off = len(text_to_bytes('"' + nom_fr + "\\n" + out_fr))
                diff = orig_off - fr_off
            
        out_fr += '[NULL][NULL]"' + parts_fr[i]'''
code = code.replace(align_mid_old, align_mid_new)

with open(path, 'w', encoding='utf-8') as f:
    f.write(code)

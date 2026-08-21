import sys

path = 'p2is_tool/server/src/config.py'
with open(path, 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace('("\xc8", "\u0168")', '("\xc8", "\u0145")')

with open(path, 'w', encoding='utf-8') as f:
    f.write(code)

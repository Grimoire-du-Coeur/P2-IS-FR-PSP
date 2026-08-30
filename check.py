with open('p2is_tool/server/src/core/text.py', 'r', encoding='utf-8') as f:
    text = f.read()
idx = text.find('if b0 in (0x7b, 0x7f, 0x81, 0x0d, 0x00, 0x1b, 0x05, 0x27, 0x09, 0x0b):')
print(text[idx:idx+400])

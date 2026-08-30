with open('p2is_tool/server/src/core/text.py', 'r', encoding='utf-8') as f:
    text = f.read()
idx = text.find('if tag.startswith("[U+")')
print(text[idx:idx+400])

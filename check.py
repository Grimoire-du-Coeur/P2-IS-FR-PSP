import sys
with open('p2is_tool/server/src/encoders/bin_encoder.py', 'r', encoding='utf-8') as f:
    text = f.read()
idx = text.find('t_fr = \\'\\'.join(tokens) + "..."')
print(text[idx-200:idx+200].encode('ascii', 'backslashreplace').decode('ascii'))

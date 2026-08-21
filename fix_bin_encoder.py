import sys

path = 'p2is_tool/server/src/encoders/bin_encoder.py'
with open(path, 'r', encoding='utf-8') as f:
    code = f.read()

old_loop = '''                while tokens and len(text_to_bytes('"' + n_fr + "\\n" + ''.join(tokens))) > avail - len(nl_suffix):
                    tokens.pop()
                    
                t_fr = ''.join(tokens)'''

new_loop = '''                while tokens and len(text_to_bytes('"' + n_fr + "\\n" + ''.join(tokens) + "...")) > avail - len(nl_suffix):
                    tokens.pop()
                if tokens:
                    t_fr = ''.join(tokens) + "..."
                else:
                    t_fr = ""'''

code = code.replace(old_loop, new_loop)

old_loop2 = '''                while tokens and len(text_to_bytes('"' + n_fr + "\\n" + ''.join(tokens))) > avail - len(nl_sfx):
                    tokens.pop()
                    
                t_fr = ''.join(tokens)'''

new_loop2 = '''                while tokens and len(text_to_bytes('"' + n_fr + "\\n" + ''.join(tokens) + "...")) > avail - len(nl_sfx):
                    tokens.pop()
                if tokens:
                    t_fr = ''.join(tokens) + "..."
                else:
                    t_fr = ""'''

code = code.replace(old_loop2, new_loop2)

with open(path, 'w', encoding='utf-8') as f:
    f.write(code)

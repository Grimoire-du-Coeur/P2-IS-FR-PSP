import os, json
sys.path.append('p2is_tool/server')
from pad_menus import align_menu_options

trad_dir = r'C:\Users\nolan\Desktop\6666666656\repo\traduction'

toro_menus = {
    'What[SP]can[SP]I[SP]do[SP]for[SP]you[SP]today?\n[1208][0003][1210][U+0475]Ask[SP]about[SP]rumors\nTalk[SP]with[SP]Toro\nNever[SP]mind': 'Je peux vous aider?\n[1208][0003][1210][0475]Infos rumeurs\nParler à Toro\nRien',
    'What[SP]do[SP]you[SP]want[SP]to[SP]know[SP]about?\n[1208][0004][1210][U+0476]Weapon[SP]shop[SP]rumors\n[1210][U+0477]Armor[SP]shop[SP]rumors\n[1210][U+0478]Other[SP]rumors\nNothing': 'Sur quoi?\n[1208][0004][1210][0476]Rumeurs armureries\n[1210][0477]Rumeurs armures\n[1210][0478]Autres rumeurs\nRien',
    'For[SP]which[SP]area?\n[1208][0005][1210][U+046A]Rengedai\n[1210][U+046B]Yumezaki\n[1210][U+046C]Aoba\n[1210][U+046D]Kounan\nNone': 'Secteur?\n[1208][0005][1210][046A]Rengedai\n[1210][046B]Yumezaki\n[1210][046C]Aoba\n[1210][046D]Kounan\nRien',
    'For[SP]which[SP]area?\n[1208][0005][1210][U+046E]Rengedai\n[1210][U+046F]Yumezaki\n[1210][U+0470]Aoba\n[1210][U+0471]Kounan\nNone': 'Secteur?\n[1208][0005][1210][046E]Rengedai\n[1210][046F]Yumezaki\n[1210][0470]Aoba\n[1210][0471]Kounan\nRien',
    'What[SP]do[SP]you[SP]want[SP]to[SP]know[SP]about?\n[1208][0004][1210][U+0472]Magazine[SP]sweepstakes[SP]rumors\n[1210][U+0473]Mu[SP]rumors\n[1210][U+0474]Legendary[SP]weapon[SP]rumors\nNone[SP]of[SP]them': 'Sur quoi?\n[1208][0004][1210][0472]Tirages de magazines\n[1210][0473]Infos Mu\n[1210][0474]Armes légendaires\nAucune'
}
chikarin_menus = {
    'What[SP]do[SP]you[SP]want[SP]to[SP]know[SP]about?\n[1208][0003][1210][U+0475]Ask[SP]about[SP]rumors\nTalk[SP]with[SP]Chikarin\nNever[SP]mind': 'Sur quoi?\n[1208][0003][1210][0475]Infos rumeurs\nParler à Chikarin\nRien',
    'What[SP]rumor[SP]do[SP]you[SP]want[SP]details[SP]on?\n[1208][0004][1210][U+0472]Magazine[SP]sweepstakes\n[1210][U+0473]Mu\n[1210][U+0474]Legendary[SP]weapons\nNone': 'Laquelle ?\n[1208][0004][1210][0472]Tirages de magazines\n[1210][0473]Sur Mu\n[1210][0474]Armes légendaires\nAucune'
}
all_menus = {**toro_menus, **chikarin_menus}
total = 0
files_ch = 0
for r, _, fs in os.walk(trad_dir):
    for file in fs:
        if not file.endswith('.json'): continue
        path = os.path.join(r, file)
        with open(path, 'r', encoding='utf-8') as f:
            try: d = json.load(f)
            except: continue
        ch = False
        for e in d:
            o = e.get('texte_orig', '')
            if o in all_menus:
                nf = all_menus[o]
                pf = align_menu_options(o, nf, e.get('id'))
                if e.get('texte_fr') != pf:
                    e['texte_fr'] = pf
                    ch = True
                    total += 1
        if ch:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(d, f, ensure_ascii=False, indent=2)
            files_ch += 1
print(f'Fixed {total} menus in {files_ch} files.')

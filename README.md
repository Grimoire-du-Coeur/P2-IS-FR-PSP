# Persona 2: Innocent Sin FR (PSP) — ULES01557

Projet de traduction française amateur de Persona 2: Innocent Sin sur PSP.
Ce dépôt contient les outils pour extraire, traduire et réinjecter les scripts du jeu.

> ⚠️ Ce projet ne distribue aucun fichier du jeu. 
> Vous devez posséder votre propre ISO européenne (ULES01557).

## Pipeline complet
```
ISO (ULES01557)
    │
    ▼  extract_cpk_from_iso()
P2PT_ALL.cpk
    │
    ▼  extract_event_from_cpk()
event.bin
    │
    ▼  extract_scripts_from_event()
script_0.bin … script_398.bin
    │
    ▼  decode_all_scripts()
script_0.json … script_398.json   ← ✏️ on traduit ici
    │
    ▼  encode_script()
script_0_fr.bin … script_398_fr.bin
    │
    ▼  rebuild_iso()
ISO traduite ✅
```

### Installation
```bash
git clone https://github.com/chenetulipe/P2-FR-IS-PSP
cd P2-FR-IS-PSP
pip install customtkinter
python p2is_tool.py
```

### Utilisation

Lance `p2is_tool.py` et suis les 3 onglets dans l'ordre :

1. **Pipeline Extraction** — charge ton ISO et extrais les scripts en JSON en 4 clics
2. **Traduction** — encode tes JSON traduits en `.bin`
3. **Rebuild ISO** — réinjecte tout et génère l'ISO FR jouable

## Avancement

| Contenu               | Progression  |
|-----------------------|--------------|
| Scripts (dialogues)   |     1/399    |
| Police (accents FR)   |   En cours   |
| Menus                 | Non commencé |
| ...                   | Non commencé |

### Outils tiers utilisés
- [UMDGen](https://www.romhacking.net/utilities/1218/) — manipulation ISO PSP
- [CriFsLib](https://github.com/Sewer56/CriFsV2Lib) — extraction CPK
- [PPSSPP](https://www.ppsspp.org/) — émulation PSP pour les tests

## Inspirations & Références

- [P2-EP-PSP](https://github.com/sayucchin/P2-EP-PSP) par **sayucchin & équipe** — 
  projet de traduction de Persona 2: Eternal Punishment PSP.  
  L'analyse de leur code source (event.rs, main.rs) nous a permis de comprendre la structure de event.bin (gzip + table d'offsets). Nos outils ont été développés indépendamment en Python.

## Contact & Contribuer

Tu veux aider à traduire, tester, ou juste suivre l'avancement ?

- **Discord serveur** : [Rejoindre](https://discord.gg/rd4ckSWHNm)
- **Discord perso** : `@chenetulipe`
- **GitHub Issues** : pour signaler un bug ou proposer une amélioration
- **Pull Requests** : les contributions sont les bienvenues !

## Crédits
- @chenetulipe
- @GarloulouLeAsriel
- **Atlus** — Persona 2: Innocent Sin (© Atlus)

## Avertissement légal

Ce projet est une traduction amateur à but non lucratif.
Tous les droits sur Persona 2: Innocent Sin appartiennent à Atlus.
Ne distribuez pas les fichiers du jeu.

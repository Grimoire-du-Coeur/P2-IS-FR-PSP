# Persona 2: Innocent Sin FR (PSP) - ULES01557
![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)

Projet de traduction française amateur de Persona 2: Innocent Sin sur PSP.
Ce dépôt contient les outils pour extraire, traduire et réinjecter les scripts du jeu.

> ⚠️ Ce projet ne distribue aucun fichier du jeu.
> Vous devez posséder votre propre ISO européenne (ULES01557).

---

## 📺 Vidéo de présentation
🎬 **[Clique ici pour voir la vidéo](https://youtu.be/wxEEJYjx2Sw)**

![Miniature](https://img.youtube.com/vi/wxEEJYjx2Sw/maxresdefault.jpg)

---

## Avancement
| Contenu               | Progression  |
|-----------------------|--------------|
| [Scripts (dialogues)](https://github.com/chenetulipe/P2-FR-IS-PSP/tree/main/scripts)   |     304/399    |
| Police (accents FR)   |      ✅      |
| Textures HD        | 34/42 |
| ...                   | 🔄 |

### Outil dédié au projet
- [JsonVerify](https://github.com/Garloulou/JsonVerify) par **@Garloulou** - outil de validation des fichiers JSON traduits

---
## Compatibilité Pack HD
Le projet supporte le mod **HD UI for Persona 2 - Innocent Sin**, pour lequel nous avons reçu une autorisation de modification.
> Conformément à notre accord, nous ne distribuons qu'un patch contenant les textures françaises modifiées.
> Téléchargez le pack original : [HD UI on GameBanana](https://gamebanana.com/mods/308752) 
> Appliquez notre patch FR (disponible bientôt) par-dessus.

Un immense merci à [@racawr](https://gamebanana.com/members/1865032) pour son travail incroyable et sa gentillesse.

---

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
1. **Pipeline Extraction** - charge ton ISO et extrais les scripts en JSON
2. **Traduction** - encode tes JSON traduits en `.bin`
3. **Rebuild ISO** - réinjecte tout et génère l'ISO FR jouable

### Outils tiers utilisés
- [UMDGen](https://www.romhacking.net/utilities/1218/) - manipulation ISO PSP
- [CriFsLib](https://github.com/Sewer56/CriFsV2Lib) - extraction CPK
- [PPSSPP](https://www.ppsspp.org/) - émulation PSP pour les tests

---

## Inspirations & Références
- [P2-EP-PSP](https://github.com/sayucchin/P2-EP-PSP) par **sayucchin & équipe** -
  projet de traduction de Persona 2: Eternal Punishment PSP.
  L'analyse de leur code source (event.rs, main.rs) nous a permis de comprendre la structure de event.bin (gzip + table d'offsets). Nos outils ont été développés indépendamment en Python.

---

## Contact & Contribuer
Tu veux aider à traduire, tester, ou juste suivre l'avancement ?
- **Discord serveur** : [Rejoindre](https://discord.gg/rd4ckSWHNm)
- **Discord perso** : `@chenetulipe`
- **GitHub Issues** : pour signaler un bug ou proposer une amélioration
- **Pull Requests** : les contributions sont les bienvenues !

## Crédits
- @chenetulipe
- @Garloulou
- **Atlus** - Persona 2: Innocent Sin (© Atlus)

---

## Licence & Avertissement légal
Ce projet est sous licence **[CC BY-NC-SA 4.0](LICENSE)** - libre d'utilisation et de modification,
interdit à la vente, attribution obligatoire.

Persona 2: Innocent Sin est © Atlus. Ce projet est une traduction amateur à but non lucratif.
Aucun fichier du jeu n'est distribué. Vous devez posséder votre propre copie du jeu.

---

## Star History

<a href="https://www.star-history.com/?repos=chenetulipe%2FP2-FR-IS-PSP&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/image?repos=chenetulipe/P2-FR-IS-PSP&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/image?repos=chenetulipe/P2-FR-IS-PSP&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/image?repos=chenetulipe/P2-FR-IS-PSP&type=date&legend=top-left" />
 </picture>
</a>

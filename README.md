<div align="center">

# Persona 2: Innocent Sin â€” Traduction FranÃ§aise

**Patch de traduction intÃ©gral pour la version PSP europÃ©enne (ULES01557)**

<br/>

<a href="https://fr.wikipedia.org/wiki/PlayStation_Portable"><img src="https://img.shields.io/badge/PlayStation_Portable-103F91?style=for-the-badge&logo=playstation&logoColor=white" alt="Plateforme" /></a>
<img src="https://img.shields.io/badge/Statut-BÃŠTA_PUBLIQUE-6b21a8?style=for-the-badge" alt="Statut" />
<a href="https://personalegrimoireducoeur.fr/"><img src="https://img.shields.io/badge/Site_Web-personagrimoireducoeur.fr-10b981?style=for-the-badge&logo=vercel&logoColor=white" alt="Site Officiel" /></a>

<br/>

<a href="https://github.com/chenetulipe/P2-FR-IS-PSP/commits/main"><img src="https://img.shields.io/github/last-commit/chenetulipe/P2-FR-IS-PSP?style=flat-square&color=2ea043" alt="Dernier Commit" /></a>
<a href="https://github.com/chenetulipe/P2-FR-IS-PSP/issues"><img src="https://img.shields.io/github/issues/chenetulipe/P2-FR-IS-PSP?style=flat-square&color=d73a49" alt="Issues" /></a>
<a href="https://discord.gg/rd4ckSWHNm"><img src="https://img.shields.io/discord/1400909421609095323?color=5865F2&label=Discord&logo=discord&logoColor=white&style=flat-square" alt="Discord" /></a>
<a href="https://github.com/chenetulipe/P2-FR-IS-PSP/stargazers"><img src="https://img.shields.io/github/stars/chenetulipe/P2-FR-IS-PSP?style=flat-square&color=e3b341" alt="Stars" /></a>

<br/><br/>

[![TÃ©lÃ©charger le Patch](https://img.shields.io/badge/TÃ‰LÃ‰CHARGER_LE_PATCH_FR_â€”_BÃŠTA_v0.1.3-e3b341?style=for-the-badge&logo=github&logoColor=black)](https://github.com/chenetulipe/P2-FR-IS-PSP/releases)

**L'intÃ©gralitÃ© du scÃ©nario principal est jouable en franÃ§ais.**

</div>

<br/>

---

## AperÃ§u du Projet

Persona 2: Innocent Sin n'a jamais eu de version française officielle. Ce dépôt regroupe tout ce qui tourne autour du projet : le patch jouable, les outils de romhacking qu'on a développés pour ça, et la documentation technique qu'on a accumulée pendant le reverse-engineering du jeu.

<div align="center">
  <a href="https://youtu.be/rGHRMPw-bbo">
    <img src="https://img.youtube.com/vi/rGHRMPw-bbo/maxresdefault.jpg" alt="AperÃ§u gameplay Persona 2 FR" width="420" style="border-radius:6px;"/>
  </a>
  <a href="https://www.youtube.com/@chenetulipe">
    <img src="https://img.youtube.com/vi/aL3N1Xk6X8w/maxresdefault.jpg" alt="Tutoriel installation patch FR" width="420" style="border-radius:6px;"/>
  </a>
  <br/>
  <sub>Gauche : aperÃ§u du jeu en franÃ§ais â€” Droite : tutoriel d'installation par chenetulipe</sub>
</div>

> [!NOTE]
> **Avancement rapide** â€” Histoire principale et dialogues PNJ : **100%**. Menus et textes systÃ¨me (EBOOT) : en cours (~15%). Pour le tableau complet, voir [CONTRIBUTING.md](./CONTRIBUTING.md).

<br/>

---

## Guide d'Installation

### Ã‰tape 1 â€” Patcher l'ISO

1. TÃ©lÃ©chargez le dernier fichier `.xdelta` depuis les **[Releases](https://github.com/chenetulipe/P2-FR-IS-PSP/releases)**.
2. Procurez-vous lÃ©galement une image ISO de la version europÃ©enne du jeu (`ULES01557`).
3. Rendez-vous sur le **[Patcher Web en ligne](https://personalegrimoireducoeur.fr/patcher/)** â€” aucune installation requise.
4. DÃ©posez votre ISO et le fichier `.xdelta`, puis gÃ©nÃ©rez l'ISO traduite.

### Ã‰tape 2 â€” Installer le Pack de Textures HD (recommandÃ© sur PPSSPP)

Ce pack est nÃ©cessaire pour afficher les accents franÃ§ais avec la police haute dÃ©finition.

1. TÃ©lÃ©chargez le pack HD de base sur GameBanana : [HD UI for Persona 2](https://gamebanana.com/mods/308752).
2. Placez-le dans `TEXTURES/ULES01557/` dans le dossier de votre Ã©mulateur PPSSPP.
3. TÃ©lÃ©chargez le **Patch de Textures FR** depuis les [Releases](https://github.com/chenetulipe/P2-FR-IS-PSP/releases) et superposez-le par-dessus.
4. Activez l'option *Remplacer les textures* dans les paramÃ¨tres PPSSPP.

<br/>

---

## La Suite d'Outils

Toute la chaîne de traduction repose sur des outils qu'on a développés nous-mêmes, parce qu'aucun outil existant ne gérait les particularités du moteur Atlus PSP.

> **Dépendances Python** - Toutes les dépendances (`fastapi`, `uvicorn`, `pydantic`, `Pillow`, `pycdlib`, `customtkinter`) sont regroupées dans `requirements.txt` à la racine. Installer avec : `pip install -r requirements.txt`

---

### p2is_tool â€” L'outil principal

Application web locale permettant d'extraire, traduire et rÃ©injecter les scripts du jeu de faÃ§on collaborative.

<div align="left">
  <img src="https://img.shields.io/badge/Backend-FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/Langage-Python-3670A0?style=flat-square&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Frontend-React-20232A?style=flat-square&logo=react&logoColor=61DAFB" />
</div>

GÃ¨re l'extraction depuis l'ISO, le dÃ©codage du bytecode Atlus, la reconstruction des tables de pointeurs absolus, et la rÃ©injection dans l'archive CPK.

---

### p2is_patcher â€” Le Patcher Web

Application autonome tournant dans le navigateur, sans aucune dÃ©pendance Ã  installer cÃ´tÃ© utilisateur.

<div align="left">
  <img src="https://img.shields.io/badge/Moteur-WebAssembly-654FF0?style=flat-square&logo=webassembly&logoColor=white" />
  <img src="https://img.shields.io/badge/Frontend-HTML%2FJS-E34F26?style=flat-square&logo=html5&logoColor=white" />
</div>

BasÃ© sur DeltaPatcher compilÃ© en WASM. Utilise un Service Worker pour patcher des ISO de plus d'1 Go sans saturer la RAM du navigateur.

---

### p2is_image_lab â€” Le Laboratoire d'Images

Outil spÃ©cialisÃ© dans la manipulation des images au format GIM compressÃ© CRILAYLA, nÃ©cessaire pour modifier les Ã©crans de chargement et les Ã©lÃ©ments de l'interface graphique.

<div align="left">
  <img src="https://img.shields.io/badge/Backend-FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/Langage-Python-3670A0?style=flat-square&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Frontend-React-20232A?style=flat-square&logo=react&logoColor=61DAFB" />
</div>

ImplÃ©mente un compresseur CRILAYLA (greedy) en Python pur, permettant de rÃ©injecter des images dans les archives CPK sans dÃ©passer les contraintes de taille de l'ISO.

---

### p2is_audio_lab â€” Le Laboratoire Audio

Outil d'extraction et de conversion des pistes audio au format propriÃ©taire ATRAC3 (AT3), utilisÃ© pour les doublages et musiques du jeu.

<div align="left">
  <img src="https://img.shields.io/badge/Langage-Python-3670A0?style=flat-square&logo=python&logoColor=white" />
</div>

Pilote ATRACTool-Reloaded en ligne de commande pour assurer la conversion depuis et vers le format AT3 sans dÃ©pendance directe.

<br/>

---

## Clause de Non-ResponsabilitÃ© et Licences

> [!WARNING]
> Ce projet ne distribue **aucun fichier original du jeu ni ROM piratÃ©e**. Vous devez extraire lÃ©galement votre propre image disque depuis un UMD original. Ce patch cible exclusivement la version europÃ©enne `ULES01557`. *Persona 2: Innocent Sin* est une propriÃ©tÃ© intellectuelle d'Atlus / SEGA. L'Ã©quipe dÃ©cline toute responsabilitÃ© en cas de corruption de donnÃ©es.

### Licences

**Patch FR et outils maison** (`p2is_tool`, `p2is_audio_lab`, `p2is_image_lab`) â€” licence **[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)**.

- RÃ©utilisation et modification autorisÃ©es Ã  condition de crÃ©diter l'Ã©quipe, de ne pas en faire un usage commercial, et de redistribuer sous la mÃªme licence.
- Les crÃ©ateurs de contenu (YouTube, Twitch) peuvent utiliser ce patch et monÃ©tiser leurs vidÃ©os normalement.

**Web Patcher** (`p2is_patcher`) â€” licence **[GPL-2.0](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html)**, imposÃ©e par l'intÃ©gration du code source de DeltaPatcher.

### Outils tiers utilisÃ©s

| Outil | RÃ´le | Licence |
|:---|:---|:---|
| **p2is_cpk_tool.py** | Extraction et reconstruction CPK (remplace CriFsLib) | Interne CC BY-NC-SA 4.0 |
| **pspdecrypt** (John-K) | DÃ©chiffrement EBOOT, appelÃ© en externe | Open-Source |
| **pycdlib** (clalancette) | Lecture ISO 9660, importÃ©e dynamiquement | LGPL-2.1 |
| **DeltaPatcher** (marco-calautti) | Moteur de patch binaire compilÃ© dans p2is_patcher | GPL-2.0 |
| **ATRACTool-Reloaded** (XyLe-GBP) | Conversion audio AT3, appelÃ© en externe | Voir dÃ©pÃ´t |

<br/>

---

## Documentation

| Fichier | Contenu |
|:---|:---|
| [DEVELOPER.md](./DEVELOPER.md) | Architecture technique complÃ¨te, reverse-engineering du moteur Atlus, formats de fichiers, opcodes, algorithmes |
| [CONTRIBUTING.md](./CONTRIBUTING.md) | Guide de contribution, tableau d'avancement dÃ©taillÃ©, rÃ¨gles de traduction |
| [Dictionnaire.md](./Dictionnaire.md) | Glossaire officiel de traduction â€” rÃ©fÃ©rence absolue |
| [SUIVI.md](./SUIVI.md) | Historique des versions et notes de patch |
| [CREDITS.md](./CREDITS.md) | Ã‰quipe principale et contributeurs |

Besoin d'aide ? Consultez la **[FAQ officielle](https://personalegrimoireducoeur.fr/faq.html)** ou rejoignez le **[Discord](https://discord.gg/rd4ckSWHNm)**.

<div align="center">
  <a href="https://www.star-history.com/?repos=chenetulipe%2FP2-FR-IS-PSP&type=date&legend=top-left">
    <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=chenetulipe/P2-FR-IS-PSP&type=date&legend=top-left&sealed_token=LFm90kimgTV0pKr7wph4I01fXMDcl0pp1R6gKZQj-A7IbzSxbcuQ3Te4pkPherfmIEivpEoqHEUGj9nyRkBIcEEDu5ejv9MLjA1aY8v8ynFglkEs_gTGdQ" width="800" />
  </a>
</div>


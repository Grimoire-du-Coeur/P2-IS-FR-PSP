<div align="center">

# Persona 2: Innocent Sin - Traduction Française

**Patch de traduction intégral pour la version PSP européenne (ULES01557)**

<br/>

<a href="https://fr.wikipedia.org/wiki/PlayStation_Portable"><img src="https://img.shields.io/badge/PlayStation_Portable-103F91?style=for-the-badge&logo=playstation&logoColor=white" alt="Plateforme" /></a>
<img src="https://img.shields.io/badge/Statut-BÊTA_PUBLIQUE-6b21a8?style=for-the-badge" alt="Statut" />
<a href="https://personalegrimoireducoeur.fr/"><img src="https://img.shields.io/badge/Site_Web-personagrimoireducoeur.fr-10b981?style=for-the-badge&logo=vercel&logoColor=white" alt="Site Officiel" /></a>

<br/>

<a href="https://github.com/chenetulipe/P2-FR-IS-PSP/commits/main"><img src="https://img.shields.io/github/last-commit/chenetulipe/P2-FR-IS-PSP?style=flat-square&color=2ea043" alt="Dernier Commit" /></a>
<a href="https://github.com/chenetulipe/P2-FR-IS-PSP/issues"><img src="https://img.shields.io/github/issues/chenetulipe/P2-FR-IS-PSP?style=flat-square&color=d73a49" alt="Issues" /></a>
<a href="https://discord.gg/rd4ckSWHNm"><img src="https://img.shields.io/discord/1400909421609095323?color=5865F2&label=Discord&logo=discord&logoColor=white&style=flat-square" alt="Discord" /></a>
<a href="https://github.com/chenetulipe/P2-FR-IS-PSP/stargazers"><img src="https://img.shields.io/github/stars/chenetulipe/P2-FR-IS-PSP?style=flat-square&color=e3b341" alt="Stars" /></a>

<br/><br/>

[![Télécharger le Patch](https://img.shields.io/badge/TÉLÉCHARGER_LE_PATCH_FR_-_BÊTA_v0.1.3-e3b341?style=for-the-badge&logo=github&logoColor=black)](https://github.com/chenetulipe/P2-FR-IS-PSP/releases)

**L'intégralité du scénario principal est jouable en français.**

</div>

<br/>

---

## Aperçu du Projet

Persona 2: Innocent Sin n'a jamais eu de version française officielle. Ce dépôt regroupe tout ce qui tourne autour du projet : le patch jouable, les outils de romhacking qu'on a développés pour ça, et la documentation technique qu'on a accumulée pendant le reverse-engineering du jeu.

<div align="center">
  <a href="https://youtu.be/rGHRMPw-bbo">
    <img src="https://img.youtube.com/vi/rGHRMPw-bbo/maxresdefault.jpg" alt="Aperçu gameplay Persona 2 FR" width="420" style="border-radius:6px;"/>
  </a>
  <a href="https://www.youtube.com/@chenetulipe">
    <img src="https://img.youtube.com/vi/aL3N1Xk6X8w/maxresdefault.jpg" alt="Tutoriel installation patch FR" width="420" style="border-radius:6px;"/>
  </a>
  <br/>
  <sub>Gauche : aperçu du jeu en français - Droite : tutoriel d'installation par chenetulipe</sub>
</div>

> [!NOTE]
> **Avancement rapide** - Histoire principale et dialogues PNJ : **100%**. Menus et textes système (EBOOT) : en cours (~15%). Pour le tableau complet, voir [CONTRIBUTING.md](./CONTRIBUTING.md).

<br/>

---

## Guide d'Installation

### Étape 1 - Patcher l'ISO

1. Téléchargez le dernier fichier `.xdelta` depuis les **[Releases](https://github.com/chenetulipe/P2-FR-IS-PSP/releases)**.
2. Procurez-vous légalement une image ISO de la version européenne du jeu (`ULES01557`).
3. Rendez-vous sur le **[Patcher Web en ligne](https://personalegrimoireducoeur.fr/patcher/)** - aucune installation requise.
4. Déposez votre ISO et le fichier `.xdelta`, puis générez l'ISO traduite.

### Étape 2 - Installer le Pack de Textures HD (recommandé sur PPSSPP)

Ce pack est nécessaire pour afficher les accents français avec la police haute définition.

1. Téléchargez le pack HD de base sur GameBanana : [HD UI for Persona 2](https://gamebanana.com/mods/308752).
2. Placez-le dans `TEXTURES/ULES01557/` dans le dossier de votre émulateur PPSSPP.
3. Téléchargez le **Patch de Textures FR** depuis les [Releases](https://github.com/chenetulipe/P2-FR-IS-PSP/releases) et superposez-le par-dessus.
4. Activez l'option *Remplacer les textures* dans les paramètres PPSSPP.

<br/>

---

## La Suite d'Outils

Toute la chaîne de traduction repose sur des outils qu'on a développés nous-mêmes, parce qu'aucun outil existant ne gérait les particularités du moteur Atlus PSP.

> **Dépendances Python** - Toutes les dépendances (`fastapi`, `uvicorn`, `pydantic`, `Pillow`, `pycdlib`, `customtkinter`) sont regroupées dans `requirements.txt` à la racine. Installer avec : `pip install -r requirements.txt`

---

### p2is_tool - L'outil principal

Application web locale permettant d'extraire, traduire et réinjecter les scripts du jeu de façon collaborative.

<div align="left">
  <img src="https://img.shields.io/badge/Backend-FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/Langage-Python-3670A0?style=flat-square&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Frontend-React-20232A?style=flat-square&logo=react&logoColor=61DAFB" />
</div>

Gère l'extraction depuis l'ISO, le décodage du bytecode Atlus, la reconstruction des tables de pointeurs absolus, et la réinjection dans l'archive CPK.

---

### p2is_patcher - Le Patcher Web

Application autonome tournant dans le navigateur, sans aucune dépendance à installer côté utilisateur.

<div align="left">
  <img src="https://img.shields.io/badge/Moteur-WebAssembly-654FF0?style=flat-square&logo=webassembly&logoColor=white" />
  <img src="https://img.shields.io/badge/Frontend-HTML%2FJS-E34F26?style=flat-square&logo=html5&logoColor=white" />
</div>

Basé sur DeltaPatcher compilé en WASM. Utilise un Service Worker pour patcher des ISO de plus d'1 Go sans saturer la RAM du navigateur.

---

### p2is_image_lab - Le Laboratoire d'Images

Outil spécialisé dans la manipulation des images au format GIM compressé CRILAYLA, nécessaire pour modifier les écrans de chargement et les éléments de l'interface graphique.

<div align="left">
  <img src="https://img.shields.io/badge/Backend-FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/Langage-Python-3670A0?style=flat-square&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Frontend-React-20232A?style=flat-square&logo=react&logoColor=61DAFB" />
</div>

Implémente un compresseur CRILAYLA (greedy) en Python pur, permettant de réinjecter des images dans les archives CPK sans dépasser les contraintes de taille de l'ISO.

---

### p2is_audio_lab - Le Laboratoire Audio

Outil d'extraction et de conversion des pistes audio au format propriétaire ATRAC3 (AT3), utilisé pour les doublages et musiques du jeu.

<div align="left">
  <img src="https://img.shields.io/badge/Langage-Python-3670A0?style=flat-square&logo=python&logoColor=white" />
</div>

Pilote ATRACTool-Reloaded en ligne de commande pour assurer la conversion depuis et vers le format AT3 sans dépendance directe.

<br/>

---

## Clause de Non-Responsabilité et Licences

> [!WARNING]
> Ce projet ne distribue **aucun fichier original du jeu ni ROM piratée**. Vous devez extraire légalement votre propre image disque depuis un UMD original. Ce patch cible exclusivement la version européenne `ULES01557`. *Persona 2: Innocent Sin* est une propriété intellectuelle d'Atlus / SEGA. L'équipe décline toute responsabilité en cas de corruption de données.

### Licences

**Patch FR et outils maison** (`p2is_tool`, `p2is_audio_lab`, `p2is_image_lab`) - licence **[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)**.

- Réutilisation et modification autorisées à condition de créditer l'équipe, de ne pas en faire un usage commercial, et de redistribuer sous la même licence.
- Les créateurs de contenu (YouTube, Twitch) peuvent utiliser ce patch et monétiser leurs vidéos normalement.

**Web Patcher** (`p2is_patcher`) - licence **[GPL-2.0](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html)**, imposée par l'intégration du code source de DeltaPatcher.

### Outils tiers utilisés

| Outil | Rôle | Licence |
|:---|:---|:---|
| **p2is_cpk_tool.py** | Extraction et reconstruction CPK (remplace CriFsLib) | Interne CC BY-NC-SA 4.0 |
| **NOTRE OUTIL** | Déchiffrement EBOOT, outil interne | Interne CC BY-NC-SA 4.0 |
| **pycdlib** (clalancette) | Lecture ISO 9660, importée dynamiquement | LGPL-2.1 |
| **DeltaPatcher** (marco-calautti) | Moteur de patch binaire compilé dans p2is_patcher | GPL-2.0 |
| **ATRACTool-Reloaded** (XyLe-GBP) | Conversion audio AT3, appelé en externe | Voir dépôt |

<br/>

---

## Documentation

| Fichier | Contenu |
|:---|:---|
| [DEVELOPER.md](./DEVELOPER.md) | Architecture technique complète, reverse-engineering du moteur Atlus, formats de fichiers, opcodes, algorithmes |
| [CONTRIBUTING.md](./CONTRIBUTING.md) | Guide de contribution, tableau d'avancement détaillé, règles de traduction |
| [Dictionnaire.md](./Dictionnaire.md) | Glossaire officiel de traduction - référence absolue |
| [SUIVI.md](./SUIVI.md) | Historique des versions et notes de patch |
| [CREDITS.md](./CREDITS.md) | Équipe principale et contributeurs |

Besoin d'aide ? Consultez la **[FAQ officielle](https://personalegrimoireducoeur.fr/faq.html)** ou rejoignez le **[Discord](https://discord.gg/rd4ckSWHNm)**.

<div align="center">
  <a href="https://www.star-history.com/?repos=chenetulipe%2FP2-FR-IS-PSP&type=date&legend=top-left">
    <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=chenetulipe/P2-FR-IS-PSP&type=date&legend=top-left&sealed_token=LFm90kimgTV0pKr7wph4I01fXMDcl0pp1R6gKZQj-A7IbzSxbcuQ3Te4pkPherfmIEivpEoqHEUGj9nyRkBIcEEDu5ejv9MLjA1aY8v8ynFglkEs_gTGdQ" width="800" />
  </a>
</div>

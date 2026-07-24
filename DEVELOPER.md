<div align="center">
  
# Guide Développeur & Base de Connaissances (P2IS Tool)
  
**Persona 2: Innocent Sin FR (PSP) - ULES01557**

<br/>

<img src="https://img.shields.io/badge/Statut-Documentation_Technique-0366d6?style=for-the-badge" alt="Statut" />
<img src="https://img.shields.io/badge/Reverse_Engineering-Atlus_%2F_CRI-d73a49?style=for-the-badge" alt="Reverse Engineering" />

</div>

<br/>

> [!NOTE]
> Bienvenue dans la documentation technique exhaustive du projet P2-FR-IS-PSP. Ce document centralise toutes les connaissances accumulées lors du reverse-engineering du jeu. Il est destiné aux développeurs, programmeurs et romhackers souhaitant comprendre ou modifier l'outil de compilation maison (`p2is_tool`), les spécificités du moteur d'Atlus et le format des archives CRI Middleware.

<br/>

---

## Sommaire
1. [Architecture Globale et Stack Technique](#architecture-globale-et-stack-technique)
2. [Dépendances, Outils Tiers et Licences](#dépendances-outils-tiers-et-licences)
3. [Spécificités du Moteur Atlus et du Bytecode](#spécificités-du-moteur-atlus-et-du-bytecode)
4. [Tableau Détaillé des Opcodes](#tableau-détaillé-des-opcodes)
5. [Anomalies Découvertes et Résolutions Techniques](#anomalies-découvertes-et-résolutions-techniques)
6. [Algorithme du Delta (Gestion Mémoire)](#algorithme-du-delta-gestion-mémoire)
7. [Structure du Code Source](#structure-du-code-source)
8. [Le Patcher Web (WebAssembly)](#le-patcher-web-webassembly)

<br/>

---

## Architecture Globale et Stack Technique

Le processus de romhacking a été intégralement restructuré en une application web locale, performante et asynchrone (V2).

<div align="left">
  <img src="https://img.shields.io/badge/Backend-FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/Langage-Python-3670A0?style=flat-square&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Frontend-React-20232A?style=flat-square&logo=react&logoColor=61DAFB" />
</div>

### Le Pipeline de Compilation
Le traitement automatisé de l'ISO s'articule autour de 4 grandes phases, orchestrées par le Backend Python :

1. **Extraction :** Isolement du fichier `P2PT_ALL.cpk` depuis l'ISO. Appel à l'outil tiers *CriFsLib* pour dépaqueter l'archive. Décompression LZSS (`CRILAYLA`) des fichiers vitaux comme `event.bin`, puis découpage séquentiel des 399 scripts d'histoire.
2. **Décodage (Parsing) :** Analyse du bytecode Atlus, séparation des opcodes de contrôle (convertis en balises `[TAG]`) du texte pur. Génération de fichiers `.json` destinés aux traducteurs.
3. **Encodage (Injection) :** Lecture du JSON traduit. Remappage des accents français (via la table `ACCENT_MAP`). **Recalcul dynamique des tables de pointeurs absolus** pour s'adapter aux variations de taille des dialogues français.
4. **Rebuild (Compilation ISO) :** Recompression LZSS des nouveaux scripts. Injection binaire dans l'archive CPK, puis **Injection LBA RAW** dans l'image `.iso` 9660.

> [!TIP]
> **Live-Logging React :** L'interface utilisateur Web communique de manière asynchrone avec le backend Python via FastAPI. Les sorties consoles (logs) du serveur sont retransmises en temps réel vers le Front-End, évitant de bloquer l'UI durant les lourdes opérations de reconstruction (qui manipulent des fichiers de plus d'1 Go).

<br/>

---

## Dépendances, Outils Tiers et Licences

Le projet repose sur plusieurs dépendances fondamentales. L'intégration de ces outils respecte leurs licences respectives (détails complets disponibles sur nos mentions légales).

| Dépendance | Fonction dans le projet | Auteur / Licence |
|:---|:---|:---|
| **CriFsLib (.NET)** | Extraction et re-création de l'archive `P2PT_ALL.cpk`. Il s'agit du format propriétaire de CRI Middleware. Cet outil permet de manipuler l'archive sans la corrompre. | *Sewer56* (Licence MIT / Open-Source) |
| **pycdlib (Python)** | Modification de l'image ISO 9660. Utilisée pour extraire le CPK et localiser l'EBOOT.BIN via son Logical Block Address (LBA) pour une injection de bas niveau. | *clalancette* (Licence LGPL-2.1) |
| **DeltaPatcher (C++)** | Utilisé pour générer le patch `.xdelta` final qui sera distribué aux joueurs (calculant la différence binaire entre l'ISO EUR originale et notre ISO traduite). | *marco-calautti* (Licence GPL-2.0) |

<br/>

---

## Spécificités du Moteur Atlus et du Bytecode

Persona 2 sur PSP utilise un moteur de jeu complexe reposant sur une architecture mémoire rigide.

| Fichier Cible | Format du Texte | Contrainte Technique Majeure |
|:---|:---|:---|
| **`event.bin`** (Histoire) | Shift-JIS & Opcodes Hex | Table d'Offsets Absolus au début de chaque script. Le moindre décalage d'un seul octet lors de l'injection provoque un crash du jeu. Le script Python reconstruit entièrement cette table pour chaque dialogue traduit. |
| **`EBOOT.BIN`** (Système) | ENGBIN / Custom Font | Le fichier exécutable contient les menus système et les descriptions d'objets. La police du jeu a été modifiée par les localisateurs anglais, posant des problèmes uniques d'encodage (voir section *Anomalies Découvertes*). |
| **`F_BE.BNP`** (Combat) | Shift-JIS (Pointeurs) | L'ajout d'octets de padding (`0x00`) à la fin d'un texte provoque un *Invalid Memory Access* (Crash au lancement des combats). L'**Algorithme du Delta** (voir plus bas) est utilisé pour compacter l'espace binaire de manière purement séquentielle sans padding. |

<br/>

---

## Tableau Détaillé des Opcodes

Le moteur lit des opcodes de contrôle hexadécimaux spécifiques que notre outil de parsing convertit en balises textuelles (ex: `[NL]`) pour les protéger lors de la traduction humaine.

> [!CAUTION]
> **Architecture de Contrôle :** Ces balises ne doivent jamais être retirées d'une ligne de dialogue par un traducteur, au risque de briser le fonctionnement du script In-Game.

| Opcode (Hex) | Tag Python | Fonction In-Game détaillée |
|:---:|:---:|:---|
| `00 22` | `[START]` | Initialise une nouvelle chaîne de caractères dans le buffer de la console. |
| `11 07` | `[END]` | Termine la chaîne et purge le buffer d'affichage. Absolument critique à la fin des PNJ. |
| `11 01` | `[NL]` | Sauts de ligne (New Line). Indispensable pour ne pas déborder des fenêtres de dialogue (max 3 lignes). |
| `12 08` | `[CHOICE]` | Déclenche l'affichage d'un menu contextuel à choix multiples. L'offset de cet opcode est pointé ailleurs dans le script. |
| `14 31` | `[ANIM]` | Instruction d'animation ou de comportement de l'UI (clignement d'yeux, mouvement de sprite). |
| `02 11` | `[WAIT]` | Met le dialogue en pause en attendant l'input (croix) du joueur. |
| `11 12` / `11 13` | `[1112]` | Variables système appelant le Nom ou Prénom du héros défini par le joueur. |
| `12 05` | `[1205]` | Pause dramatique automatique du texte (généralement suivie de `[001E]`). |

<br/>

---

## Anomalies Découvertes et Résolutions Techniques

Durant le développement, l'équipe a fait face à plusieurs problématiques nécessitant du reverse-engineering poussé.

### 1. Le Mystère des Tildes (`~`) et de l'Espace Japonais (`0x8140`)
Lors du test de l'injection des textes systèmes dans l'`EBOOT.BIN`, l'ensemble des espaces apparaissaient sous forme de tildes (`Ajuster ~ la ~ difficulté`). 
* **L'explication :** Les développeurs de Ghostlight (traducteurs anglais originaux) n'ont **pas** utilisé l'encodage classique ASCII pour l'espace (`0x0020`). Ils ont physiquement écrasé ce caractère dans la police (font) VRAM du jeu, le remplaçant par un tilde. En échange, ils ont forcé l'utilisation de l'**espace pleine chasse japonais Shift-JIS** (`0x8140`).
* **La solution :** L'encodeur `eboot_parser.py` intercepte tous les types d'espaces générés par les traducteurs (espace normal `0x0020`, espaces insécables `\xA0` de DeepL, ou idéographiques `\u3000`) et force leur encodage binaire en `0x8140`. De plus, les retours à la ligne `\n` sont sécurisés et traduits obligatoirement en `0x000A`.

### 2. Le Crash TypeError de l'API avec les Points de suspension (`…`)
* **L'explication :** Le script d'encodage de l'EBOOT utilise la normalisation Unicode `unicodedata.normalize('NFKD')` pour nettoyer les accents non pris en charge. Cependant, le caractère "points de suspension" (`…`) se décomposait en trois points distincts (`.`, `.`, `.`). La boucle d'encodage binaire `ord(c)` qui s'attendait à un seul caractère recevait une chaîne de longueur 3 et faisait crasher brutalement tout le backend.
* **La solution :** La normalisation NFKD a été déplacée pour ne s'appliquer qu'à la chaîne globale, avant la boucle itérative par caractère, évitant ainsi la fragmentation. L'outil convertit d'ailleurs automatiquement le glyphe `…` en trois points standards `...` par mesure de sécurité binaire.

### 3. L'Injection RAW (LBA) de l'EBOOT.BIN
* **L'explication :** L'ISO 9660 de la PSP possède une *Table of Contents* stricte. Au départ, l'outil recompilait un fichier `EBOOT_MODIFIED.BIN` sans parvenir à le réinsérer proprement au sein de l'ISO originale, car les utilitaires de type *UMDGen* cassaient les pointeurs.
* **La solution :** L'outil Python `core/iso.py` exploite la librairie `pycdlib` pour identifier le LBA (Logical Block Address) physique de `/PSP_GAME/SYSDIR/EBOOT.BIN`. Le script ouvre alors l'ISO en mode octet pur (`'rb+'`), cherche ce secteur spécifique (LBA × 2048), écrase l'exécutable original avec la version traduite, et rajoute un padding de `0x00` jusqu'à atteindre la taille exacte d'origine pour ne pas corrompre le disque.

<br/>

---

## Algorithme du Delta (Gestion Mémoire)

Dans les fichiers de type `.BNP` (comme `F_BE.BNP` gérant le texte de combat), le moteur de jeu charge le texte de manière séquentielle, pointeur après pointeur, sans table d'offsets absolus de référence.

Si une traduction française est plus courte que l'originale anglaise, ajouter du padding (remplissage avec `00`) provoque un dépassement de mémoire (Invalid Memory Access) car le jeu tente d'exécuter le padding comme s'il s'agissait d'un opcode de combat.

**Solution employée (Le Delta) :**
Plutôt que de combler l'espace vide par des zéros, l'encodeur "tasse" (compacte) tous les blocs de dialogues les uns derrière les autres. La différence de taille (le *Delta*) est calculée et soustraite de tous les pointeurs dynamiques qui suivent dans la mémoire. À la toute fin du bloc global de données, le padding est injecté pour atteindre la taille de fichier originale, évitant ainsi au jeu de tomber dessus par erreur en plein combat.

<br/>

---

## Structure du Code Source

Le backend Python localisé dans `p2is_tool/src/` suit une séparation stricte des responsabilités :

* ✦ **`core/iso.py`** : Manipulation directe de l'ISO 9660, extraction raw LBA, injection de l'EBOOT et patch du CPK.
* ✦ **`core/text.py`** : Moteur de conversion String ↔ Shift-JIS Atlus et intégration de la table `ACCENT_MAP` (remappage des accents).
* ✦ **`core/compression.py`** : Logique bas niveau des algorithmes de décompression LZSS propriétaire `CRILAYLA`.
* ✦ **`parsers/`** : Scripts spécialisés dans l'heuristique de détection de texte (ex. `bin_parser.py`, `eboot_parser.py`).
* ✦ **`encoders/`** : Logique d'assemblage binaire, de reconstruction des tables de pointeurs (`event.bin`) et d'application de l'Algorithme du Delta.

<br/>

---

## Le Patcher Web (WebAssembly)

Afin de faciliter l'installation du patch FR par les joueurs sans nécessiter le téléchargement d'un logiciel tiers, un **Patcher Web** complet a été intégré au projet dans le dossier `p2is_patcher/`.

* ✦ **Moteur :** Basé sur *DeltaPatcher* compilé en WebAssembly (`xdelta3.wasm`).
* ✦ **Performance :** L'application tourne dans un Web Worker (`xdelta3.worker.js`) pour ne pas faire geler l'interface (React/HTML) du navigateur lors du calcul du patch.
* ✦ **Gestion Mémoire :** Pour gérer des ISO de plus de 1 Go dans le navigateur sans saturer la RAM (limite critique des navigateurs), le patcher utilise des *Streams* et un *Service Worker* (`sw.js` / `mitm.html`) permettant de télécharger le fichier de sortie bit par bit au fur et à mesure de sa création locale.

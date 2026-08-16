<div align="center">

# Documentation Technique â€” Persona 2: Innocent Sin FR

**Base de connaissances du reverse-engineering et des outils de romhacking**

<br/>

<img src="https://img.shields.io/badge/Version_PSP-ULES01557-103F91?style=for-the-badge&logo=playstation&logoColor=white" />
<img src="https://img.shields.io/badge/Moteur-Atlus_Custom-d73a49?style=for-the-badge" />
<img src="https://img.shields.io/badge/Format_Archive-CRI_CRILAYLA-654FF0?style=for-the-badge" />

</div>

<br/>

> [!NOTE]
> Ce document centralise tout ce qu'on a découvert en reverse-engineerant Persona 2: Innocent Sin PSP. C'est la référence technique du projet : formats de fichiers, opcodes, algorithmes de compression, problèmes rencontrés et comment on les a résolus. Si tu veux comprendre ou modifier les outils, commence ici.

<br/>

---

## Sommaire

1. [Architecture du Pipeline de Traduction](#architecture-du-pipeline-de-traduction)
2. [Structure de l'UMD et Formats de Fichiers](#structure-de-lumd-et-formats-de-fichiers)
3. [Le SystÃ¨me de Compression CRILAYLA](#le-systÃ¨me-de-compression-crilayla)
4. [Bytecode Atlus et Opcodes de ContrÃ´le](#bytecode-atlus-et-opcodes-de-contrÃ´le)
5. [SpÃ©cificitÃ©s par Fichier Cible](#spÃ©cificitÃ©s-par-fichier-cible)
6. [Anomalies DÃ©couvertes et RÃ©solutions](#anomalies-dÃ©couvertes-et-rÃ©solutions)
7. [L'Algorithme du Delta (F_BE.BNP)](#lalgorithme-du-delta-fbebnp)
8. [Le Patcher Web (WebAssembly)](#le-patcher-web-webassembly)
9. [L'Image Lab (GIM / CRILAYLA)](#limage-lab-gim--crilayla)
10. [DÃ©pendances et Licences](#dÃ©pendances-et-licences)

<br/>

---

## Architecture du Pipeline de Traduction

L'outil principal (`p2is_tool`) est une application web locale pilotÃ©e par Python. Le pipeline complet se dÃ©roule en quatre phases distinctes.

<div align="left">
  <img src="https://img.shields.io/badge/Backend-FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/Langage-Python-3670A0?style=flat-square&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Frontend-React-20232A?style=flat-square&logo=react&logoColor=61DAFB" />
</div>

### Phase 1 â€” Extraction (I/O LBA)

Le module `core/iso.py` utilise `pycdlib` pour analyser l'arborescence ISO 9660 et localiser les fichiers via leur *Logical Block Address* (LBA). L'archive `P2PT_ALL.cpk` (254 Mo, 136 fichiers) est dÃ©compressÃ©e par `p2is_cpk_tool.py`. Les sous-fichiers CRILAYLA (comme `event.bin`) sont ensuite dÃ©compressÃ©s et dÃ©coupÃ©s sÃ©quentiellement en scripts individuels.

### Phase 2 â€” DÃ©codage (Parsing)

Les parsers dans `src/parsers/` analysent le bytecode Atlus. Chaque mot de 2 octets (Little-Endian hexadÃ©cimal) est converti en balise textuelle lisible (ex: `[NL]`, `[E1]`, `[1208]`). Les valeurs inconnues sont capturÃ©es sous la forme `[U+XXXX]` pour garantir une rÃ©tention mÃ©moire Ã  100% lors du rebuild. Les scripts sont exportÃ©s au format `.json`.

### Phase 3 â€” Encodage (Injection)

Les encodeurs dans `src/encoders/` lisent les JSON traduits. Ils effectuent :
- Le remappage des accents franÃ§ais vers leur Ã©quivalent PSP
- La reconstruction dynamique des tables de pointeurs absolus
- L'alignement des pointeurs de menus Ã  choix multiples via injection de `[SP]`
- Le calcul du Delta pour les fichiers BNP sans table d'index globale

### Phase 4 â€” Rebuild (Compilation ISO)

Les scripts compressÃ©s en CRILAYLA sont injectÃ©s dans l'archive CPK modifiÃ©e. L'ISO finale est reconstruite par **injection LBA RAW** : le code se positionne exactement Ã  l'adresse LBA du fichier d'origine et Ã©crase physiquement les secteurs concernÃ©s, sans modifier la structure ISO 9660.

<br/>

---

## Structure de l'UMD et Formats de Fichiers

L'UMD de Persona 2 IS PSP utilise une architecture propriÃ©taire imbriquÃ©e. La connaissance exacte de chaque format est indispensable pour intervenir sans corrompre l'ISO.

### Formats SystÃ¨me Sony (PSP)

| Format | Fichier(s) | Contenu |
|:---|:---|:---|
| `.SFO` | `PARAM.SFO` | MÃ©tadonnÃ©es du jeu : ID (`ULES01557`), rÃ©gion, flags firmware |
| `.PMF` | `F0141.pmf` â€” `F0159.pmf` | 19 cinÃ©matiques (~300 Mo). Lues par le Media Engine matÃ©riel. `F0158.pmf` contient un double en-tÃªte BND Pack avec des sous-titres encodÃ©s en dur |
| `.GIM` | Divers | Images optimisÃ©es VRAM PSP avec swizzling Z-Curve. Contenues dans les mini-archives `.bin` |

### Formats PropriÃ©taires CRI et Atlus

| Format | Description |
|:---|:---|
| `.CPK` | Archive CRI File System. IndexÃ©e par une TOC stricte, contenu compressÃ© CRILAYLA. Fichier principal : `P2PT_ALL.cpk` (254 Mo, 136 fichiers) |
| `.BIN` (majuscule) | Flux binaires purs. Exemple : `SE_DVL.BIN` (66 Mo), banque de bruitages de Personas |
| `.bin` (minuscule) | Mini-archives Atlus avec TOC interne. Exemple : `ch_menu.bin` contient **43 images GIM**. Fichier le plus petit du jeu : `namedic_dat.bin` (22 octets). Exception : `event.bin` (37 Mo) contient tous les scripts de l'histoire |
| `.BNP` | Bind Pack Atlus. DonnÃ©es organisÃ©es sÃ©quentiellement, sans table d'offsets globale. Exemples : `F_BE.BNP` (combats), `MMAP*.BNP` (dialogues PNJ carte), `TM_EVE.BNP` (cinÃ©matiques in-game), `EVTUNIT.BNP` (modÃ¨les 3D, ~7.5 Mo) |

### Fichiers ClÃ©s du CPK

```
P2PT_ALL.cpk
â”œâ”€â”€ event.bin        â€” Scripts d'histoire (37 Mo, 399 fichiers)
â”œâ”€â”€ F_BE.BNP         â€” Textes de combat et menus d'action
â”œâ”€â”€ MMAP01-06.BNP    â€” Dialogues PNJ sur les 6 cartes du jeu
â”œâ”€â”€ TM_EVE.BNP       â€” CinÃ©matiques scriptÃ©es in-game
â”œâ”€â”€ CD_SHOP.BNP      â€” Boutique de CD (musiques)
â”œâ”€â”€ ch_menu.bin      â€” 43 images GIM de l'interface (menus, HUD)
â”œâ”€â”€ syscg.bin        â€” Images compressÃ©es systÃ¨me (Ã©crans de chargement, etc.)
â”œâ”€â”€ SE_DVL.BIN       â€” Banque audio Personas (66 Mo)
â””â”€â”€ EBOOT.BIN        â€” ExÃ©cutable principal (menus systÃ¨me, textes ENGBIN)
```

<br/>

---

## Le SystÃ¨me de Compression CRILAYLA

CRILAYLA est l'algorithme de compression propriÃ©taire de CRI Middleware, utilisÃ© pour les sous-fichiers dans les archives CPK. Sa maÃ®trise est critique pour la rÃ©injection d'images et de scripts.

### Format du Flux CompressÃ©

Le flux CRILAYLA se lit **Ã  rebours** (de la fin vers le dÃ©but). C'est un algorithme LZ77-like :

- **En-tÃªte (8 octets)** : Signature `CRILAYLA`, taille non-compressÃ©e, taille compressÃ©e
- **Flux de bits** : SÃ©quence de blocs encodÃ©s en sens inverse
- **Bloc littÃ©ral** : `0` + 8 bits de donnÃ©es brutes
- **Bloc rÃ©fÃ©rence** : `1` + distance (offset dans le dictionnaire) + longueur de la copie

### Contrainte de Taille dans l'ISO

La TOC du CPK stocke les offsets LBA de chaque fichier. **La taille compressÃ©e d'un fichier ne peut pas dÃ©passer sa taille d'origine**, sinon elle dÃ©borde sur le fichier suivant et corrompt l'ISO. Il n'est pas possible d'ajouter de l'espace : tout ce qui dÃ©passe la taille allouÃ©e est interdit.

### StratÃ©gie de Compression pour l'Image Lab

Pour `syscg.bin` (Ã©crans de chargement), la contrainte est particuliÃ¨rement sÃ©vÃ¨re : la taille compressÃ©e maximale est de **57 320 octets** pour un contenu dÃ©compressÃ© de **321 712 octets**.

La stratÃ©gie adoptÃ©e :
1. Injection de la nouvelle image GIM Ã  l'offset `0x760` (slot de l'Ã©cran de chargement)
2. Mise Ã  zÃ©ro d'une image de tutoriel inutilisÃ©e (offset `0x31130`) pour rÃ©duire l'entropie du flux
3. Compression CRILAYLA greedy en Python pur (rÃ©sultat : ~52 000 octets)
4. Padding de zÃ©ros jusqu'Ã  57 320 octets pour respecter la taille allouÃ©e

Les images Ã  ne jamais toucher dans `syscg.bin` :
- `0x42f40` : ChronomÃ¨tre (Time Limit)
- `0x43250` : Compteur de piÃ¨ces (Total Coins)

<br/>

---

## Bytecode Atlus et Opcodes de ContrÃ´le

Le moteur Atlus encode ses scripts en bytecode Little-Endian 16 bits. L'architecture mÃ©moire de la PSP est rigide : un octet mal placÃ© provoque une exception `Invalid Memory Access` et crashe le jeu.

Le dÃ©codeur convertit chaque opcode en balise textuelle. **Ces balises ne doivent jamais Ãªtre supprimÃ©es du texte traduit.** Toute valeur inconnue est capturÃ©e sous la forme `[U+XXXX]`.

### Table des Opcodes Reconnus

| Opcode (Hex) | Balise | CatÃ©gorie | Description |
|:---:|:---:|:---|:---|
| `11 20` | `[SP]` | Formatage | Espace pleine chasse. UtilisÃ© aussi comme padding d'alignement |
| `11 01` | `[NL]` | Formatage | Saut de ligne. Son absence en fin de rÃ©plique produit le glitch `â–½â–½â–½` |
| `11 06` | `[E1]` | Terminateur | Bloc de fin de dialogue, partie 1/4 |
| `11 02` | `[E2]` | Terminateur | Bloc de fin de dialogue, partie 2/4 |
| `11 03` | `[E3]` | Terminateur | Bloc de fin de dialogue, partie 3/4 |
| `14 31` | `[E4]` | Terminateur | Fin de dialogue / marqueur d'animation UI dans `F_BE` |
| `11 09` | `[1109]` | Terminateur | Variante de `[E1]` pour le chaÃ®nage continu (`1109 E2 E3 E4`) |
| `12 08` | `[1208]` | Choix | DÃ©clencheur d'un menu de choix. Toujours suivi de `[0002]` |
| `00 02` | `[0002]` | Choix | Activation de la fenÃªtre de choix |
| `00 14` | `[0014]` | Choix | SÃ©parateur de fin de chaÃ®ne pour chaque option |
| `14 32` | `[1432]` | MÃ©moire / UI | Positionnement du curseur dans les menus |
| `00 10` | `[0010]` | MÃ©moire / UI | Variable d'espacement interne des menus |
| `00 00` | `[NULL]` | Structurel | Null byte de fin de variable ou dÃ©calage de pointeur |
| `12 05` | `[1205]` | CinÃ©matique | Pause automatique du texte (gÃ©nÃ©ralement suivie de `[001E]`) |
| `00 1E` | `[001E]` | CinÃ©matique | DurÃ©e de la pause (30 frames environ) |
| `11 07` | `[1107]` | Buffer | Nettoyage du buffer d'affichage, clÃ´ture une fenÃªtre |
| `11 08` | `[1108]` | Visuel | Gestion de la fenÃªtre lors de l'apparition d'un Bust-up |
| `11 12` | `[1112]` | Variable | Injection du nom de famille du hÃ©ros (dÃ©fini par le joueur) |
| `11 13` | `[1113]` | Variable | Injection du prÃ©nom du hÃ©ros (dÃ©fini par le joueur) |
| `12 0Câ€“0F` | `[120C]`... | Visuel | Effets de couleur ou de style sur la police |
| `12 10` | `[1210]` | Visuel | Restauration de la couleur de police par dÃ©faut |
| `12 1E` | `[121E]` | Interaction | ForÃ§age d'une attente de pression de touche |
| `XXXX` | `[U+XXXX]` | Secours | Opcode inconnu â€” stockÃ© pour garantir l'intÃ©gritÃ© au rebuild |

<br/>

---

## SpÃ©cificitÃ©s par Fichier Cible

### event.bin â€” Scripts de l'Histoire

- **Format** : Bytecode Atlus avec table d'offsets absolus en dÃ©but de chaque script
- **Contrainte majeure** : La table d'offsets est entiÃ¨rement recalculÃ©e et reconstruite par l'encodeur Ã  chaque compilation
- **Encodage texte** : Shift-JIS remaniÃ©. L'espace ASCII (`0x0020`) a Ã©tÃ© physiquement remplacÃ© par un tilde dans la police VRAM par Ghostlight. L'encodeur force tous les espaces vers l'espace pleine chasse japonais Shift-JIS (`0x8140`)

### EBOOT.BIN â€” Menus SystÃ¨me

- **Format** : ENGBIN custom. Contient ~6 574 entrÃ©es de texte pour l'interface, les noms de personnages, les descriptions d'objets et de compÃ©tences
- **Contrainte police** : Les dÃ©veloppeurs de Ghostlight ont altÃ©rÃ© la police originale. Le parser (`eboot_parser.py`) effectue un mappage hexadÃ©cimal vers `0x00E0`, `0x0101` et `0x00CF` pour aligner les lettres latines franÃ§aises avec cette police modifiÃ©e
- **Organisation** : Le fichier est dÃ©coupÃ© en 7 parties (Part 1â€“7, ~1000 entrÃ©es chacune) dans le dossier `EBOOT_decoupe/` pour Ã©viter les limitations GitHub

### F_BE.BNP â€” Combats et Interface

- **Format** : Shift-JIS sÃ©quentiel, sans table d'index globale
- **Contrainte** : L'ajout de padding classique entre les entrÃ©es provoque un crash (le moteur tente d'exÃ©cuter les octets nuls `0x00` comme du code)
- **Solution** : L'Algorithme du Delta â€” voir section dÃ©diÃ©e

### MMAP01â€“06.BNP â€” Dialogues PNJ

- **Format** : BNP sÃ©quentiel avec index interne par secteur de carte
- **Contrainte** : La longueur en octets de chaque entrÃ©e doit rester identique Ã  l'original, sinon les pointeurs de la carte se dÃ©calent

### syscg.bin et ch_menu.bin â€” Images

- **Format** : Mini-archives Atlus contenant des images GIM compressÃ©es CRILAYLA
- **Contrainte** : Taille compressÃ©e maximale imposÃ©e par la TOC du CPK. Voir section Image Lab

<br/>

---

## Anomalies DÃ©couvertes et RÃ©solutions

### 1. Le MystÃ¨re des Tildes et de l'Espace Japonais

**SymptÃ´me** : L'espace ASCII (`0x0020`) affiche un tilde au lieu d'un espace vide en jeu.

**Cause** : Ghostlight a physiquement Ã©crasÃ© le glyphe d'espace dans la police VRAM, le remplaÃ§ant par un tilde, et a forcÃ© l'utilisation de l'espace pleine chasse japonais Shift-JIS (`0x8140`) Ã  la place.

**Solution** : L'encodeur intercepte tous les types d'espaces (ASCII, insÃ©cable DeepL, idÃ©ographique japonais) et les force vers `0x8140` avant l'Ã©criture binaire.

### 2. La Corruption des Menus Ã  Choix Multiples

**SymptÃ´me** : Les options de choix s'affichent dans le dÃ©sordre ou se superposent aprÃ¨s traduction.

**Cause** : Le moteur stocke des pointeurs absolus vers chaque option de choix. Si la question traduite est plus courte en octets que l'originale, les pointeurs se dÃ©calent et le moteur pointe vers les mauvaises adresses mÃ©moire.

**Solution** : L'algorithme `_align_menu_text` calcule la diffÃ©rence de longueur binaire entre la version franÃ§aise et l'originale japonaise, puis injecte des `[SP]` invisibles avant le marqueur `[1208]` pour restaurer l'alignement mÃ©moire exact.

### 3. Le Glitch `â–½â–½â–½` (Fin de Dialogue Manquante)

**SymptÃ´me** : Le jeu affiche des caractÃ¨res parasites `â–½â–½â–½` Ã  la fin de certaines boÃ®tes de dialogue ou saute des rÃ©pliques entiÃ¨res.

**Cause** : Le bloc de terminaison `[E1][E2][E3][E4]` doit apparaÃ®tre Ã  une position prÃ©cise aprÃ¨s la derniÃ¨re ligne. Si le texte franÃ§ais dÃ©borde sur la position attendue des terminateurs, le moteur ne les trouve pas.

**Solution** : Limitation stricte Ã  3 lignes par boÃ®te de dialogue, repositionnement systÃ©matique des balises de terminaison en fin de chaque bloc `[E3]`.

### 4. La Corruption des Pointeurs dans F_BE.BNP

**SymptÃ´me** : Crash `Invalid Memory Access` sur l'Ã©cran de combat aprÃ¨s traduction.

**Cause** : Le moteur lit le fichier BNP sÃ©quentiellement, sans table d'offsets. Si du padding nul (`0x00`) est insÃ©rÃ© entre les entrÃ©es pour combler les diffÃ©rences de taille, ces octets sont interprÃ©tÃ©s comme des opcodes et font crasher le CPU de la PSP.

**Solution** : Voir l'Algorithme du Delta ci-dessous.

<br/>

---

## L'Algorithme du Delta (F_BE.BNP)

Ce problÃ¨me est spÃ©cifique aux fichiers BNP sans table d'offsets globale (`F_BE.BNP`, certains `MMAP*.BNP`).

**Principe** :

L'encodeur `fbe_parser.py` compacte tous les blocs de dialogues franÃ§ais les uns derriÃ¨re les autres, sans aucun espace mort entre eux. La diffÃ©rence de taille accumulÃ©e entre le texte original et le texte franÃ§ais (le *Delta*) est conservÃ©e en mÃ©moire tout au long de l'encodage. Une fois le dernier bloc Ã©crit, la somme totale du Delta est injectÃ©e en un seul bloc de padding Ã  la toute fin du fichier.

**Pourquoi Ã§a fonctionne** :

Le moteur lit sÃ©quentiellement du dÃ©but vers la fin. Il ne rencontre jamais de padding avant une entrÃ©e de dialogue rÃ©elle, donc il ne tente jamais d'exÃ©cuter des octets nuls comme du code. La taille totale du fichier reste identique Ã  l'original, ce qui maintient l'intÃ©gritÃ© de la TOC du CPK sans altÃ©rer la RAM de la console.

**Condition critique** : Le texte franÃ§ais total doit Ãªtre Ã©gal ou infÃ©rieur en octets au texte original. Si une entrÃ©e individuelle est plus longue, elle est tronquÃ©e automatiquement avec un avertissement.

<br/>

---

## Le Patcher Web (WebAssembly)

Le patcher web (`p2is_patcher`) permet aux joueurs d'appliquer le patch `.xdelta` directement dans leur navigateur, sans installer de logiciel.

**Moteur WASM** : La librairie C++ *DeltaPatcher* (xdelta3) est compilÃ©e en WebAssembly. Elle ne stocke que la diffÃ©rence binaire brute entre l'ISO anglaise originale et l'ISO franÃ§aise, ce qui rÃ©duit drastiquement la taille du fichier de patch.

**Worker asynchrone** : L'application s'exÃ©cute dans un Web Worker (`xdelta3.worker.js`) pour ne pas bloquer l'interface du navigateur pendant le patch.

**Gestion de la mÃ©moire (Streams + Service Worker)** : Un onglet de navigateur est limitÃ© Ã  environ 2 Go de RAM. Les ISO PSP dÃ©passent souvent 1 Go. Pour rÃ©soudre ce problÃ¨me, le patcher utilise l'API Streams avec un Service Worker (`mitm.html` + `sw.js`). Le Service Worker agit comme un intermÃ©diaire et Ã©crit le fichier gÃ©nÃ©rÃ© sur le disque dur local en streaming, bit par bit, au fur et Ã  mesure de sa crÃ©ation en mÃ©moire. Il n'est donc jamais nÃ©cessaire de charger l'ISO complÃ¨te en RAM.

<br/>

---

## L'Image Lab (GIM / CRILAYLA)

Le laboratoire d'images (`p2is_image_lab`) est un outil web local (FastAPI + React) permettant d'extraire, Ã©diter et rÃ©injecter des images GIM dans les archives CPK.

### Format GIM (Graphic Image Map)

Le format GIM est propriÃ©taire Sony. Les pixels sont encodÃ©s en Z-Curve (*swizzling* matÃ©riel), ce qui optimise les accÃ¨s VRAM sur la PSP. Pour rÃ©injecter une image PNG externe :

1. Redimensionnement Ã  la rÃ©solution cible (ex: 480Ã—272 pour un Ã©cran de chargement)
2. Conversion en palette 8 bits (256 couleurs) ou en RGBA16 selon le slot cible
3. Encodage de l'en-tÃªte GIM avec les mÃ©tadonnÃ©es de format
4. Application du swizzling Z-Curve sur les donnÃ©es pixel

### Compresseur CRILAYLA (Python)

Le compresseur implÃ©mentÃ© dans `core/image_format.py` utilise une approche greedy : pour chaque position dans les donnÃ©es non-compressÃ©es, il cherche la meilleure rÃ©fÃ©rence possible dans le dictionnaire de 8 Ko. Les rÃ©sultats typiques :

- `syscg.bin` original : 57 320 octets compressÃ©s / 321 712 octets non-compressÃ©s
- AprÃ¨s injection et recompression : ~52 000 octets, compatible avec la contrainte de taille

### Isolation des Slots d'Images dans syscg.bin

| Offset | Contenu | Modifiable |
|:---:|:---|:---:|
| `0x760` | Ã‰cran de chargement principal | Oui |
| `0x31130` | Image de tutoriel (inutilisÃ©e) | Oui (mise Ã  zÃ©ro autorisÃ©e) |
| `0x42f40` | ChronomÃ¨tre (Time Limit) | Non |
| `0x43250` | Compteur de piÃ¨ces (Total Coins) | Non |

<br/>

---

## DÃ©pendances et Licences

| Composant | RÃ´le | Auteur | Licence |
|:---|:---|:---|:---|
| **FastAPI** | Backend API REST de l'outil principal | SebastiÃ¡n RamÃ­rez | MIT |
| **React** | Interface web de l'outil principal | Meta | MIT |
| **pycdlib** | Lecture et Ã©criture ISO 9660 | clalancette | LGPL-2.1 |
| **Pillow** | Manipulation d'images (PNG â†’ GIM) | Pillow contributors | HPND |
| **p2is_cpk_tool.py** | Extraction et reconstruction CPK | chenetulipe | Interne |
| **pspdecrypt** | DÃ©chiffrement EBOOT (DRM KIRK) | John-K | Open-Source |
| **DeltaPatcher** | Moteur de patch binaire xdelta3 | marco-calautti | GPL-2.0 |
| **ATRACTool-Reloaded** | Conversion audio AT3 | XyLe-GBP | Voir dÃ©pÃ´t |
| **customtkinter** | Interface graphique Python (scripts utilitaires) | Tom Schimansky | MIT |


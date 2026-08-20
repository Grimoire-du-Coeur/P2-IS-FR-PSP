<div align="center">

# Documentation Technique - Persona 2: Innocent Sin FR

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
3. [Le Système de Compression CRILAYLA](#le-système-de-compression-crilayla)
4. [Bytecode Atlus et Opcodes de Contrôle](#bytecode-atlus-et-opcodes-de-contrôle)
5. [Spécificités par Fichier Cible](#spécificités-par-fichier-cible)
6. [Anomalies Découvertes et Résolutions](#anomalies-découvertes-et-résolutions)
7. [L'Algorithme du Delta (F_BE.BNP)](#lalgorithme-du-delta-fbebnp)
8. [Le Patcher Web (WebAssembly)](#le-patcher-web-webassembly)
9. [L'Image Lab (GIM / CRILAYLA)](#limage-lab-gim--crilayla)
10. [Dépendances et Licences](#dépendances-et-licences)

<br/>

---

## Architecture du Pipeline de Traduction

L'outil principal (`p2is_tool`) est une application web locale pilotée par Python. Le pipeline complet se déroule en quatre phases distinctes.

<div align="left">
  <img src="https://img.shields.io/badge/Backend-FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/Langage-Python-3670A0?style=flat-square&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Frontend-React-20232A?style=flat-square&logo=react&logoColor=61DAFB" />
</div>

### Phase 1 - Extraction (I/O LBA)

Le module `core/iso.py` utilise `pycdlib` pour analyser l'arborescence ISO 9660 et localiser les fichiers via leur *Logical Block Address* (LBA). L'archive `P2PT_ALL.cpk` (254 Mo, 136 fichiers) est décompressée par `p2is_cpk_tool.py`. Les sous-fichiers CRILAYLA (comme `event.bin`) sont ensuite décompressés et découpés séquentiellement en scripts individuels.

### Phase 2 - Décodage (Parsing)

Les parsers dans `src/parsers/` analysent le bytecode Atlus. Chaque mot de 2 octets (Little-Endian hexadécimal) est converti en balise textuelle lisible (ex: `[NL]`, `[E1]`, `[1208]`). Les valeurs inconnues sont capturées sous la forme `[U+XXXX]` pour garantir une rétention mémoire à 100% lors du rebuild. Les scripts sont exportés au format `.json`.

### Phase 3 - Encodage (Injection)

Les encodeurs dans `src/encoders/` lisent les JSON traduits. Ils effectuent :
- Le remappage des accents français vers leur équivalent PSP
- La reconstruction dynamique des tables de pointeurs absolus
- L'alignement des pointeurs de menus à choix multiples via injection de `[SP]`
- Le calcul du Delta pour les fichiers BNP sans table d'index globale

### Phase 4 - Rebuild (Compilation ISO)

Les scripts compressés en CRILAYLA sont injectés dans l'archive CPK modifiée. L'ISO finale est reconstruite par **injection LBA RAW** : le code se positionne exactement à l'adresse LBA du fichier d'origine et écrase physiquement les secteurs concernés, sans modifier la structure ISO 9660.

<br/>

---

## Structure de l'UMD et Formats de Fichiers

L'UMD de Persona 2 IS PSP utilise une architecture propriétaire imbriquée. La connaissance exacte de chaque format est indispensable pour intervenir sans corrompre l'ISO.

### Formats Système Sony (PSP)

| Format | Fichier(s) | Contenu |
|:---|:---|:---|
| `.SFO` | `PARAM.SFO` | Métadonnées du jeu : ID (`ULES01557`), région, flags firmware |
| `.PMF` | `F0141.pmf` - `F0159.pmf` | 19 cinématiques (~300 Mo). Lues par le Media Engine matériel. `F0158.pmf` contient un double en-tête BND Pack avec des sous-titres encodés en dur |
| `.GIM` | Divers | Images optimisées VRAM PSP avec swizzling Z-Curve. Contenues dans les mini-archives `.bin` |

### Formats Propriétaires CRI et Atlus

| Format | Description |
|:---|:---|
| `.CPK` | Archive CRI File System. Indexée par une TOC stricte, contenu compressé CRILAYLA. Fichier principal : `P2PT_ALL.cpk` (254 Mo, 136 fichiers) |
| `.BIN` (majuscule) | Flux binaires purs. Exemple : `SE_DVL.BIN` (66 Mo), banque de bruitages de Personas |
| `.bin` (minuscule) | Mini-archives Atlus avec TOC interne. Exemple : `ch_menu.bin` contient **43 images GIM**. Fichier le plus petit du jeu : `namedic_dat.bin` (22 octets). Exception : `event.bin` (37 Mo) contient tous les scripts de l'histoire |
| `.BNP` | Bind Pack Atlus. Données organisées séquentiellement, sans table d'offsets globale. Exemples : `F_BE.BNP` (combats), `MMAP*.BNP` (dialogues PNJ carte), `TM_EVE.BNP` (cinématiques in-game), `EVTUNIT.BNP` (modèles 3D, ~7.5 Mo) |

### Fichiers Clés du CPK

```
P2PT_ALL.cpk
├── event.bin        - Scripts d'histoire (37 Mo, 399 fichiers)
├── F_BE.BNP         - Textes de combat et menus d'action
├── MMAP01-06.BNP    - Dialogues PNJ sur les 6 cartes du jeu
├── TM_EVE.BNP       - Cinématiques scriptées in-game
├── CD_SHOP.BNP      - Boutique de CD (musiques)
├── ch_menu.bin      - 43 images GIM de l'interface (menus, HUD)
├── syscg.bin        - Images compressées système (écrans de chargement, etc.)
├── SE_DVL.BIN       - Banque audio Personas (66 Mo)
```

<br/>

---

## Le Système de Compression CRILAYLA

CRILAYLA est l'algorithme de compression propriétaire de CRI Middleware, utilisé pour les sous-fichiers dans les archives CPK. Sa maîtrise est critique pour la réinjection d'images et de scripts.

### Format du Flux Compressé

Le flux CRILAYLA se lit **à rebours** (de la fin vers le début). C'est un algorithme LZ77-like :

- **En-tête (8 octets)** : Signature `CRILAYLA`, taille non-compressée, taille compressée
- **Flux de bits** : Séquence de blocs encodés en sens inverse
- **Bloc littéral** : `0` + 8 bits de données brutes
- **Bloc référence** : `1` + distance (offset dans le dictionnaire) + longueur de la copie

### Contrainte de Taille dans l'ISO

La TOC du CPK stocke les offsets LBA de chaque fichier. **La taille compressée d'un fichier ne peut pas dépasser sa taille d'origine**, sinon elle déborde sur le fichier suivant et corrompt l'ISO. Il n'est pas possible d'ajouter de l'espace : tout ce qui dépasse la taille allouée est interdit.

---

## Bytecode Atlus et Opcodes de Contrôle

Le moteur Atlus encode ses scripts en bytecode Little-Endian 16 bits. L'architecture mémoire de la PSP est rigide : un octet mal placé provoque une exception `Invalid Memory Access` et crashe le jeu.

Le décodeur convertit chaque opcode en balise textuelle. **Ces balises ne doivent jamais être supprimées du texte traduit.** Toute valeur inconnue est capturée sous la forme `[U+XXXX]`.

### Table des Opcodes Reconnus

| Opcode (Hex) | Balise | Catégorie | Description |
|:---:|:---:|:---|:---|
| `11 20` | `[SP]` | Formatage | Espace pleine chasse. Utilisé aussi comme padding d'alignement |
| `11 01` | `[NL]` | Formatage | Saut de ligne. Son absence en fin de réplique produit le glitch `▽▽▽` |
| `11 06` | `[E1]` | Terminateur | Bloc de fin de dialogue, partie 1/4 |
| `11 02` | `[E2]` | Terminateur | Bloc de fin de dialogue, partie 2/4 |
| `11 03` | `[E3]` | Terminateur | Bloc de fin de dialogue, partie 3/4 |
| `14 31` | `[E4]` | Terminateur | Fin de dialogue / marqueur d'animation UI dans `F_BE` |
| `11 09` | `[1109]` | Terminateur | Variante de `[E1]` pour le chaînage continu (`1109 E2 E3 E4`) |
| `12 08` | `[1208]` | Choix | Déclencheur d'un menu de choix. Toujours suivi de `[0002]` |
| `00 02` | `[0002]` | Choix | Activation de la fenêtre de choix |
| `00 14` | `[0014]` | Choix | Séparateur de fin de chaîne pour chaque option |
| `14 32` | `[1432]` | Mémoire / UI | Positionnement du curseur dans les menus |
| `00 10` | `[0010]` | Mémoire / UI | Variable d'espacement interne des menus |
| `00 00` | `[NULL]` | Structurel | Null byte de fin de variable ou décalage de pointeur |
| `12 05` | `[1205]` | Cinématique | Pause automatique du texte (généralement suivie de `[001E]`) |
| `00 1E` | `[001E]` | Cinématique | Durée de la pause (30 frames environ) |
| `11 07` | `[1107]` | Buffer | Nettoyage du buffer d'affichage, clôture une fenêtre |
| `11 08` | `[1108]` | Visuel | Gestion de la fenêtre lors de l'apparition d'un Bust-up |
| `11 12` | `[1112]` | Variable | Injection du nom de famille du héros (défini par le joueur) |
| `11 13` | `[1113]` | Variable | Injection du prénom du héros (défini par le joueur) |
| `12 0C–0F` | `[120C]`... | Visuel | Effets de couleur ou de style sur la police |
| `12 10` | `[1210]` | Visuel | Restauration de la couleur de police par défaut |
| `12 1E` | `[121E]` | Interaction | Forçage d'une attente de pression de touche |
| `XXXX` | `[U+XXXX]` | Secours | Opcode inconnu - stocké pour garantir l'intégrité au rebuild |

<br/>

---

## Spécificités par Fichier Cible

### event.bin - Scripts de l'Histoire

- **Format** : Bytecode Atlus avec table d'offsets absolus en début de chaque script
- **Contrainte majeure** : La table d'offsets est entièrement recalculée et reconstruite par l'encodeur à chaque compilation
- **Encodage texte** : Shift-JIS remanié. L'espace ASCII (`0x0020`) a été physiquement remplacé par un tilde dans la police VRAM par Ghostlight. L'encodeur force tous les espaces vers l'espace pleine chasse japonais Shift-JIS (`0x8140`)

### EBOOT.BIN - Menus Système

- **Format** : ENGBIN custom. Contient ~6 574 entrées de texte pour l'interface, les noms de personnages, les descriptions d'objets et de compétences
- **Contrainte police** : Les développeurs de Ghostlight ont altéré la police originale. Le parser (`eboot_parser.py`) effectue un mappage hexadécimal vers `0x00E0`, `0x0101` et `0x00CF` pour aligner les lettres latines françaises avec cette police modifiée
- **Organisation** : Le fichier est découpé en 7 parties (Part 1–7, ~1000 entrées chacune) dans le dossier `EBOOT_decoupe/` pour éviter les limitations GitHub

### F_BE.BNP - Combats et Interface

- **Format** : Shift-JIS séquentiel, sans table d'index globale
- **Contrainte** : L'ajout de padding classique entre les entrées provoque un crash (le moteur tente d'exécuter les octets nuls `0x00` comme du code)
- **Solution** : L'Algorithme du Delta - voir section dédiée

### MMAP01–06.BNP - Dialogues PNJ

- **Format** : BNP séquentiel avec index interne par secteur de carte
- **Contrainte** : La longueur en octets de chaque entrée doit rester identique à l'original, sinon les pointeurs de la carte se décalent

### syscg.bin et ch_menu.bin - Images

- **Format** : Mini-archives Atlus contenant des images GIM compressées CRILAYLA
- **Contrainte** : Taille compressée maximale imposée par la TOC du CPK. Voir section Image Lab

<br/>

---

## Anomalies Découvertes et Résolutions

### 1. Le Mystère des Tildes et de l'Espace Japonais

**Symptôme** : L'espace ASCII (`0x0020`) affiche un tilde au lieu d'un espace vide en jeu.

**Cause** : Ghostlight a physiquement écrasé le glyphe d'espace dans la police VRAM, le remplaçant par un tilde, et a forcé l'utilisation de l'espace pleine chasse japonais Shift-JIS (`0x8140`) à la place.

**Solution** : L'encodeur intercepte tous les types d'espaces (ASCII, insécable DeepL, idéographique japonais) et les force vers `0x8140` avant l'écriture binaire.

### 2. La Corruption des Menus à Choix Multiples

**Symptôme** : Les options de choix s'affichent dans le désordre ou se superposent après traduction.

**Cause** : Le moteur stocke des pointeurs absolus vers chaque option de choix. Si la question traduite est plus courte en octets que l'originale, les pointeurs se décalent et le moteur pointe vers les mauvaises adresses mémoire.

**Solution** : L'algorithme `_align_menu_text` calcule la différence de longueur binaire entre la version française et l'originale japonaise, puis injecte des `[SP]` invisibles avant le marqueur `[1208]` pour restaurer l'alignement mémoire exact.

### 3. Le Glitch `▽▽▽` (Fin de Dialogue Manquante)

**Symptôme** : Le jeu affiche des caractères parasites `▽▽▽` à la fin de certaines boîtes de dialogue ou saute des répliques entières.

**Cause** : Le bloc de terminaison `[E1][E2][E3][E4]` doit apparaître à une position précise après la dernière ligne. Si le texte français déborde sur la position attendue des terminateurs, le moteur ne les trouve pas.

**Solution** : Limitation stricte à 3 lignes par boîte de dialogue, repositionnement systématique des balises de terminaison en fin de chaque bloc `[E3]`.

### 4. La Corruption des Pointeurs dans F_BE.BNP

**Symptôme** : Crash `Invalid Memory Access` sur l'écran de combat après traduction.

**Cause** : Le moteur lit le fichier BNP séquentiellement, sans table d'offsets. Si du padding nul (`0x00`) est inséré entre les entrées pour combler les différences de taille, ces octets sont interprétés comme des opcodes et font crasher le CPU de la PSP.

**Solution** : Voir l'Algorithme du Delta ci-dessous.

<br/>

---

## L'Algorithme du Delta (F_BE.BNP)

Ce problème est spécifique aux fichiers BNP sans table d'offsets globale (`F_BE.BNP`, certains `MMAP*.BNP`).

**Principe** :

L'encodeur `fbe_parser.py` compacte tous les blocs de dialogues français les uns derrière les autres, sans aucun espace mort entre eux. La différence de taille accumulée entre le texte original et le texte français (le *Delta*) est conservée en mémoire tout au long de l'encodage. Une fois le dernier bloc écrit, la somme totale du Delta est injectée en un seul bloc de padding à la toute fin du fichier.

**Pourquoi ça fonctionne** :

Le moteur lit séquentiellement du début vers la fin. Il ne rencontre jamais de padding avant une entrée de dialogue réelle, donc il ne tente jamais d'exécuter des octets nuls comme du code. La taille totale du fichier reste identique à l'original, ce qui maintient l'intégrité de la TOC du CPK sans altérer la RAM de la console.

**Condition critique** : Le texte français total doit être égal ou inférieur en octets au texte original. Si une entrée individuelle est plus longue, elle est tronquée automatiquement avec un avertissement.

<br/>

---

## Le Patcher Web (WebAssembly)

Le patcher web (`p2is_patcher`) permet aux joueurs d'appliquer le patch `.xdelta` directement dans leur navigateur, sans installer de logiciel.

**Moteur WASM** : La librairie open-source xdelta3 est compilée en WebAssembly. Elle ne stocke que la différence binaire brute entre l'ISO anglaise originale et l'ISO française, ce qui réduit drastiquement la taille du fichier de patch.

**Worker asynchrone** : L'application s'exécute dans un Web Worker (`xdelta3.worker.js`) pour ne pas bloquer l'interface du navigateur pendant le patch.

**Gestion de la mémoire (Streams + Service Worker)** : Un onglet de navigateur est limité à environ 2 Go de RAM. Les ISO PSP dépassent souvent 1 Go. Pour résoudre ce problème, le patcher utilise l'API Streams avec un Service Worker (`mitm.html` + `sw.js`). Le Service Worker agit comme un intermédiaire et écrit le fichier généré sur le disque dur local en streaming, bit par bit, au fur et à mesure de sa création en mémoire. Il n'est donc jamais nécessaire de charger l'ISO complète en RAM.

<br/>

---

## L'Image Lab (GIM / CRILAYLA)

Le laboratoire d'images (`p2is_image_lab`) est un outil web local (FastAPI + React) permettant d'extraire, éditer et réinjecter des images GIM dans les archives CPK.

### Format GIM (Graphic Image Map)

Le format GIM est propriétaire Sony. Les pixels sont encodés en Z-Curve (*swizzling* matériel), ce qui optimise les accès VRAM sur la PSP. Pour réinjecter une image PNG externe :

1. Redimensionnement à la résolution cible (ex: 480×272 pour un écran de chargement)
2. Conversion en palette 8 bits (256 couleurs) ou en RGBA16 selon le slot cible
3. Encodage de l'en-tête GIM avec les métadonnées de format
4. Application du swizzling Z-Curve sur les données pixel

### Compresseur CRILAYLA (Python)

Le compresseur implémenté dans `core/image_format.py` utilise une approche greedy : pour chaque position dans les données non-compressées, il cherche la meilleure référence possible dans le dictionnaire de 8 Ko. Les résultats typiques :

- `syscg.bin` original : 57 320 octets compressés / 321 712 octets non-compressés
- Après injection et recompression : ~52 000 octets, compatible avec la contrainte de taille

<br/>

---

## Dépendances et Licences

| Composant | Rôle | Auteur | Licence |
|:---|:---|:---|:---|
| **FastAPI** | Backend API REST de l'outil principal | Sebastián Ramírez | MIT |
| **React** | Interface web de l'outil principal | Meta | MIT |
| **pycdlib** | Lecture et écriture ISO 9660 | clalancette | LGPL-2.1 |
| **Pillow** | Manipulation d'images (PNG → GIM) | Pillow contributors | HPND |
| **p2is_cpk_tool.py** | Extraction et reconstruction CPK | chenetulipe | Interne |
| **decrypt_eboot.py** | Déchiffrement EBOOT (DRM KIRK) | John-K | Open-Source |
| **ATRACTool-Reloaded** | Conversion audio AT3 | XyLe-GBP | Voir dépôt |
| **customtkinter** | Interface graphique Python (scripts utilitaires) | Tom Schimansky | MIT |

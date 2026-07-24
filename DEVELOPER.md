<div align="center">
  
# Guide Développeur & Base de Connaissances (P2IS Tool)
  
**Persona 2: Innocent Sin FR (PSP) - ULES01557**

<br/>

<img src="https://img.shields.io/badge/Statut-Documentation_Technique-0366d6?style=for-the-badge" alt="Statut" />
<img src="https://img.shields.io/badge/Reverse_Engineering-Atlus_%2F_CRI-d73a49?style=for-the-badge" alt="Reverse Engineering" />

</div>

<br/>

> [!NOTE]
> Bienvenue dans la documentation technique exhaustive du projet P2-FR-IS-PSP. Ce document centralise l'intégralité des connaissances accumulées lors du reverse-engineering du jeu. Il est destiné aux développeurs, programmeurs et romhackers souhaitant comprendre ou modifier l'outil de compilation maison (`p2is_tool`), le patcher web, les spécificités du moteur d'Atlus et l'architecture complète de l'UMD PSP.

<br/>

---

## Sommaire
1. [Architecture Globale et Outil Python](#architecture-globale-et-outil-python)
2. [L'Arborescence Absolue et les Formats de Fichiers](#larborescence-absolue-et-les-formats-de-fichiers)
3. [Dépendances, Outils Tiers et Licences](#dépendances-outils-tiers-et-licences)
4. [Spécificités du Moteur Atlus et du Bytecode](#spécificités-du-moteur-atlus-et-du-bytecode)
5. [Tableau Lexical des Opcodes de Contrôle](#tableau-lexical-des-opcodes-de-contrôle)
6. [Anomalies Découvertes et Résolutions Techniques](#anomalies-découvertes-et-résolutions-techniques)
7. [Algorithme du Delta (Gestion Mémoire)](#algorithme-du-delta-gestion-mémoire)
8. [Le Patcher Web (WebAssembly)](#le-patcher-web-webassembly)

<br/>

---

## Architecture Globale et Outil Python

L'outil principal de romhacking (`p2is_tool`) est une application web locale performante pilotée par Python, permettant le désassemblage et le réassemblage du jeu sans saturer la RAM.

<div align="left">
  <img src="https://img.shields.io/badge/Backend-FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/Langage-Python-3670A0?style=flat-square&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Frontend-React-20232A?style=flat-square&logo=react&logoColor=61DAFB" />
</div>

### Fonctionnement du Pipeline Interne
1. **Extraction (I/O LBA) :** L'outil Python (`core/iso.py`) utilise `pycdlib` pour localiser le `P2PT_ALL.cpk` via son *Logical Block Address* (LBA). Un outil tiers (*CriFsLib*) dépaquète cette archive. Le backend décompresse ensuite le LZSS (`CRILAYLA`) des sous-fichiers comme `event.bin` et découpe séquentiellement les scripts d'histoire.
2. **Décodage (Parsing) :** Les scripts Python dans `src/parsers/` analysent le bytecode Atlus. Ils convertissent les mots de 2 octets (hexadécimal Little-Endian) en balises textuelles (ex: `[NL]`) et génèrent les fichiers `.json`. Tout bytecode inconnu est encapsulé dynamiquement dans la balise **`[U+XXXX]`** pour éviter toute perte de données (par exemple `[U+1A2B]`).
3. **Encodage (Injection) :** Les scripts dans `src/encoders/` lisent les JSON traduits. Ils remappent les accents français, recalculent **dynamiquement les tables de pointeurs absolus**, et alignent avec `[SP]` les pointeurs internes des menus à choix multiples pour éviter la corruption de la pile d'exécution.
4. **Rebuild (Compilation ISO) :** Le module de compression Python ré-encode en LZSS les nouveaux scripts. Ils sont injectés dans l'archive CPK modifiée. Enfin, l'ISO finale est construite par **Injection LBA RAW** : on écrase physiquement les secteurs de l'ISO d'origine.

> [!TIP]
> **Live-Logging React :** Le front-end web communique en asynchrone avec FastAPI via Server-Sent Events (SSE). Les sorties consoles du serveur sont retransmises en temps réel, garantissant que l'UI ne gèle jamais durant les calculs lourds (parsing de 399 scripts).

<br/>

---

## L'Arborescence Absolue et les Formats de Fichiers

L'UMD PSP utilise une architecture propriétaire complexe. L'extraction du CPK révèle la structure suivante :

### Les Formats Système Sony (PSP)
* **`.SFO` (System File Object)** : `PARAM.SFO` contient l'ID du jeu (`ULES01557`) et les flags de firmware.
* **`.PMF` (PlayStation Movie Format)** : 19 cinématiques (`F0141.pmf` à `F0159.pmf`, ~300Mo) lues directement par le décodeur matériel (Media Engine) de la PSP pour économiser le CPU.
* **`.GIM` (Graphic Image Map)** : Format optimisé pour la VRAM PSP avec *swizzling* matériel, souvent contenu dans les archives mineures.

### Les Formats Propriétaires (CRI & Atlus)
* **`.CPK` (CRI File System Pack)** : L'archive géante du jeu (254 Mo, `P2PT_ALL.cpk`). Indexée par une "Table Of Contents" (TOC) et compressée via l'algorithme LZSS `CRILAYLA`.
* **`.BIN` (majuscule)** : Fichiers massifs, purs flux binaires sans arborescence (ex : `SE_DVL.BIN` de 66 Mo pour les sons, ou `CD_SHOP.BIN`).
* **`.bin` (minuscule)** : Mini-archives Atlus (TOC interne, données structurées). L'exception vitale est **`event.bin` (37 Mo)** qui contient tous les scripts d'événements de l'histoire.
* **`.BNP` (Bind Pack Atlus)** : Conteneurs de données organisés séquentiellement, sans table d'offsets globale. Exemples vitaux : `F_BE.BNP` (données de combats), `MMAP*.BNP` (dialogues PNJ sur la carte du monde), `TM_EVE.BNP` (cinématiques in-game), ou `EVTUNIT.BNP` (modèles 3D).

<br/>

---

## Dépendances, Outils Tiers et Licences

Notre outil utilise plusieurs dépendances fondamentales. L'intégration respecte strictement leurs licences open-source (accessibles en détails dans `CREDITS.md`).

| Dépendance / Composant | Rôle dans l'Architecture | Auteur | Licence |
|:---|:---|:---|:---|
| **CriFsLib (.NET)** | Utilisé **uniquement** pour l'extraction de l'archive `P2PT_ALL.cpk`. L'injection/rebuild se fait en Python natif pour ne pas altérer la TOC. | [Sewer56](https://github.com/Sewer56) | MIT |
| **pycdlib (Python)** | Analyse ISO 9660 et localisation LBA pour injecter le CPK ou l'EBOOT.BIN en RAW. | [clalancette](https://github.com/clalancette) | LGPL-2.1 |
| **DeltaPatcher (C++)** | Moteur de génération et d'application de patchs différentiels binaires (`.xdelta`). | [marco-calautti](https://github.com/marco-calautti) | GPL-2.0 |
| **Web Patcher (UI/UX)** | Interface Web (HTML/JS/CSS) permettant de patcher le jeu directement depuis le navigateur. | [chenetulipe](https://github.com/chenetulipe) | CC BY-NC-SA 4.0 |

<br/>

---

## Spécificités du Moteur Atlus et du Bytecode

Persona 2 PSP possède une architecture mémoire rigide où le moindre octet mal placé provoque des "Invalid Memory Access".

| Fichier Cible | Format du Texte | Contrainte Technique Majeure |
|:---|:---|:---|
| **`event.bin`** | Shift-JIS & Opcodes | Table d'Offsets Absolus au début de chaque script. Entièrement reconstruite par l'encodeur. |
| **`EBOOT.BIN`** | ENGBIN / Custom | Les menus système. La police a été physiquement altérée par Ghostlight. L'espace ASCII y est devenu un tilde (`~`). |
| **`F_BE.BNP`** | Shift-JIS séquentiel | Lecture de texte contigüe sans table d'index globale. L'ajout de padding classique crashe la PSP. Recompilation via l'Algorithme du Delta. |

<br/>

---

## Tableau Lexical des Opcodes de Contrôle

Le décodeur convertit les opcodes hexadécimaux de la PSP en balises. **Ne supprimez jamais ces balises du texte traduit.**
En plus des opcodes officiellement reconnus, le parser capture **tout hexadécimal inconnu via `[U+XXXX]`** (ex: `[U+13A4]`) pour garantir 100% de rétention mémoire lors du rebuild.

| Opcode (Hex) | Tag Python | Catégorie | Fonction In-Game détaillée |
|:---:|:---:|:---|:---|
| `11 20` | `[SP]` | Formatage | Espace standard utilisé dans le texte Shift-JIS. |
| `11 01` | `[NL]` | Formatage | Saut de ligne (New Line). Les dialogues crashent avec `ΓΓΓ` s'il manque avant la fin. |
| `11 06` | `[E1]` | Terminateur | Partie 1/4 du bloc de fin de dialogue (`E1 E2 E3 E4`). |
| `11 02` | `[E2]` | Terminateur | Partie 2/4 du bloc de fin de dialogue standard. |
| `11 03` | `[E3]` | Terminateur | Partie 3/4 du bloc de fin de dialogue standard. |
| `14 31` | `[E4]` | Terminateur | Partie 4/4 du bloc de fin. Souvent marqueur d'animation d'UI (`[ANIM]`) dans `F_BE`. |
| `11 09` | `[1109]` | Terminateur | Variante de `[E1]` pour le chaînage continu de texte (`1109 E2 E3 E4`). |
| `12 08` | `[1208]` | Choix Multiple | Déclencheur absolu d'un menu de choix. Toujours suivi de `[0002]`. |
| `00 02` | `[0002]` | Choix Multiple | Paramètre d'activation de la fenêtre de choix. |
| `00 14` | `[0014]` | Choix Multiple | Séparateur de fin de chaîne pour chaque option individuelle d'un menu. |
| `14 32` | `[1432]` | Mémoire / UI | Instruction de positionnement du curseur des options de menu. |
| `00 10` | `[0010]` | Mémoire / UI | Variable interne d'espacement des menus. |
| `00 00` | `[NULL]` | Structurel | Null Byte de fin de variable ou décalage de pointeur (`[NULL][NULL]"`). |
| `12 05` | `[1205]` | Cinématique | Pause dramatique automatique du texte (généralement suivie de `[001E]`). |
| `00 1E` | `[001E]` | Cinématique | Définition de la durée de la pause (`001E` = ~30 frames). |
| `11 07` | `[1107]` | Vidange Buffer | Opcode critique de nettoyage du buffer d'affichage (clôture une fenêtre). |
| `11 08` | `[1108]` | Visuel | Balise gérant la fenêtre de texte lors de l'apparition d'un Bust-up. |
| `11 12` | `[1112]` | Variable | Injection en temps réel du Nom de famille du héros défini par le joueur. |
| `11 13` | `[1113]` | Variable | Injection en temps réel du Prénom du héros défini par le joueur. |
| `12 0C...0F` | `[120C]`... | Visuel | Opcodes de changement de couleur du texte ou d'effet sur la police. |
| `12 10` | `[1210]` | Visuel | Restauration de la couleur du texte par défaut. |
| `12 1E` | `[121E]` | Interaction | Force le jeu à attendre l'appui sur ✖ (Similaire à `WAIT`). |
| `XXXX` | `[U+XXXX]` | Secours (Fallback)| Toute valeur binaire de contrôle inconnue est stockée ainsi pour ne pas corrompre le fichier au remontage. |

<br/>

---

## Anomalies Découvertes et Résolutions Techniques

### 1. Le Mystère des Tildes (`~`) et de l'Espace Japonais (`0x8140`)
* **L'explication :** Les développeurs de Ghostlight ont physiquement écrasé l'espace ASCII (`0x0020`) dans la police VRAM du jeu en le remplaçant par un tilde. Ils ont forcé l'utilisation de **l'espace pleine chasse japonais Shift-JIS** (`0x8140`).
* **La solution :** L'encodeur intercepte tous les espaces (normaux, insécables DeepL, ou idéographiques) et force leur encodage binaire en `0x8140`.

### 2. L'Alignement Corrompu des Menus de Choix
* **L'explication :** Le moteur stocke des pointeurs absolus vers les options d'un menu. Si la question FR est plus courte que l'originale anglaise, les pointeurs se décalent, corrompant les choix affichés.
* **La solution :** L'algorithme `_align_menu_text` calcule la différence de longueur binaire et injecte des `[SP]` invisibles avant le balisage `[1208]` pour restaurer l'intégrité mémoire.

### 3. L'Injection RAW (LBA)
* **L'explication :** Recompiler `EBOOT.BIN` avec UMDGen cassait la structure ISO 9660 stricte.
* **La solution :** L'outil Python exploite le *Logical Block Address* (LBA) pour ouvrir l'ISO originale et écraser uniquement les secteurs dédiés à l'EBOOT.BIN en comblant le reste avec des `0x00`.

<br/>

---

## Algorithme du Delta (Gestion Mémoire)

Dans les `.BNP` (`F_BE.BNP` - texte de combat), le moteur charge le texte séquentiellement, sans table d'offsets absolue.

Si une traduction française est plus courte que l'originale, ajouter du padding (remplissage avec `00` entre chaque ligne) provoque un dépassement de mémoire critique (*Invalid Memory Access*) car le jeu tente d'exécuter le padding.

**Solution employée (Le Delta) :**
L'encodeur `fbe_parser.py` "tasse" (compacte) tous les blocs de dialogues français les uns derrière les autres sans espaces morts. 
La différence de taille (le *Delta*) est accumulée. À la toute fin du bloc global de données (après la toute dernière ligne de dialogue du fichier), la somme exacte du padding de tout le fichier est injectée d'un coup pour atteindre la taille du fichier d'origine, maintenant l'intégrité de la TOC du CPK.

<br/>

---

## Le Patcher Web (WebAssembly)

Afin de distribuer facilement la traduction, un **Patcher Web local** ultra-performant a été développé (`p2is_patcher`).

* ✦ **Moteur de Diff (WASM) :** Basé sur la librairie C++ *DeltaPatcher* compilée en WebAssembly (`xdelta3.wasm`).
* ✦ **Worker Asynchrone :** L'application s'exécute dans un Web Worker (`xdelta3.worker.js`) pour ne pas faire geler l'interface du navigateur lors du patch.
* ✦ **Gestion Mémoire (Streams & Service Worker) :** La limite de RAM d'un onglet de navigateur est d'environ 2Go. Pour patcher une ISO PSP, le patcher utilise l'API Streams associée à un *Service Worker* (via `mitm.html` et `sw.js`). Il "télécharge" le fichier généré bit par bit sur le disque dur local au fur et à mesure de sa création en mémoire. Cela permet de traiter d'immenses fichiers sans jamais saturer la RAM.

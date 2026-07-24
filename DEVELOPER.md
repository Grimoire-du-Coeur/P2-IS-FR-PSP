<div align="center">
  
# Guide Développeur & Base de Connaissances (P2IS Tool)
  
**Persona 2: Innocent Sin FR (PSP) - ULES01557**

<br/>

<img src="https://img.shields.io/badge/Statut-Documentation_Technique-0366d6?style=for-the-badge" alt="Statut" />
<img src="https://img.shields.io/badge/Reverse_Engineering-Atlus_%2F_CRI-d73a49?style=for-the-badge" alt="Reverse Engineering" />

</div>

<br/>

> [!NOTE]
> Bienvenue dans la documentation technique exhaustive (V2) du projet P2-FR-IS-PSP. Ce document centralise l'intégralité des connaissances accumulées lors du reverse-engineering du jeu. Il est destiné aux développeurs, programmeurs et romhackers souhaitant comprendre ou modifier l'outil de compilation maison (`p2is_tool`), les spécificités du moteur d'Atlus et l'architecture complète de l'UMD PSP.

<br/>

---

## Sommaire
1. [Architecture Globale et Stack Technique](#architecture-globale-et-stack-technique)
2. [L'Arborescence Absolue et les Formats de Fichiers](#larborescence-absolue-et-les-formats-de-fichiers)
3. [Dépendances, Outils Tiers et Licences](#dépendances-outils-tiers-et-licences)
4. [Spécificités du Moteur Atlus et du Bytecode](#spécificités-du-moteur-atlus-et-du-bytecode)
5. [Tableau Lexical des Opcodes de Contrôle](#tableau-lexical-des-opcodes-de-contrôle)
6. [Anomalies Découvertes et Résolutions Techniques](#anomalies-découvertes-et-résolutions-techniques)
7. [Algorithme du Delta (Gestion Mémoire)](#algorithme-du-delta-gestion-mémoire)
8. [Structure du Code Source Python](#structure-du-code-source-python)
9. [Le Patcher Web (WebAssembly)](#le-patcher-web-webassembly)

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
Le traitement automatisé de l'ISO s'articule autour de 4 grandes phases, orchestrées par le Backend Python. Le traitement manipule des fichiers allant jusqu'à plus d'1 Go sans saturer la mémoire grâce aux Streams.

1. **Extraction :** Isolement du fichier `P2PT_ALL.cpk` depuis l'ISO. Un outil tiers (*CriFsLib*) dépaquète l'archive. Ensuite, le Python décompresse en LZSS (`CRILAYLA`) les fichiers vitaux comme `event.bin`, puis découpe séquentiellement les 399 scripts d'histoire.
2. **Décodage (Parsing) :** Analyse du bytecode Atlus, séparation des opcodes de contrôle (convertis en balises textuelles `[TAG]`) du texte pur. Génération de fichiers `.json` destinés aux traducteurs.
3. **Encodage (Injection) :** Lecture du JSON traduit. Remappage des accents français (via la table `ACCENT_MAP`). **Recalcul dynamique des tables de pointeurs absolus** pour s'adapter aux variations de taille des dialogues français. Alignement conditionnel (`[SP]`) des pointeurs internes des menus à choix multiples pour éviter la corruption de la pile d'exécution du jeu.
4. **Rebuild (Compilation ISO) :** Recompression LZSS des nouveaux scripts. Injection binaire dans l'archive CPK. Le rebuild de l'ISO final est réalisé par **Injection LBA RAW** dans l'image `.iso` 9660.

> [!TIP]
> **Live-Logging React :** L'interface utilisateur Web communique de manière asynchrone avec le backend Python via FastAPI (Server-Sent Events). Les sorties consoles du serveur sont retransmises en temps réel vers le Front-End, évitant de bloquer l'UI durant les lourdes opérations I/O.

<br/>

---

## L'Arborescence Absolue et les Formats de Fichiers

La compréhension de l'architecture UMD de la PSP et des formats propriétaires japonais est primordiale pour opérer sur ce jeu. Aucun format n'est standard.

### Les Formats Système Sony (PSP)
* **`.SFO` (System File Object)** : Présent dans `PARAM.SFO`. C'est la carte d'identité du jeu, contenant l'identifiant `ULES01557` et la version du firmware requise.
* **`.PMF` (PlayStation Movie Format)** : Conteneur vidéo dérivé de l'H.264 et ATRAC3plus. Le jeu contient 19 cinématiques (`F0141.pmf` à `F0159.pmf`, environ 300Mo) lues directement par le décodeur matériel (Media Engine) de la console pour économiser le processeur central.
* **`.GIM` (Graphic Image Map)** : Format d'image optimisé pour être copié instantanément dans la mémoire vidéo (VRAM) de la PSP sans décompression CPU (les pixels utilisent le *swizzling* matériel).

### Les Formats Propriétaires (CRI & Atlus)
* **`.CPK` (CRI File System Pack)** : L'archive géante du jeu (254 Mo, `P2PT_ALL.cpk`). C'est le standard de CRI Middleware. Il contient 136 fichiers indexés par une "Table Of Contents" (TOC) stricte, et compressés via un dérivé du LZSS appelé `CRILAYLA`.
* **`.BIN` (majuscule)** : Fichiers massifs, purs flux binaires sans structure d'arborescence complexe (exemple : `SE_DVL.BIN` qui pèse 66 Mo).
* **`.bin` (minuscule)** : Mini-archives internes au moteur d'Atlus. Elles contiennent une TOC interne, des données structurées et des images GIM packées. L'exception principale est `event.bin` (37 Mo) qui rassemble tous les scripts d'événements.
* **`.BNP` (Bind Pack Atlus)** : Conteneurs de données organisés séquentiellement, sans documentation officielle. Exemples : `F_BE.BNP` (données de combats), `MMAP*.BNP` (dialogues PNJ et maps), ou encore des modèles 3D (`EVTUNIT.BNP`).

<br/>

---

## Dépendances, Outils Tiers et Licences

Le projet repose sur plusieurs dépendances fondamentales. L'intégration de ces outils respecte leurs licences respectives (détails complets disponibles sur nos mentions légales).

| Dépendance | Fonction dans le projet | Auteur / Licence |
|:---|:---|:---|
| **CriFsLib (.NET)** | **Extraction exclusive** de l'archive `P2PT_ALL.cpk`. L'injection et la recompilation du CPK modifié sont entièrement gérées en Python natif dans notre backend pour garantir l'intégrité de la TOC sans passer par une CLI externe. | *Sewer56* (Licence MIT / Open-Source) |
| **pycdlib (Python)** | Analyse du système de fichiers ISO 9660. Utilisée pour localiser les fichiers critiques (EBOOT, CPK) via leur *Logical Block Address* (LBA), permettant une injection RAW par-dessus les données existantes. | *clalancette* (Licence LGPL-2.1) |
| **DeltaPatcher (C++)** | Utilisé pour générer le patch `.xdelta` final qui sera distribué aux joueurs (calculant la différence binaire entre l'ISO EUR originale et notre ISO traduite). | *marco-calautti* (Licence GPL-2.0) |

<br/>

---

## Spécificités du Moteur Atlus et du Bytecode

Persona 2 sur PSP utilise un moteur de jeu complexe reposant sur une architecture mémoire rigide où le moindre octet mal placé provoque des "Invalid Memory Access".

| Fichier Cible | Format du Texte | Contrainte Technique Majeure |
|:---|:---|:---|
| **`event.bin`** (Histoire) | Shift-JIS & Opcodes Hex | Table d'Offsets Absolus au début de chaque script. Le script Python `bin_encoder.py` reconstruit intégralement cette table pour chaque dialogue traduit. |
| **`EBOOT.BIN`** (Système) | ENGBIN / Custom Font | Le fichier exécutable contient les menus système et descriptions d'objets. La police du jeu a été modifiée de façon très inhabituelle par les localisateurs anglais, forçant des substitutions d'octets. |
| **`F_BE.BNP`** (Combat) | Shift-JIS (Pointeurs séquentiels) | Les données sont lues de façon contigüe. L'ajout d'octets de padding (`0x00`) entre les dialogues provoque des crashs immédiats. La recompilation de ce fichier utilise **l'Algorithme du Delta** (voir plus bas) pour compacter le texte de combat de façon optimale. |

<br/>

---

## Tableau Lexical des Opcodes de Contrôle

Le moteur lit des opcodes hexadécimaux spécifiques. Notre outil de parsing convertit ces mots de 2 octets (Little-Endian) en balises textuelles (ex: `[NL]`) pour les protéger lors de la traduction. 

> [!CAUTION]
> **Architecture de Contrôle :** Ces balises ne doivent jamais être retirées d'une ligne de dialogue par un traducteur. Elles dirigent l'affichage et l'interface utilisateur.

| Opcode (Hex) | Tag Python | Catégorie | Fonction In-Game détaillée |
|:---:|:---:|:---|:---|
| `11 20` | `[SP]` | Formatage | Espace standard utilisé dans le texte Shift-JIS (Souvent réaligné par le code Python pour préserver les offsets des menus). |
| `11 01` | `[NL]` | Formatage | Saut de ligne (New Line). Obligatoire pour ne pas déborder des fenêtres (max 3 lignes). Les menus et dialogues crashent avec `ΓΓΓ` si cet opcode est manquant à la toute fin avant le terminateur. |
| `11 06` | `[E1]` | Terminateur | Partie 1/4 du bloc de fin de dialogue standard (`E1 E2 E3 E4`). |
| `11 02` | `[E2]` | Terminateur | Partie 2/4 du bloc de fin de dialogue standard. |
| `11 03` | `[E3]` | Terminateur | Partie 3/4 du bloc de fin de dialogue standard. |
| `14 31` | `[E4]` | Terminateur | Partie 4/4 du bloc de fin de dialogue. Utilisé aussi comme balise d'animation d'UI (`[ANIM]`) dans certains contextes isolés. |
| `11 09` | `[1109]` | Terminateur | Variante de `[E1]` utilisée pour l'enchaînement de dialogues continus (Chaînage `1109 E2 E3 E4`). |
| `12 08` | `[1208]` | Choix Multiple | Déclencheur absolu d'un menu de choix contextuel. Toujours suivi de `[0002]` pour activer la fenêtre de sélection. |
| `00 02` | `[0002]` | Choix Multiple | Paramètre d'activation du menu de choix (lié à `1208`). |
| `00 14` | `[0014]` | Choix Multiple | Séparateur de fin de chaîne pour chaque option individuelle d'un menu de choix. |
| `14 32` | `[1432]` | Mémoire / UI | Instruction de positionnement du curseur ou de nettoyage de la fenêtre pour les options du menu. |
| `00 10` | `[0010]` | Mémoire / UI | Variable interne d'espacement des menus. |
| `00 00` | `[NULL]` | Structurel | Null Byte de fin de variable ou décalage de pointeur `[NULL][NULL]"`. Les modifications nécessitent un réalignement parfait avec `[SP]`. |
| `12 05` | `[1205]` | Cinématique | Pause dramatique automatique du texte (généralement suivie de `[001E]`). |
| `00 1E` | `[001E]` | Cinématique | Définition de la durée de la pause (`001E` = ~30 frames). |
| `11 07` | `[1107]` | Vidange Buffer | Opcode critique de nettoyage du buffer d'affichage de la console PSP pour clore une session de dialogue. |
| `11 08` | `[1108]` | Visuel | Balise gérant la fenêtre de texte, liée aux apparitions de portraits (Bust-ups). |
| `11 12` | `[1112]` | Variable | Injection en temps réel du Nom de famille du héros défini par le joueur. |
| `11 13` | `[1113]` | Variable | Injection en temps réel du Prénom du héros défini par le joueur. |
| `12 0C...0F` | `[120C]`... | Visuel | Opcodes de changement de couleur du texte ou d'effet visuel spécifique sur la police. |
| `12 10` | `[1210]` | Visuel | Restauration de la couleur du texte par défaut (après un changement `120C`). |
| `12 1E` | `[121E]` | Interaction | Force le jeu à attendre l'appui du joueur sur ✖ pour valider la ligne (Similaire à `WAIT`). |

<br/>

---

## Anomalies Découvertes et Résolutions Techniques

Durant le développement, l'équipe a fait face à plusieurs problématiques nécessitant du reverse-engineering poussé du code d'Atlus et de Ghostlight.

### 1. Le Mystère des Tildes (`~`) et de l'Espace Japonais (`0x8140`)
Lors du test de l'injection des textes systèmes dans l'`EBOOT.BIN`, l'ensemble des espaces apparaissaient sous forme de tildes (`Ajuster ~ la ~ difficulté`). 
* **L'explication :** Les développeurs de Ghostlight (traducteurs anglais originaux) n'ont **pas** utilisé l'encodage classique ASCII pour l'espace (`0x0020`). Ils ont physiquement écrasé ce caractère dans la police (font) VRAM du jeu, le remplaçant par un tilde. En échange, ils ont forcé l'utilisation de l'**espace pleine chasse japonais Shift-JIS** (`0x8140`).
* **La solution :** L'encodeur `eboot_parser.py` intercepte tous les types d'espaces générés par les traducteurs (espace normal `0x0020`, espaces insécables ` ` de DeepL, ou idéographiques `　`) et force leur encodage binaire en `0x8140`. De plus, les retours à la ligne `
` sont sécurisés et traduits obligatoirement en `0x000A`.

### 2. L'Alignement Corrompu des Menus de Choix
* **L'explication :** Le moteur du jeu stocke des pointeurs matériels (Relatifs & Absolus) vers les options d'un menu de réponse (ex: 1. Oui / 2. Non). Si la question française précédant le menu est plus courte ou plus longue que l'anglaise, les pointeurs internes se décalent et le jeu affiche des déchets mémoires ou n'affiche que la première option.
* **La solution :** Un algorithme d'alignement a été créé dans `core/text.py` (`_align_menu_text`). L'outil Python calcule la différence de longueur binaire entre la question originelle et la française, et injecte automatiquement des `[SP]` invisibles avant le balisage `[1208]` pour restaurer l'intégrité de la structure mémoire sans corrompre le texte.

### 3. Le Crash TypeError de l'API avec les Points de suspension (`…`)
* **L'explication :** Le script d'encodage utilise la normalisation Unicode `unicodedata.normalize('NFKD')` pour nettoyer les accents non pris en charge. Cependant, le caractère "points de suspension" (`…`) se décomposait en trois points distincts (`.`, `.`, `.`). La boucle d'encodage binaire `ord(c)` qui s'attendait à un seul caractère recevait une chaîne de longueur 3 et faisait crasher brutalement le backend.
* **La solution :** La normalisation NFKD a été déplacée pour ne s'appliquer qu'à la chaîne globale, avant la boucle itérative par caractère, évitant ainsi la fragmentation. L'outil convertit automatiquement le glyphe `…` en trois points standards `...`.

### 4. L'Injection RAW (LBA) de l'EBOOT.BIN
* **L'explication :** L'ISO 9660 de la PSP possède une *Table of Contents* stricte. Au départ, l'outil recompilait un fichier `EBOOT_MODIFIED.BIN` sans parvenir à le réinsérer proprement au sein de l'ISO originale, car les utilitaires de type *UMDGen* cassaient les pointeurs relatifs.
* **La solution :** L'outil Python `core/iso.py` exploite la librairie `pycdlib` pour identifier le LBA (Logical Block Address) physique de `/PSP_GAME/SYSDIR/EBOOT.BIN`. Le script ouvre l'ISO en mode octet pur (`'rb+'`), cherche ce secteur spécifique (LBA × 2048), écrase l'exécutable original avec la version traduite, et rajoute un padding de `0x00` jusqu'à atteindre la taille exacte d'origine pour ne pas corrompre le disque.

<br/>

---

## Algorithme du Delta (Gestion Mémoire)

Dans les fichiers de type `.BNP` (comme `F_BE.BNP` gérant le texte de combat et les invocations de Personas), le moteur de jeu charge le texte de manière séquentielle, pointeur après pointeur, sans table d'offsets absolus de référence pour s'y retrouver.

Si une traduction française est plus courte que l'originale anglaise, ajouter du padding classique (remplissage avec `00` pour combler le trou) provoque un dépassement de mémoire critique (*Invalid Memory Access*) car le jeu tente d'exécuter le padding comme s'il s'agissait d'un opcode de combat.

**Solution employée (Le Delta) :**
Plutôt que de combler l'espace vide par des zéros entre les lignes, l'encodeur `fbe_parser.py` "tasse" (compacte) tous les blocs de dialogues français les uns derrière les autres. 
La différence de taille globale (le *Delta*) est accumulée et soustraite de tous les pointeurs dynamiques qui suivent dans la mémoire. 
À la toute fin du bloc global de données (après la toute dernière ligne de dialogue du fichier entier), la somme exacte du padding `00` de tout le fichier est injectée pour atteindre la taille du fichier original, évitant au jeu de tomber dessus par erreur lors d'un combat, tout en maintenant l'intégrité de la TOC de l'archive CPK.

<br/>

---

## Structure du Code Source Python

Le backend Python localisé dans `p2is_tool/src/` suit une séparation stricte des responsabilités :

* ✦ **`core/iso.py`** : Manipulation directe de l'ISO 9660, extraction raw LBA, injection de l'EBOOT et patch du CPK en RAM.
* ✦ **`core/text.py`** : Moteur de conversion String ↔ Shift-JIS Atlus, logique d'alignement de la mémoire via `[SP]`, et intégration de la table `ACCENT_MAP` (remappage dynamique des accents).
* ✦ **`core/compression.py`** : Logique bas niveau des algorithmes de décompression LZSS propriétaire `CRILAYLA`.
* ✦ **`parsers/`** : Scripts d'heuristique de détection de texte (ex. `bin_parser.py`, `eboot_parser.py`). Conçus pour isoler le texte des flux de pointeurs.
* ✦ **`encoders/`** : Logique d'assemblage binaire, de reconstruction des tables de pointeurs (`event.bin`) et d'application de l'Algorithme du Delta sur les BNP.

<br/>

---

## Le Patcher Web (WebAssembly)

Afin de faciliter l'installation du patch FR par les joueurs sans nécessiter le téléchargement d'un logiciel tiers, un **Patcher Web** complet a été développé dans le dossier `p2is_patcher/`.

* ✦ **Moteur de Diff :** Basé sur *DeltaPatcher* compilé en WebAssembly (`xdelta3.wasm`).
* ✦ **Performance et UI :** L'application tourne dans un Web Worker (`xdelta3.worker.js`) pour ne pas faire geler l'interface (React/HTML) du navigateur lors du calcul du patch.
* ✦ **Gestion Mémoire (Streams) :** Pour gérer des ISO de plus de 1 Go dans le navigateur sans saturer la RAM (limite stricte des navigateurs fixée à ~2Go), le patcher utilise l'API des *Streams* et un *Service Worker* (`sw.js` / `mitm.html`) permettant de télécharger le fichier généré bit par bit au fur et à mesure de sa création locale.

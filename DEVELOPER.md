<div align="center">
  
# Guide Développeur & Base de Connaissances
  
**Persona 2: Innocent Sin FR (PSP)**

[![Python](https://img.shields.io/badge/Python-3670A0?style=flat-square&logo=python&logoColor=white)](#)
[![Reverse Engineering](https://img.shields.io/badge/Reverse%20Engineering-Atlus%20%2F%20CRI-blue?style=flat-square)](#)
[![Statut](https://img.shields.io/badge/Statut-Documentation-orange?style=flat-square)](#)

</div>

<br/>

> [!NOTE]
> Bienvenue dans la "Bible" technique du projet de traduction française de *Persona 2: Innocent Sin* (ULES01557). Ce document s'adresse aux développeurs et romhackers souhaitant reprendre, modifier ou étudier le projet. 
> Il recense l'intégralité des connaissances acquises sur le moteur de jeu Atlus, les archives CRI Middleware, la structure de l'ISO, ainsi qu'un audit complet de l'outil `p2is_fr_tool.py`.

---

## Sommaire
1. [Vue d'Ensemble & Dépendances Tiers](#vue-densemble--dépendances-tiers)
2. [La Pipeline Complète](#la-pipeline-complète)
3. [Table des Offsets & Gestion Mémoire](#table-des-offsets--gestion-mémoire)
4. [Le Bug Philémon & L'Algorithme du Delta](#le-bug-philémon--lalgorithme-du-delta)
5. [Structure et Contraintes des Menus](#structure-et-contraintes-des-menus)
6. [Encodage des Textes et Shift-JIS](#encodage-des-textes-et-shift-jis)
7. [Dictionnaire des Opcodes et Symboles](#dictionnaire-des-opcodes-et-symboles)
8. [Glossaire des Fonctions](#glossaire-des-fonctions)
9. [Audit et Pistes d'Amélioration (V2)](#audit-et-pistes-damélioration-v2)

---

## Vue d'Ensemble & Dépendances Tiers

L'outil centralise toutes les étapes du romhacking via une interface graphique (Tkinter). Bien qu'il effectue la majorité du traitement de manière native (in-memory en Python), il s'appuie sur un outil tiers critique pour l'extraction de l'archive principale du jeu.

### CriFsLib (Extraction CPK)

Pour extraire les fichiers contenus dans `P2PT_ALL.cpk` (~800 Mo), l'outil automatise les appels en ligne de commande vers **CriFsLib.GUI.exe**. 

> [!IMPORTANT]
> **Pourquoi cette dépendance ?** Le format `.cpk` de CRI Middleware est un système de fichiers virtuel complexe. Plutôt que de réécrire un parseur de CPK entier (et lent) en Python, l'outil utilise la puissance de `CriFsLib` (codé en C# par Sewer56) pour extraire l'archive binaire instantanément et sans erreur de corruption.

**Lien officiel :** [Sewer56/CriFsV2Lib sur GitHub](https://github.com/Sewer56/CriFsV2Lib)

---

## La Pipeline Complète

Le processus de traduction s'articule autour de 3 étapes majeures, correspondant aux onglets de l'interface graphique :

```text
ISO Originale (ULES01557)
    │
[ 1. Scanner (Extraction Totale) ]
    ├── Parse de l'ISO 9660 pour extraire P2PT_ALL.cpk.
    ├── Appel subprocess vers CriFsLib pour unpacker le CPK.
    ├── Décompression interne CRILAYLA pour isoler event.bin.
    ├── Découpage de event.bin en sous-scripts (script_000.bin ➔ script_398.bin).
    ├── Parsing du binaire et création des .JSON pour les traducteurs.
    │
[ 2. Injection (Encodage Total) ]
    ├── Lecture des JSON (qui intègrent les champs question_fr et choix_fr).
    ├── Recalcul des tailles (text budget) et des tables de pointeurs.
    ├── Ré-encodage des chaînes en binaire (Shift-JIS Atlus + Balises).
    ├── Création des binaires patchés (script_XXX_fr.bin, F_BE_fr.bnp...).
    │
[ 3. Rebuild ISO ]
    ├── Compression CRILAYLA des fichiers si nécessaire.
    ├── Réinjection des scripts FR dans event.bin.
    ├── Réinjection de event.bin et F_BE dans l'ISO d'origine.
    ├── Recalcul de la TOC du CPK (Tailles modifiées).
    ├── Patch LBA (Logical Block Addressing) : l'archive grossie est déplacée à la fin de l'ISO.
    └── Génération de l'ISO finale : "Persona 2 Innocent Sin FR.iso".
```

---

## Table des Offsets & Gestion Mémoire

Le moteur d'Atlus est hétérogène. Selon le fichier, l'architecture mémoire diffère. Si un texte français est plus long ou plus court que l'anglais, le décalage doit être géré selon des règles distinctes :

| Fichier | Type de Pointeurs | Conséquence d'une modification de taille | Solution Technique Appliquée |
|---------|-------------------|------------------------------------------|------------------------------|
| **`event.bin`** | Absolus (Header) | Désynchronisation totale. Crashs et textes corrompus au chargement de la map. | L'outil reconstruit **intégralement** la table des pointeurs de A à Z lors de l'encodage. |
| **`MMAPxx.BNP`** | Absolus (Header) | Écran noir au chargement de la carte. | *Non implémenté* (le fichier ne se ré-encode pas encore correctement). |
| **`F_BE.BNP`** | Aucun Pointeur (Séquentiel) | Le moindre octet de padding fait crasher le combat. | *Non implémenté* (le fichier ne se ré-encode pas encore correctement, voir section suivante). |

---

## Le Bug Philémon & L'Algorithme du Delta

L'un des défis majeurs du projet concernait `F_BE.BNP` (Battle Engine). Initialement, pour éviter de modifier la taille globale de l'archive, l'outil comblait le texte manquant avec du remplissage (padding).

- **Essai 1 (`05 12 00 00`) :** Balise de couleur transparente. Faisait exploser le buffer de la VRAM (écrans noirs, plantages).
- **Essai 2 (`02 11` Wait) & Essai 3 (`00` Zéros) :** Déclenchait l'Erreur `Invalid Memory Access e69681a8` (Surnommée "Crash Philémon") lors des combats de boss.

> [!WARNING]
> **Pourquoi ça crashait ?**
> Le Battle Engine (`F_BE`) n'a pas de table d'offsets. Au lancement du combat, le moteur scanne séquentiellement le fichier. À chaque opcode de fin de dialogue (`31 14`), il considère automatiquement que l'octet suivant est un nouveau script et génère un pointeur en RAM. En ajoutant du padding *après* le `31 14`, le scanner prenait nos zéros pour des instructions légitimes, essayait de les exécuter, lisait la mémoire hors-limites, et crashait violemment.

**La Théorie : L'Algorithme du Delta (En chantier)**
Pour contourner ce problème, l'outil s'interdit formellement de "padder" le fichier `F_BE.BNP`. La théorie actuelle (l'Algorithme du Delta) consiste à ce que la fonction `encode_fbe_slot()` rétrécisse dynamiquement la portion du fichier et retourne la différence de taille (`delta`), pour ensuite décaler tous les slots suivants afin qu'ils s'emboîtent sans un seul octet vide.

> [!CAUTION]
> **Attention : Cette méthode ne fonctionne toujours pas.** Bien qu'elle vise à empêcher le Crash Philémon, le fichier généré reste instable ou inutilisable en jeu (artefacts visuels, blocages). Il est très probable qu'il existe des contraintes d'alignement cachées (ex: padding forcé sur 4 octets) ou des pointeurs internes non identifiés. Le ré-encodage propre de `F_BE.BNP` est donc toujours un problème ouvert et non résolu.

---

## Structure et Contraintes des Menus

### A. Structure d'un JSON avec Menu
Les menus sont encodés avec la balise de choix `[1208]`. L'outil sépare l'intro des choix dans des champs spécifiques pour simplifier la vie des traducteurs. L'encodeur reconstruit la chaîne finale à la compilation.

```json
{
  "id": 3,
  "texte_orig": "Have[SP]you[SP]decided...\\n[1208][0002]...[0014]Yeah.[0014]\\n...[0014]Not[SP]yet.[0014]",
  "question_fr": "T'as une idée de ce que tu veux faire\naprès le lycée ?",
  "choix_fr": ["Ouais, j'ai décidé.", "Pas encore."]
}
```

### B. Contraintes du Moteur de Menu

1. **Terminaison (`11 01`) :** Le jeu crash si un menu de choix ne se termine pas par un `NL` (New Line). L'outil l'ajoute silencieusement.
2. **Alignement `[SP]` :** Les choix d'un menu utilisent des **pointeurs absolus internes au bytecode**. L'outil utilise `_align_menu_text()` pour injecter intelligemment des `[SP]` (Espaces invisibles) entre la question et les choix afin de maintenir ces derniers à l'offset exact attendu par le jeu.
3. **Cohérence Intro/Menu :** Le jeu affiche d'abord l'intro, puis rafraîchit l'écran avec l'intro répétée + les choix. Une fonction dédiée vérifie que les traducteurs ont mis la même phrase dans les deux cas.

---

## Encodage des Textes et Shift-JIS

Atlus utilise un Shift-JIS lourdement modifié avec des balises de contrôle (`[COLOR_RED]`, `[WAIT]`, `[1431]`).

> [!NOTE]
> Pour afficher les accents français (é, à, ç, É), nous n'avions pas la place d'injecter une nouvelle police VRAM (taille fixe). La solution retenue est le remapping via le dictionnaire `ACCENT_MAP` en Python.

L'outil convertit un caractère accentué français vers un glyphe spécifique (souvent un caractère latin étendu inutilisé) qui a été redessiné graphiquement avec un accent dans les textures de la police (VRAM) :

| Minuscules | Glyphe Remplaçant | Majuscules | Glyphe Remplaçant |
|------------|-------------------|------------|-------------------|
| `é` | `Ğ` | `É` | `Ņ` |
| `è` | `ò` | `È` | `Ũ` |
| `ê` | `¿` | `Î` | `£` |
| `ô` | `Æ` | `Ô` | `ō` |
| `œ` | `ë` | `Œ` | `Ǩ` |
| `ü` | `ˠ` | `Û` | `ĵ` |
| `ï` | `Ȗ` | | |

L'outil remplace automatiquement ces lettres lors de l'appel à `text_to_bytes()`. L'UTF-16 brut ne marchera pas si le glyphe n'existe pas dans le VRAM font du jeu, il faut absolument utiliser ces caractères mappés.

## Dictionnaire des Opcodes et Symboles

Bien que le dictionnaire complet ne soit pas totalement reversé, voici les opcodes de contrôle majeurs que l'outil gère sous forme de tags (ex: `[1431]`) ou qu'il traite en interne :

| Opcode Hex (Little Endian) | Tag Outil / Nom | Fonction In-Game |
|----------------------------|-----------------|------------------|
| `00 22` | `[START]` | Marque officiellement le début d'une chaîne de dialogue. |
| `11 07` | `[END]` | Terminateur de chaîne standard. |
| `11 01` | `[NL]` | New Line (Retour à la ligne). Obligatoire avant le terminateur d'un menu. |
| `12 08` | `[CHOICE]` | Balise initiant l'affichage des choix d'un menu. |
| `14 31` | `[ANIM / EVENT]` | Balise complexe d'événement (visages, animations). Le scanner de `F_BE.BNP` s'en sert pour délimiter la fin d'un script de combat. |
| `02 11` | `[WAIT 0 / NOP]` | Instruction "Wait". Historiquement testée comme NOP (No Operation) pour padder, mais fait crasher les scanners séquentiels comme le Battle Engine. |
| `00 00` | `[NULL]` | Zéro terminal, parfois utilisé pour le padding, parfois lu comme un faux script. |

### Problèmes d'Encodage Persistants

> [!CAUTION]
> Bien que l'algorithme du Delta empêche les crashs mémoire, nous rencontrons encore des artefacts visuels ou des comportements anormaux sur les cartes 3D (`MMAPxx`) et dans certains scripts de boss (`F_BE`). 
> Cela est dû au fait que notre système de ré-encodage (qui recalcule brutalement la taille des chaînes) ne prend pas encore en compte *toutes* les structures internes. Par exemple, certaines balises Atlus consomment plus d'octets que prévu, ou certains blocs de textes nécessitent des alignements spécifiques sur 4 octets (Word Alignment) que l'outil ne respecte pas parfaitement. Ces mystères d'encodage nécessiteront une investigation plus poussée.

---

## Glossaire des Fonctions

L'outil actuel regroupe des dizaines de fonctions dans un unique fichier `p2is_fr_tool.py`. En voici le dictionnaire :

**1. Core / Outils de base :**
- `decode_text(data)` : Transforme le binaire propriétaire en string avec `[TAGS]`.
- `text_to_bytes(text)` : Convertit la string (avec remapping d'accents) en hexadécimal Atlus.

**2. CRILAYLA (Compression LZSS) :**
- `crilayla_decompress(data)` : Extrait les données pures depuis le buffer LZSS.
- `crilayla_compress(data)` : Recompresse les fichiers si nécessaire pour le CPK.

**3. Extraction & Parsing :**
- `extract_cpk_from_iso()` : Localise `P2PT_ALL.cpk` dans l'ISO et l'extrait.
- `extract_event_from_cpk()` : Unpack CPK et décompression CRILAYLA de `event.bin`.
- `find_dialogs(data)` : Scanne avec heuristique hexadécimale et produit les JSON.
- `decode_fbe_slot()` / `parse_fbe_text()` : Décodage très spécifique pour extraire les balises d'animations (`[1431]`) intriquées dans le texte du Battle Engine.

**4. Manipulation des Menus JSON :**
- `_parse_choices(body)` : Coupe de force brute le bytecode des menus pour séparer question et choix.
- `_rebuild_choice_body()` : Reformate l'objet JSON en string de compilation complète.
- `_align_menu_text()` : Algorithme critique qui comble l'espace manquant de la Question FR avec des `[SP]`.

**5. Encodage Binaire :**
- `encode_bin_from_json()` : Encode un fichier script d'Histoire normal.
- `encode_fbe_bnp_from_json()` : Encode le Battle Engine avec gestion mathématique du **Delta**.
- `rebuild_event_bin()` : Recalcule la Table des Pointeurs Absolus d'`event.bin` et concatène les sous-scripts.

**6. ISO Rebuild (La MasterClass) :**
- `update_iso_metadata()` : Modifie la TOC (Table of Contents) du fichier CPK.
- `rebuild_iso()` : Parcours les tables LBA (Logical Block Addressing) Path Table L/M de l'ISO 9660, écrase les vieux blocs avec le nouveau CPK grossi en fin de disque, et génère l'ISO modifiée.

---

## Audit et Pistes d'Amélioration (V2)

Si l'outil doit être repris ou amélioré, plusieurs défauts d'architecture sont à corriger :

1. **Architecture Monolithique (God Object) :** Le script de 3100 lignes contient le GUI (Tkinter), la compression binaire, la table LBA, et le traducteur. Le code doit être modularisé (`gui.py`, `iso_builder.py`, `text_engine.py`, `crilayla.py`).
2. **Goulot d'étranglement CRILAYLA :** La décompression LZSS en pur Python prend de précieuses secondes et fait figer le GUI. Une extension C (`ctypes` / `cffi`) ou Cython devrait être implémentée pour la méthode `crilayla_decompress`.
3. **Modifications In-Place & RAM (`bytearray`) :** Manipuler un `P2PT_ALL.cpk` de 800 Mo sous forme de `bytearray` et y insérer/supprimer des données provoque des décalages mémoires massifs (ralentissements). Utiliser `io.BytesIO` ou traiter le fichier par chunks est obligatoire pour une V2 propre.
4. **Troncature "Tag-Aware" :** Actuellement, si le texte FR déborde du budget strict d'un slot binaire non extensible, le script le tronque aveuglément via un slice Python (`t_bytes = text_to_bytes(t_fr[:budget//2])`). Cela peut couper une chaîne au milieu d'une balise Atlus `[COLOR_RED]` et faire crasher le moteur. L'encodeur doit devenir conscient des balises ("Tag-Aware").

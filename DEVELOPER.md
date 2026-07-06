<div align="center">
  
# Guide Développeur & Base de Connaissances
  
**Persona 2: Innocent Sin FR (PSP)**

[![Statut](https://img.shields.io/badge/Statut-Documentation-orange?style=flat-square)](#)
[![Reverse Engineering](https://img.shields.io/badge/Reverse%20Engineering-Atlus%20%2F%20CRI-blue?style=flat-square)](#)

</div>

<br/>

> [!NOTE]
> Bienvenue dans la documentation technique exhaustive du projet. Ce document s'adresse aux développeurs, programmeurs et romhackers. Il détaille l'architecture de notre outil de compilation maison (`p2is_tool`), les spécificités du moteur Atlus et le fonctionnement des archives CRI Middleware.

---

## Sommaire
1. [La Stack Technique (V2)](#la-stack-technique-v2)
2. [Architecture et Pipeline de Compilation](#architecture-et-pipeline-de-compilation)
3. [Gestion Mémoire et Algorithme du Delta](#gestion-mémoire-et-algorithme-du-delta)
4. [Le Remappage Automatique des Accents](#le-remappage-automatique-des-accents)
5. [Opcodes et Bytecode Atlus](#opcodes-et-bytecode-atlus)
6. [Structure Modulaire du Code Source](#structure-modulaire-du-code-source)

---

## La Stack Technique (V2)

L'outil de romhacking a été restructuré en une application web locale performante, asynchrone et modulaire.

**Technologies employées :**
- **Backend :** [![Python](https://img.shields.io/badge/Python-3670A0?style=flat-square&logo=python&logoColor=white)](#) [![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)](#) L'API se charge de la décompression, de l'analyse (parsing) et de la recompilation de l'ISO en manipulant directement les flux hexadécimaux.
- **Frontend :** [![React](https://img.shields.io/badge/React-20232A?style=flat-square&logo=react&logoColor=61DAFB)](#) Une interface utilisateur réactive fournissant des retours visuels en temps réel.
- **Déploiement Automatisé :** L'application est orchestrée via le fichier `start.bat` qui installe de façon autonome les dépendances nécessaires (Node.js et Python).

### Dépendance Externe : CriFsLib
L'extraction de l'archive principale du jeu (`P2PT_ALL.cpk`, environ 800 Mo) est déléguée à l'exécutable tiers `CriFsLib.GUI.exe` (développé par Sewer56). Ce choix garantit une extraction rapide et sécurisée du système de fichiers propriétaire de CRI Middleware.

---

## Architecture et Pipeline de Compilation

Le traitement automatisé de l'ISO s'articule autour de quatre phases :

1. **Extraction :**
   - Isolement du fichier `P2PT_ALL.cpk` depuis l'ISO originale.
   - Appel à CriFsLib pour dépaqueter l'archive.
   - Décompression LZSS (algorithme `CRILAYLA`) des fichiers vitaux tels que `event.bin`.
   - Découpage séquentiel des scripts (`script_000.bin` à `script_398.bin`).
2. **Décodage (Parsing) :**
   - L'API analyse le bytecode propriétaire d'Atlus et sépare les opcodes du texte original.
   - Génération de fichiers `.json` clairs et normalisés destinés à la traduction.
3. **Encodage (Injection) :**
   - Lecture et validation des données JSON traduites.
   - Application du remappage des accents français vers les ID VRAM.
   - **Recalcul dynamique des tables de pointeurs absolus** afin d'accommoder les variations de longueur de texte.
   - Génération des nouveaux fichiers binaires modifiés.
4. **Rebuild (Compilation ISO) :**
   - Recompression LZSS des nouveaux scripts.
   - Réinjection dans le CPK et actualisation stricte de la TOC (Table Of Contents).
   - Patch LBA (Logical Block Addressing) de l'ISO 9660 : déplacement des secteurs de l'archive modifiée à la fin de l'image disque.

---

## Gestion Mémoire et Algorithme du Delta

Le moteur de jeu Atlus gère la mémoire différemment selon le type de fichier, imposant des contraintes d'injection spécifiques.

| Fichier | Gestion des Pointeurs | Contrainte Technique Majeure |
|---------|-----------------------|------------------------------|
| **`event.bin`** | Table d'Offsets Absolus (En-tête) | Le moindre décalage provoque un crash. Le script reconstruit la table entière. |
| **`F_BE.BNP`** | Scanner Séquentiel (Moteur de Combat) | L'ajout d'octets de padding (remplissage `00`) provoque le "Crash Philémon" (Invalid Memory Access). L'Algorithme du Delta est utilisé pour compacter l'espace binaire de manière séquentielle et sans padding. |

---

## Le Remappage Automatique des Accents

Atlus utilise un encodage Shift-JIS personnalisé. L'UTF-8 standard n'est pas interprété par le jeu.
Pour permettre l'affichage des caractères français (`é, à, ç, etc.`), des caractères asiatiques inutilisés ont été écrasés graphiquement dans les textures de la police (VRAM) du jeu.

Le fonctionnement est transparent pour l'utilisateur : le dictionnaire `ACCENT_MAP` défini dans `src/config.py` se charge de la substitution en amont. L'encodeur Python identifie la lettre française dans le JSON et injecte l'hexadécimal du caractère VRAM correspondant dans le fichier final.

---

## Opcodes et Bytecode Atlus

Le moteur lit des opcodes de contrôle spécifiques que l'outil de parsing convertit en balises textuelles (`[TAG]`) pour les protéger lors de la traduction :

| Opcode Hex (Little Endian) | Tag Python | Fonction In-Game |
|----------------------------|------------|------------------|
| `00 22` | `[START]` | Initialise une nouvelle chaîne de caractères en mémoire. |
| `11 07` | `[END]` | Termine la chaîne et réinitialise le buffer d'affichage. |
| `11 01` | `[NL]` | Applique un retour à la ligne. |
| `12 08` | `[CHOICE]` | Affiche les options d'un menu contextuel. |
| `14 31` | `[ANIM]` | Déclenche un événement lié à l'animation ou à l'UI (ex. visages). |
| `02 11` | `[WAIT]` | Instruction de pause (historiquement responsable de crashs si mal positionnée). |

---

## Structure Modulaire du Code Source

Le backend Python localisé dans `p2is_tool/src/` suit une séparation stricte des responsabilités :

- **`core/iso.py`** : Manipulation directe de l'ISO 9660, extraction des secteurs et patching LBA.
- **`core/text.py`** : Moteur de conversion String ↔ Shift-JIS Atlus et intégration de `ACCENT_MAP`.
- **`core/compression.py`** : Logique bas niveau des algorithmes de (dé)compression LZSS propriétaire `CRILAYLA`.
- **`parsers/`** : Scripts spécialisés dans l'heuristique de détection de texte (ex. `bin_parser.py`, `fbe_parser.py`).
- **`encoders/`** : Logique d'assemblage binaire, de reconstruction des tables de pointeurs et d'application de l'Algorithme du Delta.

<div align="center">
  
# Guide Développeur & Reverse Engineering
  
**Persona 2: Innocent Sin FR (PSP)**

[![Statut](https://img.shields.io/badge/Statut-Documentation-orange?style=flat-square)](#)
[![Reverse Engineering](https://img.shields.io/badge/Reverse%20Engineering-Atlus%20%2F%20CRI-blue?style=flat-square)](#)

</div>

<br/>

> [!NOTE]
> Bienvenue dans la "Bible" technique du projet. Ce document s'adresse aux développeurs, programmeurs et romhackers. Il recense l'intégralité des connaissances acquises sur le moteur Atlus, les archives CRI Middleware, et documente l'architecture de notre outil de compilation maison (`p2is_tool`).

---

## 📑 Sommaire
1. [La Stack Technique (V2)](#la-stack-technique-v2)
2. [Architecture et Pipeline de Compilation](#architecture-et-pipeline-de-compilation)
3. [Gestion Mémoire et Algorithme du Delta](#gestion-mémoire-et-algorithme-du-delta)
4. [Le Remappage Automatique des Accents](#le-remappage-automatique-des-accents)
5. [Opcodes et Bytecode Atlus](#opcodes-et-bytecode-atlus)
6. [Structure Modulaire du Code Source](#structure-modulaire-du-code-source)

---

## 🚀 La Stack Technique (V2)

L'outil centralisant toutes les étapes du romhacking a été modernisé pour devenir une véritable application web locale robuste et asynchrone, abandonnant le vieux script monolithique.

**Technologies utilisées :**
- **Backend :** [![Python](https://img.shields.io/badge/Python-3670A0?style=flat-square&logo=python&logoColor=white)](#) [![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)](#) L'API ultra-rapide qui décompresse, parse, et recompile l'ISO en manipulant les pointeurs hexadécimaux.
- **Frontend :** [![React](https://img.shields.io/badge/React-20232A?style=flat-square&logo=react&logoColor=61DAFB)](#) [![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black)](#) Une interface moderne et fluide offrant des logs en temps réel.
- **Déploiement Automatisé :** L'outil se lance via un simple `start.bat` qui gère silencieusement l'installation des dépendances (Node.js/Python) pour offrir une expérience Plug & Play à l'utilisateur final.

---

## ⚙️ Architecture et Pipeline de Compilation

Le traitement complet de l'ISO s'effectue en 4 grandes étapes orchestrées par l'outil :

1. **Extraction (Unpacking) :**
   - Extraction de `P2PT_ALL.cpk` depuis l'ISO.
   - Appel transparent à l'exécutable tiers `CriFsLib.GUI.exe` (par Sewer56) pour unpacker le CPK instantanément.
   - Décompression LZSS (algorithme propriétaire `CRILAYLA`) des fichiers vitaux comme `event.bin`.
2. **Décodage (Parsing) :**
   - L'API scanne le bytecode propriétaire d'Atlus et isole le texte japonais/anglais.
   - Génération de fichiers de traduction `.json` structurés et sérialisés.
3. **Encodage (Injection) :**
   - Lecture des traductions françaises depuis les JSON.
   - L'API **recalcule intégralement les tables de pointeurs absolus** des fichiers modifiés (le français étant plus lourd en octets).
   - Re-génération des binaires patchés.
4. **Rebuild (Compilation ISO) :**
   - Compression LZSS des nouveaux scripts.
   - Injection dans le CPK et mise à jour de sa TOC (Table of Contents).
   - Patch LBA de l'ISO : L'archive a grossi, l'outil déplace intelligemment ses secteurs LBA à la fin de l'ISO 9660.

---

## 🧠 Gestion Mémoire et Algorithme du Delta

La plus grande contrainte du moteur est la disparité de gestion de la mémoire entre les fichiers.

| Fichier | Gestion des Pointeurs | Contrainte Technique Majeure |
|---------|-----------------------|------------------------------|
| **`event.bin`** | Table d'Offsets Absolus en Header | Exige la recréation parfaite du Header. Réussi. |
| **`F_BE.BNP`** | Scanner Séquentiel (Battle Engine) | **Le "Crash Philémon"**. L'ajout d'octets de padding (`00`) fait crasher l'interpréteur de scripts de combat. La solution réside dans l'Algorithme du Delta : tout compacter au bit près et décaler les adresses. |

---

## 🔠 Le Remappage Automatique des Accents

L'UTF-8 ou UTF-16 natif n'est pas supporté par le jeu. Atlus utilise un Shift-JIS customisé. 
Pour introduire les accents français (`é, à, ç...`), nous avons modifié graphiquement la texture de la VRAM en écrasant des caractères asiatiques inutilisés.

La magie opère dans `src/config.py` via `ACCENT_MAP`. L'encodeur Python va parser la chaîne française du traducteur, intercepter chaque accent, et le remplacer par l'hexadécimal du "faux" caractère japonais correspondant. 
**Résultat :** Les traducteurs tapent normalement, et le jeu affiche un français irréprochable.

---

## 🧬 Opcodes et Bytecode Atlus

L'interpréteur du jeu repose sur des opcodes de contrôle. L'outil les sanitarise sous forme de Tags textuels `[TAG]` :

| Opcode Hex (Little Endian) | Tag Python | Effet Moteur |
|----------------------------|------------|--------------|
| `00 22` | `[START]` | Alloue la mémoire pour une nouvelle string. |
| `11 07` | `[END]` | Vide le buffer d'affichage (Terminateur). |
| `11 01` | `[NL]` | Force un retour à la ligne strict. |
| `14 31` | `[ANIM]` | Déclenche un appel de fonction (Visage, Sprite, Script visuel). |

---

## 📂 Structure Modulaire du Code Source

Le backend (`p2is_tool/src/`) est strictement organisé :
- **`core/iso.py`** : Les algorithmes de manipulation de l'ISO 9660 et du patching LBA.
- **`core/text.py`** : Le moteur de conversion String ↔ Shift-JIS Atlus et le dictionnaire `ACCENT_MAP`.
- **`core/compression.py`** : Algorithmique bas niveau pour le LZSS `CRILAYLA`.
- **`parsers/`** : Les heuristiques de détection de texte (ex: `bin_parser.py`, `fbe_parser.py`).
- **`encoders/`** : Le nerf de la guerre. Les scripts qui reconstruisent les tables de pointeurs (`bin_encoder.py`).

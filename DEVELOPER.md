<div align="center">
  
# Guide Développeur & Base de Connaissances
  
**Persona 2: Innocent Sin FR (PSP)**

<br/>

[![Statut](https://img.shields.io/badge/Statut-Documentation_Technique-0366d6?style=for-the-badge)](#)
[![Reverse Engineering](https://img.shields.io/badge/Reverse_Engineering-Atlus_%2F_CRI-d73a49?style=for-the-badge)](#)

</div>

<br/>

> [!NOTE]
> Bienvenue dans la documentation technique exhaustive du projet. Ce document s'adresse aux développeurs, programmeurs et romhackers. Il détaille l'architecture de notre outil de compilation maison (`p2is_tool`), les spécificités du moteur Atlus et le fonctionnement des archives CRI Middleware.

<br/>

---

## Sommaire
1. [La Stack Technique (V2)](#la-stack-technique-v2)
2. [Architecture et Pipeline de Compilation](#architecture-et-pipeline-de-compilation)
3. [Gestion Mémoire et Algorithme du Delta](#gestion-mémoire-et-algorithme-du-delta)
4. [Opcodes et Bytecode Atlus](#opcodes-et-bytecode-atlus)
5. [Structure Modulaire du Code Source](#structure-modulaire-du-code-source)

<br/>

---

## La Stack Technique (V2)

L'outil de romhacking a été restructuré en une application web locale performante, asynchrone et modulaire.

<div align="left">
  <img src="https://img.shields.io/badge/Backend-FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/Langage-Python-3670A0?style=flat-square&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Frontend-React-20232A?style=flat-square&logo=react&logoColor=61DAFB" />
</div>

<br/>

* ✦ **Backend :** L'API se charge de la décompression, de l'analyse (parsing) et de la recompilation de l'ISO en manipulant directement les flux hexadécimaux.
* ✦ **Frontend :** Une interface utilisateur réactive fournissant des retours visuels en temps réel.
* ✦ **Déploiement Automatisé :** L'application est orchestrée via le fichier `start.bat` qui installe de façon autonome les dépendances nécessaires.

**Dépendance Externe : CriFsLib**<br/>
L'extraction de l'archive principale du jeu (`P2PT_ALL.cpk`, environ 800 Mo) est déléguée à l'exécutable tiers `CriFsLib.GUI.exe` (développé par Sewer56). Ce choix garantit une extraction rapide et sécurisée du système de fichiers propriétaire de CRI Middleware.

<br/>

---

## Architecture et Pipeline de Compilation

Le traitement automatisé de l'ISO s'articule autour de quatre phases :

<details>
<summary><b>► 1. Extraction</b></summary>
<ul>
<li>Isolement du fichier <code>P2PT_ALL.cpk</code> depuis l'ISO originale.</li>
<li>Appel à CriFsLib pour dépaqueter l'archive.</li>
<li>Décompression LZSS (algorithme <code>CRILAYLA</code>) des fichiers vitaux tels que <code>event.bin</code>.</li>
<li>Découpage séquentiel des scripts (<code>script_000.bin</code> à <code>script_398.bin</code>).</li>
</ul>
</details>

<details>
<summary><b>► 2. Décodage (Parsing)</b></summary>
<ul>
<li>L'API analyse le bytecode propriétaire d'Atlus et sépare les opcodes du texte original.</li>
<li>Génération de fichiers <code>.json</code> clairs et normalisés destinés à la traduction.</li>
</ul>
</details>

<details>
<summary><b>► 3. Encodage (Injection)</b></summary>
<ul>
<li>Lecture et validation des données JSON traduites.</li>
<li>Application du remappage des accents français vers les ID VRAM.</li>
<li><b>Recalcul dynamique des tables de pointeurs absolus</b> afin d'accommoder les variations de longueur de texte.</li>
<li>Génération des nouveaux fichiers binaires modifiés.</li>
</ul>
</details>

<details>
<summary><b>► 4. Rebuild (Compilation ISO)</b></summary>
<ul>
<li>Recompression LZSS des nouveaux scripts.</li>
<li>Réinjection dans le CPK et actualisation stricte de la TOC (Table Of Contents).</li>
<li>Patch LBA (Logical Block Addressing) de l'ISO 9660 : déplacement des secteurs de l'archive modifiée à la fin de l'image disque.</li>
</ul>
</details>

<br/>

---

## Gestion Mémoire et Algorithme du Delta

Le moteur de jeu Atlus gère la mémoire différemment selon le type de fichier, imposant des contraintes d'injection drastiques.

| Fichier Cible | Gestion des Pointeurs | Contrainte Technique Majeure |
|:---|:---|:---|
| **`event.bin`** | Table d'Offsets Absolus | Le moindre décalage provoque un crash immédiat. Le script reconstruit la table entière (offsets absolus et longueurs) à chaque compilation. |
| **`F_BE.BNP`** | Scanner Séquentiel (Combat) | L'ajout d'octets de padding (remplissage `00`) provoque un Invalid Memory Access (Crash Philémon). **L'Algorithme du Delta** est utilisé pour compacter l'espace binaire de manière purement séquentielle. |

<br/>

---

## Opcodes et Bytecode Atlus

Le moteur lit des opcodes de contrôle spécifiques que l'outil de parsing convertit en balises textuelles (`[TAG]`) pour les protéger lors de la traduction :

| Opcode Hex (Little Endian) | Tag Python | Fonction In-Game |
|:---:|:---:|:---|
| `00 22` | `[START]` | Initialise une nouvelle chaîne de caractères en mémoire. |
| `11 07` | `[END]` | Termine la chaîne et réinitialise le buffer d'affichage. |
| `11 01` | `[NL]` | Applique un retour à la ligne. |
| `12 08` | `[CHOICE]` | Affiche les options d'un menu contextuel. |
| `14 31` | `[ANIM]` | Déclenche un événement lié à l'animation ou à l'UI (ex. visages). |
| `02 11` | `[WAIT]` | Instruction de pause (historiquement responsable de crashs si mal positionnée). |

<br/>

---

## Structure Modulaire du Code Source

Le backend Python localisé dans `p2is_tool/src/` suit une séparation stricte des responsabilités :

* ✦ **`core/iso.py`** : Manipulation directe de l'ISO 9660, extraction des secteurs et patching LBA.
* ✦ **`core/text.py`** : Moteur de conversion String ↔ Shift-JIS Atlus et intégration de la table `ACCENT_MAP`.
* ✦ **`core/compression.py`** : Logique bas niveau des algorithmes de décompression LZSS propriétaire `CRILAYLA`.
* ✦ **`parsers/`** : Scripts spécialisés dans l'heuristique de détection de texte (ex. `bin_parser.py`).
* ✦ **`encoders/`** : Logique d'assemblage binaire, de reconstruction des tables de pointeurs et d'application de l'Algorithme du Delta.

<!-- updated -->

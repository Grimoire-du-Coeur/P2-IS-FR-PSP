<div align="center">
  
# Guide Développeur & Base de Connaissances
  
**Persona 2: Innocent Sin FR (PSP)**

[![React](https://img.shields.io/badge/React-20232A?style=flat-square&logo=react&logoColor=61DAFB)](#)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)](#)
[![Python](https://img.shields.io/badge/Python-3670A0?style=flat-square&logo=python&logoColor=white)](#)
[![Reverse Engineering](https://img.shields.io/badge/Reverse%20Engineering-Atlus%20%2F%20CRI-blue?style=flat-square)](#)

</div>

<br/>

> [!NOTE]
> Bienvenue dans la "Bible" technique du projet de traduction française de *Persona 2: Innocent Sin* (ULES01557). Ce document s'adresse aux développeurs et romhackers souhaitant reprendre, modifier ou étudier le projet. 
> Il recense l'intégralité des connaissances acquises sur le moteur de jeu Atlus, les archives CRI Middleware, la structure de l'ISO, ainsi qu'une présentation complète du nouvel outil modulaire `p2is_tool`.

---

## Sommaire
1. [Vue d'Ensemble & Architecture (V2)](#vue-densemble--architecture-v2)
2. [Statistiques du Code](#statistiques-du-code)
3. [La Pipeline Complète](#la-pipeline-complète)
4. [Table des Offsets & Gestion Mémoire](#table-des-offsets--gestion-mémoire)
5. [Structure et Contraintes des Menus](#structure-et-contraintes-des-menus)
6. [Encodage des Textes et Accents](#encodage-des-textes-et-accents)
7. [Dictionnaire des Opcodes et Symboles](#dictionnaire-des-opcodes-et-symboles)
8. [Glossaire des Fonctions Modulaires](#glossaire-des-fonctions-modulaires)

---

## Vue d'Ensemble & Architecture (V2)

L'outil a été modernisé et centralise toutes les étapes du romhacking via une application web locale très simple d'utilisation pour l'utilisateur final.

L'outil se lance simplement avec un `start.bat` qui donne confiance à l'utilisateur : il n'y a rien à installer manuellement, le `.bat` vérifie et télécharge automatiquement les modules Python et Node.js requis, puis lance le serveur et ouvre l'interface dans le navigateur.

**Les technologies de la V2 :**
1. **Frontend (React/Vite) :** L'interface utilisateur est désormais une application web moderne. Les appels sont asynchrones et ne bloquent pas l'UI.
2. **Backend (FastAPI) :** Le moteur de romhacking est une API Python rapide et robuste.
3. **Code Modulaire :** Le code Python n'est plus un énorme fichier monolithique, mais est proprement rangé dans `src/core`, `src/parsers`, et `src/encoders`.

### Dépendance Externe : CriFsLib
Pour extraire les fichiers contenus dans `P2PT_ALL.cpk` (~800 Mo), l'outil s'appuie sur `CriFsLib.GUI.exe` développé par Sewer56, ce qui garantit une extraction ultra-rapide et sans corruption du système de fichiers propriétaire de CRI Middleware.

---

## Statistiques du Code

Voici la répartition en direct des langages utilisés pour coder cet outil de traduction (React, Python, etc.) :

<div align="center">
  <a href="https://github.com/chenetulipe/P2-FR-IS-PSP">
    <img src="https://github-readme-stats.vercel.app/api/top-langs/?username=chenetulipe&repo=P2-FR-IS-PSP&layout=compact&theme=dark" alt="Top Languages" />
  </a>
</div>

---

## La Pipeline Complète

Le processus de traduction s'articule autour de 4 grandes étapes automatisées :

```text
ISO Originale (ULES01557)
    │
[ 1. Extraction ]
    ├── Extraction du P2PT_ALL.cpk depuis l'ISO.
    ├── Appel à CriFsLib pour unpacker l'archive.
    ├── Décompression interne CRILAYLA de event.bin.
    └── Découpage en sous-scripts (script_000.bin ➔ script_398.bin).
    │
[ 2. Décodage (Parsing) ]
    ├── Analyse hexadécimale de chaque script.
    ├── Séparation des opcodes Atlus et du texte anglais.
    └── Génération de dizaines de fichiers JSON propres pour les traducteurs.
    │
[ 3. Encodage (Injection) ]
    ├── L'outil lit les JSON traduits.
    ├── Les accents français sont remplacés par les glyphes de la VRAM (é, à, ç, etc).
    ├── Recalcul de l'intégralité des pointeurs absolus (car le FR est plus long).
    └── Génération de nouveaux fichiers binaires (script_XXX_fr.bin, F_BE.bnp).
    │
[ 4. Rebuild ISO ]
    ├── Compression CRILAYLA des nouveaux fichiers.
    ├── Réinjection de event.bin et F_BE dans l'ISO.
    ├── Mise à jour de la TOC (Table Of Contents) du CPK.
    └── Génération de "Persona 2 Innocent Sin FR.iso" prête à jouer !
```

---

## Table des Offsets & Gestion Mémoire

Selon le fichier, la modification de la taille du texte a des conséquences techniques différentes :

| Fichier | Type de Pointeurs | Conséquence | Solution Technique Appliquée |
|---------|-------------------|-------------|------------------------------|
| **`event.bin`** | Absolus (Header) | Crash si un texte change de taille. | L'outil reconstruit **intégralement** la table des pointeurs lors de l'encodage. |
| **`MMAPxx.BNP`** | Absolus (Header) | Écran noir sur les cartes 3D. | Nécessite un recalibrage spécifique des headers LBA internes. |
| **`F_BE.BNP`** | Séquentiel | "Crash Philémon" en plein combat. | Les scripts de combat (F_BE) sont encodés via un "Algorithme du Delta" pour éviter les octets de padding mortels. |

---

## Structure et Contraintes des Menus

Les menus sont très sensibles dans le jeu. L'outil gère automatiquement de nombreuses contraintes pour faciliter la vie des traducteurs :

1. **JSON structuré :** L'outil sépare l'intro et les choix (`question_fr` et `choix_fr`) dans le JSON.
2. **Terminaison (`11 01`) :** Le jeu crash si un menu ne se termine pas par un `NL` (New Line). L'outil l'ajoute silencieusement s'il manque.
3. **Alignement des pointeurs internes :** Les choix utilisent des offsets internes au bloc de texte. L'outil injecte des espaces invisibles (`[SP]`) si la question française est plus courte, afin de maintenir l'alignement binaire parfait exigé par Atlus.

---

## Encodage des Textes et Accents

Pour afficher les accents français (é, à, ç, É, etc.), il a fallu modifier la texture de la police du jeu (VRAM). Comme la taille était fixe, des caractères originaux (souvent des symboles ou des caractères inusités) ont été remplacés graphiquement.

**Mappage automatique :** 
Le dictionnaire `ACCENT_MAP` (dans `src/config.py`) se charge de la conversion : l'encodeur convertit automatiquement la lettre tapée par le traducteur (ex: `é`) vers l'identifiant hexadécimal de son remplaçant dans la VRAM du jeu.
Cela concerne un grand nombre de caractères : **à, â, ç, é, è, ê, ë, î, ï, ô, ù, û**, ainsi que leurs versions majuscules. Le traducteur n'a donc pas besoin de taper des codes étranges, l'outil gère tout nativement.

---

## Dictionnaire des Opcodes et Symboles

L'outil gère (et protège dans les JSON) une multitude de balises hexadécimales de contrôle utilisées par le jeu. Voici les principales :

| Opcode Hex | Tag Outil | Fonction In-Game |
|------------|-----------|------------------|
| `00 22` | `[START]` | Marque le début d'un dialogue. |
| `11 07` | `[END]` | Terminateur de chaîne standard. |
| `11 01` | `[NL]` | New Line (Retour à la ligne). |
| `12 08` | `[CHOICE]` | Affiche les choix d'un menu. |
| `14 31` | `[ANIM / EVENT]` | Balise d'événement (visages, animations). Très utilisée dans le Battle Engine. |
| `11 13` | `[1113]` / `[1112]` | Affiche le Nom / Prénom du Héros. |

---

## Glossaire des Fonctions Modulaires

Avec la V2, le backend a été proprement découpé. Voici où trouver les fonctions clés si vous souhaitez modifier l'outil :

**1. `src/core/iso.py` :**
Gère tout ce qui touche à l'ISO et au CPK.
- `extract_cpk_from_iso()` : Récupère l'archive du jeu.
- `rebuild_iso()` : Réinjecte le CPK modifié avec correction LBA.

**2. `src/core/text.py` :**
Moteur de conversion binaire <-> texte.
- `decode_text()` : Transforme l'hexa en texte lisible avec tags.
- `text_to_bytes()` : Convertit le texte FR en Shift-JIS Atlus (avec le dictionnaire des accents).

**3. `src/core/compression.py` :**
- `crilayla_decompress()` et `crilayla_compress()` : Algorithmes de (dé)compression LZSS propriétaires à CRI Middleware.

**4. `src/parsers/` (Extraction) :**
- `bin_parser.py` : Scanne les fichiers histoire (`event.bin`) pour en extraire les textes et générer les JSON.
- `fbe_parser.py` : Algorithme sur-mesure pour extraire les textes de combat qui n'ont aucune table de pointeurs.

**5. `src/encoders/` (Injection) :**
- `bin_encoder.py` : Lit les traductions JSON, reconstruit la table des pointeurs absolue, et génère le fichier binaire.
- `fbe_encoder.py` : Ré-encode les combats (Battle Engine) en évitant les crashs Philémon.
- `pipeline.py` : Orchestre tout le processus d'encodage par lots.


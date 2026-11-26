---
tags: [accueil, index]
---

# Accueil : le cerveau du projet

Point d'entrée de la documentation. Le dépôt s'ouvre tel quel comme **coffre Obsidian**
(*Ouvrir un dossier comme coffre* → la racine du dépôt) : les liens ci-dessous marchent
dans Obsidian comme sur GitHub, et la vue graphe relie toutes les notes. Le dossier
`.obsidian/` (réglages perso) n'est pas versionné.

## Par où commencer

| Je veux... | Note |
|:---|:---|
| Installer le patch | [README](../README.md) |
| Traduire ou relire | [Guide de contribution](../CONTRIBUTING.md) |
| Vérifier un nom, un terme | [Dictionnaire](Dictionnaire.md) |
| Savoir ce qui a changé | [Journal des versions](SUIVI.md) |
| Comprendre les formats du jeu | [Guide développeur](DEVELOPER.md) |
| Voir qui a fait quoi | [Crédits](CREDITS.md) |
| Relire l'audit d'octobre 2026 | [Analyse du dépôt](ANALYSE.md) *(archive)* |

## Les fichiers du jeu, en bref

| Fichier | Contenu | Traduction (`traduction/`) |
|:---|:---|:---|
| `event.bin` | Scripts de l'histoire | `event_scripts/`, `event_blocs.json` |
| `MMAP01` à `06` | PNJ des cartes | `MMAP0X.json` |
| `DNGSCN.BNP` | PNJ du lycée et des donjons | `DNGSCN.json` |
| `P_DEMO.BNP` | Démonstrations | `P_DEMO.json` |
| `F_BE.BNP` | Répliques de combat | `F_BE.json` |
| `TM_EVE.BNP` | Réponses des démons (Contacts) | `TM_EVE.json` |
| `CD_SHOP.BNP` | Boutique de CD | `CD_SHOP.json` |
| `EBOOT.BIN` | Menus, noms, descriptions | `EBOOT_decoupe/` |
| `q00.bin` | Climax Theater | `climax_theater/` *(prévu avec les DLC)* |

## Pistes ouvertes

- **Accents sur vraie PSP** (issue #569) : la police d'origine (`syscg.bin`) n'a pas
  de lettres accentuées. Il faut les dessiner dans des codes libres de la police, puis
  les déclarer dans la table de caractères et les tables de largeurs de l'EBOOT, pour
  se passer du Pack HD.
- **Cinématiques** : les `.pmf` ne sont pas encore sous-titrées.
- **Musique** : certaines pistes de `BGMALL.BIN` existent en double (une copie par
  mode Musique Original / Remix). L'Audio Lab remplace les copies identiques ensemble ;
  l'ouverture a deux versions différentes (pistes 3 et 147), à remplacer toutes les deux.

## Règles à ne jamais oublier

- **Jamais plus long que l'original** dans `EBOOT.BIN`, `F_BE` et `TM_EVE` : le jeu plante.
  Voir [la contrainte de longueur](../CONTRIBUTING.md#la-contrainte-critique-de-longueur).
- **Les accents ne s'affichent qu'avec le Pack HD** (PPSSPP). Sur vraie PSP, la police
  d'origine n'a pas de glyphes accentués.
- **Les noms suivent le [Dictionnaire](Dictionnaire.md)**, sans exception.
- Avant une PR : `py -m pytest -q`, `py -m ruff check p2is labs tests`,
  `py -m p2is.outils.verify_json`.

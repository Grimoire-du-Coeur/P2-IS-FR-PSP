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

- **Accents sur vraie PSP** (issue #569) : la traduction espagnole
  ([AlexEn64bits](https://alexen64bits.com/traduccion-persona-2-innocent-sin.html),
  même ISO `ULES01557`) a dessiné ses lettres accentuées dans des codes libres de la
  police `syscg.bin`, puis les a ajoutées à la table de caractères et aux deux tables
  de largeurs de l'EBOOT. Pas de majuscules accentuées. C'est la voie à suivre pour
  se passer du Pack HD.
- **Cinématiques** : la même équipe a ré-encodé les `.pmf` en H.264 avec sous-titres
  incrustés, en gardant l'audio ATRAC tel quel (5 vidéos sous-titrées sur 19).
  Leurs outils ne sont pas publiés.
- **Musique d'ouverture** (issue #505) : la piste 147 de `BGMALL.BIN` n'est partagée
  avec aucune autre. Si la remplacer ne change rien, l'ouverture joue sans doute le son
  de la vidéo, pas BGMALL.

## Règles à ne jamais oublier

- **Jamais plus long que l'original** dans `EBOOT.BIN`, `F_BE` et `TM_EVE` : le jeu plante.
  Voir [la contrainte de longueur](../CONTRIBUTING.md#la-contrainte-critique-de-longueur).
- **Les accents ne s'affichent qu'avec le Pack HD** (PPSSPP). Sur vraie PSP, la police
  d'origine n'a pas de glyphes accentués.
- **Les noms suivent le [Dictionnaire](Dictionnaire.md)**, sans exception.
- Avant une PR : `py -m pytest -q`, `py -m ruff check p2is labs tests`,
  `py -m p2is.outils.verify_json`.

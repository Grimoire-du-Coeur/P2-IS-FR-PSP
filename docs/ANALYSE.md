# Analyse du dépôt — 27 octobre 2026

> ## État au 31 octobre 2026
>
> **§1 Rangement — fait**, sauf un point. Le paquet `p2is/` existe, les trois
> copies de l'outil CPK sont ramenées à une (les deux `p2is_cpk_tool.py`
> étaient identiques à 100 % hors CLI), `config.py` est coupé en `p2is/tables.py`
> et `labs/tool/ui_config.py`, les `dist/` sont sortis de Git. **Reste**
> `p2is/core/cpk_image.py` : cette troisième copie a réellement divergé (36 à
> 81 % de lignes communes selon la fonction), la fondre demande un aller-retour
> sur un vrai CPK, pas une relecture.
>
> **Deux points de §1.1 n'étaient pas des doublons** : les deux `iso_builder.py`
> font deux métiers différents sous le même nom (renommés `iso_images.py` et
> `iso_audio.py`), et l'`index.html` de la racine est la redirection GitHub
> Pages, pas une copie du patcher.
>
> **§2 Ce qu'il reste à traduire — périmé.** Plus aucune entrée vide : 19 772
> entrées, 92,7 % traduites, 7,3 % identiques à l'anglais (dont les noms propres).
>
> **§3 Bugs — toujours ouvert**, et plus large que décrit : 667 entrées de
> `EBOOT_decoupe/` sur 6 574 perdent une balise, terminateurs `<0004>` et
> `<FF03>` compris, depuis la traduction intégrale du 28/10.

État des lieux avant la passe de rangement et de finition. Trois volets indépendants :
**le rangement**, **ce qu'il reste à traduire**, **les bugs trouvés**.

Tout ce qui suit est mesuré sur le dépôt, pas estimé. Les scripts d'analyse sont
reproductibles.

---

## 1. Rangement

### 1.1 Trois copies divergentes de l'outil CPK

| Chemin | Lignes | Empreinte |
|---|---|---|
| `p2is/core/cpk.py` *(racine)* | 710 | `17f1b6f8` |
| `p2is/core/cpk.py` | 708 | `6aef2822` |
| `p2is/core/cpk_image.py` | 662 | `18d7d97c` |

Les trois ont **divergé**. C'est le problème le plus coûteux du dépôt : un bug corrigé
dans l'une des copies reste vivant dans les deux autres, et personne ne sait laquelle
fait foi.

Autres doublons du même genre :

- `iso_builder.py` — dans `labs/audio/server/core/` **et** `labs/image/server/core/`
- `logger.py` — idem
- `check_overflows.py` (31 lignes) vs `p2is/outils/check_real_overflows.py` (39 lignes)
- `index.html` à la racine **et** `patcher/index.html`

### 1.2 2,6 Mo d'artefacts de build versionnés

28 fichiers compilés sont dans Git, dont des `dist/` **imbriqués trois fois** :

```text
labs/tool/server/dist/
labs/tool/server/dist/dist/
labs/tool/server/dist/dist/dist/assets/index-glxgM1IZ.js
```

Chaque compilation a été copiée dans le dossier de la précédente. `labs/audio` et
`labs/tool` traînent chacun **3 bundles JS différents**, soit des builds périmés que
plus rien ne sert.

Cause : `.gitignore` couvre `node_modules/` et `__pycache__/` mais **pas `dist/`**.

### 1.3 La documentation ne décrit pas l'arborescence réelle

`DEVELOPER.md` parle de `p2is/parsers/` et `p2is/encoders/`. Le vrai chemin est
`p2is/parsers/`. Quelqu'un qui suit la doc ne trouve rien.

### 1.4 `.gitignore` partiellement périmé

Il ignore `AutreScript/prompts_gemini/`, `json_verify/` et `p2is/outils/harmonize_*.py` —
aucun n'existe plus. Et il ignore `*.bin` et `*.dat` largement : si un fichier de
données légitime doit un jour être versionné, il sera silencieusement ignoré.

### 1.5 Rangement proposé

L'idée directrice : **une seule copie de chaque outil**, un noyau partagé, et les trois
labos qui s'appuient dessus au lieu de se recopier.

```text
P2-IS-FR-PSP/
├── docs/                  README, DEVELOPER, CONTRIBUTING, Dictionnaire, CREDITS, SUIVI
├── traduction/            inchangé — c'est la partie saine du dépôt
│   ├── event_scripts/     399 fichiers
│   └── EBOOT_decoupe/     7 fichiers
├── p2is/                  LE paquet Python, une seule fois
│   ├── core/              compression, iso, text, cpk  <- la copie unique de CPK
│   ├── parsers/           bin, eboot, fbe
│   ├── encoders/          bin, fbe, mmap, pipeline
│   └── outils/            auto_wrap, mmap_fixer, check_overflows, decrypt_eboot
├── labs/
│   ├── audio/             ne garde que son code propre
│   ├── image/
│   └── tool/
├── patcher/               index.html, xdelta3.*
└── .gitignore             + dist/, build/, *.egg-info
```

Déplacements concrets, dans l'ordre où je les ferais :

1. **Choisir la copie CPK de référence** (diff des trois, garder la plus complète),
   la mettre dans `p2is/core/cpk.py`, supprimer les deux autres et corriger les imports.
2. `git rm -r --cached` sur tous les `dist/`, ajouter `dist/` au `.gitignore`.
3. Factoriser `iso_builder.py` et `logger.py` dans `p2is/core/`.
4. Remonter `p2is/` en `p2is/`, puis corriger `DEVELOPER.md`.
5. Déplacer les scripts racine (`p2is/outils/decrypt_eboot.py`, `p2is/core/cpk.py`) dans `p2is/outils/`.
6. Nettoyer les entrées mortes du `.gitignore`.

> Les étapes 1 à 3 se font sans rien casser côté traduction. La 4 touche aux imports,
> à faire d'un bloc avec un test de bout en bout derrière.

---

## 2. Ce qu'il reste à traduire

Mesuré sur les **18 040** entrées de texte du dépôt :

| | Entrées | Part |
|---|---:|---:|
| Traduites | 12 413 | 68,8 % |
| **Vides** | **5 274** | **29,2 %** |
| Restées en anglais (`fr` == `en`) | 353 | 2,0 % |
| **Total à traiter** | **5 627** | **31,2 %** |

**Les 5 274 entrées vides sont toutes dans `EBOOT_decoupe/`**, aucune dans les scripts
d'histoire. C'est cohérent avec le journal : l'histoire est finie depuis juin, c'est le
texte système qui ne l'est pas.

| Fichier | Entrées vides |
|---|---:|
| `EBOOT_Part3.json` | 1 000 |
| `EBOOT_Part6.json` | 966 |
| `EBOOT_Part5.json` | 951 |
| `EBOOT_Part4.json` | 873 |
| `EBOOT_Part2.json` | 805 |
| `EBOOT_Part7.json` | 392 |
| `EBOOT_Part1.json` | 287 |

L'EBOOT, ce sont les menus, noms d'objets, descriptions de compétences et de Personas.
C'est répétitif et très contraint en longueur — donc fastidieux, mais beaucoup plus
mécanique qu'un dialogue.

---

## 3. Bugs trouvés

Règle de `DEVELOPER.md` : *« Ces balises ne doivent jamais être supprimées du texte
traduit. »* 1 007 entrées en perdent au moins une. Mais toutes les balises n'ont pas le
même poids — classées par gravité réelle d'après la table des opcodes :

### 🔴 56 entrées, 17 fichiers — peut casser le jeu

| Balise perdue | Occurrences | Ce que ça fait |
|---|---:|---|
| `[U+070F]` et autres `[U+XXXX]` | 105 | opcodes inconnus conservés **pour l'intégrité du rebuild** |
| `[NULL]` | 41 | décalage de pointeur |
| `[1432]` | 16 | positionnement du curseur de menu |
| `[0014]` | 16 | fin de chaîne d'une option de choix |
| `[E4]` | 5 | terminateur de dialogue |

### 🟠 4 entrées — visible à l'écran

`[1113]` manquant : **le prénom du héros ne s'affiche pas**. Exemple dans
`script_007.json` #16.

### ⚪ 947 entrées — cosmétique

`[1205]`, `[000F]`, `[000A]`, `[001E]` : des pauses de mise en scène. Leur absence
accélère le dialogue, elle ne casse rien. 94 % du total : **à ne pas traiter en
priorité**, et sans doute à accepter tel quel.

### 🔴 Un cas à part : `script_123.json` #12

Le texte français n'a aucun rapport avec l'anglais :

```text
EN : Leave the solo to the great Michel![1208][0005][1432][NULL][0014]...
FR : Mon Papa...[1205][001E] Il est...[1205][001E] C'est pas un bon...
```

Les entrées #8 à #11 du même fichier sont correctes : ce n'est donc pas un décalage
global, mais un copier-coller d'un autre script dans la dernière entrée. Le menu de
choix `[1208]` disparaît au passage. **À corriger en priorité**, c'est une réplique
fausse doublée d'un menu cassé.

---

## 4. Ordre de travail suggéré

1. **`script_123.json` #12** — un seul correctif, effet immédiat.
2. **Les 56 entrées critiques** (17 fichiers) — liste reproductible, chacune se règle en
   remettant les balises manquantes.
3. **Les 4 `[1113]`** — le prénom du héros.
4. **Le rangement**, étapes 1 à 3 (CPK unique, `dist/` sortis de Git) — sans risque.
5. **L'EBOOT**, 5 274 entrées — le gros morceau, à étaler.
6. Le rangement, étapes 4 à 6 (imports), quand le reste est stabilisé.

Les 947 pauses cosmétiques ne figurent volontairement pas dans cette liste.

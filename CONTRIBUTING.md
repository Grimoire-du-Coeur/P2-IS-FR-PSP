<div align="center">

# Guide de Contribution et Relecture

**Persona 2: Innocent Sin FR â€” PSP (ULES01557)**

<br/>

<img src="https://img.shields.io/badge/Statut-Ouvert_aux_contributions-2ea043?style=for-the-badge" alt="Statut" />
<a href="https://discord.gg/rd4ckSWHNm"><img src="https://img.shields.io/discord/1400909421609095323?color=5865F2&label=Discord&logo=discord&logoColor=white&style=flat-square" alt="Discord" /></a>
<a href="https://hamzakarrouchi.github.io/p2is-relecture/"><img src="https://img.shields.io/badge/Outil_de_Relecture-En_Ligne-009688?style=for-the-badge" alt="Outil de Relecture" /></a>

</div>

<br/>

> [!NOTE]
> Bienvenue ! Que tu veuilles aider à traduire, relire des dialogues, ou juste comprendre comment le projet est organisé, tout est ici. On a essayé de tout documenter clairement pour que ce soit accessible même si tu n'as jamais fait de romhacking.

<br/>

---

## Sommaire

1. [Tableau d'Avancement DÃ©taillÃ©](#tableau-davancement-dÃ©taillÃ©)
2. [L'Outil de Relecture en Ligne](#loutil-de-relecture-en-ligne)
3. [Soumettre vos Contributions](#soumettre-vos-contributions)
4. [La Contrainte Critique de Longueur](#la-contrainte-critique-de-longueur)
5. [RÃ¨gles de Traduction et de Style](#rÃ¨gles-de-traduction-et-de-style)
6. [RÃ©fÃ©rence des Balises In-Game](#rÃ©fÃ©rence-des-balises-in-game)

<br/>

---

## Tableau d'Avancement DÃ©taillÃ©

### ScÃ©nario et Dialogues

| Fichier / Composant | Contenu | Progression | Statut |
|:---|:---|:---:|:---|
| `event.bin` | 399 scripts d'histoire | 100% | ![](https://img.shields.io/badge/-TerminÃ©-2ea043?style=flat-square) |
| `MMAP01` Ã  `MMAP06` | Dialogues sur les cartes | 100% | ![](https://img.shields.io/badge/-TerminÃ©-2ea043?style=flat-square) |
| `CD_SHOP.BNP` | Boutique de CD / musique | 100% | ![](https://img.shields.io/badge/-TerminÃ©-2ea043?style=flat-square) |
| `F_BE.BNP` | RÃ©pliques de combat | 100% | ![](https://img.shields.io/badge/-TerminÃ©-2ea043?style=flat-square) |
| `TM_EVE.BNP` | CinÃ©matiques in-game | 100% | ![](https://img.shields.io/badge/-TerminÃ©-2ea043?style=flat-square) |

### EBOOT.BIN â€” Textes SystÃ¨me

Le fichier est dÃ©coupÃ© en 7 parties (~1 000 entrÃ©es chacune) dans le dossier `EBOOT_decoupe/` pour Ã©viter les limitations GitHub.

| Contenu | Fichier | IDs (estimatif) | EntrÃ©es | Progression | Statut |
|:---|:---:|:---:|:---:|:---:|:---:|
| Menus & Interface | Part 1 | 0 â€” 179 | ~180 | **72.2%** | <img src="https://img.shields.io/badge/-En%20cours-0366d6?style=flat-square" alt="En cours" /> |
| Noms de Personnages / PNJs / Boss | Part 1 | 180 â€” 449 | ~270 | **87.4%** | <img src="https://img.shields.io/badge/-AvancÃ©-2ea44f?style=flat-square" alt="AvancÃ©" /> |
| Commandes & Messages de Combat | Part 1 | 600 â€” 899 | ~300 | **79.0%** | <img src="https://img.shields.io/badge/-En%20cours-0366d6?style=flat-square" alt="En cours" /> |
| Noms & Descriptions de Personae / DÃ©mons | Part 2 & 4 | 900 â€” 3999 | ~800 | **28.0%** | <img src="https://img.shields.io/badge/-DÃ©butÃ©-ffa500?style=flat-square" alt="DÃ©butÃ©" /> |
| Noms & Descriptions de CompÃ©tences | Part 2 | 1200 â€” 1599 | ~400 | **0.0%** | <img src="https://img.shields.io/badge/-Ã€%20faire-red?style=flat-square" alt="Ã€ faire" /> |
| Noms d'Armes / Armures / Accessoires | Part 2 & 3 | 1600 â€” 2199 | ~600 | **0.0%** | <img src="https://img.shields.io/badge/-Ã€%20faire-red?style=flat-square" alt="Ã€ faire" /> |
| Objets de quÃªte / Rumeurs / ClÃ©s | Part 3 & 4 | 2800 â€” 3499 | ~700 | **0.0%** | <img src="https://img.shields.io/badge/-Ã€%20faire-red?style=flat-square" alt="Ã€ faire" /> |
| Noms de lieux / Donjons / Carte | Part 5 â€” 7 | 4000 â€” 6500 | ~2501 | **0.1%** | <img src="https://img.shields.io/badge/-DÃ©butÃ©-ffa500?style=flat-square" alt="DÃ©butÃ©" /> |
| Autres textes (Tutoriels, Infos) | Part 1, 2, 7 | 450 â€” 868 | ~177 | **11.9%** | <img src="https://img.shields.io/badge/-DÃ©butÃ©-ffa500?style=flat-square" alt="DÃ©butÃ©" /> |
| **Total EBOOT** | **Part 1 Ã  7** | **0 â€” 6573** | **~5 928** | **14.3%** | |

### Ã‰lÃ©ments Graphiques

| Composant | IntÃ©gration | Accents supportÃ©s | Progression | Statut |
|:---|:---:|:---|:---:|:---|
| Textures HD | Oui | â€” | 35/42 | ![](https://img.shields.io/badge/-En%20cours-0366d6?style=flat-square) |
| Police HD (Accents FR) | Oui | Ã© Ã  Ãª Ã¨ Ã§ Ã® Ã¯ Ã¹ Ã´ + majuscules | 100% | ![](https://img.shields.io/badge/-TerminÃ©%20(Bugs)-e1ad01?style=flat-square) |
| Textures ISO | Non | â€” | 0/42 | ![](https://img.shields.io/badge/-Non%20dÃ©marrÃ©-critical?style=flat-square) |
| Police ISO (Accents FR) | Oui | N/A | 0% | ![](https://img.shields.io/badge/-Non%20dÃ©marrÃ©-critical?style=flat-square) |

<br/>

---

## L'Outil de Relecture en Ligne

Pour Ã©viter que les contributeurs ne manipulent directement les fichiers JSON bruts, une application web dÃ©diÃ©e a Ã©tÃ© dÃ©veloppÃ©e par **@HamzaKarrouchi**.

> [!IMPORTANT]
> **AccÃ©der Ã  l'outil :** [Site de Relecture P2IS FR](https://hamzakarrouchi.github.io/p2is-relecture/)  
> **Le Glossaire Officiel :** [Dictionnaire P2IS FR](https://hamzakarrouchi.github.io/p2is-relecture/dictionnaire.html)

Cet outil est obligatoire pour toute contribution car il :

- Affiche simultanÃ©ment le texte anglais original et votre proposition franÃ§aise
- IntÃ¨gre un compteur dynamique d'octets qui vous alerte si votre texte dÃ©passe la limite du moteur
- VÃ©rifie automatiquement la terminologie par rapport au [Dictionnaire.md](./Dictionnaire.md)
- GÃ©nÃ¨re un bloc de texte prÃªt Ã  Ãªtre soumis sans manipuler de fichiers JSON manuellement

<br/>

---

## Soumettre vos Contributions

Une fois votre travail terminÃ© sur le site de relecture, deux mÃ©thodes pour le soumettre :

**Via Discord (mÃ©thode recommandÃ©e)**

Copiez le bloc gÃ©nÃ©rÃ© par l'outil et collez-le dans le salon `#scripts` sur le [serveur Discord officiel](https://discord.gg/rd4ckSWHNm). Un dÃ©veloppeur prendra en charge l'injection.

**Via GitHub (contributeurs avancÃ©s)**

Forkez ce dÃ©pÃ´t, modifiez les fichiers `.json` concernÃ©s dans le dossier `traduction/`, et ouvrez une Pull Request avec le titre `[Script XXX] Traduction/Relecture`.

<br/>

---

## La Contrainte Critique de Longueur

> [!WARNING]
> Le franÃ§ais est structurellement 20 Ã  30 % plus long que l'anglais. L'architecture mÃ©moire de la PSP est stricte : un dÃ©passement de la taille allouÃ©e provoque un crash `Invalid Memory Access`.

**La rÃ¨gle d'or : la concision.**

PrivilÃ©giez toujours une adaptation naturelle et percutante plutÃ´t qu'une traduction littÃ©rale.

- **Pour l'histoire (`event.bin`)** : L'outil recalcule l'espace dynamiquement, mais l'Ã©cran de la PSP ne grandit pas. Ne dÃ©passez jamais **3 lignes par boÃ®te de dialogue**.
- **Pour les combats et menus (`F_BE.BNP`, `EBOOT.BIN`)** : La contrainte est absolue. Si le texte traduit dÃ©passe le nombre d'octets de l'original, le jeu plantera. L'outil de relecture vous avertit â€” respectez toujours ses limites.

<br/>

---

## RÃ¨gles de Traduction et de Style

### Accents FranÃ§ais

Les accents sont entiÃ¨rement supportÃ©s : `Ã© Ã  Ãª Ã¨ Ã§ Ã® Ã¯ Ã¹ Ã´` et leurs majuscules. L'encodeur gÃ¨re automatiquement leur conversion vers les glyphes PSP compatibles. Tapez normalement avec votre clavier franÃ§ais.

### Espaces et Balises

- La balise `[SP]` dans le texte original reprÃ©sente un espace pleine chasse japonais. Dans votre traduction, **remplacez-la par un espace ordinaire**.
- Le retour Ã  la ligne `\n` structure les paragraphes. Utilisez-le pour aÃ©rer les boÃ®tes longues.
- Les points de suspension `...` peuvent Ãªtre tapÃ©s directement, l'encodeur les gÃ¨re.

### Style et Registre

- Registre : familier ou neutre selon le personnage. Ã‰vitez le registre soutenu sauf pour les personnages qui l'exigent (PhilÃ©mon, certains antagonistes).
- Noms propres : respectez scrupuleusement le [Dictionnaire.md](./Dictionnaire.md). Aucune traduction alternative sans validation de l'Ã©quipe.
- Ponctuation : appliquer les rÃ¨gles typographiques franÃ§aises (espace insÃ©cable avant `?`, `!`, `:`, `;`).

<br/>

---

## RÃ©fÃ©rence des Balises In-Game

Les textes bruts contiennent des balises entre crochets reprÃ©sentant des opcodes hexadÃ©cimaux du moteur Atlus. Ces balises envoient des instructions directes au CPU de la PSP.

> [!CAUTION]
> Ne jamais supprimer une balise. Si une balise disparaÃ®t lors de la traduction, le jeu crashera au moment oÃ¹ le moteur tentera de l'exÃ©cuter.

| Balise | Fonction | Exemple d'utilisation |
|:---|:---|:---|
| `[1205][001E]` | Pause dramatique (~30 frames) | `Tu penses vraiment...[1205][001E] que c'est fini ?` |
| `[1113]` | PrÃ©nom du hÃ©ros (variable dynamique) | `Salut [1113], tu vas bien ?` |
| `[1112]` | Nom de famille du hÃ©ros (variable dynamique) | `Le cadet de la famille [1112].` |
| `[1208][0002]` | DÃ©clencheur de menu de choix | Toujours prÃ©sent avant une liste d'options |
| `[0014]` | SÃ©parateur entre deux options de choix | `[0014]Oui[0014]Non` |
| `[1108]` | Affichage d'un portrait de personnage (Bust-up) | En dÃ©but ou fin de rÃ©plique |
| `[1107]` | Nettoyage du buffer d'affichage | ClÃ´ture une fenÃªtre de dialogue |
| `[NL]` / `\n` | Saut de ligne | Structure les blocs de texte longs |
| `[U+XXXX]` | Opcode inconnu (fallback) | Laisser exactement Ã  sa position originale |

Pour la liste complÃ¨te des opcodes et leur description technique, voir [DEVELOPER.md](./DEVELOPER.md).


<div align="center">

# Guide de Contribution et Relecture

**Persona 2: Innocent Sin FR — PSP (ULES01557)**

<br/>

<img src="https://img.shields.io/badge/Statut-Ouvert_aux_contributions-2ea043?style=for-the-badge" alt="Statut" />
<a href="https://discord.gg/rd4ckSWHNm"><img src="https://img.shields.io/discord/1400909421609095323?color=5865F2&label=Discord&logo=discord&logoColor=white&style=flat-square" alt="Discord" /></a>
<a href="https://hamzakarrouchi.github.io/p2is-relecture/"><img src="https://img.shields.io/badge/Outil_de_Relecture-En_Ligne-009688?style=for-the-badge" alt="Outil de Relecture" /></a>

</div>

<br/>

> [!NOTE]
> Ce guide centralise tout ce qu'il faut savoir pour participer au projet : utilisation de l'outil de relecture, règles de traduction, contraintes techniques du moteur Atlus PSP, et tableau d'avancement détaillé.

<br/>

---

## Sommaire

1. [Tableau d'Avancement Détaillé](#tableau-davancement-détaillé)
2. [L'Outil de Relecture en Ligne](#loutil-de-relecture-en-ligne)
3. [Soumettre vos Contributions](#soumettre-vos-contributions)
4. [La Contrainte Critique de Longueur](#la-contrainte-critique-de-longueur)
5. [Règles de Traduction et de Style](#règles-de-traduction-et-de-style)
6. [Référence des Balises In-Game](#référence-des-balises-in-game)

<br/>

---

## Tableau d'Avancement Détaillé

### Scénario et Dialogues

| Fichier / Composant | Contenu | Progression | Statut |
|:---|:---|:---:|:---|
| `event.bin` | 399 scripts d'histoire | 100% | ![](https://img.shields.io/badge/-Terminé-2ea043?style=flat-square) |
| `MMAP01` à `MMAP06` | Dialogues sur les cartes | 100% | ![](https://img.shields.io/badge/-Terminé-2ea043?style=flat-square) |
| `CD_SHOP.BNP` | Boutique de CD / musique | 100% | ![](https://img.shields.io/badge/-Terminé-2ea043?style=flat-square) |
| `F_BE.BNP` | Répliques de combat | 100% | ![](https://img.shields.io/badge/-Terminé-2ea043?style=flat-square) |
| `TM_EVE.BNP` | Cinématiques in-game | 100% | ![](https://img.shields.io/badge/-Terminé-2ea043?style=flat-square) |

### EBOOT.BIN — Textes Système

Le fichier est découpé en 7 parties (~1 000 entrées chacune) dans le dossier `EBOOT_decoupe/` pour éviter les limitations GitHub.

| Contenu | Fichier | IDs (estimatif) | Entrées | Progression | Statut |
|:---|:---:|:---:|:---:|:---:|:---:|
| Menus & Interface | Part 1 | 0 — 179 | ~180 | **72.2%** | <img src="https://img.shields.io/badge/-En%20cours-0366d6?style=flat-square" alt="En cours" /> |
| Noms de Personnages / PNJs / Boss | Part 1 | 180 — 449 | ~270 | **87.4%** | <img src="https://img.shields.io/badge/-Avancé-2ea44f?style=flat-square" alt="Avancé" /> |
| Commandes & Messages de Combat | Part 1 | 600 — 899 | ~300 | **79.0%** | <img src="https://img.shields.io/badge/-En%20cours-0366d6?style=flat-square" alt="En cours" /> |
| Noms & Descriptions de Personae / Démons | Part 2 & 4 | 900 — 3999 | ~800 | **28.0%** | <img src="https://img.shields.io/badge/-Débuté-ffa500?style=flat-square" alt="Débuté" /> |
| Noms & Descriptions de Compétences | Part 2 | 1200 — 1599 | ~400 | **0.0%** | <img src="https://img.shields.io/badge/-À%20faire-red?style=flat-square" alt="À faire" /> |
| Noms d'Armes / Armures / Accessoires | Part 2 & 3 | 1600 — 2199 | ~600 | **0.0%** | <img src="https://img.shields.io/badge/-À%20faire-red?style=flat-square" alt="À faire" /> |
| Objets de quête / Rumeurs / Clés | Part 3 & 4 | 2800 — 3499 | ~700 | **0.0%** | <img src="https://img.shields.io/badge/-À%20faire-red?style=flat-square" alt="À faire" /> |
| Noms de lieux / Donjons / Carte | Part 5 — 7 | 4000 — 6500 | ~2501 | **0.1%** | <img src="https://img.shields.io/badge/-Débuté-ffa500?style=flat-square" alt="Débuté" /> |
| Autres textes (Tutoriels, Infos) | Part 1, 2, 7 | 450 — 868 | ~177 | **11.9%** | <img src="https://img.shields.io/badge/-Débuté-ffa500?style=flat-square" alt="Débuté" /> |
| **Total EBOOT** | **Part 1 à 7** | **0 — 6573** | **~5 928** | **14.3%** | |

### Éléments Graphiques

| Composant | Intégration | Accents supportés | Progression | Statut |
|:---|:---:|:---|:---:|:---|
| Textures HD | Oui | — | 35/42 | ![](https://img.shields.io/badge/-En%20cours-0366d6?style=flat-square) |
| Police HD (Accents FR) | Oui | é à ê è ç î ï ù ô + majuscules | 100% | ![](https://img.shields.io/badge/-Terminé%20(Bugs)-e1ad01?style=flat-square) |
| Textures ISO | Non | — | 0/42 | ![](https://img.shields.io/badge/-Non%20démarré-critical?style=flat-square) |
| Police ISO (Accents FR) | Oui | N/A | 0% | ![](https://img.shields.io/badge/-Non%20démarré-critical?style=flat-square) |

<br/>

---

## L'Outil de Relecture en Ligne

Pour éviter que les contributeurs ne manipulent directement les fichiers JSON bruts, une application web dédiée a été développée par **@HamzaKarrouchi**.

> [!IMPORTANT]
> **Accéder à l'outil :** [Site de Relecture P2IS FR](https://hamzakarrouchi.github.io/p2is-relecture/)  
> **Le Glossaire Officiel :** [Dictionnaire P2IS FR](https://hamzakarrouchi.github.io/p2is-relecture/dictionnaire.html)

Cet outil est obligatoire pour toute contribution car il :

- Affiche simultanément le texte anglais original et votre proposition française
- Intègre un compteur dynamique d'octets qui vous alerte si votre texte dépasse la limite du moteur
- Vérifie automatiquement la terminologie par rapport au [Dictionnaire.md](./Dictionnaire.md)
- Génère un bloc de texte prêt à être soumis sans manipuler de fichiers JSON manuellement

<br/>

---

## Soumettre vos Contributions

Une fois votre travail terminé sur le site de relecture, deux méthodes pour le soumettre :

**Via Discord (méthode recommandée)**

Copiez le bloc généré par l'outil et collez-le dans le salon `#scripts` sur le [serveur Discord officiel](https://discord.gg/rd4ckSWHNm). Un développeur prendra en charge l'injection.

**Via GitHub (contributeurs avancés)**

Forkez ce dépôt, modifiez les fichiers `.json` concernés dans le dossier `traduction/`, et ouvrez une Pull Request avec le titre `[Script XXX] Traduction/Relecture`.

<br/>

---

## La Contrainte Critique de Longueur

> [!WARNING]
> Le français est structurellement 20 à 30 % plus long que l'anglais. L'architecture mémoire de la PSP est stricte : un dépassement de la taille allouée provoque un crash `Invalid Memory Access`.

**La règle d'or : la concision.**

Privilégiez toujours une adaptation naturelle et percutante plutôt qu'une traduction littérale.

- **Pour l'histoire (`event.bin`)** : L'outil recalcule l'espace dynamiquement, mais l'écran de la PSP ne grandit pas. Ne dépassez jamais **3 lignes par boîte de dialogue**.
- **Pour les combats et menus (`F_BE.BNP`, `EBOOT.BIN`)** : La contrainte est absolue. Si le texte traduit dépasse le nombre d'octets de l'original, le jeu plantera. L'outil de relecture vous avertit — respectez toujours ses limites.

<br/>

---

## Règles de Traduction et de Style

### Accents Français

Les accents sont entièrement supportés : `é à ê è ç î ï ù ô` et leurs majuscules. L'encodeur gère automatiquement leur conversion vers les glyphes PSP compatibles. Tapez normalement avec votre clavier français.

### Espaces et Balises

- La balise `[SP]` dans le texte original représente un espace pleine chasse japonais. Dans votre traduction, **remplacez-la par un espace ordinaire**.
- Le retour à la ligne `\n` structure les paragraphes. Utilisez-le pour aérer les boîtes longues.
- Les points de suspension `...` peuvent être tapés directement, l'encodeur les gère.

### Style et Registre

- Registre : familier ou neutre selon le personnage. Évitez le registre soutenu sauf pour les personnages qui l'exigent (Philémon, certains antagonistes).
- Noms propres : respectez scrupuleusement le [Dictionnaire.md](./Dictionnaire.md). Aucune traduction alternative sans validation de l'équipe.
- Ponctuation : appliquer les règles typographiques françaises (espace insécable avant `?`, `!`, `:`, `;`).

<br/>

---

## Référence des Balises In-Game

Les textes bruts contiennent des balises entre crochets représentant des opcodes hexadécimaux du moteur Atlus. Ces balises envoient des instructions directes au CPU de la PSP.

> [!CAUTION]
> Ne jamais supprimer une balise. Si une balise disparaît lors de la traduction, le jeu crashera au moment où le moteur tentera de l'exécuter.

| Balise | Fonction | Exemple d'utilisation |
|:---|:---|:---|
| `[1205][001E]` | Pause dramatique (~30 frames) | `Tu penses vraiment...[1205][001E] que c'est fini ?` |
| `[1113]` | Prénom du héros (variable dynamique) | `Salut [1113], tu vas bien ?` |
| `[1112]` | Nom de famille du héros (variable dynamique) | `Le cadet de la famille [1112].` |
| `[1208][0002]` | Déclencheur de menu de choix | Toujours présent avant une liste d'options |
| `[0014]` | Séparateur entre deux options de choix | `[0014]Oui[0014]Non` |
| `[1108]` | Affichage d'un portrait de personnage (Bust-up) | En début ou fin de réplique |
| `[1107]` | Nettoyage du buffer d'affichage | Clôture une fenêtre de dialogue |
| `[NL]` / `\n` | Saut de ligne | Structure les blocs de texte longs |
| `[U+XXXX]` | Opcode inconnu (fallback) | Laisser exactement à sa position originale |

Pour la liste complète des opcodes et leur description technique, voir [DEVELOPER.md](./DEVELOPER.md).

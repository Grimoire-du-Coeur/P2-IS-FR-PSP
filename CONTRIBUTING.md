<div align="center">
  
# Guide de Contribution & Relecture
  
**Persona 2: Innocent Sin FR (PSP)**

[![Statut](https://img.shields.io/badge/Statut-Ouvert%20aux%20contributions-brightgreen?style=flat-square)](#)
[![Discord](https://img.shields.io/discord/1400909421609095323?color=5865F2&label=Discord&logo=discord&logoColor=white&style=flat-square)](https://discord.gg/rd4ckSWHNm)

</div>

<br/>

> [!NOTE]
> Merci de ton intérêt pour le projet ! Ce guide rassemble toutes les informations nécessaires pour nous aider à traduire et relire le jeu de la manière la plus simple et efficace possible.

---

## Sommaire
1. [Le Site de Relecture (Recommandé)](#le-site-de-relecture-recommandé)
2. [Soumettre ses propositions](#soumettre-ses-propositions)
3. [Règles de Traduction et Accents](#règles-de-traduction-et-accents)
4. [Balises et Codes Techniques](#balises-et-codes-techniques)
5. [Structure Technique des JSON (Avancé)](#structure-technique-des-json-avancé)

---

## Le Site de Relecture (Recommandé)

Pour faciliter le travail de tous, un outil dédié a été développé par **@Haaamza**. Il permet de traduire, comparer et vérifier les textes sans avoir à manipuler manuellement les fichiers du jeu.

> [!IMPORTANT]
> **Lien de l'outil :** [Site de Relecture P2IS FR](https://hamzakarrouchi.github.io/p2is-relecture/)  
> **Dictionnaire de Traduction :** [Dictionnaire P2IS FR](https://hamzakarrouchi.github.io/p2is-relecture/dictionnaire.html)

**Avantages de l'outil :**
- Il affiche le texte anglais original et te permet de saisir ta proposition en français directement.
- Il calcule automatiquement la **limite d'octets** (le français étant souvent plus long que l'anglais, il est crucial de respecter l'espace mémoire alloué).
- Il t'aide à vérifier la cohérence de tes choix avec le glossaire officiel.

---

## Soumettre ses propositions

Une fois tes modifications terminées sur le site de relecture, l'outil te permet de générer tes propositions finalisées. 

Tu as deux options pour nous les transmettre :
1. **Discord (Le plus simple) :** Copie tes propositions générées par le site et colle-les directement dans le salon dédié `#📄・scripts` sur notre [serveur Discord](https://discord.gg/rd4ckSWHNm).
2. **GitHub (Pour les habitués) :** Fork le dépôt, intègre tes modifications dans les fichiers JSON du dossier `traduction/event_scripts/` et ouvre une *Pull Request* avec le titre : `[Script XXX] Proposition de traduction`.

---

## Règles de Traduction et Accents

### Limite de Longueur
Le français est environ 20–30 % plus long que l'anglais. Chaque dialogue possède un espace fixe alloué dans le code du jeu (`slot_size`). Si ta traduction dépasse cette limite, l'outil de ré-encodage l'ignorera et gardera l'anglais en jeu. **Sois concis et privilégie l'adaptation plutôt que le mot à mot.**

### Espaces et Retours à la ligne
- Le code `[SP]` dans le texte anglais représente un espace. Dans ta traduction française, utilise **un espace normal**.
- Le code `\n` représente un vrai retour à la ligne. Pense à aérer tes textes s'ils sont trop longs pour l'écran de la PSP.

### Accents Supportés
L'équipe a modifié la police du jeu (VRAM) pour inclure certains caractères français. Tu peux utiliser librement ces accents dans tes traductions :
`é è ê ô œ ü ï É È Î Ô Û Œ`

---

## Balises et Codes Techniques

Certains codes entre crochets ont un rôle technique pour le moteur du jeu. **Ils doivent impérativement être conservés et placés judicieusement dans ta traduction.**

| Code / Balise | Signification | Comportement à adopter |
|---------------|---------------|------------------------|
| `[1205][001E]` | Pause d'animation | Conserve-le pour marquer une hésitation. (Ex: `Prends...[1205][001E] ma main...`) |
| `[1113]` et `[1112]` | Prénom et Nom du Héros | Variables remplacées par le choix du joueur. Traite-les comme `{{Prénom}}` et `{{Nom}}`. |

> [!CAUTION]
> **Codes interdits à la saisie manuelle :** Ne tape jamais `[E1]`, `[E2]`, `[E3]`, `[E4]`, `[NULL]`, `[1208]` ou `[0014]`. Ces codes structurels sont gérés automatiquement par notre compilateur ou sont réservés à l'architecture des menus.

---

## Structure Technique des JSON (Avancé)

Si tu choisis d'éditer manuellement les fichiers `.json` (sans passer par le site de relecture), voici les règles strictes à suivre :

### Dialogues Classiques
Ne modifie **que** les champs `nom_fr` et `texte_fr`. Ne touche jamais à l'ID, aux offsets, aux termes de fin (`_term`) ou au texte original.

```json
{
  "nom_orig": "Thuggish[SP]student",
  "texte_orig": "Yo...[SP]Goin'[SP]somewhere?",
  "nom_fr": "Étudiant voyou",
  "texte_fr": "Yo... Tu vas quelque part ?"
}
```

### Menus de Choix
Les dialogues contenant des choix pour le joueur utilisent des champs spécifiques (`question_fr` et `choix_fr`). **Ne traduis pas le champ `texte_fr` dans ce cas.**

```json
{
  "question_orig": "Have[SP]you[SP]decided[SP]what[SP]you[SP]want[SP]to[SP]do\nafter[SP]graduation?",
  "choix_orig": ["Yeah,[SP]I've[SP]decided.", "Not[SP]yet."],
  "question_fr": "T'as une idée de ce que tu veux faire\naprès le lycée ?",
  "choix_fr": ["Ouais, j'ai décidé.", "Pas encore."]
}
```

> [!WARNING]
> Le champ `choix_fr` doit contenir **exactement le même nombre d'options** que l'original. Par ailleurs, la question française ne peut pas dépasser la longueur de la question anglaise sous peine de corrompre l'affichage du menu.

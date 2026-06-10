# Contribuer à la traduction de Persona 2: Innocent Sin en Français

Merci de ton intérêt pour le projet ! Voici tout ce qu'il faut savoir pour contribuer correctement.

---

## 📁 Structure d'un fichier JSON

Chaque script est un fichier JSON dans le dossier `traduction/event_scripts/`. Voici à quoi ressemble une entrée normale :

```json
{
  "id": 1,
  "offset": 379818,
  "data_size": 90,
  "slot_size": 94,
  "_term": [4361, 4354, 4355, 5169],
  "nom_orig": "Thuggish[SP]student",
  "texte_orig": "Yo...[SP]Goin'[SP]somewhere?",
  "nom_fr": "",
  "texte_fr": ""
}
```

### ✅ Tu remplis UNIQUEMENT ces deux champs :
- `"nom_fr"` le nom du personnage traduit en français
- `"texte_fr"` le dialogue traduit en français

### ❌ Tu ne touches JAMAIS à :
- `"id"`, `"offset"`, `"data_size"`, `"slot_size"`, `"_term"` données techniques indispensables au jeu
- `"nom_orig"`, `"texte_orig"` le texte original anglais, sert uniquement de référence

---

## 🎯 Les menus de choix

Les entrées avec un menu de choix ont des champs supplémentaires. **C'est ici que tu dois traduire**, pas dans `texte_fr` :

```json
{
  "id": 3,
  "nom_orig": "Ms.[SP]Saeko",
  "texte_orig": "Have[SP]you[SP]decided...",
  "nom_fr": "Mme Saeko",
  "texte_fr": "",
  "question_orig": "Have[SP]you[SP]decided[SP]what[SP]you[SP]want[SP]to[SP]do\nafter[SP]graduation?",
  "choix_orig": ["Yeah,[SP]I've[SP]decided.", "Not[SP]yet."],
  "question_fr": "",
  "choix_fr": ["", ""]
}
```

### ✅ Pour les menus, tu remplis :
- `"question_fr"` la question posée par le personnage
- `"choix_fr"` la liste des options du joueur, **dans le même ordre** que `choix_orig`

```json
"question_fr": "T'as une idée de ce que tu veux faire\naprès le lycée ?",
"choix_fr": ["Ouais, j'ai décidé.", "Pas encore."]
```

> ⚠️ `choix_fr` doit toujours avoir le **même nombre d'éléments** que `choix_orig`. Ne jamais en ajouter ou en supprimer.

---

## ✍️ Règles de traduction

### Les espaces et retours à la ligne

| Dans l'original | Dans ta traduction |
|---|---|
| `[SP]` | Un espace normal ` ` |
| `\n` | Un vrai retour à la ligne |

```json
"texte_orig": "Nothin'[SP]to[SP]say,[SP]huh?",
"texte_fr":   "Rien à dire, hein ?"
```

```json
"texte_orig": "Nothin'[SP]to\n[SP]say,[SP]huh?",
"texte_fr":   "Rien à\ndire, hein ?"
```

---

## 🔒 Codes à garder tels quels

Ces codes ont un rôle technique. Copie-les exactement à la même position que dans `texte_orig`.

### `[1205][001E]` Pause joueur

```json
"texte_orig": "Take...[SP][1205][001E]my...[SP][1205][001E]hand...",
"texte_fr":   "Prends...[1205][001E] ma main...[1205][001E]"
```

### `[1113]` et `[1112]` Prénom et nom du héros

Ce sont des placeholders remplacés par le jeu selon le nom choisi par le joueur. Traite-les comme `{{PRENOM}}` et `{{NOM}}`.

```json
"texte_orig": "That [1113] [1112] I've heard rumors about.",
"texte_fr":   "Ce [1113] [1112] dont j'ai entendu parler..."
```

> Note : dans certains anciens fichiers tu peux voir `[U+1113]` c'est le même code, les deux sont acceptés.

---

## 🚫 Ne jamais écrire

| Code | Raison |
|---|---|
| `[E1][E2][E3][E4]` | Fin de dialogue ajoutée automatiquement par l'outil |
| `[NULL]` seul | Padding technique géré automatiquement |
| `[1208]`, `[0014]`, `[1432][NULL][NULL]` | Structure de menu gérée via `question_fr`/`choix_fr` |

---

## 📏 Limite de longueur

Le français est environ **20–30 % plus long** que l'anglais. Chaque dialogue a un espace fixe (`slot_size`). Si ta traduction est trop longue, l'outil la **ignorera** et gardera l'anglais dans le jeu.

✅ Sois concis, adapte plutôt que de traduire mot à mot.

Pour vérifier tes fichiers : [JsonVerify](https://github.com/Garloulou/JsonVerify) par **@Garloulou**.

> ⚠️ Pour les menus de choix, la **question** (`question_fr`) ne peut pas être plus longue que la version anglaise. Si c'est le cas, l'outil affiche un warning et les choix risquent d'être mal affichés en jeu.

---

## 🔤 Accents supportés

Ces accents sont supportés dans le jeu grâce aux textures modifiées :

`é è ê ô œ ü ï É È Î Ô Û Œ`

Les autres caractères spéciaux non listés risquent de s'afficher incorrectement.

---

## 📬 Comment soumettre ta traduction

1. **Fork** ce repo sur GitHub
2. Traduis le ou les scripts JSON de ton choix dans `traduction/event_scripts/`
3. Ouvre une **Pull Request** avec le titre : `[Script XXX] Traduction`
4. Décris brièvement ce que tu as traduit dans la description

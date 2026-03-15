# Contribuer à la traduction — Persona 2: Innocent Sin FR
Merci de ton intérêt pour le projet ! Voici tout ce qu'il faut savoir pour contribuer correctement.


## 📁 Structure d'un fichier JSON

Chaque script est un fichier JSON dans le dossier `scripts/`. Voici à quoi ressemble une entrée :

```json
{
  "id": 1,
  "offset": 379818,
  "slot_size": 94,
  "data_size": 90,
  "nom_orig": "Thuggish[SP]student",
  "texte_orig": "Yo...[SP]Goin'[SP]somewhere?",
  "nom_fr": "",
  "texte_fr": ""
}
```
### ✅ Tu remplis UNIQUEMENT ces deux champs :
- `"nom_fr"` — le nom du personnage traduit en français
- `"texte_fr"` — le dialogue traduit en français

### ❌ Tu ne touches JAMAIS à :
- `"id"`, `"offset"`, `"slot_size"`, `"data_size"` — données techniques, le script en a besoin
- `"nom_orig"`, `"texte_orig"` — le texte original anglais, référence uniquement

---

## ✍️ Règles de traduction

### Les espaces et retours à la ligne

| Dans l'original | Dans ta traduction |
|---|---|
| `[SP]` | Un espace normal ` ` |
| `\n` | Un vrai retour à la ligne |

```json
"texte_orig": "Nothin'[SP]to[SP]say,[SP]huh?",
"texte_fr":   "Rien à dire, hein?"
```

---

## 🔒 Codes à garder tels quels

Ces codes ont un rôle technique — copie-les exactement à la même position que dans `texte_orig`.

### `[1205][001E]` — Pause joueur
```json
"texte_orig": "Take...[SP][1205][001E]my...[SP][1205][001E]hand...",
"texte_fr":   "Prends...[1205][001E] ma main...[1205][001E]"
```

### `[U+1113]` et `[U+1112]` — Prénom et nom du héros
Ce sont des placeholders remplacés dynamiquement par le jeu selon le nom choisi par le joueur. Traite-les comme `{{PRENOM}}` et `{{NOM}}`.
```json
"texte_orig": "That [U+1113] [U+1112] I've heard rumors about.",
"texte_fr":   "Ce [U+1113] [U+1112] dont j'ai entendu parler..."
```

### `[1432][NULL][NULL][0014]` — Menu de choix Oui/Non
Garde la structure, traduis uniquement le texte **entre** les codes :
```json
"texte_orig": "I'll let you alone.[1432][NULL][NULL][0014]He'll[1432][NULL][NULL][0014]",
"texte_fr":   "Je te laisse.[1432][NULL][NULL][0014]Il va bien.[1432][NULL][NULL][0014]"
```
> Pour tout questionnement sur certains code, contactez nous.

---

## 🚫 Ne jamais écrire

| Code | Raison |
|---|---|
| `[E1][E2][E3][E4]` | Fin de dialogue — ajouté automatiquement par le script |
| `[NULL]` seul | Padding technique — géré automatiquement |

> Exception : `[NULL]` dans `[1432][NULL][NULL][0014]` → là tu le gardes.

---

## 📏 Limite de longueur

Le français est environ **20-30% plus long** que l'anglais. Chaque dialogue a un espace fixe dans le jeu (`slot_size`). Si ta traduction est trop longue, le script la **sautera automatiquement** et gardera l'anglais.

✅ Sois concis, adapte plutôt que de traduire mot à mot.

---

## 🔤 Accents supportés

Ces accents sont supportés dans le jeu grâce aux textures modifiées :

`é è ê à ç ù â î ô û œ`  
`É È Ê À Ç Ù Â Î Ô Û Œ`

Les autres caractères spéciaux non listés risquent de s'afficher incorrectement.

---

## 📬 Comment soumettre ta traduction

1. **Fork** ce repo sur GitHub
2. Traduis le ou les scripts JSON de ton choix dans `scripts/`
3. Ouvre une **Pull Request** avec le titre : `[Script XX] Traduction`
4. Décris brièvement ce que tu as traduit dans la description


---

## 📞 Contact

- **Discord serveur** : [Rejoindre](https://discord.gg/rd4ckSWHNm)
- **Discord perso** : `@chenetulipe`

---

*Projet sous licence [CC BY-NC-SA 4.0](LICENSE) — @chenetulipe*




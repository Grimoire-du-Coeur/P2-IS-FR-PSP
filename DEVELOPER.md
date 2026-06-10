## 📺 Vidéo de présentation
🎬 **[Clique ici pour voir la vidéo](https://youtu.be/wxEEJYjx2Sw)**

![Miniature](https://img.youtube.com/vi/wxEEJYjx2Sw/maxresdefault.jpg)

---

# 🛠️ Toolkit de Traduction

Ce document explique comment fonctionne `p2is_fr_tool.py`, utile pour extraire, traduire et reconstruire l'ISO de Persona 2: Innocent Sin.

---

## ⚙️ Pipeline complet

```
ISO (ULES01557)
    │
    ▼  extract_cpk_from_iso()
P2PT_ALL.cpk
    │
    ▼  extract_event_from_cpk()
event.bin
    │
    ▼  extract_scripts_from_event()
script_000.bin … script_398.bin
    │
    ▼  decode_all_scripts()
script_000.json … script_398.json   ← ✏️ on traduit ici
    │
    ▼  validate_all_scripts()        ← 🔍 vérification cohérence menus (optionnel)
    │
    ▼  encode_all()
script_000_fr.bin … script_398_fr.bin
    │
    ▼  rebuild_iso()
ISO traduite ✅
```

---

## 🗂️ Structure interne d'un slot JSON

`find_dialogs()` extrait chaque dialogue du binaire et produit cette structure :

**Slot normal :**
```json
{
  "id": 1,
  "offset": 389018,
  "data_size": 156,
  "slot_size": 160,
  "_term": [4361, 4354, 4355, 5169],
  "nom_orig": "Ms.[SP]Saeko",
  "texte_orig": "Don't[SP]worry,[SP]guidance[SP]counseling...",
  "nom_fr": "Mme Saeko",
  "texte_fr": "T'inquiète pas, l'entretien d'orientation..."
}
```

**Slot avec menu de choix** (champs supplémentaires générés par `_parse_choices()`) :
```json
{
  "id": 3,
  "nom_orig": "Ms.[SP]Saeko",
  "texte_orig": "Have[SP]you[SP]decided...\\n[1208][0002]...[0014]Yeah.[0014]\\n...[0014]Not[SP]yet.[0014]",
  "nom_fr": "Mme Saeko",
  "texte_fr": "...",
  "question_orig": "Have[SP]you[SP]decided[SP]what[SP]you[SP]want[SP]to[SP]do\\nafter[SP]graduation?",
  "choix_orig": ["Yeah,[SP]I've[SP]decided.", "Not[SP]yet."],
  "question_fr": "T'as une idée de ce que tu veux faire\naprès le lycée ?",
  "choix_fr": ["Ouais, j'ai décidé.", "Pas encore."]
}
```

> L'encodeur (`encode_bin_from_json`) lit `question_fr`/`choix_fr` en priorité et reconstruit `texte_fr` via `_rebuild_choice_body()`. `texte_fr` peut rester rempli, il sert de fallback si les nouveaux champs sont vides.

---

## 🔧 Fonctions clés

| Fonction | Rôle |
|---|---|
| `extract_cpk_from_iso()` | Extrait `P2PT_ALL.cpk` depuis l'ISO |
| `extract_event_from_cpk()` | Extrait `event.bin` depuis le CPK |
| `extract_scripts_from_event()` | Découpe `event.bin` en `script_XXX.bin` |
| `find_dialogs(data)` | Parse un `.bin` et retourne la liste des slots JSON |
| `_parse_choices(body)` | Extrait `question_orig`/`choix_orig` depuis un texte de menu |
| `migrate_choices_in_json(entries)` | Peuple `question_fr`/`choix_fr` à partir de `texte_fr` existants |
| `decode_all_scripts()` | Appelle `find_dialogs()` sur tous les `.bin` → JSON |
| `check_menu_consistency(json_path)` | Vérifie la cohérence intro/menu pour un fichier |
| `validate_all_scripts()` | Lance `check_menu_consistency()` sur tous les JSON |
| `_align_menu_text()` | Insère du padding SP pour aligner les options sur leurs offsets originaux |
| `encode_bin_from_json()` | Réécrit un `.bin` depuis un JSON traduit |
| `encode_all()` | Encode tous les JSON traduits en `.bin` |
| `rebuild_event_bin()` | Réinjecte les `.bin` FR dans `event.bin` |
| `rebuild_iso()` | Génère l'ISO finale traduite |

---

## ⚠️ Contraintes techniques des menus de choix

### 1. NL de fin de menu
Le moteur PSP Atlus exige un `NL` (0x1101) juste avant le terminateur de chaque slot de menu. `encode_bin_from_json()` l'insère automatiquement, ne pas le mettre manuellement dans `texte_fr`.

### 2. Alignement des offsets
Le moteur PSP stocke des **pointeurs absolus** vers chaque option de menu dans le bytecode compressé. `_align_menu_text()` insère automatiquement des `[SP]` invisibles entre la question FR et `[1208]` pour que les options restent aux mêmes offsets que dans le binaire original.

Si la question FR est **plus longue** que l'originale anglaise, un warning est loggé :
```
⚠ [id 5] question FR trop longue de 1 mot(s) → les choix seront décalés ! Raccourcir la question.
```

### 3. Cohérence intro/menu
Le moteur affiche les menus en deux temps :
- **slot N** : le personnage pose la question (dialogue normal)
- **slot N+1** : même question répétée + les choix `[1208]`

`validate_all_scripts()` détecte les incohérences entre les deux formulations et les reporte :
```
script_001.json : 3 incohérence(s) détectée(s)
  ⚠ id=2 (intro) ne se termine pas par la question de id=3
```

---

## 🔤 Encodage des accents

Les accents français sont remappés vers des glyphes japonais disponibles dans la police du jeu via `ACCENT_MAP` :

| Français | Remappé |
|---|---|
| `é è ê` | `Ğ ò ¿` |
| `ô œ ü ï` | `Æ ë ˠ Ȗ` |
| `É È Î Ô Û` | `Ņ Ũ £ ō ĵ` |
| `Œ` | `Ǩ` |

Tout autre caractère non listé dans `ACCENT_MAP` est encodé en UTF-16 LE brut, si le glyphe n'existe pas dans la police du jeu, il s'affiche incorrectement.

---

## 🔍 Validation (`validate_all_scripts`)

```python
result = validate_all_scripts("traduction/event_scripts/", log_fn=print)
# retourne : {"total_files": int, "files_with_issues": int, "problems": list}
```

Chaque problème dans `problems` contient :
```python
{
    "file": "script_001.json",
    "intro_id": 2,
    "menu_id": 3,
    "q_menu": "T'as une idée...",
    "intro_end": "Bien, commençons !..."
}
```

---

## 🚀 Installation
```bash
git clone https://github.com/chenetulipe/P2-FR-IS-PSP
cd P2-FR-IS-PSP
pip install customtkinter
python p2is_fr_tool.py
```

---

## 🖥️ Utilisation
Lance `p2is_fr_tool.py` et suis les 3 onglets dans l'ordre :
1. **Pipeline Extraction** charge ton ISO et extrait les scripts en JSON
2. **Traduction** encode tes JSON traduits en `.bin`
3. **Rebuild ISO** réinjecte tout et génère l'ISO FR jouable

---

## 🧰 Outils du projet
- [JsonVerify](https://github.com/Garloulou/JsonVerify) par **@Garloulou** validation des fichiers JSON traduits

## 🔩 Outils tiers utilisés
- [UMDGen](https://www.romhacking.net/utilities/1218/) : manipulation ISO PSP
- [CriFsLib](https://github.com/Sewer56/CriFsV2Lib) : extraction CPK
- [PPSSPP](https://www.ppsspp.org/) : émulation PSP pour les tests

---

## 📚 Inspirations & Références
- [P2-EP-PSP](https://github.com/sayucchin/P2-EP-PSP) : par **sayucchin & équipe**
  projet de traduction de Persona 2: Eternal Punishment PSP.
  L'analyse de leur code source (`event.rs`, `main.rs`) nous a permis de comprendre la structure de `event.bin` (gzip + table d'offsets). Nos outils ont été développés indépendamment en Python.

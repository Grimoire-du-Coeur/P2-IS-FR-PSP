# Migration des traductions vers event_scripts — Plan d'implémentation

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Construire un moteur de transfert qui migre `nom_fr`/`texte_fr` de l'ancien format `scripts/` vers le nouveau `traduction/event_scripts/`, en transférant automatiquement les entrées sûres et en signalant les cas menu/Q-R pour revue manuelle, plus un nouveau vérificateur d'octets adapté au format.

**Architecture:** Deux outils CLI Python (stdlib uniquement) partageant des fonctions pures. `core.py` contient la logique de décision (normaliser-puis-comparer + détection de déclencheurs). `byte_budget.py` réutilise l'`estimate_bytes` existant de `json_verify/utils.py` (DRY). `transfer.py` orchestre le transfert script par script et émet un rapport de revue. `verify.py` valide la limite d'octets et la convention du nouveau format.

**Tech Stack:** Python 3.8+, `unittest` (stdlib, zéro dépendance), réutilisation de `json_verify/utils.py`.

---

## Structure des fichiers

| Fichier | Responsabilité |
|---|---|
| `migration/core.py` | Fonctions pures : `texte_nu`, `has_trigger`, `convert_fr`, `extract_codes`, `decide` |
| `migration/byte_budget.py` | Coût/budget d'octets, réutilise `estimate_bytes` existant |
| `migration/transfer.py` | CLI orchestration : transfert auto + rapport de pauses pour 1 script |
| `migration/verify.py` | CLI nouveau vérificateur (octets + convention nouveau format) |
| `migration/tests/test_core.py` | Tests des fonctions pures |
| `migration/tests/test_byte_budget.py` | Tests du calcul d'octets |
| `migration/tests/test_transfer.py` | Test d'intégration transfert sur fixture |
| `migration/tests/test_verify.py` | Tests du vérificateur |
| `migration/tests/fixtures/` | Mini paires ancien/nouveau pour tests |

**Conventions de référence :**
- Placeholders nouveau format : `[1113]` (prénom héros), `[1112]` (nom héros). Ancien : `[U+1113]`, `[U+1112]`.
- Déclencheurs de pause : `[1432]`, `[1208]`, `[E1]`, `[E2]`, `[E3]`, `[E4]`.
- Budget d'octets d'une entrée = `data_size - 8`, mesuré sur `'"' + nom_fr + "\n" + texte_fr + "\n"` (réplique exacte de `json_verify/cli.py`).

**Note `[NULL]` :** `json_verify/utils.py` compte `[NULL]` comme +2 octets (alors que `CLAUDE.md` dit 0). On réplique le comportement existant (c'est lui qui a validé les traductions actuelles). À signaler à l'utilisateur, ne pas modifier sans accord.

---

### Task 1 : `texte_nu` — normalisation pour comparaison

**Files:**
- Create: `migration/core.py`
- Test: `migration/tests/test_core.py`

- [ ] **Step 1: Écrire le test qui échoue**

```python
# migration/tests/test_core.py
import os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from core import texte_nu

class TestTexteNu(unittest.TestCase):
    def test_supprime_tous_les_codes(self):
        s = "Yo...[SP]Goin'[SP]somewhere?[1205][001E]"
        self.assertEqual(texte_nu(s), "Yo... Goin' somewhere?")

    def test_placeholder_disparait(self):
        # [U+1113] et [1113] donnent le meme texte nu (les deux disparaissent)
        self.assertEqual(texte_nu("Hi[SP][U+1113]!"), texte_nu("Hi[SP][1113]!"))

    def test_bloc_bio_laisse_le_texte_brut(self):
        # le texte du bloc bio (mots reels) reste -> divergence detectable
        avec = "Right![SP][E1][E2]Eikichi[SP]Mishina[E4][NULL][NULL][0002]"
        sans = "Right!"
        self.assertNotEqual(texte_nu(avec), texte_nu(sans))

    def test_newline_reel_devient_espace(self):
        self.assertEqual(texte_nu("a\nb"), "a b")

if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Lancer le test pour vérifier l'échec**

Run: `python -m unittest migration.tests.test_core -v` (depuis la racine `P2-FR-IS-PSP/`)
Expected: FAIL avec `ModuleNotFoundError: No module named 'core'` ou `ImportError`.

- [ ] **Step 3: Implémenter `texte_nu`**

```python
# migration/core.py
import re

_CODE_RE = re.compile(r"\[[^\]]*\]")
_WS_RE = re.compile(r"\s+")

def texte_nu(s):
    """Texte 'nu' pour comparaison : sans codes, [SP] et sauts de ligne -> espace."""
    s = s.replace("[SP]", " ")
    s = _CODE_RE.sub("", s)          # retire tous les codes [...]
    s = s.replace("\n", " ")
    s = _WS_RE.sub(" ", s).strip()
    return s
```

- [ ] **Step 4: Lancer le test pour vérifier le succès**

Run: `python -m unittest migration.tests.test_core -v`
Expected: PASS (4 tests).

- [ ] **Step 5: Commit**

```bash
git -C /home/pchamza/Project/Trad_Persona2/P2-FR-IS-PSP add migration/core.py migration/tests/test_core.py
git -C /home/pchamza/Project/Trad_Persona2/P2-FR-IS-PSP commit -m "[Migration] texte_nu : normalisation pour comparaison"
```

---

### Task 2 : `has_trigger`, `convert_fr`, `extract_codes`

**Files:**
- Modify: `migration/core.py`
- Test: `migration/tests/test_core.py`

- [ ] **Step 1: Ajouter les tests qui échouent**

```python
# Ajouter dans migration/tests/test_core.py (avant le if __name__)
from core import has_trigger, convert_fr, extract_codes

class TestHasTrigger(unittest.TestCase):
    def test_detecte_1432(self):
        self.assertTrue(has_trigger("Oui[1432][NULL][NULL][0014]Non"))
    def test_detecte_1208(self):
        self.assertTrue(has_trigger("[1208][U+0004]Buy"))
    def test_detecte_E_blocs(self):
        self.assertTrue(has_trigger("x[E1][E2]bio[E4]"))
    def test_sans_declencheur(self):
        self.assertFalse(has_trigger("Yo...[SP]Goin'?[1205][001E]"))

class TestConvertFr(unittest.TestCase):
    def test_convertit_placeholders_heros(self):
        self.assertEqual(convert_fr("Salut [U+1113] [U+1112]!"), "Salut [1113] [1112]!")
    def test_laisse_autres_codes(self):
        self.assertEqual(convert_fr("a[1205][U+000A]b"), "a[1205][U+000A]b")

class TestExtractCodes(unittest.TestCase):
    def test_liste_les_codes(self):
        self.assertEqual(extract_codes("a[1205][001E]b[NULL]"), ["[1205]", "[001E]", "[NULL]"])
```

- [ ] **Step 2: Lancer pour vérifier l'échec**

Run: `python -m unittest migration.tests.test_core -v`
Expected: FAIL `ImportError: cannot import name 'has_trigger'`.

- [ ] **Step 3: Implémenter les trois fonctions**

```python
# Ajouter dans migration/core.py
TRIGGERS = ["[1432]", "[1208]", "[E1]", "[E2]", "[E3]", "[E4]"]

# Renommages de codes connus ancien -> nouveau (ordre important : plus longs d'abord)
_KNOWN_RENAMES = [("[U+1113]", "[1113]"), ("[U+1112]", "[1112]")]

def has_trigger(s):
    """Vrai si s contient un code menu / question-reponse."""
    return any(t in s for t in TRIGGERS)

def convert_fr(s):
    """Convertit les codes de l'ancien format FR vers le nouveau."""
    for old, new in _KNOWN_RENAMES:
        s = s.replace(old, new)
    return s

def extract_codes(s):
    """Liste ordonnee des codes [...] presents dans s."""
    return _CODE_RE.findall(s)
```

- [ ] **Step 4: Lancer pour vérifier le succès**

Run: `python -m unittest migration.tests.test_core -v`
Expected: PASS (tous).

- [ ] **Step 5: Commit**

```bash
git -C /home/pchamza/Project/Trad_Persona2/P2-FR-IS-PSP add migration/core.py migration/tests/test_core.py
git -C /home/pchamza/Project/Trad_Persona2/P2-FR-IS-PSP commit -m "[Migration] has_trigger, convert_fr, extract_codes"
```

---

### Task 3 : `decide` — règle de décision par entrée

**Files:**
- Modify: `migration/core.py`
- Test: `migration/tests/test_core.py`

- [ ] **Step 1: Ajouter les tests qui échouent**

```python
# Ajouter dans migration/tests/test_core.py
from core import decide

def _e(texte_orig, nom_fr="", texte_fr=""):
    return {"id": 0, "texte_orig": texte_orig, "nom_fr": nom_fr, "texte_fr": texte_fr}

class TestDecide(unittest.TestCase):
    def test_auto_quand_texte_nu_identique_sans_declencheur(self):
        old = _e("Yo...[SP]Goin'?", nom_fr="Délinquant", texte_fr="Hep...")
        new = _e("Yo...[SP]Goin'?")
        status, reason = decide(old, new)
        self.assertEqual(status, "auto")

    def test_auto_avec_placeholder_different(self):
        old = _e("Hi[SP][U+1113]", nom_fr="X", texte_fr="Salut [U+1113]")
        new = _e("Hi[SP][1113]")
        self.assertEqual(decide(old, new)[0], "auto")

    def test_untranslated_quand_ancien_vide(self):
        old = _e("Yo?", nom_fr="", texte_fr="")
        new = _e("Yo?")
        self.assertEqual(decide(old, new)[0], "untranslated")

    def test_pause_quand_texte_diverge(self):
        old = _e("Right![SP][E1]Eikichi[SP]Mishina[E4]", nom_fr="X", texte_fr="Voilà!")
        new = _e("Right!")
        self.assertEqual(decide(old, new)[0], "pause")

    def test_pause_quand_declencheur_meme_si_texte_identique(self):
        old = _e("Oui[1432][NULL][NULL][0014]Non", nom_fr="X", texte_fr="Oui[1432][NULL][NULL][0014]Non")
        new = _e("Oui[1432][NULL][NULL][0014]Non")
        self.assertEqual(decide(old, new)[0], "pause")
```

- [ ] **Step 2: Lancer pour vérifier l'échec**

Run: `python -m unittest migration.tests.test_core -v`
Expected: FAIL `ImportError: cannot import name 'decide'`.

- [ ] **Step 3: Implémenter `decide`**

```python
# Ajouter dans migration/core.py
def decide(old_e, new_e):
    """Retourne (status, reason) : 'auto' | 'pause' | 'untranslated'."""
    nom = old_e.get("nom_fr", "").strip()
    txt = old_e.get("texte_fr", "").strip()
    if not nom and not txt:
        return ("untranslated", "ancien non traduit")

    nu_match = texte_nu(old_e["texte_orig"]) == texte_nu(new_e["texte_orig"])
    trig = has_trigger(old_e["texte_orig"]) or has_trigger(new_e["texte_orig"])

    if nu_match and not trig:
        return ("auto", "")

    reasons = []
    if not nu_match:
        reasons.append("texte divergent")
    if trig:
        reasons.append("menu/Q-R")
    return ("pause", " + ".join(reasons))
```

- [ ] **Step 4: Lancer pour vérifier le succès**

Run: `python -m unittest migration.tests.test_core -v`
Expected: PASS (tous).

- [ ] **Step 5: Commit**

```bash
git -C /home/pchamza/Project/Trad_Persona2/P2-FR-IS-PSP add migration/core.py migration/tests/test_core.py
git -C /home/pchamza/Project/Trad_Persona2/P2-FR-IS-PSP commit -m "[Migration] decide : regle normaliser-puis-comparer"
```

---

### Task 4 : `byte_budget` — coût et budget d'octets (réutilise l'existant)

**Files:**
- Create: `migration/byte_budget.py`
- Test: `migration/tests/test_byte_budget.py`

- [ ] **Step 1: Écrire le test qui échoue**

```python
# migration/tests/test_byte_budget.py
import os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from byte_budget import cost, budget, fits

class TestByteBudget(unittest.TestCase):
    def test_cost_compte_2_octets_par_char(self):
        # '"' + nom + "\n" + texte + "\n"  ->  ici nom="X" texte="ab"
        # '"' (1) X (1) \n (compte 2) a b (2) \n (2)  => 1+1+1+2+1 chars, chacun 2 octets
        self.assertEqual(cost("X", "ab"), len('"X\nab\n') * 2)

    def test_cost_code_nouveau_format_vaut_2(self):
        # '"' + "" + "\n" + "[1113]" + "\n"  ->  3 chars (" \n \n) * 2 + [1113] (2) = 8
        # [1113] (len 6) est reconnu -> 2 octets, pas 12
        self.assertEqual(cost("", "[1113]"), 8)

    def test_budget_est_data_size_moins_8(self):
        self.assertEqual(budget({"data_size": 90}), 82)

    def test_fits_vrai_sous_la_limite(self):
        self.assertTrue(fits({"data_size": 200}, "X", "Salut"))

    def test_fits_faux_au_dessus(self):
        self.assertFalse(fits({"data_size": 12}, "X", "Phrase beaucoup trop longue ici"))

    def test_fits_faux_si_crochet_non_ferme(self):
        # estimate_bytes renvoie -1 -> ne rentre pas
        self.assertFalse(fits({"data_size": 999}, "X", "oups [ pas ferme"))

if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Lancer pour vérifier l'échec**

Run: `python -m unittest migration.tests.test_byte_budget -v`
Expected: FAIL `ModuleNotFoundError: No module named 'byte_budget'`.

- [ ] **Step 3: Implémenter `byte_budget.py`**

```python
# migration/byte_budget.py
import os, sys

# Reutilise l'estimateur d'octets valide existant (DRY)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "json_verify"))
from utils import estimate_bytes  # noqa: E402

def cost(nom_fr, texte_fr):
    """Cout en octets d'une entree, identique a json_verify/cli.py. -1 si crochet non ferme."""
    return estimate_bytes('"' + nom_fr + "\n" + texte_fr + "\n")

def budget(entry):
    """Budget d'octets disponible pour une entree."""
    return entry.get("data_size", 8) - 8

def fits(entry, nom_fr, texte_fr):
    """Vrai si (nom_fr, texte_fr) tient dans le budget de l'entree."""
    c = cost(nom_fr, texte_fr)
    return c != -1 and c <= budget(entry)
```

- [ ] **Step 4: Lancer pour vérifier le succès**

Run: `python -m unittest migration.tests.test_byte_budget -v`
Expected: PASS (6 tests).

- [ ] **Step 5: Commit**

```bash
git -C /home/pchamza/Project/Trad_Persona2/P2-FR-IS-PSP add migration/byte_budget.py migration/tests/test_byte_budget.py
git -C /home/pchamza/Project/Trad_Persona2/P2-FR-IS-PSP commit -m "[Migration] byte_budget : reutilise estimate_bytes existant"
```

---

### Task 5 : Fixtures de test (mini paires ancien/nouveau)

**Files:**
- Create: `migration/tests/fixtures/old_script.json`
- Create: `migration/tests/fixtures/new_script.json`

- [ ] **Step 1: Créer la fixture ancienne**

```json
[
  {
    "id": 0,
    "offset": 100,
    "slot_size": 40,
    "data_size": 36,
    "nom_orig": "Thug",
    "texte_orig": "Yo...[SP]Goin'[SP]somewhere?",
    "nom_fr": "Délinquant",
    "texte_fr": "Hep... On va où?"
  },
  {
    "id": 1,
    "offset": 200,
    "slot_size": 200,
    "data_size": 196,
    "nom_orig": "Hanya",
    "texte_orig": "You're[SP]that[SP][U+1113][SP][U+1112].",
    "nom_fr": "Hanya",
    "texte_fr": "Tu es ce [U+1113] [U+1112]."
  },
  {
    "id": 2,
    "offset": 300,
    "slot_size": 500,
    "data_size": 496,
    "nom_orig": "Eikichi",
    "texte_orig": "Right![SP][E1][E2]Eikichi[SP]Mishina[E4][NULL][NULL][0002]",
    "nom_fr": "Eikichi",
    "texte_fr": "Voilà![E1][E2]Eikichi Mishina[E4][NULL][NULL][0002]"
  },
  {
    "id": 3,
    "offset": 800,
    "slot_size": 60,
    "data_size": 56,
    "nom_orig": "Voice",
    "texte_orig": "......?",
    "nom_fr": "",
    "texte_fr": ""
  }
]
```

- [ ] **Step 2: Créer la fixture nouvelle (FR vides, placeholders nouveau format, bloc bio retiré sur id=2)**

```json
[
  {
    "id": 0,
    "offset": 100,
    "data_size": 36,
    "slot_size": 40,
    "_term": [4358, 4354, 4355, 5169],
    "nom_orig": "Thug",
    "texte_orig": "Yo...[SP]Goin'[SP]somewhere?",
    "nom_fr": "",
    "texte_fr": ""
  },
  {
    "id": 1,
    "offset": 200,
    "data_size": 196,
    "slot_size": 200,
    "_term": [4358, 4354, 4355, 5169],
    "nom_orig": "Hanya",
    "texte_orig": "You're[SP]that[SP][1113][SP][1112].",
    "nom_fr": "",
    "texte_fr": ""
  },
  {
    "id": 2,
    "offset": 300,
    "data_size": 80,
    "slot_size": 84,
    "_term": [4358, 4354, 4355, 5169],
    "nom_orig": "Eikichi",
    "texte_orig": "Right!",
    "nom_fr": "",
    "texte_fr": ""
  },
  {
    "id": 3,
    "offset": 800,
    "data_size": 56,
    "slot_size": 60,
    "_term": [4358, 4354, 4355, 5169],
    "nom_orig": "Voice",
    "texte_orig": "......?",
    "nom_fr": "",
    "texte_fr": ""
  }
]
```

- [ ] **Step 3: Commit**

```bash
git -C /home/pchamza/Project/Trad_Persona2/P2-FR-IS-PSP add migration/tests/fixtures/
git -C /home/pchamza/Project/Trad_Persona2/P2-FR-IS-PSP commit -m "[Migration] fixtures de test ancien/nouveau"
```

---

### Task 6 : `transfer` — fonction de transfert (logique testable)

**Files:**
- Create: `migration/transfer.py`
- Test: `migration/tests/test_transfer.py`

- [ ] **Step 1: Écrire le test d'intégration qui échoue**

```python
# migration/tests/test_transfer.py
import os, sys, json, shutil, tempfile, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from transfer import transfer_script

FIX = os.path.join(os.path.dirname(__file__), "fixtures")

class TestTransferScript(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.old = os.path.join(FIX, "old_script.json")
        self.new = os.path.join(self.tmp, "new_script.json")
        shutil.copy(os.path.join(FIX, "new_script.json"), self.new)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_transfere_auto_et_signale_pauses(self):
        result = transfer_script(self.old, self.new)
        data = json.load(open(self.new, encoding="utf-8"))

        # id=0 : auto, copie directe
        self.assertEqual(data[0]["texte_fr"], "Hep... On va où?")
        self.assertEqual(data[0]["nom_fr"], "Délinquant")
        # id=1 : auto avec conversion de placeholder
        self.assertEqual(data[1]["texte_fr"], "Tu es ce [1113] [1112].")
        # id=2 : pause (bloc bio retire) -> reste vide
        self.assertEqual(data[2]["texte_fr"], "")
        # id=3 : untranslated -> reste vide
        self.assertEqual(data[3]["texte_fr"], "")

        # _term preserve
        self.assertEqual(data[0]["_term"], [4358, 4354, 4355, 5169])

        # rapport
        self.assertEqual(result["auto"], 2)
        self.assertEqual(result["untranslated"], 1)
        self.assertEqual(len(result["pauses"]), 1)
        p = result["pauses"][0]
        self.assertEqual(p["id"], 2)
        self.assertIn("texte divergent", p["reason"])
        self.assertEqual(p["reco_nom_fr"], "Eikichi")
        self.assertIn("budget", p)
        self.assertIn("reco_cost", p)

    def test_erreur_si_nombre_entrees_different(self):
        bad = os.path.join(self.tmp, "bad.json")
        json.dump(json.load(open(self.new, encoding="utf-8"))[:2],
                  open(bad, "w", encoding="utf-8"))
        with self.assertRaises(ValueError):
            transfer_script(self.old, bad)

if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Lancer pour vérifier l'échec**

Run: `python -m unittest migration.tests.test_transfer -v`
Expected: FAIL `ModuleNotFoundError: No module named 'transfer'`.

- [ ] **Step 3: Implémenter `transfer_script` (sans la partie CLI)**

```python
# migration/transfer.py
import os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
from core import decide, convert_fr           # noqa: E402
from byte_budget import cost, budget           # noqa: E402

def _load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def _save(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")

def transfer_script(old_path, new_path):
    """Transfere les entrees sures de old_path vers new_path (en place).
    Retourne un rapport {auto, untranslated, pauses:[...]}."""
    old = _load(old_path)
    new = _load(new_path)

    if len(old) != len(new):
        raise ValueError(f"Nombre d'entrees different : ancien={len(old)} nouveau={len(new)}")

    old_by_id = {e["id"]: e for e in old}
    if set(old_by_id) != {e["id"] for e in new}:
        raise ValueError("Les ensembles d'id ne correspondent pas")

    report = {"auto": 0, "untranslated": 0, "pauses": []}

    for ne in new:
        oe = old_by_id[ne["id"]]
        status, reason = decide(oe, ne)

        if status == "auto":
            ne["nom_fr"] = convert_fr(oe.get("nom_fr", ""))
            ne["texte_fr"] = convert_fr(oe.get("texte_fr", ""))
            report["auto"] += 1
        elif status == "untranslated":
            report["untranslated"] += 1
        else:  # pause
            reco_nom = convert_fr(oe.get("nom_fr", ""))
            reco_txt = convert_fr(oe.get("texte_fr", ""))
            report["pauses"].append({
                "id": ne["id"],
                "reason": reason,
                "nom_orig": ne.get("nom_orig", ""),
                "texte_orig_new": ne.get("texte_orig", ""),
                "reco_nom_fr": reco_nom,
                "reco_texte_fr": reco_txt,
                "budget": budget(ne),
                "reco_cost": cost(reco_nom, reco_txt),
            })

    _save(new_path, new)
    return report
```

- [ ] **Step 4: Lancer pour vérifier le succès**

Run: `python -m unittest migration.tests.test_transfer -v`
Expected: PASS (2 tests).

- [ ] **Step 5: Commit**

```bash
git -C /home/pchamza/Project/Trad_Persona2/P2-FR-IS-PSP add migration/transfer.py migration/tests/test_transfer.py
git -C /home/pchamza/Project/Trad_Persona2/P2-FR-IS-PSP commit -m "[Migration] transfer_script : transfert auto + rapport de pauses"
```

---

### Task 7 : `transfer.py` — interface CLI + rapport lisible

**Files:**
- Modify: `migration/transfer.py`

- [ ] **Step 1: Écrire le test de résolution de chemins**

```python
# Ajouter dans migration/tests/test_transfer.py
from transfer import resolve_paths

class TestResolvePaths(unittest.TestCase):
    def test_resout_numero_en_chemins(self):
        old, new = resolve_paths("007", base="/proj")
        self.assertEqual(old, "/proj/scripts/script_007.json")
        self.assertEqual(new, "/proj/traduction/event_scripts/script_007.json")

    def test_accepte_nom_complet(self):
        old, new = resolve_paths("script_042", base="/proj")
        self.assertTrue(old.endswith("scripts/script_042.json"))
        self.assertTrue(new.endswith("event_scripts/script_042.json"))
```

- [ ] **Step 2: Lancer pour vérifier l'échec**

Run: `python -m unittest migration.tests.test_transfer -v`
Expected: FAIL `ImportError: cannot import name 'resolve_paths'`.

- [ ] **Step 3: Ajouter `resolve_paths`, `format_report` et le `main`**

```python
# Ajouter dans migration/transfer.py
import re as _re

_PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def resolve_paths(token, base=None):
    """'007' ou 'script_007' -> (old_path, new_path)."""
    base = base or _PROJ
    m = _re.search(r"(\d+)", token)
    if not m:
        raise ValueError(f"Impossible d'extraire un numero de '{token}'")
    num = m.group(1).zfill(3)
    name = f"script_{num}.json"
    return (os.path.join(base, "scripts", name),
            os.path.join(base, "traduction", "event_scripts", name))

def format_report(token, report):
    lines = [f"=== {token} : {report['auto']} auto, "
             f"{len(report['pauses'])} pause, {report['untranslated']} a traduire ==="]
    for p in report["pauses"]:
        over = "" if p["reco_cost"] != -1 and p["reco_cost"] <= p["budget"] else "  ⚠ DEPASSE"
        lines.append(f"\n-- PAUSE id={p['id']} ({p['reason']}){over}")
        lines.append(f"   nom_orig      : {p['nom_orig']}")
        lines.append(f"   texte_orig    : {p['texte_orig_new']}")
        lines.append(f"   RECO nom_fr   : {p['reco_nom_fr']}")
        lines.append(f"   RECO texte_fr : {p['reco_texte_fr']}")
        lines.append(f"   octets        : reco={p['reco_cost']} / budget={p['budget']}")
    return "\n".join(lines)

def main(argv):
    if not argv:
        print("Usage: python migration/transfer.py <numero|script_NNN> [...]")
        return 1
    for token in argv:
        old_path, new_path = resolve_paths(token)
        report = transfer_script(old_path, new_path)
        print(format_report(token, report))
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
```

- [ ] **Step 4: Lancer les tests + un essai réel à blanc**

Run: `python -m unittest migration.tests.test_transfer -v`
Expected: PASS.

Run: `python migration/transfer.py 007`
Expected: affiche le rapport pour script_007 ; `git -C ... status` montre `traduction/event_scripts/script_007.json` modifié avec des FR remplis.

- [ ] **Step 5: Commit**

```bash
git -C /home/pchamza/Project/Trad_Persona2/P2-FR-IS-PSP add migration/transfer.py migration/tests/test_transfer.py
git -C /home/pchamza/Project/Trad_Persona2/P2-FR-IS-PSP commit -m "[Migration] transfer.py : CLI + rapport de pauses lisible"
```

---

### Task 8 : `verify.py` — nouveau vérificateur format event_scripts

**Files:**
- Create: `migration/verify.py`
- Test: `migration/tests/test_verify.py`

- [ ] **Step 1: Écrire les tests qui échouent**

```python
# migration/tests/test_verify.py
import os, sys, json, tempfile, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from verify import verify_data

def _entry(data_size, nom_fr, texte_fr, texte_orig="x"):
    return {"id": 1, "data_size": data_size, "slot_size": data_size + 4,
            "_term": [1, 2], "nom_orig": "N", "texte_orig": texte_orig,
            "nom_fr": nom_fr, "texte_fr": texte_fr}

class TestVerifyData(unittest.TestCase):
    def test_ok_sous_la_limite(self):
        res = verify_data([_entry(200, "X", "Salut")])
        self.assertEqual(res["error_cnt"], 0)
        self.assertEqual(res["ok"], 1)

    def test_erreur_si_depasse(self):
        res = verify_data([_entry(12, "X", "Phrase beaucoup trop longue pour 4 octets")])
        self.assertEqual(res["error_cnt"], 1)
        self.assertIn("ID 1", res["errors"][0])

    def test_skip_si_vide(self):
        res = verify_data([_entry(100, "", "")])
        self.assertEqual(res["skip"], 1)

    def test_avertit_si_ancien_placeholder(self):
        res = verify_data([_entry(300, "X", "Salut [U+1113]")])
        self.assertTrue(any("[U+1113]" in w for w in res["warnings"]))

    def test_avertit_si_structure_1432_cassee(self):
        # un seul [1432] sans la structure complete attendue
        res = verify_data([_entry(300, "X", "Oui[1432]Non")])
        self.assertTrue(any("1432" in w for w in res["warnings"]))

    def test_pas_d_avertissement_si_structure_1432_correcte(self):
        res = verify_data([_entry(300, "X", "Oui[1432][NULL][NULL][0014]Non")])
        self.assertFalse(any("1432" in w for w in res["warnings"]))
```

- [ ] **Step 2: Lancer pour vérifier l'échec**

Run: `python -m unittest migration.tests.test_verify -v`
Expected: FAIL `ModuleNotFoundError: No module named 'verify'`.

- [ ] **Step 3: Implémenter `verify.py`**

```python
# migration/verify.py
import os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
from byte_budget import cost, budget           # noqa: E402

_OLD_PLACEHOLDERS = ["[U+1113]", "[U+1112]"]

def _check_1432(texte):
    """Avertit si un [1432] n'est pas suivi de [NULL][NULL][0014]."""
    warns = []
    idx = 0
    while True:
        i = texte.find("[1432]", idx)
        if i == -1:
            break
        if not texte[i:].startswith("[1432][NULL][NULL][0014]"):
            warns.append("structure [1432] incomplete (attendu [1432][NULL][NULL][0014])")
        idx = i + 6
    return warns

def verify_data(data):
    """Verifie une liste d'entrees (nouveau format). Retourne ok/error/skip + listes."""
    res = {"ok": 0, "error_cnt": 0, "skip": 0, "errors": [], "warnings": []}
    for d in data:
        nom = d.get("nom_fr", "").strip()
        texte = d.get("texte_fr", "").strip()
        if not nom or not texte:
            res["skip"] += 1
            continue

        c = cost(nom, texte)
        lim = budget(d)
        if c == -1:
            res["error_cnt"] += 1
            res["errors"].append(f"ID {d['id']} : crochet '[' non ferme")
        elif c > lim:
            excess = c - lim
            res["error_cnt"] += 1
            res["errors"].append(
                f"ID {d['id']} : +{excess} octets (+{excess // 2} chars en trop) | Max: ~{lim // 2} chars")
        else:
            res["ok"] += 1

        for ph in _OLD_PLACEHOLDERS:
            if ph in nom or ph in texte:
                res["warnings"].append(f"ID {d['id']} : ancien placeholder {ph} (attendu sans U+)")
        for w in _check_1432(texte):
            res["warnings"].append(f"ID {d['id']} : {w}")
    return res

def verify_file(path):
    with open(path, encoding="utf-8") as f:
        return verify_data(json.load(f))

def main(argv):
    if not argv:
        print("Usage: python migration/verify.py <fichier.json> [...]")
        return 1
    had_error = False
    for path in argv:
        res = verify_file(path)
        print(f"{path}: {res['ok']} OK, {res['error_cnt']} ERROR, {res['skip']} SKIP")
        for e in res["errors"]:
            print(f"  ERREUR  - {e}")
        for w in res["warnings"]:
            print(f"  warn    - {w}")
        had_error = had_error or res["error_cnt"] > 0
    return 1 if had_error else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
```

- [ ] **Step 4: Lancer pour vérifier le succès**

Run: `python -m unittest migration.tests.test_verify -v`
Expected: PASS (6 tests).

- [ ] **Step 5: Commit**

```bash
git -C /home/pchamza/Project/Trad_Persona2/P2-FR-IS-PSP add migration/verify.py migration/tests/test_verify.py
git -C /home/pchamza/Project/Trad_Persona2/P2-FR-IS-PSP commit -m "[Migration] verify.py : verificateur format event_scripts"
```

---

### Task 9 : Détection de renommages de codes systématiques (filet de sécurité)

**Files:**
- Modify: `migration/transfer.py`
- Test: `migration/tests/test_transfer.py`

- [ ] **Step 1: Écrire le test qui échoue**

```python
# Ajouter dans migration/tests/test_transfer.py
from transfer import detect_code_renames

class TestDetectRenames(unittest.TestCase):
    def test_signale_un_code_inconnu_present_dans_ancien_mais_pas_nouveau(self):
        old = [{"id": 0, "texte_orig": "a[U+9999]b", "nom_fr": "X", "texte_fr": "y"}]
        new = [{"id": 0, "texte_orig": "a[8888]b", "nom_fr": "", "texte_fr": ""}]
        diffs = detect_code_renames(old, new)
        # apres conversion connue, [U+9999] reste cote ancien, [8888] cote nouveau
        self.assertIn("[U+9999]", diffs["ancien_seul"])
        self.assertIn("[8888]", diffs["nouveau_seul"])

    def test_rien_a_signaler_si_seuls_les_renommages_connus(self):
        old = [{"id": 0, "texte_orig": "a[U+1113]b", "nom_fr": "X", "texte_fr": "y"}]
        new = [{"id": 0, "texte_orig": "a[1113]b", "nom_fr": "", "texte_fr": ""}]
        diffs = detect_code_renames(old, new)
        self.assertEqual(diffs["ancien_seul"], {})
        self.assertEqual(diffs["nouveau_seul"], {})
```

- [ ] **Step 2: Lancer pour vérifier l'échec**

Run: `python -m unittest migration.tests.test_transfer -v`
Expected: FAIL `ImportError: cannot import name 'detect_code_renames'`.

- [ ] **Step 3: Implémenter `detect_code_renames`**

```python
# Ajouter dans migration/transfer.py
from collections import Counter
from core import extract_codes                 # noqa: E402

def detect_code_renames(old, new):
    """Compare les multiset de codes (apres conversion connue) entre ancien et nouveau.
    Retourne {ancien_seul: {code: n}, nouveau_seul: {code: n}}."""
    old_codes = Counter()
    new_codes = Counter()
    new_by_id = {e["id"]: e for e in new}
    for oe in old:
        ne = new_by_id.get(oe["id"])
        if ne is None:
            continue
        old_codes.update(extract_codes(convert_fr(oe["texte_orig"])))
        new_codes.update(extract_codes(ne["texte_orig"]))
    ancien_seul = {c: old_codes[c] - new_codes[c]
                   for c in old_codes if old_codes[c] > new_codes[c]}
    nouveau_seul = {c: new_codes[c] - old_codes[c]
                    for c in new_codes if new_codes[c] > old_codes[c]}
    return {"ancien_seul": ancien_seul, "nouveau_seul": nouveau_seul}
```

- [ ] **Step 4: Lancer pour vérifier le succès**

Run: `python -m unittest migration.tests.test_transfer -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git -C /home/pchamza/Project/Trad_Persona2/P2-FR-IS-PSP add migration/transfer.py migration/tests/test_transfer.py
git -C /home/pchamza/Project/Trad_Persona2/P2-FR-IS-PSP commit -m "[Migration] detect_code_renames : filet de securite codes systematiques"
```

---

### Task 10 : Passage à blanc global + diagnostic des renommages

**Files:**
- Create: `migration/scan_renames.py`

- [ ] **Step 1: Écrire le script de diagnostic global**

```python
# migration/scan_renames.py
"""Scanne TOUS les scripts apparies et agrege les renommages de codes
au-dela des conversions connues. Lecture seule, n'ecrit rien."""
import os, sys, json, glob
sys.path.insert(0, os.path.dirname(__file__))
from transfer import detect_code_renames        # noqa: E402
from collections import Counter

_PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main():
    anc = Counter()
    nouv = Counter()
    for old_path in sorted(glob.glob(os.path.join(_PROJ, "scripts", "script_*.json"))):
        name = os.path.basename(old_path)
        new_path = os.path.join(_PROJ, "traduction", "event_scripts", name)
        if not os.path.exists(new_path):
            continue
        try:
            old = json.load(open(old_path, encoding="utf-8"))
            new = json.load(open(new_path, encoding="utf-8"))
        except Exception as e:
            print(f"SKIP {name}: {e}")
            continue
        if len(old) != len(new):
            print(f"DIVERGE {name}: tailles {len(old)} vs {len(new)}")
            continue
        d = detect_code_renames(old, new)
        anc.update(d["ancien_seul"])
        nouv.update(d["nouveau_seul"])

    print("\n=== Codes presents cote ANCIEN seulement (apres conversion connue) ===")
    for c, n in anc.most_common(40):
        print(f"  {c}: {n}")
    print("\n=== Codes presents cote NOUVEAU seulement ===")
    for c, n in nouv.most_common(40):
        print(f"  {c}: {n}")

if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Lancer le diagnostic (lecture seule)**

Run: `python migration/scan_renames.py`
Expected: affiche les codes asymétriques. **Analyser la sortie avec l'utilisateur** : si un code apparaît massivement « ancien seul » avec un équivalent « nouveau seul », c'est un renommage systématique à ajouter dans `_KNOWN_RENAMES` (core.py). Les `[E1]..[E4]` et bio resteront asymétriques (normal, ce sont des pauses).

- [ ] **Step 3: Commit du script de diagnostic**

```bash
git -C /home/pchamza/Project/Trad_Persona2/P2-FR-IS-PSP add migration/scan_renames.py
git -C /home/pchamza/Project/Trad_Persona2/P2-FR-IS-PSP commit -m "[Migration] scan_renames : diagnostic global des codes"
```

---

### Task 11 : Validation end-to-end sur un script réel + suite complète

**Files:** (aucun nouveau ; validation)

- [ ] **Step 1: Lancer toute la suite de tests**

Run: `python -m unittest discover -s migration/tests -v`
Expected: tous les tests PASS.

- [ ] **Step 2: Transférer un script déjà traduit et le vérifier**

```bash
python migration/transfer.py 000
python migration/verify.py traduction/event_scripts/script_000.json
```
Expected: le transfert remplit les entrées auto de script_000, liste les pauses (id 19 a un `[1432]`), et `verify.py` ne signale aucune erreur d'octets sur les entrées remplies.

- [ ] **Step 3: Vérifier visuellement la non-divergence**

Run: `git -C /home/pchamza/Project/Trad_Persona2/P2-FR-IS-PSP diff traduction/event_scripts/script_000.json`
Expected: seuls `nom_fr`/`texte_fr` changent ; `_term`, `data_size`, `slot_size`, `offset`, `texte_orig` intacts ; placeholders en `[1113]`/`[1112]`.

- [ ] **Step 4: Décision sur les pauses de script_000 (revue avec l'utilisateur)**

Pour chaque pause listée : présenter la recommandation, valider/ajuster avec l'utilisateur, écrire dans le fichier (édition directe), relancer `verify.py`.

- [ ] **Step 5: Commit du premier script migré**

```bash
git -C /home/pchamza/Project/Trad_Persona2/P2-FR-IS-PSP add traduction/event_scripts/script_000.json
git -C /home/pchamza/Project/Trad_Persona2/P2-FR-IS-PSP commit -m "[Script 000] Migration vers event_scripts (transfert + pauses validees)"
```

---

## Notes de revue

- **`[NULL]` = 2 octets** dans la logique réutilisée (vs `CLAUDE.md` qui dit 0). Réplique volontaire du vérificateur existant. À confirmer avec l'utilisateur si on veut un jour aligner sur le moteur réel.
- **`scan_renames.py` d'abord** : faire tourner le diagnostic (Task 10) tôt permet de découvrir d'éventuels renommages de codes systématiques au-delà de `[U+1113]`/`[U+1112]` avant de migrer en masse.
- **Périmètre** : ce plan couvre `event_scripts`. `AutreScript/` (CD_SHOP, MMAP01-06) → `traduction/` se fera ensuite en généralisant `resolve_paths`.
```

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
        with open(self.new, encoding="utf-8") as f:
            data = json.load(f)

        self.assertEqual(data[0]["texte_fr"], "Hep... On va où?")
        self.assertEqual(data[0]["nom_fr"], "Délinquant")
        self.assertEqual(data[1]["texte_fr"], "Tu es ce [1113] [1112].")
        self.assertEqual(data[2]["texte_fr"], "")
        self.assertEqual(data[3]["texte_fr"], "")

        self.assertEqual(data[0]["_term"], [4358, 4354, 4355, 5169])

        self.assertEqual(result["auto"], 2)
        self.assertEqual(result["untranslated"], 1)
        self.assertEqual(len(result["pauses"]), 1)
        p = result["pauses"][0]
        self.assertEqual(p["id"], 2)
        self.assertIn("texte divergent", p["reason"])
        self.assertEqual(p["reco_nom_fr"], "Eikichi")
        self.assertIn("budget", p)
        self.assertIn("reco_cost", p)

    def test_compte_divergent_produit_new_only(self):
        old = [{"id": 0, "offset": 1, "slot_size": 40, "data_size": 36,
                "nom_orig": "A", "texte_orig": "Bonjour le monde",
                "nom_fr": "A", "texte_fr": "Salut"}]
        new = [
            {"id": 0, "offset": 1, "data_size": 36, "slot_size": 40, "_term": [1],
             "nom_orig": "A", "texte_orig": "Bonjour le monde", "nom_fr": "", "texte_fr": ""},
            {"id": 1, "offset": 2, "data_size": 36, "slot_size": 40, "_term": [1],
             "nom_orig": "B", "texte_orig": "Entree totalement nouvelle ici",
             "nom_fr": "", "texte_fr": ""},
        ]
        op = os.path.join(self.tmp, "o.json")
        np = os.path.join(self.tmp, "n.json")
        with open(op, "w", encoding="utf-8") as f:
            json.dump(old, f)
        with open(np, "w", encoding="utf-8") as f:
            json.dump(new, f)
        result = transfer_script(op, np)
        self.assertEqual(result["auto"], 1)
        self.assertEqual(len(result["new_only"]), 1)
        self.assertEqual(result["new_only"][0]["id"], 1)
        with open(np, encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data[0]["texte_fr"], "Salut")
        self.assertEqual(data[1]["texte_fr"], "")

    def test_ancien_sans_contrepartie_devient_orphan(self):
        old = [
            {"id": 0, "offset": 1, "slot_size": 40, "data_size": 36,
             "nom_orig": "A", "texte_orig": "Phrase A unique",
             "nom_fr": "A", "texte_fr": "TradA"},
            {"id": 1, "offset": 2, "slot_size": 40, "data_size": 36,
             "nom_orig": "B", "texte_orig": "Phrase B disparue",
             "nom_fr": "B", "texte_fr": "TradB"},
        ]
        new = [{"id": 0, "offset": 1, "data_size": 36, "slot_size": 40, "_term": [1],
                "nom_orig": "A", "texte_orig": "Phrase A unique",
                "nom_fr": "", "texte_fr": ""}]
        op = os.path.join(self.tmp, "o.json")
        np = os.path.join(self.tmp, "n.json")
        with open(op, "w", encoding="utf-8") as f:
            json.dump(old, f)
        with open(np, "w", encoding="utf-8") as f:
            json.dump(new, f)
        result = transfer_script(op, np)
        self.assertEqual(result["auto"], 1)
        self.assertEqual(len(result["orphans"]), 1)
        self.assertEqual(result["orphans"][0]["id"], 1)

    def test_replace_avec_ancien_non_traduit_compte_untranslated(self):
        # bloc replace ou l'ancien n'est PAS traduit -> untranslated, pas de pause
        old = [{"id": 0, "offset": 1, "slot_size": 40, "data_size": 36,
                "nom_orig": "A", "texte_orig": "Texte ancien divergent",
                "nom_fr": "", "texte_fr": ""}]
        new = [{"id": 0, "offset": 1, "data_size": 36, "slot_size": 40, "_term": [1],
                "nom_orig": "A", "texte_orig": "Texte nouveau completement autre",
                "nom_fr": "", "texte_fr": ""}]
        op = os.path.join(self.tmp, "o.json")
        np = os.path.join(self.tmp, "n.json")
        with open(op, "w", encoding="utf-8") as f:
            json.dump(old, f)
        with open(np, "w", encoding="utf-8") as f:
            json.dump(new, f)
        result = transfer_script(op, np)
        self.assertEqual(result["untranslated"], 1)
        self.assertEqual(len(result["pauses"]), 0)

    def test_reco_reason_inclut_menu_si_declencheur_dans_replace(self):
        # bloc replace dont le nouveau contient [1432] -> reason doit mentionner menu/Q-R
        old = [{"id": 0, "offset": 1, "slot_size": 90, "data_size": 86,
                "nom_orig": "A", "texte_orig": "Question ancienne",
                "nom_fr": "A", "texte_fr": "Trad"}]
        new = [{"id": 0, "offset": 1, "data_size": 86, "slot_size": 90, "_term": [1],
                "nom_orig": "A", "texte_orig": "Question nouvelle[1432][NULL][NULL][0014]Oui",
                "nom_fr": "", "texte_fr": ""}]
        op = os.path.join(self.tmp, "o.json")
        np = os.path.join(self.tmp, "n.json")
        with open(op, "w", encoding="utf-8") as f:
            json.dump(old, f)
        with open(np, "w", encoding="utf-8") as f:
            json.dump(new, f)
        result = transfer_script(op, np)
        self.assertEqual(len(result["pauses"]), 1)
        self.assertIn("menu/Q-R", result["pauses"][0]["reason"])

    def test_format_report_signale_reconciliation(self):
        from transfer import format_report
        report = {"auto": 0, "untranslated": 0, "pauses": [],
                  "new_only": [{"id": 5, "nom_orig": "X", "texte_orig": "y"}],
                  "orphans": [{"id": 9, "nom_fr": "X", "texte_fr": "z"}]}
        out = format_report("test", report)
        self.assertIn("reconcilier", out)

    def test_auto_n_efface_pas_une_valeur_nouvelle_existante(self):
        old = [{"id": 0, "offset": 1, "slot_size": 40, "data_size": 36,
                "nom_orig": "X", "texte_orig": "hi", "nom_fr": "Nom", "texte_fr": ""}]
        new = [{"id": 0, "offset": 1, "data_size": 36, "slot_size": 40, "_term": [1],
                "nom_orig": "X", "texte_orig": "hi", "nom_fr": "DejaNom", "texte_fr": "Deja traduit"}]
        op = os.path.join(self.tmp, "o.json")
        np = os.path.join(self.tmp, "n.json")
        with open(op, "w", encoding="utf-8") as f:
            json.dump(old, f)
        with open(np, "w", encoding="utf-8") as f:
            json.dump(new, f)
        transfer_script(op, np)
        with open(np, encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data[0]["texte_fr"], "Deja traduit")  # non efface

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

from transfer import detect_code_renames

class TestDetectRenames(unittest.TestCase):
    def test_signale_un_code_inconnu_present_dans_ancien_mais_pas_nouveau(self):
        old = [{"id": 0, "texte_orig": "a[U+9999]b", "nom_fr": "X", "texte_fr": "y"}]
        new = [{"id": 0, "texte_orig": "a[8888]b", "nom_fr": "", "texte_fr": ""}]
        diffs = detect_code_renames(old, new)
        self.assertIn("[U+9999]", diffs["ancien_seul"])
        self.assertIn("[8888]", diffs["nouveau_seul"])

    def test_rien_a_signaler_si_seuls_les_renommages_connus(self):
        old = [{"id": 0, "texte_orig": "a[U+1113]b", "nom_fr": "X", "texte_fr": "y"}]
        new = [{"id": 0, "texte_orig": "a[1113]b", "nom_fr": "", "texte_fr": ""}]
        diffs = detect_code_renames(old, new)
        self.assertEqual(diffs["ancien_seul"], {})
        self.assertEqual(diffs["nouveau_seul"], {})

if __name__ == "__main__":
    unittest.main()

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

    def test_erreur_si_nombre_entrees_different(self):
        bad = os.path.join(self.tmp, "bad.json")
        with open(self.new, encoding="utf-8") as f:
            entries = json.load(f)[:2]
        with open(bad, "w", encoding="utf-8") as f:
            json.dump(entries, f)
        with self.assertRaises(ValueError):
            transfer_script(self.old, bad)

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

if __name__ == "__main__":
    unittest.main()

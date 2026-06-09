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
        json.dump(json.load(open(self.new, encoding="utf-8"))[:2],
                  open(bad, "w", encoding="utf-8"))
        with self.assertRaises(ValueError):
            transfer_script(self.old, bad)

if __name__ == "__main__":
    unittest.main()

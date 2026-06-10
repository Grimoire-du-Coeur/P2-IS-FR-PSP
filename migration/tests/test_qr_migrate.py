import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from qr_migrate import _load_p2is_tool, _rebuild_sur


class TestQrMigrate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tool = _load_p2is_tool()

    def test_import_sans_gui(self):
        self.assertTrue(callable(self.tool._parse_choices))
        self.assertTrue(callable(self.tool.migrate_choices_in_json))

    def test_parse_menu_1432(self):
        body = ("Question ?\n[1208][0002][1432][NULL][NULL][0014]Oui"
                "[1432][NULL][NULL][0014]\n[1432][NULL][NULL][0014]Non"
                "[1432][NULL][NULL][0014]")
        q, opts = self.tool._parse_choices(body)
        self.assertEqual(q, "Question ?")
        self.assertEqual(opts, ["Oui", "Non"])

    def test_rebuild_sur_accepte_menu_0002_canonique(self):
        orig = ("Question?\n[1208][0002][1432][NULL][NULL][0014]Yes"
                "[1432][NULL][NULL][0014]\n[1432][NULL][NULL][0014]No"
                "[1432][NULL][NULL][0014]")
        e = {"texte_orig": orig, "data_size": 400, "nom_fr": "X",
             "question_fr": "Question ?", "choix_fr": ["Oui", "Non"]}
        self.assertTrue(_rebuild_sur(self.tool, e))

    def test_rebuild_sur_refuse_menu_3_options(self):
        # marqueur [U+0003] (3 options) : _rebuild ecrit [0002] en dur -> exclu
        orig = ("Question?\n[1208][U+0003]Opt1\n[1432][NULL][NULL][0014]Opt2"
                "[1432][NULL][NULL][0014]\nOpt3")
        e = {"texte_orig": orig, "data_size": 400, "nom_fr": "X",
             "question_fr": "Question ?", "choix_fr": ["A", "B", "C"]}
        self.assertFalse(_rebuild_sur(self.tool, e))

    def test_rebuild_sur_refuse_hors_budget(self):
        orig = ("Q?\n[1208][0002][1432][NULL][NULL][0014]Yes"
                "[1432][NULL][NULL][0014]\n[1432][NULL][NULL][0014]No"
                "[1432][NULL][NULL][0014]")
        e = {"texte_orig": orig, "data_size": 40, "nom_fr": "X",
             "question_fr": "Question beaucoup trop longue pour ce slot",
             "choix_fr": ["Oui", "Non"]}
        self.assertFalse(_rebuild_sur(self.tool, e))


if __name__ == "__main__":
    unittest.main()

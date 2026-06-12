import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from byte_budget import cost, budget, fits


class TestByteBudget(unittest.TestCase):
    def test_cost_compte_2_octets_par_char(self):
        self.assertEqual(cost("X", "ab"), len('"X\nab\n') * 2)

    def test_cost_code_nouveau_format_vaut_2(self):
        # '"' + "" + "\n" + "[1113]" + "\n"  ->  3 chars (" \n \n) * 2 + [1113] (2) = 8
        self.assertEqual(cost("", "[1113]"), 8)

    def test_budget_est_data_size_moins_8(self):
        self.assertEqual(budget({"data_size": 90}), 82)

    def test_fits_vrai_sous_la_limite(self):
        self.assertTrue(fits({"data_size": 200}, "X", "Salut"))

    def test_fits_faux_au_dessus(self):
        self.assertFalse(fits({"data_size": 12}, "X", "Phrase beaucoup trop longue ici"))

    def test_fits_faux_si_crochet_non_ferme(self):
        self.assertFalse(fits({"data_size": 999}, "X", "oups [ pas ferme"))


if __name__ == "__main__":
    unittest.main()

import os
import sys
import json
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from verify import verify_data


def _entry(data_size, nom_fr, texte_fr, texte_orig="x"):
    return {
        "id": 1,
        "data_size": data_size,
        "slot_size": data_size + 4,
        "_term": [1, 2],
        "nom_orig": "N",
        "texte_orig": texte_orig,
        "nom_fr": nom_fr,
        "texte_fr": texte_fr,
    }


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
        res = verify_data([_entry(300, "X", "Oui[1432]Non")])
        self.assertTrue(any("1432" in w for w in res["warnings"]))

    def test_pas_d_avertissement_si_structure_1432_correcte(self):
        res = verify_data([_entry(300, "X", "Oui[1432][NULL][NULL][0014]Non")])
        self.assertFalse(any("1432" in w for w in res["warnings"]))


if __name__ == "__main__":
    unittest.main()

import os
import sys
import json
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from verify import verify_data, render, expand_paths


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

    def test_pas_d_avertissement_sur_variante_1432(self):
        # [1432][NULL][NULL][U+0007] est une variante legitime (stylisation)
        res = verify_data([_entry(300, "X", "miaou[1432][NULL][NULL][U+0007]")])
        self.assertFalse(any("1432" in w for w in res["warnings"]))

    def test_avertit_sur_code_famille_residuel(self):
        res = verify_data([_entry(300, "X", "Choix [U+1208] menu")])
        self.assertTrue(any("[U+1208]" in w for w in res["warnings"]))


def _res(ok=0, err=0, skip=0, errors=None, warnings=None):
    return {"ok": ok, "error_cnt": err, "skip": skip,
            "errors": errors or [], "warnings": warnings or []}


class TestRender(unittest.TestCase):
    def test_errors_only_masque_fichiers_propres(self):
        results = [("a.json", _res(ok=5)),
                   ("b.json", _res(err=1, errors=["ID 1 : trop long"]))]
        out = render(results, errors_only=True)
        self.assertNotIn("a.json", out)
        self.assertIn("b.json", out)

    def test_no_warnings_masque_warnings(self):
        results = [("a.json", _res(ok=1, warnings=["ID 1 : ancien placeholder"]))]
        self.assertNotIn("warn", render(results, show_warnings=False))
        self.assertIn("warn", render(results, show_warnings=True))

    def test_markdown_produit_tableau(self):
        out = render([("a.json", _res(ok=2))], markdown=True)
        self.assertIn("| Fichier | OK | ERROR | SKIP |", out)
        self.assertIn("| a.json | 2 | 0 | 0 |", out)

    def test_summary_totaux(self):
        results = [("a.json", _res(ok=2, err=1, errors=["x"])),
                   ("b.json", _res(ok=3, skip=1))]
        out = render(results, summary=True)
        self.assertIn("TOTAL", out)
        self.assertIn("5 OK", out)
        self.assertIn("1 ERROR", out)


class TestExpandPaths(unittest.TestCase):
    def test_dossier_expanse_en_json(self):
        d = tempfile.mkdtemp()
        for n in ("x.json", "y.json", "z.txt"):
            open(os.path.join(d, n), "w").close()
        got = expand_paths([d])
        self.assertEqual(len(got), 2)
        self.assertTrue(all(p.endswith(".json") for p in got))

    def test_fichier_inchange(self):
        self.assertEqual(expand_paths(["a.json"]), ["a.json"])


if __name__ == "__main__":
    unittest.main()

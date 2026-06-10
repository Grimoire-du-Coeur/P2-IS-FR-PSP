import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from recover import (split_speaker_segments, build_segment_index,
                     build_name_map, fill_from_segments)

# Bloc d'intro de locuteur reutilise dans les fixtures.
_BLK = '[U+1109][E2][E3][E4][NULL][NULL]"Ms.[SP]Saeko\n'
_BLK_FR = '[U+1109][E2][E3][E4][NULL][NULL]"Mme Saeko\n'


class TestSplit(unittest.TestCase):
    def test_decoupe_en_deux_au_bloc_locuteur(self):
        t = "Question?\n" + _BLK + "Suite du dialogue."
        segs = split_speaker_segments(t)
        self.assertEqual(len(segs), 2)
        self.assertIn("Question?", segs[0])
        self.assertIn("Suite du dialogue.", segs[1])

    def test_sans_bloc_un_seul_segment(self):
        self.assertEqual(len(split_speaker_segments("Juste du texte.")), 1)


def _old_combined():
    return [{
        "id": 0, "data_size": 400, "slot_size": 404,
        "nom_orig": "Ms.[SP]Saeko", "nom_fr": "Mme Saeko",
        "texte_orig": "Have[SP]you[SP]decided?\n" + _BLK + "And?[SP]Will[SP]you[SP]apply?",
        "texte_fr": "T'as decide ?\n" + _BLK_FR + "Et ? Tu postules ?",
    }]


def _new_split():
    return [
        {"id": 0, "data_size": 200, "slot_size": 204, "_term": [1],
         "nom_orig": "Ms.[SP]Saeko", "texte_orig": "Have[SP]you[SP]decided?",
         "nom_fr": "", "texte_fr": ""},
        {"id": 1, "data_size": 200, "slot_size": 204, "_term": [1],
         "nom_orig": "Ms.[SP]Saeko", "texte_orig": "And?[SP]Will[SP]you[SP]apply?",
         "nom_fr": "", "texte_fr": ""},
    ]


class TestIndex(unittest.TestCase):
    def test_index_segmente_les_deux_parties(self):
        idx = build_segment_index(_old_combined())
        self.assertIn("Have you decided?", idx)
        self.assertIn("And? Will you apply?", idx)
        self.assertEqual(idx["And? Will you apply?"], "Et ? Tu postules ?")

    def test_name_map(self):
        m = build_name_map(_old_combined())
        self.assertEqual(m["Ms.[SP]Saeko"], "Mme Saeko")


class TestFill(unittest.TestCase):
    def test_remplit_les_deux_entrees_scindees(self):
        new = _new_split()
        report = fill_from_segments(_old_combined(), new)
        self.assertEqual(report["filled"], 2)
        self.assertEqual(new[0]["texte_fr"], "T'as decide ?")
        self.assertEqual(new[1]["texte_fr"], "Et ? Tu postules ?")
        self.assertEqual(new[0]["nom_fr"], "Mme Saeko")

    def test_n_ecrase_pas_une_entree_deja_traduite(self):
        new = _new_split()
        new[0]["texte_fr"] = "DEJA TRADUIT"
        fill_from_segments(_old_combined(), new)
        self.assertEqual(new[0]["texte_fr"], "DEJA TRADUIT")

    def test_refuse_si_depasse_budget(self):
        new = _new_split()
        new[1]["data_size"] = 12  # budget 4 -> "Et ? Tu postules ?" ne tient pas
        report = fill_from_segments(_old_combined(), new)
        self.assertIn(1, report["over_budget"])
        self.assertEqual(new[1]["texte_fr"], "")

    def test_sans_segment_correspondant(self):
        new = _new_split()
        new[1]["texte_orig"] = "Phrase[SP]absente[SP]de[SP]l'ancien"
        report = fill_from_segments(_old_combined(), new)
        self.assertIn(1, report["no_match"])


if __name__ == "__main__":
    unittest.main()

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from recover import (split_speaker_segments, build_segment_index,
                     build_name_map, fill_from_segments)

# Bloc d'intro de locuteur reutilise dans les fixtures.
_BLK = '[U+1109][E2][E3][E4][NULL][NULL]"Ms.[SP]Saeko\n'
_BLK_FR = '[U+1109][E2][E3][E4][NULL][NULL]"Mme Saeko\n'
# Meme bloc apres convert_fr ([U+1109] -> [1109]), tel qu'il sort de l'index.
_BLK_FR_CONV = _BLK_FR.replace("[U+1109]", "[1109]")


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

    def test_index_inclut_l_entree_entiere(self):
        # une entree NON scindee doit etre retrouvable telle quelle
        old = [{
            "id": 0, "nom_orig": "X", "nom_fr": "X",
            "texte_orig": "Bonjour[SP]le[SP]monde", "texte_fr": "Salut le monde",
        }]
        idx = build_segment_index(old)
        self.assertEqual(idx["Bonjour le monde"], "Salut le monde")


def _old_three_segments():
    # 3 repliques dans une seule ancienne entree, 2 blocs locuteur.
    return [{
        "id": 0, "data_size": 600, "slot_size": 604,
        "nom_orig": "Ms.[SP]Saeko", "nom_fr": "Mme Saeko",
        "texte_orig": ("Listen[SP]up!\n" + _BLK + "Calm[SP]down.\n" + _BLK
                       + "Now[SP]go[SP]home."),
        "texte_fr": ("Ecoutez !\n" + _BLK_FR + "Du calme.\n" + _BLK_FR
                     + "Rentrez chez vous."),
    }]


class TestSpans(unittest.TestCase):
    def test_index_contient_la_plage_de_deux_segments(self):
        # le nouveau format peut garder 2 repliques ensemble (delimiteur inclus) :
        # la plage seg1+delim+seg2 doit etre indexee, avec le delimiteur FR dedans.
        idx = build_segment_index(_old_three_segments())
        nu_plage = 'Calm down. "Ms. Saeko Now go home.'
        self.assertIn(nu_plage, idx)
        self.assertEqual(idx[nu_plage],
                         "Du calme.\n" + _BLK_FR_CONV + "Rentrez chez vous.")

    def test_remplit_une_entree_couvrant_deux_segments(self):
        new = [{"id": 0, "data_size": 300, "slot_size": 304,
                "nom_orig": "Ms.[SP]Saeko",
                "texte_orig": "Calm[SP]down.\n" + _BLK + "Now[SP]go[SP]home.",
                "nom_fr": "", "texte_fr": ""}]
        report = fill_from_segments(_old_three_segments(), new)
        self.assertEqual(report["filled"], 1)
        self.assertEqual(new[0]["texte_fr"],
                         "Du calme.\n" + _BLK_FR_CONV + "Rentrez chez vous.")


class TestCopieAnglaise(unittest.TestCase):
    def test_n_indexe_pas_une_copie_anglaise(self):
        # vieille entree "traduite" par copie de l'anglais : ne pas la propager.
        old = [{"id": 0, "nom_orig": "Tamaki", "nom_fr": "Tamaki",
                "texte_orig": "What[SP]can[SP]I[SP]help[SP]you[SP]with?",
                "texte_fr": "What can I help you with?"}]
        idx = build_segment_index(old)
        self.assertNotIn("What can I help you with?", idx)

    def test_l_entree_reste_vide_pour_traduction_fraiche(self):
        old = [{"id": 0, "nom_orig": "Tamaki", "nom_fr": "Tamaki",
                "texte_orig": "What[SP]can[SP]I[SP]help[SP]you[SP]with?",
                "texte_fr": "What can I help you with?"}]
        new = [{"id": 0, "data_size": 200, "slot_size": 204,
                "nom_orig": "Tamaki",
                "texte_orig": "What[SP]can[SP]I[SP]help[SP]you[SP]with?",
                "nom_fr": "", "texte_fr": ""}]
        report = fill_from_segments(old, new)
        self.assertIn(0, report["no_match"])
        self.assertEqual(new[0]["texte_fr"], "")


class TestGlobalFallback(unittest.TestCase):
    def test_remplit_depuis_l_index_global_si_absent_du_script(self):
        autre = [{"id": 0, "nom_orig": "Eikichi", "nom_fr": "Eikichi",
                  "texte_orig": "See[SP]ya[SP]later!", "texte_fr": "A plus !"}]
        new = [{"id": 0, "data_size": 200, "slot_size": 204,
                "nom_orig": "Eikichi", "texte_orig": "See[SP]ya[SP]later!",
                "nom_fr": "", "texte_fr": ""}]
        report = fill_from_segments([], new,
                                    extra_idx=build_segment_index(autre),
                                    extra_names=build_name_map(autre))
        self.assertEqual(report["filled"], 1)
        self.assertEqual(new[0]["texte_fr"], "A plus !")
        self.assertEqual(new[0]["nom_fr"], "Eikichi")

    def test_le_meme_script_garde_la_priorite(self):
        local = [{"id": 0, "nom_orig": "X", "nom_fr": "X",
                  "texte_orig": "Hello", "texte_fr": "Salut"}]
        autre_idx = {"Hello": "Bonjour"}
        new = [{"id": 0, "data_size": 200, "slot_size": 204,
                "nom_orig": "X", "texte_orig": "Hello",
                "nom_fr": "", "texte_fr": ""}]
        fill_from_segments(local, new, extra_idx=autre_idx)
        self.assertEqual(new[0]["texte_fr"], "Salut")


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

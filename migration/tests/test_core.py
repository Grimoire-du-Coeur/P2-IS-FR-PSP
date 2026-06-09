import os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from core import texte_nu, has_trigger, convert_fr, extract_codes

class TestTexteNu(unittest.TestCase):
    def test_supprime_tous_les_codes(self):
        s = "Yo...[SP]Goin'[SP]somewhere?[1205][001E]"
        self.assertEqual(texte_nu(s), "Yo... Goin' somewhere?")

    def test_placeholder_disparait(self):
        self.assertEqual(texte_nu("Hi[SP][U+1113]!"), texte_nu("Hi[SP][1113]!"))

    def test_bloc_bio_laisse_le_texte_brut(self):
        avec = "Right![SP][E1][E2]Eikichi[SP]Mishina[E4][NULL][NULL][0002]"
        sans = "Right!"
        self.assertNotEqual(texte_nu(avec), texte_nu(sans))

    def test_newline_reel_devient_espace(self):
        self.assertEqual(texte_nu("a\nb"), "a b")

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

if __name__ == "__main__":
    unittest.main()

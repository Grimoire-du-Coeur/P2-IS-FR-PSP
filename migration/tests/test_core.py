import os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from core import texte_nu

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

if __name__ == "__main__":
    unittest.main()

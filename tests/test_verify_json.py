"""Le controle des balises se juge par rapport a l'original, pas dans l'absolu.

Le controle exigeait auparavant autant de `[` que de `]` dans chaque champ
traduit. Les pages d'aide du casino designent les touches de la PSP par des
caracteres ASCII (`[`, `>`, `b`, `` ` ``) : elles sont donc volontairement
desequilibrees des l'anglais, et toute traduction fidele l'etait aussi. Le
controle refusait du texte correct, et c'est l'inverse qu'il faut : signaler
la traduction qui s'ecarte de son original.
"""

import json

from p2is.outils.verify_json import verifier_fichier


def _ecrire(tmp_path, entrees, nom="extrait.json"):
    chemin = tmp_path / nom
    chemin.write_text(json.dumps(entrees, ensure_ascii=False), encoding="utf-8")
    return str(chemin)


def test_desequilibre_herite_de_l_original_accepte(tmp_path):
    """« Touche [ » vient de l'anglais : la traduction a le droit de le garder."""
    chemin = _ecrire(tmp_path, [{
        "id": 1,
        "texte_orig": "Press the [ button to Stand",
        "texte_fr": "Touche [ pour Rester",
    }])

    erreurs, _ = verifier_fichier(chemin)

    assert erreurs == []


def test_balise_perdue_signalee(tmp_path):
    """Perdre un glyphe present dans l'original reste une erreur."""
    chemin = _ecrire(tmp_path, [{
        "id": 1,
        "texte_orig": "Press the [ button to Stand",
        "texte_fr": "Touche carree pour Rester",
    }])

    erreurs, _ = verifier_fichier(chemin)

    assert len(erreurs) == 1
    assert "Crochets" in erreurs[0]


def test_balise_ajoutee_signalee(tmp_path):
    """Introduire un crochet orphelin absent de l'original est une erreur."""
    chemin = _ecrire(tmp_path, [{
        "id": 1,
        "texte_orig": "Stand with this hand",
        "texte_fr": "Rester avec [ cette main",
    }])

    erreurs, _ = verifier_fichier(chemin)

    assert len(erreurs) == 1
    assert "Crochets" in erreurs[0]


def test_balises_appairees_acceptees(tmp_path):
    """Le cas courant : des balises de controle bien formees des deux cotes."""
    chemin = _ecrire(tmp_path, [{
        "id": 1,
        "texte_orig": "Hello[SP]there[E4]",
        "texte_fr": "Salut[SP]toi[E4]",
    }])

    erreurs, _ = verifier_fichier(chemin)

    assert erreurs == []


def test_chevrons_juges_pareil(tmp_path):
    """Meme regle pour les chevrons, qui portent les balises de l'EBOOT."""
    garde = _ecrire(tmp_path, [{
        "id": 1,
        "texte_orig": "A<6 in any order",
        "texte_fr": "A<6 dans tout ordre",
    }], nom="garde.json")
    perdu = _ecrire(tmp_path, [{
        "id": 2,
        "texte_orig": "A<6 in any order",
        "texte_fr": "A a 6 dans tout ordre",
    }], nom="perdu.json")

    assert verifier_fichier(garde)[0] == []
    assert len(verifier_fichier(perdu)[0]) == 1

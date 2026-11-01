"""Le verificateur de depassements : son budget, et son perimetre.

Un depassement n'est pas cosmetique : `bin_encoder.py` tronque le texte trop
long sans rien dire, et la replique part amputee dans le patch.

Le perimetre compte autant que la formule. L'outil globait aussi
`EBOOT_decoupe/`, dont les entrees n'ont pas de bloc `_term` et ne passent pas
par cet encodeur : il remontait pres de 6 000 faux depassements, un rapport que
plus personne ne lisait. L'EBOOT a son propre auditeur.
"""

import json
import subprocess
import sys

import p2is
from p2is.outils.check_overflows import budget


def test_le_budget_retire_deux_octets_par_terminateur():
    assert budget({"data_size": 142, "_term": [1, 2, 3]}) == 136
    assert budget({"data_size": 142, "_term": [1, 2, 3, 4]}) == 134


def test_sans_terminateur_declare_le_budget_suppose_le_bloc_complet():
    """Le defaut historique, garde pour ne pas sous-estimer un budget."""
    assert budget({"data_size": 100}) == 92


def test_l_eboot_n_est_pas_dans_le_perimetre():
    res = subprocess.run(
        [sys.executable, "-m", "p2is.outils.check_overflows"],
        capture_output=True, text=True, cwd=str(p2is.RACINE), timeout=600,
    )
    assert "EBOOT_Part" not in res.stdout, (
        "l'EBOOT est reapparu dans le rapport : il a un autre encodeur, "
        "voir p2is/outils/audit_eboot.py"
    )


# script_389.json est un doublon, au bit pres, de traduction/CD_SHOP.json : la
# boutique de disques GIGA MACHO, posee a la main dans event_scripts/. Ses
# entrees n'ont ni `offset` ni `data_size`, donc bin_encoder leverait un
# KeyError si elle passait par la. Trouve le 31/10/2026, laisse en place : ce
# sont des donnees de traduction, elles ne se suppriment pas dans une refonte
# d'architecture.
DOUBLON_CD_SHOP = "script_389.json"


def test_seul_le_doublon_connu_n_a_pas_de_terminateur():
    """Si un script d'evenement perd son `_term`, le verificateur l'ignore en silence."""
    dossier = p2is.RACINE / "traduction" / "event_scripts"
    sans = set()
    for chemin in sorted(dossier.glob("*.json")):
        for entree in json.loads(chemin.read_text(encoding="utf-8")):
            if isinstance(entree, dict) and "_term" not in entree:
                sans.add(chemin.name)
    assert sans <= {DOUBLON_CD_SHOP}, f"nouveaux fichiers sans `_term` : {sans - {DOUBLON_CD_SHOP}}"


def test_le_doublon_est_bien_identique_a_CD_SHOP():
    """Le jour ou les deux divergent, c'est que quelqu'un a traduit le mauvais."""
    a = (p2is.RACINE / "traduction" / "CD_SHOP.json").read_bytes()
    b = (p2is.RACINE / "traduction" / "event_scripts" / DOUBLON_CD_SHOP).read_bytes()
    assert a == b, (
        f"{DOUBLON_CD_SHOP} et CD_SHOP.json ont diverge : seul CD_SHOP.json est injecte"
    )

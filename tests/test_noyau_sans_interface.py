"""Le noyau ne doit jamais retomber dans la dependance a l'interface.

C'est le test de non-regression de la refonte du 31/10/2026. Avant elle,
`config.py` melangeait la table d'opcodes, les couleurs du theme et les chaines
de l'interface, importait tkinter et customtkinter, et posait le theme a
l'import. Onze modules faisaient `from src.config import *`.

Consequence concrete : `python scripts/check_overflows.py` s'arretait sur
`ModuleNotFoundError: No module named 'packaging'`, remonte depuis
customtkinter. Aucun verificateur ne pouvait tourner en integration continue.
"""

import subprocess
import sys

MODULES_NOYAU = [
    "p2is.tables",
    "p2is.core.text",
    "p2is.core.cpk",
    "p2is.core.compression",
    "p2is.parsers.bin_parser",
    "p2is.parsers.fbe_parser",
    "p2is.encoders.bin_encoder",
    "p2is.encoders.mmap_encoder",
    "p2is.outils.check_overflows",
]

INTERDITS = ("tkinter", "customtkinter")


def test_aucun_module_du_noyau_ne_charge_une_bibliotheque_de_fenetres():
    """Un sous-processus neuf par module : l'ordre des imports ne doit rien y faire."""
    for module in MODULES_NOYAU:
        code = (
            f"import importlib, sys; importlib.import_module({module!r}); "
            f"print(','.join(n for n in {INTERDITS!r} if n in sys.modules))"
        )
        res = subprocess.run(
            [sys.executable, "-c", code], capture_output=True, text=True, timeout=120
        )
        assert res.returncode == 0, f"{module} ne s'importe pas :\n{res.stderr}"
        charges = res.stdout.strip()
        assert not charges, f"{module} a charge {charges}"


def test_les_tables_ne_dependent_de_rien():
    """`p2is.tables` ne doit importer aucun module, pas meme de la bibliotheque standard."""
    import ast
    from pathlib import Path

    import p2is

    arbre = ast.parse((p2is.RACINE / "p2is" / "tables.py").read_text(encoding="utf-8"))
    imports = [n for n in ast.walk(arbre) if isinstance(n, (ast.Import, ast.ImportFrom))]
    assert imports == [], f"p2is.tables importe {[ast.dump(i) for i in imports]}"
    assert Path(p2is.RACINE / "p2is" / "config.py").exists() is False

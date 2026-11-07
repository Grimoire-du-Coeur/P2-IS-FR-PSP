"""
Extraction des conteneurs compressés « 01 02 » qui contiennent du texte :
DNGSCN.BNP (PNJ du lycée et des donjons, fleurs du parc, énigme de la forêt...)
et P_DEMO.BNP (paroles des Personae à leur obtention).

Chaque bloc décompressé a le même format qu'un script d'event.bin : on en tire
les répliques « "Nom » (find_dialogs) et les autres messages (messages_parser).
Chaque entrée porte le numéro de son bloc (`bloc`) ; les messages ont en plus
`message: true` et leur `taille` (en caractères encodés).
"""

import json
from pathlib import Path

from p2is.core.lz_bnp import blocs
from p2is.parsers.bin_parser import find_dialogs, migrate_choices_in_json
from p2is.parsers.messages_parser import messages_hors_dialogues

FICHIERS_LZ = ("dngscn", "p_demo")


def est_conteneur_lz(data: bytes) -> bool:
    return data[:4] == b"\x01\x02\x00\x00"


def extraire_lz_bnp(data: bytes) -> list:
    entrees = []
    bl, _ = blocs(data)
    for k, (_off, _tot, typ, x, _ds) in enumerate(bl):
        if typ != 2:
            continue
        dl = migrate_choices_in_json(find_dialogs(x))
        for e in dl:
            e = {"bloc": k, **e}
            e.setdefault("nom_fr", "")
            e.setdefault("texte_fr", "")
            entrees.append(e)
        for o, n, t in messages_hors_dialogues(x, dl):
            entrees.append({"bloc": k, "message": True, "offset": o, "taille": n,
                            "texte_orig": t, "texte_fr": ""})
    return entrees


def scan_lz_bnp(data: bytes, stem: str, out_dir: Path, log_fn=None) -> int:
    """Écrit traduction/<STEM>.json. Les traductions déjà présentes sont gardées
    (même bloc, même position)."""
    out_path = Path(out_dir) / f"{stem.upper()}.json"
    ancien = {}
    if out_path.exists():
        for e in json.load(open(out_path, encoding="utf-8")):
            ancien[(e["bloc"], e["offset"])] = e
    entrees = extraire_lz_bnp(data)
    for e in entrees:
        a = ancien.get((e["bloc"], e["offset"]))
        if a and a.get("texte_orig") == e["texte_orig"]:
            for cle in ("texte_fr", "nom_fr", "question_fr", "choix_fr"):
                if cle in a:
                    e[cle] = a[cle]
    with open(out_path, "w", encoding="utf-8", newline="\r\n") as f:
        json.dump(entrees, f, ensure_ascii=False, indent=2)
        f.write("\n")
    if log_fn:
        log_fn(f"  {stem.upper()}: {len(entrees)} textes (conteneur compressé) → {out_path.name}", "ok")
    return len(entrees)

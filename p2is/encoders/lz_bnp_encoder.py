"""
Réinjection des conteneurs compressés « 01 02 » (DNGSCN.BNP, P_DEMO.BNP).

Pour chaque bloc qui a des traductions : les répliques sont encodées comme un
script d'event.bin (encode_bin_from_json), les messages réécrits à leur place
(appliquer_messages), puis le bloc est recompressé à sa taille exacte
d'origine. Un bloc qui ne tient plus une fois compressé reste en anglais (le
journal indique de combien il dépasse : il suffit de raccourcir un peu ses textes).
"""

import json
import tempfile
from pathlib import Path

from p2is.core.lz_bnp import ENTETE, ajuster, blocs, lz_compresser, reconstruire
from p2is.encoders.bin_encoder import encode_bin_from_json
from p2is.parsers.messages_parser import appliquer_messages


def encode_lz_bnp_from_json(orig_path: str, json_path: str, log_fn=None, out_path: str = None) -> dict:
    d = Path(orig_path).read_bytes()
    bl, _ = blocs(d)
    E = json.load(open(json_path, encoding="utf-8"))
    nom = Path(orig_path).name
    nouveaux, refuses = {}, []
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for k in sorted({e["bloc"] for e in E if e.get("texte_fr")}):
            x = bl[k][3]
            dial = [{c: v for c, v in e.items() if c != "bloc"} for e in E
                    if e["bloc"] == k and not e.get("message")]
            y = x
            if any(e.get("texte_fr") for e in dial):
                bs, js, fr = tmp / f"b{k}.bin", tmp / f"b{k}.json", tmp / f"b{k}_fr.bin"
                bs.write_bytes(x)
                json.dump(dial, open(js, "w", encoding="utf-8"), ensure_ascii=False)
                encode_bin_from_json(str(bs), str(js), None, out_path=str(fr))
                y = fr.read_bytes()
            mess = [e for e in E if e["bloc"] == k and e.get("message")]
            y = appliquer_messages(y, x, mess, log_fn, f"{nom} bloc {k}")
            if len(y) != len(x):
                refuses.append((k, "taille décompressée changée"))
                continue
            dispo = bl[k][1] - ENTETE
            comp = lz_compresser(y)
            if len(comp) > dispo:
                refuses.append((k, f"+{len(comp) - dispo} octets une fois compressé"))
                continue
            ajuster(comp, y, dispo)  # vérifie que la taille exacte est atteignable
            nouveaux[k] = y
    out = reconstruire(d, nouveaux)
    assert len(out) == len(d)
    if out_path:
        Path(out_path).write_bytes(out)
    if log_fn:
        log_fn(f"  {nom} : {len(nouveaux)} bloc(s) traduit(s) sur {len(bl)}", "ok")
        for k, raison in refuses:
            log_fn(f"  {nom} bloc {k} : {raison} -> reste en anglais (raccourcir ses textes)", "warn")
    return {"traduits": len(nouveaux), "refuses": refuses}

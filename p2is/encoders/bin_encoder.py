#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P2IS FR Tool  ·  Persona 2 Innocent Sin PSP (EUR ULES01557)
============================================================
Outil de traduction fan-made : extraction, décodage, traduction, rebuild ISO.

Pipeline complet :
  ISO → P2PT_ALL.cpk → event.bin → scripts (0-398) → JSON à traduire
  JSON traduits → scripts encodés → event.bin patché → ISO finale

Fichiers supplémentaires : CD_SHOP.BIN · F_BE.BNP · TM_EVE.BNP · MMAP01-06.BNP

Auteurs : chenetulipe & GarloulouLeAsriel
GitHub  : https://github.com/chenetulipe/P2-FR-IS-PSP
"""

import gzip
import io
import json
import struct
import zlib
from pathlib import Path

from p2is.tables import E1, E2, E3, E4, NL
from p2is.core.text import _needs_nl_suffix, _align_menu_text, _align_mid_text
from p2is.core.text import text_to_bytes
from p2is.parsers.bin_parser import find_dialogs, _rebuild_choice_body
def encode_bin_from_json(
    bin_path: str, json_path: str, log_fn, out_path: str = None
) -> str:
    data = bytearray(open(bin_path, "rb").read())
    dlgs_input = json.loads(open(json_path, encoding="utf-8").read(), strict=False)
    
    bin_dialogs = find_dialogs(data)
    input_by_id = {d["id"]: d for d in dlgs_input if isinstance(d, dict) and "id" in d}
    
    dlgs = []
    for idx, bd in enumerate(bin_dialogs):
        d_merged = dict(bd)
        inp = input_by_id.get(bd["id"]) or (dlgs_input[idx] if idx < len(dlgs_input) else None)
        if inp and isinstance(inp, dict):
            for k in ("nom_fr", "texte_fr", "choix_fr", "question_fr", "count_tag"):
                if k in inp:
                    d_merged[k] = inp[k]
        dlgs.append(d_merged)

    ok = skip = kept = 0
    for d in dlgs:
        n_fr_input = d.get("nom_fr", "").strip()
        t_fr_input = d.get("texte_fr", "").strip()
        # Si c'est un menu de choix avec les champs dédiés, reconstruire texte_fr
        choix_fr = d.get("choix_fr")
        q_fr = d.get("question_fr", "").strip()
        count_tag = d.get("count_tag") or d.get("count_tag_orig")
        if choix_fr is not None:
            # Utiliser question_fr/choix_fr si remplis, sinon fallback sur texte_fr
            filled_choices = [c for c in choix_fr if c.strip()]
            if q_fr and filled_choices:
                t_fr = _rebuild_choice_body(q_fr, choix_fr, count_tag)
            elif not t_fr_input:
                # Rien de traduit du tout → skip
                kept += 1
                continue
            else:
                t_fr = t_fr_input
        elif not n_fr_input and not t_fr_input:
            kept += 1
            continue
        else:
            t_fr = t_fr_input or d.get("texte_orig", "").strip()

        n_fr = n_fr_input or d.get("nom_orig", "").strip()

        term = d.get("_term", [E1, E2, E3, E4])
        avail = d["data_size"] - (len(term) * 2)
        # NL avant terminateur : règle binaire universelle (event + MMAP + autres)
        nl_suffix = (
            struct.pack("<H", NL)
            if _needs_nl_suffix(term, d.get("texte_orig", ""))
            else b""
        )
        # Aligner AVANT d'encoder (on a besoin d'avail pour le test d'alignement)
        enc_pre = text_to_bytes('"' + n_fr + "\n" + t_fr)
        t_fr = _align_menu_text(
            d.get("nom_orig", ""), d.get("texte_orig", ""), n_fr, t_fr
        )
        t_fr = _align_mid_text(
            d.get("nom_orig", ""), d.get("texte_orig", ""), n_fr, t_fr
        )
        enc = text_to_bytes('"' + n_fr + "\n" + t_fr)
        
        # Si l'alignement a ajouté trop de [SP] et dépasse avail, réduire le padding de sécurité
        if len(enc) + len(nl_suffix) > avail and ("[1208]" in t_fr or "[U+1208]" in t_fr):
            marker = "[U+1208]" if "[U+1208]" in t_fr else "[1208]"
            parts = t_fr.split(marker, 1)
            while parts[0].endswith("[SP]") and (len(text_to_bytes('"' + n_fr + "\n" + parts[0] + marker + parts[1])) + len(nl_suffix) > avail):
                parts[0] = parts[0][:-4]
            t_fr = parts[0] + marker + parts[1]
            enc = text_to_bytes('"' + n_fr + "\n" + t_fr)
        
        if "[1208]" in t_fr or "[U+1208]" in t_fr:
            marker = "[U+1208]" if "[U+1208]" in t_fr else "[1208]"
            pre_fr = text_to_bytes('"' + n_fr + "\n" + t_fr.split(marker)[0])
            pre_or = text_to_bytes(
                '"'
                + d.get("nom_orig", "").replace("[SP]", " ")
                + "\n"
                + d.get("texte_orig", "").split("[1208]")[0]
            )
            if len(pre_fr) > len(pre_or) and log_fn:
                log_fn(
                    f"  ⚠ [id {d['id']}] question FR trop longue de {(len(pre_fr)-len(pre_or))//2} mot(s) → alignement désactivé.",
                    "warn",
                )
        if len(enc) + len(nl_suffix) > avail:
            depassement = len(enc) + len(nl_suffix) - avail
            if log_fn:
                log_fn(
                    f"  [!] [DEPASSEMENT] [id {d['id']}] Texte FR trop long de {depassement} octets ({len(enc)} > {avail}). Troncature automatique.",
                    "warn",
                )
            if choix_fr is not None or "[1208]" in t_fr:
                # Troncature sécurisée des options pour préserver les balises [1208], [1432], [NULL], [0014]
                q_to_use = q_fr or d.get("question_orig", "")
                opts_to_use = list(choix_fr or d.get("choix_orig", []))
                while opts_to_use and len(text_to_bytes('"' + n_fr + "\n" + _rebuild_choice_body(q_to_use, opts_to_use, count_tag))) > avail - len(nl_suffix):
                    longest_idx = max(range(len(opts_to_use)), key=lambda idx: len(opts_to_use[idx]))
                    if len(opts_to_use[longest_idx]) > 3:
                        opts_to_use[longest_idx] = opts_to_use[longest_idx][:-1]
                    else:
                        break
                t_fr = _rebuild_choice_body(q_to_use, opts_to_use, count_tag)
                enc = text_to_bytes('"' + n_fr + "\n" + t_fr)
            else:
                import re
                tokens = re.split(r'(\[[a-zA-Z0-9+\-_]+\]|\s)', t_fr)
                tokens = [t for t in tokens if t]
                
                while tokens and len(text_to_bytes('"' + n_fr + "\n" + ''.join(tokens) + "...")) > avail - len(nl_suffix):
                    tokens.pop()
                if tokens:
                    t_fr = ''.join(tokens) + "..."
                else:
                    t_fr = ""
                enc = text_to_bytes('"' + n_fr + "\n" + t_fr)
            
        pad_len = avail - len(enc) - len(nl_suffix)
        if pad_len < 0:
            pad_len = 0

        end_c = b"".join(struct.pack("<H", t) for t in term)
        null_gap_orig = data[
            d["offset"] + d["data_size"] : d["offset"] + d["slot_size"]
        ]

        # PAD AVANT LE TERMINATEUR avec des espaces (0x1120) pour que le texte soit juste plus long
        # et que le moteur de script atterrisse sur le bon opcode suivant !
        # Le padding après le terminateur (0x0000) plantait le jeu car exécuté comme opcode par le moteur.
        null_pad = struct.pack("<H", 0x1120) * (pad_len // 2)
        full = enc + null_pad + nl_suffix + end_c + null_gap_orig

        if len(full) != d["slot_size"]:
            skip += 1
            continue
        data[d["offset"] : d["offset"] + d["slot_size"]] = full
        ok += 1
    if out_path is None:
        out_path = bin_path
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(data)
    if log_fn:
        log_fn(
            f"  [RESUME] {Path(out_path).name} : {ok} injectes avec succes, {skip} rejetes (trop longs), {kept} laisses en japonais.",
            "ok",
        )
    return out_path


# ── Scan fichiers BNP/BIN ─────────────────────────────────────────────────────


def encode_bnp_from_json(
    bin_path: str, json_path: str, log_fn, out_path: str = None
) -> str:
    """
    Réécrit les dialogues traduits dans un fichier BNP/BIN qui peut contenir
    des blocs gzip embeddés (MMAP01-06).

    Stratégie :
    - Entrées sans _source (dialogues dans le BNP brut) → même logique que encode_bin_from_json
    - Entrées avec _source="gz@0xOFFSET" → décompresser le bloc gzip à cet offset,
      patcher le dialogue dedans, recompresser, réinjecter dans le BNP
    """
    data = bytearray(open(bin_path, "rb").read())
    dlgs = json.loads(open(json_path, encoding="utf-8").read(), strict=False)

    # Grouper les entrées par source
    direct = []  # pas de _source : offset direct dans BNP
    by_gz = {}  # "gz@0xXXXX" → liste d'entrées

    for d in dlgs:
        src = d.get("_source", "")
        if src.startswith("gz@"):
            by_gz.setdefault(src, []).append(d)
        else:
            direct.append(d)

    ok = skip = kept = 0

    # ── 1. Entrées directes (même logique que encode_bin_from_json) ───────────
    for d in direct:
        n_fr_input = d.get("nom_fr", "").strip()
        t_fr_input = d.get("texte_fr", "").strip()
        choix_fr = d.get("choix_fr")
        q_fr = d.get("question_fr", "").strip()
        count_tag = d.get("count_tag") or d.get("count_tag_orig")
        if choix_fr is not None:
            filled = [c for c in choix_fr if c.strip()]
            if q_fr and filled:
                t_fr = _rebuild_choice_body(q_fr, choix_fr, count_tag)
            elif not t_fr_input:
                kept += 1
                continue
            else:
                t_fr = t_fr_input
        elif not n_fr_input and not t_fr_input:
            kept += 1
            continue
        else:
            t_fr = t_fr_input or d.get("texte_orig", "").strip()

        n_fr = n_fr_input or d.get("nom_orig", "").strip()
        t_fr = _align_menu_text(
            d.get("nom_orig", ""), d.get("texte_orig", ""), n_fr, t_fr
        )
        t_fr = _align_mid_text(
            d.get("nom_orig", ""), d.get("texte_orig", ""), n_fr, t_fr
        )
        for seq in (
            "[E1][E2][E3][E4]",
            "[1109][E2][E3][E4]",
            "[E1][E2][E4]",
            "[1109][E2][E4]",
            "[E1][E2][E3]",
            "[1109][E2][E3]",
        ):
            t_fr = t_fr.replace(seq, "")
        enc = text_to_bytes('"' + n_fr + "\n" + t_fr)
        term = d.get("_term", [E1, E2, E3, E4])
        avail = d["data_size"] - (len(term) * 2)
        is_menu = "[1208]" in d.get("texte_orig", "") or "[U+1208]" in d.get(
            "texte_orig", ""
        )
        nl_sfx = struct.pack("<H", NL) if is_menu else b""

        # TRONCATURE AUTOMATIQUE SÉCURISÉE si le texte FR est trop long
        if len(enc) > avail - len(nl_sfx):
            depassement = len(enc) - (avail - len(nl_sfx))
            if log_fn:
                log_fn(
                    f"  [!] [DEPASSEMENT] [id {d['id']}] Texte FR trop long de {depassement//2} caracteres.",
                    "warn",
                )
            
            import re
            tokens = re.split(r'(\[[a-zA-Z0-9+\-_]+\]|\s)', t_fr)
            tokens = [t for t in tokens if t]
            
            while tokens and len(text_to_bytes('"' + n_fr + "\n" + ''.join(tokens))) > avail - len(nl_sfx):
                tokens.pop()
                
            t_fr = ''.join(tokens)
            enc = text_to_bytes('"' + n_fr + "\n" + t_fr)

        pad_len = avail - len(enc) - len(nl_sfx)
        end_c = b"".join(struct.pack("<H", t) for t in term)
        null_gap_orig = data[
            d["offset"] + d["data_size"] : d["offset"] + d["slot_size"]
        ]
        null_pad = struct.pack("<H", 0x1120) * (pad_len // 2)
        full = enc + null_pad + nl_sfx + end_c + null_gap_orig
        if len(full) != d["slot_size"]:
            skip += 1
            continue
        data[d["offset"] : d["offset"] + d["slot_size"]] = full
        ok += 1

    # ── 2. Entrées dans des blocs gzip embeddés ───────────────────────────────
    for src, entries in by_gz.items():
        # Parser l'offset du bloc gzip dans le BNP : "gz@0x1A3F" → 0x1A3F
        try:
            gz_off = int(src.split("@")[1], 16)
        except (IndexError, ValueError):
            if log_fn:
                log_fn(f"  _source invalide : {src}", "err")
            skip += len(entries)
            continue

        # Trouver la fin du bloc gzip (gzip.decompress lit jusqu'à la fin naturelle)
        try:
            dec = bytearray(gzip.decompress(data[gz_off:]))
        except Exception as e:
            if log_fn:
                log_fn(f"  Erreur décompression {src} : {e}", "err")
            skip += len(entries)
            continue

        # Patcher chaque entrée dans le binaire décompressé
        patched_in_gz = 0
        for d in entries:
            n_fr_input = d.get("nom_fr", "").strip()
            t_fr_input = d.get("texte_fr", "").strip()
            choix_fr = d.get("choix_fr")
            q_fr = d.get("question_fr", "").strip()
            count_tag = d.get("count_tag") or d.get("count_tag_orig")
            if choix_fr is not None:
                filled = [c for c in choix_fr if c.strip()]
                if q_fr and filled:
                    t_fr = _rebuild_choice_body(q_fr, choix_fr, count_tag)
                elif not t_fr_input:
                    kept += 1
                    continue
                else:
                    t_fr = t_fr_input
            elif not n_fr_input and not t_fr_input:
                kept += 1
                continue
            else:
                t_fr = t_fr_input or d.get("texte_orig", "").strip()

            n_fr = n_fr_input or d.get("nom_orig", "").strip()
            t_fr = _align_menu_text(
                d.get("nom_orig", ""), d.get("texte_orig", ""), n_fr, t_fr
            )
            t_fr = _align_mid_text(
                d.get("nom_orig", ""), d.get("texte_orig", ""), n_fr, t_fr
            )
            enc = text_to_bytes('"' + n_fr + "\n" + t_fr)
            term = d.get("_term", [E1, E2, E3, E4])
            avail = d["data_size"] - (len(term) * 2)
            nl_sfx = (
                struct.pack("<H", NL)
                if _needs_nl_suffix(
                    d.get("_term", [E1, E2, E3, E4]), d.get("texte_orig", "")
                )
                else b""
            )
            if len(enc) + len(nl_sfx) > avail:
                if log_fn:
                    log_fn(f"  [id {d['id']}] trop long, troncature automatique", "warn")
                
                import re
                tokens = re.split(r'(\[[a-zA-Z0-9+\-_]+\]|\s)', t_fr)
                tokens = [t for t in tokens if t]
                
                while tokens and len(text_to_bytes('"' + n_fr + "\n" + ''.join(tokens) + "...")) > avail - len(nl_sfx):
                    tokens.pop()
                if tokens:
                    t_fr = ''.join(tokens) + "..."
                else:
                    t_fr = ""
                enc = text_to_bytes('"' + n_fr + "\n" + t_fr)
                
            pad_len = avail - len(enc) - len(nl_sfx)
            if pad_len < 0:
                pad_len = 0
            term = d.get("_term", [E1, E2, E3, E4])
            end_c = b"".join(struct.pack("<H", t) for t in term)
            null_gap_orig = dec[
                d["offset"] + d["data_size"] : d["offset"] + d["slot_size"]
            ]
            null_pad = struct.pack("<H", 0x1120) * (pad_len // 2)
            full = enc + null_pad + nl_sfx + end_c + null_gap_orig
            if len(full) != d["slot_size"]:
                skip += 1
                continue
            dec[d["offset"] : d["offset"] + d["slot_size"]] = full
            patched_in_gz += 1
            ok += 1

        if patched_in_gz == 0:
            continue  # rien à réécrire dans ce bloc

        # Recompresser et calculer la taille du bloc original dans le BNP
        gz_buf = io.BytesIO()
        with gzip.GzipFile(filename=b"", mode="wb", fileobj=gz_buf, mtime=0) as gz:
            gz.write(bytes(dec))
        new_gz = gz_buf.getvalue()

        # Trouver la taille du bloc gzip original (lire jusqu'au prochain magic ou fin)
        orig_end = gz_off + 10  # gzip header minimum
        # Avancer jusqu'à trouver la fin du stream gzip original
        try:
            import io as _io

            tmp = _io.BytesIO(data[gz_off:])
            with gzip.GzipFile(fileobj=tmp) as _gz:
                _gz.read()
            orig_gz_size = tmp.tell()
        except Exception:
            orig_gz_size = len(new_gz)  # fallback

        if len(new_gz) > orig_gz_size:
            if log_fn:
                log_fn(
                    f"  ⚠ {src} : bloc gzip FR trop grand ({len(new_gz)} > {orig_gz_size}), ignoré",
                    "warn",
                )
            ok -= patched_in_gz
            skip += patched_in_gz
            continue

        # Z_SYNC_FLUSH Split Padding pour atteindre orig_gz_size exactement.
        def _pad_gz(dec_data, target_size):
            base_comp = zlib.compressobj(level=9, wbits=-15)
            base_stream = base_comp.compress(dec_data) + base_comp.flush()
            header = b"\x1f\x8b\x08\x00\x00\x00\x00\x00\x02\xff"
            crc = struct.pack("<I", zlib.crc32(dec_data) & 0xFFFFFFFF)
            isize = struct.pack("<I", len(dec_data) & 0xFFFFFFFF)
            base_sz = len(header) + len(base_stream) + len(crc) + len(isize)
            if base_sz == target_size:
                return header + base_stream + crc + isize
            if base_sz > target_size:
                return None

            split_points = [len(dec_data) * i // 5 for i in range(1, 5)]
            for mask in range(1 << 4):
                comp = zlib.compressobj(level=9, wbits=-15)
                stream = b""
                last = 0
                for i in range(4):
                    if mask & (1 << i):
                        stream += comp.compress(
                            dec_data[last : split_points[i]]
                        ) + comp.flush(zlib.Z_SYNC_FLUSH)
                        last = split_points[i]
                stream += comp.compress(dec_data[last:]) + comp.flush(zlib.Z_SYNC_FLUSH)
                cur = len(header) + len(stream) + len(crc) + len(isize)
                diff = target_size - cur
                if diff >= 5 and diff % 5 == 0:
                    pad_stream = (
                        b"\x00\x00\x00\xff\xff" * ((diff // 5) - 1)
                        + b"\x01\x00\x00\xff\xff"
                    )
                    return header + stream + pad_stream + crc + isize

            # Fallback to random splits if mod 5 didn't hit
            import random

            for _ in range(500):
                comp = zlib.compressobj(level=9, wbits=-15)
                splits = sorted(
                    random.sample(range(1, len(dec_data)), random.randint(1, 5))
                )
                stream = b""
                last = 0
                for sp in splits:
                    stream += comp.compress(dec_data[last:sp]) + comp.flush(
                        zlib.Z_SYNC_FLUSH
                    )
                    last = sp
                stream += comp.compress(dec_data[last:]) + comp.flush(zlib.Z_SYNC_FLUSH)
                cur = len(header) + len(stream) + len(crc) + len(isize)
                diff = target_size - cur
                if diff >= 5 and diff % 5 == 0:
                    pad_stream = (
                        b"\x00\x00\x00\xff\xff" * ((diff // 5) - 1)
                        + b"\x01\x00\x00\xff\xff"
                    )
                    return header + stream + pad_stream + crc + isize

            return None

        res_gz = _pad_gz(dec, orig_gz_size)
        if res_gz is None:
            if log_fn:
                log_fn(
                    f"  [!] {src} : Impossible d'atteindre exactement la taille gzip ({orig_gz_size})",
                    "warn",
                )
            ok -= patched_in_gz
            skip += patched_in_gz
            continue
        data[gz_off : gz_off + orig_gz_size] = res_gz

    if out_path is None:
        out_path = bin_path
    from pathlib import Path

    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(data)
    if log_fn:
        log_fn(
            f"  {ok} traduits | {skip} ignores | {kept} conserves -> {Path(out_path).name}",
            "ok",
        )
    return out_path

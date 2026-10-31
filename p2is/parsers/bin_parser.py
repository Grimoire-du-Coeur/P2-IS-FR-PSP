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
import json
import re
import struct
import concurrent.futures
from pathlib import Path

from p2is.tables import CHAIN_E1, E1, E2, E3, E4, NL, SP
from p2is.core.compression import crilayla_decompress
from p2is.core.text import (
    decode_text,
    detect,
    _valid_name,
)
def find_dialogs(data: bytes) -> list:
    """Scanne un buffer binaire et extrait tous les dialogues valides."""
    dialogs = []
    i = 0
    while i < len(data) - 1:
        w = struct.unpack_from("<H", data, i)[0]
        if w != 0x0022 or not _valid_name(data, i):
            i += 2
            continue
        start = i
        chars = []
        j = i
        found = False
        term = None
        while j < len(data) - 1:
            c = struct.unpack_from("<H", data, j)[0]
            chars.append(c)
            if len(chars) > 2000:
                break
            t4 = chars[-4:]
            t3 = chars[-3:]
            if t4 in ([E1, E2, E3, E4], [CHAIN_E1, E2, E3, E4]):
                end = j + 2
                term = t4
                found = True
                break
            if t3 in ([E1, E2, E4], [CHAIN_E1, E2, E4], [E1, E2, E3], [CHAIN_E1, E2, E3]):
                end = j + 2
                term = t3
                found = True
                break
            j += 2
        if not found:
            i += 2
            continue
        k = end
        while k + 1 < len(data) and struct.unpack_from("<H", data, k)[0] == 0:
            k += 2
        raw_b = data[start:end]
        ac = tc = 0
        pnl = False
        for bi in range(0, len(raw_b) - 1, 2):
            bv = struct.unpack_from("<H", raw_b, bi)[0]
            if bv == NL:
                pnl = True
                continue
            if not pnl:
                continue
            if bv in {E1, E2, E3, E4, SP, CHAIN_E1}:
                continue
            tc += 1
            if 0x20 <= bv <= 0x7E:
                ac += 1
        if tc > 5 and (ac / tc) < 0.25:
            i += 2
            continue
        txt = decode_text(raw_b)
        lns = txt.split("\n")
        nom = lns[0].lstrip('"') if lns else ""
        body = "\n".join(lns[1:])
        for seq in (
            "[E1][E2][E3][E4]",
            "[1109][E2][E3][E4]",
            "[E1][E2][E4]",
            "[1109][E2][E4]",
            "[E1][E2][E3]",
            "[1109][E2][E3]",
        ):
            body = body.replace(seq, "")
        body_clean = body.strip()
        question, choices, count_tag = _parse_choices(body_clean)
        entry = {
            "id": len(dialogs),
            "offset": start,
            "data_size": end - start,
            "slot_size": k - start,
            "_term": term,
            "nom_orig": nom,
            "texte_orig": body_clean,
            "nom_fr": "",
            "texte_fr": "",
        }
        if choices is not None:
            entry["question_orig"] = question
            entry["choix_orig"] = choices
            entry["count_tag"] = count_tag
            entry["question_fr"] = ""
            entry["choix_fr"] = [""] * len(choices)
        dialogs.append(entry)
        i = k
    return dialogs


def _parse_choices(body: str) -> tuple:
    """
    Si body contient un menu de choix (marqueur [1208] ou [U+1208]),
    retourne (question, [option1, option2, ...], count_tag) avec les balises de contrôle préservées.
    Sinon retourne (body, None, None).

    Format binaire Atlus PSP pour les menus :
      Question\n[1208][COUNT][1432][NULL][NULL][0014]Option1[1432][NULL][NULL][0014]\n[1432][NULL][NULL][0014]Option2...
    Le [0014] sépare les options, [1208][COUNT] ouvre le menu (ex: [0002], [U+0003], [U+0004]).
    """
    marker = None
    for m in ("[1208]", "[U+1208]"):
        if m in body:
            marker = m
            break
    if marker is None:
        return body, None, None

    # Séparer la question du bloc de choix
    parts = body.split(marker, 1)
    question = parts[0].rstrip("\n").strip()
    choice_block = marker + parts[1]

    # Extraire le count_tag (ex: [0002], [U+0003], [0004], [U+0005])
    count_tag = "[0002]"
    match_tag = re.search(r"(\[1208\]|\[U\+1208\])(\[U\+[0-9A-Fa-f]{4}\]|\[[0-9A-Fa-f]{4}\])", choice_block)
    if match_tag:
        count_tag = match_tag.group(2)

    if "[0014]" in choice_block:
        raw_opts = re.split(r"\[0014\]", choice_block)
        options = []
        for o in raw_opts:
            cleaned = (
                re.sub(
                    r"\[1208\]|\[U\+1208\]|\[U\+[0-9A-Fa-f]{4}\]|\[0002\]|\[1432\]|\[NULL\]",
                    "",
                    o,
                )
                .strip("\n")
                .strip()
            )
            if cleaned and "\n" not in cleaned:
                options.append(cleaned)
    else:
        after_header = choice_block
        if match_tag:
            after_header = choice_block[match_tag.end():]
        else:
            after_header = choice_block[len(marker):]
        
        lines = [l.strip() for l in after_header.split("\n") if l.strip()]
        options = []
        for l in lines:
            cleaned = re.sub(r"\[1208\]|\[U\+1208\]|\[U\+[0-9A-Fa-f]{4}\]|\[1432\]|\[NULL\]", "", l).strip()
            if cleaned:
                options.append(cleaned)

    if not options:
        return body, None, None
    return question, options, count_tag


def _rebuild_choice_body(question: str, options: list, count_tag: str = None) -> str:
    """
    Reconstruit le texte complet du menu de choix à partir de la question
    et de la liste d'options, en préservant le count_tag original (ex: [0002], [U+0003], [U+0004]).
    """
    if not count_tag:
        n = len(options)
        count_tag = f"[U+{n:04X}]" if n > 2 else "[0002]"

    sep = "[1432][NULL][NULL][0014]"
    header = f"\n[1208]{count_tag}"
    opt_str = sep
    opt_str += (sep + "\n" + sep).join(options)
    opt_str += sep
    return question + header + opt_str


def check_menu_consistency(json_path: str, log_fn=None) -> list:
    """
    Vérifie qu'un fichier JSON de script est cohérent pour les menus de choix.

    Le moteur Atlus PSP affiche toujours deux slots consécutifs pour un menu :
      slot N   = texte d'intro qui SE TERMINE par la question
      slot N+1 = même question répétée + menu [1208][0002]...[0014]...

    Si la fin de l'intro (texte_fr de N) ne correspond pas à la question
    du menu (texte_fr de N+1), le joueur voit deux formulations différentes.

    Retourne la liste des problèmes trouvés :
      [{"intro_id": int, "menu_id": int, "q_menu": str, "intro_end": str}, ...]
    """
    try:
        data = json.load(open(json_path, encoding="utf-8"))
    except Exception as e:
        if log_fn:
            log_fn(f"  Impossible de lire {json_path} : {e}", "err")
        return []

    by_id = {e["id"]: e for e in data}
    problems = []

    # Identifier les slots avec menu de choix
    menu_slots = [
        e
        for e in data
        if "[1208]" in e.get("texte_orig", "") or "[0002]" in e.get("texte_orig", "")
    ]

    for menu_entry in menu_slots:
        intro_entry = by_id.get(menu_entry["id"] - 1)
        if not intro_entry:
            continue

        # Ne vérifier que si les deux ont une traduction
        q_fr_raw = menu_entry.get("texte_fr", "")
        i_fr_raw = intro_entry.get("texte_fr", "")
        if not q_fr_raw or not i_fr_raw:
            continue

        # Extraire la question du menu = tout avant [1208] / [0002]
        q_fr = (
            q_fr_raw.split("[U+1208]")[0].split("[1208]")[0].split("[0002]")[0].strip()
        )

        # Normaliser pour comparaison souple (ignorer espaces/ponctuation finale)
        def norm(s):
            return s.strip().rstrip("?! ").replace(" ", "").replace("\n", "").lower()

        q_norm = norm(q_fr)
        i_norm = norm(i_fr_raw)

        # La fin de l'intro doit correspondre à la question (sur les 20 derniers chars)
        tail = max(15, len(q_norm) - 3)
        if not i_norm.endswith(q_norm[-tail:]):
            problems.append(
                {
                    "intro_id": intro_entry["id"],
                    "menu_id": menu_entry["id"],
                    "q_menu": q_fr,
                    "intro_end": i_fr_raw,
                }
            )
            if log_fn:
                log_fn(
                    f"  ⚠ Incohérence menu : id={intro_entry['id']} (intro) "
                    f"ne se termine pas par la question de id={menu_entry['id']}",
                    "warn",
                )

    return problems


def validate_all_scripts(scripts_json_dir: str, log_fn=None, progress_fn=None) -> dict:
    """
    Parcourt tous les script_XXX.json traduits et vérifie la cohérence
    des menus de choix dans chaque fichier.

    Retourne {"total_files": int, "files_with_issues": int, "problems": list}
    """
    jdir = Path(scripts_json_dir)
    files = sorted(jdir.glob("script_*.json"))
    if not files:
        if log_fn:
            log_fn("  Aucun fichier JSON trouvé.", "warn")
        return {"total_files": 0, "files_with_issues": 0, "problems": []}

    all_problems = []
    files_with_issues = 0

    for i, jf in enumerate(files):
        if progress_fn:
            progress_fn((i + 1) / len(files))
        probs = check_menu_consistency(str(jf), log_fn=None)
        if probs:
            files_with_issues += 1
            for p in probs:
                p["file"] = jf.name
            all_problems.extend(probs)
            if log_fn:
                log_fn(f"  {jf.name} : {len(probs)} incohérence(s) détectée(s)", "warn")

    if log_fn:
        if all_problems:
            log_fn(
                f"  {files_with_issues}/{len(files)} fichiers avec incohérences "
                f"({len(all_problems)} total)",
                "warn",
            )
        else:
            log_fn(f"  Tous les menus sont cohérents ({len(files)} fichiers).", "ok")

    return {
        "total_files": len(files),
        "files_with_issues": files_with_issues,
        "problems": all_problems,
    }


def scan_bnp_bin(data: bytes, stem: str, out_dir: Path, log_fn) -> int:
    from p2is.parsers.fbe_parser import scan_fbe_bnp

    """Extrait les dialogues d'un BNP/BIN (route vers le décodeur spécial si F_BE/TM_EVE)."""
    if stem.lower() in ("f_be", "tm_eve"):
        return scan_fbe_bnp(data, stem, out_dir, log_fn)
    all_dlgs = find_dialogs(data)
    pos = gz_n = 0
    while gz_n < 200:
        idx = data.find(b"\x1f\x8b", pos)
        if idx == -1:
            break
        try:
            dec = gzip.decompress(data[idx:])
            if len(dec) > 64:
                for d in find_dialogs(dec):
                    d["_source"] = f"gz@0x{idx:X}"
                    all_dlgs.append(d)
                gz_n += 1
        except:
            pass
        pos = idx + 2
    if detect(data) == "CRILAYLA":
        dec = crilayla_decompress(data)
        if dec:
            for d in find_dialogs(dec):
                d["_source"] = "crilayla"
                all_dlgs.append(d)
    seen = set()
    unique = []
    for d in all_dlgs:
        k = (d["offset"], d["data_size"])
        if k not in seen:
            seen.add(k)
            unique.append(d)
    for k, d in enumerate(unique):
        d["id"] = k
    if not unique:
        return 0
    out_path = out_dir / f"{stem.upper()}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(unique, f, ensure_ascii=False, indent=2)
    if log_fn:
        log_fn(f"  {stem.upper()}: {len(unique)} dialogues → {out_path.name}", "ok")
    return len(unique)


def _decode_single_script(idx, scripts_dir, output_dir):
    bf = scripts_dir / f"script_{idx:03d}.bin"
    if not bf.exists():
        bf = scripts_dir / f"script_{idx}.bin"
    if not bf.exists():
        return None

    raw = open(bf, "rb").read()
    if raw[:2] == b"\x1f\x8b":
        try:
            raw = gzip.decompress(raw)
        except:
            pass

    dlgs = find_dialogs(raw)
    out_json = output_dir / f"script_{idx:03d}.json"

    # Si un JSON traduit existe déjà, préserver les traductions
    if out_json.exists():
        try:
            existing = json.load(open(out_json, encoding="utf-8"))
            by_offset = {e["offset"]: e for e in existing}
            for d in dlgs:
                prev = by_offset.get(d["offset"])
                if prev:
                    d["nom_fr"] = prev.get("nom_fr", "")
                    d["texte_fr"] = prev.get("texte_fr", "")
                    if "choix_orig" in d:
                        d["question_fr"] = prev.get("question_fr", "")
                        # Récupérer choix_fr depuis prev si disponible, sinon depuis texte_fr
                        prev_choix = prev.get("choix_fr")
                        if prev_choix and len(prev_choix) == len(d["choix_orig"]):
                            d["choix_fr"] = prev_choix
        except Exception:
            pass

    migrate_choices_in_json(dlgs)
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(dlgs, f, ensure_ascii=False, indent=2)

    return len(dlgs)


def decode_all_scripts(
    scripts_dir: Path, output_dir: Path, log_fn=None, progress_fn=None
):
    """Décode tous les scripts_bin/*.bin en fichiers JSON prêts à traduire."""
    output_dir.mkdir(parents=True, exist_ok=True)
    total = vides = 0
    total_scripts = 399
    completed = 0

    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [
            executor.submit(_decode_single_script, idx, scripts_dir, output_dir)
            for idx in range(total_scripts)
        ]

        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            completed += 1
            if progress_fn:
                progress_fn(completed / total_scripts)
            if res is not None:
                total += 1
                if res == 0:
                    vides += 1

    if log_fn:
        log_fn(f"  {total} scripts décodés ({vides} vides) via ProcessPool", "ok")


# ── Validation cohérence menus de choix ───────────────────────────────────────


def migrate_choices_in_json(entries: list) -> list:
    """
    Migration : pour les entrées déjà traduites (texte_fr rempli) qui contiennent
    un menu de choix, peuple question_fr/choix_fr à partir du texte_fr existant.
    Les entrées sans texte_fr gardent question_fr="" et choix_fr=["","..."].
    """
    for e in entries:
        if "choix_orig" not in e:
            continue  # pas un menu de choix
        # Si question_fr/choix_fr déjà remplis, ne pas écraser
        if e.get("question_fr") or any(c.strip() for c in e.get("choix_fr", [])):
            continue
        t_fr = e.get("texte_fr", "").strip()
        if not t_fr:
            continue
        q_fr, opts_fr, c_tag = _parse_choices(t_fr)
        if opts_fr is not None and len(opts_fr) == len(e["choix_orig"]):
            e["question_fr"] = q_fr
            e["choix_fr"] = opts_fr
            if c_tag:
                e["count_tag"] = c_tag
        elif opts_fr is not None:
            # Nombre d'options différent — on met quand même ce qu'on a
            e["question_fr"] = q_fr
            e["choix_fr"] = opts_fr + [""] * max(0, len(e["choix_orig"]) - len(opts_fr))
            if c_tag:
                e["count_tag"] = c_tag
    return entries

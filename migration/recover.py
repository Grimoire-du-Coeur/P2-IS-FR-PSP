"""Recuperation des entrees scindees : quand le nouveau format coupe une ancienne
entree en plusieurs (au niveau des blocs d'intro de locuteur), on decoupe l'ancienne
traduction aux memes marqueurs et on distribue chaque morceau a la bonne entree.
Purement additif : ne remplit que les entrees nouvelles dont texte_fr est vide."""
import os
import sys
import re
import json
import glob

sys.path.insert(0, os.path.dirname(__file__))
from core import texte_nu, convert_fr, extract_codes  # noqa: E402
from byte_budget import cost, budget                  # noqa: E402

# Bloc d'intro de locuteur : (codes)[E4][NULL][NULL]"<nom>\n  -> separe deux repliques.
_DELIM = re.compile(r'\n?(?:\[(?:U\+)?[0-9A-Fa-f]{4}\]|\[E[1-9]\])*\[E4\]\[NULL\]\[NULL\]"[^\n]*\n')

_STRUCT_CODES = ("[1432]", "[E1]", "[E2]", "[E3]", "[E4]",
                 "[0002]", "[0014]", "[NULL]", "[U+0006]", "[0010]")


def split_speaker_segments(texte):
    """Decoupe un texte aux blocs d'intro de locuteur. Retourne la liste des segments."""
    return _DELIM.split(texte)


def speaker_spans(texte):
    """Toutes les plages contiguës de segments, delimiteurs INTERNES inclus.

    Le nouveau format ne scinde pas a chaque bloc locuteur : une nouvelle entree
    peut couvrir plusieurs repliques consecutives, blocs "Nom compris. On retourne
    (plages, nb_delimiteurs) ; les plages i==j sont les segments simples."""
    ms = list(_DELIM.finditer(texte))
    starts = [0] + [m.end() for m in ms]
    ends = [m.start() for m in ms] + [len(texte)]
    n = len(starts)
    return ([texte[starts[i]:ends[j]] for i in range(n) for j in range(i, n)],
            len(ms))


def _struct(s):
    return [c for c in extract_codes(s) if c in _STRUCT_CODES]


def build_segment_index(old):
    """{texte_nu(orig): convert_fr(fr)} depuis les anciennes entrees traduites.

    On indexe l'entree ENTIERE (cas ou le nouveau format garde l'ancienne entree
    telle quelle) ET chaque plage contigue de segments (cas ou le nouveau format
    l'a scindee a certains blocs d'intro de locuteur seulement). Les codes des
    delimiteurs etant identiques dans texte_orig et texte_fr, les deux se decoupent
    en autant de plages ; on ignore le decoupage d'une entree si le compte differe."""
    idx = {}
    for e in old:
        if not e.get("texte_fr", "").strip():
            continue
        to = e.get("texte_orig", "")
        tf = e.get("texte_fr", "")
        # Vieille entree "traduite" par copie de l'anglais (trad jamais faite) :
        # ne rien indexer, sinon on propagerait de l'anglais dans les texte_fr.
        if texte_nu(to) == texte_nu(tf):
            continue
        # 1) entree entiere
        nu = texte_nu(to)
        if nu and nu not in idx:
            idx[nu] = convert_fr(tf.strip())
        # 2) plages de segments
        so, no_delim = speaker_spans(to)
        sf, nf_delim = speaker_spans(tf)
        if no_delim != nf_delim:
            continue
        for o, f in zip(so, sf):
            snu = texte_nu(o)
            if snu and snu != texte_nu(f) and snu not in idx:
                idx[snu] = convert_fr(f.strip())
    return idx


def build_name_map(old):
    """{nom_orig: convert_fr(nom_fr)} depuis les anciennes entrees."""
    m = {}
    for e in old:
        no = e.get("nom_orig", "")
        nf = e.get("nom_fr", "")
        if no and nf and no not in m:
            m[no] = convert_fr(nf)
    return m


def fill_from_segments(old, new, extra_idx=None, extra_names=None):
    """Remplit les entrees NOUVELLES dont texte_fr est vide, depuis l'index de segments.

    `extra_idx`/`extra_names` : index global (tous scripts confondus) consulte en
    REPLI seulement — le meme script garde la priorite.
    Garde-fous : ne touche jamais une entree deja traduite ; n'ecrit que si la
    structure de balises correspond ET si le cout tient dans le budget.
    Retourne {filled, over_budget:[id], struct_diff:[id], no_match:[id]}."""
    idx = build_segment_index(old)
    names = build_name_map(old)
    extra_idx = extra_idx or {}
    extra_names = extra_names or {}
    report = {"filled": 0, "over_budget": [], "struct_diff": [], "no_match": []}
    for e in new:
        if e.get("texte_fr", "").strip():
            continue
        nu = texte_nu(e.get("texte_orig", ""))
        if not nu:
            continue
        fr = idx.get(nu) or extra_idx.get(nu)
        if not fr:
            report["no_match"].append(e["id"])
            continue
        nom = names.get(e.get("nom_orig", "")) or extra_names.get(e.get("nom_orig", ""), "")
        if _struct(e.get("texte_orig", "")) != _struct(fr):
            report["struct_diff"].append(e["id"])
            continue
        if cost(nom, fr) > budget(e):
            report["over_budget"].append(e["id"])
            continue
        e["texte_fr"] = fr
        if not e.get("nom_fr", "").strip():
            e["nom_fr"] = nom
        report["filled"] += 1
    return report


_PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _paths(token):
    m = re.search(r"(\d+)", token)
    num = m.group(1).zfill(3)
    name = f"script_{num}.json"
    return (os.path.join(_PROJ, "scripts", name),
            os.path.join(_PROJ, "traduction", "event_scripts", name))


def recover_file(old_path, new_path, extra_idx=None, extra_names=None):
    with open(old_path, encoding="utf-8") as f:
        old = json.load(f)
    with open(new_path, encoding="utf-8") as f:
        new = json.load(f)
    report = fill_from_segments(old, new, extra_idx, extra_names)
    if report["filled"]:
        with open(new_path, "w", encoding="utf-8") as f:
            json.dump(new, f, ensure_ascii=False, indent=2)
            f.write("\n")
    return report


def build_global_index():
    """Index (textes + noms) sur TOUT l'ancien scripts/, pour le repli inter-scripts."""
    g_idx, g_names = {}, {}
    for p in sorted(glob.glob(os.path.join(_PROJ, "scripts", "script_*.json"))):
        with open(p, encoding="utf-8") as f:
            old = json.load(f)
        for nu, fr in build_segment_index(old).items():
            g_idx.setdefault(nu, fr)
        for no, nf in build_name_map(old).items():
            g_names.setdefault(no, nf)
    return g_idx, g_names


def main(argv):
    if not argv:
        print("Usage: python migration/recover.py <numero|all>")
        return 1
    if argv[0] == "all":
        tokens = sorted(glob.glob(os.path.join(_PROJ, "scripts", "script_*.json")))
        tokens = [os.path.basename(p) for p in tokens]
    else:
        tokens = argv
    g_idx, g_names = build_global_index()
    tot = 0
    for tok in tokens:
        op, npth = _paths(tok)
        if not os.path.exists(npth):
            continue
        r = recover_file(op, npth, g_idx, g_names)
        tot += r["filled"]
        if r["filled"]:
            print(f"{os.path.basename(npth)}: +{r['filled']} recuperees "
                  f"(reste: {len(r['over_budget'])} hors-budget, "
                  f"{len(r['struct_diff'])} balises, {len(r['no_match'])} sans match)")
    print(f"TOTAL recuperees: {tot}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

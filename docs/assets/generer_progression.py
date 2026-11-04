#!/usr/bin/env python3
"""Fabrique le panneau d'avancement anime du README, a partir des JSON reels.

Le README et CONTRIBUTING.md annoncaient un EBOOT « a 15 % » longtemps apres
qu'il ait ete fini : des chiffres recopies a la main vieillissent toujours mal.
Ce script compte ce qui est reellement dans `traduction/`, pour que la
banniere d'avancement ne puisse plus mentir.

Une entree compte comme traduite si son champ `texte_fr` est non vide. Les
entrees sans `texte_orig` sont ignorees : ce sont des trous de la table, pas
du texte a traduire.

Usage : python docs/assets/generer_progression.py
"""

from __future__ import annotations

import glob
import json
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
RACINE = ICI.parent.parent

# (libelle, motif glob, precision affichee a droite)
SECTIONS = [
    ("Scripts d'évènement", "traduction/event_scripts/*.json", "399 fichiers"),
    ("EBOOT — menus & système", "traduction/EBOOT_decoupe/*.json", "7 parties"),
    ("MMAP — dialogues de carte", "traduction/MMAP*.json", "6 cartes"),
    ("TM_EVE — cinématiques", "traduction/TM_EVE.json", ""),
    ("F_BE — répliques de combat", "traduction/F_BE.json", ""),
    ("CD_SHOP — boutique de CD", "traduction/CD_SHOP.json", ""),
]

PALETTES = {
    "clair": {
        "fond_haut": "#e8411f", "fond_bas": "#c62b11", "encre": "#150603",
        "texte": "#2a0a04", "discret": "#4a1207", "rail": "#15060322",
        "barre": "#150603", "bordure": "#15060326",
    },
    "sombre": {
        "fond_haut": "#140604", "fond_bas": "#300b05", "encre": "#f7ece4",
        "texte": "#e5c9bd", "discret": "#bf7a66", "rail": "#f7ece41a",
        "barre": "#e0391a", "bordure": "#f7ece41f",
    },
}


def echapper(texte: str) -> str:
    sortie = []
    for caractere in texte:
        if caractere in "&<>":
            sortie.append({"&": "&amp;", "<": "&lt;", ">": "&gt;"}[caractere])
        elif ord(caractere) < 128:
            sortie.append(caractere)
        else:
            sortie.append("&#{};".format(ord(caractere)))
    return "".join(sortie)


def compter(motif: str) -> tuple:
    """Renvoie (traduites, total) pour tous les JSON correspondant au motif."""
    traduites = total = 0
    for chemin in sorted(glob.glob(str(RACINE / motif))):
        try:
            donnees = json.loads(Path(chemin).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as erreur:
            print("  ! illisible : {} ({})".format(chemin, erreur), file=sys.stderr)
            continue
        entrees = donnees if isinstance(donnees, list) else donnees.get("entrees", [])
        if not isinstance(entrees, list):
            continue
        for entree in entrees:
            if not isinstance(entree, dict):
                continue
            if not str(entree.get("texte_orig", "")).strip():
                continue
            total += 1
            if str(entree.get("texte_fr", "")).strip():
                traduites += 1
    return traduites, total


def pourcentage(valeur: float) -> str:
    """Virgule decimale francaise, et pas de « ,0 » inutile.

    Un arrondi ne doit jamais afficher 100 % tant qu'il reste une entree a
    traduire : 99,98 % devient « 99,9 », pas « 100 ».
    """
    texte = "{:.1f}".format(valeur)
    if texte == "100.0" and valeur < 100:
        texte = "99.9"
    texte = texte.replace(".", ",")
    return texte[:-2] if texte.endswith(",0") else texte


def espacer(nombre: int) -> str:
    """12345 -> 12 345, avec une espace insecable fine."""
    return "{:,}".format(nombre).replace(",", " ")


def construire(theme: str, mesures: list, traduites: int, total: int) -> str:
    p = PALETTES[theme]
    pourcent = (100 * traduites / total) if total else 0

    largeur_max = 620
    plus_gros = max(m[2] for m in mesures) or 1
    lignes = []
    y = 136
    for index, (libelle, detail, nombre, faites) in enumerate(mesures):
        largeur = max(14, round(largeur_max * nombre / plus_gros))
        part = (faites / nombre) if nombre else 0
        retard = 0.35 + index * 0.11
        pc = pourcentage(100 * part) + " %"
        lignes.append(
            '<g class="ligne" style="animation-delay:{t}s">'
            '<text x="56" y="{yt}" class="lib" fill="{fg}">{lib}</text>'
            '<rect x="320" y="{yb}" width="{w}" height="14" rx="2" fill="{rail}"/>'
            '<rect class="jauge" x="320" y="{yb}" width="{wf}" height="14" rx="2" '
            'fill="{barre}" style="animation-delay:{t2}s"/>'
            '<text x="{xn}" y="{yt}" class="val" fill="{fg2}">{nb}</text>'
            '<text x="1144" y="{yt}" class="pc" fill="{fg2}" text-anchor="end">{pc}</text>'
            "</g>".format(
                t=retard, t2=retard + 0.12, yt=y + 12, yb=y + 1,
                lib=echapper(libelle + ("  ·  " + detail if detail else "")),
                w=largeur, wf=round(largeur * part), rail=p["rail"],
                barre=p["barre"], fg=p["texte"], fg2=p["encre"],
                xn=320 + largeur + 14, nb=espacer(faites), pc=pc,
            )
        )
        y += 34

    return """<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{hauteur}"
     viewBox="0 0 1200 {hauteur}" role="img"
     aria-label="Avancement de la traduction : {traduites} entrees sur {total}">
  <title>Avancement de la traduction</title>
  <defs>
    <linearGradient id="fond" x1="0" y1="0" x2="0.3" y2="1">
      <stop offset="0%" stop-color="{fond_haut}"/>
      <stop offset="100%" stop-color="{fond_bas}"/>
    </linearGradient>
    <clipPath id="cadre"><rect width="1200" height="{hauteur}" rx="4"/></clipPath>
  </defs>
  <style>
    .ligne {{ opacity: 0; animation: monte .6s cubic-bezier(.2,.75,.3,1) forwards; }}
    @keyframes monte {{ from {{ opacity: 0; transform: translateY(10px); }}
                        to   {{ opacity: 1; transform: translateY(0); }} }}
    .jauge {{ transform-origin: 320px center;
              animation: remplir 5s cubic-bezier(.25,.8,.3,1) infinite; }}
    @keyframes remplir {{ 0%        {{ transform: scaleX(0); }}
                          32%, 84%  {{ transform: scaleX(1); }}
                          100%      {{ transform: scaleX(0); }} }}
    .entete {{ opacity: 0; animation: monte .7s cubic-bezier(.2,.75,.3,1) .1s forwards; }}
    @media (prefers-reduced-motion: reduce) {{
      .ligne, .jauge, .entete {{ animation: none; opacity: 1; transform: none; }}
    }}
    .titre {{ font: 700 26px 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
              letter-spacing: 1px; }}
    .chapeau {{ font: 600 13px 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
                letter-spacing: 3.6px; }}
    .lib {{ font: 600 14px 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }}
    .val {{ font: 700 13px 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }}
    .pc  {{ font: 700 14px 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }}
  </style>
  <g clip-path="url(#cadre)">
    <rect width="1200" height="{hauteur}" fill="url(#fond)"/>
    <g class="entete">
      <text x="56" y="56" class="chapeau" fill="{discret}">AVANCEMENT DE LA TRADUCTION</text>
      <text x="56" y="98" class="titre" fill="{encre}">{traduites_fmt} / {total_fmt} entrées &#183; {pourcent}&#8239;%</text>
    </g>
    {lignes}
    <rect x="1" y="1" width="1198" height="{bord_h}" rx="4" fill="none"
          stroke="{bordure}" stroke-width="2"/>
  </g>
</svg>
""".format(
        hauteur=y + 26, bord_h=y + 24, lignes="\n    ".join(lignes),
        traduites=traduites, total=total,
        traduites_fmt=espacer(traduites), total_fmt=espacer(total),
        pourcent=pourcentage(pourcent), **p,
    )


def main() -> int:
    mesures = []
    traduites_tot = total_tot = 0
    for libelle, motif, detail in SECTIONS:
        faites, nombre = compter(motif)
        if nombre == 0:
            print("  ! section vide, ignoree : {}".format(libelle), file=sys.stderr)
            continue
        mesures.append((libelle, detail, nombre, faites))
        traduites_tot += faites
        total_tot += nombre
        print("{:30} {:>6} / {:<6}".format(libelle, faites, nombre))

    if not mesures:
        print("Aucune donnee de traduction trouvee.", file=sys.stderr)
        return 1

    print("{:30} {:>6} / {:<6}".format("TOTAL", traduites_tot, total_tot))
    for theme in PALETTES:
        cible = ICI / "progression-{}.svg".format(theme)
        cible.write_text(
            construire(theme, mesures, traduites_tot, total_tot), encoding="utf-8"
        )
        print("{} ecrit".format(cible.name))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

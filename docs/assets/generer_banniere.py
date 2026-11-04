#!/usr/bin/env python3
"""Fabrique la banniere animee du README (theme clair + theme sombre).

Direction artistique : celle d'Innocent Sin, pas une invention. Le jeu se
reconnait a un vermillon plat, du noir, une typo capitale tres serree et le
sceau du kanji 罪 (« faute »). C'est la charte de la pochette du Mini
Soundtrack. Eternal Punishment est le pendant bleu : ne pas melanger les deux
est le seul point non negociable de ce fichier.

Le rendu GitHub d'un README n'execute pas de JavaScript et ne charge pas de
police distante, mais il affiche un SVG via <img> : les animations CSS placees
*dans* le SVG tournent, et une image encodee en base64 dans ce meme SVG
s'affiche. C'est le seul moyen d'avoir une banniere animee sans GIF.

L'illustration garde ses couleurs d'origine : le vermillon est le decor, pas un
filtre pose sur le personnage. Elle est seulement recadree, redimensionnee,
reencodee en WebP et inlinee.

Usage : python docs/assets/generer_banniere.py [source.webp]
"""

from __future__ import annotations

import base64
import io
import sys
from pathlib import Path

from PIL import Image

ICI = Path(__file__).resolve().parent
SOURCE_PAR_DEFAUT = ICI / "tatsuya.webp"
HAUTEUR_PERSO = 520

# Le vermillon de reference, releve sur la pochette du Mini Soundtrack.
VERMILLON = "#e0391a"

PALETTES = {
    # Pochette : fond vermillon, encre noire.
    "clair": {
        "fond_haut": "#e8411f",
        "fond_bas": "#c62b11",
        "encre": "#150603",
        "titre": "#150603",
        "bandeau": "#150603",
        "bandeau_texte": "#f7ece4",
        "texte": "#2a0a04",
        "discret": "#330c04",
        "puce_fond": "#15060314",
        "puce_bord": "#15060340",
        "bordure": "#15060326",
        "sceau": "#150603",
    },
    # Revers : fond encre, vermillon en lumiere.
    "sombre": {
        "fond_haut": "#140604",
        "fond_bas": "#300b05",
        "encre": "#f7ece4",
        "titre": "#f7ece4",
        "bandeau": VERMILLON,
        "bandeau_texte": "#140604",
        "texte": "#e5c9bd",
        "discret": "#bf7a66",
        "puce_fond": "#f7ece40f",
        "puce_bord": "#f7ece42e",
        "bordure": "#f7ece41f",
        "sceau": VERMILLON,
    },
}

SURTITRE = "FAN-TRADUCTION FRANÇAISE · PSP ULES01557"
SLOGAN = "« Les rumeurs deviennent réalité. »"
VERTICAL = "GRIMOIRE DU CŒUR"

PASTILLES = [
    ("Scénario principal", "100 %"),
    ("Scripts traduits", "399"),
    ("Version", "v0.2.8-bêta"),
]

# Pile de polices CJK : le sceau 罪 doit tomber sur une vraie police japonaise,
# sinon il s'affiche en tofu. On ratisse Windows, macOS et Linux.
POLICES_CJK = (
    "'Yu Mincho','Yu Gothic','MS Gothic','Hiragino Mincho ProN',"
    "'Hiragino Sans','Noto Serif CJK JP','Noto Sans CJK JP',"
    "'Source Han Sans JP','Microsoft YaHei',serif"
)


def echapper(texte: str) -> str:
    """Rend le texte sur en XML : tout ce qui n'est pas ASCII passe en entite.

    Le SVG est declare en UTF-8, mais un README se fait relire, recopier et
    reenregistrer par des editeurs qui ne respectent pas toujours l'encodage.
    Des entites numeriques survivent a ca, un « é » brut pas toujours.
    """
    sortie = []
    for caractere in texte:
        if caractere in "&<>":
            sortie.append({"&": "&amp;", "<": "&lt;", ">": "&gt;"}[caractere])
        elif ord(caractere) < 128:
            sortie.append(caractere)
        else:
            sortie.append("&#{};".format(ord(caractere)))
    return "".join(sortie)


def encoder_illustration(source: Path) -> tuple:
    """Recadre, redimensionne et encode l'illustration en data URI WebP."""
    image = Image.open(source).convert("RGBA")
    boite = image.getbbox()
    if boite:
        image = image.crop(boite)
    largeur = round(image.width * HAUTEUR_PERSO / image.height)
    image = image.resize((largeur, HAUTEUR_PERSO), Image.LANCZOS)

    tampon = io.BytesIO()
    image.save(tampon, format="WEBP", quality=84, method=6)
    donnees = base64.b64encode(tampon.getvalue()).decode("ascii")
    return "data:image/webp;base64," + donnees, largeur


def pastilles(p: dict) -> str:
    morceaux = []
    x = 62
    for index, (libelle, valeur) in enumerate(PASTILLES):
        largeur = 22 + max(len(libelle) * 6.6, len(valeur) * 9.4)
        retard = 1.25 + index * 0.12
        morceaux.append(
            '<g class="monte" style="animation-delay:{t}s">'
            '<rect x="{x}" y="306" width="{w:.0f}" height="52" rx="2" '
            'fill="{bg}" stroke="{bd}"/>'
            '<text x="{xt}" y="327" class="puce-lib" fill="{fg1}">{lib}</text>'
            '<text x="{xt}" y="348" class="puce-val" fill="{fg2}">{val}</text>'
            "</g>".format(
                t=retard, x=x, w=largeur, bg=p["puce_fond"], bd=p["puce_bord"],
                xt=x + 13, fg1=p["discret"], fg2=p["encre"],
                lib=echapper(libelle), val=echapper(valeur),
            )
        )
        x += largeur + 13
    return "\n    ".join(morceaux)


GABARIT = """<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="420"
     viewBox="0 0 1200 420" role="img"
     aria-label="Persona 2 Innocent Sin - traduction francaise">
  <title>Persona 2: Innocent Sin - Traduction francaise</title>
  <defs>
    <linearGradient id="fond" x1="0" y1="0" x2="0.3" y2="1">
      <stop offset="0%" stop-color="{fond_haut}"/>
      <stop offset="100%" stop-color="{fond_bas}"/>
    </linearGradient>
    <radialGradient id="vignette" cx="46%" cy="45%" r="64%">
      <stop offset="55%" stop-color="#000000" stop-opacity="0"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.28"/>
    </radialGradient>
    <radialGradient id="assise" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#150603" stop-opacity="0.38"/>
      <stop offset="100%" stop-color="#150603" stop-opacity="0"/>
    </radialGradient>
    <clipPath id="cadre"><rect width="1200" height="420" rx="4"/></clipPath>
    <clipPath id="bandeau-masque"><rect x="58" y="194" width="580" height="48"/></clipPath>
  </defs>

  <style>
    .surgit {{ opacity: 0; animation: surgit .85s cubic-bezier(.2,.75,.3,1) forwards; }}
    .monte  {{ opacity: 0; animation: monte  .7s cubic-bezier(.2,.75,.3,1) forwards; }}
    @keyframes surgit {{ from {{ opacity: 0; transform: translateX(-30px); }}
                         to   {{ opacity: 1; transform: translateX(0); }} }}
    @keyframes monte  {{ from {{ opacity: 0; transform: translateY(14px); }}
                         to   {{ opacity: 1; transform: translateY(0); }} }}

    .perso {{ opacity: 0; transform-origin: 50% 100%;
              animation: entree-perso 1.3s cubic-bezier(.2,.75,.3,1) .1s forwards,
                         flotte 8s ease-in-out 1.5s infinite; }}
    @keyframes entree-perso {{ from {{ opacity: 0; transform: translateY(30px) scale(.99); }}
                               to   {{ opacity: 1; transform: translateY(0) scale(1); }} }}
    @keyframes flotte {{ 0%,100% {{ transform: translateY(0); }}
                         50%     {{ transform: translateY(-10px); }} }}

    /* Le bandeau se deroule depuis la gauche, comme un trait de pinceau. */
    .bandeau {{ transform-origin: left center;
                animation: deroule .7s cubic-bezier(.25,.8,.3,1) .5s both; }}
    .trait   {{ transform-origin: left center;
                animation: deroule .8s cubic-bezier(.25,.8,.3,1) 1s both; }}
    @keyframes deroule {{ from {{ transform: scaleX(0); }} to {{ transform: scaleX(1); }} }}

    /* Le sceau se pose : il arrive trop grand, de travers, puis se plaque. */
    .sceau {{ opacity: 0; transform-origin: 1128px 300px;
              animation: appose .7s cubic-bezier(.2,1.45,.4,1) 1.55s forwards; }}
    @keyframes appose {{ from {{ opacity: 0; transform: scale(1.55) rotate(-8deg); }}
                         to   {{ opacity: 1; transform: scale(1) rotate(0deg); }} }}

    .vertical {{ opacity: 0; animation: monte .9s ease-out 1.95s forwards; }}

    @media (prefers-reduced-motion: reduce) {{
      .surgit, .monte, .perso, .bandeau, .trait, .sceau, .vertical {{
        animation: none; opacity: 1; transform: none;
      }}
    }}

    .surtitre {{ font: 600 14px 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
                 letter-spacing: 4.6px; }}
    .t1 {{ font: 800 78px 'Arial Narrow', 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
           letter-spacing: -2.5px; }}
    .t2 {{ font: 700 26px 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
           letter-spacing: 11px; }}
    .slogan {{ font: italic 400 19px Georgia, 'Times New Roman', serif; }}
    .puce-lib {{ font: 600 10.5px 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
                 letter-spacing: 1.5px; }}
    .puce-val {{ font: 700 17px 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }}
    .kanji {{ font: 400 56px {cjk}; }}
    .cote {{ font: 600 12px 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
             letter-spacing: 6px; }}
  </style>

  <g clip-path="url(#cadre)">
    <rect width="1200" height="420" fill="url(#fond)"/>

    <ellipse class="perso" cx="{assise_x}" cy="300" rx="250" ry="190" fill="url(#assise)"/>
    <image class="perso" x="{perso_x}" y="-16" width="{perso_w}" height="{perso_h}"
           href="{illustration}" preserveAspectRatio="xMidYMax meet"/>

    <rect width="1200" height="420" fill="url(#vignette)"/>

    <text x="62" y="84" class="surtitre surgit" fill="{discret}"
          style="animation-delay:.12s">{surtitre}</text>

    <text x="56" y="174" class="t1 surgit" fill="{titre}"
          style="animation-delay:.28s">PERSONA 2</text>

    <g clip-path="url(#bandeau-masque)">
      <rect class="bandeau" x="58" y="194" width="462" height="48" fill="{bandeau}"/>
    </g>
    <text x="76" y="226" class="t2 surgit" fill="{bandeau_texte}"
          style="animation-delay:.78s">INNOCENT SIN</text>

    <rect class="trait" x="60" y="262" width="168" height="3" fill="{bandeau}"/>

    <text x="60" y="292" class="slogan surgit" fill="{texte}"
          style="animation-delay:1.05s">{slogan}</text>

    {pastilles}

    <g class="sceau">
      <rect x="1090" y="262" width="76" height="76" fill="none"
            stroke="{sceau}" stroke-width="3"/>
      <text x="1128" y="318" class="kanji" fill="{sceau}"
            text-anchor="middle">&#32618;</text>
    </g>

    <rect x="1" y="1" width="1198" height="418" rx="4" fill="none"
          stroke="{bordure}" stroke-width="2"/>
  </g>
</svg>
"""


def construire(theme: str, illustration: str, largeur_perso: int) -> str:
    p = PALETTES[theme]
    return GABARIT.format(
        pastilles=pastilles(p),
        illustration=illustration,
        perso_x=1200 - largeur_perso - 148,
        assise_x=1200 - largeur_perso // 2 - 148,
        perso_w=largeur_perso,
        perso_h=HAUTEUR_PERSO,
        surtitre=echapper(SURTITRE),
        slogan=echapper(SLOGAN),
        vertical=echapper(VERTICAL),
        cjk=POLICES_CJK,
        **p,
    )


def main() -> int:
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else SOURCE_PAR_DEFAUT
    if not source.exists():
        print("Illustration introuvable : {}".format(source), file=sys.stderr)
        return 1

    illustration, largeur = encoder_illustration(source)
    for theme in PALETTES:
        cible = ICI / "banniere-{}.svg".format(theme)
        cible.write_text(construire(theme, illustration, largeur), encoding="utf-8")
        print("{} : {:.0f} Ko".format(cible.name, cible.stat().st_size / 1024))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

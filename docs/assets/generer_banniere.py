#!/usr/bin/env python3
"""Fabrique les visuels animés du README : bannière et séparateur.

    python docs/assets/generer_banniere.py     # -> docs/assets/banniere.svg, separateur.svg

Direction artistique : celle d'Innocent Sin. Un vermillon plat, du noir, une
capitale très serrée et le sceau du kanji 罪 (« faute ») : la charte de la
pochette du Mini Soundtrack. Eternal Punishment est le pendant bleu ; ne pas
mélanger les deux reste le seul point non négociable de ce fichier.

La scène : Sumaru la nuit, ses fenêtres qui s'allument et s'éteignent, les
papillons dorés de Philémon, Tatsuya devant la ville, le sceau 罪 qui
s'appose, et un bandeau de rumeurs qui défile. Les rumeurs sont de vraies
répliques de la traduction (traduction/), à peine raccourcies.

Le texte est vectorisé (fontTools + polices Windows) : GitHub sert les SVG du
README via <img>, ce qui bloque toute police externe, et un <text> vivant
s'afficherait différemment selon l'OS. L'illustration de Tatsuya garde ses
couleurs d'origine ; elle est recadrée, réduite, encodée en WebP et inlinée.
Les animations sont en CSS ; avec « réduire les animations », tout s'affiche
à l'arrêt.

Dépendances de développement : fontTools, Pillow.
"""

from __future__ import annotations

import base64
import io
import random
import re
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from PIL import Image

ICI = Path(__file__).resolve().parent
POLICES = Path("C:/Windows/Fonts")
ILLUSTRATION = ICI / "tatsuya.webp"

VERMILLON = "#e0391a"
ENCRE = "#150603"
CREME = "#f7ece4"
DISCRET = "#d98a73"
OR, OR_PALE = "#f2b544", "#ffe3a3"
BLEU_GRIMOIRE, BLANC_GRIMOIRE, ROUGE_GRIMOIRE = "#002654", "#F5F5F5", "#CE1126"

SURTITRE = "FAN-TRADUCTION FRANÇAISE  ·  PSP  ·  ULES01557"
SLOGAN = "« Les rumeurs deviennent réalité. »"
RUMEURS = [
    "« On dit que le jeu du Joker peut exaucer n’importe quel vœu. »",
    "« La rumeur dit que le ramen de l’allée Kameya vend des armes. »",
    "« On dit que quiconque possède la Lance du Destin dominera le monde. »",
    "« La rumeur dit qu’une fois dans l’abri anti-aérien, on ne peut plus sortir. »",
    "« On dit que celui qui a maudit notre emblème serait un élève de Kasu. »",
]


class Police:
    def __init__(self, fichier: str, numero: int = 0):
        self.f = TTFont(POLICES / fichier, fontNumber=numero)
        self.glyphes = self.f.getGlyphSet()
        self.cmap = self.f.getBestCmap()
        self.em = self.f["head"].unitsPerEm

    def largeur(self, texte: str, taille: float, espacement: float = 0) -> float:
        k = taille / self.em
        return sum(self.glyphes[self.cmap[ord(c)]].width * k + espacement for c in texte) - espacement

    def chemin(self, texte: str, x: float, y: float, taille: float, espacement: float = 0) -> str:
        """Tracé SVG du texte, ligne de base en (x, y)."""
        k = taille / self.em
        morceaux = []
        for c in texte:
            nom = self.cmap[ord(c)]
            stylo = SVGPathPen(self.glyphes)
            self.glyphes[nom].draw(TransformPen(stylo, (k, 0, 0, -k, x, y)))
            morceaux.append(stylo.getCommands())
            x += self.glyphes[nom].width * k + espacement
        return _arrondir(" ".join(m for m in morceaux if m))

    def centre(self, texte: str, cx: float, y: float, taille: float, espacement: float = 0) -> str:
        return self.chemin(texte, cx - self.largeur(texte, taille, espacement) / 2, y, taille, espacement)


def _arrondir(trace: str) -> str:
    """Une décimale suffit à cette échelle : le fichier pèse quatre fois moins."""
    return re.sub(r"-?\d+\.\d+", lambda m: _n(float(m.group())), trace)


def _n(v: float) -> str:
    return f"{v:.1f}".rstrip("0").rstrip(".")


def _illustration(hauteur: int) -> tuple[str, int]:
    image = Image.open(ILLUSTRATION).convert("RGBA")
    image = image.crop(image.getbbox())
    largeur = round(image.width * hauteur / image.height)
    image = image.resize((largeur, hauteur), Image.LANCZOS)
    tampon = io.BytesIO()
    image.save(tampon, format="WEBP", quality=84, method=6)
    return "data:image/webp;base64," + base64.b64encode(tampon.getvalue()).decode("ascii"), largeur


def _papillon(cls: str) -> str:
    """Un papillon de Philémon centré en (0, 0) ; les ailes battent autour du corps."""
    haute = "M0,-1 C5,-15 21,-19 19,-6 C18,0 8,2 0,0 Z"
    basse = "M0,1 C8,2 16,8 11,15 C7,19 2,10 0,3 Z"
    ailes = f'<path d="{haute}"/><path d="{basse}"/>'
    return (f'<g class="{cls}" fill="url(#or)" filter="url(#lueur)">'
            f'<g class="aile">{ailes}</g>'
            f'<g transform="scale(-1,1)"><g class="aile">{ailes}</g></g>'
            f'<ellipse cx="0" cy="2" rx="1.6" ry="7.5" fill="{OR_PALE}"/>'
            f'<path d="M-.6,-5 C-3,-11 -5,-13 -7,-14 M.6,-5 C3,-11 5,-13 7,-14" '
            f'stroke="{OR_PALE}" stroke-width="1" fill="none"/></g>')


# ---------------------------------------------------------------- bannière

def banniere() -> str:
    W, H, BANDE = 1200, 440, 388
    noire = Police("seguibl.ttf")       # Segoe UI Black
    grasse = Police("segoeuib.ttf")     # Segoe UI Bold
    italique = Police("georgiai.ttf")   # Georgia Italic
    kanji = Police("YuGothB.ttc")       # Yu Gothic Bold
    rnd = random.Random(1999)           # sortie japonaise d'Innocent Sin : rendu reproductible

    # Sumaru la nuit : silhouettes d'immeubles, fenêtres qui clignotent.
    immeubles, fenetres = [], []
    x = -10
    while x < W:
        w = rnd.randint(34, 78)
        # Bas à gauche, sous le slogan ; plus hauts derrière Tatsuya.
        h = rnd.randint(18, 46) if x < 640 else rnd.randint(50, 140)
        immeubles.append(f'<rect x="{x}" y="{BANDE - h}" width="{w}" height="{h}"/>')
        for fy in range(BANDE - h + 8, BANDE - 6, 11):
            for fx in range(x + 6, x + w - 6, 9):
                if rnd.random() < (0.12 if x < 640 else 0.22):
                    fenetres.append(f'<rect class="f{rnd.randint(0, 3)}" x="{fx}" y="{fy}" '
                                    f'width="4" height="5"/>')
        x += w + rnd.randint(-6, 4)

    # Titre
    surtitre = grasse.chemin(SURTITRE, 62, 92, 14.5, 4.2)
    persona = noire.chemin("PERSONA 2", 56, 192, 100, -1.5)
    innocent = noire.chemin("INNOCENT SIN", 78, 248, 27, 10.5)
    slogan = italique.chemin(SLOGAN, 61, 318, 22)
    grimoire = grasse.chemin("GRIMOIRE DU CŒUR", 150, 360, 12.5, 4)

    # Sceau 罪
    sceau = kanji.centre("罪", 1126, 316, 58)

    # Bandeau de rumeurs : le texte est écrit deux fois pour boucler sans saut.
    taille, pas_puce = 17, 46
    morceaux, puces, cx = [], [], 0.0
    for r in RUMEURS:
        morceaux.append(grasse.chemin(r, cx, 0, taille))
        cx += grasse.largeur(r, taille)
        puces.append(f'<rect x="{_n(cx + pas_puce / 2 - 4)}" y="-10" width="8" height="8" '
                     f'transform="rotate(45 {_n(cx + pas_puce / 2)} -6)" fill="{VERMILLON}"/>')
        cx += pas_puce
    boucle = cx
    texte_rumeurs = " ".join(morceaux)
    duree = boucle / 62
    rumeurs = (f'<g><path d="{texte_rumeurs}" fill="{CREME}"/>{"".join(puces)}</g>'
               f'<g transform="translate({_n(boucle)} 0)"><path d="{texte_rumeurs}" fill="{CREME}"/>'
               f'{"".join(puces)}</g>')
    uwasa = kanji.centre("噂", 36, BANDE + 35, 26)
    etiquette = noire.chemin("RUMEURS", 60, BANDE + 32, 15, 2.6)
    ETIQUETTE = 60 + noire.largeur("RUMEURS", 15, 2.6) + 20

    illustration, largeur = _illustration(410)
    perso_x = 1062 - largeur

    # Trame de points, à la Persona, qui s'efface vers la droite.
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Persona 2: Innocent Sin — traduction française (PSP)">
<title>Persona 2: Innocent Sin — traduction française</title>
<defs>
  <linearGradient id="ciel" x1="0" y1="0" x2="0.25" y2="1">
    <stop offset="0" stop-color="#1c0704"/><stop offset=".62" stop-color="#3a0d06"/>
    <stop offset="1" stop-color="#5a1408"/>
  </linearGradient>
  <radialGradient id="halo" cx=".5" cy=".5" r=".5">
    <stop offset="0" stop-color="{VERMILLON}" stop-opacity=".55"/>
    <stop offset="1" stop-color="{VERMILLON}" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="vignette" cx=".45" cy=".42" r=".75">
    <stop offset=".6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".45"/>
  </radialGradient>
  <linearGradient id="or" x1="0" y1="-1" x2="0" y2="1">
    <stop offset="0" stop-color="{OR_PALE}"/><stop offset="1" stop-color="{OR}"/>
  </linearGradient>
  <linearGradient id="effacement" x1="0" x2="1">
    <stop offset="0" stop-color="#fff" stop-opacity=".9"/><stop offset=".55" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
  <pattern id="trame" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(30)">
    <circle cx="2" cy="2" r="1.3" fill="{VERMILLON}"/>
  </pattern>
  <mask id="masque-trame"><rect width="{W}" height="{H}" fill="url(#effacement)"/></mask>
  <filter id="lueur" x="-1" y="-1" width="3" height="3">
    <feGaussianBlur stdDeviation="2.2" result="flou"/>
    <feMerge><feMergeNode in="flou"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <clipPath id="cadre"><rect width="{W}" height="{H}" rx="6"/></clipPath>
  <clipPath id="bande-texte"><rect x="{_n(ETIQUETTE)}" y="{BANDE}" width="{_n(W - ETIQUETTE)}" height="{H - BANDE}"/></clipPath>
  <clipPath id="bandeau-masque"><rect x="58" y="212" width="470" height="50"/></clipPath>
</defs>
<style>
  .surgit {{ opacity: 0; animation: surgit .85s cubic-bezier(.2,.75,.3,1) forwards; }}
  @keyframes surgit {{ from {{ opacity: 0; transform: translateX(-28px); }} to {{ opacity: 1; transform: none; }} }}
  .deroule {{ transform-origin: 58px 0; animation: deroule .7s cubic-bezier(.25,.8,.3,1) .5s both; }}
  .trait {{ transform-origin: 60px 0; animation: deroule .8s cubic-bezier(.25,.8,.3,1) 1s both; }}
  @keyframes deroule {{ from {{ transform: scaleX(0); }} to {{ transform: scaleX(1); }} }}
  .perso {{ opacity: 0; animation: perso 1.3s cubic-bezier(.2,.75,.3,1) .15s forwards; }}
  @keyframes perso {{ from {{ opacity: 0; transform: translateY(26px); }} to {{ opacity: 1; transform: none; }} }}
  .halo {{ animation: halo 5s ease-in-out infinite; }}
  @keyframes halo {{ 0%,100% {{ opacity: .75; }} 50% {{ opacity: 1; }} }}
  .sceau {{ opacity: 0; transform-origin: 1126px 296px; animation: appose .7s cubic-bezier(.2,1.45,.4,1) 1.6s forwards; }}
  @keyframes appose {{ from {{ opacity: 0; transform: scale(1.6) rotate(-9deg); }} to {{ opacity: 1; transform: none; }} }}
  .f0 {{ animation: fenetre 7s steps(1) infinite; }}
  .f1 {{ animation: fenetre 11s steps(1) 2s infinite; }}
  .f2 {{ animation: fenetre 13s steps(1) 5s infinite; }}
  .f3 {{ opacity: .85; }}
  @keyframes fenetre {{ 0%,100% {{ opacity: .85; }} 40% {{ opacity: .12; }} 70% {{ opacity: .85; }} }}
  .defile {{ animation: defile {_n(duree)}s linear infinite; }}
  @keyframes defile {{ from {{ transform: translateX(0); }} to {{ transform: translateX(-{_n(boucle)}px); }} }}
  .aile {{ transform-origin: 0 0; animation: bat .55s ease-in-out infinite alternate; }}
  @keyframes bat {{ from {{ transform: scaleX(1); }} to {{ transform: scaleX(.22); }} }}
  .vol1 {{ animation: vol1 9s ease-in-out infinite; }}
  .vol2 {{ animation: vol2 11s ease-in-out infinite; }}
  .vol3 {{ animation: vol3 13s ease-in-out infinite; }}
  @keyframes vol1 {{ 0%,100% {{ transform: translate(0,0) rotate(-8deg); }} 50% {{ transform: translate(34px,-22px) rotate(10deg); }} }}
  @keyframes vol2 {{ 0%,100% {{ transform: translate(0,0) rotate(12deg); }} 50% {{ transform: translate(-28px,18px) rotate(-6deg); }} }}
  @keyframes vol3 {{ 0%,100% {{ transform: translate(0,0) rotate(4deg); }} 50% {{ transform: translate(20px,-30px) rotate(-12deg); }} }}
  @media (prefers-reduced-motion: reduce) {{
    .surgit, .deroule, .trait, .perso, .halo, .sceau, .f0, .f1, .f2, .defile, .aile, .vol1, .vol2, .vol3 {{
      animation: none; opacity: 1; transform: none;
    }}
  }}
</style>
<g clip-path="url(#cadre)">
  <rect width="{W}" height="{H}" fill="url(#ciel)"/>
  <rect width="{W}" height="{H}" fill="url(#trame)" mask="url(#masque-trame)" opacity=".16"/>
  <ellipse class="halo" cx="{_n(perso_x + largeur / 2)}" cy="230" rx="300" ry="230" fill="url(#halo)"/>
  <g fill="#0b0302">{"".join(immeubles)}</g>
  <g fill="{OR}">{"".join(fenetres)}</g>
  <image class="perso" x="{perso_x}" y="{BANDE - 410}" width="{largeur}" height="410" href="{illustration}"/>
  <rect width="{W}" height="{H}" fill="url(#vignette)"/>

  <path class="surgit" style="animation-delay:.1s" d="{surtitre}" fill="{DISCRET}"/>
  <path class="surgit" style="animation-delay:.25s" d="{persona}" fill="{CREME}"/>
  <g clip-path="url(#bandeau-masque)"><rect class="deroule" x="58" y="212" width="470" height="50" fill="{VERMILLON}"/></g>
  <path class="surgit" style="animation-delay:.8s" d="{innocent}" fill="{ENCRE}"/>
  <rect class="trait" x="60" y="282" width="170" height="3" fill="{VERMILLON}"/>
  <path class="surgit" style="animation-delay:1.05s" d="{slogan}" fill="#ecd3c8"/>
  <g class="surgit" style="animation-delay:1.3s">
    <rect x="62" y="351" width="24" height="5" fill="{BLEU_GRIMOIRE}"/>
    <rect x="86" y="351" width="24" height="5" fill="{BLANC_GRIMOIRE}"/>
    <rect x="110" y="351" width="24" height="5" fill="{ROUGE_GRIMOIRE}"/>
    <path d="{grimoire}" fill="#c99482"/>
  </g>

  <g class="sceau">
    <rect x="1086" y="256" width="80" height="80" fill="none" stroke="{VERMILLON}" stroke-width="3.5"/>
    <path d="{sceau}" fill="{VERMILLON}"/>
  </g>

  <g transform="translate(690 96) scale(1.2)"><g class="vol1">{_papillon("p")}</g></g>
  <g transform="translate(1112 96)"><g class="vol2">{_papillon("p")}</g></g>
  <g transform="translate(590 300) scale(.75)"><g class="vol3">{_papillon("p")}</g></g>

  <rect y="{BANDE}" width="{W}" height="{H - BANDE}" fill="{ENCRE}"/>
  <rect y="{BANDE}" width="{W}" height="2" fill="{VERMILLON}"/>
  <g clip-path="url(#bande-texte)">
    <g transform="translate({_n(ETIQUETTE + 20)} {BANDE + 33})"><g class="defile">{rumeurs}</g></g>
  </g>
  <rect y="{BANDE}" width="{_n(ETIQUETTE)}" height="{H - BANDE}" fill="{VERMILLON}"/>
  <path d="{uwasa}" fill="{ENCRE}"/>
  <path d="{etiquette}" fill="{ENCRE}"/>
  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="6" fill="none" stroke="#f7ece4" stroke-opacity=".12" stroke-width="2"/>
</g>
</svg>
'''


# ---------------------------------------------------------------- séparateur

def separateur() -> str:
    W, H = 1200, 46
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="">
<defs>
  <linearGradient id="ligne" x1="0" x2="1">
    <stop offset="0" stop-color="{VERMILLON}" stop-opacity="0"/>
    <stop offset=".5" stop-color="{VERMILLON}"/>
    <stop offset="1" stop-color="{VERMILLON}" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="eclat" x1="0" x2="1">
    <stop offset="0" stop-color="{OR_PALE}" stop-opacity="0"/>
    <stop offset=".5" stop-color="{OR_PALE}"/>
    <stop offset="1" stop-color="{OR_PALE}" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="or" x1="0" y1="-1" x2="0" y2="1">
    <stop offset="0" stop-color="{OR_PALE}"/><stop offset="1" stop-color="{OR}"/>
  </linearGradient>
  <filter id="lueur" x="-1" y="-1" width="3" height="3">
    <feGaussianBlur stdDeviation="2" result="flou"/>
    <feMerge><feMergeNode in="flou"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <clipPath id="ligne-masque"><rect x="0" y="20" width="{W}" height="6"/></clipPath>
</defs>
<style>
  .eclat {{ animation: eclat 4.5s ease-in-out infinite; }}
  @keyframes eclat {{ from {{ transform: translateX(-200px); }} to {{ transform: translateX({W}px); }} }}
  .aile {{ transform-origin: 0 0; animation: bat .55s ease-in-out infinite alternate; }}
  @keyframes bat {{ from {{ transform: scaleX(1); }} to {{ transform: scaleX(.22); }} }}
  @media (prefers-reduced-motion: reduce) {{ .eclat, .aile {{ animation: none; transform: none; }} .eclat {{ opacity: 0; }} }}
</style>
<rect x="0" y="22" width="{W}" height="2" fill="url(#ligne)"/>
<g clip-path="url(#ligne-masque)"><rect class="eclat" x="0" y="21" width="160" height="4" fill="url(#eclat)"/></g>
<g transform="translate(600 24)">{_papillon("p")}</g>
</svg>
'''


def main() -> int:
    for nom, contenu in (("banniere.svg", banniere()), ("separateur.svg", separateur())):
        cible = ICI / nom
        cible.write_text(contenu, encoding="utf-8", newline="\n")
        print(f"{nom} : {cible.stat().st_size / 1024:.0f} Ko")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

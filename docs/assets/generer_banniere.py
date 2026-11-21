#!/usr/bin/env python3
"""Fabrique les visuels animés du README : bannière et séparateur.

    python docs/assets/generer_banniere.py     # -> docs/assets/banniere.svg, separateur.svg

Même construction que les bannières de Persona (P1-FR-PSP) et de Persona Q2
(PQ2-FR-3DS) : un titre centré et lumineux dans un décor qui raconte le jeu,
puis la ligne « traduction française » et le ruban tricolore du Grimoire.

Direction artistique : celle d'Innocent Sin. Un vermillon plat, du noir, une
capitale très serrée et le kanji 罪 (« faute ») : la charte de la pochette du
Mini Soundtrack. Eternal Punishment est le pendant bleu ; ne pas mélanger les
deux reste le seul point non négociable de ce fichier.

Le décor : Sumaru la nuit, ses fenêtres qui s'allument et s'éteignent ; un
grand 罪 en filigrane d'où partent des ondes, comme une rumeur qui se
propage ; les papillons dorés de Philémon ; le sceau 罪 qui s'appose à côté
du titre ; en pied, un bandeau de rumeurs qui défile. Les rumeurs sont de
vraies répliques de la traduction (traduction/), à peine raccourcies.

Le texte est vectorisé (fontTools + polices Windows) : GitHub sert les SVG du
README via <img>, ce qui bloque toute police externe, et un <text> vivant
s'afficherait différemment selon l'OS. Les animations sont en CSS ; avec
« réduire les animations », tout s'affiche à l'arrêt.

Dépendance de développement : fontTools.
"""

from __future__ import annotations

import random
import re
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

ICI = Path(__file__).resolve().parent
POLICES = Path("C:/Windows/Fonts")

VERMILLON = "#e0391a"
ENCRE = "#150603"
CREME = "#f7ece4"
SABLE = "#f3d9a8"
DISCRET = "#c99482"
OR, OR_PALE = "#f2b544", "#ffe3a3"
BLEU_GRIMOIRE, BLANC_GRIMOIRE, ROUGE_GRIMOIRE = "#002654", "#F5F5F5", "#CE1126"

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


def _papillon(cls: str = "p") -> str:
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


_DEFS_PAPILLON = f'''  <linearGradient id="or" x1="0" y1="-1" x2="0" y2="1">
    <stop offset="0" stop-color="{OR_PALE}"/><stop offset="1" stop-color="{OR}"/>
  </linearGradient>
  <filter id="lueur" x="-1" y="-1" width="3" height="3">
    <feGaussianBlur stdDeviation="2.2" result="flou"/>
    <feMerge><feMergeNode in="flou"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>'''


# ---------------------------------------------------------------- bannière

def banniere() -> str:
    W, H, BANDE, CX = 1200, 440, 388, 600
    noire = Police("seguibl.ttf")       # Segoe UI Black
    grasse = Police("segoeuib.ttf")     # Segoe UI Bold
    kanji = Police("YuGothB.ttc")       # Yu Gothic Bold
    rnd = random.Random(1999)           # sortie japonaise d'Innocent Sin : rendu reproductible

    # Étoiles, dans le haut du ciel.
    etoiles = "".join(
        f'<circle class="e{rnd.randint(0, 2)}" cx="{rnd.randint(8, W - 8)}" cy="{rnd.randint(8, 190)}" '
        f'r="{rnd.choice((0.8, 1, 1.3))}"/>' for _ in range(70))

    # Sumaru la nuit : immeubles hauts sur les côtés, bas sous le titre.
    immeubles, fenetres = [], []
    x = -10
    while x < W:
        w = rnd.randint(30, 74)
        centre = 330 < x + w / 2 < 870
        h = rnd.randint(16, 38) if centre else rnd.randint(54, 156)
        immeubles.append(f'<rect x="{x}" y="{BANDE - h}" width="{w}" height="{h}"/>')
        for fy in range(BANDE - h + 8, BANDE - 6, 11):
            for fx in range(x + 6, x + w - 6, 9):
                if rnd.random() < (0.1 if centre else 0.24):
                    fenetres.append(f'<rect class="f{rnd.randint(0, 3)}" x="{fx}" y="{fy}" '
                                    f'width="4" height="5"/>')
        x += w + rnd.randint(-6, 4)

    # Titre, centré
    surtitre = grasse.centre("SHIN MEGAMI TENSEI", CX, 80, 17, 7.5)
    persona = noire.centre("PERSONA 2", CX, 178, 104, 1)
    bande_l = 446
    innocent = noire.centre("INNOCENT SIN", CX, 229, 26, 11)
    francais = grasse.centre("TRADUCTION FRANÇAISE  ·  PSP", CX, 292, 19, 5)
    grimoire = grasse.centre("GRIMOIRE DU CŒUR", CX, 334, 12.5, 5)
    filigrane = kanji.centre("罪", CX, 322, 330)
    sceau_x, sceau_y = CX + bande_l / 2 + 14, 192
    sceau = kanji.centre("罪", sceau_x + 27, sceau_y + 41, 40)

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
    rumeurs = (f'<g><path d="{texte_rumeurs}" fill="{CREME}"/>{"".join(puces)}</g>'
               f'<g transform="translate({_n(boucle)} 0)"><path d="{texte_rumeurs}" fill="{CREME}"/>'
               f'{"".join(puces)}</g>')
    uwasa = kanji.centre("噂", 36, BANDE + 35, 26)
    etiquette = noire.chemin("RUMEURS", 60, BANDE + 32, 15, 2.6)
    ETIQUETTE = 60 + noire.largeur("RUMEURS", 15, 2.6) + 20

    ondes = "".join(f'<circle class="onde" style="animation-delay:{k * 2}s" cx="{CX}" cy="200" r="70" '
                    f'fill="none" stroke="{VERMILLON}" stroke-width="2"/>' for k in range(3))

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Persona 2: Innocent Sin — traduction française (PSP)">
<title>Persona 2: Innocent Sin — traduction française</title>
<defs>
  <linearGradient id="ciel" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#0d0302"/><stop offset=".55" stop-color="#2a0905"/>
    <stop offset="1" stop-color="#6a1709"/>
  </linearGradient>
  <radialGradient id="horizon" cx=".5" cy="1" r=".75">
    <stop offset="0" stop-color="{VERMILLON}" stop-opacity=".55"/>
    <stop offset="1" stop-color="{VERMILLON}" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="vignette" cx=".5" cy=".45" r=".75">
    <stop offset=".6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".5"/>
  </radialGradient>
  <linearGradient id="filet" x1="0" x2="1">
    <stop offset="0" stop-color="{SABLE}" stop-opacity="0"/><stop offset=".5" stop-color="{SABLE}"/>
    <stop offset="1" stop-color="{SABLE}" stop-opacity="0"/>
  </linearGradient>
  <pattern id="trame" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(30)">
    <circle cx="2" cy="2" r="1.3" fill="{VERMILLON}"/>
  </pattern>
{_DEFS_PAPILLON}
  <filter id="halo-titre" x="-.2" y="-.5" width="1.4" height="2">
    <feGaussianBlur in="SourceAlpha" stdDeviation="9" result="flou"/>
    <feFlood flood-color="{VERMILLON}" flood-opacity=".85"/>
    <feComposite in2="flou" operator="in" result="rouge"/>
    <feMerge><feMergeNode in="rouge"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <clipPath id="cadre"><rect width="{W}" height="{H}" rx="6"/></clipPath>
  <clipPath id="bande-texte"><rect x="{_n(ETIQUETTE)}" y="{BANDE}" width="{_n(W - ETIQUETTE)}" height="{H - BANDE}"/></clipPath>
</defs>
<style>
  .monte {{ opacity: 0; animation: monte .9s cubic-bezier(.2,.75,.3,1) forwards; }}
  @keyframes monte {{ from {{ opacity: 0; transform: translateY(16px); }} to {{ opacity: 1; transform: none; }} }}
  .titre {{ opacity: 0; animation: titre 1.2s cubic-bezier(.2,.75,.3,1) .2s forwards; }}
  @keyframes titre {{ from {{ opacity: 0; transform: translateY(-10px); }} to {{ opacity: 1; transform: none; }} }}
  .deroule {{ transform-origin: {CX}px 0; animation: deroule .75s cubic-bezier(.25,.8,.3,1) .7s both; }}
  .filet {{ transform-origin: {CX}px 0; animation: deroule 1s cubic-bezier(.25,.8,.3,1) 1.2s both; }}
  @keyframes deroule {{ from {{ transform: scaleX(0); }} to {{ transform: scaleX(1); }} }}
  .sceau {{ opacity: 0; transform-origin: {_n(sceau_x + 27)}px {sceau_y + 27}px;
            animation: appose .7s cubic-bezier(.2,1.45,.4,1) 1.7s forwards; }}
  @keyframes appose {{ from {{ opacity: 0; transform: scale(1.7) rotate(-10deg); }} to {{ opacity: 1; transform: none; }} }}
  .filigrane {{ animation: respire 7s ease-in-out infinite; }}
  @keyframes respire {{ 0%,100% {{ opacity: .1; }} 50% {{ opacity: .19; }} }}
  .onde {{ opacity: 0; transform-origin: {CX}px 200px; animation: onde 6s ease-out infinite; }}
  @keyframes onde {{ 0% {{ opacity: .5; transform: scale(.4); }} 100% {{ opacity: 0; transform: scale(6.5); }} }}
  .e0 {{ animation: scintille 3s ease-in-out infinite; }}
  .e1 {{ animation: scintille 4.5s ease-in-out 1s infinite; }}
  .e2 {{ opacity: .5; }}
  @keyframes scintille {{ 0%,100% {{ opacity: .7; }} 50% {{ opacity: .15; }} }}
  .f0 {{ animation: fenetre 7s steps(1) infinite; }}
  .f1 {{ animation: fenetre 11s steps(1) 2s infinite; }}
  .f2 {{ animation: fenetre 13s steps(1) 5s infinite; }}
  .f3 {{ opacity: .85; }}
  @keyframes fenetre {{ 0%,100% {{ opacity: .85; }} 40% {{ opacity: .12; }} 70% {{ opacity: .85; }} }}
  .defile {{ animation: defile {_n(boucle / 62)}s linear infinite; }}
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
    .monte, .titre, .deroule, .filet, .sceau, .e0, .e1, .f0, .f1, .f2, .defile, .aile, .vol1, .vol2, .vol3 {{
      animation: none; opacity: 1; transform: none;
    }}
    .filigrane {{ animation: none; opacity: .14; }}
    .onde {{ display: none; }}
  }}
</style>
<g clip-path="url(#cadre)">
  <rect width="{W}" height="{H}" fill="url(#ciel)"/>
  <rect width="{W}" height="{H}" fill="url(#trame)" opacity=".07"/>
  <rect width="{W}" height="{H}" fill="url(#horizon)"/>
  <g fill="{CREME}">{etoiles}</g>
  <path class="filigrane" d="{filigrane}" fill="{VERMILLON}" opacity=".1"/>
  {ondes}
  <g fill="#0b0302">{"".join(immeubles)}</g>
  <g fill="{OR}">{"".join(fenetres)}</g>
  <rect width="{W}" height="{H}" fill="url(#vignette)"/>

  <path class="monte" style="animation-delay:.05s" d="{surtitre}" fill="{SABLE}"/>
  <path class="titre" d="{persona}" fill="{CREME}" filter="url(#halo-titre)"/>
  <rect class="deroule" x="{_n(CX - bande_l / 2)}" y="196" width="{bande_l}" height="46" fill="{VERMILLON}"/>
  <path class="monte" style="animation-delay:.95s" d="{innocent}" fill="{ENCRE}"/>
  <g class="sceau">
    <rect x="{_n(sceau_x)}" y="{sceau_y}" width="54" height="54" fill="none" stroke="{VERMILLON}" stroke-width="3"/>
    <path d="{sceau}" fill="{VERMILLON}"/>
  </g>
  <rect class="filet" x="{CX - 150}" y="258" width="300" height="1.5" fill="url(#filet)"/>
  <path class="monte" style="animation-delay:1.3s" d="{francais}" fill="{SABLE}"/>
  <g class="monte" style="animation-delay:1.5s">
    <rect x="{CX - 57}" y="307" width="38" height="5" fill="{BLEU_GRIMOIRE}"/>
    <rect x="{CX - 19}" y="307" width="38" height="5" fill="{BLANC_GRIMOIRE}"/>
    <rect x="{CX + 19}" y="307" width="38" height="5" fill="{ROUGE_GRIMOIRE}"/>
    <path d="{grimoire}" fill="{DISCRET}"/>
  </g>

  <g transform="translate(230 128) scale(1.3)"><g class="vol1">{_papillon()}</g></g>
  <g transform="translate(985 104)"><g class="vol2">{_papillon()}</g></g>
  <g transform="translate(1040 262) scale(.75)"><g class="vol3">{_papillon()}</g></g>
  <g transform="translate(150 290) scale(.65)"><g class="vol2">{_papillon()}</g></g>

  <rect y="{BANDE}" width="{W}" height="{H - BANDE}" fill="{ENCRE}"/>
  <rect y="{BANDE}" width="{W}" height="2" fill="{VERMILLON}"/>
  <g clip-path="url(#bande-texte)">
    <g transform="translate({_n(ETIQUETTE + 20)} {BANDE + 33})"><g class="defile">{rumeurs}</g></g>
  </g>
  <rect y="{BANDE}" width="{_n(ETIQUETTE)}" height="{H - BANDE}" fill="{VERMILLON}"/>
  <path d="{uwasa}" fill="{ENCRE}"/>
  <path d="{etiquette}" fill="{ENCRE}"/>
  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="6" fill="none" stroke="{CREME}" stroke-opacity=".12" stroke-width="2"/>
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
{_DEFS_PAPILLON}
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
<g transform="translate(600 24)">{_papillon()}</g>
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

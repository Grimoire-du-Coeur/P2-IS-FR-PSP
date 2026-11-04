#!/usr/bin/env python3
"""Fabrique la boite de dialogue animee du README.

Une capture d'ecran montre que le jeu est traduit ; une boite qui tape le texte
le fait *voir*. Les repliques ci-dessous sortent telles quelles de
`traduction/event_scripts/`, ponctuation comprise : c'est une vitrine du
travail reel, pas un faux texte de demonstration.

Technique : pas de clipPath anime (support irregulier). Le texte est pose, puis
recouvert d'un cache de la couleur exacte du fond de la boite, qui se decale
vers la droite par paliers (`steps`). Le curseur est le bord gauche du cache.
La police est a chasse fixe pour que les paliers tombent pile sur les
caracteres.

Usage : python docs/assets/generer_dialogue.py
"""

from __future__ import annotations

from pathlib import Path

ICI = Path(__file__).resolve().parent

# (locuteur, replique, fichier d'origine) — verifiables dans le depot.
REPLIQUES = [
    ("Lycéenne", "Ça s'appelle le jeu Persona, et...", "script_107"),
    ("Maya", "Ouuaaah! Trop cool, Yukki! Regarde ça!", "script_009"),
    ("Eikichi", "Prends tes responsabilités et règle ça!", "script_008"),
    ("Ginko", "Étrange, sa présence me rend nostalgique...", "script_009"),
]

TAILLE = 21          # corps du texte de dialogue, en px
CHASSE = 0.6         # avance d'un caractere en police a chasse fixe (em)
X_TEXTE = 104        # origine du texte dans la boite
SECONDES_PAR_CARACTERE = 0.045
MAINTIEN = 2.6       # temps d'affichage une fois la replique tapee

PALETTES = {
    "clair": {
        "fond": "#e8411f", "boite": "#190704", "bord": "#190704",
        "texte": "#f7ece4", "nom": "#e8411f", "nom_fond": "#f7ece4",
        "chapeau": "#4a1207", "accent": "#e8411f", "source": "#8a634f",
        "bordure": "#19070426",
    },
    "sombre": {
        "fond": "#140604", "boite": "#1e0805", "bord": "#e0391a",
        "texte": "#f7ece4", "nom": "#140604", "nom_fond": "#e0391a",
        "chapeau": "#bf7a66", "accent": "#e0391a", "source": "#7d5546",
        "bordure": "#f7ece41f",
    },
}

POLICE_MONO = "'Cascadia Mono','Consolas','DejaVu Sans Mono','Menlo',monospace"


def echapper(texte: str) -> str:
    sortie = []
    for caractere in texte:
        if caractere in "&<>":
            sortie.append({"&": "&amp;", "<": "&lt;", ">": "&gt;"}[caractere])
        elif caractere == "'":
            sortie.append("&#39;")
        elif ord(caractere) < 128:
            sortie.append(caractere)
        else:
            sortie.append("&#{};".format(ord(caractere)))
    return "".join(sortie)


def construire(theme: str) -> str:
    p = PALETTES[theme]

    frappes = [len(r[1]) for r in REPLIQUES]
    durees = [n * SECONDES_PAR_CARACTERE + MAINTIEN for n in frappes]
    total = sum(durees)

    blocs, keyframes = [], []
    debut = 0.0
    for index, (nom, replique, source) in enumerate(REPLIQUES):
        nb = frappes[index]
        duree = durees[index]
        frappe = nb * SECONDES_PAR_CARACTERE
        largeur = nb * TAILLE * CHASSE

        # Fenetre de visibilite de la replique, en % du cycle complet.
        pc_debut = 100 * debut / total
        pc_frappe = 100 * (debut + frappe) / total
        pc_fin = 100 * (debut + duree) / total
        fondu = 0.6

        keyframes.append(
            "@keyframes vis{i} {{ 0%,{a:.3f}% {{ opacity: 0; }}"
            " {b:.3f}%,{c:.3f}% {{ opacity: 1; }}"
            " {d:.3f}%,100% {{ opacity: 0; }} }}".format(
                i=index, a=max(pc_debut - 0.01, 0), b=pc_debut,
                c=max(pc_fin - fondu, pc_debut), d=pc_fin,
            )
        )
        keyframes.append(
            "@keyframes tape{i} {{ 0%,{a:.3f}% {{ transform: translateX(0); }}"
            " {b:.3f}%,100% {{ transform: translateX({w:.0f}px); }} }}".format(
                i=index, a=pc_debut, b=pc_frappe, w=largeur,
            )
        )

        largeur_nom = 26 + len(nom) * 9.2
        blocs.append(
            """<g style="animation: vis{i} {t:.2f}s linear infinite">
      <rect x="92" y="88" width="{wn:.0f}" height="30" rx="2" fill="{nom_fond}"/>
      <text x="{xn:.0f}" y="109" class="nom" fill="{nom}" text-anchor="middle">{nomtxt}</text>
      <text x="{xt}" y="166" class="dlg" fill="{texte}">{dlg}</text>
      <g style="animation: tape{i} {t:.2f}s steps({n}) infinite">
        <rect x="{xt}" y="146" width="3" height="26" fill="{accent}"/>
        <rect x="{xc}" y="140" width="960" height="40" fill="{boite}"/>
      </g>
      <text x="1112" y="196" class="src" fill="{source}" text-anchor="end">{src}.json</text>
    </g>""".format(
                i=index, t=total, n=nb,
                wn=largeur_nom, xn=92 + largeur_nom / 2,
                nomtxt=echapper(nom), dlg=echapper(replique),
                xt=X_TEXTE, xc=X_TEXTE + 3, src=echapper(source),
                **p,
            )
        )
        debut += duree

    return """<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="250"
     viewBox="0 0 1200 250" role="img"
     aria-label="Extraits de dialogues traduits en francais">
  <title>Le jeu, en francais</title>
  <defs>
    <clipPath id="cadre"><rect width="1200" height="250" rx="4"/></clipPath>
  </defs>
  <style>
    {keyframes}
    @keyframes clignote {{ 0%,45% {{ opacity: 1; }} 55%,100% {{ opacity: 0; }} }}
    .fleche {{ animation: clignote 1.1s steps(1) infinite; }}
    .chapeau {{ font: 600 13px 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
                letter-spacing: 3.6px; }}
    .nom {{ font: 700 15px 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }}
    .dlg {{ font: 400 {taille}px {mono}; }}
    .src {{ font: 400 11px {mono}; }}
    @media (prefers-reduced-motion: reduce) {{
      g[style*="animation"] {{ animation: none !important; }}
      .fleche {{ animation: none; }}
    }}
  </style>
  <g clip-path="url(#cadre)">
    <rect width="1200" height="250" fill="{fond}"/>
    <text x="56" y="48" class="chapeau" fill="{chapeau}">LE JEU, EN FRAN&#199;AIS</text>

    <rect x="56" y="72" width="1088" height="150" rx="3"
          fill="{boite}" stroke="{bord}" stroke-width="2"/>

    {blocs}

    <path class="fleche" d="M1104 202 l10 0 l-5 9 z" fill="{accent}"/>
    <rect x="1" y="1" width="1198" height="248" rx="4" fill="none"
          stroke="{bordure}" stroke-width="2"/>
  </g>
</svg>
""".format(
        keyframes="\n    ".join(keyframes),
        blocs="\n    ".join(blocs),
        taille=TAILLE, mono=POLICE_MONO,
        **p,
    )


def main() -> int:
    for theme in PALETTES:
        cible = ICI / "dialogue-{}.svg".format(theme)
        cible.write_text(construire(theme), encoding="utf-8")
        print("{} : {:.0f} Ko".format(cible.name, cible.stat().st_size / 1024))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

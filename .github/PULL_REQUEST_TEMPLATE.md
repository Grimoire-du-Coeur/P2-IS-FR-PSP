<!--
Merci pour la contribution. Le gabarit est court exprès : seules les deux
dernières cases comptent vraiment, parce qu'une balise perdue ou un texte trop
long fait planter le jeu chez tout le monde.
-->

## Ce que change cette PR

<!-- Une ou deux phrases. Si cette PR ferme une issue : « Ferme #123 ». -->

## Type

- [ ] Correction de traduction (texte)
- [ ] Correction de bug en jeu (crash, texte coupé)
- [ ] Outils (`p2is`, `labs/`, patcher)
- [ ] Documentation
- [ ] Maintenance du dépôt / CI

## Vérifications

- [ ] Les **balises de contrôle** (`[SP]`, `[NULL]`, `[E4]`, `[1205]`…) sont intactes :
      `python -m p2is.outils.verify_json <fichiers modifiés>` ne renvoie aucune erreur.
- [ ] Aucun texte ne dépasse son slot : `python -m p2is.outils.check_overflows`
      n'ajoute pas de nouvelle ligne par rapport à `main`.
- [ ] Pour une modification d'outils : `pytest` et `ruff check p2is labs tests` passent.
- [ ] Le vocabulaire suit le [Dictionnaire](../blob/main/docs/Dictionnaire.md),
      ou bien la PR explique pourquoi il faut l'amender.

## Vérifié en jeu ?

<!-- Capture d'écran si le changement est visible. Indiquez PPSSPP ou PSP réelle. -->

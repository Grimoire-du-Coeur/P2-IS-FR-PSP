# Migration des traductions vers le nouveau format `event_scripts`

**Date :** 2026-06-09
**Statut :** Design validé

## Contexte

La traduction FR de Persona 2: Innocent Sin (PSP) a été réalisée dans l'ancien
format `scripts/script_NNN.json` (301 scripts traduits sur 399). Un nouveau
format d'extraction existe dans `traduction/event_scripts/script_NNN.json`
(399 fichiers, champs FR vides). On doit transférer les traductions
(`nom_fr`, `texte_fr`) de l'ancien vers le nouveau, **sans corruption**.

L'ancien vérificateur (`json_verify/`) n'est plus adapté au nouveau format.

### Différences ancien → nouveau format

Structure JSON :

| | Ancien (`scripts/`) | Nouveau (`event_scripts/`) |
|---|---|---|
| Ordre clés | `id, offset, slot_size, data_size, nom_orig, texte_orig, nom_fr, texte_fr` | `id, offset, data_size, slot_size, _term, nom_orig, texte_orig, nom_fr, texte_fr` |
| Champ `_term` | absent | présent (liste d'entiers, ne pas toucher) |
| Placeholder héros | `[U+1113]` / `[U+1112]` | `[1113]` / `[1112]` |
| Champs FR | remplis | vides |

Deux natures de divergence dans `texte_orig` :

1. **Cosmétique / systématique** — `[U+1113]`→`[1113]`, `[U+1112]`→`[1112]`.
   Transférable automatiquement après conversion.
2. **Structurelle / dangereuse** — certains blocs menu/bio
   (`[E1][E2]...[E4][NULL][NULL][0002]`) ont été découpés différemment.
   Exemple `script_002` id=2 : l'ancien `texte_orig` (data_size 464) contenait
   dialogue + bloc bio Eikichi ; le nouveau (data_size 146) ne contient que le
   dialogue. Copier l'ancien `texte_fr` tel quel corromprait l'entrée.
   → ces cas doivent passer en **revue manuelle** (pause).

## Périmètre

- **Première construction : `event_scripts` uniquement** (399 scripts, mapping
  1:1 par nom de fichier, aucun trou).
- `AutreScript/*.json` (CD_SHOP, MMAP01-06) → `traduction/*.json` : **plus tard**,
  même outil une fois rodé.
- `traduction/F_BE.json` et `traduction/TM_EVE.json` : aucune source ancienne →
  traduction fraîche, hors périmètre du transfert.

## Décisions de design

- **Stratégie d'appariement :** normaliser puis comparer.
- **Granularité :** script par script (cohérent avec « 1 script = 1 commit »).
- **À chaque pause :** Claude propose une recommandation FR (souvent l'ancien
  `texte_fr` déjà converti, prêt à valider).
- **Cible :** écriture en place dans `traduction/event_scripts/*.json`.

## Architecture

```
transfer.py   moteur déterministe : transfère le sûr, signale les pauses
verify.py     nouveau vérificateur format event_scripts (limite d'octets)
workflow      script par script : transfert auto → revue des pauses → commit
```

Le moteur Python fait le travail mécanique et produit un **rapport de pauses**.
La revue des pauses se fait conversationnellement (Claude + utilisateur), car
elle requiert un jugement et des recommandations.

### Composant 1 — Normalisation pour comparaison

Fonction `texte_nu(s)` :
- supprime tous les codes entre crochets `[...]`
- `[SP]` → espace, `\n` → espace
- compresse les espaces multiples, trim

Appliquée à `texte_orig` ancien ET nouveau pour comparer le texte « nu ».

### Composant 2 — Règle de décision (par entrée, appariée par `id`)

1. Calculer `texte_nu` ancien et nouveau.
2. Détecter les **codes-déclencheurs** : `[1432]`, `[1208]`, `[E1]`–`[E4]`
   (dans l'ancien ou le nouveau).
3. Décision :
   - `texte_nu` ancien == nouveau **ET** aucun déclencheur → **TRANSFERT AUTO**.
   - sinon → **PAUSE** avec raison (`texte divergent` et/ou `menu/Q-R`).

« Pause » ≠ retraduction : dans la majorité des cas, la reco = ancien `texte_fr`
converti, à valider. Seuls les blocs réellement déplacés demandent un choix.

### Composant 3 — Conversion des codes au transfert

- `[U+1113]`→`[1113]`, `[U+1112]`→`[1112]` (connus).
- **Auto-détection** : au premier passage, le moteur scanne toutes les entrées
  qui matchent, diffe les séquences de codes ancien/nouveau, et signale tout
  autre renommage systématique au-delà des 2 connus (filet de sécurité).
- `nom_fr` transféré quand `nom_orig` correspond.

### Composant 4 — Vérificateur (`verify.py`)

Reprend le calcul d'octets exact de l'ancien `json_verify` (à lire pour copie),
adapté au nouveau format :
- Budget = `data_size - 8`.
- Coût : caractère standard ou accentué (liste supportée) = 2 octets ;
  balise reconnue `[XXXX]` = 2 octets ; `[NULL]` = 0 octet ; `[` non fermé = erreur.
- Signale les entrées dépassant le budget.
- Avertit si un `[U+1113]`/`[U+1112]` subsiste dans un champ FR (mauvaise convention).
- Vérifie l'intégrité de `[1432][NULL][NULL][0014]` quand présent.
- Connaît `_term` (lecture seule).

### Composant 5 — Orchestration `transfer.py script_NNN`

- Charge ancien + nouveau.
- Vérifie l'alignement (même nombre d'entrées, appariement par `id`).
- Pour chaque entrée : applique la règle de décision.
- Transfert auto en place (préserve l'ordre des clés et `_term` du nouveau format).
- Collecte les cas de pause → rapport structuré : `id`, raison, `nom_fr` ancien,
  `texte_fr` ancien converti (= recommandation), `texte_orig` nouveau,
  budget d'octets, coût de la recommandation.
- N'écrit PAS les cas de pause (laissés vides jusqu'à décision).

## Cas limites

- Ancien script vide (98 scripts non traduits) → rien à transférer → entrées
  marquées « à traduire ».
- Nombre d'entrées différent ancien/nouveau → erreur dure, pause du script entier.
- Appariement par champ `id`, jamais par position.
- Préserver strictement les champs non-FR du nouveau format (`_term`, tailles, offset).

## Règles de traduction (rappel, inchangées)

- Dictionnaire officiel obligatoire (`scripts/Dictionnaire.md`).
- Accents supportés : `é è ê à ç ù â î ô û œ ü ï É È Ê À Ç Ù Â Î Ô Û Œ`.
- Limite effective = `data_size - 8` octets.
- Onomatopées / expressions de choc : suspendre et demander.
```

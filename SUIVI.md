<div align="center">
  
# Tableau de Bord & Suivi d'Avancement
  
**Persona 2: Innocent Sin FR (PSP)**

<br/>

<img src="https://img.shields.io/badge/Statut-B%C3%8ATA_EN_APPROCHE-6b21a8?style=for-the-badge" alt="Statut" />
<img src="https://img.shields.io/badge/Progression-99%25-2ea043?style=for-the-badge" alt="Progression" />

</div>

<br/>

> [!NOTE]
> Cette page documente l'avancement global du projet de traduction. L'histoire principale est achevée, nous nous concentrons actuellement sur la phase d'Assurance Qualité (QA) et la relecture finale In-Game.

<div align="center">
  <a href="https://docs.google.com/spreadsheets/d/1d0MADmYznfH-R43RLZAHrngTT5flK9UTVt4wTzc10Uw/edit?gid=0#gid=0"><b>📊 Suivi Détaillé sur Google Sheets</b></a> | <a href="./SUIVI_TECHNIQUE.md"><b>🛠️ Problèmes Connus & Bugs</b></a>
</div>

<br>

---

## Graphique d'Avancement Global

Voici la répartition des **406 fichiers scripts** gérant l'intégralité des textes du jeu :

```mermaid
pie title Progression des 406 Scripts
    "Traduits (314)" : 314
    "Vides / Sans texte (91)" : 91
    "En Cours (1)" : 1
```

> [!TIP]
> **Les Scripts Vides (91) :** Ils correspondent à des événements, des déclencheurs invisibles ou des chargements ne contenant aucun texte. Ils sont considérés comme terminés d'office.

<br/>

---

## Détails de la Traduction

<div align="center">

| Catégorie | Fichiers | Statut Actuel |
|:---|:---:|:---:|
| **Scripts d'Histoire** (`script_000` à `script_396`) | 397 | <img src="https://img.shields.io/badge/-Termin%C3%A9e-2ea043?style=flat-square" alt="Terminée" /> |
| **Scripts de Carte** (`MMAP01` à `06`) | 5/6 | <img src="https://img.shields.io/badge/-En%20Cours-0366d6?style=flat-square" alt="En Cours" /> |
| **Boutique de CDs** (`CD_SHOP`) | 1 | <img src="https://img.shields.io/badge/-Termin%C3%A9e-2ea043?style=flat-square" alt="Terminée" /> |
| **Combats & Menus** (`F_BE`) | 1 | <img src="https://img.shields.io/badge/-Termin%C3%A9e-2ea043?style=flat-square" alt="Terminée" /> |
| **Cinématiques narratives** (`TM_EVE`) | 1 | <img src="https://img.shields.io/badge/-En%20Cours-0366d6?style=flat-square" alt="En Cours" /> |

</div>

> [!IMPORTANT]
> Le fichier `TM_EVE` est l'unique script nécessitant encore une intervention de traduction textuelle. La trame principale de l'histoire est achevée à 100 %.

<br/>

---

## Phase de Relecture et Lancement

Le projet traverse actuellement la phase critique de vérification In-Game (Assurance Qualité).

```mermaid
gantt
    title Planning vers la Version BÊTA
    dateFormat  YYYY-MM-DD
    axisFormat  %d/%m
    
    section Traduction
    Histoire Principale      :done,    des1, 2023-01-01, 2026-06-25
    Textes Annexes (F_BE...) :done,    des2, 2026-05-01, 2026-06-28
    Dernier fichier (TM_EVE) :active,  des3, 2026-06-25, 2026-07-05
    
    section Qualité (QA)
    Phase de Correction In-Game :active,  rel1, 2026-06-20, 2026-07-09
    
    section Sortie
    Lancement Version BÊTA Publique   :milestone, 2026-07-10, 0d
```

<!-- updated -->

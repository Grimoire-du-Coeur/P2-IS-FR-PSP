<div align="center">
  
# Tableau de Bord & Suivi d'Avancement
  
**Persona 2: Innocent Sin FR (PSP) - ULES01557**

<br/>

<img src="https://img.shields.io/badge/Statut-Phase_de_Bêta_QA-6b21a8?style=for-the-badge" alt="Statut" />
<img src="https://img.shields.io/badge/Progression-99%25-2ea043?style=for-the-badge" alt="Progression" />

</div>

<br/>

> [!NOTE]
> Cette page documente l'avancement global et en temps réel du projet de traduction. L'histoire principale est achevée. Nous sommes actuellement focalisés sur la phase critique d'Assurance Qualité (QA) In-Game pour chasser les derniers bugs d'affichage et de pointeurs mémoires.

<div align="center">
  <a href="https://docs.google.com/spreadsheets/d/1d0MADmYznfH-R43RLZAHrngTT5flK9UTVt4wTzc10Uw/edit?gid=0#gid=0"><b>📊 Suivi Détaillé sur Google Sheets</b></a> | <a href="./SUIVI_TECHNIQUE.md"><b>🛠️ Problèmes Connus & Bugs (Technique)</b></a>
</div>

<br>

---

## Graphique d'Avancement Global

Voici la répartition des **406 fichiers scripts** identifiés qui gèrent l'intégralité des textes et des choix du jeu :

```mermaid
pie title Progression des 406 Scripts
    "Traduits et Validés (314)" : 314
    "Fichiers Vides / Triggers (91)" : 91
    "En Cours d'Édition (1)" : 1
```

> [!TIP]
> **Les Scripts Vides (91) :** Notre scanner d'arborescence a détecté de nombreux scripts sans texte (déclencheurs d'événements invisibles ou chargements mémoires). Ils sont classés comme terminés d'office pour la traduction.

<br/>

---

## Détails de la Traduction par Composant

Chaque composant vital du jeu possède sa propre structure de données. Voici l'état d'avancement pour chacun d'eux (pour plus de détails sur le format de ces fichiers, consultez notre `DEVELOPER.md`).

<div align="center">

| Cible dans l'Arborescence | Rôle In-Game | Statut Actuel |
|:---|:---|:---:|
| **Scripts d'Histoire** (`event.bin`) | Contient les 399 sous-scripts de la trame narrative principale. | <img src="https://img.shields.io/badge/-Terminée-2ea043?style=flat-square" alt="Terminée" /> |
| **Scripts de Carte** (`MMAP01` à `06`) | Dialogues ambiants des PNJ selon le quartier (Sumaru City). | <img src="https://img.shields.io/badge/-En%20Cours-0366d6?style=flat-square" alt="En Cours" /> |
| **Boutique de CDs** (`CD_SHOP.BIN`) | Noms des morceaux et descriptions dans la boutique musicale. | <img src="https://img.shields.io/badge/-Terminée-2ea043?style=flat-square" alt="Terminée" /> |
| **Combats & Menus** (`F_BE.BNP`) | Noms des démons, attaques, sorts, et interface de combat. | <img src="https://img.shields.io/badge/-Terminée-2ea043?style=flat-square" alt="Terminée" /> |
| **Cinématiques** (`TM_EVE.BNP`) | Scènes 3D scriptées et événements visuels majeurs. | <img src="https://img.shields.io/badge/-En%20Cours-0366d6?style=flat-square" alt="En Cours" /> |

</div>

> [!IMPORTANT]
> Le fichier `TM_EVE.BNP` est le dernier fichier massif nécessitant encore une intervention de traduction textuelle. Une fois celui-ci achevé, la traduction brute du jeu atteindra officiellement les 100 %.

<br/>

---

## Phase de Relecture et Lancement

Le projet traverse actuellement sa phase la plus délicate : l'Assurance Qualité (QA) sur hardware réel ou émulateur, visant à déceler les crashs liés à la compression `CRILAYLA` et à la longueur des chaînes françaises.

```mermaid
gantt
    title Planning de Sortie (Version BÊTA)
    dateFormat  YYYY-MM-DD
    axisFormat  %d/%m
    
    section Traduction
    Histoire Principale      :done,    des1, 2023-01-01, 2026-06-25
    Textes Annexes (F_BE...) :done,    des2, 2026-05-01, 2026-06-28
    Dernier fichier (TM_EVE) :done,    des3, 2026-06-25, 2026-07-24
    
    section Qualité (QA)
    Traque des Crashs & Pointeurs :active,  rel1, 2026-06-20, 2026-08-15
    Test sur Vrai Hardware PSP    :         rel2, 2026-08-01, 2026-08-15
    
    section Sortie
    Lancement Version BÊTA Publique   :milestone, 2026-08-15, 0d
```


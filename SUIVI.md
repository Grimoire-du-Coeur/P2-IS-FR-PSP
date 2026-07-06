<div align="center">
  
# Tableau de Bord & Suivi d'Avancement
  
**Persona 2: Innocent Sin FR (PSP)**

[![Statut](https://img.shields.io/badge/Statut-BÊTA%20en%20approche-blueviolet?style=flat-square)](#)
[![Progression](https://img.shields.io/badge/Progression-99%25-brightgreen?style=flat-square)](#)

</div>

<br/>

> [!NOTE]
> Cette page synthétise l'avancement global du projet de traduction. L'histoire principale est achevée, nous sommes dans les finitions et les tests qualité.

---

## 📊 Graphique d'Avancement Global

Voici la répartition en direct des **406 fichiers scripts** gérant l'intégralité des textes du jeu :

```mermaid
pie title Progression des 406 Scripts
    "Traduits (314)" : 314
    "Vides / Sans texte (91)" : 91
    "En Cours (1)" : 1
```

> [!TIP]
> **Les Scripts Vides (91) :** Ils correspondent à des événements ou des zones du jeu sans dialogue textuel (cinématiques muettes, triggers invisibles, chargements). Ils sont validés de fait.

---

## 📈 Détails de la Traduction

| Catégorie | Fichiers | Statut Actuel |
|-----------|:--------:|:-------------:|
| **Scripts d'Histoire** (`script_000` à `script_396`) | 397 | ✅ **Terminé** |
| **Scripts de Carte** (`MMAP01` à `06`) | 6 | ✅ **Terminé** |
| **Boutique de CDs** (`CD_SHOP`) | 1 | ✅ **Terminé** |
| **Combats & Menus** (`F_BE`) | 1 | ✅ **Terminé** |
| **Cinématiques narratives** (`TM_EVE`) | 1 | 🔄 **En Cours** |

> [!IMPORTANT]
> Le seul fichier nécessitant encore du travail de traduction pure est `TM_EVE`. L'histoire principale est achevée à 100%.

---

## 🗓️ Phase de Relecture et Lancement

Le projet est actuellement en pleine phase de vérification In-Game (QA).

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

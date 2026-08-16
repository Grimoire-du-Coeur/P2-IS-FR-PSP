<div align="center">

# Journal des Versions â€” Persona 2: Innocent Sin FR

**Suivi des releases, corrections techniques et historique du projet**

<br/>

<img src="https://img.shields.io/badge/Version_Actuelle-BÃŠTA_v0.1.3-6b21a8?style=for-the-badge" alt="Version actuelle" />
<img src="https://img.shields.io/badge/Statut-En_dÃ©veloppement_actif-2ea043?style=for-the-badge" alt="Statut" />

</div>

<br/>

> [!NOTE]
> Ce document retrace l'historique complet des versions publiÃ©es, leurs corrections techniques, et les grandes Ã©tapes du projet. Pour le tableau d'avancement en temps rÃ©el, voir [CONTRIBUTING.md](./CONTRIBUTING.md).

<br/>

---

## Frise Chronologique

```mermaid
timeline
    title Historique du Projet
    Mars 2026 : 14/03 - Premier teaser (hykalys)
              : 15/03 - CrÃ©ation du projet et du dÃ©pÃ´t GitHub
              : 16/03 - Annonce sur X et dairoku_kizashi56
              : 17/03 - Dictionnaire de lore et Gyotre
              : 22/03 - ArsenetheIV prÃ©sente le projet
              : 29/03 - 63.7% du jeu traduit (162 scripts)
    Avril 2026 : 17/04 - Premier aperÃ§u de gameplay
               : 19/04 - Arati prÃ©sente le projet
               : 21/04 - 78% de traduction (225 scripts)
    Juin 2026 : 05/06 - 100% de l'histoire principale traduite
              : 22/06 - Lancement de l'outil de relecture collaboratif
    Juillet 2026 : 10/07 - Sortie BÃŠTA v0.1 (jouable Ã  100%)
                 : 15/07 - Tutoriel d'installation vidÃ©o
                 : 17/07 - BÃŠTA v0.1.1 (auto-wrap, typographie)
                 : 19/07 - Bilan de l'avancement sur X
                 : 21/07 - BÃŠTA v0.1.2 (correction crashs mÃ©moire)
                 : 24/07 - BÃŠTA v0.1.3 (rÃ©vision scÃ©nario, sauts de ligne)
```

<br/>

---

## Historique des Versions

### BÃŠTA v0.1.3 â€” *24 Juillet 2026*

**RÃ©vision scÃ©nario et corrections d'affichage.**

- RÃ©vision complÃ¨te des textes du scÃ©nario principal sur l'ensemble des 399 scripts
- Correction des sauts de ligne incorrects dans les boÃ®tes de dialogue longues
- PrÃ©paration technique de la traduction des menus (EBOOT)

---

### BÃŠTA v0.1.2 â€” *21 Juillet 2026*

**Mise Ã  jour critique â€” StabilitÃ©, encodage et rendu.**

- **Correction du glitch mÃ©moire** : Refonte du padding de fin de dialogue. Les espacements utilisent dÃ©sormais des `[SP]` invisibles au lieu d'octets nuls (`0x0000`) qui faisaient crasher le CPU de la PSP
- **Gestion du dÃ©filement** : Repositionnement des balises de terminaison `[E1][E2]` en fin de bloc `[E3]` â€” 35 fichiers corrigÃ©s
- **BoÃ®tes de choix stabilisÃ©es** : Nettoyage des balises de mise en page mal injectÃ©es dans les listes `[1208]` â€” 87 fichiers corrigÃ©s
- **Typographie et nameplates** : Conversion des caractÃ¨res spÃ©ciaux vers ASCII et correction des retours Ã  la ligne aprÃ¨s les noms `[E4]` â€” 50 fichiers corrigÃ©s
- **Tronquage automatique** : Limitation stricte Ã  3 lignes par boÃ®te pour Ã©viter les dÃ©bordements visuels

---

### BÃŠTA v0.1.1 â€” *17 Juillet 2026*

**Mise Ã  jour mineure â€” Optimisation et correction de texte.**

- **Auto-wrap** : SystÃ¨me de retour Ã  la ligne automatique pour que le texte s'adapte aux boÃ®tes de dialogue sans intervention manuelle
- **RÃ©vision typographique** : Ajout des espaces insÃ©cables avant la ponctuation double (`?`, `!`, `:`, `;`), ajustement des apostrophes typographiques
- **RÃ©solution des troncatures** : Correction des bugs visuels qui coupaient la fin de certaines rÃ©pliques

---

### BÃŠTA v0.1 â€” *10 Juillet 2026*

**PremiÃ¨re version bÃªta publique.**

- Jouable du dÃ©but Ã  la fin sur l'intÃ©gralitÃ© du scÃ©nario principal (`event.bin` Ã  100%)
- Dialogues de PNJ sur les cartes partiellement intÃ©grÃ©s
- Textes de combat et menus (EBOOT) encore en cours d'intÃ©gration

---

### Pack HD FR v0.1 â€” *6 Mai 2026*

**PremiÃ¨re sortie du pack de textures franÃ§aises.**

- Traduction des menus et Ã©lÃ©ments de l'interface en haute dÃ©finition
- Ã€ superposer sur le pack HD original de racawr dans PPSSPP

<br/>

---

## Ã‰tat d'Avancement Global

| Fichier / Composant | Contenu | Progression |
|:---|:---|:---:|
| `event.bin` | 399 scripts d'histoire | **100%** |
| `MMAP01` Ã  `MMAP06` | Dialogues PNJ sur les cartes | **100%** |
| `CD_SHOP.BNP` | Boutique de CD | **100%** |
| `F_BE.BNP` | RÃ©pliques de combat | **100%** |
| `TM_EVE.BNP` | CinÃ©matiques in-game scriptÃ©es | **100%** |
| `EBOOT.BIN` | Menus, noms, descriptions (6574 entrÃ©es) | **~15%** |
| Textures HD | Interface graphique haute dÃ©finition | **35/42** |
| Textures ISO | Ã‰lÃ©ments graphiques embarquÃ©s dans l'ISO | **0/42** |

> [!IMPORTANT]
> L'EBOOT.BIN est le dernier grand chantier restant. Sa traduction complÃ¨te marquera la couverture textuelle Ã  100% du jeu.


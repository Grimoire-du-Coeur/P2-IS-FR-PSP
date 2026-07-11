<div align="center">
  
# Persona 2: Innocent Sin FR
  
**Le patch de traduction française intégral (PSP - ULES01557)**

<br/>

<a href="https://fr.wikipedia.org/wiki/PlayStation_Portable"><img src="https://img.shields.io/badge/PlayStation_Portable-103F91?style=for-the-badge&logo=playstation&logoColor=white" alt="Plateforme" /></a>
<img src="https://img.shields.io/badge/Statut-B%C3%8ATA_DISPONIBLE-6b21a8?style=for-the-badge" alt="Statut" />
<a href="https://personalegrimoireducoeur.fr/"><img src="https://img.shields.io/badge/Site_Web-personagrimoireducoeur.fr-10b981?style=for-the-badge&logo=vercel&logoColor=white" alt="Site Officiel" /></a>

<br/>

<a href="https://github.com/chenetulipe/P2-FR-IS-PSP/commits/main"><img src="https://img.shields.io/github/last-commit/chenetulipe/P2-FR-IS-PSP?style=flat-square&color=2ea043" alt="Dernier Commit" /></a>
<a href="https://github.com/chenetulipe/P2-FR-IS-PSP/issues"><img src="https://img.shields.io/github/issues/chenetulipe/P2-FR-IS-PSP?style=flat-square&color=d73a49" alt="Issues" /></a>
<a href="https://github.com/chenetulipe/P2-FR-IS-PSP/stargazers"><img src="https://img.shields.io/github/stars/chenetulipe/P2-FR-IS-PSP?style=flat-square&color=e3b341" alt="Stars" /></a>
<a href="https://discord.gg/rd4ckSWHNm"><img src="https://img.shields.io/discord/1400909421609095323?color=5865F2&label=Discord&logo=discord&logoColor=white&style=flat-square" alt="Discord" /></a>

</div>

<br/>

> [!WARNING]
> **Clause de Tolérance Zéro**<br/>
> Ce projet ne distribue **aucun fichier original du jeu ni ROM piratée**. Vous devez extraire légalement votre propre image disque (ISO) depuis votre UMD original. Ce patch est conçu **exclusivement** pour la version Europe (ULES01557). L'équipe ne peut être tenue responsable d'éventuels dommages liés à son utilisation.

<br/>

Ce dépôt centralise l'intégralité du projet : le patch de traduction jouable, les outils de romhacking développés sur-mesure pour ce moteur, ainsi que la documentation technique complète du jeu.

---

## Sommaire
1. [Aperçu du Projet](#aperçu-du-projet)
2. [État d'Avancement](#état-davancement)
3. [Installation et Utilisation](#installation-et-utilisation)
4. [L'Outil de Romhacking](#loutil-de-romhacking-p2is_tool)
5. [Le Patcher Web](#le-patcher-web-p2is_patcher)
6. [Compatibilité Pack HD](#compatibilité-pack-hd)
7. [Foire Aux Questions (FAQ)](#foire-aux-questions-faq)
8. [Clause de Non-Responsabilité](#clause-de-non-responsabilite)
9. [Documentation du Projet](#documentation-du-projet)
10. [Communauté et Liens](#communauté-et-liens)
11. [Licence et Crédits](#licence-et-crédits)

<br/>

---

## Aperçu du Projet

<div align="center">
  <a href="https://youtu.be/rGHRMPw-bbo?si=vIguQ4_gXU1r-yoH">
    <img src="https://img.youtube.com/vi/rGHRMPw-bbo/maxresdefault.jpg" alt="Vidéo de gameplay" width="650" style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);"/>
  </a>
  <br/><br/>
  <i>Cliquez sur l'image pour visionner un aperçu du jeu en français.</i>
</div>

<br/>

---

## État d'Avancement

Voici l'état actuel de la traduction. Pour des statistiques plus détaillées (graphiques et progression fichier par fichier), veuillez consulter le tableau de bord officiel : **[SUIVI.md](./SUIVI.md)**.

<br/>

<div align="center">

| Contenu du Jeu | Progression | Statut |
|:---|:---:|:---:|
| **Scripts (Dialogues Histoire)** | 100% | <img src="https://img.shields.io/badge/-Termin%C3%A9-2ea043?style=flat-square" alt="Terminé" /> |
| **Police d'écriture (Accents FR)** | 100% | <img src="https://img.shields.io/badge/-Termin%C3%A9-2ea043?style=flat-square" alt="Terminé" /> |
| **Scripts (Boutiques, Carte)** | 8/9 | <img src="https://img.shields.io/badge/-En%20cours-0366d6?style=flat-square" alt="En cours" /> |
| **Textures HD** | 35/42 | <img src="https://img.shields.io/badge/-En%20cours-0366d6?style=flat-square" alt="En cours" /> |
| **Autres éléments (Menus)** | ~ | <img src="https://img.shields.io/badge/-En%20cours-0366d6?style=flat-square" alt="En cours" /> |

</div>

<br/>

---

## Installation et Utilisation

Le projet est actuellement en phase de **BÊTA publique**.

Cette version est jouable du début à la fin de l'histoire principale. L'objectif de cette bêta est de recueillir vos retours pour corriger les éventuels bugs avant la version finale 1.0.

> [!NOTE]
> **Procédure d'installation :**
> 
> 1. Téléchargez le dernier patch BÊTA au format `.xdelta` depuis la section **[Releases](https://github.com/chenetulipe/P2-FR-IS-PSP/releases/tag/Patch-FR%2BPack-HD)**.
> 2. Appliquez le patch sur votre ISO originale (`ULES01557`) de préférence via notre **[Patcher Web P2IS FR](./p2is_patcher)** (simple, rapide, sans rien installer) ou à l'aide d'un outil externe tel que **DeltaPatcher**.
> 3. Lancez l'ISO modifiée sur votre console PSP (équipée d'un Custom Firmware) ou sur l'émulateur **PPSSPP**.

<br/>

---

## L'Outil de Romhacking (p2is_tool)

Le dossier `p2is_tool/` contient le code source de l'application de romhacking créée spécifiquement pour traduire Persona 2. 

Construit sur une architecture moderne, l'outil s'installe et se lance automatiquement via le fichier `start.bat`.

<div align="left">
  <img src="https://img.shields.io/badge/Backend-FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/Langage-Python-3670A0?style=flat-square&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Frontend-React-20232A?style=flat-square&logo=react&logoColor=61DAFB" />
</div>

<br/>

---

## Le Patcher Web (p2is_patcher)

Le dossier `p2is_patcher/` contient le code source de l'application web permettant aux joueurs d'appliquer le patch FR directement dans leur navigateur, sans aucun logiciel à installer.

Construit sur une architecture autonome, l'outil s'exécute localement et se lance automatiquement via le fichier `lancer_patcher.bat`.

<div align="left">
  <img src="https://img.shields.io/badge/Moteur-WebAssembly-654FF0?style=flat-square&logo=webassembly&logoColor=white" />
  <img src="https://img.shields.io/badge/Frontend-HTML%2FCSS-E34F26?style=flat-square&logo=html5&logoColor=white" />
  <img src="https://img.shields.io/badge/Langage-JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black" />
</div>

<br/>

---

## Compatibilité Pack HD

Ce projet supporte officiellement le mod **HD UI for Persona 2 - Innocent Sin**. L'auteur nous a autorisé à le modifier. Conformément à notre accord, nous ne distribuons qu'un patch contenant les textures françaises modifiées.

<details>
<summary><b>► Afficher la procédure d'installation du pack HD</b></summary>
<br>

1. Téléchargez le pack HD original : [HD UI on GameBanana](https://gamebanana.com/mods/308752).
2. Installez-le dans le dossier de textures de votre émulateur PPSSPP.
3. Appliquez notre patch de textures FR par-dessus les fichiers du pack HD original.

*Un immense merci à [@racawr](https://gamebanana.com/members/1865032) pour son travail fantastique et son aimable autorisation.*

</details>

<br/>

---

## Foire Aux Questions (FAQ)

<details>
<summary><b>► Y aura-t-il un tutoriel vidéo pour installer le patch ?</b></summary>
<br>
Oui. Une vidéo explicative détaillée sortira sur la chaîne YouTube de <a href="https://www.youtube.com/@chenetulipe">chenetulipe</a> prochainement. En attendant, n'hésitez pas à demander de l'aide sur notre serveur Discord.
</details>

<details>
<summary><b>► Comment puis-je aider à la relecture du jeu ?</b></summary>
<br>
La phase de relecture est ouverte pour traquer les fautes, harmoniser les noms et améliorer les tournures de phrases. Un outil dédié a été développé par <a href="https://github.com/HamzaKarrouchi">Hamza</a> : <a href="https://hamzakarrouchi.github.io/p2is-relecture/">Site de relecture en ligne</a>. 
<br><br>
Vous pouvez y comparer le texte original avec la traduction et utiliser le Dictionnaire pour assurer la cohérence. Une fois vos modifications effectuées, postez-les dans le salon Discord <code>scripts</code> (ou via une Pull Request sur GitHub).
</details>

<details>
<summary><b>► Quel est le contenu de la version BÊTA actuelle ?</b></summary>
<br>
Les 398 scripts de l'histoire principale (event.bin) sont 100 % traduits. La version BÊTA est donc jouable du début à la fin avec l'histoire intégralement en français.
<br><br>
Les dialogues sur la carte 3D (MMAP) et les lignes de combat (F_BE) sont en cours d'intégration et n'y figurent pas encore. L'objectif actuel est de repérer les bugs et les crashs dans l'histoire.
</details>

<br/>

---

<br/>

---

## Clause de Non-Responsabilité

> [!CAUTION]
> **Avertissement Légal & Technique**
> 
> L'équipe de développement du projet **P2‑FR‑IS‑PSP** décline formellement toute responsabilité en cas de :
> - Dommages matériels, logiciels ou usure prématurée de vos appareils.
> - Perte de données, corruption de sauvegardes (saves), ou corruption de votre fichier ISO.
> - Crashs, blocages (freezes), ou dysfonctionnements graphiques/sonores rencontrés en jeu.
> - Incompatibilité avec certains Custom Firmwares (CFW), plugins, ou versions spécifiques d'émulateurs.
> - Tout autre problème direct ou indirect survenant suite à l'application du patch, à l'utilisation du patcher web, de l'outil de romhacking ou du pack de textures HD.

<br/>

**Plateforme officiellement supportée**

Pour le moment, seule la plateforme PPSSPP (PC, Android, macOS) est officiellement testée et recommandée.  
L'ISO patchée peut techniquement fonctionner sur PSP console avec un Custom Firmware, mais nous n'avons pas mené de tests approfondis sur le matériel réel. L'utilisation sur PSP se fait donc à vos propres risques.

<br/>

**Recommandations impératives avant toute manipulation**

- **Backup ISO :** Conservez précieusement une copie de sécurité de votre ISO originale `ULES01557` (non modifiée) avant de lui appliquer le patch `.xdelta`.
- **Backup Sauvegardes :** Sauvegardez vos fichiers de sauvegarde (memory stick) sur un support externe (PC, cloud, clé USB) avant de lancer le jeu patché pour la première fois.
- **Sécurité :** Utilisez exclusivement le patcher web officiel fourni sur notre dépôt GitHub. Nous ne collectons aucune donnée personnelle. Méfiez-vous des patchs ou exécutables téléchargés sur des sites tiers non officiels.

<br/>

> En téléchargeant les fichiers, en patchant votre ISO et en jouant à cette version modifiée, vous reconnaissez avoir pris connaissance de la présente clause et acceptez d'utiliser ce patch **à vos propres risques et périls**.

<br/>

---

## Documentation du Projet

Afin d'assurer la transparence et la pérennité du projet, la documentation technique et organisationnelle a été structurée en plusieurs documents de référence :

* **[DEVELOPER.md](./DEVELOPER.md)** : Architecture technique, reverse-engineering du jeu et fonctionnement du compilateur.
* **[CONTRIBUTING.md](./CONTRIBUTING.md)** : Guide pour rejoindre l'équipe de traduction et utiliser l'interface de relecture.
* **[Dictionnaire.md](./Dictionnaire.md)** : Le glossaire officiel pour garantir la cohérence absolue des termes du jeu.
* **[SUIVI.md](./SUIVI.md)** : Tableau de bord et statistiques détaillées de l'avancement.
* **[CREDITS.md](./CREDITS.md)** : Équipe principale, classement des contributeurs et remerciements.

<br/>

---

## Communauté et Liens

Le projet est avant tout collaboratif. Vous pouvez suivre notre actualité, télécharger les patchs ou venir discuter avec nous via ces canaux :

* ✦ **Site Officiel :** [personalegrimoireducoeur.fr](https://personalegrimoireducoeur.fr/)
* ✦ **Serveur Discord :** [Rejoindre l'équipe et la communauté](https://discord.gg/rd4ckSWHNm)
* ✦ **Contact Projet :** `chenetulipe@personalegrimoireducoeur.fr`

*Pour signaler une erreur de traduction ou un bug technique, veuillez ouvrir une [issue](https://github.com/chenetulipe/P2-FR-IS-PSP/issues) directement sur ce dépôt GitHub.*

<br/>

---

## Licence et Crédits

**Atlus / SEGA** : Développeurs originaux et ayants droit exclusifs du jeu.

**L'Équipe de Traduction Principale :** 
* [@chenetulipe](https://github.com/chenetulipe) (Fondateur & Romhacking)
* [@Garloulou](https://github.com/Garloulou) (Co-traduction)
* [@HamzaKarrouchi](https://github.com/HamzaKarrouchi) (Développement Web & Relecture)

> [!CAUTION]
> **Licence du Patch :** [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)<br/>
> Libre d'utilisation et de modification. **La vente ou la monétisation de ce patch est strictement interdite.** Attribution obligatoire aux créateurs originaux.

*Persona 2: Innocent Sin* est une marque déposée de © Atlus / SEGA. Ce projet est une traduction amateur à but strictement non lucratif, réalisée par des fans pour des fans. Aucun fichier protégé par le droit d'auteur n'est hébergé sur ce dépôt. Le partage d'ISO est strictement interdit dans l'espace communautaire lié à ce projet.

<br/>

<div align="center">
  <a href="https://www.star-history.com/?repos=chenetulipe%2FP2-FR-IS-PSP&type=date&legend=top-left">
   <picture>
     <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=chenetulipe/P2-FR-IS-PSP&type=date&theme=dark&legend=top-left&sealed_token=LFm90kimgTV0pKr7wph4I01fXMDcl0pp1R6gKZQj-A7IbzSxbcuQ3Te4pkPherfmIEivpEoqHEUGj9nyRkBIcEEDu5ejv9MLjA1aY8v8ynFglkEs_gTGdQ" />
     <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=chenetulipe/P2-FR-IS-PSP&type=date&legend=top-left&sealed_token=LFm90kimgTV0pKr7wph4I01fXMDcl0pp1R6gKZQj-A7IbzSxbcuQ3Te4pkPherfmIEivpEoqHEUGj9nyRkBIcEEDu5ejv9MLjA1aY8v8ynFglkEs_gTGdQ" />
     <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=chenetulipe/P2-FR-IS-PSP&type=date&legend=top-left&sealed_token=LFm90kimgTV0pKr7wph4I01fXMDcl0pp1R6gKZQj-A7IbzSxbcuQ3Te4pkPherfmIEivpEoqHEUGj9nyRkBIcEEDu5ejv9MLjA1aY8v8ynFglkEs_gTGdQ" width="800" />
   </picture>
  </a>
</div>

<!-- updated -->

<div align="center">
  
# Persona 2: Innocent Sin FR
  
**Le patch de traduction française intégral (PSP - ULES01557)**

<br/>

<a href="https://fr.wikipedia.org/wiki/PlayStation_Portable"><img src="https://img.shields.io/badge/PlayStation_Portable-103F91?style=for-the-badge&logo=playstation&logoColor=white" alt="Plateforme" /></a>
<img src="https://img.shields.io/badge/Statut-BÊTA_DISPONIBLE-6b21a8?style=for-the-badge" alt="Statut" />
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

> [!IMPORTANT]
> **DERNIÈRE RELEASE DISPONIBLE : BÊTA v0.1.2** (21 Juillet 2026)<br/>
> Cette mise à jour corrige le bug critique du glitch mémoire, stabilise les boîtes de choix et empêche le jeu de sauter les dialogues automatiquement. L'histoire principale est 100% jouable en français.<br/>
> [Télécharger le Patch](https://github.com/chenetulipe/P2-FR-IS-PSP/releases) | [Lire le Patch Note complet](https://personalegrimoireducoeur.fr/patch-notes.html)

<br/>

Ce dépôt centralise l'intégralité du projet : le patch de traduction jouable, les outils de romhacking développés sur-mesure pour ce moteur, ainsi que la documentation technique complète du jeu.

---

## Sommaire
1. [Aperçu du Projet](#aperçu-du-projet)
2. [État d'Avancement](#état-davancement)
3. [Guide d'Installation (Patch & HD UI)](#guide-dinstallation-patch--hd-ui)
4. [L'Outil de Romhacking (p2is_tool)](#loutil-de-romhacking-p2is_tool)
5. [Le Patcher Web (p2is_patcher)](#le-patcher-web-p2is_patcher)
6. [Documentation et Liens Utiles](#documentation-et-liens-utiles)
7. [Licence et Crédits](#licence-et-crédits)

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

# Progression de la traduction française

## État d'Avancement

| Fichier / Composant | Contenu | Progression | Statut |
|:---|:---|:---:|:---|
| **Event.bin** | 399 scripts d'histoire | 100% | ![](https://img.shields.io/badge/-Terminé-2ea043?style=flat-square) |
| **MMAP01 · MMAP02 · MMAP03 · MMAP04 · MMAP05 · MMAP06** | Dialogues sur les cartes | 100% | ![](https://img.shields.io/badge/-Terminé-2ea043?style=flat-square) |
| **CD_SHOP** | Boutique de CD / musique | 100% | ![](https://img.shields.io/badge/-Terminé-2ea043?style=flat-square) |
| **F_BE** | Répliques de combat | 100% | ![](https://img.shields.io/badge/-Terminé-2ea043?style=flat-square) |
| **TM_EVE** | Événements scénaristiques | En cours | ![](https://img.shields.io/badge/-En%20cours-0366d6?style=flat-square) → [PR #423](https://github.com/chenetulipe/P2-FR-IS-PSP/pull/423) |

### Accents français

| Composant | Intégration | Accents pris en charge | Progression | Statut |
|:---|:---:|:---|:---:|:---|
| Textures HD | Oui | — | 35/42 | ![](https://img.shields.io/badge/-En%20cours-0366d6?style=flat-square) |
| Police d'écriture HD (Accents FR) | Oui | é è ê ë à â ç î ï ô ù û + majuscules | 100% | ![](https://img.shields.io/badge/-Terminé%20(Bugs)-e1ad01?style=flat-square) |
| Textures ISO | Non | — | 0/42 | ![](https://img.shields.io/badge/-Non%20démarré-critical?style=flat-square) |
| Police d'écriture (Accents FR) | Oui | N/A | 0% | ![](https://img.shields.io/badge/-Non%20démarré-critical?style=flat-square) |

### EBOOT (Textes Système)

Le fichier original a été découpé en 7 parties (de 1000 entrées chacune) dans le dossier `EBOOT_decoupe` pour éviter les crashs sur GitHub. Voici la correspondance précise des contenus et des IDs pour vous repérer lors de la traduction :

| Contenu | Fichier | IDs (Estimatif) | Entrées | Progression | Statut |
|:---|:---:|:---:|:---:|:---:|:---:|
| Menus & Interface (Titre, Paramètres, Sauvegarde) | Part 1 | 0 à 179 | ~180 | 0% | <img src="https://img.shields.io/badge/-En%20cours-0366d6?style=flat-square" alt="En cours" /> |
| Noms de Personnages / PNJs / Boss | Part 1 | 180 à 449 | ~250 | 0% | <img src="https://img.shields.io/badge/-En%20cours-0366d6?style=flat-square" alt="En cours" /> |
| Commandes & Messages de Combat | Part 1 | 600 à 949 | ~350 | 0% | <img src="https://img.shields.io/badge/-En%20cours-0366d6?style=flat-square" alt="En cours" /> |
| Noms & Descriptions de Personas / Démons | Part 2 & Part 4 | 900 à 1199 & 3500 à 3999 | ~450 | 0% | <img src="https://img.shields.io/badge/-En%20cours-0366d6?style=flat-square" alt="En cours" /> |
| Noms & Descriptions de Compétences | Part 2 | 1200 à 1599 | ~900 | 0% | <img src="https://img.shields.io/badge/-En%20cours-0366d6?style=flat-square" alt="En cours" /> |
| Noms d'Armes / Armures / Accessoires | Part 2 & Part 3 | 1600 à 2199 | ~600 | 0% | <img src="https://img.shields.io/badge/-En%20cours-0366d6?style=flat-square" alt="En cours" /> |
| Objets de quête / Rumeurs / Clés | Part 3 & Part 4 | 2800 à 3499 | ~200 | 0% | <img src="https://img.shields.io/badge/-En%20cours-0366d6?style=flat-square" alt="En cours" /> |
| Noms de lieux / Donjons / Carte | Part 5 à Part 7 | 4000 à 6500 | ~850 | 0% | <img src="https://img.shields.io/badge/-En%20cours-0366d6?style=flat-square" alt="En cours" /> |
| Autres textes (Tutoriels, Infos, etc.) | Part 7 | Divers | ~250 | 0% | <img src="https://img.shields.io/badge/-En%20cours-0366d6?style=flat-square" alt="En cours" /> |
| **Total** | **Part 1 à 7** | **0 à 6573** | **~6 574** | **0%** | |

<br/>

---

**Notes**

- L'eboot est le dernier gros fichier restant.
- La police d'écriture fonctionne mais nécessite encore des ajustements mineurs.
- Le travail sur les textures HD est séparé des textures ISO. Il reste 7 textures HD à finaliser.

---

## Guide d'Installation (Patch & HD UI)

Le projet est actuellement en phase de **BÊTA publique**. Cette version vous permet de parcourir l'intégralité du scénario principal en français.

### Étape 1 : Patcher l'ISO originale
1. Téléchargez le dernier fichier patch au format `.xdelta` depuis notre page **[Releases](https://github.com/chenetulipe/P2-FR-IS-PSP/releases)**.
2. Munissez-vous de votre ISO originale issue de la version européenne du jeu (`ULES01557`).
3. Rendez-vous sur notre **[Patcher Web](https://personalegrimoireducoeur.fr/patcher/)** (aucune installation requise).
4. Glissez votre ISO et le fichier `.xdelta` dans le Patcher Web pour générer votre ISO modifiée en français.

### Étape 2 : Installer le Pack de Textures HD (PPSSPP Uniquement)
Ce projet supporte officiellement le mod *HD UI for Persona 2*. Son installation est requise pour afficher les menus et inventaires traduits avec une typographie haute définition.
1. Téléchargez et installez le pack HD de base sur GameBanana : [HD UI for Persona 2](https://gamebanana.com/mods/308752).
2. Placez-le dans le dossier `TEXTURES/ULES01557/` de votre émulateur PPSSPP.
3. Téléchargez notre correctif **Patch de Textures FR** (disponible dans la section Releases).
4. Collez les dossiers extraits par-dessus le pack HD original pour écraser les textures anglaises par notre version française.
5. Assurez-vous que l'option *Remplacer les textures* est cochée dans les paramètres de PPSSPP.

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

Le dossier `p2is_patcher/` contient le code source de l'application web permettant aux joueurs d'appliquer le patch FR directement dans leur navigateur, sans aucun logiciel lourd à installer.

Construit sur une architecture autonome, l'outil s'exécute localement et se lance via le fichier `lancer_patcher.bat`.

<div align="left">
  <img src="https://img.shields.io/badge/Moteur-WebAssembly-654FF0?style=flat-square&logo=webassembly&logoColor=white" />
  <img src="https://img.shields.io/badge/Frontend-HTML%2FCSS-E34F26?style=flat-square&logo=html5&logoColor=white" />
  <img src="https://img.shields.io/badge/Langage-JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black" />
</div>

<br/>

---

## Documentation et Liens Utiles

Afin d'assurer la transparence et la pérennité du projet, toute la documentation technique et organisationnelle a été structurée :

* **[DEVELOPER.md](./DEVELOPER.md)** : Architecture technique, reverse-engineering du jeu et fonctionnement du compilateur.
* **[CONTRIBUTING.md](./CONTRIBUTING.md)** : Guide pour rejoindre l'équipe de traduction et utiliser l'interface de relecture.
* **[Dictionnaire.md](./Dictionnaire.md)** : Le glossaire officiel pour garantir la cohérence absolue des termes du jeu.
* **[SUIVI.md](./SUIVI.md)** : Tableau de bord, progression détaillée et historique des patchs.
* **[CREDITS.md](./CREDITS.md)** : Équipe principale, classement des contributeurs et remerciements.

### Support & Foire Aux Questions

Si vous rencontrez le moindre problème lors de l'installation, des crashs en jeu ou si vous cherchez des réponses aux questions fréquentes, merci de consulter notre plateforme officielle :

> **[Consulter la F.A.Q Officielle (personalegrimoireducoeur.fr)](https://personalegrimoireducoeur.fr/faq.html)**

Vous pouvez également rejoindre la communauté et demander de l'aide sur notre **[Serveur Discord](https://discord.gg/rd4ckSWHNm)**. Pour les bugs purement techniques, merci d'ouvrir une [Issue GitHub](https://github.com/chenetulipe/P2-FR-IS-PSP/issues).

<br/>

---

## Licence et Crédits

**Atlus / SEGA** : Développeurs originaux et ayants droit exclusifs du jeu.

**L'Équipe de Traduction Principale :** 

* **[@chenetulipe](https://github.com/chenetulipe) (Chef de Projet)**  
  Créateur et pilier du projet. Il s'occupe de la majorité des tâches techniques (reverse-engineering, extraction et réinjection des textes, gestion du romhacking) tout en assurant le rôle de chef d'orchestre pour diriger l'équipe de traduction.

* **[@HamzaKarrouchi](https://github.com/HamzaKarrouchi) (Développeur & Top Traducteur)**  
  Un véritable fou malade du code et de la traduction. Il a abattu un travail colossal sur les scripts du jeu en validant les 100% de complétion de l'histoire et en harmonisant la terminologie. Il a également développé de A à Z la plateforme web "P2IS Relecture" pour faciliter la vie de toute l'équipe.

* **[@Garloulou](https://github.com/Garloulou) (Support & Intégration)**  
  A énormément contribué aux fondations du projet lors de ses débuts, notamment en gérant les fusions (Merge Pull Requests) de la communauté sur GitHub, apportant une aide d'intégration précieuse avant de passer le flambeau.

> [!CAUTION]
> **Clause de Non-Responsabilité & Licence**
> 
> *Persona 2: Innocent Sin* est une marque déposée de © Atlus / SEGA. Ce projet est une traduction amateur à but non lucratif, réalisée par des passionnés. L'utilisation du patch se fait à vos propres risques. L'équipe décline toute responsabilité en cas de corruption de sauvegarde ou de dommages logiciels.
> 
> **Licences du Projet et Dépendances :**
> 
> - **Le Patch de Traduction** (textes, images, `.xdelta`, et code de l'outil `p2is_tool`) est sous licence **[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)**. Libre d'utilisation et de modification pour un usage personnel. **La vente ou la monétisation de ce patch est strictement interdite.**
> - **Le Web Patcher** (l'application web `p2is_patcher` / UI) intègre directement le code source du moteur DeltaPatcher et est donc distribué sous licence **[GPL-2.0](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html)** afin de respecter les droits d'auteur de ce dernier.
> 
> **Dépendances & Outils tiers utilisés (100% compatibles légalement) :**
> - **CriFsLib** par Sewer56 ([MIT](https://opensource.org/licenses/MIT)) : Exécutable `.exe` appelé en externe pour extraire le CPK. Son utilisation via ligne de commande le rend totalement indépendant de notre code.
> - **pspdecrypt** par John-K (Open-Source) : Exécutable `.exe` appelé en externe pour déchiffrer l'EBOOT. Totalement indépendant.
> - **pycdlib** par clalancette ([LGPL-2.1](https://www.gnu.org/licenses/old-licenses/lgpl-2.1.html)) : Bibliothèque Python importée dynamiquement par notre outil. Le projet "utilise" la bibliothèque sans l'intégrer ou la modifier, ce qui est parfaitement autorisé par la LGPL.
> - **DeltaPatcher** par marco-calautti ([GPL-2.0](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html)) : Moteur de patch binaire. Son code est compilé directement dans le Web Patcher, forçant ce dernier à adopter la licence GPL-2.0 (sans contaminer le reste du projet qui reste sous CC).

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


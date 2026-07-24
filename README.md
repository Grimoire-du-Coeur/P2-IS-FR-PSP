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

---

## État d'Avancement

Voici l'état actuel de la traduction globale. Pour des statistiques exhaustives (graphiques et progression fichier par fichier), veuillez consulter le document **[SUIVI.md](./SUIVI.md)**.

<div align="center">

| Contenu du Jeu | Progression | Statut |
|:---|:---:|:---:|
| **Scripts (Dialogues Histoire)** | 100% | <img src="https://img.shields.io/badge/-Terminé-2ea043?style=flat-square" alt="Terminé" /> |
| **Police d'écriture (Accents FR)** | 100% | <img src="https://img.shields.io/badge/-Terminé-2ea043?style=flat-square" alt="Terminé" /> |
| **Scripts (Boutiques, Carte)** | 8/9 | <img src="https://img.shields.io/badge/-En%20cours-0366d6?style=flat-square" alt="En cours" /> |
| **Textures HD** | 35/42 | <img src="https://img.shields.io/badge/-En%20cours-0366d6?style=flat-square" alt="En cours" /> |
| **Autres éléments (Menus, Combats)** | ~ | <img src="https://img.shields.io/badge/-En%20cours-0366d6?style=flat-square" alt="En cours" /> |

</div>

<br/>

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
* [@chenetulipe](https://github.com/chenetulipe) (Fondateur & Romhacking)
* [@Garloulou](https://github.com/Garloulou) (Co-traduction)
* [@HamzaKarrouchi](https://github.com/HamzaKarrouchi) (Développement Web & Relecture)

> [!CAUTION]
> **Clause de Non-Responsabilité & Licence**
> 
> *Persona 2: Innocent Sin* est une marque déposée de © Atlus / SEGA. Ce projet est une traduction amateur à but non lucratif, réalisée par des passionnés. L'utilisation du patch se fait à vos propres risques. L'équipe décline toute responsabilité en cas de corruption de sauvegarde ou de dommages logiciels.
> 
> **Licence du Patch :** [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)<br/>
> Libre d'utilisation et de modification pour un usage personnel. **La vente ou la monétisation de ce patch, sous quelque forme que ce soit, est strictement interdite.**

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


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

<br/>

<a href="https://youtu.be/rGHRMPw-bbo?si=vIguQ4_gXU1r-yoH">
  <img src="https://img.youtube.com/vi/rGHRMPw-bbo/maxresdefault.jpg" alt="Vidéo de gameplay" width="700" style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);"/>
</a>
<br/><br/>
<i>Cliquez sur l'image pour visionner un aperçu du jeu en français.</i>

</div>

<br/>

> [!WARNING]
> **Clause de Tolérance Zéro**<br/>
> Ce projet ne distribue **aucun fichier original du jeu ni ROM piratée**. Vous devez extraire légalement votre propre image disque (ISO) depuis votre UMD original. Ce patch est conçu **exclusivement** pour la version Europe (ULES01557). L'équipe ne peut être tenue responsable d'éventuels dommages liés à son utilisation.

<br/>

---

## 🌟 Pourquoi jouer à cette version ?

- 📖 **100% Français (Accents Natifs) :** La trame scénaristique, le nom des démons, et l'interface ont été intégralement traduits. Finis les caractères manquants, la police a été reprogrammée pour afficher parfaitement les lettres accentuées françaises.
- 🎨 **Compatible HD UI :** Profitez de notre support officiel du fabuleux pack de textures HD pour émulateur, avec nos propres éléments UI remasterisés en français !
- ⚡ **Zéro Installation :** Vous ne voulez pas télécharger de logiciel complexe ? Utilisez notre *Patcher Web* directement dans votre navigateur.

<br/>

---

## 🎮 Joueurs : Guide d'Installation Rapide

Le projet est actuellement en phase de **BÊTA publique**. L'histoire principale est intégralement jouable en français.

```mermaid
graph LR
    A[ISO UMD
Europe] -->|Obligatoire| B(Patcher Web)
    C[Fichier Patch
.xdelta] -->|Téléchargement| B
    B --> D{ISO Patchée FR}
    D --> E[PPSSPP]
    D --> F[Console PSP]
```

<details>
<summary><b>► ÉTAPE PAR ÉTAPE : Comment appliquer le patch ?</b></summary>
<br>

1. **Obtenez le patch** : Téléchargez le dernier patch BÊTA au format `.xdelta` depuis la section **[Releases](https://github.com/chenetulipe/P2-FR-IS-PSP/releases)**.
2. **Préparez votre jeu** : Munissez-vous de l'ISO européenne officielle (`ULES01557`) issue de votre UMD.
3. **Appliquez la traduction** : Allez sur notre **[Patcher Web P2IS FR](./p2is_patcher)** (simple, rapide, aucune installation requise).
4. **Jouez !** : Lancez l'ISO fraîchement générée sur l'émulateur **PPSSPP** (PC, Android, Mac) ou sur votre console PSP équipée d'un Custom Firmware.

</details>

<details>
<summary><b>► OPTIONNEL : Installer le Pack de Textures HD</b></summary>
<br>

1. Téléchargez le pack HD original sur GameBanana : [HD UI for Persona 2](https://gamebanana.com/mods/308752).
2. Installez-le dans le dossier de textures de votre émulateur PPSSPP.
3. Appliquez notre **patch de textures FR** (fourni dans nos Releases) par-dessus les fichiers du pack HD original pour remplacer les menus anglais par notre version française remasterisée !
*Un immense merci à [@racawr](https://gamebanana.com/members/1865032) pour ce travail titanesque.*

</details>

<br/>

---

## 🛠️ Romhackers : Outils et Documentation

Ce dépôt n'héberge pas qu'un simple patch. Il centralise l'intégralité du code source de nos outils développés sur-mesure pour outrepasser les limitations du moteur d'Atlus. 

* ⚙️ **`p2is_tool/` (Backend de Romhacking)** : Une application locale (FastAPI/React/Python) ultra-performante. Elle décompose l'ISO, injecte des espaces mémoires de padding, intercepte les opcodes de Ghostlight, recalcule dynamiquement les pointeurs de la TOC du `CPK`, et ré-assemble l'ISO sans saturer la RAM.
* 🌐 **`p2is_patcher/` (Moteur WASM)** : Un Patcher Web (HTML/JS) autonome embarquant `DeltaPatcher` compilé en WebAssembly. Il utilise l'API Streams et un *Service Worker* pour patcher des fichiers de plus d'1 Go sans crasher le navigateur.

### Documentation Technique Complète
Pour assurer la transmission du savoir-faire à la communauté, nous avons documenté chaque aspect du projet :
* 📘 **[DEVELOPER.md](./DEVELOPER.md)** : La Bible technique (reverse-engineering, formats `.BNP` / `.GIM`, et opcodes).
* 📗 **[CONTRIBUTING.md](./CONTRIBUTING.md)** : Le guide à destination des traducteurs (limites de mémoire, relecture).
* 📙 **[Dictionnaire.md](./Dictionnaire.md)** : Le glossaire officiel pour garantir la cohérence absolue de l'univers.
* 📊 **[SUIVI.md](./SUIVI.md)** : Le tableau de bord et la progression détaillée du projet.
* 🏆 **[CREDITS.md](./CREDITS.md)** : L'équipe de traduction et nos dépendances Open-Source (CriFsLib, pycdlib, pspdecrypt).

<br/>

---

## ❓ Foire Aux Questions (FAQ)

<details>
<summary><b>Y aura-t-il un tutoriel vidéo pour installer le patch ?</b></summary>
Oui. Une vidéo explicative détaillée sortira sur la chaîne YouTube de <a href="https://www.youtube.com/@chenetulipe">chenetulipe</a> prochainement. En attendant, n'hésitez pas à demander de l'aide sur notre serveur Discord.
</details>

<details>
<summary><b>Comment puis-je aider à la relecture du jeu ?</b></summary>
La phase de relecture est ouverte ! Un outil dédié a été développé par <a href="https://github.com/HamzaKarrouchi">Hamza</a> : <a href="https://hamzakarrouchi.github.io/p2is-relecture/">Site de relecture en ligne</a>. <br/>
Vous pouvez y comparer le texte original avec la traduction et utiliser le Dictionnaire pour assurer la cohérence. Postez ensuite vos corrections dans le salon Discord <code>#scripts</code>.
</details>

<details>
<summary><b>Le jeu plante sur ma PSP physique, pourquoi ?</b></summary>
Le jeu modifie très lourdement les instructions de la RAM et de la VRAM, tout en imposant une compression CRILAYLA stricte. Si vous rencontrez un crash sur vrai hardware, signalez-le nous en ouvrant une Issue GitHub ou via Discord. Actuellement, l'émulateur PPSSPP est la plateforme la plus stable pour profiter du jeu.
</details>

<br/>

---

## ⚖️ Avertissement Légal & Licence

> [!CAUTION]
> **Clause de Non-Responsabilité**
> 
> L'équipe de **P2‑FR‑IS‑PSP** décline formellement toute responsabilité en cas de dommages matériels ou logiciels, corruption de sauvegardes ou de l'ISO, et de dysfonctionnements rencontrés en jeu. 
> L'utilisation du patch et des outils se fait **à vos propres risques**. Nous recommandons vivement d'effectuer une copie de sécurité (Backup) de votre ISO originale et de vos Memory Sticks avant toute manipulation.

*Persona 2: Innocent Sin* est une marque déposée de © Atlus / SEGA. Ce projet est une traduction amateur à but non lucratif, réalisée par des passionnés. 

**Licence du Patch :** [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)<br/>
Libre d'utilisation et de modification pour un usage personnel. **La vente ou la monétisation de ce patch, sous quelque forme que ce soit, est strictement interdite.**

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


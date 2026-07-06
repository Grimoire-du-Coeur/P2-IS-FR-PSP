<div align="center">
  
# Persona 2: Innocent Sin FR (PSP)
  
**Projet de traduction française amateur de Persona 2: Innocent Sin sur PSP (ULES01557)**

[![Plateforme](https://img.shields.io/badge/Plateforme-PlayStation%20Portable-blue?style=flat-square&logo=playstation)](https://fr.wikipedia.org/wiki/PlayStation_Portable)
[![Langage](https://img.shields.io/badge/Python-3670A0?style=flat-square&logo=python&logoColor=white)](#)
[![Langage](https://img.shields.io/badge/React-20232A?style=flat-square&logo=react&logoColor=61DAFB)](#)
[![Langage](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)](#)
[![Statut](https://img.shields.io/badge/Statut-En%20Développement-orange?style=flat-square)](#)
[![Dernier Commit](https://img.shields.io/github/last-commit/chenetulipe/P2-FR-IS-PSP?style=flat-square&color=green)](https://github.com/chenetulipe/P2-FR-IS-PSP/commits/main)
[![Issues](https://img.shields.io/github/issues/chenetulipe/P2-FR-IS-PSP?style=flat-square&color=red)](https://github.com/chenetulipe/P2-FR-IS-PSP/issues)
[![Stars](https://img.shields.io/github/stars/chenetulipe/P2-FR-IS-PSP?style=flat-square&color=gold)](https://github.com/chenetulipe/P2-FR-IS-PSP/stargazers)
[![Licence](https://img.shields.io/badge/Licence-CC%20BY--NC--SA%204.0-lightgrey.svg?style=flat-square)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![Discord](https://img.shields.io/discord/1400909421609095323?color=5865F2&label=Discord&logo=discord&logoColor=white&style=flat-square)](https://discord.gg/rd4ckSWHNm)

</div>

<br/>

> [!WARNING]
> Ce projet ne distribue aucun fichier du jeu. Vous devez posséder votre propre image disque (ISO) extraite de votre UMD original. La version supportée est **Persona 2: Innocent Sin - PSP Europe (ULES01557)**.

Ce dépôt centralise l'intégralité du projet : le patch de traduction, les outils de romhacking développés sur-mesure pour extraire et réinjecter les scripts, ainsi que toute la documentation technique relative au moteur du jeu.

---

## Sommaire
1. [Aperçu du Projet](#aperçu-du-projet)
2. [État d'Avancement](#état-davancement)
3. [Installation et Utilisation](#installation-et-utilisation)
4. [L'Outil de Romhacking (p2is_tool)](#loutil-de-romhacking-p2is_tool)
5. [Compatibilité Pack HD](#compatibilité-pack-hd)
6. [Foire Aux Questions (FAQ)](#foire-aux-questions-faq)
7. [Clause de Non-Responsabilité](#clause-de-non-responsabilité)
8. [Documentation du Projet](#documentation-du-projet)
9. [Contact et Communauté](#contact-et-communauté)
10. [Licence et Crédits](#licence-et-crédits)

---

## Aperçu du Projet

<div align="center">
  <a href="https://youtu.be/rGHRMPw-bbo?si=vIguQ4_gXU1r-yoH">
    <img src="https://img.youtube.com/vi/rGHRMPw-bbo/maxresdefault.jpg" alt="Vidéo de gameplay" width="600"/>
  </a>
</div>

## État d'Avancement

| Contenu | Progression |
|---------|:-----------:|
| [Scripts (Dialogues Histoire)](https://github.com/chenetulipe/P2-FR-IS-PSP/tree/main/scripts) | Terminé |
| [Autres Scripts (CD shop, Dialogues Carte)](https://github.com/chenetulipe/P2-FR-IS-PSP/tree/main/AutreScript) | 8/9 |
| Police d'écriture (Accents FR) | Terminé |
| Textures HD | 35/42 |
| Autres éléments (Menus, interface) | En cours |

*(Consultez le fichier [SUIVI.md](./SUIVI.md) pour les statistiques détaillées.)*

## Installation et Utilisation

Le projet est actuellement en développement. Une première version **BÊTA** sera mise en ligne le **10 juillet**. Cette version sera jouable du début à la fin, mais pourra encore contenir des fautes de traduction, des textes en anglais résiduels, ou des bugs mineurs. L'objectif est de recueillir vos retours afin d'affiner la version 1.0.

**Procédure d'installation :**

1. Téléchargez le patch au format `.xdelta` depuis la section [Releases](https://github.com/chenetulipe/P2-FR-IS-PSP/releases).
2. Appliquez le patch sur votre ISO originale (version Europe ULES01557) à l'aide d'un outil tel que DeltaPatcher ou xdelta UI.
3. Lancez l'ISO modifiée sur votre console PSP (équipée d'un Custom Firmware) ou sur un émulateur tel que PPSSPP.

## L'Outil de Romhacking (p2is_tool)

Le dossier `p2is_tool/` contient le code source de l'application de romhacking créée spécifiquement pour traduire Persona 2.
Construit sur une architecture moderne (Backend FastAPI et Frontend React), l'outil s'installe et se lance automatiquement via le fichier `start.bat`.

## Compatibilité Pack HD

Ce projet supporte officiellement le mod **HD UI for Persona 2 - Innocent Sin**. L'auteur nous a autorisé à le modifier. Conformément à notre accord, nous ne distribons qu'un patch contenant les textures françaises modifiées.

**Procédure d'installation du pack HD :**

1. Téléchargez le pack HD original : [HD UI on GameBanana](https://gamebanana.com/mods/308752).
2. Installez-le dans le dossier de textures de votre émulateur PPSSPP.
3. Appliquez notre patch de textures FR par-dessus les fichiers du pack HD original.

Un immense merci à [@racawr](https://gamebanana.com/members/1865032) pour son travail et son aimable autorisation.

## Foire Aux Questions (FAQ)

**Y aura-t-il un tutoriel vidéo pour installer le patch ?**
Oui. Une vidéo explicative détaillée sortira sur la chaîne YouTube de [chenetulipe](https://www.youtube.com/@chenetulipe) aux alentours de la date de sortie du patch (prévue pour le 10 juillet).

**Comment puis-je aider à la relecture du jeu ?**
La phase de relecture est ouverte pour traquer les fautes, harmoniser les noms et améliorer les tournures de phrases. Un outil dédié a été développé par [Hamza](https://github.com/HamzaKarrouchi) : [Site de relecture](https://hamzakarrouchi.github.io/p2is-relecture/). 
Vous pouvez y comparer le texte original avec la traduction (en respectant la limite d'octets de chaque ligne) et utiliser le [Dictionnaire de traduction](https://hamzakarrouchi.github.io/p2is-relecture/dictionnaire.html) pour assurer la cohérence. Une fois vos modifications effectuées, générez vos propositions depuis le site et postez-les dans le salon Discord `scripts` (ou via une Pull Request sur GitHub).

**Quel est le contenu de la version BÊTA du 10 juillet ?**
Les 398 scripts de l'histoire principale (event.bin) sont 100 % traduits. La version BÊTA prévue pour le 10 juillet sera donc jouable du début à la fin avec l'histoire intégralement en français. Si nous parvenons à résoudre les problèmes techniques d'ici là, les dialogues sur la carte 3D (MMAP) et les lignes de combat (F_BE) seront également inclus. Dans le cas contraire, la bêta ne contiendra que le fichier event.bin. Toutefois, puisqu'il s'agit d'une version de test, elle pourra encore contenir des fautes de traduction, quelques textes annexes en anglais ou de potentiels crashs. L'objectif de cette bêta est de récolter vos retours pour finaliser la version 1.0.

## Clause de Non-Responsabilité

> [!CAUTION]
> Ce patch de traduction est fourni en l'état, sans aucune garantie quant à son bon fonctionnement, sa stabilité ou sa compatibilité avec toutes les configurations.

L'équipe du projet ne peut en aucun cas être tenue responsable des éventuels dommages (perte ou corruption de sauvegardes, plantages, ralentissements, instabilité de la console ou de l'émulateur). Il est impératif de conserver une copie de sauvegarde de votre ISO d'origine ainsi que de vos fichiers de sauvegarde avant toute manipulation.

En téléchargeant et en utilisant ce patch, vous acceptez pleinement cette clause.

## Documentation du Projet

Afin d'assurer la transparence et la pérennité du projet, la documentation complète est disponible :
- [**DEVELOPER.md**](./DEVELOPER.md) : L'architecture technique, le reverse-engineering du jeu et le fonctionnement de l'outil.
- [**CONTRIBUTING.md**](./CONTRIBUTING.md) : Le guide pour rejoindre les traducteurs et utiliser le site de relecture.
- [**Dictionnaire.md**](./Dictionnaire.md) : Le glossaire officiel pour garantir la cohérence des termes du jeu.
- [**CREDITS.md**](./CREDITS.md) : L'équipe principale et les remerciements.

## Contact et Communauté

Besoin d'aide ou envie de participer ? Vous pouvez nous contacter via ces canaux :

- **Serveur Discord** : [Rejoindre le projet](https://discord.gg/rd4ckSWHNm)
- **Contact Discord** : `@chenetulipe`
- **Adresse Mail** : `chenetulipe@personalegrimoireducoeur.fr`
- **Signalement de Bugs** : Pour signaler une erreur de traduction ou un bug technique, veuillez ouvrir une issue sur ce dépôt GitHub.

## Licence et Crédits

**Atlus / SEGA** : Développeurs originaux et ayants droit du jeu.

**Équipe de Traduction** : `@chenetulipe`, `@Garloulou`.

**Licence du patch** : [CC BY-NC-SA 4.0](LICENSE) (Libre d'utilisation et de modification, interdit à la vente, attribution obligatoire).

> *Persona 2: Innocent Sin* est une marque déposée de © Atlus / SEGA. Ce projet est une traduction amateur à but strictement non lucratif, réalisée par des fans pour des fans. Aucun fichier protégé par le droit d'auteur (iso, cpk, bin, etc.) n'est hébergé ou distribué sur ce dépôt. Le partage de tels fichiers est strictement interdit dans l'espace communautaire lié à ce projet.

## Star History

<a href="https://www.star-history.com/?repos=chenetulipe%2FP2-FR-IS-PSP&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=chenetulipe/P2-FR-IS-PSP&type=date&theme=dark&legend=top-left&sealed_token=LFm90kimgTV0pKr7wph4I01fXMDcl0pp1R6gKZQj-A7IbzSxbcuQ3Te4pkPherfmIEivpEoqHEUGj9nyRkBIcEEDu5ejv9MLjA1aY8v8ynFglkEs_gTGdQ" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=chenetulipe/P2-FR-IS-PSP&type=date&legend=top-left&sealed_token=LFm90kimgTV0pKr7wph4I01fXMDcl0pp1R6gKZQj-A7IbzSxbcuQ3Te4pkPherfmIEivpEoqHEUGj9nyRkBIcEEDu5ejv9MLjA1aY8v8ynFglkEs_gTGdQ" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=chenetulipe/P2-FR-IS-PSP&type=date&legend=top-left&sealed_token=LFm90kimgTV0pKr7wph4I01fXMDcl0pp1R6gKZQj-A7IbzSxbcuQ3Te4pkPherfmIEivpEoqHEUGj9nyRkBIcEEDu5ejv9MLjA1aY8v8ynFglkEs_gTGdQ" />
 </picture>
</a>

<div align="center">
  
# Persona 2: Innocent Sin FR (PSP)
  
**Projet de traduction française amateur de Persona 2: Innocent Sin sur PSP (ULES01557)**

[![Plateforme](https://img.shields.io/badge/Plateforme-PlayStation%20Portable-blue?style=flat-square&logo=playstation)](https://fr.wikipedia.org/wiki/PlayStation_Portable)
[![Langage](https://img.shields.io/badge/Python-3670A0?style=flat-square&logo=python&logoColor=white)](#)
[![Langage](https://img.shields.io/badge/React-20232A?style=flat-square&logo=react&logoColor=61DAFB)](#)
[![Langage](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)](#)
[![Statut](https://img.shields.io/badge/Statut-En%20Développement-orange?style=flat-square)](#)
[![Licence](https://img.shields.io/badge/Licence-CC%20BY--NC--SA%204.0-lightgrey.svg?style=flat-square)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![Discord](https://img.shields.io/discord/1400909421609095323?color=5865F2&label=Discord&logo=discord&logoColor=white&style=flat-square)](https://discord.gg/rd4ckSWHNm)

</div>

<br/>

> [!WARNING]
> Ce projet ne distribue aucun fichier du jeu original ni ROM piratée. Vous devez posséder votre propre image disque (ISO) extraite légalement depuis votre UMD original. Le patch est conçu exclusivement pour la version **Europe (ULES01557)**.

Ce dépôt centralise l'intégralité du projet : le patch de traduction, les outils de romhacking développés sur-mesure pour extraire et réinjecter les scripts, ainsi que toute la documentation technique relative au moteur du jeu.

---

## Sommaire
1. [Aperçu du Projet](#aperçu-du-projet)
2. [État d'Avancement](#état-davancement)
3. [Installation et Utilisation](#installation-et-utilisation)
4. [L'Outil de Romhacking (p2is_tool)](#loutil-de-romhacking-p2is_tool)
5. [Documentation du Projet](#documentation-du-projet)
6. [Licence et Crédits](#licence-et-crédits)

---

## Aperçu du Projet

<div align="center">
  <a href="https://youtu.be/rGHRMPw-bbo?si=vIguQ4_gXU1r-yoH">
    <img src="https://img.youtube.com/vi/rGHRMPw-bbo/maxresdefault.jpg" alt="Vidéo de gameplay" width="600"/>
  </a>
</div>

## État d'Avancement

| Contenu du Jeu | Progression |
|----------------|:-----------:|
| [Scripts (Dialogues Histoire Principale)](https://github.com/chenetulipe/P2-FR-IS-PSP/tree/main/scripts) | Terminée |
| [Autres Scripts (Boutiques, Dialogues Carte)](https://github.com/chenetulipe/P2-FR-IS-PSP/tree/main/AutreScript) | En cours (8/9) |
| Interface & Menus de Combat | En cours |
| Police d'écriture (Accents Français) | Terminée |
| Textures HD | En cours (35/42) |

*(Consultez le fichier [SUIVI.md](./SUIVI.md) pour les statistiques détaillées.)*

## Installation et Utilisation

Le projet est actuellement en développement actif. Une version **BÊTA** publique sera mise en ligne le **10 juillet**. Cette version sera jouable du début à la fin, avec pour objectif de recueillir les retours de la communauté pour affiner la version finale.

**Procédure d'installation :**
1. Téléchargez le patch au format `.xdelta` depuis la section [Releases](https://github.com/chenetulipe/P2-FR-IS-PSP/releases).
2. Appliquez le patch sur votre ISO originale (version Europe ULES01557) à l'aide d'un outil tel que DeltaPatcher ou xdelta UI.
3. Lancez l'ISO modifiée sur votre console PSP (équipée d'un Custom Firmware) ou sur un émulateur tel que PPSSPP.

## L'Outil de Romhacking (p2is_tool)

Le dossier `p2is_tool/` contient le code source de l'application de romhacking créée spécifiquement pour traduire Persona 2.
Construit sur une architecture moderne (Backend FastAPI et Frontend React), l'outil s'installe et se lance automatiquement via le fichier `start.bat`.

## Documentation du Projet

Afin d'assurer la transparence et la pérennité du projet, la documentation complète est disponible :
- [**DEVELOPER.md**](./DEVELOPER.md) : L'architecture technique, le reverse-engineering du jeu et le fonctionnement de l'outil.
- [**CONTRIBUTING.md**](./CONTRIBUTING.md) : Le guide pour rejoindre les traducteurs et utiliser le site de relecture.
- [**Dictionnaire.md**](./Dictionnaire.md) : Le glossaire officiel pour garantir la cohérence des termes du jeu.
- [**CREDITS.md**](./CREDITS.md) : L'équipe principale et les remerciements.

<div align="center">
  
# Guide de Contribution & Relecture
  
**Persona 2: Innocent Sin FR (PSP)**

[![Statut](https://img.shields.io/badge/Statut-Ouvert%20aux%20contributions-brightgreen?style=flat-square)](#)
[![Discord](https://img.shields.io/discord/1400909421609095323?color=5865F2&label=Discord&logo=discord&logoColor=white&style=flat-square)](https://discord.gg/rd4ckSWHNm)

</div>

<br/>

> [!NOTE]
> Merci de ton intérêt pour le projet ! Ce guide rassemble toutes les informations nécessaires pour nous aider à traduire et relire le jeu de la manière la plus simple et efficace possible.

---

## 📑 Sommaire
1. [Le Site de Relecture (Recommandé)](#le-site-de-relecture-recommandé)
2. [Soumettre ses propositions](#soumettre-ses-propositions)
3. [Règles de Traduction et Accents](#règles-de-traduction-et-accents)
4. [Balises et Codes Techniques](#balises-et-codes-techniques)

---

## 🌐 Le Site de Relecture (Recommandé)

Pour faciliter le travail de tous, un outil dédié a été développé par **@Haaamza**. Il permet de traduire, comparer et vérifier les textes sans avoir à manipuler manuellement les fichiers du jeu.

> [!IMPORTANT]
> **Lien de l'outil :** [Site de Relecture P2IS FR](https://hamzakarrouchi.github.io/p2is-relecture/)  
> **Dictionnaire de Traduction :** [Dictionnaire P2IS FR](https://hamzakarrouchi.github.io/p2is-relecture/dictionnaire.html)

**Avantages de l'outil en ligne :**
- Affiche le texte anglais et permet la saisie directe en français.
- Calcule automatiquement la **limite d'octets** du moteur du jeu.
- Connecté au glossaire officiel pour assurer la cohérence.

---

## 📬 Soumettre ses propositions

Une fois tes modifications terminées sur le site, l'outil te génère tes propositions finalisées. Tu as deux options pour nous les transmettre :

1. **Discord (Le plus simple) :** Copie les textes générés et colle-les dans le salon `#📄・scripts` sur notre [serveur Discord](https://discord.gg/rd4ckSWHNm).
2. **GitHub (Avancé) :** Fais un Fork du dépôt, modifie les fichiers JSON dans `traduction/event_scripts/` et ouvre une Pull Request titrée `[Script XXX] Proposition de traduction`.

---

## ✍️ Règles de Traduction et Accents

### 📏 Limite de Longueur
Le français est environ 20–30 % plus long que l'anglais. Chaque dialogue a un budget mémoire strict (`slot_size`). Si tu dépasses, le jeu plantera ou ignorera la phrase. **Sois concis, privilégie l'adaptation naturelle au mot-à-mot laborieux.**

### ⌨️ Espaces et Retours à la ligne
- Le code `[SP]` représente un espace. Utilise **un espace normal** dans ta traduction.
- Le code `\n` représente un retour à la ligne. Aère tes textes pour l'écran de la PSP (maximum 3 lignes par boîte de dialogue).

### ✨ Accents Supportés (100% Fonctionnels)
Grâce à un système de remappage interne et une modification de la police VRAM, **absolument tous les accents français classiques sont supportés** !

Tu peux taper naturellement sur ton clavier : 
**`é, è, ê, ë, à, â, ç, î, ï, ô, ù, û`** (ainsi que les majuscules **`É, È, À, Ç`**, etc).

L'outil s'occupe de la conversion magique en arrière-plan. Ne te prive pas de faire du vrai français propre !

---

## ⚙️ Balises et Codes Techniques

Certains codes entre crochets ont un rôle technique. **Ne les supprime jamais.**

| Balise | Signification | Comportement à adopter |
|--------|---------------|------------------------|
| `[1205][001E]` | Pause d'animation / Hésitation | Conserve-la. (Ex: `Prends...[1205][001E] ma main...`) |
| `[1113]` / `[1112]` | Prénom / Nom du Héros | Traite-les comme des variables `{{Prénom}}`. |
| `[COLOR_RED]` | Changement de couleur | Conserve-la autour du mot important. |

> [!CAUTION]
> **Codes structurels :** Si un dialogue original contient des balises comme `[NULL]`, `[1431]`, ou `[START]`, laisse-les exactement là où elles sont. Elles gèrent l'architecture de la mémoire.

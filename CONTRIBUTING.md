<div align="center">
  
# Guide de Contribution & Relecture
  
**Persona 2: Innocent Sin FR (PSP)**

[![Statut](https://img.shields.io/badge/Statut-Ouvert%20aux%20contributions-brightgreen?style=flat-square)](#)
[![Discord](https://img.shields.io/discord/1400909421609095323?color=5865F2&label=Discord&logo=discord&logoColor=white&style=flat-square)](https://discord.gg/rd4ckSWHNm)

</div>

<br/>

> [!NOTE]
> Merci de votre intérêt pour le projet. Ce guide rassemble toutes les instructions nécessaires pour participer à la traduction et à la relecture du jeu de manière optimale.

---

## Sommaire
1. [Le Site de Relecture (Recommandé)](#le-site-de-relecture-recommandé)
2. [Soumettre ses propositions](#soumettre-ses-propositions)
3. [Règles de Traduction et Accents](#règles-de-traduction-et-accents)
4. [Balises et Codes Techniques](#balises-et-codes-techniques)

---

## Le Site de Relecture (Recommandé)

Pour faciliter le travail de l'équipe, un outil web dédié a été développé par **@Haaamza**. Il permet de traduire, comparer et vérifier les textes sans avoir à manipuler manuellement les fichiers JSON du jeu.

> [!IMPORTANT]
> **Lien de l'outil :** [Site de Relecture P2IS FR](https://hamzakarrouchi.github.io/p2is-relecture/)  
> **Dictionnaire de Traduction :** [Dictionnaire P2IS FR](https://hamzakarrouchi.github.io/p2is-relecture/dictionnaire.html)

**Avantages de l'outil en ligne :**
- Affichage simultané du texte anglais original et du champ de saisie français.
- Calcul automatique de la **limite d'octets** imposée par le moteur du jeu.
- Intégration du glossaire officiel pour assurer la cohérence des termes.

---

## Soumettre ses propositions

Une fois vos modifications terminées sur le site, l'outil génère vos propositions finalisées. Deux méthodes s'offrent à vous pour nous les transmettre :

1. **Discord (Méthode Recommandée) :** Copiez les textes générés et collez-les dans le salon dédié `#scripts` sur notre [serveur Discord](https://discord.gg/rd4ckSWHNm).
2. **GitHub (Utilisateurs Avancés) :** Effectuez un Fork du dépôt, modifiez les fichiers JSON ciblés dans le dossier `traduction/event_scripts/` et ouvrez une Pull Request avec le titre `[Script XXX] Proposition de traduction`.

---

## Règles de Traduction et Accents

### Limite de Longueur
La langue française est généralement 20 à 30 % plus longue que l'anglais. Chaque dialogue possède un budget mémoire strict (`slot_size`). En cas de dépassement, le jeu ignorera la traduction ou plantera. **La concision est primordiale ; privilégiez l'adaptation naturelle plutôt qu'une traduction littérale.**

### Espaces et Retours à la ligne
- Le code `[SP]` dans le texte anglais représente un espace. Dans votre traduction française, utilisez **un espace classique**.
- Le code `\n` représente un retour à la ligne. Aérez vos textes pour l'écran de la PSP (un maximum de 3 lignes par boîte de dialogue est recommandé).

### Accents Supportés (100% Fonctionnels)
Grâce à un système de remappage interne opéré par l'outil de compilation et à une modification de la police VRAM du jeu, **l'intégralité des accents français classiques est supportée**.

Vous pouvez taper naturellement sur votre clavier les caractères suivants : 
**`é, è, ê, ë, à, â, ç, î, ï, ô, ù, û`** ainsi que leurs équivalents majuscules.

L'outil convertira ces caractères de manière transparente en arrière-plan.

---

## Balises et Codes Techniques

Certains codes entre crochets ont un rôle technique dicté par le moteur du jeu. **Ils ne doivent jamais être supprimés.**

| Balise | Signification | Comportement à adopter |
|--------|---------------|------------------------|
| `[1205][001E]` | Pause d'animation / Hésitation | À conserver. (Exemple : `Prends...[1205][001E] ma main...`) |
| `[1113]` / `[1112]` | Prénom / Nom du Héros | À traiter comme une variable de type `{{Prénom}}`. |
| `[COLOR_RED]` | Changement de couleur | À encadrer autour du mot mis en évidence. |

> [!CAUTION]
> **Codes structurels :** Si un dialogue original contient des balises de contrôle de type `[NULL]`, `[1431]`, ou `[START]`, celles-ci doivent impérativement rester à leur position initiale. Elles régissent l'architecture de la mémoire.

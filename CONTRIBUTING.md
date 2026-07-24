<div align="center">
  
# Guide de Contribution & Relecture
  
**Persona 2: Innocent Sin FR (PSP) - ULES01557**

<br/>

<img src="https://img.shields.io/badge/Statut-Ouvert_aux_contributions-2ea043?style=for-the-badge" alt="Statut" />
<a href="https://discord.gg/rd4ckSWHNm"><img src="https://img.shields.io/discord/1400909421609095323?color=5865F2&label=Discord&logo=discord&logoColor=white&style=flat-square" alt="Discord" /></a>
<img src="https://img.shields.io/badge/Outil_Relecture-En_Ligne-009688?style=for-the-badge" alt="Outil de Relecture" />

</div>

<br/>

> [!NOTE]
> Merci de votre intérêt pour le projet de traduction française de *Persona 2: Innocent Sin* ! Ce guide rassemble toutes les instructions et règles techniques nécessaires pour participer à la traduction et à la relecture du jeu en toute sécurité, sans risquer de corrompre les fichiers de l'ISO.

<br/>

---

## Sommaire
1. [L'Outil de Relecture en Ligne (Obligatoire)](#loutil-de-relecture-en-ligne-obligatoire)
2. [Soumettre vos traductions](#soumettre-vos-traductions)
3. [La Limite Critique de Longueur (Octets)](#la-limite-critique-de-longueur-octets)
4. [Règles de Traduction et d'Écriture](#règles-de-traduction-et-décriture)
5. [Le Dictionnaire des Balises In-Game](#le-dictionnaire-des-balises-in-game)

<br/>

---

## L'Outil de Relecture en Ligne (Obligatoire)

Pour simplifier le travail de l'équipe et éviter que les contributeurs ne manipulent directement du code JSON complexe, une application web dédiée a été développée par **@HamzaKarrouchi**. C'est le centre de contrôle de la traduction.

> [!IMPORTANT]
> ✦ **Accéder à l'Outil :** [Site de Relecture P2IS FR](https://hamzakarrouchi.github.io/p2is-relecture/)<br/>
> ✦ **Le Glossaire Officiel :** [Dictionnaire P2IS FR](https://hamzakarrouchi.github.io/p2is-relecture/dictionnaire.html)

**Pourquoi utiliser cet outil est obligatoire ?**
* **Double Affichage :** Affiche simultanément le dialogue anglais original et votre proposition française.
* **Sécurité Anti-Crash :** L'outil intègre un compteur dynamique qui calcule la limite stricte de longueur en octets pour éviter de faire planter le moteur du jeu.
* **Intégration du Lore :** Le glossaire est directement intégré pour garantir la cohérence des noms propres (Démons, Sorts, Objets).

<br/>

---

## Soumettre vos traductions

Une fois vos relectures ou traductions terminées sur le site de @HamzaKarrouchi, l'outil vous générera un bloc de texte propre et formaté. Deux méthodes pour nous le transmettre :

1. **Via Discord (Méthode Recommandée) :** 
   Copiez simplement le bloc généré par l'outil web et collez-le dans le salon `#scripts` sur notre [serveur Discord officiel](https://discord.gg/rd4ckSWHNm). Un développeur se chargera de l'injecter.
   
2. **Via GitHub (Utilisateurs Avancés) :** 
   Effectuez un Fork de ce dépôt, insérez vos modifications dans les fichiers `.json` du dossier `traduction/` et ouvrez une Pull Request avec le titre `[Script XXX] Proposition de traduction`.

<br/>

---

## La Limite Critique de Longueur (Octets)

> [!WARNING]
> La langue française est structurellement 20 à 30 % plus longue que l'anglais. Or, l'architecture du jeu PSP est extrêmement stricte concernant la mémoire.

**La Règle d'Or : La Concision.**
Privilégiez toujours l'adaptation naturelle et percutante plutôt que la traduction littérale mot-à-mot. 

* **Pour l'histoire (`event.bin`) :** L'outil de compilation arrive à recalculer l'espace dynamiquement, mais l'écran de la console, lui, ne grandit pas ! Aérez toujours vos textes avec des sauts de ligne pour **ne jamais dépasser 3 lignes par boîte de dialogue**.
* **Pour les combats et menus (`F_BE.BNP` / `EBOOT.BIN`) :** La contrainte est absolue. Si le texte de combat dépasse le nombre d'octets originaux, le jeu subira un dépassement de mémoire (*Invalid Memory Access*) et la PSP s'éteindra. L'Outil de Relecture vous avertira si votre texte est trop long, écoutez-le toujours !

<br/>

---

## Règles de Traduction et d'Écriture

### 1. Les Accents Français (100% Supportés !)
Contrairement à beaucoup de vieux jeux japonais, **vous n'avez pas à vous soucier des accents**. 
Vous pouvez taper naturellement sur votre clavier français :
**`é, è, ê, ë, à, â, ç, î, ï, ô, ù, û`** ainsi que leurs majuscules.

Notre outil de compilation possède un algorithme (`ACCENT_MAP`) qui intercepte vos lettres et les convertit en secret vers des glyphes modifiés que le jeu peut lire.

### 2. Espaces et Ponctuation
* Le code `[SP]` dans le texte anglais représente un espace insécable. Dans votre traduction française, **effacez-le et utilisez un espace classique** de la barre d'espace de votre clavier.
* Le code `
` représente un retour à la ligne. Utilisez-le intelligemment pour structurer vos paragraphes.
* Les points de suspension `...` doivent être tapés classiquement (trois petits points), l'outil les gérera tout seul.

<br/>

---

## Le Dictionnaire des Balises In-Game

Dans les textes anglais de l'outil, vous trouverez des codes étranges entre crochets. Ce sont des **Opcodes hexadécimaux** qui donnent des ordres directs au processeur de la PSP (comme nettoyer l'écran, afficher un menu de choix, ou mettre le jeu en pause).

> [!CAUTION]
> **Règle vitale :** Vous devez copier ces balises et les placer logiquement dans votre traduction française. Si vous supprimez accidentellement une balise, le jeu crashera.

| Balise à Conserver | Fonction Visuelle dans le jeu | Exemple d'utilisation dans la traduction |
|:---|:---|:---|
| `[1205][001E]` | **Pause Dramatique** du texte. Oblige le joueur à attendre une seconde avant la suite de la phrase. | `Tu penses vraiment...[1205][001E] qu'on va te laisser filer ?` |
| `[1113]` | **Prénom du Héros** (Tatsuya). C'est une variable dynamique car le joueur peut renommer le héros. | `Salut [1113], comment ça va ?` |
| `[1112]` | **Nom de Famille** (Suou). | `C'est le cadet de la famille [1112].` |
| `[1208][0002]` | **Déclencheur de Menu de Choix !** (Critique). Apparaît quand le joueur doit répondre Oui ou Non. | `Tu viens avec nous ?
[1208][0002][1432]...` |
| `[0014]` | **Séparateur d'options** d'un menu de choix. Sépare le "Oui" du "Non". Ne jamais effacer ! | `...[0014]Oui[1432][NULL][0014]
[1432]...[0014]Non` |
| `[COLOR_RED]` | **Changement de Couleur**. Doit encadrer le mot mis en évidence. | `C'est une rumeur très [COLOR_RED]dangereuse[COLOR_DEFAULT].` |
| `[1108]` | **Fenêtre de Portrait (Bust-up)**. Demande au jeu d'afficher le dessin du personnage qui parle. | Se trouve souvent au début ou à la fin d'une réplique. |
| `[U+XXXX]` | **Balise Inconnue**. Si vous voyez `[U+1A2B]`, c'est un code de la console que l'on n'a pas encore décrypté. | À laisser exactement là où il était. |


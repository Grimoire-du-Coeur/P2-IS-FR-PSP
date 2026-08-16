<div align="center">
  
# 🎭 Persona 2: Innocent Sin FR 🎭
  
**Le patch de traduction française intégral pour PSP (ULES01557)**

<br/>

<a href="https://fr.wikipedia.org/wiki/PlayStation_Portable"><img src="https://img.shields.io/badge/PlayStation_Portable-103F91?style=for-the-badge&logo=playstation&logoColor=white" alt="Plateforme" /></a>
<img src="https://img.shields.io/badge/Statut-BÊTA_DISPONIBLE-6b21a8?style=for-the-badge" alt="Statut" />
<a href="https://personalegrimoireducoeur.fr/"><img src="https://img.shields.io/badge/Site_Web-personagrimoireducoeur.fr-10b981?style=for-the-badge&logo=vercel&logoColor=white" alt="Site Officiel" /></a>

<br/>

<a href="https://github.com/chenetulipe/P2-FR-IS-PSP/commits/main"><img src="https://img.shields.io/github/last-commit/chenetulipe/P2-FR-IS-PSP?style=flat-square&color=2ea043" alt="Dernier Commit" /></a>
<a href="https://github.com/chenetulipe/P2-FR-IS-PSP/issues"><img src="https://img.shields.io/github/issues/chenetulipe/P2-FR-IS-PSP?style=flat-square&color=d73a49" alt="Issues" /></a>
<a href="https://discord.gg/rd4ckSWHNm"><img src="https://img.shields.io/discord/1400909421609095323?color=5865F2&label=Discord&logo=discord&logoColor=white&style=flat-square" alt="Discord" /></a>

<br/><br/>

[![Télécharger le Patch](https://img.shields.io/badge/TÉLÉCHARGER_LE_PATCH_FR-Release_BÊTA_v0.1.3-e3b341?style=for-the-badge&logo=github&logoColor=black)](https://github.com/chenetulipe/P2-FR-IS-PSP/releases)

L'histoire principale est **100% jouable en français** avec le dernier patch !

</div>

<br/>

---

## 📖 Aperçu du Projet

Bienvenue sur le dépôt officiel du projet de traduction française de **Persona 2: Innocent Sin**. 
Ce dépôt centralise non seulement le patch jouable, mais également l'intégralité des **outils de romhacking** que nous avons développés sur-mesure, ainsi que la documentation technique du jeu.

### Vidéos de présentation & Tutoriels d'installation

<div align="center">
  <a href="https://youtu.be/rGHRMPw-bbo">
    <img src="https://img.youtube.com/vi/rGHRMPw-bbo/maxresdefault.jpg" alt="Aperçu du jeu en français" width="400" style="border-radius: 8px; margin-right: 15px;"/>
  </a>
  <a href="https://www.youtube.com/@chenetulipe">
    <img src="https://img.youtube.com/vi/aL3N1Xk6X8w/maxresdefault.jpg" alt="Tutoriel d'installation par chenetulipe" width="400" style="border-radius: 8px;"/>
  </a>
  <br/>
  <i>(Gauche: Gameplay du patch FR | Droite: Tutoriels sur la chaîne de chenetulipe)</i>
</div>

> [!NOTE]
> 📈 **État d'avancement rapide** : L'histoire principale (Event.bin) et les dialogues des PNJs (MMAP) sont à **100% traduits**. Les menus, objets et sorts (EBOOT) sont en cours de traduction (environ **15%**). Pour voir le tableau complet de notre progression, [consultez notre Guide de Contribution (CONTRIBUTING.md)](./CONTRIBUTING.md).

<br/>

---

## 📥 Guide d'Installation (Patch & Textures HD)

Le projet est actuellement en phase de **BÊTA publique**.

### Étape 1 : Patcher l'ISO originale
1. Téléchargez le dernier fichier patch au format `.xdelta` depuis la section **[Releases](https://github.com/chenetulipe/P2-FR-IS-PSP/releases)**.
2. Obtenez (légalement) une image ISO de la version européenne originale du jeu (`ULES01557`).
3. Allez sur notre **[Patcher Web en Ligne](https://personalegrimoireducoeur.fr/patcher/)** (aucune installation n'est requise sur votre PC).
4. Glissez votre fichier ISO et notre fichier `.xdelta` dans le Patcher Web pour générer votre ISO modifiée en français.

### Étape 2 : Installer le Pack de Textures HD (PPSSPP)
L'installation de ce pack est fortement recommandée sur émulateur pour afficher la nouvelle police française haute définition avec les accents.
1. Téléchargez le pack HD de base sur GameBanana : [HD UI for Persona 2](https://gamebanana.com/mods/308752).
2. Placez-le dans le dossier `TEXTURES/ULES01557/` de votre émulateur PPSSPP.
3. Téléchargez notre correctif **Patch de Textures FR** (disponible dans les [Releases](https://github.com/chenetulipe/P2-FR-IS-PSP/releases)).
4. Collez les dossiers extraits par-dessus le pack HD pour écraser les textures anglaises par notre version française.
5. Activez l'option *Remplacer les textures* dans PPSSPP.

<br/>

---

## 🛠️ La Suite d'Outils de Romhacking

Nous avons dû créer toute une suite de logiciels internes pour analyser, extraire et réinjecter les données complexes du jeu.

> 💡 **Note sur les dépendances Python** : L'intégralité des dépendances de TOUS nos scripts (`p2is_tool`, `p2is_audio_lab`, `p2is_image_lab`, outils CPK...) a été consolidée. Exécutez simplement `pip install -r requirements.txt` à la racine pour tout installer.

### 1. L'Outil Principal (p2is_tool)
Le cœur du projet. Application moderne développée pour extraire et traduire de façon collaborative (via API) les scripts complexes du jeu.
* **Techno** : FastAPI (Python), React (JS).
* **Usage** : Extraction massive, gestion des balises Hexa, interface web pour les traducteurs.

### 2. Le Patcher Web (p2is_patcher)
Application 100% autonome et locale tournant dans le navigateur, permettant aux joueurs d'appliquer le patch `.xdelta` sans installer de logiciel externe.
* **Techno** : WebAssembly, HTML/CSS, Vanilla JS.

### 3. L'Outil de Traitement d'Images (p2is_image_lab)
Laboratoire complet spécialisé dans l'extraction, l'édition et la réinjection chirurgicale des images compressées au format propriétaire GIM (CRILAYLA), nécessaire pour modifier les écrans de chargement et l'UI sans dépasser les limites de taille de l'ISO.
* **Techno** : Python, Algorithmes CRILAYLA, FastAPI.

### 4. L'Outil de Traitement Audio (p2is_audio_lab)
Laboratoire permettant d'extraire, d'isoler et de convertir les pistes audio du jeu (doublages et musiques) depuis et vers le format propriétaire AT3 (ATRAC3).
* **Techno** : Python, wrappers pour ATRACTool.

<br/>

---

## ⚖️ Clause de Non-Responsabilité & Licences

> [!WARNING]
> **Tolérance Zéro au Piratage** : Ce projet ne distribue **aucun fichier original du jeu ni ROM piratée**. Vous devez extraire légalement votre propre image disque (ISO) depuis votre UMD original. Ce patch est exclusif à la version Europe. L'équipe décline toute responsabilité en cas de corruption de sauvegarde. *Persona 2: Innocent Sin* est une marque déposée de © Atlus / SEGA.

### 📜 Licences du Code et du Patch

Afin de protéger le travail communautaire tout en respectant les outils open-source tiers, notre projet repose sur un modèle de licences scindé :

1. **Le Patch FR et nos Outils Maison (p2is_tool, image_lab, audio_lab)**
   Distribués sous licence **[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)**. 
   * Vous pouvez les utiliser, les modifier (pour créer une trad dans une autre langue par exemple) à condition de **créditer notre équipe**, de **ne pas en faire d'usage commercial** (vente strictement interdite), et de **partager votre projet dérivé sous la même licence**.
   * *Note pour les créateurs :* Les YouTubers et Streamers sont autorisés à utiliser ce patch et monétiser leurs vidéos.

2. **Le Web Patcher (p2is_patcher)**
   Il intègre directement le code source du moteur DeltaPatcher. Pour respecter les droits d'auteur d'origine, cette partie spécifique est sous licence **[GPL-2.0](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html)**.

### ⚙️ Mentions des Outils Tiers (Légaux et Indépendants)
* **p2is_cpk_tool.py** : Notre propre script Python d'extraction/reconstruction des archives CPK, remplaçant *CriFsLib*.
* **pspdecrypt** (par John-K) : Exécutable `.exe` open-source appelé en externe pour déchiffrer l'EBOOT.
* **pycdlib** (par clalancette) : Importée dynamiquement (LGPL-2.1). Notre code Python interagit avec l'API pycdlib sans la modifier, respectant les termes de la LGPL.
* **ATRACTool-Reloaded** (par XyLe-GBP) : Exécutable appelé en ligne de commande par `p2is_audio_lab`.

<br/>

---

## 📚 Documentation et Liens

* **[DEVELOPER.md](./DEVELOPER.md)** : Architecture technique et reverse-engineering.
* **[CONTRIBUTING.md](./CONTRIBUTING.md)** : Guide de contribution et tableau d'avancement des traductions.
* **[Dictionnaire.md](./Dictionnaire.md)** : Le glossaire officiel pour garantir la cohérence des termes.
* **[SUIVI.md](./SUIVI.md)** : Historique détaillé des patchs.
* **[CREDITS.md](./CREDITS.md)** : Équipe principale et contributeurs.

Besoin d'aide ? Consultez notre **[F.A.Q Officielle](https://personalegrimoireducoeur.fr/faq.html)** ou rejoignez-nous sur **[Discord](https://discord.gg/rd4ckSWHNm)** !

<div align="center">
  <a href="https://www.star-history.com/?repos=chenetulipe%2FP2-FR-IS-PSP&type=date&legend=top-left">
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=chenetulipe/P2-FR-IS-PSP&type=date&legend=top-left&sealed_token=LFm90kimgTV0pKr7wph4I01fXMDcl0pp1R6gKZQj-A7IbzSxbcuQ3Te4pkPherfmIEivpEoqHEUGj9nyRkBIcEEDu5ejv9MLjA1aY8v8ynFglkEs_gTGdQ" width="800" />
  </a>
</div>

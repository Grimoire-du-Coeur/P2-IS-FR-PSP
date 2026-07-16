# Suivi Technique et Problèmes Connus

Ce document répertorie les limitations techniques, les bugs connus et la dette technique du projet de traduction de Persona 2: Innocent Sin (PSP).

## 1. Dépassements de Mémoire (Overflows)

### Le problème
Le moteur du jeu alloue une taille maximale stricte (en octets) pour chaque bloc de texte dans les fichiers binaires (`.BNP`, `.BIN`). Si la traduction française est plus longue (en octets) que le texte original anglais/japonais, le compilateur (`compile_event_en.exe`) tronque purement et simplement le texte, causant des textes coupés en plein milieu d'une phrase.

### La solution
Nous avons généré un inventaire complet de ces dépassements (199 textes concernés). Pour les corriger, il faut **reformuler la traduction** pour la rendre plus courte. Le script `check_real_overflows.py` (dans `scripts/`) permet de recalculer la taille en temps réel.

## 2. L'encodage des fichiers MMAP et F_BE

### Le problème
Contrairement à `event.bin` (les dialogues principaux) qui est relativement bien géré, les fichiers **MMAP** (noms des lieux, texte de la carte) et **F_BE** (menus de combat, UI) sont extrêmement capricieux :
- Les longueurs maximales de ces textes sont codées en dur à plusieurs endroits.
- Ils n'utilisent pas exactement les mêmes tables de caractères ou les mêmes règles de saut de ligne.
- Toute modification un peu trop longue fait crasher l'ISO ou provoque des glitchs graphiques.

### Ce qu'il faut faire
- Garder les textes des menus (F_BE) et de la carte (MMAP) **aussi courts que possible**, idéalement de la même longueur exacte que l'anglais.
- Ne pas utiliser de caractères spéciaux ou de balises complexes dans ces fichiers.

## 3. Découpage dynamique des boîtes de dialogue (auto_wrap)

### Le fonctionnement actuel
Pour éviter que le texte ne sorte visuellement de la boîte de dialogue, nous avons mis en place le script `auto_wrap.py`. Il recalcule la longueur visuelle de chaque mot (en ignorant les balises d'émotion qui prennent 0 caractère, mais en corrigeant les espaces manquants après la ponctuation).

- **Limite actuelle** : 46 caractères par ligne maximum.
- **Lignes par page** : Le moteur gère automatiquement le passage à la page suivante (avec la petite flèche rouge) au bout de 3 lignes pleines. Le script équilibre le texte pour que les 3 lignes soient de longueur égale.

### Bugs restants / à surveiller
- Vérifier que certaines balises d'émotion (ex: `[1205][U+XXXX]`) ne provoquent pas d'espacements bizarres si elles sont collées à la ponctuation. Le script `auto_wrap.py` gère normalement les espaces de manière intelligente.

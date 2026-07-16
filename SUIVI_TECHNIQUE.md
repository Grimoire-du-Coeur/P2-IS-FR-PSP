# Suivi Technique et Problèmes Connus

Ce document répertorie les limitations techniques, les bugs connus et la dette technique du projet de traduction de Persona 2: Innocent Sin (PSP).

## 1. Dépassements de Mémoire (Overflows)

### Le problème
Le moteur du jeu alloue une taille maximale stricte (en octets) pour chaque bloc de texte dans les fichiers binaires (.BNP, .BIN). Si la traduction française est plus longue (en octets) que le texte original anglais/japonais, le compilateur (compile_event_en.exe) tronque purement et simplement le texte, causant des textes coupés en plein milieu d'une phrase.

### La solution
Nous avons généré un inventaire complet de ces dépassements (199 textes concernés). Pour les corriger, il faut **reformuler la traduction** pour la rendre plus courte. Le script check_real_overflows.py (dans scripts/) permet de recalculer la taille en temps réel.

<details><summary><b>Cliquez ici pour afficher le tableau des 199 dépassements réels</b></summary>
<br>

# Vrai Inventaire des Dépassements de Mémoire

Voici la liste **réelle** des dialogues qui dépassent la taille mémoire allouée par le jeu dans les fichiers binaires (slot_size). Ce ne sont pas des débordements visuels, mais bien des textes trop longs pour rentrer dans la mémoire de la PSP !

Il y a **199** vrais dépassements.

| Fichier | ID | Taille Actuelle | Limite |
|---|---|---|---|
| script_004.json | 17 | 64 octets | 60 octets |
| script_013.json | 25 | 178 octets | 172 octets |
| script_016.json | 5 | 194 octets | 192 octets |
| script_023.json | 10 | 264 octets | 256 octets |
| script_023.json | 12 | 180 octets | 170 octets |
| script_023.json | 13 | 128 octets | 114 octets |
| script_024.json | 8 | 192 octets | 190 octets |
| script_024.json | 10 | 202 octets | 200 octets |
| script_031.json | 18 | 206 octets | 204 octets |
| script_031.json | 21 | 210 octets | 206 octets |
| script_034.json | 1 | 490 octets | 488 octets |
| script_085.json | 64 | 86 octets | 82 octets |
| script_085.json | 146 | 180 octets | 178 octets |
| script_085.json | 147 | 204 octets | 202 octets |
| script_142.json | 17 | 284 octets | 274 octets |
| script_149.json | 5 | 244 octets | 242 octets |
| script_149.json | 32 | 326 octets | 322 octets |
| script_149.json | 33 | 210 octets | 204 octets |
| script_197.json | 10 | 176 octets | 166 octets |
| script_199.json | 0 | 1192 octets | 1162 octets |
| script_258.json | 17 | 296 octets | 286 octets |
| script_258.json | 20 | 310 octets | 300 octets |
| script_258.json | 22 | 234 octets | 220 octets |
| script_261.json | 6 | 160 octets | 158 octets |
| script_261.json | 13 | 196 octets | 192 octets |
| script_261.json | 15 | 164 octets | 162 octets |
| script_261.json | 16 | 164 octets | 162 octets |
| script_266.json | 0 | 258 octets | 256 octets |
| script_266.json | 15 | 652 octets | 638 octets |
| script_268.json | 11 | 310 octets | 304 octets |
| script_281.json | 53 | 688 octets | 682 octets |
| script_281.json | 88 | 240 octets | 230 octets |
| script_281.json | 90 | 178 octets | 174 octets |
| script_281.json | 91 | 178 octets | 174 octets |
| script_288.json | 91 | 394 octets | 392 octets |
| script_288.json | 95 | 140 octets | 138 octets |
| script_289.json | 52 | 140 octets | 138 octets |
| script_290.json | 90 | 130 octets | 128 octets |
| script_291.json | 8 | 208 octets | 204 octets |
| script_291.json | 33 | 408 octets | 400 octets |
| script_291.json | 37 | 130 octets | 128 octets |
| script_292.json | 52 | 138 octets | 136 octets |
| script_293.json | 37 | 138 octets | 136 octets |
| script_294.json | 30 | 196 octets | 194 octets |
| script_295.json | 24 | 196 octets | 194 octets |
| script_295.json | 30 | 204 octets | 202 octets |
| script_296.json | 76 | 290 octets | 276 octets |
| script_296.json | 93 | 312 octets | 300 octets |
| script_296.json | 94 | 294 octets | 288 octets |
| script_296.json | 263 | 134 octets | 130 octets |
| script_296.json | 278 | 208 octets | 194 octets |
| script_296.json | 299 | 288 octets | 274 octets |
| script_296.json | 300 | 344 octets | 330 octets |
| script_296.json | 301 | 352 octets | 338 octets |
| script_296.json | 308 | 134 octets | 132 octets |
| script_311.json | 108 | 112 octets | 110 octets |
| script_311.json | 118 | 112 octets | 110 octets |
| script_312.json | 8 | 202 octets | 198 octets |
| script_312.json | 11 | 180 octets | 176 octets |
| script_312.json | 59 | 112 octets | 110 octets |
| script_312.json | 69 | 112 octets | 110 octets |
| script_313.json | 33 | 518 octets | 512 octets |
| script_313.json | 78 | 484 octets | 482 octets |
| script_315.json | 81 | 138 octets | 136 octets |
| script_316.json | 19 | 138 octets | 136 octets |
| script_317.json | 50 | 198 octets | 196 octets |
| script_318.json | 17 | 198 octets | 196 octets |
| script_319.json | 179 | 180 octets | 178 octets |
| script_319.json | 180 | 204 octets | 202 octets |
| script_320.json | 80 | 110 octets | 104 octets |
| script_320.json | 81 | 188 octets | 186 octets |
| script_320.json | 82 | 204 octets | 202 octets |
| script_321.json | 37 | 318 octets | 314 octets |
| script_321.json | 109 | 180 octets | 178 octets |
| script_321.json | 110 | 204 octets | 202 octets |
| script_324.json | 53 | 794 octets | 792 octets |
| script_324.json | 126 | 194 octets | 192 octets |
| script_324.json | 128 | 166 octets | 162 octets |
| script_324.json | 129 | 166 octets | 162 octets |
| script_325.json | 28 | 166 octets | 162 octets |
| script_325.json | 29 | 166 octets | 162 octets |
| script_326.json | 71 | 320 octets | 298 octets |
| script_327.json | 11 | 306 octets | 298 octets |
| script_327.json | 14 | 310 octets | 298 octets |
| script_332.json | 57 | 272 octets | 268 octets |
| script_335.json | 5 | 408 octets | 370 octets |
| script_335.json | 8 | 314 octets | 298 octets |
| script_336.json | 109 | 138 octets | 136 octets |
| script_336.json | 113 | 290 octets | 288 octets |
| script_336.json | 114 | 306 octets | 304 octets |
| script_337.json | 19 | 138 octets | 136 octets |
| script_338.json | 68 | 214 octets | 212 octets |
| script_339.json | 20 | 214 octets | 212 octets |
| script_342.json | 213 | 142 octets | 140 octets |
| script_343.json | 82 | 142 octets | 140 octets |
| script_347.json | 14 | 1912 octets | 1906 octets |
| script_349.json | 45 | 388 octets | 364 octets |
| script_349.json | 48 | 334 octets | 314 octets |
| script_349.json | 64 | 148 octets | 146 octets |
| script_349.json | 82 | 148 octets | 146 octets |
| script_350.json | 19 | 368 octets | 364 octets |
| script_350.json | 22 | 368 octets | 364 octets |
| script_350.json | 65 | 148 octets | 146 octets |
| script_350.json | 83 | 148 octets | 146 octets |
| script_351.json | 67 | 130 octets | 128 octets |
| script_352.json | 4 | 488 octets | 448 octets |
| script_352.json | 24 | 130 octets | 128 octets |
| script_353.json | 61 | 138 octets | 136 octets |
| script_354.json | 21 | 138 octets | 136 octets |
| script_355.json | 49 | 212 octets | 208 octets |
| script_355.json | 56 | 218 octets | 216 octets |
| script_355.json | 73 | 200 octets | 196 octets |
| script_356.json | 19 | 228 octets | 208 octets |
| script_356.json | 26 | 218 octets | 216 octets |
| script_356.json | 33 | 216 octets | 196 octets |
| script_359.json | 97 | 1008 octets | 990 octets |
| script_359.json | 214 | 126 octets | 124 octets |
| script_360.json | 9 | 180 octets | 176 octets |
| script_360.json | 10 | 210 octets | 194 octets |
| script_360.json | 22 | 316 octets | 308 octets |
| script_360.json | 35 | 1018 octets | 990 octets |
| script_360.json | 147 | 126 octets | 124 octets |
| script_365.json | 20 | 272 octets | 270 octets |
| script_365.json | 23 | 240 octets | 238 octets |
| script_365.json | 55 | 120 octets | 118 octets |
| script_365.json | 70 | 120 octets | 118 octets |
| script_366.json | 11 | 272 octets | 270 octets |
| script_366.json | 14 | 240 octets | 238 octets |
| script_366.json | 25 | 120 octets | 118 octets |
| script_366.json | 40 | 120 octets | 118 octets |
| script_367.json | 59 | 298 octets | 288 octets |
| script_367.json | 62 | 294 octets | 288 octets |
| script_367.json | 84 | 146 octets | 144 octets |
| script_368.json | 21 | 322 octets | 288 octets |
| script_368.json | 24 | 322 octets | 288 octets |
| script_368.json | 34 | 146 octets | 144 octets |
| script_369.json | 69 | 138 octets | 136 octets |
| script_370.json | 21 | 138 octets | 136 octets |
| script_371.json | 92 | 184 octets | 182 octets |
| script_372.json | 19 | 184 octets | 182 octets |
| script_373.json | 125 | 164 octets | 162 octets |
| script_373.json | 126 | 164 octets | 162 octets |
| script_375.json | 55 | 298 octets | 296 octets |
| script_375.json | 81 | 208 octets | 206 octets |
| script_375.json | 108 | 280 octets | 264 octets |
| script_375.json | 109 | 226 octets | 224 octets |
| script_375.json | 110 | 226 octets | 224 octets |
| script_375.json | 134 | 162 octets | 160 octets |
| script_376.json | 45 | 208 octets | 206 octets |
| script_376.json | 73 | 228 octets | 224 octets |
| script_376.json | 74 | 228 octets | 224 octets |
| script_377.json | 27 | 116 octets | 114 octets |
| script_378.json | 19 | 270 octets | 254 octets |
| script_379.json | 17 | 288 octets | 276 octets |
| script_379.json | 21 | 312 octets | 300 octets |
| script_379.json | 22 | 294 octets | 288 octets |
| script_379.json | 139 | 134 octets | 130 octets |
| script_379.json | 142 | 206 octets | 194 octets |
| script_379.json | 163 | 286 octets | 274 octets |
| script_379.json | 164 | 460 octets | 448 octets |
| script_379.json | 165 | 360 octets | 338 octets |
| script_379.json | 170 | 134 octets | 132 octets |
| script_381.json | 47 | 180 octets | 178 octets |
| script_381.json | 48 | 204 octets | 202 octets |
| script_382.json | 32 | 202 octets | 192 octets |
| script_382.json | 34 | 164 octets | 162 octets |
| script_382.json | 35 | 164 octets | 162 octets |
| script_387.json | 7 | 312 octets | 310 octets |
| script_389.json | 20 | 124 octets | 122 octets |
| script_390.json | 73 | 272 octets | 262 octets |
| script_390.json | 74 | 248 octets | 238 octets |
| script_390.json | 75 | 260 octets | 250 octets |
| script_390.json | 76 | 260 octets | 250 octets |
| script_390.json | 77 | 260 octets | 250 octets |
| script_390.json | 78 | 292 octets | 282 octets |
| script_390.json | 79 | 296 octets | 286 octets |
| script_390.json | 80 | 384 octets | 374 octets |
| script_390.json | 81 | 384 octets | 374 octets |
| script_390.json | 85 | 264 octets | 254 octets |
| script_390.json | 95 | 174 octets | 172 octets |
| script_390.json | 96 | 174 octets | 172 octets |
| script_395.json | 3 | 344 octets | 342 octets |
| F_BE.json | 2 | 306 octets | 276 octets |
| F_BE.json | 3 | 132 octets | 94 octets |
| F_BE.json | 4 | 88 octets | 78 octets |
| F_BE.json | 5 | 100 octets | 98 octets |
| F_BE.json | 6 | 296 octets | 264 octets |
| F_BE.json | 7 | 124 octets | 116 octets |
| F_BE.json | 9 | 118 octets | 96 octets |
| F_BE.json | 10 | 294 octets | 264 octets |
| F_BE.json | 13 | 338 octets | 302 octets |
| F_BE.json | 14 | 140 octets | 118 octets |
| F_BE.json | 16 | 108 octets | 104 octets |
| F_BE.json | 17 | 116 octets | 102 octets |
| F_BE.json | 21 | 96 octets | 94 octets |
| F_BE.json | 23 | 322 octets | 290 octets |
| F_BE.json | 24 | 116 octets | 102 octets |
| F_BE.json | 26 | 290 octets | 260 octets |
| MMAP06.json | 277 | 244 octets | 242 octets |


</details>

## 2. Le Bug de la Cinématique de Philemon (Saut de Scène)

### Le problème
Au début du jeu, lors de la scène de rencontre avec Eikichi, ce dernier s'énerve et invoque sa Persona. Normalement, la scène se poursuit (Lisa et Tatsuya invoquent aussi leur Persona, puis tous s'évanouissent). 
**Bug actuel :** Dès qu'Eikichi s'énerve, le jeu saute brusquement à la cinématique de Philemon, qui s'affiche de manière décalée (glitch).

### Explication Technique
Ce problème est probablement lié à un bug d'encodage (dans F_BE.json ou un MMAP). Le moteur lit une balise erronée (ou un dépassement de tampon) qui agit comme un déclencheur involontaire sautant le script d'événement normal pour lancer la cinématique suivante. 
Ces systèmes de codage différents rendent la suppression de certaines balises récalcitrantes très difficile sous peine de corrompre l'ordre d'exécution des événements.

## 3. L'encodage des fichiers MMAP et F_BE

### Le problème
Contrairement à event.bin (les dialogues principaux) qui est relativement bien géré, les fichiers **MMAP** (noms des lieux, texte de la carte) et **F_BE** (menus de combat, UI) sont extrêmement capricieux :
- Les longueurs maximales de ces textes sont codées en dur à plusieurs endroits.
- Ils n'utilisent pas exactement les mêmes tables de caractères ou les mêmes règles de saut de ligne.
- Toute modification un peu trop longue fait crasher l'ISO ou provoque des glitchs graphiques.

### Ce qu'il faut faire
- Garder les textes des menus (F_BE) et de la carte (MMAP) **aussi courts que possible**, idéalement de la même longueur exacte que l'anglais.
- **Rappel :** Le fichier MMAP03 est actuellement **non traduit** et devra être traité avec les mêmes précautions.

## 4. Finalisation de TM_EVE.json

La traduction des cinématiques narratives (TM_EVE.json) a été initiée via une Pull Request, mais elle est très incomplète. Ce fichier est crucial pour l'histoire principale et doit être finalisé au plus vite pour garantir une expérience de jeu cohérente.

## 5. Découpage dynamique des boîtes de dialogue (auto_wrap)

### Le fonctionnement actuel
Pour éviter que le texte ne sorte visuellement de la boîte de dialogue, nous avons mis en place le script uto_wrap.py. Il recalcule la longueur visuelle de chaque mot.
- **Limite actuelle** : 46 caractères par ligne maximum.
- **Lignes par page** : Le moteur gère le passage à la page suivante au bout de 3 lignes pleines. Le script équilibre le texte pour que les 3 lignes soient de longueur égale.

### Bugs restants / à surveiller
- Vérifier que certaines balises d'émotion (ex: [1205][U+XXXX]) ne provoquent pas d'espacements bizarres si elles sont collées à la ponctuation. Le script uto_wrap.py gère normalement les espaces de manière intelligente.

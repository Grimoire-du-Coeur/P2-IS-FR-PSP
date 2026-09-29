# 📋 Rapport Exhaustif des Modifications et Calibrages (v0.2.8)
### *Persona 2: Innocent Sin (PSP EUR) — Traduction Française*

> **Statut :** Validé à 100% — **0 dépassement binaire restant sur l'ensemble du jeu.**
> **Nombre total de dialogues traités :** **477** répliques optimisées.
> **Garantie d'intégrité :** Aucun ISO ni patch xdelta n'a été produit ; seuls les fichiers sources JSON ont été harmonisés.

---

## 1. Synthèse des Interventions

Afin de garantir que le jeu ne freeze jamais, ne corrompe pas la mémoire de la PSP et respecte rigoureusement la taille allouée (`data_size`) pour chaque slot de dialogue, les interventions suivantes ont été menées par vagues chirurgicales :

1. **Nettoyage des méga-accidents d'édition :**
   - Plusieurs dialogues contenaient par mégarde des descriptions d'éléments de décor (inventaire de chambre, textes de mégalithes, panneaux d'orientation de commissariat, lettres de loterie, reliefs de temples...) collées à la suite des paroles des personnages. Ces ajouts parasites créaient des dépassements de 200 à 800+ octets qui ont été intégralement purgés pour revenir au dialogue VO.
2. **Calibrage des menus à choix multiples (`[1208]`) :**
   - En conformité avec le système Atlus PSP, les options de menus nécessitent un alignement d'offset absolu (`_align_menu_text`). Les libellés d'options ont été calibrés au caractère près pour préserver la réactivité du pointeur de sélection en jeu.
3. **Restauration des opcodes critiques :**
   - Restauration des balises de temporisation et de pagination (`[1205]`, `[000E]`, `[000A]`) qui avaient disparu lors de relectures antérieures, empêchant de futurs softlocks ou blocages de fenêtres.
4. **Élagage stylistique et naturel du français :**
   - Reformulation de répliques trop verbeuses, suppression des anglicismes lourds (« *that's rich!* » $\rightarrow$ « *Elle est bonne !* », « *deadbeat* » $\rightarrow$ « *vaurien* ») et réajustement des phrases pour offrir un doublage texte percutant, fluide et fidèle aux personnalités des protagonistes.

---

## 2. Table Complète des Modifications (Avant / Après)

Le tableau ci-dessous recense chronologiquement par script l'ensemble des répliques ajustées.

### 🔹 `script_000.json` — ID 17 | **Proviseur Hanya**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 180 octets)*

```diff
- Ah, j'aurais dû m'en douter...[1205][001E]
- Tu es ce fameux [1113] [1112]
- dont tout le monde parle.
+ J'aurais dû m'en douter...[1205][001E]
+ Tu es ce [1113] [1112]
+ des rumeurs.
```

### 🔹 `script_002.json` — ID 29 | **Eikichi**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 172 octets)*

```diff
- C'est pas Calbute ! Je m'appelle Eikichi
- Mishina ! EIKICHI ! MISHINAAAAA !
+ Pas Calbute ! Je m'appelle Eikichi
+ Mishina ! EIKICHI ! MISHINAAAAA !
```

### 🔹 `script_003.json` — ID 8 | **Philémon**
- **Catégorie :** Correction / Réécriture fidèle *(Budget alloué : 260 octets)*

```diff
- Je vous ai convoqués ici pour vous
- dire ceci.[1205][001E] Allez maintenant, et avec
- vos Personas, affronte ce destin.
+ Je vous ai convoqués ici pour vous
+ dire ceci.[1205][001E] Allez maintenant, et avec
+ vos Personae, affrontez ce destin.
```

### 🔹 `script_004.json` — ID 28 | **Joker**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 196 octets)*

```diff
- Ça fait un bail, [1113] [1112]...[1205][001E] J'ai attendu...[1205][001E] J'ai
- attendu le moment de vous revoir, tous.
+ Ça fait un bail, [1113] [1112]...[1205][001E]
+ J'attendais...[1205][001E] le moment où vous
+ m'invoqueriez tous !
```

### 🔹 `script_005.json` — ID 44 | **Lisa**
- **Catégorie :** Correction / Réécriture fidèle *(Budget alloué : 260 octets)*

```diff
- Si les rumeurs se réalisent, ça
- vaut la peine d'essayer...[1205][001E] N'avoir
- que nos Personas ne suffira pas.
+ Si les rumeurs se réalisent, ça
+ vaut la peine d'essayer...[1205][001E] Mais compter sur le fait
+ que nos Personae ne suffira pas.
```

### 🔹 `script_006.json` — ID 1 | **Lycéen**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 176 octets)*

```diff
- Exactement ! La grande horloge de la
- tour s'est soudainement mise en marche !
+ Et comment ! La grande horloge de la
+ tour s'est soudain mise en marche !
```

### 🔹 `script_007.json` — ID 16 | **Lisa**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 230 octets)*

```diff
- Vite, allons trouver le proviseur
- Hanya ! On doit lever la malédiction
- avant que mon visage ne change encore !
+ Vite, trouvons Hanya ! Il faut lever
+ la malédiction avant que nos visages
+ ne soient défigurés !
```

### 🔹 `script_009.json` — ID 37 | **Maya**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 182 octets)*

```diff
- *regaaaaaarde*[1205][001E] Mais bon, à part ça,
- [1205][000F][1113]-kun...[1205][001E] On s'est déjà vus quelque part?
+ *regard fixe*[1205][001E] Mais à part ça,
+ [1113]-kun...[1205][001E] On s'est déjà vus quelque part ?
```

### 🔹 `script_010.json` — ID 36 | **Mme Saeko**
- **Catégorie :** Correction / Réécriture fidèle *(Budget alloué : 268 octets)*

```diff
- Ce vieux chauv--[1205][001E] je veux dire...[1205][001E] 
- Tu aimes aussi Hanya, pas [1113]vrai?
+ Ce vieux chauv--[1205][001E] je veux dire...[1205][001E]
+ Tu aimes aussi Hanya, pas vrai, [1113] ?
```

### 🔹 `script_011.json` — ID 20 | **Concierge**
- **Catégorie :** Nettoyage accident d'édition (texte parasite collé) *(Budget alloué : 210 octets)*

```diff
- La clé... La clé... Je la vois souvent...
- Tant pis, je vais dîner. Poster de l'actrice
- Saiyuri Yoshikawa. Ses lèvres sont usées
- sans raison... Calendrier de l'actrice
- Saiyuri Yoshikawa... d'il y a 30 ans! Ses
- lèvres sont usées... Cordes et bougies dans
- la boîte... Pour les urgences... Vieille TV.
- Elle a même un bouton pour les chaînes.
- Cachées parmi les photos de Saiyuri dans le
- tiroir...< des coupures de la même actrice.
- Le frigo est plein de plats sous film
- plastique. Rien dans le placard. Il y a des
- futons au fond.
+ La clé... la clé... Elle traîne toujours
+ par ici... Bon, je vais dîner.
```

### 🔹 `script_012.json` — ID 4 | **Fantôme du prof**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 66 octets)*

```diff
- ...pas être...
+ ...ne pas...
```

### 🔹 `script_012.json` — ID 5 | **Eikichi**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 40 octets)*

```diff
- ... Huh?
+ ...Euh?
```

### 🔹 `script_012.json` — ID 6 | **Fantôme du prof**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 316 octets)*

```diff
- J'ai dit...[1205][001E] [1205][001E] que le temps...[1205][001E] doit rester
- figé...[1205][001E] Je le disais... [E1][E2]
- [E3][E4][NULL][NULL]"Maya Il a
- disparu![1205][001E] J'ai l'impression... que je l'ai...
+ J'ai dit...[1205][001E] le temps...[1205][001E] ne doit pas
+ être libéré...[1205][001E] Je l'ai tant dit...[E1][E2][E3][E4][NULL][NULL]"Maya
+ Disparu ![1205][001E] Mais... j'ai l'impression...
```

### 🔹 `script_012.json` — ID 23 | **Joker**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 202 octets)*

```diff
- Les Pléiades ont libéré le temps... [E1][E2]
- [E3][E4][NULL][NULL]"Joker
- La vengeance n'est pas mon seul mobile.
+ Les Pléiades libèrent le temps...[E1][E2][E3][E4][NULL][NULL]"Joker
+ Pas seulement par vengeance.
```

### 🔹 `script_012.json` — ID 24 | **Joker**
- **Catégorie :** Correction / Réécriture fidèle *(Budget alloué : 202 octets)*

```diff
- C'est entre moi, le Donneur, et toi, le
- Voleur...[1205][001E] Un combat contre [1113][1112] pour mon rêve!
+ C'est entre moi, le Donneur, et toi, le
+ Voleur...[1205][001E]
+ Un combat contre [1113] [1112] pour mon rêve !
```

### 🔹 `script_014.json` — ID 7 | **Yukino**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 196 octets)*

```diff
- Ne fais pas ça. Jouer un rôle n'est pas
- cool.[E1][E2] [E3][E4][NULL][NULL]"Anna ... T'es qui toi?
+ Arrête ça. Jouer un rôle n'a rien
+ de cool.
+ [E1][E2]
+ [E3][E4][NULL][NULL]"Anna
+ ...T'es qui ?
```

### 🔹 `script_019.json` — ID 23 | **Ginko**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 266 octets)*

```diff
- Bon, on a notre coupable. Prochaine étape,
- le président du conseil étudiant de Lycée
- Kasu ! Je vais lui régler son compte !
+ Voilà notre coupable ! Prochaine étape,
+ le président des élèves de Kasu !
+ Je vais lui régler son compte !
```

### 🔹 `script_022.json` — ID 7 | **Ginko**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 176 octets)*

```diff
- Aill...[1205][000F] [001E]. euh... Quoi!? T'as intérêt à
- te tenir responsable pour ça, abruti!
+ Aïe...[1205][000F] yaah...[1205][001E] Et maintenant !? Tu as
+ intérêt à assumer ça, abruti !
```

### 🔹 `script_022.json` — ID 29 | **Maya**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 94 octets)*

```diff
- Bonne nuit, [1113]-kun...[1205][001E] Fais de beaux rêves...
+ Bonne nuit, [1113]-kun...[1205][001E]
+ Dors bien...
```

### 🔹 `script_023.json` — ID 3 | **Gamin**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 140 octets)*

```diff
- C'est le trésor que Papa ma[1205][001E]
- donné. [001E]Tu peux le [1113]prendre.
+ C'est le trésor que Papa m'a[1205][001E]
+ donné. Prends-le, [1113].
```

### 🔹 `script_023.json` — ID 5 | **Gamin**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 176 octets)*

```diff
- C'est pas...[1205][001E] ton trésor? J'croyais que ton
- père te l'avait donné... Tu peux pas...
+ C'est pas...[1205][001E] ton trésor ? Ton père
+ te l'a donné... Tu ne peux pas...
```

### 🔹 `script_023.json` — ID 6 | **Gamin**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 106 octets)*

```diff
- Ok... je comprends. C'est a moi maintenant!
+ Compris ! C'est mon trésor maintenant !
```

### 🔹 `script_024.json` — ID 40 | **Maya**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 172 octets)*

```diff
- ...Enfin, non ! Oooh, t'es
- fort... Je suis tombée dans le
- panneau. Essaie de te rappeler !
+ ...Euh non ! Bien joué...
+ Je me suis fait avoir. Souviens-toi !
```

### 🔹 `script_025.json` — ID 5 | **Anna**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 50 octets)*

```diff
- ... Quel abruti.
+ ...Quel idiot.
```

### 🔹 `script_026.json` — ID 24 | **Yasuo**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 284 octets)*

```diff
- Je déteste la violence...[1205][001E]Mais je suppose que je n'ai plus le choix.
- Tu mourras en regrettant de t'être mêlé de
- ça ! Gueueueueueue !
+ Je hais la violence...[1205][001E] Mais je suppose que
+ je n'ai plus le choix. Tu vas regretter de
+ t'être mêlé de ça ! Hihihaha !
```

### 🔹 `script_027.json` — ID 6 | **Eikichi & Ginko**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 86 octets)*

```diff
- [1432][NULL][NULL][0014]Le cercle masqué[1432][NULL][NULL][0014]
+ [1432][NULL][NULL][0014]Cercle masqué[1432][NULL][NULL][0014]?
```

### 🔹 `script_027.json` — ID 17 | **Dame Scorpion**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 112 octets)*

```diff
- ... Yukino Mayuzumi? T'es toujours là.
+ ...Yukino Mayuzumi ? Toujours là.
```

### 🔹 `script_027.json` — ID 20 | **Dame Scorpion**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 66 octets)*

```diff
- ... C'est tout?
+ ...C'est tout?
```

### 🔹 `script_027.json` — ID 26 | **Roi Lion**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 236 octets)*

```diff
- On me nomme Roi Lion! Je suis le plus
- puissant des 4 dirigents du Cercle
- Masqué porteur du signe du Lion.
+ On m'appelle Roi Lion ! Je suis le plus
+ puissant des 4 chefs du Cercle masqué,
+ porteur du signe du Lion.
```

### 🔹 `script_027.json` — ID 29 | **Dame Scorpion**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 106 octets)*

```diff
- ... Yukino m'appartient. Laisse la.
+ ...Yukino m'appartient. Laisse-la.
```

### 🔹 `script_027.json` — ID 32 | **Roi Lion**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 236 octets)*

```diff
- Étoile maudite...[1205][001E] Toi et la sorcière
- envoyée au purgatoire finirez comme
- le misérable de tout à l'heure.
+ Étoile maudite...[1205][001E] La sorcière et toi finirez
+ au Purgatoire, comme ce misérable.
```

### 🔹 `script_028.json` — ID 26 | **Gérant**
- **Catégorie :** Nettoyage accident d'édition (texte parasite collé) *(Budget alloué : 276 octets)*

```diff
- Techniquement on est ouverts aujourd'hui,
- mais on est fermés pour un tournage de clip.
- Et avec tous ces clients... Machine #1 de la
- rangée des bornes Wild 9.[E1][E2] [E3][E4][NULL][NULL]"Manager Oh
- désolé, monsieur! Vous ne pouvez pas jouer
- maintenant.C'est un peu chaotique en ce
- moment. Machine #2 de la rangée des bornes
- Wild 9.
+ Techniquement on est ouverts aujourd'hui,
+ mais fermés pour le tournage d'un clip.
+ Et avec tous ces clients...
```

### 🔹 `script_028.json` — ID 27 | **Gérant**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 222 octets)*

```diff
- Oh désolé, monsieur ! Vous ne pouvez pas
- jouer maintenant. C'est un peu chaotique en
- ce moment.[E1][E2][E3] Machine #3 de la rangée des
- bornes Wild 9.
+ Oh, désolé, monsieur ! Vous ne pouvez pas
+ jouer actuellement. C'est un peu
+ chaotique en ce moment.
```

### 🔹 `script_028.json` — ID 28 | **Gérant**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 222 octets)*

```diff
- Oh désolé, monsieur! Vous ne pouvez pas
- jouer maintenant. C'est un peu chaotique en
- ce moment. Machine #3 de la rangée des
- bornes Wild 9.
+ Oh, désolé, monsieur ! Vous ne pouvez pas
+ jouer actuellement. C'est un peu
+ chaotique en ce moment.
```

### 🔹 `script_028.json` — ID 29 | **Gérant**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 222 octets)*

```diff
- Oh désolé, monsieur! Vous ne pouvez pas
- jouer maintenant. C'est un peu chaotique en
- ce moment. Machine #4 de la rangée des
- bornes Wild 9.
+ Oh, désolé, monsieur ! Vous ne pouvez pas
+ jouer actuellement. C'est un peu
+ chaotique en ce moment.
```

### 🔹 `script_028.json` — ID 30 | **Gérant**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 222 octets)*

```diff
- Oh désolé, monsieur! Vous ne pouvez pas
- jouer maintenant. C'est un peu chaotique en
- ce moment. Machine #5 de la rangée des
- bornes Wild 9.
+ Oh, désolé, monsieur ! Vous ne pouvez pas
+ jouer actuellement. C'est un peu
+ chaotique en ce moment.
```

### 🔹 `script_028.json` — ID 31 | **Gérant**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 222 octets)*

```diff
- Oh désolé, monsieur! Vous ne pouvez pas
- jouer maintenant. C'est un peu chaotique en
- ce moment. Machine #6 de la rangée des
- bornes Wild 9.
+ Oh, désolé, monsieur ! Vous ne pouvez pas
+ jouer actuellement. C'est un peu
+ chaotique en ce moment.
```

### 🔹 `script_028.json` — ID 32 | **Gérant**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 222 octets)*

```diff
- Oh désolé, monsieur! Vous ne pouvez pas
- jouer maintenant. C'est un peu chaotique en
- ce moment. Machine #7 de la rangée des
- bornes Wild 9.
+ Oh, désolé, monsieur ! Vous ne pouvez pas
+ jouer actuellement. C'est un peu
+ chaotique en ce moment.
```

### 🔹 `script_028.json` — ID 33 | **Gérant**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 222 octets)*

```diff
- Oh désolé, monsieur! Vous ne pouvez pas
- jouer maintenant. C'est un peu chaotique en
- ce moment. Machine #8 de la rangée des
- bornes Wild 9.
+ Oh, désolé, monsieur ! Vous ne pouvez pas
+ jouer actuellement. C'est un peu
+ chaotique en ce moment.
```

### 🔹 `script_028.json` — ID 34 | **Gérant**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 222 octets)*

```diff
- Oh désolé, monsieur! Vous ne pouvez pas
- jouer maintenant. C'est un peu chaotique en
- ce moment. Machine #9 de la rangée des
- bornes Wild 9.
+ Oh, désolé, monsieur ! Vous ne pouvez pas
+ jouer actuellement. C'est un peu
+ chaotique en ce moment.
```

### 🔹 `script_028.json` — ID 35 | **Gérant**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 222 octets)*

```diff
- Oh désolé, monsieur! Vous ne pouvez pas
- jouer maintenant. C'est un peu chaotique en
- ce moment. Machine #10 de la rangée des
- bornes Wild 9.
+ Oh, désolé, monsieur ! Vous ne pouvez pas
+ jouer actuellement. C'est un peu
+ chaotique en ce moment.
```

### 🔹 `script_028.json` — ID 36 | **Gérant**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 222 octets)*

```diff
- Oh désolé, monsieur! Vous ne pouvez pas
- jouer maintenant. C'est un peu chaotique en
- ce moment. Machine de blackjack [NULL][NULL]Unissons nos
- Forces[NULL][NULL].
+ Oh, désolé, monsieur ! Vous ne pouvez pas
+ jouer actuellement. C'est un peu
+ chaotique en ce moment.
```

### 🔹 `script_028.json` — ID 37 | **Gérant**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 222 octets)*

```diff
- Oh désolé, monsieur! Vous ne pouvez pas
- jouer maintenant. C'est un peu chaotique en
- ce moment. Machine #1 de la rangée des
- machines Arouse Blank.
+ Oh, désolé, monsieur ! Vous ne pouvez pas
+ jouer actuellement. C'est un peu
+ chaotique en ce moment.
```

### 🔹 `script_028.json` — ID 38 | **Gérant**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 222 octets)*

```diff
- Oh désolé, monsieur! Vous ne pouvez pas
- jouer maintenant. C'est un peu chaotique en
- ce moment. Machine #2 de la rangée des
- machines Arouse Blank.
+ Oh, désolé, monsieur ! Vous ne pouvez pas
+ jouer actuellement. C'est un peu
+ chaotique en ce moment.
```

### 🔹 `script_028.json` — ID 39 | **Gérant**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 222 octets)*

```diff
- Oh désolé, monsieur! Vous ne pouvez pas
- jouer maintenant. C'est un peu chaotique en
- ce moment. Machine #3 de la rangée des
- machines Arouse Blank.
+ Oh, désolé, monsieur ! Vous ne pouvez pas
+ jouer actuellement. C'est un peu
+ chaotique en ce moment.
```

### 🔹 `script_028.json` — ID 40 | **Gérant**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 222 octets)*

```diff
- Oh désolé, monsieur! Vous ne pouvez pas
- jouer maintenant. C'est un peu chaotique en
- ce moment. Machine #4 de la rangée des
- machines Arouse Blank.
+ Oh, désolé, monsieur ! Vous ne pouvez pas
+ jouer actuellement. C'est un peu
+ chaotique en ce moment.
```

### 🔹 `script_028.json` — ID 41 | **Gérant**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 222 octets)*

```diff
- Oh désolé, monsieur! Vous ne pouvez pas
- jouer maintenant. C'est un peu chaotique en
- ce moment. Machine #5 de la rangée des
- machines Arouse Blank.
+ Oh, désolé, monsieur ! Vous ne pouvez pas
+ jouer actuellement. C'est un peu
+ chaotique en ce moment.
```

### 🔹 `script_028.json` — ID 42 | **Gérant**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 222 octets)*

```diff
- Oh désolé, monsieur! Vous ne pouvez pas
- jouer maintenant. C'est un peu chaotique en
- ce moment. Machine #6 de la rangée des
- machines Arouse Blank.
+ Oh, désolé, monsieur ! Vous ne pouvez pas
+ jouer actuellement. C'est un peu
+ chaotique en ce moment.
```

### 🔹 `script_028.json` — ID 43 | **Gérant**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 222 octets)*

```diff
- Oh désolé, monsieur! Vous ne pouvez pas
- jouer maintenant. C'est un peu chaotique en
- ce moment. Machine #7 de la rangée des
- machines Arouse Blank.
+ Oh, désolé, monsieur ! Vous ne pouvez pas
+ jouer actuellement. C'est un peu
+ chaotique en ce moment.
```

### 🔹 `script_028.json` — ID 44 | **Gérant**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 222 octets)*

```diff
- Oh désolé, monsieur! Vous ne pouvez pas
- jouer maintenant. C'est un peu chaotique en
- ce moment. Machine #8 de la rangée des
- machines Arouse Blank.
+ Oh, désolé, monsieur ! Vous ne pouvez pas
+ jouer actuellement. C'est un peu
+ chaotique en ce moment.
```

### 🔹 `script_028.json` — ID 45 | **Gérant**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 222 octets)*

```diff
- Oh désolé, monsieur! Vous ne pouvez pas
- jouer maintenant. C'est un peu chaotique
- en ce moment. Jeu de bingo [NULL][NULL]Fortune's Reel[NULL][NULL].
+ Oh, désolé, monsieur ! Vous ne pouvez pas
+ jouer actuellement. C'est un peu
+ chaotique en ce moment.
```

### 🔹 `script_028.json` — ID 46 | **Gérant**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 222 octets)*

```diff
- Oh, désolé, monsieur ! Vous ne pouvez
- pas jouer là pour l'instant. Désolé,
- c'est un peu la panique en ce moment.
+ Oh, désolé, monsieur ! Vous ne pouvez pas
+ jouer actuellement. C'est un peu
+ chaotique en ce moment.
```

### 🔹 `script_030.json` — ID 2 | **???**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 232 octets)*

```diff
- Ahahah...[1205][001E] Là tu m'as eu. Ouais, c'est
- le moment. Il semblerait que notre
- dernière invitée vient d'arriver.
+ Ahahah...[1205][001E] Bien vu. Ouais, c'est
+ le moment. On dirait bien que notre
+ dernière invitée vient d'arriver.
```

### 🔹 `script_030.json` — ID 15 | **Eikichi**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 38 octets)*

```diff
- .. Moi?
+ ...Moi
```

### 🔹 `script_030.json` — ID 21 | **Ginji**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 252 octets)*

```diff
- Elle est basée sur le [1432][NULL][NULL][0014]jeu Joker[1432][NULL][NULL][0014]
- qui fait fureur chez les jeunes. La
- chanson s'appelle, du coup, [1432][NULL][NULL][0014]Joker[1432][NULL][NULL][0014]!
+ Inspirée du [1432][NULL][NULL][0014]jeu Joker[1432][NULL][NULL][0014] qui fait
+ fureur chez les jeunes. Elle s'intitule,
+ bien sûr, [1432][NULL][NULL][0014]Joker[1432][NULL][NULL][0014] !
```

### 🔹 `script_031.json` — ID 6 | **Maya**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 180 octets)*

```diff
- Tu as raison. On s'en tiens au plan
- de Yukki! [1113][U+113], nous feras-tu l'honneur?
+ Tu as raison. On s'en tient au plan
+ de Yukki ! [1113], nous feras-tu l'honneur ?
```

### 🔹 `script_031.json` — ID 17 | **Personnel**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 292 octets)*

```diff
- Euh...? Tu veux récupérer nos tâches? Tu
- veux voir le concert mais tu n'as pas pu
- avoir de tickets? Quelle drôle de
- coincidence...
+ Euh...? Tu veux prendre notre service ?
+ Tu veux voir le show sans tickets ?
+ Drôle de coïncidence...
```

### 🔹 `script_031.json` — ID 18 | **Personnel**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 206 octets)*

```diff
- Bonjour les ennuis si ils s'en aperçoivent,
- mais... J'ai vraiment pas envie d'être
- ici...
+ Gros soucis s'ils le découvrent,
+ mais... je n'ai vraiment pas envie
+ d'être ici...
```

### 🔹 `script_031.json` — ID 25 | **Personnel**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 128 octets)*

```diff
- Hé, seul le personnel est
- autorisé à passer par là.
+ Seul le personnel est
+ autorisé à passer par là.
```

### 🔹 `script_033.json` — ID 0 | **Voix de Ginji**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 282 octets)*

```diff
- Ahaha... Mes jolis papillons...[1205][001E] L'énergie de vos idéaux va concrétiser
- les rêves du Cercle Masqué...
+ Ahaha... Mes chers papillons...[1205][001E] L'énergie de vos idéaux va nourrir
+ les rêves du Cercle Masqué...
```

### 🔹 `script_033.json` — ID 2 | **Mami[1121]& Miho**
- **Catégorie :** Correction / Réécriture fidèle *(Budget alloué : 310 octets)*

```diff
- Gloire au Masque... [E1][E2]
- [E3][E4][NULL][NULL]"Prince Taureau
- Ginji Sasaki...[1205][001E] ou plutôt Prince
- Taureau,vous présente un nouveau membre.
+ Gloire au Masque...
+ [E1][E2]
+ [E3][E4][NULL][NULL]"Prince Taureau
+ Ginji Sasaki...[1205][001E] ou plutôt Prince
+ Taureau, vous présente un nouveau membre.
```

### 🔹 `script_033.json` — ID 9 | **Ginko**
- **Catégorie :** Correction / Réécriture fidèle *(Budget alloué : 248 octets)*

```diff
- [1113]et les autres sont aussi mes amis...
- Je peux pas les trahir![1205][001E] Et je
- refuse de vivre un rêve d'emprunt!
+ [1113] et les autres sont aussi mes amis...
+ Je peux pas les trahir ![1205][001E] Et je
+ refuse de vivre un rêve d'emprunt !
```

### 🔹 `script_033.json` — ID 11 | **Prince Taureau**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 482 octets)*

```diff
- Hah... On dirait que je me suis fait avoir.[1205][001E]Peu importe. SPADE, sur scène.[1205][001E]Vous chanterez une chanson étrangère...
- [1432][NULL][NULL][0014]Joker.[1432][NULL][NULL][0014] [E1][E2] [E3][E4][NULL][NULL]Prince Taurus Maintenant...[1205][001E]Un papillon qui refuse de s'envoler doit
- être épinglé et exposé !
+ Hah... Je me suis fait avoir.[1205][001E]
+ Peu importe. SPADE, en scène.[1205][001E]
+ Chantez l'air étranger...
+ [1432][NULL][NULL][0014]Joker.[1432][NULL][NULL][0014]
+ [E1][E2]
+ [E3][E4][NULL][NULL]"Prince Taureau
+ Maintenant...[1205][001E] Un papillon refusant de
+ s'envoler doit être épinglé !
```

### 🔹 `script_034.json` — ID 0 | **Roi Lion**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 312 octets)*

```diff
- Il semble que les choses ont dérapé,
- Taurus.[1205][001E] C'est bien l'Étoile Maudite
- prédite par les cieux...[1205][001E] Tu ne
- devrais pas les prendre dehaut.
+ Il semble que les choses ont dérapé,
+ Taureau.[1205][001E] C'est bien l'Étoile Maudite
+ prédite par les cieux...[1205][001E] Ne les prends
+ pas de trop haut.
```

### 🔹 `script_034.json` — ID 1 | **Prince Taureau**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 490 octets)*

```diff
- Ngh...[1205][001E]La [1432][NULL][NULL][0014]chanson étrangère[1432][NULL][NULL][0014] s'est finie...[1205][001E]Ma tâche va finir.[E1][E2] [E3][E4][NULL][NULL]"Prince Taureau Le crâne
- de cristal de la Terre sera bientôt plein...[1205][001E]Je m'assurerai que tout soit prêtpour la Fin
- de Nahui-Ollin...
+ Ngh...[1205][001E] La [1432][NULL][NULL][0014]chanson étrangère[1432][NULL][NULL][0014] a fini...[1205][001E]
+ Ma tâche va s'achever.
+ [E1][E2]
+ [E3][E4][NULL][NULL]"Prince Taureau
+ Le crâne de cristal sera bientôt plein...[1205][001E]
+ Tout sera prêt pour la Fin de Nahui-Ollin...
```

### 🔹 `script_034.json` — ID 3 | **Roi Lion**
- **Catégorie :** Correction / Réécriture fidèle *(Budget alloué : 182 octets)*

```diff
- Quitte ces lieux, Taurus. Si tu
- meurs maintenant, tu gêneras le plan.
+ Quitte ces lieux, Taureau. Si tu
+ meurs maintenant, tu gêneras le plan.
```

### 🔹 `script_034.json` — ID 7 | **Roi Lion**
- **Catégorie :** Correction / Réécriture fidèle *(Budget alloué : 220 octets)*

```diff
- C'est à moi que tu as affaire...[1205][001E] Je pourrais te tuer, mais
- pourquoi ne pas jouer un peu...?
+ C'est à moi que tu as affaire...[1205][001E]
+ Je pourrais te briser, mais si
+ on jouait plutôt à un jeu... ?
```

### 🔹 `script_034.json` — ID 9 | **Roi Lion**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 278 octets)*

```diff
- Hahaha! L'un d'eux est ici...[1205][001E]Fouillez cette salle pour trouver la
- cible...[1205][001E]Quelque part ici, vous trouverez une énigme!
+ Hahaha ! L'un d'eux est ici...[1205][001E]
+ Fouillez la salle pour la cible...[1205][001E]
+ Vous trouverez une charmante énigme !
```

### 🔹 `script_035.json` — ID 0 | **Prince Taureau**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 256 octets)*

```diff
- Tch... Quelle interférence inutile...[1205][001E]
- Bon, maintenant tu sais, Lisa-kun.
- Dans le peu de temps qu'il reste, dansons !
+ Tch... Vaine interférence...[1205][001E] Te voilà au
+ courant, Lisa-kun. Dansons dans le peu
+ de temps qu'il reste !
```

### 🔹 `script_036.json` — ID 2 | **Eikichi**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 172 octets)*

```diff
- Inutile de retourner sur scène maintenant.
- Dépêchons-nous de trouver Ginko !
+ Inutile de retourner sur scène.
+ Vite, allons trouver Ginko !
```

### 🔹 `script_037.json` — ID 6 | **Maya**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 224 octets)*

```diff
- Les rêves ne sont pas une béquille
- qu'on peut s'accorder ou un cadeau qu'on
- reçoit. Lisa finira par comprendre.
+ Un rêve n'est pas une béquille ni
+ un cadeau tout fait. Lisa finira par
+ le comprendre.
```

### 🔹 `script_039.json` — ID 13 | **Ginji**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 246 octets)*

```diff
- La journaliste, la photographe...[1205][001E] Même ce chef de gang a un rêve.
- Pourtant, tu n'en as aucun à toi.
+ La journaliste, la photographe...[1205][001E]
+ Même ce chef de gang a un rêve.
+ Mais toi, tu n'en as aucun à toi.
```

### 🔹 `script_041.json` — ID 8 | **Personnel**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 470 octets)*

```diff
- On est sensé être gardiens à l'interieur du
- hall, donc tu peux pas sortir ici. [NULL][NULL]"Personel
- du concert Ce travail est dûr. On se met sur
- la ligne pour retenir les foules. T'as
- interêt à être prêt.[E1][E2][E3][E4]
+ On doit garder l'intérieur du hall,
+ tu ne peux pas sortir dehors.
+ [E1][E2]
+ [E3][E4][NULL][NULL]"Personnel
+ Ce travail est dur. On fait face à
+ la foule en délire. T'as intérêt à être prêt.
```

### 🔹 `script_042.json` — ID 21 | **Prince Taureau**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 256 octets)*

```diff
- Tch... Quelle interférence inutile...[1205][001E]
- Bon, maintenant tu sais, Lisa-kun.
- Dans le peu de temps qu'il reste, dansons !
+ Tch... Vaine interférence...[1205][001E] Te voilà au
+ courant, Lisa-kun. Dansons dans le peu
+ de temps qu'il reste !
```

### 🔹 `script_044.json` — ID 12 | **Eikichi**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 116 octets)*

```diff
- C'est quoi ce bazar? Où
- veut en venir ce truc?
+ C'est quoi ce délire ?
+ Où ça veut en venir ?
```

### 🔹 `script_044.json` — ID 13 | **Mme Idéale**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 532 octets)*

```diff
- La [1432][NULL][NULL][0014]chanson étrangere[1432][NULL][NULL][0014]... Les [1432][NULL][NULL][0014]flammes de
- l'expiation[1432][NULL][NULL][0014]...[1205][001E]C'est sûrement l'Oracle de Maia! M-Mais
- qui...!? [E1][E2] [E3][E4][NULL][NULL]"Maya Excusez-moi... Vous êtes Mme
- Okamura de Seven, n'est-ce pas? Je suis Maya
- Amano, de la redaction deCoolest.
+ La [1432][NULL][NULL][0014]chanson étrangère[1432][NULL][NULL][0014]... Les [1432][NULL][NULL][0014]flammes de
+ l'expiation[1432][NULL][NULL][0014]...[1205][001E] L'Oracle de Maia !
+ M-Mais qui... !?
+ [E1][E2]
+ [E3][E4][NULL][NULL]"Maya
+ Excusez-moi... Vous êtes Mme Okamura de
+ Seven ? Je suis Maya Amano, de Coolest.
```

### 🔹 `script_044.json` — ID 14 | **Maya**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 236 octets)*

```diff
- Vous avez parlé de l'Oracle de
- Maia...[1205][001E] Vous en savez quelque chose?
- Si ça ne vous dit rien, j'aimerais--
+ Vous avez parlé de l'Oracle
+ de Maia...[1205][001E] Vous en savez quelque chose ?
+ Si possible, j'aimerais--
```

### 🔹 `script_045.json` — ID 11 | **Ginko**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 118 octets)*

```diff
- Les Pléiades... Une seconde!
- Ça veut dire Seven...?
+ Pléiades... Attends !
+ Ça veut dire Seven... ?
```

### 🔹 `script_045.json` — ID 24 | **Yukino**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 126 octets)*

```diff
- Mais on n'a pas de temps à
- perdre ! Allons-y, [1113], Maya-san !
+ Pas de temps à perdre ! En route,
+ [1113], Maya-san !
```

### 🔹 `script_047.json` — ID 20 | **Yukino**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 182 octets)*

```diff
- On couvre plus de terrain si on se sépare
- pour chercher. Prenons chacun un étage !
+ On couvrira plus de terrain en se séparant.
+ Prenons chacun un étage !
```

### 🔹 `script_051.json` — ID 31 | **Troupe Leo**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 64 octets)*

```diff
- Gloire au Masque!
+ Vive le Masque !
```

### 🔹 `script_051.json` — ID 49 | **Ixquic**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 248 octets)*

```diff
- Je ne laisserai jamais quiconque interférer
- avec le plan de Maître Léo ! Je n'ai plus
- de transmetteur, mais j'ai mon Persona !
+ Pas question d'entraver le plan du
+ Maître Leo ! Je n'ai plus d'émetteur,
+ mais j'ai toujours mon Persona !
```

### 🔹 `script_054.json` — ID 3 | **Maya**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 186 octets)*

```diff
- Il semble qu'Ulala soit là. Je devrais
- passer au ring de boxe pour lui dire
- d'évacuer.
+ On dirait qu'Ulala est là. Je devrais passer
+ au ring pour lui dire d'évacuer.
```

### 🔹 `script_057.json` — ID 0 | **Maya**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 164 octets)*

```diff
- Un haltère!? C'est pas drôle... Je
- serai morte s'il tombait dessus![E4][NULL][NULL]"Maya
- Grazie, ... Je t'en dois une.
+ Un haltère !? C'est pas drôle...
+ Je serais morte s'il tombait sur moi !
```

### 🔹 `script_057.json` — ID 1 | **Maya**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 86 octets)*

```diff
- Oulah! Il y a des bombes! On a pas
- le temps de toutes les désamorcer!
+ Grazie [1113]-kun !
+ Je t'en dois une !
```

### 🔹 `script_058.json` — ID 3 | **Eikichi**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 364 octets)*

```diff
- On dit quoi pour les types comme lui?
- Polaroïd?[E1][E2] [E3][E4][NULL][NULL]"Eikichi Il a détalé en nous
- voyant! C'est louche. Chopons-le, [1113]!
+ Ged?[E1][E2]
+ [E3][E4][NULL][NULL]"Eikichi
+ Il a détalé en nous voyant ! C'est suspect !
```

### 🔹 `script_058.json` — ID 7 | **Yukino**
- **Catégorie :** Nettoyage accident d'édition (texte parasite collé) *(Budget alloué : 256 octets)*

```diff
- S'il est du Cercle masqué, on peut lui tirer
- des infos sur Joker. Traquons-le. Le casier
- contient un mot: [NULL][NULL]stupide[NULL][NULL]... et une [E4][NULL][NULL]bombe[E4][NULL][NULL].[E4][NULL][NULL]
- Juste une [E4][NULL][NULL]bombe[E4][NULL][NULL] dans la poubelle.[E4][NULL][NULL]
+ S'il est du Cercle masqué, profitons-en
+ pour lui tirer des infos sur Joker.
+ Traquons-le !
```

### 🔹 `script_059.json` — ID 1 | **Eikichi**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 162 octets)*

```diff
- ... Oouch! Hé, t'as sauvé Maya quand
- c'est arrivé, pourquoi pas moi!?
+ ...Aïe ! Hé, t'as sauvé Maya-san,
+ alors pourquoi pas moi !?
```

### 🔹 `script_059.json` — ID 2 | **Ginko**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 182 octets)*

```diff
- Aiyah! Regardez ces maillots de bain!
- Si [1113]portait un truc pareil...[1205][001E] Aaaaaa!
+ Aiyah ! Regardez ces maillots !
+ Si [1113] portait un truc pareil...[1205][001E]
+ Aaaaaa !
```

### 🔹 `script_059.json` — ID 10 | **Eikichi**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 162 octets)*

```diff
- ... Oouch! Hé, t'as sauvé Maya quand
- c'est arrivé, pourquoi pas moi!?
+ ...Aïe ! Hé, t'as sauvé Maya-san,
+ alors pourquoi pas moi !?
```

### 🔹 `script_061.json` — ID 0 | **Maya**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 152 octets)*

```diff
- Tu l'as trouvé!? Super! Bien joué,
- [1113]! Maintenant, détruisons-le! Vous
- détruisez le [E4][NULL][NULL]transmetteur[E4][NULL][NULL] dans le casier.[E4][NULL][NULL]
+ Tu l'as trouvé !? Super ! Bien joué,
+ [1113] ! Allez, détruisons-le !
```

### 🔹 `script_064.json` — ID 9 | **Personnel**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 206 octets)*

```diff
- Lisa-chan et les autres sont parties il
- y a un moment. Je crois qu'elles sont
- dans la salle d'attente maintenant.
+ Lisa-chan et les autres sont parties.
+ Elles doivent être en salle d'attente.
```

### 🔹 `script_066.json` — ID 7 | **Yukino**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 152 octets)*

```diff
- Mme Saeko m'a sauvée autrefois, et
- maintenant c'est mon tour de sauver cette
- fille !
+ Mme Saeko m'a sauvée, à mon tour de
+ sauver cette fille !
```

### 🔹 `script_068.json` — ID 17 | **Eikichi**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 124 octets)*

```diff
- On va chercher une corde.
- [1113]garde un œil sur maya
+ On cherche une corde.
+ [1113], surveille Maya !
```

### 🔹 `script_070.json` — ID 12 | **Yukino**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 204 octets)*

```diff
- Pourquoi cette fille était dans
- l'avion en premier lieu ? C'est aussi
- l'œuvre de ce poseur de bombes ?
+ Que faisait cette fille dans l'avion ?
+ Encore un coup de ce poseur de bombes ?
```

### 🔹 `script_071.json` — ID 4 | **Yukino**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 220 octets)*

```diff
- Tu parles d'une situation...
- Bon, on va juste le sortir de
- là. J'ai besoin de ton aide là, [1113][u+1113]!
+ Quelle drôle de situation...
+ Tant pis, tirons-le de là.
+ J'ai besoin de ton aide, [1113] !
```

### 🔹 `script_078.json` — ID 7 | **Tatsuya Sudou**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 284 octets)*

```diff
- Quand la Croix Cosmique se formera,
- l'Enfer s'élèvera vers les cieux...[1205][001E] Notre chance en 15 000 ans est là!
+ Quand la Sainte Croix se formera,
+ l'Enfer montera aux cieux...[1205][001E]
+ Notre chance en 15 000 ans arrive !
```

### 🔹 `script_079.json` — ID 3 | **Maya**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 92 octets)*

```diff
- La salle de contrôle doit être devant.
+ La salle de contrôle est tout droit.
```

### 🔹 `script_080.json` — ID 5 | **Maya**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 94 octets)*

```diff
- C'est parti pour de vrai... Décollage !
+ C'est du sérieux... Décollage !
```

### 🔹 `script_083.json` — ID 2 | **Eikichi**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 182 octets)*

```diff
- H-Vous entendez ça, les gars...? Y-Y a
- rien à-à craindre... C-C'est compris...?
+ V-Vous entendez, les gars... ? Y-Y a
+ rien à craindre... C-Compris... ?
```

### 🔹 `script_083.json` — ID 6 | **Yukino**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 114 octets)*

```diff
- On dirait qu'ils vont bien.
- OK, prochain groupe, allez !
+ Ils ont l'air d'aller bien. Au suivant !
```

### 🔹 `script_084.json` — ID 35 | **Maya**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 236 octets)*

```diff
- J'espère juste que ça marchera...[1205][001E] Bon, on n'a plus rien à faire ici.
- Allons à l'agence de détectives.
+ J'espère que ça marchera...[1205][001E] Bon,
+ on n'a plus rien à faire ici.
+ Allons à l'agence de détectives.
```

### 🔹 `script_085.json` — ID 8 | **Présentateur**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 298 octets)*

```diff
- Une version les dépeint comme de vicieux
- terroristes, l'autre en fait des héros...[1205][001E] Mais laquelle de ces rumeurs est vraie?
+ Une version les dépeint comme de vicieux
+ terroristes, l'autre en fait des héros...[1205][001E]
+ Mais quelle rumeur dit la vérité ?
```

### 🔹 `script_085.json` — ID 32 | **Tamaki**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 488 octets)*

```diff
- Q-Quelle imagination...[1205][001E]Pourquoi le Cercle masqué et le Bataillon
- veulent ce Xibalba? [NULL][NULL]"Mme Idéale Car quand
- l'Oracle sera accompli, Xibalba et les
- crânes de cristal exauceront le rêve de
- l'humanité...[E1][E2][E3][E4]
+ Q-Quelle imagination...[1205][001E]
+ Pourquoi le Cercle et le Bataillon
+ veulent ce Xibalba ?
+ [E1][E2]
+ [E3][E4][NULL][NULL]"Mme Idéale
+ Car quand l'Oracle sera accompli,
+ Xibalba et les crânes réaliseront
+ le rêve ultime de l'humanité...
```

### 🔹 `script_085.json` — ID 149 | **Chef Todoroki**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 110 octets)*

```diff
- Vous n'avez pas les moyens
- pour mes honoraires.
+ Vous n'avez pas de quoi me payer.
```

### 🔹 `script_091.json` — ID 1 | **Philémon**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 278 octets)*

```diff
- Tu commences à te rappeler ton
- passé oublié...[1205][001E] Si tu souhaites
- connaître la vérité, va à la
- caverne Alaya derrière le temple.
+ Tu retrouves la mémoire de ton passé...[1205][001E]
+ Pour connaître la vérité, va à la caverne
+ Alaya derrière ce sanctuaire.
```

### 🔹 `script_092.json` — ID 0 | **Ginko**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 240 octets)*

```diff
- Tu ne te souviens toujours pas? [1205][001E][1113]...
- Tes vacances d'été il y a 10 ans...
- Cette grotte était notre cachette...
+ Tu ne t'en souviens pas ? [1205][001E][1113]...
+ Nos vacances d'été il y a 10 ans...
+ Cette grotte était notre cachette...
```

### 🔹 `script_092.json` — ID 1 | **Eikichi**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 198 octets)*

```diff
- Impossible...[1205][001E] [001E]J'ai vu cet endroit tout ce
- temps dans mes rêves... Il y est toujours...
+ Impossible...[1205][001E] J'ai vu cet endroit tout
+ ce temps dans mes rêves... C'est bien réel...
```

### 🔹 `script_092.json` — ID 7 | **Eikichi**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 128 octets)*

```diff
- [1113]...[1205][001E] Je, euh... Je ne veux
- vraiment pas y aller...[1205][001E] 
+ [1113]...[1205][001E] J-Je... Je ne veux pas
+ continuer...[1205][001E]
```

### 🔹 `script_092.json` — ID 9 | **Maya**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 134 octets)*

```diff
- Eh...[1205][001E] Quelle ironie. C'est
- comme si je voyais mon reflet.
+ Heh...[1205][001E] Quelle ironie.
+ Comme face à un miroir.
```

### 🔹 `script_101.json` — ID 4 | **Garçon masqué**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 306 octets)*

```diff
- Papa et Maman se disputaient encore...[1205][001E] Ils avaient promis de venir au festival
- avec moi.[1205][001E] Pourquoi ils s'énervent autant?
+ Papa et Maman se disputaient encore...[1205][001E]
+ Ils avaient promis de venir au festival
+ avec moi.[1205][001E] Pourquoi ils s'énervent tant ?
```

### 🔹 `script_101.json` — ID 29 | **Garçon masqué**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 204 octets)*

```diff
- Hmm...[1205]< Le Cercle Masqué ! Désormais,
- répandons les rumeurs pour les
- faire revenir à la réalité.
+ Hmm...[1205]< Le Cercle Masqué ! Désormais,
+ nous formons le Cercle Masqué !
```

### 🔹 `script_102.json` — ID 5 | **Yukino**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 82 octets)*

```diff
- Non...[1205][001E] Comment est-ce possible...?
+ Non...[1205][001E] Comment... ?
```

### 🔹 `script_107.json` — ID 12 | **Lycéenne**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 132 octets)*

```diff
- Ça s'appelle le Jeu du Persona,
- et... c'est difficile à expliquer.
+ Ça s'appelle le jeu Persona, et...
```

### 🔹 `script_110.json` — ID 11 | **Ginko**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 90 octets)*

```diff
- Arrêtez...[1205][001E] Je vous en supplie, arrêtez...!
+ Non...[1205][001E] Pitié, arrêtez... !
```

### 🔹 `script_111.json` — ID 43 | **Joker**
- **Catégorie :** Correction / Réécriture fidèle *(Budget alloué : 120 octets)*

```diff
- Arrête...[1205][001E] C'est impossible...[1205][001E] [1113]t'a tuée...!
+ Arrête...[1205][001E] C'est impossible...[1205][001E]
+ [1113] t'a tuée... !
```

### 🔹 `script_111.json` — ID 45 | **Joker**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 68 octets)*

```diff
- TUEZ-LA ! TUEZ-LA MAINTENANT !
+ TUEZ-LA ! VITE !
```

### 🔹 `script_112.json` — ID 1 | **Maya**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 142 octets)*

```diff
- J'ai vu la source en venant...[1205][001E] Je me suis souvenue de tout.
+ J'ai vu la source en venant...[1205][001E]
+ Je me suis souvenue de tout.
```

### 🔹 `script_112.json` — ID 6 | **Eikichi**
- **Catégorie :** Correction / Réécriture fidèle *(Budget alloué : 200 octets)*

```diff
- Je...[1205][001E] J'ai fait quelque chose de terrible...[1205][001E] Je comprendrais si tu m'en voulais...
+ Je...[1205][001E]
+ J'ai fait quelque chose d'horrible...[1205][001E]
+ Je comprendrais que tu m'en veuilles...
```

### 🔹 `script_112.json` — ID 9 | **Fille fantôme**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 48 octets)*

```diff
- ......
+ .....
```

### 🔹 `script_112.json` — ID 13 | **Maya illusoire**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 216 octets)*

```diff
- Jun-kun souffre aussi de faux souvenirs...[1205][001E] Je... n'ai pu que le voir changer...
+ Jun-kun souffre aussi de faux souvenirs...[1205][001E]
+ Je n'ai pu que le voir changer...
```

### 🔹 `script_112.json` — ID 15 | **Maya illusoire**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 92 octets)*

```diff
- Grazie...[1205][001E] Mon...[1205][001E] héros...
+ Grazie...[1205][001E] Mon héros...
```

### 🔹 `script_113.json` — ID 6 | **Maia Prime**
- **Catégorie :** Correction / Réécriture fidèle *(Budget alloué : 322 octets)*

```diff
- Je suis [E4][NULL][NULL][0005]Maia[E4][NULL][NULL][0002]... messagère éveillée
- des Pléiades:[1205][001E] Fleurs au passé;
- fertilité à ton cœur. La lune du
- seizième soir brilledésormais...
+ Je suis [E4][NULL][NULL][0005]Maia[E4][NULL][NULL][0002], messagère éveillée des Pléiades :[1205][001E]
+ Fleurs au passé ; fertilité à ton cœur.
+ La lune du seizième soir brille désormais...
```

### 🔹 `script_114.json` — ID 0 | **Maya**
- **Catégorie :** Correction / Réécriture fidèle *(Budget alloué : 244 octets)*

```diff
- C'est ici que j'ai passé la nuit
- avec [1205][1113]-kun...[1205][001E] Où j'ai joué avec vous
- tous... Tant de bons souvenirs ici...
+ C'est ici que j'ai passé la nuit
+ avec [1113]-kun...[1205][001E] Où j'ai joué avec vous
+ tous...[1205][001E] Tant de bons souvenirs ici...
```

### 🔹 `script_114.json` — ID 2 | **Ginko**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 150 octets)*

```diff
- Ouais...[1205][001E] Trouvons Jun! On est le
- Cercle Masqué, c'est possible!
+ Ouais...[1205][001E] Sauvons Jun !
+ Le Cercle Masqué va y arriver !
```

### 🔹 `script_114.json` — ID 4 | **Voix de Tamaki**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 104 octets)*

```diff
- Une fleur, certes, mais c'est une
- fleur très précieuse...[1205][001E] Il est temps
- de rendre le crâne de cristal de vent !
+ Oubliez ça ! Regardez le ciel !
```

### 🔹 `script_115.json` — ID 9 | **Yukino**
- **Catégorie :** Correction / Réécriture fidèle *(Budget alloué : 230 octets)*

```diff
- Tu as dit M. Katatsumuri![1205][001E]? Shunsuke est au temple! S'il lui arrive
- quelque chose, je...!
+ Tu as dit le mont Katatsumuri !?[1205][001E]
+ Shunsuke est au temple ! S'il lui arrive
+ quelque chose, je... !
```

### 🔹 `script_116.json` — ID 3 | **Maya**
- **Catégorie :** Correction / Réécriture fidèle *(Budget alloué : 208 octets)*

```diff
- La route directe serait plus courte...[1205][001E]Mais je ne pense pas que ce sera forcément
- facile.
+ La route directe serait plus courte...[1205][001E]
+ Mais je ne pense pas que ce sera forcément
+ facile.
```

### 🔹 `script_120.json` — ID 4 | **Voix d'Eikichi**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 88 octets)*

```diff
- Au fait, Jun...[1205][001E] Qu'est-ce
- que tu regardes comme ça ?
+ Rock and roooooooooll !
```

### 🔹 `script_121.json` — ID 15 | **Novice**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 78 octets)*

```diff
- Là là...[1205][001E] C'est grâce à Eikichi-kun
- qu'on a repéré le piège. Allez,
- traînons pas trop par ici...
+ Regardez...[1205][001E] Le ciel !
```

### 🔹 `script_122.json` — ID 18 | **Yukino**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 128 octets)*

```diff
- Rrrrrgh ! J-Je suis particulièrement à
- cran là ! Pourquoi j'ai mis tout ça !?
+ Maya-san ? Qu'y a-t-il ? Faut aller
+ au sommet...
```

### 🔹 `script_123.json` — ID 3 | **???**
- **Catégorie :** Nettoyage accident d'édition (texte parasite collé) *(Budget alloué : 114 octets)*

```diff
- Attends, Elf.[1205][001E]Mon sonar a repéré un truc. Ordre de la
- Sainte Lance Unité anti-Persona du Dernier
- Bataillon, 13 chevaliers pilotantles
- Marionette Jaeger [NULL][NULL]Himmel Feurer.[NULL][NULL][E4][NULL][NULL]
+ Attends, Elf.[1205][001E] Mon sonar capte un truc.
```

### 🔹 `script_124.json` — ID 14 | **Maya**
- **Catégorie :** Correction / Réécriture fidèle *(Budget alloué : 162 octets)*

```diff
- [1113]a raison...[1205][001E] Fujii voulait que
- tu atteignes ton rêve, Yukki...
+ [1113] a raison...[1205][001E]
+ Fujii voulait que tu atteignes ton rêve,
+ Yukki...
```

### 🔹 `script_124.json` — ID 19 | **Durga**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 296 octets)*

```diff
- Je suis [E4][NULL][NULL][0005]Durga[E4][NULL][NULL][0002].[1205][001E] Mon devoir est de
- pourfendre le mal qui menace ce monde...[1205][001E] Sache que ton destin n'est rien de
- moinsque cela. Le stock de Personae est
- plein. Veuillez libérer un emplacement.[E4][NULL][NULL]
+ Je suis [E4][NULL][NULL][0005]Durga[E4][NULL][NULL][0002].[1205][001E] Mon devoir est de
+ pourfendre le mal qui menace ce monde...[1205][001E]
+ Sache que ton destin n'est rien de moins.
```

### 🔹 `script_124.json` — ID 30 | **Yukino**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 186 octets)*

```diff
- Il fait froid ici...[1205][001E]Mais attends-moi...[1205][001E]Je reviendrai vite te chercher... Le corps
- de Fujii. Son visage est paisible et fier.
- Le visage d'un homme ayant accompli ses
- rêves...
+ Il fait froid ici...[1205][001E] Mais attends-moi...[1205][001E]
+ Je reviendrai vite te chercher...
```

### 🔹 `script_124.json` — ID 31 | **Maya**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 166 octets)*

```diff
- Je suppose que c'est inévitable...[1205][001E] On va devoir affronter cet
- homme bientôt, après tout...
+ Où vas-tu, [1113]-kun ?[1205][001E]
+ On n'a rien à faire par là-bas...
```

### 🔹 `script_128.json` — ID 6 | **Longinus #9**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 178 octets)*

```diff
- Hahaha ! Quel culot, vermine !? Ton
- bourdonnement pitoyable n'est rien pour moi
- !
+ Hahaha ! Quel culot, vermine !
+ Ton bourdonnement ne me fait rien !
```

### 🔹 `script_129.json` — ID 5 | **Ombre de Yukino**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 738 octets)*

```diff
- Tu n'as ni le cerveau pour enseigner, ni
- l'œil pour la photo. Tu es en enfer, prise
- entre idéaux et réalité. [E1][E2] [E3][E4][NULL][NULL]"Ombre de Yukino
- Alors dis à la fille ici...[1205][001E]Qu'il est plus facile des'en prendre à tout
- le monde, comme avant.[1205][001E]Qu'il est plus facile de coucher partout.[E1][E2]
- [E3][E4][NULL][NULL]"Eikichi Enfoirée...[1205][001E]Tu n'es qu'une foutue imposteu--
+ Tu n'as ni l'esprit pour enseigner, ni l'œil
+ pour la photo. Tu es en enfer.
+ [E1][E2]
+ [E3][E4][NULL][NULL]"Ombre de Yukino
+ Dis-lui...[1205][001E] C'est plus facile de s'en prendre
+ à tous, comme avant.[1205][001E] Plus facile de coucher.
+ [E1][E2]
+ [E3][E4][NULL][NULL]"Eikichi
+ Enfoirée...[1205][001E] Foutue impostrice--
```

### 🔹 `script_130.json` — ID 9 | **Ombre de Yukino**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 184 octets)*

```diff
- Ahahaha ![1205][001E] Tu es jaloux de ma petite
- poupée adorable ? Prends-la si tu peux !
+ Hahaha ![1205][001E] Jalouse de ma jolie poupée ?
+ Prends-la si tu l'oses !
```

### 🔹 `script_131.json` — ID 8 | **Eikichi**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 240 octets)*

```diff
- T-Tu as raison...[1205][001E] La vraie est dehors...[1205][001E] C'était une impostrice, comme la
- fausse Grande Maya de tout à l'heure...
+ T-Tu as raison...[1205][001E] La vraie est dehors...[1205][001E]
+ Un leurre, comme la fausse Grande
+ Maya tout à l'heure...
```

### 🔹 `script_133.json` — ID 9 | **Jun**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 64 octets)*

```diff
- Aaaaaaaaaaaah ! Grande Sœur !
+ Aaaaaah ! Grande Sœur !
```

### 🔹 `script_134.json` — ID 0 | **Jun**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 162 octets)*

```diff
- *Snif* Soeurette...[1205][001E] [1205][001E] Pardon... Pardon!
- Je... n'ai pas pu te sauver...
+ *Snif* Sœurette...[1205][001E] Pardon ! Pardon ![1205][001E]
+ Je n'ai pas pu te sauver...
```

### 🔹 `script_134.json` — ID 7 | **Ginko**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 186 octets)*

```diff
- [1432][NULL][NULL][0014]Le regret...[1205][001E] [1432][NULL][NULL][0014]... Jun n'a pas changé du
- tout... Le vrai Jun est toujours là!
+ [1432][NULL][NULL][0014]Regret[1432][NULL][NULL][0014]...[1205][001E] Jun n'a pas changé...[1205][001E]
+ Le vrai Jun est toujours là !
```

### 🔹 `script_134.json` — ID 13 | **Eikichi**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 178 octets)*

```diff
- C'est pour ça que je ne laisserai personne
- les violer ![1205][001E] On ne touche pas à ça !
+ Je laisserai personne les profaner ![1205][001E]
+ Pas touche à ça !
```

### 🔹 `script_136.json` — ID 12 | **Jun**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 282 octets)*

```diff
- On aimait tous les deux Grande Sœur...[1205][001E] On avait promis de protéger notre
- [1432][NULL][NULL][0014]Maman[1432][NULL][NULL][0014] quoi qu'il arrive...[1205][001E] Et toi tu as
- brisé cette promesse et tu l'as tuée !
+ On l'aimait tous les deux...[1205][001E] On avait juré
+ de protéger notre [1432][NULL][NULL][0014]Maman[1432][NULL][NULL][0014]...[1205][001E] Mais tu as
+ trahis ta promesse et tu l'as tuée !
```

### 🔹 `script_137.json` — ID 4 | **Ginko**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 180 octets)*

```diff
- Je vois... Je ne savais pas ça...[1205][001E] Tout le
- monde aimait Grande Sœur.[1205][001E] Alors pourquoi...?
+ Je vois... J'ignorais ça...[1205][001E] Tout le
+ monde l'aimait.[1205][001E] Alors pourquoi... ?
```

### 🔹 `script_139.json` — ID 16 | **Joker**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 84 octets)*

```diff
- C'est vrai...[1205][001E] Je suis... le Joker !
+ Oui...[1205][001E] Je suis... Joker !
```

### 🔹 `script_140.json` — ID 2 | **Voix inconnue**
- **Catégorie :** Correction / Réécriture fidèle *(Budget alloué : 236 octets)*

```diff
- Tu veux le pouvoir...[1205][001E] ? Alors
- demande-le. Déteste-toi, immole-toi
- dans les flammes de l'aversion...
+ Tu veux le pouvoir... ?[1205][001E] Désire-le...
+ Hais...[1205][001E] Immole-toi dans les flammes
+ de l'abomination...
```

### 🔹 `script_142.json` — ID 14 | **Hermès**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 324 octets)*

```diff
- Je suis [E4][NULL][NULL][0005]Hermès[E4][NULL][NULL][0002]...[1205][001E]Donneur de fortune et de gloire, héraut des
- âmes...[1205][001E]À mon alter égo: Aime ton voisin, incarne le
- vent ded'altruisme... Le stock de Personae
- est plein. Libérez un emplacement.[E4][NULL][NULL]
+ Je suis [E4][NULL][NULL][0005]Hermès[E4][NULL][NULL][0002]...[1205][001E] Héraut des âmes, porteur
+ de fortune et de gloire...[1205][001E] À mon alter ego :
+ Aime ton prochain d'un cœur pur comme le vent...
```

### 🔹 `script_142.json` — ID 17 | **Apollo**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 276 octets)*

```diff
- Je suis toi... Tu es moi...[1205][001E] Arrivé depuis
- l'océan de ton âme...[1205][001E] Souverain du soleil
- embrasé, des cieux azurés, [E4][NULL][NULL][0005]Apollo[E4][NULL][NULL][0002]...
+ Je suis toi... Tu es moi...[1205][001E] Issu des flots
+ de ton âme...[1205][001E] Maître du soleil ardent et
+ des cieux azur, [E4][NULL][NULL][0005]Apollo[E4][NULL][NULL][0002]...
```

### 🔹 `script_142.json` — ID 41 | **Hermès**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 324 octets)*

```diff
- Je suis [E4][NULL][NULL][0005]Hermès[E4][NULL][NULL][0002]...[1205][001E]Donneur de fortune et de gloire, héraut des
- âmes...[1205][001E]À mon alter égo: Aime ton voisin, incarne le
- vent ded'altruisme... Le stock de Personae
- est plein. Libérez un emplacement.[E4][NULL][NULL]
+ Je suis [E4][NULL][NULL][0005]Hermès[E4][NULL][NULL][0002]...[1205][001E] Héraut des âmes, porteur
+ de fortune et de gloire...[1205][001E] À mon alter ego :
+ Aime ton prochain d'un cœur pur comme le vent...
```

### 🔹 `script_143.json` — ID 70 | **Jun**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 238 octets)*

```diff
- S'il te plaît, [1113], j'ai besoin de ta
- force... Je dois arrêter Père ! C'est la
- seule façon d'expier ce que j'ai fait.
+ S'il te plaît, [1113], prête-moi ta force...
+ Je dois arrêter Père ! C'est ma seule façon
+ d'expier mes actes.
```

### 🔹 `script_145.json` — ID 19 | **Jun**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 110 octets)*

```diff
- Après ça...[1205][001E] Il ne restera plus que Père.
- Quelque chose est écrit dans le relief.
+ Après ça...[1205][001E] Plus qu'à vaincre Père.
```

### 🔹 `script_147.json` — ID 18 | **Jun**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 102 octets)*

```diff
- [1113]...[1205][001E] Ce signe est digne de toi. Quelque
- chose est inscrit dans le relief.
+ [1113]...[1205][001E] Une constellation digne de toi.
```

### 🔹 `script_149.json` — ID 5 | **Ombre de [1113]**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 244 octets)*

```diff
- Quand arrêtera-tu de te voiler la
- face? Le vrai toi ne prends jamais de
- décisions, même dans son propre intérêt.
+ Quand cesseras-tu de te leurrer ?
+ Tu ne prends jamais de décision, même
+ pour ton propre bien.
```

### 🔹 `script_149.json` — ID 13 | **Ombre de [1113]**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 238 octets)*

```diff
- Quand arrêtera-tu de te voiler la
- face? Le vrai toi a abandonné ses
- rêves...[1205][001E] abandonné sa vie entière.
+ Quand cesseras-tu de te leurrer ?
+ Tu as renoncé à tes rêves...[1205][001E]
+ Tu as renoncé à ta vie entière.
```

### 🔹 `script_149.json` — ID 33 | **Ombre de [1113]**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 206 octets)*

```diff
- Quelle prétention...[1205][001E] À quel point
- ton égo est-il grand pour que
- tu juges les autres comme ça?
+ Quelle prétention...[1205][001E] Ton ego est-il si
+ démesuré pour juger les autres ainsi ?
```

### 🔹 `script_149.json` — ID 39 | **Ombre de [1113]**
- **Catégorie :** Restauration d'opcode critique *(Budget alloué : 260 octets)*

```diff
- S'il te plaît, [1113], j'ai besoin de ta
- force... Je dois arrêter Père ! C'est la
- seule façon d'expier ce que j'ai fait.
+ C'est cette faiblesse qui te définit...[1205][001E]
+ La faiblesse est un péché. Je te rejette ![1205][001E]
+ Prépare-toi à mourir ici !
```

### 🔹 `script_150.json` — ID 33 | **Maya**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 136 octets)*

```diff
- On a terminé ici ? Bien, en
- route pour le prochain temple !
+ On a fini ici ? En route pour le
+ prochain temple !
```

### 🔹 `script_152.json` — ID 21 | **Jun**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 110 octets)*

```diff
- Après ça...[1205][001E] On devra juste vaincre Père.
- Il y a une inscription sur ce relief.
+ Après ça...[1205][001E] Plus qu'à vaincre Père.
```

### 🔹 `script_154.json` — ID 4 | **Jun**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 222 octets)*

```diff
- Les Taureaux sont très jaloux, cette
- constellation va donc à merveille
- à Lisa. Inscription sur le relief.
+ Les Taureaux sont très jaloux, cette
+ constellation va à merveille à Lisa.
```

### 🔹 `script_157.json` — ID 1 | **Ginko**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 200 octets)*

```diff
- Je ne veux pas être un frein
- pour toi...[1205][001E] Ahaha... Pas le
- meilleur moment pour dire, hein?
+ Je ne veux pas être un fardeau...[1205][001E]
+ Ahaha... Pas trop le moment, hein ?
```

### 🔹 `script_157.json` — ID 13 | **Eikichi**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 188 octets)*

```diff
- *siffle* Elle est [1205][001E]toujours aussi passionnée.
- C'est dur d'être un séducteur, hein?
+ *siffle*[1205][001E] Toujours aussi passionnée !
+ C'est dur d'être un tombeur, pas vrai ?
```

### 🔹 `script_157.json` — ID 18 | **Jun**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 60 octets)*

```diff
- Maintenant. [1205][001E]On y va?
+ Alors...[1205][001E] On y va ?
```

### 🔹 `script_159.json` — ID 19 | **Jun**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 110 octets)*

```diff
- Après...[1205][001E] Reste plus qu'à vaincre mon père.
- Il y a une inscription sur le relief.
+ Après ça...[1205][001E] Plus qu'à vaincre Père.
```

### 🔹 `script_161.json` — ID 7 | **Jun**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 220 octets)*

```diff
- Ils peuvent être silencieux, cruels,
- criminels, mais Michel a laissé ça
- derrière... Une inscription sur le relief.
+ Ils peuvent être calmes, cruels et
+ criminels, mais Michel a laissé tout
+ ça derrière lui...
```

### 🔹 `script_163.json` — ID 21 | **Ombre d'Eikichi**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 48 octets)*

```diff
- Tch !
+ Tch
```

### 🔹 `script_164.json` — ID 4 | **Miyabi**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 78 octets)*

```diff
- Merci, Eikichi...[1205][001E] Merci...
+ Merci...[1205][001E] Merci...
```

### 🔹 `script_164.json` — ID 28 | **Eikichi**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 124 octets)*

```diff
- OK, le show est terminé. Il est temps
- d'aller vite au prochain concert !
+ Fin du spectacle ! Vite, au prochain
+ concert !
```

### 🔹 `script_166.json` — ID 22 | **Jun**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 110 octets)*

```diff
- Après ça...[1205][001E] Il ne restera plus que Père.
- Quelque chose est écrit dans le relief.
+ Après ça...[1205][001E] Reste plus qu'à vaincre Père.
```

### 🔹 `script_168.json` — ID 7 | **Jun**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 264 octets)*

```diff
- Mais ces mots ne valent rien...[1205][001E]Je représente l'arrogance, comment
- pourrais-je aider quiconque à atteindre ses
- idéaux? Quelque chose est écrit dans le
- relief.
+ Ce ne sont que des mots...[1205][001E] En vérité,
+ je ne suis qu'un vantard. Jamais je ne
+ pourrai guider les gens vers leur idéal...
```

### 🔹 `script_171.json` — ID 2 | **Jun**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 60 octets)*

```diff
- Agh...[1205][001E] Ma... mère...?
+ Agh...[1205][001E] Maman... ?
```

### 🔹 `script_171.json` — ID 20 | **Jun**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 88 octets)*

```diff
- Filons maintenant au prochain temple !
+ Vite, au prochain temple !
```

### 🔹 `script_172.json` — ID 0 | **Eikichi**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 258 octets)*

```diff
- Je sais qu'il y a une rivière pas loin,
- mais cette Rivière d'Argent machinchose[1205][001E]
- juste là-dessous.[001E].. C'est ridicule.
+ Cette Rivière d'Argent est là-dessous ?
+ Je sais qu'il y a un fleuve tout près,
+ mais quand même...[1205][001E] C'est ridicule.
```

### 🔹 `script_174.json` — ID 6 | **Eikichi**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 78 octets)*

```diff
- (Dis... Elle va y arriver?)
+ (Tu crois qu'elle peut ?)
```

### 🔹 `script_174.json` — ID 16 | **Maya**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 52 octets)*

```diff
- ...Oui, Madame...
+ ...Oui Madame...
```

### 🔹 `script_176.json` — ID 7 | **Eikichi**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 114 octets)*

```diff
- Au fait, Jun...[1205][001E] Qu'est-ce
- que tu regardes comme ça ?
+ Au fait, Jun...[1205][001E] Tu regardes quoi ?
```

### 🔹 `script_184.json` — ID 11 | **Jun**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 104 octets)*

```diff
- Mon Papa...[1205][001E] Il est...[1205][001E] C'est pas un bon à rien !
+ Mon Papa...[1205][001E] Il est...[1205][001E] pas un vaurien !
```

### 🔹 `script_185.json` — ID 9 | **Maya**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 196 octets)*

```diff
- Je suppose que c'est inévitable...[1205][001E] On va devoir affronter cet
- homme bientôt, après tout...
+ Je suppose que c'est fatal...[1205][001E] On devra
+ affronter cet homme sous peu, après tout...
```

### 🔹 `script_186.json` — ID 0 | **Eikichi**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 102 octets)*

```diff
- Quoi...[1205][001E] qu'est-ce qui s'est passé ici?
+ Mais enfin... ?[1205][001E] Que s'est-il passé ?
```

### 🔹 `script_186.json` — ID 10 | **Maya**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 212 octets)*

```diff
- Le [1121]corps de Mme Ideal ne semble
- pas ici, elle est peut-être encore
- [1205][001E]en vie... où elle est passée.
+ Pas de [1121]corps en vue, elle doit être
+ en vie...[1205][001E] Mais où est-elle passée ?
```

### 🔹 `script_186.json` — ID 17 | **Jun**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 262 octets)*

```diff
- Les rêves... Les idéaux...[1205][001E] Les gens sont
- souvent prêts à risquer leur vie pour eux.
- Alors vaut-il mieux ne pas en avoir...?
+ Rêves... Idéaux...[1205][001E] Les gens risquent
+ souvent leur vie pour eux. Alors,
+ vaut-il mieux ne pas en avoir... ?
```

### 🔹 `script_187.json` — ID 12 | **Maya**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 140 octets)*

```diff
- Non ![1205][001E] Je ne suis pas la fille bien que
- tu crois que je suis ! Ne pars pas !
+ Non ![1205][001E] Je ne suis pas si parfaite !
+ Ne pars pas !
```

### 🔹 `script_189.json` — ID 16 | **Maya**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 172 octets)*

```diff
- A-Attendez une seconde, vous deux...!
- Est-ce que ça ne vous semble pas
- un peu trop beau pour être vrai !?
+ A-Attendez deux secondes...!
+ C'est pas un peu trop beau
+ pour être vrai !?
```

### 🔹 `script_190.json` — ID 0 | **Eikichi**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 238 octets)*

```diff
- Mince, où sont passés les autres? Les
- laisser faire, ça va poser problème?[E1][E2] [E3][E4][NULL][NULL]"Jun
- L-Lisa!?
+ Que font les autres ? Les laisser faire
+ à leur guise, c'est risqué ?[E1][E2]
+ [E3][E4][NULL][NULL]"Jun
+ Lisa!?
```

### 🔹 `script_190.json` — ID 6 | **Maya**
- **Catégorie :** Correction / Réécriture fidèle *(Budget alloué : 234 octets)*

```diff
- *pam* *pam* C-C'est pas drôle...[1205][001E] !
- J'ai failli me faire écraser comme un
- costume neuf! J'aurais pu y rester!
+ *pfff* *pfff*[1205][001E] C-C'est pas drôle... ![1205][001E]
+ J'ai failli finir aplatie comme une crêpe !
+ J'aurais pu y passer !
```

### 🔹 `script_190.json` — ID 13 | **Ginko**
- **Catégorie :** Correction / Réécriture fidèle *(Budget alloué : 140 octets)*

```diff
- Je ne rigole pas! [1113]La source
- curative était vraiment là!
+ Je blague pas, [1113] ! La source
+ curative était vraiment là !
```

### 🔹 `script_191.json` — ID 5 | **Jun**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 154 octets)*

```diff
- Hmm...[1205][001E] Je m'inquiète pour Michel et
- Grande Maya. On devrait retourner, [1113].
+ Hmm...[1205][001E] Je m'inquiète pour Michel et
+ Maya. Rentrons, [1113].
```

### 🔹 `script_192.json` — ID 5 | **???**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 110 octets)*

```diff
- Oh, bonjour...[1205][001E] Merci de t'être occupé de Jun.
+ Oh, bonjour...[1205][001E] Merci de t'occuper de Jun...
```

### 🔹 `script_192.json` — ID 8 | **Jun**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 124 octets)*

```diff
- N-Non...[1205][001E] Attends... C'est
- ça...[1205][001E] A-Arrête... ARRÊTE !
+ N-Non...[1205][001E] Attends... C'est
+ ça...[1205][001E] Arrête... STOP !
```

### 🔹 `script_194.json` — ID 32 | **Jun**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 182 octets)*

```diff
- Je dois assumer mes responsabilités.[1205][001E] Quel que
- soit le châtiment qui m'attend à la fin...
+ Je dois assumer mes actes.[1205][001E] Quel que
+ soit le châtiment qui m'attend à la fin...
```

### 🔹 `script_195.json` — ID 1 | **Longinus #1**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 162 octets)*

```diff
- Ah, Fraulein...[1205][001E] Il semble que tu
- as percé le secret de Xibalba.
+ Ah, Fräulein...[1205][001E] Tu as donc percé
+ le secret de Xibalba.
```

### 🔹 `script_195.json` — ID 6 | **Maya**
- **Catégorie :** Calibrage menu à choix *(Budget alloué : 322 octets)*

```diff
- Malheureusement pour toi, on va
- DÉFINITIVEMENT gagner. Hein, tout le monde !?
- [E1][E2]
- [E3][E4][NULL][NULL]Maya
- Hein, tout le monde !?
- [1208][0002][1432][NULL][NULL][0014]Bien sûr que oui.[1432][NULL][NULL][0014]
- [1432][NULL][NULL][0014]J'en suis pas si sûr...[1432][NULL][NULL][0014]
+ Pas de chance pour toi, on va
+ GAGNER à coup sûr. Pas vrai !?
+ [E1][E2]
+ [E3][E4][NULL][NULL]"Maya
+ Pas vrai !?
+ [1208][0002][1432][NULL][NULL][0014]Carrément.[1432][NULL][NULL][0014]
+ [1432][NULL][NULL][0014]Pas si sûr...[1432][NULL][NULL][0014]
```

### 🔹 `script_198.json` — ID 8 | **Maya**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 70 octets)*

```diff
- Fais attention à toi aussi, [1113]-kun.
+ Sois prudent, [1113]-kun.
```

### 🔹 `script_199.json` — ID 0 | **Ginko**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 1164 octets)*

```diff
- Hey, Jun! Ton papa est incroyable, il peut
- tout faire, pas vrai? Tu penses qu'on va le
- voir aujourd'hui? [E1][E2] [E3][E4][NULL][NULL]"Jun Pe-Peut-être...[1205][001E]Il... est occupé, donc... [E1][E2] [E3][E4][NULL][NULL]"Eikichi Mon
- p-père travaille dans un restaurant de
- sushi...S-Sérieux je dois manger des
- s-suhshi tout les jours. [E1][E2] [E3][E4][NULL][NULL]"Maya C'est
- bientôt l'heure pour vos familles de venir
- vous chercher. [E1][E2] [E3][E4][NULL][NULL]"Ginko Je me demande si ma
- maman sera première aujourd'hui?J'ai faim! [E1][E2]
- [E3][E4][NULL][NULL]"Eikichi Oh, y'a quelqu'un. Je ne le
- reconnais pas...[1205][001E]M-Mais il a l'air cool! [E1][E2] [E3][E4][NULL][NULL]"Père de Jun Je
- viens te chercher, Jun.
+ Hé, Jun ! Ton père est génial, il sait
+ tout faire, pas vrai ? On va le voir
+ aujourd'hui ?
+ [E1][E2]
+ [E3][E4][NULL][NULL]"Jun
+ P-Peut-être...[1205][001E] Mais il est très occupé...
+ [E1][E2]
+ [E3][E4][NULL][NULL]"Eikichi
+ J'aimerais que mon père t-travaille pas
+ dans un resto de sushis... J-Je dois en
+ manger tous les jours.
+ [E1][E2]
+ [E3][E4][NULL][NULL]"Maya
+ Vos parents vont bientôt venir vous
+ chercher.
+ [E1][E2]
+ [E3][E4][NULL][NULL]"Ginko
+ Ma maman sera la première ? J'ai faim !
+ [E1][E2]
+ [E3][E4][NULL][NULL]"Eikichi
+ Oh, quelqu'un arrive. Je le connais
+ pas...[1205][001E] M-Mais il a trop la classe !
+ [E1][E2]
+ [E3][E4][NULL][NULL]"Père de Jun
+ Je viens te chercher, Jun.
```

### 🔹 `script_199.json` — ID 5 | **Ginko**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 378 octets)*

```diff
- T'avais raison ! Il est super cool ! [E1][E2] [E3][E4][NULL][NULL]Maya
- Je suis contente pour toi, Jun-kun ! C'est
- bien que ton père soit venu te chercher. [E1][E2]
- [E3][E4][NULL][NULL]Jun M-Maman m'attend pas à la maison...![1205][001E]Ne fais pas ça...!
+ C'est vrai ! Il a trop la classe !
+ [E1][E2]
+ [E3][E4][NULL][NULL]"Maya
+ Contente pour toi, Jun ! C'est bien que
+ ton père vienne te chercher.
+ [E1][E2]
+ [E3][E4][NULL][NULL]"Jun
+ M-Maman m'attend pas... ![1205][001E]
+ Arrête... !
```

### 🔹 `script_200.json` — ID 0 | **Jun**
- **Catégorie :** Correction / Réécriture fidèle *(Budget alloué : 148 octets)*

```diff
- Maman... Ne me rejette pas...[1205][001E] Ne
- me hais pas... À l'aide Papa...
+ Maman... M'efface pas...[1205][001E] Ne me
+ hais pas...[1205][001E] À l'aide, Papa...
```

### 🔹 `script_200.json` — ID 2 | **Maman en métal**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 124 octets)*

```diff
- Jun...[1205][001E] Sans toi et Papa, je serais libre.
+ Jun...[1205][001E] Sans vous deux, je serais libre.
```

### 🔹 `script_200.json` — ID 4 | **Maya**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 194 octets)*

```diff
- Jun-kun ![1205][001E] Ce n'est qu'une illusion
- née de tes douloureux souvenirs
- ! Tu ne disparaîtras pas !
+ Jun-kun ![1205][001E] C'est juste une illusion de tes
+ souvenirs ! Tu ne vas pas disparaître !
```

### 🔹 `script_201.json` — ID 19 | **Jun**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 216 octets)*

```diff
- À l'époque...[1205][001E] J'étais jaloux des familles
- heureuses des autres...[1205][001E] C'est pour ça
- que j'ai menti au sujet de la mienne...
+ À l'époque...[1205][001E] J'enviais le bonheur
+ des autres...[1205][001E] C'est pour ça que
+ j'ai menti sur la mienne...
```

### 🔹 `script_202.json` — ID 3 | **Ginko**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 134 octets)*

```diff
- Aiyah...[1205][001E] !? C'est quoi ces
- extraterrestres absurde...!?
+ Aiyah... !?[1205][001E] C'est quoi ces aliens ridicules...!?
```

### 🔹 `script_202.json` — ID 8 | **Jun**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 234 octets)*

```diff
- Une seule personne connaît Lak'ech,
- a part toi et Roi Tatsuya Sudou...[1205][001E] Je suis le fils d'Akinari Kashihara!
+ Un seul homme connaissait l'In Lak'ech,
+ à part toi et le Roi...[1205][001E] Je suis le
+ fils d'Akinari Kashihara !
```

### 🔹 `script_202.json` — ID 12 | **Mme Idéale**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 230 octets)*

```diff
- Je n'ai pas peur de mourir pour prouver que
- ses recherches étaient vraies ! J'étais plus
- digne d'être sa femme que cette harpie !
+ Mourir pour ses thèses ne m'effraie pas !
+ J'étais plus digne d'être sa femme
+ que cette mégère !
```

### 🔹 `script_203.json` — ID 0 | **Eikichi**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 424 octets)*

```diff
- Elle s'en sort. Elle est juste évanouie.[1205][001E]Putain, quelle folle...[E1][E2] [E3][E4][NULL][NULL]"Jun Je pense...
- Elle était vraiment prête à mourir...[1205][001E]La dernière étape de l'Oracleest le
- sacrifice de la Vierge Maia...
+ Elle s'en sort, elle est juste sonnée.[1205][001E]
+ Quelle folle dingue...
+ [E1][E2]
+ [E3][E4][NULL][NULL]"Jun
+ Je crois... qu'elle voulait mourir...[1205][001E]
+ L'étape finale de l'Oracle est le sacrifice
+ de la Vierge Maia...
```

### 🔹 `script_203.json` — ID 25 | **Jun**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 200 octets)*

```diff
- Mais il était gentil avec moi...[1205][001E] Pourquoi
- n'ai-je pas été assez fier pour le
- revendiquer comme mon père ce jour-là...?
+ Il était si doux...[1205][001E] Pourquoi n'ai-je pas
+ osé dire qu'il était mon père ce jour-là... ?
```

### 🔹 `script_204.json` — ID 10 | **Führer**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 84 octets)*

```diff
- Aheheh...[1205][001E] Fwahahahahahahaha !
+ Aheheh...[1205][001E] Fwahahahahahahaha!
```

### 🔹 `script_206.json` — ID 0 | **Reine Verseau**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 140 octets)*

```diff
- J...[1205]< Jun...[1205]< J'espère que
- tu trouveras... le bonheur...
+ J...[1205]< Jun...[1205]< Trouve...
+ le bonheur...
```

### 🔹 `script_207.json` — ID 13 | **Maya**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 164 octets)*

```diff
- Si j'accordais une seconde pensée à la
- défaite, je n'atteindrais jamais mes rêves !
+ Si je songeais à la défaite,
+ je n'atteindrais jamais mes rêves !
```

### 🔹 `script_208.json` — ID 8 | **Nyarlathotep**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 294 octets)*

```diff
- Il serait plus juste de dire [1432][NULL][NULL][0014]TOI.[1432][NULL][NULL][1205][0014][001E] LUI ne
- peut qu'observer. Mais moi... Je suis
- différent. [E1][E2] [E3][E4][NULL][NULL]"Maya P... Pourquoi?
+ Il serait plus juste de dire [1432][NULL][NULL][0014]toi[1432][NULL][NULL][0014].[1205][001E]
+ LUI ne peut qu'observer. Mais moi...
+ Je suis différent.
+ [E1][E2]
+ [E3][E4][NULL][NULL]"Maya
+ Pourquoi... ?
```

### 🔹 `script_208.json` — ID 24 | **Nyarlathotep**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 234 octets)*

```diff
- Et en signe de respect, je vous
- accorderai le rêve de destruction que
- vous les humains avez toujours voulu !
+ Par respect, je vous offrirai ce rêve de
+ destruction que vous, humains, désirez tant !
```

### 🔹 `script_209.json` — ID 22 | **Philémon**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 188 octets)*

```diff
- Je suis toi. Tu es moi...[1205][001E] Je veillerai
- toujours sur toi de l'intérieur. Adieu...
+ Je suis toi. Tu es moi...[1205][001E] Je veillerai
+ toujours sur toi de l'intérieur. Adieu.
```

### 🔹 `script_210.json` — ID 13 | **Lisa**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 200 octets)*

```diff
- A-Allez, oublie-le ! On va au
- karaoké ! On doit s'entraîner
- pour nos débuts ensemble, non ?
+ A-Allez, oublie-le ! Au karaoké !
+ On doit s'entraîner pour nos débuts
+ ensemble, pas vrai ?
```

### 🔹 `script_211.json` — ID 7 | **Eikichi**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 164 octets)*

```diff
- Bah... J'ai besoin de plus de
- membres. Je suppose que ça ne
- ferait pas de mal de le rencontrer.
+ Bah... Il me faut des membres.
+ Ça ne coûte rien de le voir.
```

### 🔹 `script_212.json` — ID 0 | **Jun**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 242 octets)*

```diff
- C'était magnifique, Mère. [E1][E2] [E3][E4][NULL][NULL]"Maman de Jun
- Merci Jun. C'est un [E4][NULL][NULL][0006]pois de senteur[E4][NULL][NULL][0002], tu
- vois?
+ C'était magnifique, Mère.
+ [E1][E2]
+ [E3][E4][NULL][NULL]"Mère de Jun
+ Merci, Jun. Un [E4][NULL][NULL][0006]pois de senteur[E4][NULL][NULL][0002], oui ?
```

### 🔹 `script_212.json` — ID 3 | **Mère de Jun**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 186 octets)*

```diff
- Je n'ai pas tout à fait fini de tourner
- ici, j'ai bien peur. Tu peux rentrer seul ?
+ Le tournage n'est pas encore fini,
+ hélas. Tu peux rentrer seul ?
```

### 🔹 `script_214.json` — ID 0 | **Philémon**
- **Catégorie :** Correction / Réécriture fidèle *(Budget alloué : 160 octets)*

```diff
- [1113][1112]...[1205][001E] Vas-tu vraiment en finir
- sans réaliser ton rêve?
+ [1113] [1112]...[1205][001E] Vas-tu vraiment en finir
+ sans réaliser ton rêve ?
```

### 🔹 `script_214.json` — ID 2 | **Philémon**
- **Catégorie :** Correction / Réécriture fidèle *(Budget alloué : 160 octets)*

```diff
- [1113][1112]...[1205][001E] Vas-tu vraiment en finir
- sans réaliser ton rêve?
+ [1113] [1112]...[1205][001E] Vas-tu vraiment en finir
+ sans réaliser ton rêve ?
```

### 🔹 `script_217.json` — ID 1 | **Gérant**
- **Catégorie :** Correction / Réécriture fidèle *(Budget alloué : 488 octets)*

```diff
- V-Vieilles bombes!? Enfin, sortir d'ici
- avant l'explosion![E1][E2] [E3][E4][NULL][NULL]"Maya Elle était
- secouée...[1205][001E]Allez, vite, trouvons l'énigme et filons!
+ V-Vieilles bombes !? Enfin, sortir d'ici
+ avant l'explosion !
+ [E1][E2]
+ [E3][E4][NULL][NULL]"Maya
+ Elle était secouée...[1205][001E] Allez, vite,
+ trouvons l'énigme et filons !
```

### 🔹 `script_217.json` — ID 9 | **Yukino**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 132 octets)*

```diff
- Tu l'as trouvé !? Bien joué, [1113]
- ! Maintenant on dégage d'ici !
+ Tu l'as trouvé !? Bien joué, [1113] !
+ Partons vite d'ici !
```

### 🔹 `script_219.json` — ID 7 | **Yukino**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 252 octets)*

```diff
- C'est vrai ! Je peux pas mourir en simple
- apprentie ! Et puis... Il y a quelque
- chose que je dois dire avant de partir !
+ C'est vrai ! Pas question de mourir en
+ simple apprentie ! Et puis... j'ai un truc
+ sur le cœur avant de partir !
```

### 🔹 `script_221.json` — ID 11 | **Yukino**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 252 octets)*

```diff
- C'est vrai ! Je peux pas mourir en simple
- apprentie ! Et puis... Il y a quelque
- chose que je dois dire avant de partir !
+ C'est vrai ! Pas question de mourir en
+ simple apprentie ! Et puis... j'ai un truc
+ sur le cœur avant de partir !
```

### 🔹 `script_222.json` — ID 9 | **Yukino**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 252 octets)*

```diff
- C'est vrai ! Je peux pas mourir en simple
- apprentie ! Et puis... Il y a quelque
- chose que je dois dire avant de partir !
+ C'est vrai ! Pas question de mourir en
+ simple apprentie ! Et puis... j'ai un truc
+ sur le cœur avant de partir !
```

### 🔹 `script_226.json` — ID 4 | **Eikichi**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 444 octets)*

```diff
- H-Hey là! Pourquoi tu te tiens comme ça à
- l'épaule?[E1][E2] [E3][E4][NULL][NULL]"Eikichi J-Je veux dire, tu fais
- ça depuis le Caracol...[1205]< Pourquoion ne
- laisserait pas Mr. Tomi y jeter un coup
- d'oeil![1205][001E]J-Je plaisante...
+ H-Hé ! Pourquoi tu te tiens l'épaule
+ comme ça ?
+ [E1][E2]
+ [E3][E4][NULL][NULL]"Eikichi
+ Tu fais ça depuis le Caracol...[1205]< Et si
+ on demandait à M. Tomi de regarder ![1205][001E]
+ J-Je rigole...
```

### 🔹 `script_226.json` — ID 8 | **Yukino**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 146 octets)*

```diff
- ...[1205][001E] Allons-y, [1113]...[1205][001E] Il y a encore
- quelque chose que je dois faire...
+ ...[1205][001E] En route, [1113]...[1205][001E]
+ J'ai encore quelque chose à faire...
```

### 🔹 `script_232.json` — ID 7 | **Yukino**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 252 octets)*

```diff
- C'est vrai ! Je peux pas mourir en simple
- apprentie ! Et puis... Il y a quelque
- chose que je dois dire avant de partir !
+ C'est vrai ! Pas question de mourir en
+ simple apprentie ! Et puis... j'ai un truc
+ sur le cœur avant de partir !
```

### 🔹 `script_233.json` — ID 0 | **Eikichi**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 112 octets)*

```diff
- Mince ! Je le laisse pas s'échapper encore !
+ Merde ! Il m'échappera pas cette fois !
```

### 🔹 `script_245.json` — ID 2 | **Femme de bureau**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 266 octets)*

```diff
- Ça me rappelle, il paraît qu'il y a
- un salon secret au fond du Zodiac.[1205][000F] Je
- n'ai pas encore réussi à le trouver...
+ Ça me rappelle, on dit qu'il y a
+ un salon secret au fond du Zodiac.[1205][000F] Je
+ ne l'ai pas encore trouvé...
```

### 🔹 `script_248.json` — ID 4 | **Fantôme du prof**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 66 octets)*

```diff
- .. ne dois...
+ ...jamais...
```

### 🔹 `script_248.json` — ID 33 | **Proviseur Hanya**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 184 octets)*

```diff
- Venez, imbéciles! La tour sera votre
- salle de détention! Gloire au Masque!
+ Venez, fous ! Cette tour sera votre colle !
+ Gloire au Masque !
```

### 🔹 `script_248.json` — ID 34 | **Eikichi**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 130 octets)*

```diff
- Qu'est-ce qu'il y a ? J'ai
- quelque chose sur le visage...?
+ Qu'y a-t-il ? J'ai quelque chose
+ sur le visage... ?
```

### 🔹 `script_251.json` — ID 22 | **Lycéenne**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 270 octets)*

```diff
- C'est terrible ! Vraiment terrible ![1205][000F] Mme
- Saeko est aussi prisonnière quelque part ![1205][000F]
- Mais je suis sûre que le Proviseur Hanya va
- la sauver.
+ C'est affreux, affreux ![1205][000F] Mme Saeko est
+ prisonnière elle aussi ![1205][000F] Mais le proviseur
+ Hanya la sauvera, c'est sûr !
```

### 🔹 `script_252.json` — ID 18 | **Lycéenne**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 270 octets)*

```diff
- C'est terrible ! Vraiment terrible ![1205][000F] Mme
- Saeko est aussi prisonnière quelque part ![1205][000F]
- Mais je suis sûre que le Proviseur Hanya va
- la sauver.
+ C'est affreux, affreux ![1205][000F] Mme Saeko est
+ prisonnière elle aussi ![1205][000F] Mais le proviseur
+ Hanya la sauvera, c'est sûr !
```

### 🔹 `script_253.json` — ID 5 | **Lycéenne blessée**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 294 octets)*

```diff
- Seven Sisters est tellement plein de beaufs
- ? Et toi tu es le plus beau, mais bon ?
- Cette histoire de malédiction, c'est
- vraiment nul ?
+ Seven Sisters a plein de beaux gosses ?
+ Et t'es le plus craquant, tu sais ? Mais
+ cette malédiction, c'est trop nul, genre ?
```

### 🔹 `script_254.json` — ID 29 | **Lycéen blessé**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 228 octets)*

```diff
- Oh, je pige! Vous êtes potes
- maintenant. On dirait que les
- rumeurs sur vos exploits sont vraies!
+ Oh, je pige ! Vous êtes potes.
+ On dirait que les rumeurs sur vos
+ exploits sont vraies !
```

### 🔹 `script_255.json` — ID 6 | **Lycéen blessé**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 304 octets)*

```diff
- On l'appelle [1432][NULL][NULL][0014]la Rumouriste[1432][NULL][NULL][0014], alors je pensais
- qu'elle pourrait savoir quelque chose sur la
- malédiction... Peut-être qu'elle est allée
- au Peace Diner ?
+ On la nomme [1432][NULL][NULL][0014]la Rumouriste[1432][NULL][NULL][0014], elle
+ doit tout savoir de la malédiction...
+ Elle est peut-être au Peace Diner ?
```

### 🔹 `script_256.json` — ID 39 | **Lycéen blessé**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 284 octets)*

```diff
- Vous devriez aider à nettoyer, Senpai. Le
- Proviseur Hanya semblait furieux... On
- n'aurait jamais dû détruire tous ces
- insignes.
+ Aidez-nous à nettoyer, Senpai. Le proviseur
+ Hanya avait l'air furieux... On n'aurait
+ jamais dû briser ces insignes.
```

### 🔹 `script_257.json` — ID 3 | **Concierge**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 288 octets)*

```diff
- Je me demande combien d'années ont
- passé depuis cette tragédie...[1205][001E] C'était
- horrible. Namu Amida Butsu, Namu Amida
- Butsu...[1205]< Bah, c'est l'heure du dîner !
+ Que d'années depuis cette tragédie...[1205][001E]
+ C'était affreux. Namu Amida Butsu,
+ Namu Amida Butsu...[1205]< À table !
```

### 🔹 `script_258.json` — ID 4 | **Eikichi**
- **Catégorie :** Correction / Réécriture fidèle *(Budget alloué : 284 octets)*

```diff
- Pas de [1432][NULL][NULL][0014]romantisme[1432][NULL][NULL][0014] sans [1432][NULL][NULL][0014]homme[1432][NULL][NULL][0014]!
- [1113]et moi on a pigé. Je dirai rien
- sur la boîte, sois tranquille!
+ Pas de [1432][NULL][NULL][0014]romantisme[1432][NULL][NULL][0014] sans [1432][NULL][NULL][0014]homme[1432][NULL][NULL][0014] !
+ [1113] et moi on a pigé. Je dirai rien
+ sur la boîte, sois tranquille !
```

### 🔹 `script_258.json` — ID 26 | **Concierge**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 252 octets)*

```diff
- Oh là là... La tour de l'horloge... Elle
- s'est effondrée... C'était pour le mieux...?
- J'espère que cet enseignant peut reposer en
- paix...
+ La tour de l'horloge s'est écroulée...
+ Était-ce un bien... ? J'espère que cet
+ enseignant repose en paix...
```

### 🔹 `script_260.json` — ID 7 | **Ginko**
- **Catégorie :** Nettoyage accident d'édition (texte parasite collé) *(Budget alloué : 236 octets)*

```diff
- Comme on disait! Les rumeurs se réalisent.[1205][001E]Youhou, 3000 yens de plus pour moi! Allons
- dîner, [1113]! Pierre Narurato Un mégalithe
- déterré à la construction du lycée. Fait de
- thamatite, il possède un magnétisme anormal.[E1][E2]
- La légende dit que c'est une pierre
- gardienne où l'être céleste Hiremon a scellé
- le démon Narurato Hotefu. Statue en
- l'honneur du directeur Hanya [NULL][NULL]Regardez-moi!
- Suivez-moi! Ne comptez pas sur moi![NULL][NULL] est
- lacitation contradictoire écrite ici. La
- regarder vous met étrangement en colère...
+ C'est comme on disait ! Les rumeurs
+ deviennent réalité.[1205][001E] Youhou, 3000 yens
+ en plus ! Allons dîner, [1113] !
```

### 🔹 `script_260.json` — ID 33 | **Lycéenne**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 130 octets)*

```diff
- Tu peux te reposer maintenant...
- Proviseur Hanya... *sniff*
+ Reposez en paix...
+ Proviseur Hanya... *snif*
```

### 🔹 `script_261.json` — ID 19 | **Toro l'informateur**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 246 octets)*

```diff
- Ouah...[1205][001E] Le directeur de Seven a
- poussé des cheveux? Je me demande
- si c'était sa requête pour Joker.
+ Ouah...[1205][001E] Le proviseur s'est vu pousser
+ des cheveux ? Serait-ce son vœu au Joker ?
```

### 🔹 `script_262.json` — ID 4 | **Lycéenne**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 292 octets)*

```diff
- Hein ? Mme Saeko ?[1205][001E] Je sais pas...
- Dans la salle des profs au deuxième
- étage ?[1205][001E] *soupir* Bien sûr que
- c'est pas moi que vous cherchez...
+ Mme Saeko ?[1205][001E] En salle des profs au
+ deuxième étage, peut-être ?[1205][001E] *soupir*
+ Évidemment, c'est pas moi que vous cherchez...
```

### 🔹 `script_263.json` — ID 22 | **Lycéenne**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 288 octets)*

```diff
- J'ai entendu que c'est le proviseur qui a
- levé la malédiction.[1205][000F] Mais le Boss a aussi
- fait sa part ![1205][000F] En remerciement, je lui ai
- donné mon premier baiser...
+ Le proviseur aurait levé le sort.[1205][000F] Mais
+ le Boss a aidé aussi ![1205][000F] Pour le remercier,
+ je lui ai donné mon premier baiser...
```

### 🔹 `script_264.json` — ID 11 | **Lycéenne blessée**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 256 octets)*

```diff
- C'est peut-être pareil pour ce Joker.
- Tu vois, vu qu'il porte un masque et
- que personne n'a jamais vu son visage.
+ C'est peut-être pareil pour Joker. Il a un
+ masque et personne n'a vu son visage.
```

### 🔹 `script_265.json` — ID 48 | **Lycéen**
- **Catégorie :** Nettoyage accident d'édition (texte parasite collé) *(Budget alloué : 172 octets)*

```diff
- Tu as détruit celui-là, [1112]-senpai. Maintenant
- va t'occuper des autres! Ce sont les restes
- d'une horloge qui était au mur... Il y a une
- horloge au mur avec l'emblème de l'école
- dessus.
+ Tu as détruit celui-là, [1112]-senpai.
+ Maintenant, va t'occuper des autres !
```

### 🔹 `script_266.json` — ID 16 | **Rédacteur du journal scolaire**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 296 octets)*

```diff
- Kozy est partie interviewer des élèves
- de Kakasu, donc je suis un peu inquiet.
- J'espère qu'elle n'est pas en danger..
+ Kozy interviewe des élèves de Kasu,
+ alors je m'inquiète un peu. Pourvu
+ qu'elle n'ait pas d'ennuis...
```

### 🔹 `script_267.json` — ID 2 | **Eikichi**
- **Catégorie :** Restauration d'opcode critique *(Budget alloué : 292 octets)*

```diff
- Ce principal se rapelle notre dernier
- combat, non? 5]non? Je me suis donné à
- fond... Je serais pas surpris si il m'en
- veut par rapport à ça.
+ Ce proviseur se rappelle notre combat,
+ non ?[1205][000F] Je ne retenais pas mes coups...
+ Pas étonnant s'il m'en veut pour ça.
```

### 🔹 `script_267.json` — ID 3 | **Ginko**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 272 octets)*

```diff
- Proviseur Hanya...[1205][000F] Qu'est ce qu'il se
- passe ici?? C'est le principal celui qui a
- vaincus les sbires du Batailon à cet étage?
+ Proviseur Hanya... ?[1205][000F] Que se passe-t-il ?[1205][000F]
+ C'est lui qui a étalé les sbires du
+ Dernier Bataillon par terre ?
```

### 🔹 `script_270.json` — ID 35 | **Lycéenne**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 272 octets)*

```diff
- *cri de joie*[1205][0008] La malédiction est levée ! Je
- suis trop de chance ![1205][000F] Et le proviseur
- partit, je vais pouvoir rentrer tard le soir
- !
+ *Youpi !*[1205][0008] La malédiction est levée ![1205][000F]
+ Et sans le proviseur, je vais pouvoir
+ traîner tard le soir !
```

### 🔹 `script_273.json` — ID 32 | **Mme Saeko**
- **Catégorie :** Restauration d'opcode critique *(Budget alloué : 152 octets)*

```diff
- Je suis désolée... Pourriez-vous me laisser
- seule un moment...?
+ Désolée...[1205][000A] Laissez-moi seule
+ un instant, je vous en prie...
```

### 🔹 `script_274.json` — ID 47 | **Mme Saeko**
- **Catégorie :** Restauration d'opcode critique *(Budget alloué : 152 octets)*

```diff
- Je suis désolée... Pourriez-vous me laisser
- seule un moment...?
+ Désolée...[1205][000A] Laissez-moi seule
+ un instant, je vous en prie...
```

### 🔹 `script_279.json` — ID 9 | **Ginko**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 68 octets)*

```diff
- Serait-ce...[1205][000F] ? Mais...
+ Serait-ce...[1205][000F] Mais...
```

### 🔹 `script_279.json` — ID 14 | **Ginko**
- **Catégorie :** Correction / Réécriture fidèle *(Budget alloué : 184 octets)*

```diff
- Cette pauvre fille... Elle attendait
- [1113]tout ce temps...[1205][000F] Toute seule...
+ Cette pauvre fille... Elle attendait
+ [1113] tout ce temps...[1205][000F] Toute seule...
```

### 🔹 `script_279.json` — ID 34 | **Vieille dame**
- **Catégorie :** Restauration d'opcode critique *(Budget alloué : 232 octets)*

```diff
- Le fantôme de la fille disparaît
- toujours dans le 205]le sanctuaire.
- Serait-ce lié à l'autre monde?
+ Le fantôme de la fille disparaît toujours
+ dans le sanctuaire.[1205][000F] Serait-il lié
+ à l'autre monde ?
```

### 🔹 `script_279.json` — ID 41 | **Vieille dame triste**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 292 octets)*

```diff
- Je me demande s'il est vraiment triste que
- nos petits-enfants ne viennent plus. Tu
- pourrais lui parler ? Il doit traîner
- quelque part en ville.
+ Serait-il triste que nos petits-enfants
+ ne viennent plus ? Va lui parler.
+ Il doit traîner quelque part en ville.
```

### 🔹 `script_281.json` — ID 87 | **Toku-san l'informateur**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 94 octets)*

```diff
- Ah, c'est vous. Bonjour.
+ Tiens, c'est vous !
```

### 🔹 `script_281.json` — ID 110 | **Toku-san l'informateur**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 242 octets)*

```diff
- J'ai entendu que les armures sont
- tendance cette année. Un provincial
- en parlait encore il y a peu.
+ L'armure serait tendance cette année.
+ Un provincial en parlait encore
+ il y a un instant.
```

### 🔹 `script_281.json` — ID 117 | **Toku-san l'informateur**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 260 octets)*

```diff
- Il semble que la prétention du patron
- à tout tailler, des armures aux
- robes de mariée, n'était pas vaine.
+ Le tailleur disait vrai : il conçoit de
+ tout, de l'armure aux robes de mariée.
```

### 🔹 `script_281.json` — ID 123 | **Toku-san l'informateur**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 148 octets)*

```diff
- Hm? Cercle masqué? Non, je
- n'en ai jamais entendu parler.
+ Le Cercle masqué ?
+ Non, jamais entendu parler.
```

### 🔹 `script_281.json` — ID 127 | **Toku-san l'informateur**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 302 octets)*

```diff
- De plus, les langues se délient. Ici, on
- entend ce que les gens pensent vraiment.
- Ainsi je connais l'état misérable du monde.
+ Ici les langues se délient. On entend ce
+ que pensent vraiment les gens. Je connais
+ bien l'état misérable de ce monde.
```

### 🔹 `script_281.json` — ID 167 | **Étudiant ennuyé**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 264 octets)*

```diff
- Il y a un gars nommé Tony dans le
- quartier commerçant de Yumezaki. [1205][000F]La
- rumeur dit qu'il est receleur de la Mafia.
+ Un certain Tony traîne au quartier
+ commerçant de Yumezaki.[1205][000F] Il serait
+ receleur pour la Mafia.
```

### 🔹 `script_281.json` — ID 170 | **Étudiant ennuyé**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 330 octets)*

```diff
- Il y avait une rumeur que le Cercle masqué
- était derrière les attentats, mais c'est
- vrai? [1205][000F]Sont-ils vraiment une
- organisationmaléfique...
+ On disait le Cercle masqué derrière ces attentats,
+ mais c'est vrai ?[1205][000F] Sont-ils vraiment
+ une organisation maléfique... ?
```

### 🔹 `script_281.json` — ID 177 | **Étudiant ennuyé**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 120 octets)*

```diff
- Je me demande ce qui le rend si sinistre.
+ Qu'est-ce qui le rend si sinistre ?
```

### 🔹 `script_281.json` — ID 181 | **Étudiant ennuyé**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 188 octets)*

```diff
- Mais quelle est la différence entre
- un taxi maudit et une escorte maudite?
+ Quelle est la différence entre un
+ taxi maudit et une escorte maudite ?
```

### 🔹 `script_281.json` — ID 225 | **Étudiant ennuyé**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 218 octets)*

```diff
- On peut jouer de l'argent au
- Mu à Yumezaki. Quelqu'un aurait
- décroché le jackpot au poker.
+ On parie de l'argent au Mu à Yumezaki.
+ Quelqu'un a raflé le jackpot au poker.
```

### 🔹 `script_281.json` — ID 226 | **Étudiant ennuyé**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 222 octets)*

```diff
- On peut jouer de l'argent au Mu
- à Yumezaki. Quelqu'un a décroché
- le jackpot aux machines à sous.
+ On parie de l'argent au Mu à Yumezaki.
+ Quelqu'un a raflé le gros lot aux machines.
```

### 🔹 `script_281.json` — ID 227 | **Étudiant ennuyé**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 222 octets)*

```diff
- On peut jouer de l'argent au
- Mu à Yumezaki. Quelqu'un aurait
- décroché le jackpot au blackjack.
+ On parie de l'argent au Mu à Yumezaki.
+ Quelqu'un a raflé le jackpot au blackjack.
```

### 🔹 `script_281.json` — ID 237 | **Étudiant ennuyé**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 286 octets)*

```diff
- Vous savez quoi ? J'ai entendu que les
- fleurs du parc d'Aoba peuvent parler. Paraît
- qu'elles sont comme des gens... Y'en a des
- bonnes et des mauvaises.
+ Tu sais quoi ? Les fleurs du parc d'Aoba
+ parleraient ! Il y en a des bonnes et
+ des mauvaises, tout comme nous.
```

### 🔹 `script_282.json` — ID 13 | **Lycéen**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 84 octets)*

```diff
- J-J'admire notre président. C'est lui qui
- a remis notre école sur pied alors qu'on
- était méprisés depuis si longtemps...
+ Ouais, bonne chance ! À plus !
```

### 🔹 `script_283.json` — ID 52 | **Ken**
- **Catégorie :** Correction / Réécriture fidèle *(Budget alloué : 222 octets)*

```diff
- Sauf qu'après ce qu'on a entendu
- sur [1113]au collège, on savait qu'il
- viendrait pas comme ça, donc...
+ Sauf qu'après ce qu'on a entendu
+ sur [1113] au collège, on savait qu'il
+ viendrait pas comme ça, donc...
```

### 🔹 `script_283.json` — ID 81 | **Eikichi**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 78 octets)*

```diff
- EIKICHI MISHINA, bon sang !
+ EIKICHI MISHINA, bordel !
```

### 🔹 `script_285.json` — ID 12 | **Toku-san l'informateur**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 258 octets)*

```diff
- Acceptes-tu de me partager les rumeurs
- que tu connais? En échange, je te
- partagerais celles que j'entend.
+ Tu veux bien me dire tes rumeurs ?
+ En échange, je te raconterai
+ celles que j'ai entendues.
```

### 🔹 `script_285.json` — ID 20 | **Toku-san l'informateur**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 244 octets)*

```diff
- Hm...[1205][001E] Les cheveux du proviseur
- de Seven ont soudainement poussé?
- Il a du demander ça au Joker.
+ Hm...[1205][001E] Le proviseur de Seven a des
+ cheveux ? Il a sans doute
+ demandé ça au Joker.
```

### 🔹 `script_285.json` — ID 21 | **Toku-san l'informateur**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 198 octets)*

```diff
- Bon, à moi alors. Tu vois le centre
- commercial Lotus qui est ici à Rengedai?
+ À mon tour. Tu connais le centre
+ commercial Lotus, ici à Rengedai ?
```

### 🔹 `script_285.json` — ID 23 | **Toku-san l'informateur**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 330 octets)*

```diff
- Il est assez suspect et s'exprime comme s'il
- pouvait voir à travers les gens. Il se fait
- même appeler Comte... Doncla rumeur ne
- m'étonne pas.
+ Il est louche et parle comme s'il lisait
+ en nous. Il se fait appeler Comte...
+ Cette rumeur ne m'étonne guère.
```

### 🔹 `script_285.json` — ID 24 | **Toku-san l'informateur**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 276 octets)*

```diff
- Hm? Un fantôme à l'horloge de Seven?
- Une histoire de fantômes d'écolier...
- Bon, d'accord. Voici une histoire à moi.
+ Hm ? Un fantôme à l'horloge de Seven ?
+ Une légende scolaire... Bon,
+ d'accord. À moi de raconter.
```

### 🔹 `script_285.json` — ID 26 | **Toku-san l'informateur**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 316 octets)*

```diff
- Je n'entend pas de très bonne rumeurs sur
- lui, tu sais. Certains disent même qu'il
- baigne dans le crime organisé. Peut-être,
- qui sait?
+ Les rumeurs sur lui ne sont pas tendres.
+ On dit qu'il trempe dans la pègre...
+ Qui sait, c'est peut-être vrai.
```

### 🔹 `script_285.json` — ID 29 | **Toku-san l'informateur**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 324 octets)*

```diff
- Aussi, le Garçon là-bas aurait chassé des
- voyous armés de couteaux, ajoutant qu'il
- aurait un fusil la prochainefois. Il n'est
- pas ordinaire.
+ Le Garçon aurait chassé des voyous armés
+ de couteaux, jurant de sortir le fusil la
+ prochaine fois. Pas banal, le gars.
```

### 🔹 `script_285.json` — ID 30 | **Toku-san l'informateur**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 306 octets)*

```diff
- Quoi? Ce producteur faisait partie du Cercle
- Masqué? Voilà une information bien utile. Je
- pense avoir une rumeur à la hauteur de ça.
+ Quoi ? Ce producteur est du Cercle masqué ?
+ Sacrée info. J'ai une rumeur qui
+ vaut bien ça en échange.
```

### 🔹 `script_285.json` — ID 37 | **Toku-san l'informateur**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 306 octets)*

```diff
- Il y a un salon secret au Zodiac? J'en ai
- entendu parler, mais le fait qu'il existe
- vraiment... Très bien. Voici ce que je sais.
+ Un salon secret au Zodiac ? J'en avais
+ ouï-dire, mais qu'il existe vraiment...
+ Bon, voici ce que je sais.
```

### 🔹 `script_285.json` — ID 43 | **Toku-san l'informateur**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 260 octets)*

```diff
- Il semble que le propriétaire affirmant
- pouvoir tout façonner, de l'armure
- à la robe de mariage, disait vrai.
+ Le tailleur disait vrai : il conçoit de
+ tout, de l'armure aux robes de mariée.
```

### 🔹 `script_285.json` — ID 44 | **Toku-san l'informateur**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 302 octets)*

```diff
- Tamaki de l'Agence de Détective Kuzunoha est
- une Devil Summoner? C'est un vrai métier?
- Jamais entendu parler... Hmm. Très bien.
+ Tamaki serait une Devil Summoner ?
+ Ça existe, ce métier ? Jamais
+ entendu parler... Bon, d'accord.
```

### 🔹 `script_285.json` — ID 46 | **Toku-san l'informateur**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 310 octets)*

```diff
- Ah... Donc les démons existent pour de vrai?[1205][001E]
- Voilà qui est farfelu. Je pense plutôt que
- le mal se terre dans le coeur des gens.
+ Ah... Les démons existent pour de vrai ?
+ [1205][001E]C'est bien tiré par les cheveux.
+ Le mal naît plutôt du cœur des gens.
```

### 🔹 `script_285.json` — ID 47 | **Toku-san l'informateur**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 188 octets)*

```diff
- Bon, à mon tour alors. Connais-tu
- la salle d'arcade Mu, à Yumezaki?
+ À mon tour. Tu connais la salle
+ d'arcade Mu, à Yumezaki ?
```

### 🔹 `script_285.json` — ID 49 | **Toku-san l'informateur**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 192 octets)*

```diff
- Hein? Le Bataillon est mené par le
- Führer? [1205][000F]Est-ce seulement possible?
+ Le Bataillon est mené par le Führer ?
+ [1205][000F]C'est possible, ça ?
```

### 🔹 `script_285.json` — ID 54 | **Toku-san l'informateur**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 246 octets)*

```diff
- Chaque histoire étrange se révèle
- vraie. Elles se répandent plus
- vite que des rumeurs ordinaires.
+ Ces histoires folles sont vraies.
+ C'est du bouche-à-oreille plutôt
+ que de simples rumeurs.
```

### 🔹 `script_285.json` — ID 56 | **Toku-san l'informateur**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 326 octets)*

```diff
- Ce sont les rumeurs que je connais. Je t'en
- dirais plus quand j'en aurais d'autres.
- Assure-toi d'avoir desinformations
- alléchantes pour moi!
+ C'est tout ce que je sais. Je t'en dirai
+ plus si j'en apprends. Prépare-moi de
+ bonnes infos la prochaine fois !
```

### 🔹 `script_285.json` — ID 57 | **Toku-san l'informateur**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 242 octets)*

```diff
- Je vois. Reviens ici si tu veux
- entendre mes rumeurs. Je serais
- toujours là, à regarder le ciel.
+ Je vois. Reviens pour d'autres rumeurs.
+ Je serai toujours là, les yeux
+ tournés vers le ciel.
```

### 🔹 `script_286.json` — ID 60 | **Père de Ginko**
- **Catégorie :** Nettoyage accident d'édition (texte parasite collé) *(Budget alloué : 210 octets)*

```diff
- Le tirage au sort, vous dites? Ah, oui, bien
- sûr. On vous l'a livré ici. Allez,
- prenez-le. Lettre [NULL][NULL]Merci de votre
- participation au tirage. Hélas, vous n'êtes
- pas gagnant cettefois. Nous vous
- encourageons à continuer![NULL][NULL]
+ Le tirage au sort ? Ah, oui, bien sûr.
+ On l'a reçu ici. Tenez, prenez-le.
```

### 🔹 `script_286.json` — ID 61 | **Père de Ginko**
- **Catégorie :** Nettoyage accident d'édition (texte parasite collé) *(Budget alloué : 210 octets)*

```diff
- Le tirage au sort, vous dites? Ah, oui, bien
- sûr. On vous l'a livré ici. Allez,
- prenez-le. Lettre [NULL][NULL]Merci de votre
- participation au tirage. Félicitations! Vous
- avez étésélectionné comme gagnant! [NULL][NULL]Veuillez
- accepter [E4][NULL][NULL][NULL][E4][NULL][NULL] en guise de prix. Continuez à
- participer![NULL][NULL] Vous n'avez pas de place pour
- un(e) autre [E4][NULL][NULL][NULL][E4][NULL][NULL]...
+ Le tirage au sort ? Ah, oui, bien sûr.
+ On l'a reçu ici. Tenez, prenez-le.
```

### 🔹 `script_286.json` — ID 80 | **Père de Ginko**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 288 octets)*

```diff
- C'est la maison de ma famille. Quiconque la
- menace, le chef de famille doit la défendre.
- Je... veux que vous protégiez ma fille.
+ C'est le foyer de ma famille. Quiconque le
+ menace, le chef doit le protéger.
+ Je... veux que vous protégiez ma fille.
```

### 🔹 `script_287.json` — ID 20 | **Père de Ginko**
- **Catégorie :** Nettoyage accident d'édition (texte parasite collé) *(Budget alloué : 210 octets)*

```diff
- Le tirage au sort, vous dites? Ah, oui, bien
- sûr. On vous l'a livré ici. Allez,
- prenez-le. Lettre [NULL][NULL]Merci de votre
- participation au tirage. Hélas, vous n'êtes
- pas gagnant cettefois. Nous vous
- encourageons à continuer![NULL][NULL]
+ Le tirage au sort ? Ah, oui, bien sûr.
+ On vous l'a livré ici. Tenez, prenez-le.
```

### 🔹 `script_287.json` — ID 21 | **Père de Ginko**
- **Catégorie :** Nettoyage accident d'édition (texte parasite collé) *(Budget alloué : 210 octets)*

```diff
- Le tirage au sort, vous dites? Ah, oui, bien
- sûr. On vous l'a livré ici. Allez,
- prenez-le. Lettre [NULL][NULL]Merci de votre
- participation au tirage. Félicitations! Vous
- avez étésélectionné comme gagnant! [NULL][NULL]Veuillez
- accepter [E4][NULL][NULL][NULL][E4][NULL][NULL] en guise de prix. Continuez à
- participer![NULL][NULL] Vous n'avez pas de place pour
- un(e) autre [E4][NULL][NULL][NULL][E4][NULL][NULL]...
+ Le tirage au sort ? Ah, oui, bien sûr.
+ On vous l'a livré ici. Tenez, prenez-le.
```

### 🔹 `script_287.json` — ID 24 | **Père de Ginko**
- **Catégorie :** Restauration d'opcode critique *(Budget alloué : 314 octets)*

```diff
- Je ne peux plus retenir ma fille à ce stade.
- C'est ]C'est pourquoi je voudrais vous
- confier sa sécurité. Veuillez veiller sur
- Lisa à maplace.
+ Je ne peux plus retenir ma fille.[1205][000F]
+ C'est pourquoi je vous la confie.
+ Veillez sur Lisa à ma place.
```

### 🔹 `script_287.json` — ID 28 | **Père de Ginko**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 318 octets)*

```diff
- J'ai entendu que quelqu'un était intervenu
- pour sauver les élèves de Seven Sisters
- High.[1205][000F] Il reste donc des gens à Sumaru prêts
- à se battre...
+ Quelqu'un a sauvé les élèves de Seven
+ Sisters High ?[1205][000F] Il reste donc des gens
+ prêts à se battre à Sumaru...
```

### 🔹 `script_288.json` — ID 27 | **Maya**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 388 octets)*

```diff
- Ceux qui ont oublié leur passé réalisent,
- via l'In Lak'ech, leur expiation destinée.[E1][E2]
- [E3][E4][NULL][NULL]"Maya Héhé... T'es pas d'accord, [1113]-kun?
+ Ceux qui oublient leur passé réalisent,
+ via l'In Lak'ech, leur expiation.[E1][E2]
+ [E3][E4][NULL][NULL]"Maya
+ Héhé... Pas vrai, [1113]-kun ?
```

### 🔹 `script_288.json` — ID 39 | **Comte**
- **Catégorie :** Nettoyage accident d'édition (texte parasite collé) *(Budget alloué : 326 octets)*

```diff
- Et que voudriez-vous vendre?
- [1208][0007][111F][1210][B_00][U+5501][B_00]Sélection cachée
- [111F]Objets
- [111F]Armes[SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP]
- [111F][1210][B_00][U+5301][B_00]Armure de tête
- [111F]Armure[SP][SP][SP][SP][SP][SP][SP]
- [111F][1210][B_00][U+5301][B_00]Jambes[SP][SP][SP][SP][SP][SP]
- [111F]Accessoires[B_00][5501][B_00][B_00][5301][B_00][B_00][5301][B_00]
+ Et que voudriez-vous vendre ?
+ [1208][0007][111F][1210][B_00][U+5501][B_00]Sélection cachée
+ [111F]Objets
+ [111F]Armes
+ [111F][1210][B_00][U+5301][B_00]Armure de tête
+ [111F]Armure
+ [111F][1210][B_00][U+5301][B_00]Jambes
+ [111F]Accessoires[B_00][5501][B_00][B_00][5301][B_00][B_00][5301][B_00]
```

### 🔹 `script_288.json` — ID 92 | **Comte**
- **Catégorie :** Nettoyage accident d'édition (texte parasite collé) *(Budget alloué : 330 octets)*

```diff
- Et que voudriez-vous vendre?
- [1208][0007][111F][1210][B_00][U+5501][B_00]Sélection cachée
- [111F]Objets
- [111F]Armes[SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP]
- [111F][1210][B_00][U+5301][B_00]Armure de tête
- [111F]Sell armor[SP][SP][SP]
- [111F][1210][B_00][U+1001][U+0012][U+5301][B_00]Jambes[SP][SP][SP][SP][SP][SP]
- [111F]Accessoires[B_00][5501][B_00][B_00][5301][B_00][B_00][1001][0012][5301][B_00]
+ Et que voudriez-vous vendre ?
+ [1208][0007][111F][1210][B_00][U+5501][B_00]Sélection cachée
+ [111F]Objets
+ [111F]Armes
+ [111F][1210][B_00][U+5301][B_00]Armure de tête
+ [111F]Armure
+ [111F][1210][B_00][U+1001][U+0012][U+5301][B_00]Jambes
+ [111F]Accessoires[B_00][5501][B_00][B_00][5301][B_00][B_00][1001][0012][5301][B_00]
```

### 🔹 `script_289.json` — ID 13 | **Comte**
- **Catégorie :** Nettoyage accident d'édition (texte parasite collé) *(Budget alloué : 326 octets)*

```diff
- Et que voudriez-vous vendre?
- [1208][0007][111F][1210][B_00][U+5501][B_00]Sélection cachée
- [111F]Objets
- [111F]Armes[SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP]
- [111F][1210][B_00][U+5301][B_00]Armure de tête
- [111F]Armure[SP][SP][SP][SP][SP][SP][SP]
- [111F][1210][B_00][U+5301][B_00]Jambes[SP][SP][SP][SP][SP][SP]
- [111F]Accessoires[B_00][5501][B_00][B_00][5301][B_00][B_00][5301][B_00]
+ Et que voudriez-vous vendre ?
+ [1208][0007][111F][1210][B_00][U+5501][B_00]Sélection cachée
+ [111F]Objets
+ [111F]Armes
+ [111F][1210][B_00][U+5301][B_00]Armure de tête
+ [111F]Armure
+ [111F][1210][B_00][U+5301][B_00]Jambes
+ [111F]Accessoires[B_00][5501][B_00][B_00][5301][B_00][B_00][5301][B_00]
```

### 🔹 `script_289.json` — ID 37 | **Comte**
- **Catégorie :** Nettoyage accident d'édition (texte parasite collé) *(Budget alloué : 330 octets)*

```diff
- Et que voudriez-vous vendre?
- [1208][0007][111F][1210][B_00][U+5501][B_00]Sélection cachée
- [111F]Objets
- [111F]Armes[SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP]
- [111F][1210][B_00][U+5301][B_00]Armure de tête
- [111F]Sell armor[SP][SP][SP]
- [111F][1210][B_00][U+1001][U+0012][U+5301][B_00]Jambes[SP][SP][SP][SP][SP][SP]
- [111F]Accessoires[B_00][5501][B_00][B_00][5301][B_00][B_00][1001][0012][5301][B_00]
+ Et que voudriez-vous vendre ?
+ [1208][0007][111F][1210][B_00][U+5501][B_00]Sélection cachée
+ [111F]Objets
+ [111F]Armes
+ [111F][1210][B_00][U+5301][B_00]Armure de tête
+ [111F]Armure
+ [111F][1210][B_00][U+1001][U+0012][U+5301][B_00]Jambes
+ [111F]Accessoires[B_00][5501][B_00][B_00][5301][B_00][B_00][1001][0012][5301][B_00]
```

### 🔹 `script_290.json` — ID 81 | **Membre du Cercle masqué**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 264 octets)*

```diff
- Ouais, je suis du Cercle masqué. Une
- de ces effrayantes personnes du Cercle
- masqué! Ça te pose un problème!?
+ Ouais, je suis du Cercle masqué.
+ Un de ces membres si effrayants !
+ Ça te pose un problème !?
```

### 🔹 `script_290.json` — ID 82 | **Membre du Cercle masqué**
- **Catégorie :** Correction / Réécriture fidèle *(Budget alloué : 274 octets)*

```diff
- Le trésor secret de Sumaru...[1205][000F] Xibalba...
- Il nous transformera en Idéaliens
- et nous apprendra le sens de la vie!
+ Le trésor de Sumaru...[1205][000F] Xibalba...[1205][000F]
+ Il fera de nous des Idéaliens et nous
+ apprendra le sens de la vie !
```

### 🔹 `script_290.json` — ID 83 | **Membre du Cercle masqué**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 274 octets)*

```diff
- Oui, ce livre est totalement vrai! Un
- autre de mes idéaux sera exaucé! Je...
- Je veux savoir qui je suis vraiment!
+ Oui, ce livre dit vrai ! Un autre de mes
+ idéaux sera exaucé ! Je... Je veux savoir
+ qui je suis vraiment !
```

### 🔹 `script_295.json` — ID 51 | **Mlle Kaori**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 282 octets)*

```diff
- Et aujourd'hui, le parfum de la fleur
- légendaire... Éphémère, mais toujours
- présente. Son souffle vous donne la force de
- survivre...
+ Aujourd'hui, le parfum de la fleur
+ légendaire... Fugace, mais éternel.
+ Son souffle donne la force de survivre...
```

### 🔹 `script_296.json` — ID 94 | **Igor**
- **Catégorie :** Calibrage menu à choix *(Budget alloué : 290 octets)*

```diff
- Je vous écoute.
- [1208][0007]Bases d'invocation
- Changement mystique
- Mutation
- Contact
- Personnalité des démons
- Page préc.
- [1210][B_00][U+5501][B_00]Sélection cachée/retour[SP][SP][SP][SP]
+ Je vous écoute.
+ [1208][0007]Bases d'invocation
+ Changement mystique
+ Mutation
+ Contact
+ Personnalité des démons
+ Page préc.
+ [1210][B_00][U+5501][B_00]Choix caché/retour
```

### 🔹 `script_296.json` — ID 310 | **Igor**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 212 octets)*

```diff
- Je vais changer cet aspect qui
- a combattu à vos côtés en un [E4][NULL][NULL][0004][120E][0001][121D][0001]
- et vous le rendre... obtient [E4][NULL][NULL].
+ Je vais transformer cet aspect
+ qui a combattu à vos côtés en [E4][NULL][NULL][0004][120E][0001][121D][0001]
+ et vous le rendre...
```

### 🔹 `script_296.json` — ID 316 | **Igor**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 188 octets)*

```diff
- Il semble que vous n'ayez pas la [E4][NULL][NULL][0006]Carte
- Matériaux[E4][NULL][NULL][0002] requise pour invoquer ce Persona.
+ Vous n'avez pas la [E4][NULL][NULL][0006]Carte Matériaux[E4][NULL][NULL][0002]
+ requise pour invoquer ce Persona.
```

### 🔹 `script_300.json` — ID 19 | **Yukino**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 102 octets)*

```diff
- On ferait mieux d'aller les
- rejoindre.[1205][000F] Allez, on y va.
+ Suivons-les.[1205][000F] Allez, on y va.
```

### 🔹 `script_311.json` — ID 53 | **Patronne**
- **Catégorie :** Nettoyage accident d'édition (texte parasite collé) *(Budget alloué : 288 octets)*

```diff
- Tu vends quoi?
- [1208][0007][1210][B_00][U+5501][B_00]Sélection cachée
- Objets
- Armes[SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP]
- [1210][B_00][U+5301][B_00]Armure de tête
- Sell armor[SP][SP][SP]
- [1210][B_00][U+5301][B_00]Jambes[SP][SP][SP][SP][SP][SP]
- Accessoires[B_00][5501][B_00][B_00][5301][B_00][B_00][5301][B_00]
+ Tu vends quoi ?
+ [1208][0007][1210][B_00][U+5501][B_00]Sélection cachée
+ Objets
+ Armes
+ [1210][B_00][U+5301][B_00]Armure de tête
+ Armure
+ [1210][B_00][U+5301][B_00]Jambes
+ Accessoires[B_00][5501][B_00][B_00][5301][B_00][B_00][5301][B_00]
```

### 🔹 `script_311.json` — ID 56 | **Patronne**
- **Catégorie :** Nettoyage accident d'édition (texte parasite collé) *(Budget alloué : 288 octets)*

```diff
- Tu vends quoi?
- [1208][0007][1210][B_00][U+5501][B_00]Sélection cachée
- Objets
- Armes[SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP]
- [1210][B_00][U+5301][B_00]Armure de tête
- Sell armor[SP][SP][SP]
- [1210][B_00][U+5301][B_00]Jambes[SP][SP][SP][SP][SP][SP]
- Accessoires[B_00][5501][B_00][B_00][5301][B_00][B_00][5301][B_00]
+ Tu vends quoi ?
+ [1208][0007][1210][B_00][U+5501][B_00]Sélection cachée
+ Objets
+ Armes
+ [1210][B_00][U+5301][B_00]Armure de tête
+ Armure
+ [1210][B_00][U+5301][B_00]Jambes
+ Accessoires[B_00][5501][B_00][B_00][5301][B_00][B_00][5301][B_00]
```

### 🔹 `script_312.json` — ID 9 | **Patronne**
- **Catégorie :** Nettoyage accident d'édition (texte parasite collé) *(Budget alloué : 302 octets)*

```diff
- Tu vends quoi?
- [1208][0007][111F][1210][B_00][U+5501][B_00]Sélection cachée
- [111F]Objets
- [111F]Armes[SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP]
- [111F][1210][B_00][U+5301][B_00]Armure de tête
- [111F]Armure[SP][SP][SP][SP][SP][SP][SP]
- [111F][1210][B_00][U+5301][B_00]Jambes[SP][SP][SP][SP][SP][SP]
- [111F]Accessoires[B_00][5501][B_00][B_00][5301][B_00][B_00][5301][B_00]
+ Tu vends quoi?
+ [1208][0007][111F][1210][B_00][U+5501][B_00]Sélection cachée
+ [111F]Objets
+ [111F]Armes
+ [111F][1210][B_00][U+5301][B_00]Armure de tête
+ [111F]Armure
+ [111F][1210][B_00][U+5301][B_00]Jambes
+ [111F]Accessoires[B_00][5501][B_00][B_00][5301][B_00][B_00][5301][B_00]
```

### 🔹 `script_312.json` — ID 12 | **Patronne**
- **Catégorie :** Nettoyage accident d'édition (texte parasite collé) *(Budget alloué : 302 octets)*

```diff
- Tu vends quoi?
- [1208][0007][111F][1210][B_00][U+5501][B_00]Sélection cachée
- [111F]Objets
- [111F]Armes[SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP]
- [111F][1210][B_00][U+5301][B_00]Armure de tête
- [111F]Armure[SP][SP][SP][SP][SP][SP][SP]
- [111F][1210][B_00][U+5301][B_00]Jambes[SP][SP][SP][SP][SP][SP]
- [111F]Accessoires[B_00][5501][B_00][B_00][5301][B_00][B_00][5301][B_00]
+ Tu vends quoi?
+ [1208][0007][111F][1210][B_00][U+5501][B_00]Sélection cachée
+ [111F]Objets
+ [111F]Armes
+ [111F][1210][B_00][U+5301][B_00]Armure de tête
+ [111F]Armure
+ [111F][1210][B_00][U+5301][B_00]Jambes
+ [111F]Accessoires[B_00][5501][B_00][B_00][5301][B_00][B_00][5301][B_00]
```

### 🔹 `script_312.json` — ID 34 | **Patronne**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 108 octets)*

```diff
- Hein? La parole d'un ex-espion suffit pas?
+ Quoi ? Tu doutes d'une ex-espionne ?
```

### 🔹 `script_312.json` — ID 38 | **Patronne**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 198 octets)*

```diff
- Mais j'ai galéré à l'avoir. Forcément, elle
- a son prix. Donc j'ai une offre pour toi...
+ Mais j'ai peiné à l'avoir. Hors de question
+ de la brader. Voici ma proposition...
```

### 🔹 `script_312.json` — ID 48 | **Patronne**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 44 octets)*

```diff
- Et voici.
+ Voilà.
```

### 🔹 `script_312.json` — ID 51 | **Eikichi**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 152 octets)*

```diff
- ... D'accord...[1205][000F] Bah, ça change rien... Bien,
- c'est parti![E3] Eikichi mange...[E2][E1][E2] [E3][E4][NULL][NULL]"Eikichi J'ai
- fini... le Ramen... au Yaourt... Beuurp...!
+ ... Très bien...[1205][000F] Ça ne change rien...[1205][000F]
+ Allez, c'est parti !
```

### 🔹 `script_312.json` — ID 52 | **Eikichi**
- **Catégorie :** Correction / Réécriture fidèle *(Budget alloué : 124 octets)*

```diff
- Alors?[1205][000F] Un avis?
+ Fini...[1205][000F] ce ramen...[1205][000F] au yaourt...[1205][000F]
+ Beurp... !
```

### 🔹 `script_312.json` — ID 53 | **Patronne**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 58 octets)*

```diff
- Alors? [1205][000F]Un avis?
+ Alors ?[1205][000F] Bon ?
```

### 🔹 `script_312.json` — ID 66 | **Patronne**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 64 octets)*

```diff
- C'est presque tout.
+ Ça suffira.
```

### 🔹 `script_313.json` — ID 33 | **Maya**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 514 octets)*

```diff
- Peut-on réfuter la logique de Mme Ideal?
- [1205][000F]Vous aussi vous intervertissez rêves et
- réalité à votre avantage...[E1][E2] [E3][E4][NULL][NULL]"Maya Chacun
- prétend souhaiter la paix, mais
- peut-êtrequ'inconsciemment on souhaite tout
- détruire pour pouvoir repartir de zéro.
+ Réfuter la logique de Mme Idéal ?[1205][000F]
+ On troque rêves et réalité selon
+ son bon plaisir...[E1][E2][E3][E4][NULL][NULL]"Maya
+ Chacun veut la paix, mais au fond,
+ on rêve peut-être de tout raser pour
+ repartir de zéro.
```

### 🔹 `script_313.json` — ID 47 | **Siffleur**
- **Catégorie :** Nettoyage accident d'édition (texte parasite collé) *(Budget alloué : 318 octets)*

```diff
- Qu'est-ce que t'as pour moi?
- [1208][0007][111F][1210][B_00][U+5501][B_00]Sélection cachée
- [111F]Objets
- [111F]Armes[SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP]
- [111F][1210][B_00][U+5301][B_00]Armure de tête
- [111F]Armure[SP][SP][SP][SP][SP][SP][SP]
- [111F][1210][B_00][U+5301][B_00]Jambes[SP][SP][SP][SP][SP][SP]
- [111F]Accessoires[B_00][5501][B_00][B_00][5301][B_00][B_00][5301][B_00]
+ Qu'est-ce que t'as pour moi ?
+ [1208][0007][111F][1210][B_00][U+5501][B_00]Sélection cachée
+ [111F]Objets
+ [111F]Armes
+ [111F][1210][B_00][U+5301][B_00]Armure de tête
+ [111F]Armure
+ [111F][1210][B_00][U+5301][B_00]Jambes
+ [111F]Accessoires[B_00][5501][B_00][B_00][5301][B_00][B_00][5301][B_00]
```

### 🔹 `script_313.json` — ID 72 | **Membre du Cercle masqué**
- **Catégorie :** Restauration d'opcode critique *(Budget alloué : 364 octets)*

```diff
- Ggggn... Aaagh... Uaagh...[E1][E2] [E3][E4][NULL][NULL]"Pas une femme
- Haha... Toute ma vie on m'a dénigré car
- j'étais trop masculin, maisc'est fini! Je
- suis enfin un homme!
+ Ggggn... Aaagh...[1205][000A] Uaagh...[E1][E2][E3][E4][NULL][NULL]"Femme bizarre
+ Haha... On m'a rabaissé toute ma vie
+ car j'étais virile, mais c'est fini !
+ Je suis enfin un homme !
```

### 🔹 `script_313.json` — ID 78 | **Pas une femme**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 484 octets)*

```diff
- Quand je pense avoir trouvé de bons amis,
- leur bite prend le contrôle et ils me font
- des avances. [E4][NULL][NULL]"Femme bizarre [1205][000F]Pas une
- femmePuis quand j'ai dit non, ces [1432][NULL][NULL][0014]amis[1432][NULL][NULL][0014] sont
- devenus distants... C'est ce qui me
- débectais le plus.
+ À peine amis, ils ne pensaient
+ qu'à coucher avec moi.
+ [1205][000F]
+ [E4][NULL][NULL]"Femme bizarre
+ Et à mon refus, ces [1432][NULL][NULL][0014]amis[1432][NULL][NULL][0014] devenaient
+ glaciaux...[1205][000F] C'est ce qui m'écœurait
+ le plus.
```

### 🔹 `script_313.json` — ID 92 | **Siffleur**
- **Catégorie :** Nettoyage accident d'édition (texte parasite collé) *(Budget alloué : 318 octets)*

```diff
- Qu'est-ce que t'as pour moi?
- [1208][0007][111F][1210][B_00][U+5501][B_00]Sélection cachée
- [111F]Objets
- [111F]Armes[SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP]
- [111F][1210][B_00][U+5301][B_00]Armure de tête
- [111F]Armure[SP][SP][SP][SP][SP][SP][SP]
- [111F][1210][B_00][U+5301][B_00]Jambes[SP][SP][SP][SP][SP][SP]
- [111F]Accessoires[B_00][5501][B_00][B_00][5301][B_00][B_00][5301][B_00]
+ Qu'est-ce que t'as pour moi ?
+ [1208][0007][111F][1210][B_00][U+5501][B_00]Sélection cachée
+ [111F]Objets
+ [111F]Armes
+ [111F][1210][B_00][U+5301][B_00]Armure de tête
+ [111F]Armure
+ [111F][1210][B_00][U+5301][B_00]Jambes
+ [111F]Accessoires[B_00][5501][B_00][B_00][5301][B_00][B_00][5301][B_00]
```

### 🔹 `script_314.json` — ID 9 | **Siffleur**
- **Catégorie :** Nettoyage accident d'édition (texte parasite collé) *(Budget alloué : 318 octets)*

```diff
- Qu'est-ce que t'as pour moi?
- [1208][0007][111F][1210][B_00][U+5501][B_00]Sélection cachée
- [111F]Objets
- [111F]Armes[SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP]
- [111F][1210][B_00][U+5301][B_00]Armure de tête
- [111F]Armure[SP][SP][SP][SP][SP][SP][SP]
- [111F][1210][B_00][U+5301][B_00]Jambes[SP][SP][SP][SP][SP][SP]
- [111F]Accessoires[B_00][5501][B_00][B_00][5301][B_00][B_00][5301][B_00]
+ Qu'est-ce que t'as pour moi ?
+ [1208][0007][111F][1210][B_00][U+5501][B_00]Sélection cachée
+ [111F]Objets
+ [111F]Armes
+ [111F][1210][B_00][U+5301][B_00]Armure de tête
+ [111F]Armure
+ [111F][1210][B_00][U+5301][B_00]Jambes
+ [111F]Accessoires[B_00][5501][B_00][B_00][5301][B_00][B_00][5301][B_00]
```

### 🔹 `script_314.json` — ID 17 | **Siffleur**
- **Catégorie :** Nettoyage accident d'édition (texte parasite collé) *(Budget alloué : 318 octets)*

```diff
- Qu'est-ce que t'as pour moi?
- [1208][0007][111F][1210][B_00][U+5501][B_00]Sélection cachée
- [111F]Objets
- [111F]Armes[SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP]
- [111F][1210][B_00][U+5301][B_00]Armure de tête
- [111F]Armure[SP][SP][SP][SP][SP][SP][SP]
- [111F][1210][B_00][U+5301][B_00]Jambes[SP][SP][SP][SP][SP][SP]
- [111F]Accessoires[B_00][5501][B_00][B_00][5301][B_00][B_00][5301][B_00]
+ Qu'est-ce que t'as pour moi ?
+ [1208][0007][111F][1210][B_00][U+5501][B_00]Sélection cachée
+ [111F]Objets
+ [111F]Armes
+ [111F][1210][B_00][U+5301][B_00]Armure de tête
+ [111F]Armure
+ [111F][1210][B_00][U+5301][B_00]Jambes
+ [111F]Accessoires[B_00][5501][B_00][B_00][5301][B_00][B_00][5301][B_00]
```

### 🔹 `script_317.json` — ID 29 | **Maya**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 326 octets)*

```diff
- Hahaha...[1205][000F] Pas de soucis. Sumaru croira en
- l'In Lak'ech bientôt.[E1][E2] [E3][E4][NULL][NULL]"Maya Bientôt, les
- prophéties de ce livre deviendront réalité.
+ Hahaha...[1205][000F] Pas d'inquiétude. Sumaru
+ croira bientôt en l'In Lak'ech.
+ [E1][E2]
+ [E3][E4][NULL][NULL]"Maya
+ Bientôt, ses prophéties se réaliseront.
```

### 🔹 `script_317.json` — ID 98 | **Vieil homme guéri**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 266 octets)*

```diff
- Attendez, ces soldats ne font pas partie
- du Cercle Masqué ?[1205][000F] Ça pourrait poser
- problème...[1205][000F] On est peut-être dans le pétrin.
+ Ces soldats ne sont pas du Cercle
+ Masqué ?[1205][000F] C'est mauvais...[1205][000F] On a des
+ ennuis après tout.
```

### 🔹 `script_318.json` — ID 33 | **Vieil homme guéri**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 296 octets)*

```diff
- Tout le monde trouve le bonheur dans quelque
- chose de différent.[1205][000F] Même si on devient
- ces Ide..., ça plaira pas à tout le monde.
+ Chacun trouve son bonheur à sa façon.[1205][000F]
+ Même changés en ces « Idé... » machins,
+ ça n'ira pas à tout le monde.
```

### 🔹 `script_319.json` — ID 182 | **Chef Todoroki**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 110 octets)*

```diff
- Vous n'avez pas les moyens
- pour mes honoraires.
+ Vous n'avez pas de quoi me payer.
```

### 🔹 `script_320.json` — ID 83 | **Chef Todoroki**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 110 octets)*

```diff
- Vous n'avez pas les moyens
- pour mes honoraires.
+ Vous n'avez pas de quoi me payer.
```

### 🔹 `script_321.json` — ID 112 | **Chef Todoroki**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 110 octets)*

```diff
- Vous n'avez pas les moyens
- pour mes honoraires.
+ Vous n'avez pas de quoi me payer.
```

### 🔹 `script_324.json` — ID 12 | **Eikichi**
- **Catégorie :** Restauration d'opcode critique *(Budget alloué : 296 octets)*

```diff
- Pff... Voilà pourquoi la fille kung-fu
- attire les 05]les ennuis. Même un gosse
- devinerait que la prochaine cible est le
- bâtiment Sakanoue.
+ Pff... Voilà pourquoi la fille kung-fu
+ attire les ennuis.[1205][000F] Même un gosse verrait
+ que la cible est le bâtiment Sakanoue.
```

### 🔹 `script_324.json` — ID 53 | **Maya**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 794 octets)*

```diff
- Ma pauvre. [1205][000F]Je sais. Tu veux désespérément
- enfouir tes souvenirs du passé qui veulent
- refaire surface...[E1][E2] [E3][E4][NULL][NULL]"Maya C'est pour ça que
- tu angoisses. Mais une fois ces
- souvenirslibérés, tu seras libre de tes
- souffrances.[E1][E2] [E3][E4][NULL][NULL]"Maya Maintenant, allons tout
- nous rappeler. Héhé...[E1][E2] [E3][E4][NULL][NULL]"Maya Où Fujii-san
- pourrait-il être au Mont Katatsumuri...? Je
- me demande si Yukki aune idée.
+ Ma pauvre...[1205][000F] Tu veux enfouir tes
+ souvenirs qui refont surface...
+ [E1][E2]
+ [E3][E4][NULL][NULL]"Maya
+ Tu angoisses,[1205][000F] mais une fois libérés, tu
+ ne souffriras plus.
+ [E1][E2]
+ [E3][E4][NULL][NULL]"Maya
+ Allons nous rappeler de tout.[1205][000F] Héhé...
+ [E1][E2]
+ [E3][E4][NULL][NULL]"Maya
+ Où Fujii-san peut-il être sur le Mont
+ Katatsumuri... ? Yukki a une idée ?
```

### 🔹 `script_324.json` — ID 151 | **Toro l'informateur**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 302 octets)*

```diff
- Ouah, le Boss de Lycée Kakasu veut créer un
- groupe? Et il va être le chanteur? Hahaha,
- ça semble être un scénario plutôt commun.
+ Ouah, le Boss du Lycée Kakasu monte un
+ groupe ? Et il chantera ? Hahaha,
+ un scénario plutôt classique.
```

### 🔹 `script_325.json` — ID 136 | **Père d'Eikichi**
- **Catégorie :** Calibrage menu à choix *(Budget alloué : 92 octets)*

```diff
- Ça fait [120E][NULL] yens !
- [1208][0002]Oui
- Non
+ Ça fait [120E][NULL] yens !
+ [1208][0002]OK
+ Non
```

### 🔹 `script_326.json` — ID 85 | **Gérant**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 204 octets)*

```diff
- Ils nettoient devant. Hein ? Tu
- penses qu'on nettoie toujours ce
- coin ? W-Wow... T'es perspicace...
+ Vous devez avoir fort à faire,
+ mais repassez me voir. Je vous
+ accueillerai avec plaisir.
```

### 🔹 `script_327.json` — ID 9 | **Joueur invétéré**
- **Catégorie :** Restauration d'opcode critique *(Budget alloué : 318 octets)*

```diff
- Le Bataillon... Un vrai joker dans la
- partie. L'enjeu, 00F]L'enjeu, c'est toute la
- ville... Ce qui décidera du sort de
- Sumaru... les cartes...
+ Le Dernier Bataillon... Un vrai joker.
+ L'enjeu,[1205][000F] c'est la ville entière... Le sort
+ de Sumaru se jouera aux cartes...
```

### 🔹 `script_327.json` — ID 18 | **Gérant**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 204 octets)*

```diff
- Ils font du nettoyage là-bas. Hein?
- Vous croyez que c'est toujours comme
- ça? Étonnant... Vous êtes fort...
+ Vous avez sans doute fort à faire,
+ mais revenez. Je vous accueillerai
+ avec plaisir.
```

### 🔹 `script_332.json` — ID 39 | **Maya**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 528 octets)*

```diff
- C'est le rêve éternel de l'homme de devenir
- un Idéalien. Seul Xibalba le peut. Tous
- espèrent son avènement.[E1][E2] [E3][E4][NULL][NULL]"Maya Joker... Enfin
- Jun-kun, prépare un truc au Mt.
- Katatsumuri.Ses cadres seront avec lui
- là-bas.
+ C'est le rêve éternel de l'homme de devenir
+ un Idéalien. Seul Xibalba le peut. Tous
+ espèrent son avènement.[E1][E2]
+ [E3][E4][NULL][NULL]"Maya
+ Joker... Enfin Jun-kun, prépare un truc au
+ Mt Katatsumuri. Ses cadres seront avec lui
+ là-bas.
```

### 🔹 `script_332.json` — ID 52 | **Tony**
- **Catégorie :** Nettoyage accident d'édition (texte parasite collé) *(Budget alloué : 306 octets)*

```diff
- Tu veux me vendre quoi?
- [1208][0007][111F][1210][B_00][U+5501][B_00]Sélection cachée
- [111F]Objets
- [111F]Armes[SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP]
- [111F][1210][B_00][U+5301][B_00]Armure de tête
- [111F]Armure[SP][SP][SP][SP][SP][SP][SP]
- [111F][1210][B_00][U+5301][B_00]Jambes[SP][SP][SP][SP][SP][SP]
- [111F]Accessoires[B_00][5501][B_00][B_00][5301][B_00][B_00][5301][B_00]
+ Tu veux me vendre quoi ?
+ [1208][0007][111F][1210][B_00][U+5501][B_00]Sélection cachée
+ [111F]Objets
+ [111F]Armes
+ [111F][1210][B_00][U+5301][B_00]Armure de tête
+ [111F]Armure
+ [111F][1210][B_00][U+5301][B_00]Jambes
+ [111F]Accessoires[B_00][5501][B_00][B_00][5301][B_00][B_00][5301][B_00]
```

### 🔹 `script_332.json` — ID 55 | **Tony**
- **Catégorie :** Nettoyage accident d'édition (texte parasite collé) *(Budget alloué : 306 octets)*

```diff
- Tu veux me vendre quoi?
- [1208][0007][111F][1210][B_00][U+5501][B_00]Sélection cachée
- [111F]Objets
- [111F]Armes[SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP]
- [111F][1210][B_00][U+5301][B_00]Armure de tête
- [111F]Armure[SP][SP][SP][SP][SP][SP][SP]
- [111F][1210][B_00][U+5301][B_00]Jambes[SP][SP][SP][SP][SP][SP]
- [111F]Accessoires[B_00][5501][B_00][B_00][5301][B_00][B_00][5301][B_00]
+ Tu veux me vendre quoi ?
+ [1208][0007][111F][1210][B_00][U+5501][B_00]Sélection cachée
+ [111F]Objets
+ [111F]Armes
+ [111F][1210][B_00][U+5301][B_00]Armure de tête
+ [111F]Armure
+ [111F][1210][B_00][U+5301][B_00]Jambes
+ [111F]Accessoires[B_00][5501][B_00][B_00][5301][B_00][B_00][5301][B_00]
```

### 🔹 `script_332.json` — ID 57 | **Tony**
- **Catégorie :** Calibrage menu à choix *(Budget alloué : 270 octets)*

```diff
- Okay. Tu veux autre chose?
- [1208][0006][1210][U+03BB]Buy weapons
- Buy accessories
- Sell items
- Talk to Tony
- Never mind
- Leave the store[03BB]
+ Okay. Tu veux autre chose ?
+ [1208][0006][1210][U+03BB]Acheter armes
+ Acheter accessoires
+ Vendre objets
+ Parler à Tony
+ Rien
+ Partir
```

### 🔹 `script_332.json` — ID 58 | **Tony**
- **Catégorie :** Nettoyage accident d'édition (texte parasite collé) *(Budget alloué : 306 octets)*

```diff
- Tu veux me vendre quoi?
- [1208][0007][111F][1210][B_00][U+5501][B_00]Sélection cachée
- [111F]Objets
- [111F]Armes[SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP]
- [111F][1210][B_00][U+5301][B_00]Armure de tête
- [111F]Armure[SP][SP][SP][SP][SP][SP][SP]
- [111F][1210][B_00][U+5301][B_00]Jambes[SP][SP][SP][SP][SP][SP]
- [111F]Accessoires[B_00][5501][B_00][B_00][5301][B_00][B_00][5301][B_00]
+ Tu veux me vendre quoi ?
+ [1208][0007][111F][1210][B_00][U+5501][B_00]Sélection cachée
+ [111F]Objets
+ [111F]Armes
+ [111F][1210][B_00][U+5301][B_00]Armure de tête
+ [111F]Armure
+ [111F][1210][B_00][U+5301][B_00]Jambes
+ [111F]Accessoires[B_00][5501][B_00][B_00][5301][B_00][B_00][5301][B_00]
```

### 🔹 `script_332.json` — ID 125 | **Membre du Cercle masqué**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 280 octets)*

```diff
- Les écrits d'In Lak'ech ressemblent
- aux enseignements du Joker... L'un de
- nos cadres a-t-il fuité ce manuscrit!?
+ Les écrits d'In Lak'ech ressemblent
+ aux cours du Joker... Un de nos cadres
+ a-t-il fait fuiter ce manuscrit !?
```

### 🔹 `script_333.json` — ID 19 | **Tony**
- **Catégorie :** Nettoyage accident d'édition (texte parasite collé) *(Budget alloué : 310 octets)*

```diff
- Tu veux me vendre quoi?
- [1208][0007][111F][1210][B_00][U+5501][B_00]Sélection cachée
- [111F]Objets
- [111F]Armes[SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP]
- [111F][1210][B_00][U+5301][B_00]Armure de tête
- [111F]Sell armor[SP][SP][SP]
- [111F][1210][B_00][U+5301][B_00]Jambes
- [111F]Accessoires[SP][SP][SP][SP][SP][SP]
- [1109][E2][B_00][5501][B_00][B_00][5301][B_00][B_00][5301][B_00]
+ Tu veux me vendre quoi ?
+ [1208][0007][111F][1210][B_00][U+5501][B_00]Sélection cachée
+ [111F]Objets
+ [111F]Armes
+ [111F][1210][B_00][U+5301][B_00]Armure de tête
+ [111F]Armure
+ [111F][1210][B_00][U+5301][B_00]Jambes
+ [111F]Accessoires
+ [1109][E2][B_00][5501][B_00][B_00][5301][B_00][B_00][5301][B_00]
```

### 🔹 `script_333.json` — ID 22 | **Tony**
- **Catégorie :** Nettoyage accident d'édition (texte parasite collé) *(Budget alloué : 306 octets)*

```diff
- Tu veux me vendre quoi?
- [1208][0007][111F][1210][B_00][U+5501][B_00]Sélection cachée
- [111F]Objets
- [111F]Armes[SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP]
- [111F][1210][B_00][U+5301][B_00]Armure de tête
- [111F]Armure[SP][SP][SP][SP][SP][SP][SP]
- [111F][1210][B_00][U+5301][B_00]Jambes[SP][SP][SP][SP][SP][SP]
- [111F]Accessoires[B_00][5501][B_00][B_00][5301][B_00][B_00][5301][B_00]
+ Tu veux me vendre quoi ?
+ [1208][0007][111F][1210][B_00][U+5501][B_00]Sélection cachée
+ [111F]Objets
+ [111F]Armes
+ [111F][1210][B_00][U+5301][B_00]Armure de tête
+ [111F]Armure
+ [111F][1210][B_00][U+5301][B_00]Jambes
+ [111F]Accessoires[B_00][5501][B_00][B_00][5301][B_00][B_00][5301][B_00]
```

### 🔹 `script_333.json` — ID 25 | **Tony**
- **Catégorie :** Nettoyage accident d'édition (texte parasite collé) *(Budget alloué : 306 octets)*

```diff
- Tu veux me vendre quoi?
- [1208][0007][111F][1210][B_00][U+5501][B_00]Sélection cachée
- [111F]Objets
- [111F]Armes[SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP]
- [111F][1210][B_00][U+5301][B_00]Armure de tête
- [111F]Armure[SP][SP][SP][SP][SP][SP][SP]
- [111F][1210][B_00][U+5301][B_00]Jambes[SP][SP][SP][SP][SP][SP]
- [111F]Accessoires[B_00][5501][B_00][B_00][5301][B_00][B_00][5301][B_00]
+ Tu veux me vendre quoi ?
+ [1208][0007][111F][1210][B_00][U+5501][B_00]Sélection cachée
+ [111F]Objets
+ [111F]Armes
+ [111F][1210][B_00][U+5301][B_00]Armure de tête
+ [111F]Armure
+ [111F][1210][B_00][U+5301][B_00]Jambes
+ [111F]Accessoires[B_00][5501][B_00][B_00][5301][B_00][B_00][5301][B_00]
```

### 🔹 `script_333.json` — ID 28 | **Tony**
- **Catégorie :** Restauration d'opcode critique *(Budget alloué : 204 octets)*

```diff
- Mais l'In Lak'ech, ça s'est réalisé!
- Je vais devenir 000F]devenir un
- Idéalien? Oh, ce serait super!
+ L'In Lak'ech s'est réalisé ![1205][000F]
+ Je vais devenir un Idéalien ?
+ Oh, ce serait génial !
```

### 🔹 `script_334.json` — ID 32 | **Maya**
- **Catégorie :** Restauration d'opcode critique *(Budget alloué : 204 octets)*

```diff
- J'ai l'impression qu'il y avait
- quelque chose de 205]de plus
- profond. J'aurais aimé comprendre...
+ Il y avait un sens plus profond...[1205][000F]
+ Si seulement j'avais pu comprendre...
```

### 🔹 `script_334.json` — ID 85 | **Vendeuse**
- **Catégorie :** Restauration d'opcode critique *(Budget alloué : 208 octets)*

```diff
- Les terroristes ont aussi visé
- Smile Hirasaka, non? 5]non? Dieu
- merci quelqu'un les a arrêtés.
+ Les terroristes visaient aussi Smile
+ Hirasaka ?[1205][000F] Heureusement qu'on les
+ a arrêtés !
```

### 🔹 `script_334.json` — ID 160 | **Membre du Cercle masqué**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 310 octets)*

```diff
- Si In Lak'ech a raison... Alors je peux
- recommencer... de corps et d'esprit... Je
- peux devenir la femme que je veux
- être...Héhéhé...
+ Si l'In Lak'ech dit vrai... Je pourrai
+ repartir de zéro... de corps et d'esprit...
+ Être la femme que je veux... Héhé...
```

### 🔹 `script_335.json` — ID 2 | **Maya**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 300 octets)*

```diff
- Je me demande si Jun-kun se sent coupable
- d'avoir ordonné de protéger les gens...[1205][U+0019] Mais
- s'il ne l'avait pas fait, bien plus
- auraientpéri.[0019]
+ Je me demande si Jun-kun se sent coupable
+ d'avoir ordonné de protéger les gens...[1205][0019] Mais
+ s'il ne l'avait pas fait, bien plus
+ auraient péri.
```

### 🔹 `script_338.json` — ID 21 | **Maya**
- **Catégorie :** Restauration d'opcode critique *(Budget alloué : 220 octets)*

```diff
- Certes, ça faisait longtemps, mais
- c'était son premier 000F]premier
- amour. Oublie-t-on un visage si vite?
+ Ça faisait longtemps, mais c'était son
+ premier amour, non ?[1205][000F] On oublie un visage
+ aussi vite ?
```

### 🔹 `script_338.json` — ID 95 | **Mec**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 212 octets)*

```diff
- Ouille! Mec, t'as pas assez d'argent.
- [1205][000F] Je peux pas 0F]pas te laisser
- les lits de bronzage comme ça.
+ Oula ! T'as pas assez d'argent.[1205][000F]
+ Je peux pas te laisser utiliser les bancs
+ solaires sans payer.
```

### 🔹 `script_342.json` — ID 24 | **Eikichi**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 208 octets)*

```diff
- Y'a plus de tickets, on dirait. Je pense pas
- qu'on pourra passer [1205][000F] par l'entrée. Des
- idées?
+ Plus de tickets, on dirait. On ne pourra
+ pas passer par l'entrée.[1205][000F] Des idées ?
```

### 🔹 `script_342.json` — ID 45 | **Ginko**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 294 octets)*

```diff
- C'est pour ça que ce prof essayait
- d'empêcher l'horloge de Seven de redémarrer,
- même après [1205][000F] sa mort...? Holeen, je me sens
- mal pour lui.
+ C'est pour ça que ce prof voulait arrêter
+ l'horloge de Seven, même après sa mort... ?
+ [1205][000F]Holeen, il me fait presque pitié.
```

### 🔹 `script_342.json` — ID 99 | **Commère Chikarin**
- **Catégorie :** Restauration d'opcode critique *(Budget alloué : 368 octets)*

```diff
- Bien, tu savais que le café [E4][NULL][NULL][0006]Jolly Roger[E4][NULL][NULL][0002] à
- Kounan [E4][NULL][NULL][0006]vendait de vraies armes[E4][NULL][NULL][0002]? Il 205]Il y
- a [E4][NULL][NULL][0006]du très bon choix, mais le prix de revente
- estabyssal[E4][NULL][NULL][0002].
+ Tu savais que le [E4][NULL][NULL][0006]Jolly Roger[E4][NULL][NULL][0002] à Kounan
+ [E4][NULL][NULL][0006]vend de vraies armes[E4][NULL][NULL][0002] ?[1205][000F] Leurs [E4][NULL][NULL][0006]stocks sont
+ top, mais la reprise est minable[E4][NULL][NULL][0002].
```

### 🔹 `script_342.json` — ID 105 | **Commère Chikarin**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 336 octets)*

```diff
- Le magasin [E4][NULL][NULL][0006]Anima Mundi[E4][NULL][NULL][0002] près d'ici vend de
- [E4][NULL][NULL][0006]vraies armes[E4][NULL][NULL][0002]. [1205][000F]Il y a [E4][NULL][NULL][0006]une sélection
- incroyable, mais des prix de rachat très
- bas[E4][NULL][NULL][0002].
+ [E4][NULL][NULL][0006]Anima Mundi[E4][NULL][NULL][0002] vend de [E4][NULL][NULL][0006]vraies armes[E4][NULL][NULL][0002].[1205][000F]
+ Leur [E4][NULL][NULL][0006]choix est incroyable, mais leurs
+ prix de reprise sont ridicules[E4][NULL][NULL][0002].
```

### 🔹 `script_342.json` — ID 186 | **Fuyuko**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 276 octets)*

```diff
- Écoute. Un Chapeau de Yacht ne devrait
- pas être dans un taxi, hein? [1205][000F] Ce taxi
- d'escorte doit être une [E4][NULL][NULL][0006]Escorte Maudite[E4][NULL][NULL][0002]!
+ Écoute. Un Chapeau de yacht dans un taxi,
+ c'est louche, non ?[1205][000F] Ce taxi devait être
+ une [E4][NULL][NULL][0006]Escorte Maudite[E4][NULL][NULL][0002] !
```

### 🔹 `script_343.json` — ID 5 | **Ginko**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 282 octets)*

```diff
- C'était pas le Temple de Taurus à Kounan?
- [1205][000F]Je suis un Taureau... donc mon ombre doit
- y être. Récupérons le crâne en vitesse.
+ C'était pas le Temple du Taureau à Kounan ?
+ [1205][000F]Je suis Taureau... donc mon ombre doit
+ y être. Récupérons le crâne en vitesse.
```

### 🔹 `script_343.json` — ID 35 | **Commère Chikarin**
- **Catégorie :** Restauration d'opcode critique *(Budget alloué : 368 octets)*

```diff
- Bien, tu savais que le café [E4][NULL][NULL][0006]Jolly Roger[E4][NULL][NULL][0002] à
- Kounan [E4][NULL][NULL][0006]vendait de vraies armes[E4][NULL][NULL][0002]? Il 205]Il y
- a [E4][NULL][NULL][0006]du très bon choix, mais le prix de revente
- estabyssal[E4][NULL][NULL][0002].
+ Tu savais que le café [E4][NULL][NULL][0006]Jolly Roger[E4][NULL][NULL][0002] à
+ Kounan [E4][NULL][NULL][0006]vend de vraies armes[E4][NULL][NULL][0002] ?[1205][000F] Il y a
+ [E4][NULL][NULL][0006]du choix, mais le rachat est dérisoire[E4][NULL][NULL][0002].
```

### 🔹 `script_343.json` — ID 41 | **Commère Chikarin**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 336 octets)*

```diff
- Le magasin [E4][NULL][NULL][0006]Anima Mundi[E4][NULL][NULL][0002] près d'ici vend de
- [E4][NULL][NULL][0006]vraies armes[E4][NULL][NULL][0002]. [1205][000F]Il y a [E4][NULL][NULL][0006]une sélection
- incroyable, mais des prix de rachat très
- bas[E4][NULL][NULL][0002].
+ Le magasin [E4][NULL][NULL][0006]Anima Mundi[E4][NULL][NULL][0002] vend de
+ [E4][NULL][NULL][0006]vraies armes[E4][NULL][NULL][0002].[1205][000F] Il y a [E4][NULL][NULL][0006]du choix, mais les
+ prix de rachat sont dérisoires[E4][NULL][NULL][0002].
```

### 🔹 `script_344.json` — ID 6 | **Ginko**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 210 octets)*

```diff
- ... Évident, hein? [1205][000F]Vu qu'elle
- bosse avec eux, je trouve ça fou
- que Maya l'ai jamais remarqué.
+ ...Évident, non ?[1205][000F] Vu qu'elle bosse
+ avec eux, comment Maya n'a rien vu ?
```

### 🔹 `script_344.json` — ID 54 | **Fujii**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 220 octets)*

```diff
- Tu es aussi beau qu'on le dit. Je
- me demande si tu accepterais d'être
- mon modèle ? Si tu veux, bien sûr.
+ Tu es aussi beau qu'on le dit. Tu
+ veux bien me servir de modèle ?
+ Si tu veux, bien sûr.
```

### 🔹 `script_345.json` — ID 10 | **Journaliste**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 206 octets)*

```diff
- Fujii-san est toujours au Mont
- Katatsumuri ?[1205][000F] Le monde ne va
- pas bientôt finir ?[1205][000F] Oh là là...
+ Fujii est toujours au mont
+ Katatsumuri ?[1205][000F] La fin du monde est
+ proche ?[1205][000F] Oh là là...
```

### 🔹 `script_346.json` — ID 4 | **Eikichi**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 236 octets)*

```diff
- Vous avez senti ça...[1205][000F] ? Quand on
- y pense, doit y avoir pas mal
- d'utilisateurs de Persona dans le coin...
+ Vous avez senti ça... ?[1205][000F] Quand on
+ y pense, doit y avoir pas mal
+ d'utilisateurs de Persona ici...
```

### 🔹 `script_347.json` — ID 14 | **Réception**
- **Catégorie :** Nettoyage accident d'édition (texte parasite collé) *(Budget alloué : 244 octets)*

```diff
- Navré, mais les étages supérieurs sont
- réservés aux employés. Merci de ne pas
- utiliser l'ascenseur. C'est un modèle de
- Sumaru TV. Chaque détail a été répliqué avec
- soin. Lundi, 19H-20H [NULL][NULL]La Minute de Brown![NULL][NULL] Une
- émission de variété présentée par le
- polyvalent Brown. Mardi, 22H-23H [NULL][NULL]TV-Shopping[NULL][NULL]
- Un programme de télé-achat qui présente et
- vend des produits. Mercredi, 11H-12H [NULL][NULL]C votre
- avis?[NULL][NULL] Une émission où on analyse et imagine
- des solutions à des problématiques variées.
- Jeudi, 18H-18:30H [NULL][NULL]Lightron, Combattant du
- Carat[NULL][NULL] Un dessin animé où un jeune justicier
- setransforme en Combattant Doré pour
- affronter le mal. Vendredi, 20H-21H [NULL][NULL]Je suis
- en direct![NULL][NULL] Une émission-débat présentée par
- Junko Kurosu. Son franc-parler semble
- attirer bien des fans. Samedi, 21H-22H [NULL][NULL]Le
- Jour où Joe a Basculé[NULL][NULL] Un drame avec un
- assassin qui possède sept personalités
- différentes.
+ Désolé, les étages supérieurs sont
+ réservés aux employés. Merci de ne pas
+ utiliser l'ascenseur.
```

### 🔹 `script_347.json` — ID 18 | **Homme blême**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 234 octets)*

```diff
- Non, Kudan est un ami que rencontré
- dans l'usine abandonnée. Il m'a
- raconté une histoire terrifiante.
+ Non, Kudan est un ami de l'usine désaffectée.
+ Il m'a raconté une histoire terrifiante.
```

### 🔹 `script_347.json` — ID 19 | **Homme blême**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 158 octets)*

```diff
- C'est pour ça que j'ai dit vouloir
- oublier l'histoire de Kudan.
+ C'est pour ça que je voulais oublier
+ l'histoire de Kudan.
```

### 🔹 `script_347.json` — ID 23 | **Homme blême**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 300 octets)*

```diff
- Des choses qui apparaissent de nulle part...[1205][000F]
- Le néant qui devient quelque chose...[1205][000F]
- Peut-être que la bouche humaine est la chose
- la plus terrifiante au monde.
+ Des choses qui surgissent de nulle part...[1205][000F]
+ Le néant devient réel...[1205][000F] Les rumeurs sont
+ ce qu'il y a de plus terrifiant.
```

### 🔹 `script_348.json` — ID 9 | **Pompier**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 156 octets)*

```diff
- Comment je peux me prétendre fan
- !? Gah, ça me retourne les tripes !
+ Comment oser me dire fan !?
+ Gah, ça me retourne les tripes !
```

### 🔹 `script_349.json` — ID 0 | **Eikichi**
- **Catégorie :** Correction / Réécriture fidèle *(Budget alloué : 114 octets)*

```diff
- Mm... cette odeur.[1205]1205]J'ai la dalle.
+ Mm... cette odeur...[1205][000F]
+ J'ai la dalle.
```

### 🔹 `script_349.json` — ID 46 | **Garçon Soejima**
- **Catégorie :** Nettoyage accident d'édition (texte parasite collé) *(Budget alloué : 322 octets)*

```diff
- Que pouvez-vous me vendre?
- [1208][0007][111F][1210][B_00][U+5501][B_00]Sélection cachée
- [111F]Objets
- [111F]Armes[SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP]
- [111F][1210][B_00][U+5301][B_00]Armure de tête
- [111F]Armure[SP][SP][SP][SP][SP][SP][SP]
- [111F][1210][B_00][U+5301][B_00]Jambes[SP][SP][SP][SP][SP][SP]
- [111F]Accessoires[B_00][5501][B_00][B_00][5301][B_00][B_00][5301][B_00]
+ Que pouvez-vous me vendre ?
+ [1208][0007][111F][1210][B_00][U+5501][B_00]Sélection cachée
+ [111F]Objets
+ [111F]Armes
+ [111F][1210][B_00][U+5301][B_00]Armure de tête
+ [111F]Armure
+ [111F][1210][B_00][U+5301][B_00]Jambes
+ [111F]Accessoires[B_00][5501][B_00][B_00][5301][B_00][B_00][5301][B_00]
```

### 🔹 `script_349.json` — ID 49 | **Garçon Soejima**
- **Catégorie :** Nettoyage accident d'édition (texte parasite collé) *(Budget alloué : 322 octets)*

```diff
- Que pouvez-vous me vendre?
- [1208][0007][111F][1210][B_00][U+5501][B_00]Sélection cachée
- [111F]Objets
- [111F]Armes[SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP]
- [111F][1210][B_00][U+5301][B_00]Armure de tête
- [111F]Armure[SP][SP][SP][SP][SP][SP][SP]
- [111F][1210][B_00][U+5301][B_00]Jambes[SP][SP][SP][SP][SP][SP]
- [111F]Accessoires[B_00][5501][B_00][B_00][5301][B_00][B_00][5301][B_00]
+ Que pouvez-vous me vendre ?
+ [1208][0007][111F][1210][B_00][U+5501][B_00]Sélection cachée
+ [111F]Objets
+ [111F]Armes
+ [111F][1210][B_00][U+5301][B_00]Armure de tête
+ [111F]Armure
+ [111F][1210][B_00][U+5301][B_00]Jambes
+ [111F]Accessoires[B_00][5501][B_00][B_00][5301][B_00][B_00][5301][B_00]
```

### 🔹 `script_350.json` — ID 1 | **Eikichi**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 274 octets)*

```diff
- Le vrai moi est plus élégant... plus beau...[1205][000F]
- Ce 00F]Ce type ressemble à quelqu'un
- d'autre. Ils auraient pu faire plus
- attention.
+ Le vrai moi est plus classe... plus beau...[1205][000F]
+ Ce type a l'air d'un inconnu. Ils
+ auraient pu faire attention.
```

### 🔹 `script_350.json` — ID 6 | **Maya**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 296 octets)*

```diff
- C'était la version de nous qu'imaginaient
- les[1205][000F] autres... 00F].. Si ces croquis
- n'avaient pas circulé, elles auraient eu
- l'air tout autres.
+ C'est ainsi qu'on nous imaginait...[1205][000F]
+ Sans ces croquis, elles auraient eu
+ un tout autre visage.
```

### 🔹 `script_350.json` — ID 20 | **Garçon Soejima**
- **Catégorie :** Nettoyage accident d'édition (texte parasite collé) *(Budget alloué : 322 octets)*

```diff
- Que pouvez-vous me vendre?
- [1208][0007][111F][1210][B_00][U+5501][B_00]Sélection cachée
- [111F]Objets
- [111F]Armes[SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP]
- [111F][1210][B_00][U+5301][B_00]Armure de tête
- [111F]Armure[SP][SP][SP][SP][SP][SP][SP]
- [111F][1210][B_00][U+5301][B_00]Jambes[SP][SP][SP][SP][SP][SP]
- [111F]Accessoires[B_00][5501][B_00][B_00][5301][B_00][B_00][5301][B_00]
+ Que pouvez-vous me vendre ?
+ [1208][0007][111F][1210][B_00][U+5501][B_00]Sélection cachée
+ [111F]Objets
+ [111F]Armes
+ [111F][1210][B_00][U+5301][B_00]Armure de tête
+ [111F]Armure
+ [111F][1210][B_00][U+5301][B_00]Jambes
+ [111F]Accessoires[B_00][5501][B_00][B_00][5301][B_00][B_00][5301][B_00]
```

### 🔹 `script_350.json` — ID 23 | **Garçon Soejima**
- **Catégorie :** Nettoyage accident d'édition (texte parasite collé) *(Budget alloué : 322 octets)*

```diff
- Que pouvez-vous me vendre?
- [1208][0007][111F][1210][B_00][U+5501][B_00]Sélection cachée
- [111F]Objets
- [111F]Armes[SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP]
- [111F][1210][B_00][U+5301][B_00]Armure de tête
- [111F]Armure[SP][SP][SP][SP][SP][SP][SP]
- [111F][1210][B_00][U+5301][B_00]Jambes[SP][SP][SP][SP][SP][SP]
- [111F]Accessoires[B_00][5501][B_00][B_00][5301][B_00][B_00][5301][B_00]
+ Que pouvez-vous me vendre ?
+ [1208][0007][111F][1210][B_00][U+5501][B_00]Sélection cachée
+ [111F]Objets
+ [111F]Armes
+ [111F][1210][B_00][U+5301][B_00]Armure de tête
+ [111F]Armure
+ [111F][1210][B_00][U+5301][B_00]Jambes
+ [111F]Accessoires[B_00][5501][B_00][B_00][5301][B_00][B_00][5301][B_00]
```

### 🔹 `script_350.json` — ID 50 | **Maya**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 154 octets)*

```diff
- T-Très bien! Je vais le manger! Vous verrez![E3]
- Maya affronta le plat...[E2][E1][E2] [E3][E4][NULL][NULL] "Maya J'ai... Je
- l'ai mangé... Spaghetti... di kusaya...
+ T-Très bien, je le mange ! Regardez bien,
+ je vais vous montrer !
```

### 🔹 `script_351.json` — ID 58 | **Membre du Cercle masqué**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 196 octets)*

```diff
- Grrrrr! Joker a fait de moi une vraie
- femme, mais personne ne me croit!
+ Grrr ! Joker a fait de moi une vraie
+ femme, mais personne me croit !
```

### 🔹 `script_351.json` — ID 64 | **Membre du Cercle masqué**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 210 octets)*

```diff
- Si je deviens une Idéalienne, je trouverai
- un amour vrai qui transcende le genre...
+ En devenant Idéalienne, je trouverai le
+ vrai amour au-delà du genre...
```

### 🔹 `script_359.json` — ID 6 | **Ginko**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 188 octets)*

```diff
- H-Hé, [1113]...[1205][001E] Maya vient de me dire...[1205][001E] Elle nous a entendus, Sasaki et moi...
+ H-Hé, [1113]...[1205][001E]
+ Maya vient de me dire...[1205][001E]
+ Elle nous a entendus, Sasaki et moi...
```

### 🔹 `script_359.json` — ID 93 | **???**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 452 octets)*

```diff
- C'est ta première fois ici. Moi c'est Baofu.
- [1205][000F]Je gère ce site.[E1][E2] Baofu Colporteur de rumeurs
- en ligne avec son propre site. Rien
- n'estconnu de lui, mais il semble
- collectecter des rumeurs dans un but précis.
+ C'est ta première fois ici. Moi, c'est Baofu.
+ [1205][000F]Je gère ce site.[E1][E2]Baofu : colporteur de rumeurs en ligne.
+ On ignore tout de lui, mais il semble
+ collecter des rumeurs dans un but précis.
```

### 🔹 `script_359.json` — ID 96 | **Colporteur Baofu**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 306 octets)*

```diff
- Les rumeurs t'intéressent, non? [1205][000F]Moi aussi.
- Si tu veux, envoie-moi quelque chose.
- J'attends quelque chose qui en vaut la
- peine.
+ Les rumeurs t'intéressent ?[1205][000F] Moi aussi.
+ Si tu veux, envoie-moi des infos.
+ J'attends quelque chose qui en vaut la peine.
```

### 🔹 `script_359.json` — ID 97 | **Colporteur Baofu**
- **Catégorie :** Calibrage menu à choix *(Budget alloué : 1174 octets)*

```diff
- Tiens, de retour. Choisissez une option.
- Demander des rumeurs Parler à Baofu Annuler
- Choisissez un sujet. Rumeurs armureries
- Rumeurs armures Autres Rien Choisissez une
- région. Rengedai Yumezaki Aoba Kounan Aucune
- Choisissez une région. Rengedai Yumezaki
- Aoba Kounan Aucune Choisissez un sujet.
- Concours magazines Rumeurs Mu Armes
- légendaires Aucun Vérifié. Soumettre.
- Patientez après envoi.
+ Te revoilà.[E1][E2][E3]> Choisir une option.
+ [1208][0003][1210][U+0475]Infos rumeurs
+ Parler à Baofu
+ Annuler
+ [1109][E2][E3]> Choisir un sujet.
+ [1208][0004][1210][U+0476]Rumeurs armes
+ [1210][U+0477]Rumeurs armures
+ [1210][U+0478]Autres rumeurs
+ Rien
+ [1109][E2][E3]> Choisir un quartier.
+ [1208][0005][1210][U+046A]Rengedai
+ [1210][U+046B]Yumezaki
+ [1210][U+046C]Aoba
+ [1210][U+046D]Kounan
+ Aucun
+ [1109][E2][E3]> Choisir un quartier.
+ [1208][0005][1210][U+046E]Rengedai
+ [1210][U+046F]Yumezaki
+ [1210][U+0470]Aoba
+ [1210][U+0471]Kounan
+ Aucun
+ [1109][E2][E3]> Choisir un sujet.
+ [1208][0004][1210][U+0472]Loteries magazines
+ [1210][U+0473]Rumeurs sur le Mu
+ [1210][U+0474]Armes légendaires
+ Aucun
+ [1109][E2][E3]> Données vérifiées.
+ Envoi en cours.
+ Patientez SVP.[E1][E2][E3][E4][NULL][NULL]"[1113]
+ ...[1205][000F]...[1205][000F]...[1205][000F]...[E1][E2][E3]> Envoi des données.
+ ...[1205][000F]...[1205][000F]...[1205][000F]Envoi terminé.[E1][E2][E3][E4][NULL][NULL]
```

### 🔹 `script_359.json` — ID 120 | **Homme corpulent**
- **Catégorie :** Restauration d'opcode critique *(Budget alloué : 302 octets)*

```diff
- Hé, j'ai entendu que c'est un groupe, le
- Cercle masqué, qui fait ça. 05]ça. C'est
- vrai? J'aime pas ça... Sumaru devait être
- paisible...
+ Le Cercle masqué serait derrière
+ tout ça... C'est vrai ?[1205][000F] J'aime pas ça...
+ Sumaru était censée être paisible...
```

### 🔹 `script_359.json` — ID 137 | **Homme corpulent**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 206 octets)*

```diff
- Quels morceaux sont dessus...[1205][000F] ? Faut que
- j'en trouve une copie pour le découvrir.
+ Quels morceaux sont dessus... ?[1205][000F]
+ Faut que j'en trouve une copie !
```

### 🔹 `script_359.json` — ID 219 | **Gamin fainéant**
- **Catégorie :** Calibrage menu à choix *(Budget alloué : 100 octets)*

```diff
- Ça fait [120E][NULL] yens. OK ?
- [1208][0002]Oui
- Non
+ C'est [120E][NULL] yens. OK ?
+ [1208][0002]Oui
+ Non
```

### 🔹 `script_360.json` — ID 9 | **Ginko**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 178 octets)*

```diff
- Sheba...[1205][000F] Mee-ho... Je peux vraiment les
- retrouver? Tu t'inquiètes pas, Eikichi?
+ Sheba...[1205][000F] Mee-ho... Vais-je les revoir ?
+ Tu t'inquiètes pas, Eikichi ?
```

### 🔹 `script_360.json` — ID 10 | **Ginko**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 196 octets)*

```diff
- Tu ne retrouveras peut-être pas
- tes amis non plus. [1205][000F]Et si c'est
- le cas... pour quoi se bat-on...?
+ Et si tu ne revoyais jamais tes amis ?
+ [1205][000F]Alors... pourquoi se bat-on... ?
```

### 🔹 `script_360.json` — ID 22 | **Gamin fainéant**
- **Catégorie :** Calibrage menu à choix *(Budget alloué : 310 octets)*

```diff
- Hé. [1205][000F]Tu surfs si tôt?
- T'as du temps à perdre. Bref.
- [1208][0004]Manger ici
- Parler au gamin
- Laisser tomber
- Quitter
+ Hé.[1205][000F] Tu surfes si tôt ?
+ Tu t'ennuies ? Bref.
+ [1208][0004]Manger ici
+ Parler au gamin
+ Laisser tomber
+ Quitter
```

### 🔹 `script_360.json` — ID 31 | **???**
- **Catégorie :** Correction / Réécriture fidèle *(Budget alloué : 452 octets)*

```diff
- Première visite. Moi c'est Baofu. [1205][000F]Je gère ce
- site.[E1][E2] Baofu Colporteur en ligne avec son
- propre site. On sait rien de lui, mais
- ilcollecte des rumeurs dans un but précis.
+ C'est ta première fois ici. Moi, c'est Baofu.
+ [1205][000F]Je gère ce site.[E1][E2]Baofu : colporteur de rumeurs en ligne.
+ On ignore tout de lui, mais il semble
+ collecter des rumeurs dans un but précis.
```

### 🔹 `script_360.json` — ID 35 | **Colporteur Baofu**
- **Catégorie :** Calibrage menu à choix *(Budget alloué : 1174 octets)*

```diff
- Te revoilà. Choisis une option. Demander des
- rumeurs Parler avec Baofu Annuler Choisis un
- sujet. Rumeurs armureries Rumeurs armures
- Autres Rien Choisis une région. Rengedai
- Yumezaki Aoba Kounan Aucune Choisis une
- région. Rengedai Yumezaki Aoba Kounan Aucune
- Choisis un sujet. Rumeurs concours Rumeurs
- Mu Rumeurs armes légendaires Aucune Vérifié.
- Soumettre les infos. Après envoi, patientez.
+ Te revoilà.[E1][E2][E3]> Choisir une option.
+ [1208][0003][1210][U+0475]Infos rumeurs
+ Parler à Baofu
+ Annuler
+ [1109][E2][E3]> Choisir un sujet.
+ [1208][0004][1210][U+0476]Rumeurs armes
+ [1210][U+0477]Rumeurs armures
+ [1210][U+0478]Autres rumeurs
+ Rien
+ [1109][E2][E3]> Choisir un quartier.
+ [1208][0005][1210][U+046A]Rengedai
+ [1210][U+046B]Yumezaki
+ [1210][U+046C]Aoba
+ [1210][U+046D]Kounan
+ Aucun
+ [1109][E2][E3]> Choisir un quartier.
+ [1208][0005][1210][U+046E]Rengedai
+ [1210][U+046F]Yumezaki
+ [1210][U+0470]Aoba
+ [1210][U+0471]Kounan
+ Aucun
+ [1109][E2][E3]> Choisir un sujet.
+ [1208][0004][1210][U+0472]Loteries magazines
+ [1210][U+0473]Rumeurs sur le Mu
+ [1210][U+0474]Armes légendaires
+ Aucun
+ [1109][E2][E3]> Données vérifiées.
+ Envoi en cours.
+ Patientez SVP.[E1][E2][E3][E4][NULL][NULL]"[1113]
+ ...[1205][000F]...[1205][000F]...[1205][000F]...[E1][E2][E3]> Envoi des données.
+ ...[1205][000F]...[1205][000F]...[1205][000F]Envoi terminé.[E1][E2][E3][E4][NULL][NULL]
```

### 🔹 `script_360.json` — ID 57 | **Homme corpulent**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 70 octets)*

```diff
- É-Écoutez ça...
+ Écoutez ça...
```

### 🔹 `script_360.json` — ID 64 | **Homme corpulent**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 270 octets)*

```diff
- Quelqu'un a posté un démenti sur le
- Taxi Maudit à la fabrique abandonnée.
- [1205][000F]Il dit que c'était une Escorte Maudite.
+ Quelqu'un a démenti la rumeur du
+ Taxi Maudit à l'usine désaffectée.
+ [1205][000F]C'était en fait une Escorte Maudite.
```

### 🔹 `script_360.json` — ID 65 | **Homme corpulent**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 154 octets)*

```diff
- Vu en ligne que Kuchisake-onna
- a été aperçue au mont Iwato.
+ J'ai lu qu'on a aperçu
+ Kuchisake-onna au mont Iwato.
```

### 🔹 `script_360.json` — ID 71 | **Homme corpulent**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 132 octets)*

```diff
- C'est quoi la Vieille [1205][000F]du Tiroir? Un monstre?
+ Une Vieille du Tiroir[1205][000F] ?
+ C'est un monstre ?
```

### 🔹 `script_360.json` — ID 76 | **Homme corpulent**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 272 octets)*

```diff
- Tony, c'est ce drôle de type blanc, non?
- J'ai entendu qu'il trafique des armes.
- Bon choix, mais mauvais prix de reprise.
+ Tony, ce drôle de type blanc...
+ Il paraît qu'il vend des armes.
+ Bon choix, mais reprise minable.
```

### 🔹 `script_360.json` — ID 81 | **Homme corpulent**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 254 octets)*

```diff
- J'ai entendu qu'on peut acheter de
- vraies armes au Clair de Lune à Aoba.
- [1205][000F]Pas cher, mais qualité médiocre.
+ On vendrait de vraies armes
+ au Clair de Lune à Aoba.[1205][000F] C'est
+ pas cher, mais de piètre qualité.
```

### 🔹 `script_360.json` — ID 85 | **Homme corpulent**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 144 octets)*

```diff
- Il y a beaucoup d'informations
- dangereuses sur le net.
+ Il y a plein d'informations
+ dangereuses sur le net.
```

### 🔹 `script_360.json` — ID 87 | **Homme corpulent**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 144 octets)*

```diff
- Il y a beaucoup d'informations
- dangereuses sur le net.
+ Il y a plein d'informations
+ dangereuses sur le net.
```

### 🔹 `script_360.json` — ID 88 | **Homme corpulent**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 222 octets)*

```diff
- Tiens, j'ai vu qu'on peut acheter
- des armes au[1205][000F] Jolly Roger. Pas
- cher, mais qualité médiocre.
+ J'ai vu qu'on vend des armes
+ au[1205][000F] Jolly Roger. C'est pas cher,
+ mais de piètre qualité.
```

### 🔹 `script_360.json` — ID 89 | **Homme corpulent**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 144 octets)*

```diff
- Il y a beaucoup d'informations
- dangereuses sur le net.
+ Il y a plein d'informations
+ dangereuses sur le net.
```

### 🔹 `script_360.json` — ID 91 | **Homme corpulent**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 144 octets)*

```diff
- Il y a beaucoup d'informations
- dangereuses sur le net.
+ Il y a plein d'informations
+ dangereuses sur le net.
```

### 🔹 `script_360.json` — ID 93 | **Homme corpulent**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 144 octets)*

```diff
- Il y a beaucoup d'informations
- dangereuses sur le net.
+ Il y a plein d'informations
+ dangereuses sur le net.
```

### 🔹 `script_360.json` — ID 99 | **Homme corpulent**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 294 octets)*

```diff
- L'armure comme tendance mode, j'avais jamais
- entendu ça...[1205][000F] Mais Anima Mundi en vend.
- Qualité basse, mais au moins c'est pas cher.
+ L'armure à la mode ? Jamais vu ça...[1205][000F]
+ Mais Anima Mundi en vend. Basse
+ qualité, mais au moins c'est pas cher.
```

### 🔹 `script_360.json` — ID 137 | **Homme corpulent**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 284 octets)*

```diff
- Une arme légendaire...[1205][000F] ? Ça fait penser à
- un jeu vidéo. Tu crois vraiment trouver
- un truc comme ça dans un resto de ramen?
+ Une arme légendaire...[1205][000F] ? On se croirait
+ dans un jeu vidéo. Tu crois en trouver
+ dans un resto de ramen ?
```

### 🔹 `script_360.json` — ID 144 | **Homme corpulent**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 220 octets)*

```diff
- Le deuxième étage du Zodiac est
- un grand labyrinthe. Certains
- y ont même trouvé des trésors.
+ Le 2e étage du Zodiac est un grand
+ labyrinthe. Certains y ont même
+ trouvé des trésors.
```

### 🔹 `script_360.json` — ID 147 | **Sœur #3**
- **Catégorie :** Calibrage menu à choix *(Budget alloué : 126 octets)*

```diff
- Ça fait [120E][NULL] yens.
- Vous le voulez?
- [1208][0002]Oui
- Non
+ [120E][NULL] yens en tout.
+ Vous prenez ?
+ [1208][0002]Oui
+ Non
```

### 🔹 `script_360.json` — ID 151 | **Voix**
- **Catégorie :** Calibrage menu à choix *(Budget alloué : 92 octets)*

```diff
- Total: [120E][NULL] yens. Vendre?
- [1208][0002]Oui
- Non
+ [120E][NULL] yens au total.
+ Vendre ?
+ [1208][0002]Oui
+ Non
```

### 🔹 `script_360.json` — ID 152 | **Gamin fainéant**
- **Catégorie :** Calibrage menu à choix *(Budget alloué : 100 octets)*

```diff
- Ça fait [120E][NULL] yens. OK ?
- [1208][0002]Oui
- Non
+ [120E][NULL] yens, d'accord ?
+ [1208][0002]Oui
+ Non
```

### 🔹 `script_361.json` — ID 8 | **Maya**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 154 octets)*

```diff
- Il sait peut-être quelque chose sur
- le Cercle masqué. Demande-lui, [1113]!
+ Il sait peut-être un truc sur le Cercle
+ masqué. Demande-lui, [1113] !
```

### 🔹 `script_361.json` — ID 27 | **Clocharde**
- **Catégorie :** Nettoyage accident d'édition (texte parasite collé) *(Budget alloué : 158 octets)*

```diff
- La fin est proche. Ce garçon... je l'ai déjà
- vu quelque part? Panneau SS: Accueil
- général, Bureau étrangers RDC: Objets
- trouvés, Permis, Conseillers 2e: Aide
- victimes, Aide sinistrés Panneau 3e:
- Interrogatoire, Affaires internes 4e: Labo,
- Crimes juvéniles 5e: Personnesdisparues,
- Enquêtes spéciales
+ La fin est proche... Ce garçon... Je l'ai
+ déjà vu quelque part ?
```

### 🔹 `script_361.json` — ID 37 | **Agent de police**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 316 octets)*

```diff
- Katsuya est très populaire auprès des femmes
- du commissariat...[1205][000F] Mais pas de petite amie.
- Il est du genre marié à son boulot? Avis Si
- vous voyez cet homme, appelez le 17! Je
- crois l'avoir vu quelque part...
+ Katsuya plaît beaucoup aux femmes du
+ poste...[1205][000F] Mais pas de petite amie. Il est
+ du genre marié à son travail ?
```

### 🔹 `script_362.json` — ID 36 | **Ulala**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 206 octets)*

```diff
- Ce crétin s'est échappé, et maintenant ces
- soldats... Pourquoi j'ai si peu de chance?
- Une nouvelle chaîne. [1205][000F]La seule chose propre
- ici. Jouer un CD? OuiNon
+ Ce crétin a filé, et maintenant ces soldats
+ arrivent...[1205][000F] Pourquoi j'ai la poisse ?
```

### 🔹 `script_362.json` — ID 38 | **Ulala**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 150 octets)*

```diff
- HÉ ! C'est ma chambre ! Restez dehors
- sauf si vous voulez payer le prix fort !
+ HÉ ! C'est ma chambre ! Dehors,
+ sauf à payer le prix fort !
```

### 🔹 `script_364.json` — ID 5 | **Ulala**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 248 octets)*

```diff
- Mais tu sais... un plus jeune me tente
- aussi. Si j'en trouve un mignon, je le[1205][000F] garde
- tant que je peux... Un radiocassette neuf.
- La seule chose propre de la pièce. Lire un
- CD? OuiNon
+ Tu sais... un jeune me plairait bien.[1205][000F]
+ Si j'en trouve un mignon, je le garde
+ tant que je peux...
```

### 🔹 `script_364.json` — ID 6 | **Ulala**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 150 octets)*

```diff
- HÉ ! C'est ma chambre ! Restez dehors
- sauf si vous voulez payer le prix fort !
+ HÉ ! C'est ma chambre ! Dehors,
+ sauf à payer le prix fort !
```

### 🔹 `script_365.json` — ID 21 | **Maître**
- **Catégorie :** Nettoyage accident d'édition (texte parasite collé) *(Budget alloué : 308 octets)*

```diff
- Qu'avez-vous à vendre?
- [1208][0007][111F][1210][B_00][U+5501][B_00]Sélection cachée
- [111F]Objets
- [111F]Armes[SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP]
- [111F][1210][B_00][U+5301][B_00]Armure de tête
- [111F]Armure[SP][SP][SP][SP][SP][SP][SP]
- [111F][1210][B_00][U+5301][B_00]Jambes[SP][SP][SP][SP][SP][SP]
- [111F]Accessoires[B_00][5501][B_00][B_00][5301][B_00][B_00][5301][B_00]
+ Qu'avez-vous à vendre ?
+ [1208][0007][111F][1210][B_00][U+5501][B_00]Sélection cachée
+ [111F]Objets
+ [111F]Armes
+ [111F][1210][B_00][U+5301][B_00]Armure de tête
+ [111F]Armure
+ [111F][1210][B_00][U+5301][B_00]Jambes
+ [111F]Accessoires[B_00][5501][B_00][B_00][5301][B_00][B_00][5301][B_00]
```

### 🔹 `script_365.json` — ID 24 | **Maître**
- **Catégorie :** Nettoyage accident d'édition (texte parasite collé) *(Budget alloué : 308 octets)*

```diff
- Qu'avez-vous à vendre?
- [1208][0007][111F][1210][B_00][U+5501][B_00]Sélection cachée
- [111F]Objets
- [111F]Armes[SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP]
- [111F][1210][B_00][U+5301][B_00]Armure de tête
- [111F]Armure[SP][SP][SP][SP][SP][SP][SP]
- [111F][1210][B_00][U+5301][B_00]Jambes[SP][SP][SP][SP][SP][SP]
- [111F]Accessoires[B_00][5501][B_00][B_00][5301][B_00][B_00][5301][B_00]
+ Qu'avez-vous à vendre ?
+ [1208][0007][111F][1210][B_00][U+5501][B_00]Sélection cachée
+ [111F]Objets
+ [111F]Armes
+ [111F][1210][B_00][U+5301][B_00]Armure de tête
+ [111F]Armure
+ [111F][1210][B_00][U+5301][B_00]Jambes
+ [111F]Accessoires[B_00][5501][B_00][B_00][5301][B_00][B_00][5301][B_00]
```

### 🔹 `script_366.json` — ID 12 | **Maître**
- **Catégorie :** Nettoyage accident d'édition (texte parasite collé) *(Budget alloué : 308 octets)*

```diff
- Qu'avez-vous à vendre?
- [1208][0007][111F][1210][B_00][U+5501][B_00]Sélection cachée
- [111F]Objets
- [111F]Armes[SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP]
- [111F][1210][B_00][U+5301][B_00]Armure de tête
- [111F]Armure[SP][SP][SP][SP][SP][SP][SP]
- [111F][1210][B_00][U+5301][B_00]Jambes[SP][SP][SP][SP][SP][SP]
- [111F]Accessoires[B_00][5501][B_00][B_00][5301][B_00][B_00][5301][B_00]
+ Qu'avez-vous à vendre ?
+ [1208][0007][111F][1210][B_00][U+5501][B_00]Sélection cachée
+ [111F]Objets
+ [111F]Armes
+ [111F][1210][B_00][U+5301][B_00]Armure de tête
+ [111F]Armure
+ [111F][1210][B_00][U+5301][B_00]Jambes
+ [111F]Accessoires[B_00][5501][B_00][B_00][5301][B_00][B_00][5301][B_00]
```

### 🔹 `script_366.json` — ID 15 | **Maître**
- **Catégorie :** Nettoyage accident d'édition (texte parasite collé) *(Budget alloué : 308 octets)*

```diff
- Qu'avez-vous à vendre?
- [1208][0007][111F][1210][B_00][U+5501][B_00]Sélection cachée
- [111F]Objets
- [111F]Armes[SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP]
- [111F][1210][B_00][U+5301][B_00]Armure de tête
- [111F]Armure[SP][SP][SP][SP][SP][SP][SP]
- [111F][1210][B_00][U+5301][B_00]Jambes[SP][SP][SP][SP][SP][SP]
- [111F]Accessoires[B_00][5501][B_00][B_00][5301][B_00][B_00][5301][B_00]
+ Qu'avez-vous à vendre ?
+ [1208][0007][111F][1210][B_00][U+5501][B_00]Sélection cachée
+ [111F]Objets
+ [111F]Armes
+ [111F][1210][B_00][U+5301][B_00]Armure de tête
+ [111F]Armure
+ [111F][1210][B_00][U+5301][B_00]Jambes
+ [111F]Accessoires[B_00][5501][B_00][B_00][5301][B_00][B_00][5301][B_00]
```

### 🔹 `script_367.json` — ID 50 | **Artiste d'âge mûr**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 388 octets)*

```diff
- Beaucoup ont voulu mettre la main sur son
- œuvre, mais il refusait louanges et prix.
- [E3][E4][NULL][NULL]"Artiste d'âge mûr C'était un artiste noble
- et fier.
+ Beaucoup voulaient ses toiles, mais il
+ refusait les éloges et tout prix.
+ [E3][E4][NULL][NULL]"Artiste d'âge mûr
+ Un artiste noble et fier.
```

### 🔹 `script_367.json` — ID 60 | **Tailleur**
- **Catégorie :** Nettoyage accident d'édition (texte parasite collé) *(Budget alloué : 320 octets)*

```diff
- Qu'avez-vous à m'offrir?
- [1208][0007][111F][1210][B_00][U+5501][B_00]Sélection cachée
- [111F]Objets
- [111F]Armes[SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP]
- [111F][1210][B_00][U+5301][B_00]Armure de tête
- [111F]Armure[SP][SP][SP][SP][SP][SP][SP]
- [111F][1210][B_00][U+5301][B_00]Jambes
- [111F]Accessoires[SP][SP][SP][SP][SP][SP]
- [1109][E2][B_00][5501][B_00][B_00][5301][B_00][B_00][5301][B_00]
+ Qu'avez-vous à m'offrir ?
+ [1208][0007][111F][1210][B_00][U+5501][B_00]Sélection cachée
+ [111F]Objets
+ [111F]Armes
+ [111F][1210][B_00][U+5301][B_00]Armure de tête
+ [111F]Armure
+ [111F][1210][B_00][U+5301][B_00]Jambes
+ [111F]Accessoires
+ [1109][E2][B_00][5501][B_00][B_00][5301][B_00][B_00][5301][B_00]
```

### 🔹 `script_367.json` — ID 63 | **Tailleur**
- **Catégorie :** Nettoyage accident d'édition (texte parasite collé) *(Budget alloué : 316 octets)*

```diff
- Qu'avez-vous à m'offrir?
- [1208][0007][111F][1210][B_00][U+5501][B_00]Sélection cachée
- [111F]Objets
- [111F]Armes[SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP]
- [111F][1210][B_00][U+5301][B_00]Armure de tête
- [111F]Armure[SP][SP][SP][SP][SP][SP][SP]
- [111F][1210][B_00][U+5301][B_00]Jambes[SP][SP][SP][SP][SP][SP]
- [111F]Accessoires[B_00][5501][B_00][B_00][5301][B_00][B_00][5301][B_00]
+ Qu'avez-vous à m'offrir ?
+ [1208][0007][111F][1210][B_00][U+5501][B_00]Sélection cachée
+ [111F]Objets
+ [111F]Armes
+ [111F][1210][B_00][U+5301][B_00]Armure de tête
+ [111F]Armure
+ [111F][1210][B_00][U+5301][B_00]Jambes
+ [111F]Accessoires[B_00][5501][B_00][B_00][5301][B_00][B_00][5301][B_00]
```

### 🔹 `script_368.json` — ID 22 | **Tailleur**
- **Catégorie :** Nettoyage accident d'édition (texte parasite collé) *(Budget alloué : 316 octets)*

```diff
- Qu'avez-vous à m'offrir?
- [1208][0007][111F][1210][B_00][U+5501][B_00]Sélection cachée
- [111F]Objets
- [111F]Armes[SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP]
- [111F][1210][B_00][U+5301][B_00]Armure de tête
- [111F]Armure[SP][SP][SP][SP][SP][SP][SP]
- [111F][1210][B_00][U+5301][B_00]Jambes[SP][SP][SP][SP][SP][SP]
- [111F]Accessoires[B_00][5501][B_00][B_00][5301][B_00][B_00][5301][B_00]
+ Qu'avez-vous à m'offrir ?
+ [1208][0007][111F][1210][B_00][U+5501][B_00]Sélection cachée
+ [111F]Objets
+ [111F]Armes
+ [111F][1210][B_00][U+5301][B_00]Armure de tête
+ [111F]Armure
+ [111F][1210][B_00][U+5301][B_00]Jambes
+ [111F]Accessoires[B_00][5501][B_00][B_00][5301][B_00][B_00][5301][B_00]
```

### 🔹 `script_368.json` — ID 25 | **Tailleur**
- **Catégorie :** Nettoyage accident d'édition (texte parasite collé) *(Budget alloué : 316 octets)*

```diff
- Qu'avez-vous à m'offrir?
- [1208][0007][111F][1210][B_00][U+5501][B_00]Sélection cachée
- [111F]Objets
- [111F]Armes[SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP][SP]
- [111F][1210][B_00][U+5301][B_00]Armure de tête
- [111F]Armure[SP][SP][SP][SP][SP][SP][SP]
- [111F][1210][B_00][U+5301][B_00]Jambes[SP][SP][SP][SP][SP][SP]
- [111F]Accessoires[B_00][5501][B_00][B_00][5301][B_00][B_00][5301][B_00]
+ Qu'avez-vous à m'offrir ?
+ [1208][0007][111F][1210][B_00][U+5501][B_00]Sélection cachée
+ [111F]Objets
+ [111F]Armes
+ [111F][1210][B_00][U+5301][B_00]Armure de tête
+ [111F]Armure
+ [111F][1210][B_00][U+5301][B_00]Jambes
+ [111F]Accessoires[B_00][5501][B_00][B_00][5301][B_00][B_00][5301][B_00]
```

### 🔹 `script_370.json` — ID 8 | **Fan d'astrologie**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 310 octets)*

```diff
- J'ai entendu qu'en évoluant, on connaîtra
- notre but dans la vie, alors j'y ai beaucoup
- [1205][000F] réfléchi. Je n'y avais jamais pensé
- avant...
+ On dit qu'en évoluant, on connaîtra notre
+ but dans la vie. Alors j'y réfléchis...[1205][000F] Je n'y
+ avais jamais pensé auparavant...
```

### 🔹 `script_370.json` — ID 9 | **Fan d'astrologie**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 334 octets)*

```diff
- Je n'y suis pas tout à fait arrivée,[1205][000F] mais
- j'ai fini par me trouver moi-même... ême...
- C'est dur à expliquer, maisje sens que j'ai
- trouvé le vrai moi.
+ Je n'y suis pas tout à fait arrivée,[1205][000F] mais
+ j'ai fini par me trouver moi-même...
+ C'est dur à expliquer, mais j'ai trouvé
+ qui je suis vraiment.
```

### 🔹 `script_371.json` — ID 76 | **Membre du Cercle masqué**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 214 octets)*

```diff
- Raaah! Qui suis-je!? Que m'est-il arrivé!?
- Quels souvenirs Joker a-t-il effacés!?
+ Raaah ! Qui suis-je !?
+ Qu'est-ce que le Joker m'a effacé !?
```

### 🔹 `script_371.json` — ID 81 | **Membre du Cercle masqué**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 264 octets)*

```diff
- J'avais tort... Je voulais juste...[1205][000F] fuir...[1205][000F]
- le souvenir de mes crimes... ou ils
- m'auraient étouffé...
+ J'avais tort... Je voulais fuir...[1205][000F]
+ le poids de mes crimes...[1205][000F] sinon
+ j'étouffais...
```

### 🔹 `script_371.json` — ID 83 | **Membre du Cercle masqué**
- **Catégorie :** Restauration d'opcode critique *(Budget alloué : 100 octets)*

```diff
- Uuugghhh... Aaaaghhh...
+ Uuugh...[1205][000A] Aaagh...
```

### 🔹 `script_373.json` — ID 172 | **Membre du Cercle masqué**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 268 octets)*

```diff
- Hahaha! [1205][000F]C'est ça, brûlez! Brûlez!
- Le Joker m'a donné mon poste de
- président, mais ça ne me suffisait pas.
+ Hahaha ![1205][000F] C'est ça, brûle ![1205][000F] Brûle !
+ Le Joker m'a nommé président, mais
+ ça ne me suffisait pas.
```

### 🔹 `script_373.json` — ID 176 | **Membre du Cercle masqué**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 150 octets)*

```diff
- Hahaha, as-tu vu comment
- Smile Hirasaka a brûlé?
+ Hahaha, t'as vu brûler le Smile Hirasaka ?
```

### 🔹 `script_373.json` — ID 179 | **Membre du Cercle masqué**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 320 octets)*

```diff
- In Lak'ech... Haha, formidable! Ce monde
- morne va tomber et on entamera une nouvelle
- voie en transhumains: l'idéal de l'homme!
- Haha!
+ L'In Lak'ech... Haha, parfait ! Ce monde
+ morne prendra fin, place aux transhumains,
+ l'idéal humain ! Haha !
```

### 🔹 `script_375.json` — ID 107 | **Génie de Sumaru**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 510 octets)*

```diff
- Le karma humain...[1205][000F] Émotions refoulées... La
- carte présage une baisse de votre chance en
- argent. [E3][E4][NULL][NULL]"Génie Sumaru Pour lesprochains
- temps, vous serez compté parmi les pauvres,
- contraint de vivre dans la misère.
+ Le karma humain...[1205][000F] Émotions refoulées... La
+ carte présage une baisse de vos finances.[1205][000F]
+ [E3][E4][NULL][NULL]"Génie de Sumaru
+ Bientôt, vous serez parmi les pauvres,
+ contraint de vivre dans la misère.
```

### 🔹 `script_375.json` — ID 127 | **Génie de Sumaru**
- **Catégorie :** Restauration d'opcode critique *(Budget alloué : 226 octets)*

```diff
- Partager des histoires n'est pas
- ma vocation. Aussi ]Aussi n'ai-je
- aucun désir de contrepartie.
+ Partager des récits n'est pas ma vocation.[1205][000F]
+ Je n'ai donc nul désir de récompense.
```

### 🔹 `script_375.json` — ID 194 | **Chauffeur hargneux**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 328 octets)*

```diff
- Y'a un type qui copie mon style, mais j'le
- vois plus trop depuis un moment, alors
- j'suis venu le chercher.[1205][000F] T'aurais pas
- entendu parler de lui ?
+ Un type copie mon style, mais je le vois
+ plus. Je suis venu le chercher.[1205][000F] T'es au
+ courant de quelque chose, toi ?
```

### 🔹 `script_376.json` — ID 58 | **Génie de Sumaru**
- **Catégorie :** Nettoyage accident d'édition (texte parasite collé) *(Budget alloué : 234 octets)*

```diff
- Bientôt, la fortune t'accompgnera et tu
- vivras dans le bohnneur. [E4][NULL][NULL]"Génie Sumaru,
- colporteuse de rumeurs Oui... Je vois... Ton
- destin se cristalise... Hmm... C'est... La
- Tempérance...
+ Bientôt, la fortune t'accompagnera
+ et tu vivras dans le bonheur.
```

### 🔹 `script_376.json` — ID 72 | **Génie de Sumaru**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 510 octets)*

```diff
- Le karma... Les émotions réprimées...[1205][000F] Ta
- chance financière baissera. [E3][E4][NULL][NULL]"Génie Sumaru,
- colporteuse de rumeurs Bientôt,tu seras
- parmi les pauvres, contraint de vivre dans
- la faim et la misère.
+ Le karma humain...[1205][000F] Émotions refoulées... La
+ carte présage une baisse de vos finances.[1205][000F]
+ [E3][E4][NULL][NULL]"Génie de Sumaru
+ Bientôt, tu seras parmi les pauvres,
+ contraint de vivre dans la misère.
```

### 🔹 `script_376.json` — ID 121 | **Membre du Cercle masqué**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 240 octets)*

```diff
- Tu sais ce que ça veut dire? En tant que
- [1205][000F]politicien, je serai l'homme le plus
- puissant du monde! Mwahahaha! Message de
- debug. Vous ne devriez pas me voir. Reset du
- BIT voyance.
+ Tu sais ce que ça veut dire ?[1205][000F] En politique,
+ je serai le plus puissant ![1205][000F] Wahaha !
```

### 🔹 `script_376.json` — ID 122 | **Homme malveillant**
- **Catégorie :** Restauration d'opcode critique *(Budget alloué : 316 octets)*

```diff
- Je bosse à Sumaru TV, et un collègue est un
- vrai trouillard. à la 205]la vieille usine
- abandonnée je lui ai raconté une histoire
- flippante.
+ Je bosse à Sumaru TV, et un collègue est un
+ trouillard.[1205][000F] À la vieille usine, je lui ai
+ raconté une histoire effrayante.
```

### 🔹 `script_376.json` — ID 124 | **Homme malveillant**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 304 octets)*

```diff
- Et comme je le pensais, ce qu'il a imaginé
- l'a terrorisé. Il est devenu blanc comme un
- linge ![1205][000F] Hihi... Ahaha ! Ça me fait encore
- rire !
+ Et comme prévu, il a flippé et est
+ devenu blanc comme un linge ![1205][000F]
+ Hihi... Ahaha ! J'en ris encore !
```

### 🔹 `script_377.json` — ID 24 | **Trish**
- **Catégorie :** Nettoyage accident d'édition (texte parasite collé) *(Budget alloué : 266 octets)*

```diff
- Mes tarifs dépendent de la valeur du marché
- pour les soins, mais je soigne tout le
- monde, donc tu pourras économiser unpeu au
- final. Erreur Aucun BIT de saut. Contactez
- Kanada, ou plutôt votre chef QA.
+ Mes tarifs suivent le cours du marché,
+ mais je soigne tout le monde, tu y gagnes
+ sur la durée !
```

### 🔹 `script_377.json` — ID 34 | **Trish**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 218 octets)*

```diff
- D'accord! Douleur, douleur, va-t'... Hé!
- T'as pas assez d'argent! Reviens quand tes
- poches seront pleines! Erreur Aucun BIT de
- saut. Contactez Kanada, ou plutôt votre chef
- QA.
+ Douleur, disparais... Hé mais
+ t'as pas un sou ! Reviens quand ton larfeuille
+ sera plus garni !
```

### 🔹 `script_377.json` — ID 36 | **Jun**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 242 octets)*

```diff
- O-Oh, elle fait payer...[1205][000F] Bien sûr...
- Compréhensible...[1205][000F] Un peu d'argent en
- échange de la santé, c'est raisonnable.
+ O-Oh, c'est payant...[1205][000F] Bien sûr...
+ Normal...[1205][000F] Que vaut un peu d'argent
+ en échange de la santé ?
```

### 🔹 `script_378.json` — ID 15 | **Maya**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 490 octets)*

```diff
- La relation de Lisa avec son père est
- tendue. Quelle charge d'avoir un enfant si
- rebelle. Le pauvre homme.[E1][E2] [E3][E4][NULL][NULL]"Yukino Mon père
- est parti avec une autre femme...[1205][001E]Je lui casserais la gueule si je le
- revoyais.
+ Lisa a l'air d'avoir des soucis avec son père.[1205][001E]
+ Quelle famille difficile...
+ [E1][E2]
+ [E3][E4][NULL][NULL]"Yukino
+ Mon père est parti avec une autre femme...
```

### 🔹 `script_378.json` — ID 24 | **Père de Ginko**
- **Catégorie :** Nettoyage accident d'édition (texte parasite collé) *(Budget alloué : 210 octets)*

```diff
- Le tirage au sort? Ah oui, bien sûr. Ceci a
- été livré ici. Tenez, prenez-le. Lettre
- [NULL][NULL]Merci d'avoir participé à notre tirage.
- Malheureusement, vous n'êtes pas
- gagnantcette fois. Tentez à nouveau votre
- chance![NULL][NULL]
+ Le tirage au sort ? Ah, oui, bien sûr.
+ On l'a reçu ici. Tenez, prenez-le.
```

### 🔹 `script_378.json` — ID 25 | **Père de Ginko**
- **Catégorie :** Nettoyage accident d'édition (texte parasite collé) *(Budget alloué : 210 octets)*

```diff
- Le tirage au sort? Ah oui, bien sûr. Ceci a
- été livré ici. Tenez, prenez-le. Lettre
- [NULL][NULL]Merci d'avoir participé à notre tirage.
- Félicitations! Vous avez été
- sélectionnégagnant! [NULL][NULL]Veuillez accepter ceci [E4][NULL][NULL][NULL][E4][NULL][NULL]
- en guise de prix. Tentez à nouveau votre
- chance![NULL][NULL] Vous n'avez plus de place pour un
- autre [E4][NULL][NULL][NULL][E4][NULL][NULL]...
+ Le tirage au sort ? Ah, oui, bien sûr.
+ On l'a reçu ici. Tenez, prenez-le.
```

### 🔹 `script_379.json` — ID 22 | **Igor**
- **Catégorie :** Calibrage menu à choix *(Budget alloué : 290 octets)*

```diff
- Je vous écoute.
- [1208][0007]Bases d'invocation
- Changement mystique
- Mutation
- Contact
- Personnalité des démons
- Page préc.
- [1210][B_00][U+5501][B_00]Sélection cachée/retour[SP][SP][SP][SP]
+ Je vous écoute.
+ [1208][0007]Bases d'invocation
+ Changement mystique
+ Mutation
+ Contact
+ Personnalité des démons
+ Page préc.
+ [1210][B_00][U+5501][B_00]Choix caché/retour
```

### 🔹 `script_379.json` — ID 78 | **Igor**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 172 octets)*

```diff
- Si vous le souhaitez, je peux ajouter
- des Cartes Encens lors d'une invocation.
+ Si vous voulez, je peux ajouter
+ des Cartes Encens lors d'une invocation.
```

### 🔹 `script_379.json` — ID 172 | **Igor**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 212 octets)*

```diff
- Je vais transformer cet aspect
- qui a combattu à vos côtés en [E4][NULL][NULL][0004][120E][0001][121D][0001]
- et vous le rendre... a obtenu [E4][NULL][NULL].
+ Je vais transformer cet aspect
+ qui a combattu à vos côtés en [E4][NULL][NULL][0004][120E][0001][121D][0001]
+ et vous le rendre...
```

### 🔹 `script_379.json` — ID 178 | **Igor**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 188 octets)*

```diff
- Il semble que vous n'ayez pas la [E4][NULL][NULL][0006]Carte
- Matériaux[E4][NULL][NULL][0002] requise pour invoquer ce Persona.
+ Vous n'avez pas la [E4][NULL][NULL][0006]Carte Matériaux[E4][NULL][NULL][0002]
+ requise pour invoquer ce Persona.
```

### 🔹 `script_380.json` — ID 24 | **Homme ordinaire**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 186 octets)*

```diff
- Elle était espionne, et moi son garde
- du corps !? C'est riche ! Ahahaha !
+ Elle espionne, et moi son garde
+ du corps !? C'est trop drôle ! Ahaha !
```

### 🔹 `script_381.json` — ID 49 | **Chef Todoroki**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 110 octets)*

```diff
- Vous n'avez pas les moyens
- pour mes honoraires.
+ Vous n'avez pas de quoi me payer.
```

### 🔹 `script_387.json` — ID 7 | **Jun**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 252 octets)*

```diff
- On dirait que le Bataillon [1205][000F]ne s'en est même
- pas servi. C'est comme s'il était conçu
- spécialement pour nous... Se téléporter à
- Seven?[SP][SP] OuiNon
+ Étrange...[1205][000F] On dirait que le Bataillon
+ ne s'en est pas servi.[1205][000F] Comme s'ils l'avaient
+ laissé pour nous...
```

### 🔹 `script_387.json` — ID 15 | **Ginko**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 42 octets)*

```diff
- Aaaaaaaaah !
+ Aaaaaaaah!
```

### 🔹 `script_388.json` — ID 2 | **Eikichi**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 252 octets)*

```diff
- Il est probablement dans la salle du
- conseil étudiant au deuxième étage. Je vais
- lui faire cracher ses aveux ! Allons-y !
+ Il doit être en salle du conseil au
+ deuxième. Je vais lui faire cracher le
+ morceau ! Allons-y !
```

### 🔹 `script_390.json` — ID 92 | **Mitsugi l'ouvreuse**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 188 octets)*

```diff
- Palme d'Argent, Ours d'Or, et notre plus
- haute distinction, le Lion de Platine.
+ Palme d'argent, Ours d'or et le prix
+ suprême : le Lion de platine.
```

### 🔹 `script_390.json` — ID 96 | **Mitsugi l'ouvreuse**
- **Catégorie :** Calibrage menu à choix *(Budget alloué : 174 octets)*

```diff
- Votre billet: [120E][NULL] yens.
- Ça vous convient?
- [1208][0002]Oui
- Non
+ Votre billet : [120E][NULL] yens.
+ Prendre le billet ?
+ [1208][0002]Oui
+ Non
```

### 🔹 `script_390.json` — ID 97 | **Mitsugi l'ouvreuse**
- **Catégorie :** Calibrage menu à choix *(Budget alloué : 174 octets)*

```diff
- Votre billet: [120E][NULL] yens.
- Ça vous convient?
- [1208][0002]Oui
- Non
+ Votre billet : [120E][NULL] yens.
+ Prendre le billet ?
+ [1208][0002]Oui
+ Non
```

### 🔹 `script_391.json` — ID 7 | **Mitsugi l'ouvreuse**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 254 octets)*

```diff
- ... Quoi? Mon service impeccable
- et mes excellentes explications ne
- vous suffisent pas? Vous plaisantez?
+ ...Quoi ? Mon service parfait et mes
+ explications ne vous suffisent pas ?
+ Vous plaisantez ?
```

### 🔹 `script_391.json` — ID 9 | **Mitsugi l'ouvreuse**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 286 octets)*

```diff
- Merci pour votre travail! Je vous ai
- observé. Impressionnant! Laissez-moi
- débloquer un nouveau mode. [NULL][NULL]BGM[NULL][NULL]ajouté à la
- Galerie.
+ Merci pour votre travail ! Je vous ai
+ observé, c'est impressionnant ! Laissez-moi
+ débloquer un nouveau mode.
```

### 🔹 `script_391.json` — ID 12 | **Mitsugi l'ouvreuse**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 248 octets)*

```diff
- En attendant, je vous attends
- pour votre prochaine séance de
- cinéma. Eeeeet... Fondu au noir !
+ Je vous attends pour votre prochaine séance
+ de cinéma.
+ Eeeet... Fondu au noir !
```

### 🔹 `script_392.json` — ID 3 | **Eikichi**
- **Catégorie :** Correction / Réécriture fidèle *(Budget alloué : 254 octets)*

```diff
- C'est...[1205][0014] si précieux... Plus doux qu'avec
- [1113]ou Ginko...[1205][0014] Comme un câlin de ma mère...
+ C'est...[1205][0014] si précieux... Plus doux qu'avec
+ [1113] ou Ginko...[1205][0014]
+ Comme un câlin de ma mère...
```

### 🔹 `script_394.json` — ID 18 | **Maya**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 168 octets)*

```diff
- Et si je viens, je saurai peut-être
- comment je suis devenue Manieur de Persona.
+ En venant, je saurai peut-être
+ comment je suis devenue Manieur de Persona.
```

### 🔹 `script_394.json` — ID 37 | **Maya**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 182 octets)*

```diff
- *regaaaaaarde*[1205][001E] Mais bon, à part ça,
- [1205][000F][1113]-kun...[1205][001E] On s'est déjà vus quelque part?
+ *regard fixe*[1205][001E] Mais à part ça,
+ [1113]-kun...[1205][001E] On s'est déjà vus quelque part ?
```

### 🔹 `script_394.json` — ID 39 | **Yukino**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 242 octets)*

```diff
- C'est une surprise.[1205][001E] Je savais pas
- qu'il y avait d'autres Manieur de
- Persona...[1205][001E] En dehors de mes anciens amis.
+ Quelle surprise.[1205][001E] J'ignorais qu'il
+ y avait d'autres Manieurs de Persona...
+ [1205][001E]À part mes vieux potes.
```

### 🔹 `script_394.json` — ID 49 | **Maya**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 134 octets)*

```diff
- Oooh ! Trop cooool, Yukki !
- Hé, regardez mon super talent !
+ Oooh ! Trop cool, Yukki !
+ Hé, regardez mon super talent !
```

### 🔹 `script_395.json` — ID 6 | **Eikichi**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 52 octets)*

```diff
- Euh...[1205][000F] Ginko?
+ Euh...[1205][000F] Lisa
```

### 🔹 `script_395.json` — ID 8 | **Ginko**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 72 octets)*

```diff
- Attends... Hein ?[1205][000F] C'est...?
+ Attends...[1205][000F] C'est... ?
```

### 🔹 `script_396.json` — ID 16 | **Lisa**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 194 octets)*

```diff
- H-Hey, Boss des calbutes![1205][001E] Je connais bien
- Miyabi...[1205][001E] C'était quoi ta relation avec elle?
+ H-Hé, Boss calbute ![1205][001E] Je connais bien
+ Miyabi...[1205][001E] C'était quoi ta relation avec elle ?
```

### 🔹 `script_396.json` — ID 18 | **Ginko**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 196 octets)*

```diff
- H-Hey, Boss des calbutes![1205][001E] Je connais bien
- Miyabi...[1205][001E] C'était quoi ta relation avec elle?
+ H-Hé, Boss calbute ![1205][001E] Je connais bien
+ Miyabi...[1205][001E] C'était quoi ta relation avec elle ?
```

### 🔹 `script_396.json` — ID 31 | **Ginko**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 160 octets)*

```diff
- Hmm...[1205][001E] Je n'ai pas le temps pour
- ça, je les laisserai pour l'instant.
+ Hmm...[1205][001E] Pas le temps pour ça,
+ je les laisse en paix pour l'instant.
```

### 🔹 `script_396.json` — ID 54 | **Rédacteur du journal scolaire**
- **Catégorie :** Élagage stylistique & concision *(Budget alloué : 284 octets)*

```diff
- J'ignorais que notre rédactrice et
- Boss des calbutes étaient ensemble...
- Quel destin! Un scoop énorme! Hmmm...
+ J'ignorais que notre chef et le Boss
+ des calbutes étaient ensemble...
+ Quel destin ! Quel scoop ! Hmmm...
```

# Audio Lab : interface web

Sources React (Vite + Tailwind) de l'Audio Lab. Le build va dans `../server/dist/`,
le dossier servi par `server_audio.py` (ignoré par git).

```bash
cd labs/audio/web
npm install
npm run build
```

Tous les textes affichés sont dans `src/dict.js` (FR et EN) et passent par `t('clé')`.
Une chaîne écrite en dur dans un composant ne change pas de langue avec le bouton FR/EN.

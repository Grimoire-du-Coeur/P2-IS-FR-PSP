## 📺 Vidéo de présentation
🎬 **[Clique ici pour voir la vidéo](https://youtu.be/wxEEJYjx2Sw)**

![Miniature](https://img.youtube.com/vi/wxEEJYjx2Sw/maxresdefault.jpg)

---

# 🛠️ Toolkit de Traduction

Ce document explique comment fonctionne le tool Python, utile pour extraire, traduire et reconstruire l'ISO de Persona 2: Innocent Sin.

---

### ⚙️ Pipeline complet de l'outil

```
ISO (ULES01557)
    │
    ▼  extract_cpk_from_iso()
P2PT_ALL.cpk
    │
    ▼  extract_event_from_cpk()
event.bin
    │
    ▼  extract_scripts_from_event()
script_0.bin … script_398.bin
    │
    ▼  decode_all_scripts()
script_0.json … script_398.json   ← ✏️ on traduit ici
    │
    ▼  encode_script()
script_0_fr.bin … script_398_fr.bin
    │
    ▼  rebuild_iso()
ISO traduite ✅
```

---

### Installation
```bash
git clone https://github.com/chenetulipe/P2-FR-IS-PSP
cd P2-FR-IS-PSP
pip install customtkinter
python p2is_tool.py
```

---

### Utilisation
Lance `p2is_tool.py` et suis les 3 onglets dans l'ordre :
1. **Pipeline Extraction** - charge ton ISO et extrais les scripts en JSON
2. **Traduction** - encode tes JSON traduits en `.bin`
3. **Rebuild ISO** - réinjecte tout et génère l'ISO FR jouable
   
---

### Outil dédié au projet
- [JsonVerify](https://github.com/Garloulou/JsonVerify) par **@Garloulou** - outil de validation des fichiers JSON traduits

### Outils tiers utilisés
- [UMDGen](https://www.romhacking.net/utilities/1218/) - manipulation ISO PSP
- [CriFsLib](https://github.com/Sewer56/CriFsV2Lib) - extraction CPK
- [PPSSPP](https://www.ppsspp.org/) - émulation PSP pour les tests
  
---

### Inspirations & Références
- [P2-EP-PSP](https://github.com/sayucchin/P2-EP-PSP) par **sayucchin & équipe** -
  projet de traduction de Persona 2: Eternal Punishment PSP.
  L'analyse de leur code source (event.rs, main.rs) nous a permis de comprendre la structure de event.bin (gzip + table d'offsets). Nos outils ont été développés indépendamment en Python.

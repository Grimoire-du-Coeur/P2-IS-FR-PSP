import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Folder, Database, RefreshCcw, Download, CheckCircle, AlertTriangle, File, Wrench, Search, FileText, Languages } from 'lucide-react';

const dict = {
  fr: {
    title: "Persona 2 IS Outil de Traduction",
    work_dir: "Dossier de travail",
    iso_file: "Fichier ISO Original (.iso)",
    crifs_path: "Chemin vers CriFsLib.GUI.exe :",
    browse: "Parcourir...",
    tab1: "① Extraction",
    tab2: "② Traduction",
    tab3: "③ Encodage",
    tab4: "④ Rebuild ISO",
    step_a: "Extraction du CPK",
    desc_a: "Extrait l'archive P2PT_ALL.cpk depuis l'ISO originale.",
    btn_a: "Extraire P2PT_ALL.cpk",
    step_b: "Extraction des fichiers du jeu (CriFsLib)",
    desc_b: "1. Ouvrez CriFsLib.\n2. Ouvrez le dossier de travail.\n3. Glissez P2PT_ALL.cpk dans CriFsLib.\n4. Clic-droit : Extract All vers `cpk_files/`.",
    btn_b: "Ouvrir CriFsLib",
    btn_b2: "Dossier de travail",
    step_c: "Extraction des scripts principaux",
    desc_c: "Extrait le fichier event.bin qui contient le scénario.",
    btn_c: "Extraire event.bin",
    step_d: "Séparation des scripts",
    desc_d: "Découpe event.bin en 399 fichiers .bin individuels.",
    btn_d: "Séparer en 399 scripts",
    step_e: "Génération des fichiers de scénario",
    desc_e: "Convertit les 399 scripts binaires en fichiers JSON traduisibles.",
    btn_e: "Décoder les scripts en JSON",
    step_f: "Génération des fichiers annexes",
    desc_f: "Convertit F_BE (Combats), TM_EVE (Scènes), MMAP (PNJs) et CD_SHOP.",
    btn_f: "Extraire F_BE, MMAP, TM_EVE...",
    step_g: "Vérification de cohérence (Optionnel)",
    desc_g: "Vérifie que les menus de choix sont correctement traduits.",
    btn_g: "Vérifier les menus",
    tab3_title: "Encodage des traductions",
    tab3_desc: "Convertit vos textes modifiés (JSON) vers le format du jeu.",
    tab3_warn: "Les fichiers laissés vides dans le dossier traduction resteront automatiquement en anglais.",
    btn_h: "Lancer l'Encodage Complet",
    tab4_title: "Création de l'ISO",
    tab4_desc: "Patche vos nouveaux fichiers dans l'ISO originale pour créer le jeu traduit.",
    btn_i: "Créer P2IS_FR.iso",
    log_title: "Journal d'Événements",
    status_ready: "Prêt",
    status_running: "En cours...",
    status_done: "Terminé !",
    status_error: "Erreur",
    log_empty: "Aucune action récente.",
    log_clear: "Vider le journal",
    progress: "Progression"
  },
  en: {
    title: "Persona 2 IS Translation Tool",
    work_dir: "Working Directory",
    iso_file: "Original ISO File (.iso)",
    crifs_path: "CriFsLib.GUI.exe Path :",
    browse: "Browse...",
    tab1: "① Extraction",
    tab2: "② Translation",
    tab3: "③ Encoding",
    tab4: "④ Rebuild ISO",
    step_a: "Extract CPK",
    desc_a: "Extracts the P2PT_ALL.cpk archive from the original ISO.",
    btn_a: "Extract P2PT_ALL.cpk",
    step_b: "Extract game files (CriFsLib)",
    desc_b: "1. Open CriFsLib.\n2. Open the working directory.\n3. Drag P2PT_ALL.cpk into the window.\n4. Right-click: Extract All to `cpk_files/`.",
    btn_b: "Open CriFsLib",
    btn_b2: "Working Directory",
    step_c: "Extract main scripts",
    desc_c: "Extracts event.bin containing the scenario.",
    btn_c: "Extract event.bin",
    step_d: "Split scripts",
    desc_d: "Splits event.bin into 399 individual .bin files.",
    btn_d: "Split into 399 scripts",
    step_e: "Generate scenario files",
    desc_e: "Converts 399 binary scripts into translatable JSON files.",
    btn_e: "Decode scripts to JSON",
    step_f: "Generate secondary files",
    desc_f: "Converts F_BE (Battles), TM_EVE (Cutscenes), MMAP (NPCs) and CD_SHOP.",
    btn_f: "Extract F_BE, MMAP, TM_EVE...",
    step_g: "Consistency Check (Optional)",
    desc_g: "Verifies that choice menus are properly translated.",
    btn_g: "Verify menus",
    tab3_title: "Translation Encoding",
    tab3_desc: "Converts your modified texts (JSON) back to the game format.",
    tab3_warn: "Files left empty in the translation folder will automatically remain in English.",
    btn_h: "Run Full Encoding",
    tab4_title: "ISO Creation",
    tab4_desc: "Patches your new files into the original ISO to create the translated game.",
    btn_i: "Create P2IS_FR.iso",
    log_title: "Event Log",
    status_ready: "Ready",
    status_running: "Running...",
    status_done: "Done !",
    status_error: "Error",
    log_empty: "No recent actions.",
    log_clear: "Clear log",
    progress: "Progress"
  }
};

export default function App() {
  const [lang, setLang] = useState('fr');
  const t = (key) => dict[lang][key];

  const [activeTab, setActiveTab] = useState('1');
  const [workDir, setWorkDir] = useState('');
  const [isoPath, setIsoPath] = useState(''); // Empty by default
  const [crifsPath, setCrifsPath] = useState('');
  const [pspdecryptPath, setPspdecryptPath] = useState('');
  
  const [status, setStatus] = useState('');
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(-1); // -1 means hidden
  
  const logEndRef = useRef(null);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/default-paths')
      .then(r => r.json())
      .then(data => {
        if (!workDir) setWorkDir(data.work_dir);
      })
      .catch(console.error);
  }, []);

  // Auto-scroll for logs
  useEffect(() => {
    logEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [logs]);

  // Progress Polling
  useEffect(() => {
    let interval;
    if (loading) {
      interval = setInterval(async () => {
        try {
          const res = await fetch('http://127.0.0.1:8000/api/progress');
          const data = await res.json();
          if (data.current >= 0) {
            setProgress(data.current);
          }
        } catch(e) {}
      }, 500);
    } else {
      setProgress(-1);
    }
    return () => clearInterval(interval);
  }, [loading]);

  const addLog = (msg, type = "INFO") => {
    const time = new Date().toLocaleTimeString();
    setLogs(l => [...l, { time, msg, type }]);
  };

  const browse = async (type, ext = "") => {
    try {
      const res = await fetch(`http://127.0.0.1:8000/api/browse`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ type, ext })
      });
      const data = await res.json();
      if (data.path) {
        if (type === 'dir') setWorkDir(data.path);
        else if (ext === '.iso') setIsoPath(data.path);
        else if (ext === '.exe') {
          if (data.path.toLowerCase().includes('decrypt')) setPspdecryptPath(data.path);
          else setCrifsPath(data.path);
        }
      }
    } catch (e) {
      addLog(`Browse error: ${e.message}`, "ERROR");
    }
  };

  const callApi = async (endpoint, payload) => {
    setLoading(true);
    setStatus(t('status_running'));
    setProgress(0);
    addLog(`[${endpoint}] started...`, "INFO");
    try {
      const res = await fetch(`http://127.0.0.1:8000/api/${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      if (res.ok) {
        setStatus(t('status_done'));
        const msgStr = typeof data.result === 'object' ? JSON.stringify(data.result) : (data.msg || data.result || 'Success.');
        addLog(msgStr, "OK");
      } else {
        setStatus(t('status_error'));
        addLog(data.detail, "ERROR");
      }
    } catch (e) {
      setStatus(t('status_error'));
      addLog(e.message, "ERROR");
    }
    setLoading(false);
    setProgress(-1);
  };

  const tabs = [
    { id: '1', name: t('tab1'), icon: <Download size={18} /> },
    { id: '2', name: t('tab2'), icon: <Database size={18} /> },
    { id: '3', name: t('tab3'), icon: <RefreshCcw size={18} /> },
    { id: '4', name: t('tab4'), icon: <CheckCircle size={18} /> }
  ];

  return (
    <div className="min-h-screen text-white p-8">
      {/* Header */}
      <motion.div 
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-6xl mx-auto mb-8 relative flex flex-col items-center justify-center"
      >
        <h1 className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-300 to-cyan-100">
          {t('title')}
        </h1>
        
        {/* Language Toggle */}
        <button 
          onClick={() => setLang(lang === 'fr' ? 'en' : 'fr')}
          className="absolute right-0 top-0 bg-white/10 hover:bg-white/20 border border-white/20 rounded-full px-4 py-2 flex items-center space-x-2 transition-all cursor-pointer shadow-lg"
        >
          <Languages size={18} className="text-blue-300" />
          <span className="font-semibold text-sm tracking-wide">{lang === 'fr' ? 'FR' : 'EN'}</span>
        </button>
      </motion.div>

      <div className="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Main Panel */}
        <motion.div 
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="lg:col-span-2 glass-panel p-6 flex flex-col min-h-[600px]"
        >
          {/* Navigation */}
          <div className="flex space-x-2 mb-6 p-1 bg-black/20 rounded-xl overflow-x-auto">
            {tabs.map(tb => (
              <button
                key={tb.id}
                onClick={() => setActiveTab(tb.id)}
                className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-all ${
                  activeTab === tb.id 
                    ? 'bg-blue-500/30 text-blue-100 shadow-lg border border-blue-400/30' 
                    : 'text-blue-200/50 hover:bg-white/5 hover:text-white'
                }`}
              >
                {tb.icon}
                <span className="whitespace-nowrap">{tb.name}</span>
              </button>
            ))}
          </div>

          {/* Configuration */}
          <div className="mb-6 space-y-4 bg-black/10 p-4 rounded-xl border border-white/5">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="flex flex-col">
                <label className="text-xs text-blue-200/70 mb-1 font-semibold uppercase tracking-wider">{t('work_dir')}</label>
                <div className="flex items-center space-x-2">
                  <input type="text" value={workDir} onChange={e => setWorkDir(e.target.value)} className="glass-input flex-1" />
                  <button onClick={() => browse('dir')} className="p-2 bg-blue-500/20 hover:bg-blue-500/40 border border-blue-500/30 rounded-lg text-blue-200 transition-colors cursor-pointer" title={t('browse')}><Folder size={20} /></button>
                </div>
              </div>
              
              <div className="flex flex-col">
                <label className="text-xs text-blue-200/70 mb-1 font-semibold uppercase tracking-wider">{t('iso_file')}</label>
                <div className="flex items-center space-x-2">
                  <input type="text" value={isoPath} onChange={e => setIsoPath(e.target.value)} className="glass-input flex-1" />
                  <button onClick={() => browse('file', '.iso')} className="p-2 bg-blue-500/20 hover:bg-blue-500/40 border border-blue-500/30 rounded-lg text-blue-200 transition-colors cursor-pointer" title={t('browse')}><File size={20} /></button>
                </div>
              </div>
            </div>

            {/* CriFsLib Path only in Tab 1 */}
            <AnimatePresence>
              {activeTab === '1' && (
                <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }} exit={{ height: 0, opacity: 0 }} className="flex flex-col pt-2 border-t border-white/5">
                  <div className="flex justify-between items-center mb-1 mt-3">
                    <label className="text-xs text-blue-200/70 font-semibold uppercase tracking-wider">Chemin vers pspdecrypt.exe (Optionnel)</label>
                    <a href="https://github.com/John-K/pspdecrypt/releases" target="_blank" rel="noopener noreferrer" className="text-xs text-blue-400 hover:text-blue-300 flex items-center space-x-1">
                      <Download size={12} />
                      <span>Télécharger pspdecrypt</span>
                    </a>
                  </div>
                  <div className="flex items-center space-x-2">
                    <input type="text" value={pspdecryptPath} onChange={e => setPspdecryptPath(e.target.value)} className="glass-input flex-1" placeholder="C:/.../pspdecrypt.exe" />
                    <button onClick={() => browse('file', '.exe')} className="p-2 bg-blue-500/20 hover:bg-blue-500/40 border border-blue-500/30 rounded-lg text-blue-200 transition-colors cursor-pointer" title={t('browse')}><File size={20} /></button>
                  </div>
                  
                  <div className="flex justify-between items-center mb-1 mt-3">
                    <label className="text-xs text-blue-200/70 font-semibold uppercase tracking-wider">{t('crifs_path')}</label>
                    <a href="https://github.com/Sewer56/CriFsV2Lib/releases" target="_blank" rel="noopener noreferrer" className="text-xs text-blue-400 hover:text-blue-300 flex items-center space-x-1">
                      <Download size={12} />
                      <span>Télécharger CriFsV2Lib</span>
                    </a>
                  </div>
                  <div className="flex items-center space-x-2">
                    <input type="text" value={crifsPath} onChange={e => setCrifsPath(e.target.value)} className="glass-input flex-1" />
                    <button onClick={() => browse('file', '.exe')} className="p-2 bg-blue-500/20 hover:bg-blue-500/40 border border-blue-500/30 rounded-lg text-blue-200 transition-colors cursor-pointer" title={t('browse')}><File size={20} /></button>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          {/* Progress Bar (Visible if loading and progress >= 0) */}
          <AnimatePresence>
            {loading && progress >= 0 && (
              <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }} className="mb-4">
                <div className="flex justify-between text-xs mb-1 text-blue-200">
                  <span>{t('progress')}</span>
                  <span>{progress}%</span>
                </div>
                <div className="w-full bg-black/40 rounded-full h-2 overflow-hidden border border-white/5">
                  <motion.div 
                    className="bg-blue-500 h-2 rounded-full"
                    initial={{ width: 0 }}
                    animate={{ width: `${progress}%` }}
                    transition={{ duration: 0.2 }}
                  />
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          <div className="flex-1 bg-black/20 rounded-xl p-6 border border-white/5 relative overflow-hidden">
            <div className="absolute top-[-50px] right-[-50px] w-64 h-64 bg-blue-500/10 rounded-full blur-3xl pointer-events-none"></div>

            <AnimatePresence mode="wait">
              {activeTab === '1' && (
                <motion.div key="1" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="space-y-6 relative z-10">
                  
                  {/* Etape A */}
                  <div className="bg-white/5 border border-white/10 rounded-xl p-4">
                    <h3 className="font-semibold text-lg text-blue-100 flex items-center space-x-2 mb-2">
                      <span className="bg-blue-500/20 text-blue-300 px-2 rounded">A</span> 
                      <span>{t('step_a')}</span>
                    </h3>
                    <p className="text-sm text-blue-200/70 mb-3">{t('desc_a')}</p>
                    <button onClick={() => callApi('extract-cpk', { iso_path: isoPath, work_dir: workDir, pspdecrypt_path: pspdecryptPath })} disabled={loading} className="glass-button text-sm flex items-center space-x-2">
                      <Download size={16} /> <span>{t('btn_a')}</span>
                    </button>
                  </div>

                  {/* Etape B */}
                  <div className="bg-white/5 border border-white/10 rounded-xl p-4">
                    <h3 className="font-semibold text-lg text-blue-100 flex items-center space-x-2 mb-2">
                      <span className="bg-blue-500/20 text-blue-300 px-2 rounded">B</span> 
                      <span>{t('step_b')}</span>
                    </h3>
                    <p className="text-sm text-blue-200/70 mb-3 whitespace-pre-line">{t('desc_b')}</p>
                    <div className="flex flex-col sm:flex-row gap-3">
                      <button onClick={() => callApi('open-crifslib', { crifs_path: crifsPath })} disabled={loading} className="glass-button text-sm flex items-center space-x-2 flex-1 justify-center">
                        <Wrench size={16} /> <span>{t('btn_b')}</span>
                      </button>
                      <button onClick={() => fetch('http://127.0.0.1:8000/api/open-folder', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ work_dir: workDir })})} className="glass-button text-sm flex items-center space-x-2 flex-1 justify-center bg-blue-800/30">
                        <Folder size={16} /> <span>{t('btn_b2')}</span>
                      </button>
                    </div>
                  </div>

                  {/* Etape C */}
                  <div className="bg-white/5 border border-white/10 rounded-xl p-4">
                    <h3 className="font-semibold text-lg text-blue-100 flex items-center space-x-2 mb-2">
                      <span className="bg-blue-500/20 text-blue-300 px-2 rounded">C</span> 
                      <span>{t('step_c')}</span>
                    </h3>
                    <p className="text-sm text-blue-200/70 mb-3">{t('desc_c')}</p>
                    <button onClick={() => callApi('extract-event', { work_dir: workDir })} disabled={loading} className="glass-button text-sm flex items-center space-x-2">
                      <FileText size={16} /> <span>{t('btn_c')}</span>
                    </button>
                  </div>

                  {/* Etape D */}
                  <div className="bg-white/5 border border-white/10 rounded-xl p-4">
                    <h3 className="font-semibold text-lg text-blue-100 flex items-center space-x-2 mb-2">
                      <span className="bg-blue-500/20 text-blue-300 px-2 rounded">D</span> 
                      <span>{t('step_d')}</span>
                    </h3>
                    <p className="text-sm text-blue-200/70 mb-3">{t('desc_d')}</p>
                    <button onClick={() => callApi('split-scripts', { work_dir: workDir })} disabled={loading} className="glass-button text-sm flex items-center space-x-2">
                      <Search size={16} /> <span>{t('btn_d')}</span>
                    </button>
                  </div>

                </motion.div>
              )}

              {activeTab === '2' && (
                <motion.div key="2" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="space-y-6 relative z-10">
                  {/* Etape E */}
                  <div className="bg-white/5 border border-white/10 rounded-xl p-4">
                    <h3 className="font-semibold text-lg text-blue-100 flex items-center space-x-2 mb-2">
                      <span className="bg-blue-500/20 text-blue-300 px-2 rounded">E</span> 
                      <span>{t('step_e')}</span>
                    </h3>
                    <p className="text-sm text-blue-200/70 mb-3">{t('desc_e')}</p>
                    <button onClick={() => callApi('decode-scripts', { work_dir: workDir })} disabled={loading} className="glass-button text-sm flex items-center space-x-2">
                      <Database size={16} /> <span>{t('btn_e')}</span>
                    </button>
                  </div>
                  
                  {/* Etape F */}
                  <div className="bg-white/5 border border-white/10 rounded-xl p-4">
                    <h3 className="font-semibold text-lg text-blue-100 flex items-center space-x-2 mb-2">
                      <span className="bg-blue-500/20 text-blue-300 px-2 rounded">F</span> 
                      <span>{t('step_f')}</span>
                    </h3>
                    <p className="text-sm text-blue-200/70 mb-2">{t('desc_f')}</p>
                    <button onClick={() => callApi('scan-secondary', { work_dir: workDir })} disabled={loading} className="glass-button text-sm flex items-center space-x-2">
                      <Search size={16} /> <span>{t('btn_f')}</span>
                    </button>
                  </div>
                  
                  {/* Etape G */}
                  <div className="bg-white/5 border border-white/10 rounded-xl p-4">
                    <h3 className="font-semibold text-lg text-blue-100 flex items-center space-x-2 mb-2">
                      <span className="bg-blue-500/20 text-blue-300 px-2 rounded">G</span>
                      <span>Décodage de l'EBOOT</span>
                    </h3>
                    <p className="text-sm text-blue-200/70 mb-3">Convertit l'EBOOT décrypté en JSON traduisible.</p>
                    <button onClick={() => callApi('decode-eboot', { work_dir: workDir })} disabled={loading} className="glass-button text-sm flex items-center space-x-2">
                      <FileText size={16} /> <span>Générer EBOOT_Translation.json</span>
                    </button>
                  </div>
                  
                  {/* Etape H */}
                  <div className="bg-white/5 border border-white/10 rounded-xl p-4">
                    <h3 className="font-semibold text-lg text-blue-100 flex items-center space-x-2 mb-2">
                      <span className="bg-blue-500/20 text-blue-300 px-2 rounded">H</span> 
                      <span>{t('step_g')}</span>
                    </h3>
                    <p className="text-sm text-blue-200/70 mb-3">{t('desc_g')}</p>
                    <button onClick={() => callApi('validate', { work_dir: workDir })} disabled={loading} className="glass-button text-sm flex items-center space-x-2">
                      <CheckCircle size={16} /> <span>{t('btn_g')}</span>
                    </button>
                  </div>
                </motion.div>
              )}

              {/* Tab 3: Encodage */}
              {activeTab === '3' && (
                <motion.div key="3" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="relative z-10">
                  <div className="bg-white/5 border border-white/10 rounded-xl p-4">
                    <h3 className="font-semibold text-lg text-blue-100 flex items-center space-x-2 mb-2">
                      <span className="bg-blue-500/20 text-blue-300 px-2 rounded">I</span>
                      <span>{t('tab3_title')}</span>
                    </h3>
                    <p className="text-sm text-blue-200/70 mb-4">{t('tab3_desc')}</p>
                    
                    <div className="bg-blue-900/20 border border-blue-500/20 rounded-lg p-3 mb-4">
                      <p className="text-xs flex items-start space-x-2">
                        <AlertTriangle size={14} className="text-blue-400 mt-0.5 flex-shrink-0" />
                        <span>{t('tab3_warn')}</span>
                      </p>
                    </div>

                    <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 mb-4">
                      {[
                        { id: 'event', label: 'event.bin' },
                        { id: 'eboot', label: 'EBOOT' },
                        { id: 'cd_shop', label: 'CD_SHOP' },
                        { id: 'f_be', label: 'F_BE' },
                        { id: 'tm_eve', label: 'TM_EVE' },
                        { id: 'mmap01', label: 'MMAP01' },
                        { id: 'mmap02', label: 'MMAP02' },
                        { id: 'mmap03', label: 'MMAP03' },
                        { id: 'mmap04', label: 'MMAP04' },
                        { id: 'mmap05', label: 'MMAP05' },
                        { id: 'mmap06', label: 'MMAP06' }
                      ].map(target => (
                        <button 
                          key={target.id}
                          onClick={() => callApi('encode', { work_dir: workDir, targets: [target.id] })}
                          disabled={loading}
                          className="glass-button py-2 text-xs flex justify-center items-center hover:bg-blue-500/30 transition-all group"
                        >
                          <span className="group-hover:scale-105 transition-transform">{target.label}</span>
                        </button>
                      ))}
                    </div>

                    <button 
                      onClick={() => callApi('encode', { work_dir: workDir })}
                      disabled={loading}
                      className="glass-button w-full flex items-center justify-center space-x-2 py-3 text-md bg-blue-600/20 hover:bg-blue-500/30 border-blue-400/30 group"
                    >
                      {loading ? <RefreshCcw className="animate-spin" /> : <RefreshCcw size={18} className="group-hover:animate-spin" />}
                      <span>{t('btn_h')}</span>
                    </button>
                  </div>
                </motion.div>
              )}

              {/* Tab 4: Rebuild ISO */}
              {activeTab === '4' && (
                <motion.div key="4" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="relative z-10">
                  <div className="bg-white/5 border border-white/10 rounded-xl p-4">
                    <h3 className="font-semibold text-lg text-blue-100 flex items-center space-x-2 mb-2">
                      <span className="bg-blue-500/20 text-blue-300 px-2 rounded">J</span>
                      <span>{t('tab4_title')}</span>
                    </h3>
                    <p className="text-sm text-blue-200/70 mb-4">{t('tab4_desc')}</p>
                    
                    <button 
                      onClick={() => callApi('rebuild', { iso_path: isoPath, work_dir: workDir })}
                      disabled={loading}
                      className="glass-button w-full flex items-center justify-center space-x-2 py-3 text-md bg-green-600/50 hover:bg-green-500/60 border-green-400/30"
                    >
                      {loading ? <RefreshCcw className="animate-spin" /> : <CheckCircle size={18} />}
                      <span>{t('btn_i')}</span>
                    </button>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </motion.div>

        {/* Sidebar Log */}
        <motion.div 
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="glass-panel p-0 flex flex-col min-h-[600px] overflow-hidden bg-gray-900/80"
        >
          <div className="flex justify-between items-center p-4 bg-black/40 border-b border-white/5">
            <h3 className="font-semibold tracking-wider text-sm uppercase text-blue-200">{t('log_title')}</h3>
            <span className={`text-xs px-2 py-1 rounded-full ${loading ? 'bg-yellow-500/20 text-yellow-300' : 'bg-green-500/20 text-green-300'}`}>
              {status || t('status_ready')}
            </span>
          </div>
          
          <div className="flex-1 p-4 font-mono text-sm overflow-y-auto space-y-1">
            {logs.length === 0 ? (
              <p className="text-gray-500 italic">{t('log_empty')}</p>
            ) : (
              logs.map((log, i) => {
                let colorClass = "text-blue-100";
                if (log.type === "ERROR") colorClass = "text-red-400 font-bold bg-red-900/20 px-1 rounded";
                else if (log.type === "WARN") colorClass = "text-yellow-400";
                else if (log.type === "OK") colorClass = "text-green-400 font-semibold";
                
                return (
                  <div key={i} className="leading-relaxed border-b border-white/5 pb-1 mb-1">
                    <span className="text-gray-500 mr-2 select-none text-xs">[{log.time}]</span>
                    <span className={colorClass}>{log.msg}</span>
                  </div>
                );
              })
            )}
            <div ref={logEndRef} />
          </div>
          
          <div className="p-2 bg-black/40 border-t border-white/5 flex justify-end">
            <button 
              onClick={() => setLogs([])}
              className="text-xs text-gray-400 hover:text-white transition-colors px-2 py-1 cursor-pointer"
            >
              {t('log_clear')}
            </button>
          </div>
        </motion.div>
        
      </div>
    </div>
  );
}

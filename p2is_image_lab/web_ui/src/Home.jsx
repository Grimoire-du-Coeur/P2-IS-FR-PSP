import React, { useState } from 'react';
import { BookOpen, Cpu, Info, AlertTriangle, Folder, Disc, Loader } from 'lucide-react';
import { motion } from 'framer-motion';

export default function Home({ t, lang, addLog, browse, isoPath, setIsoPath, workspaceDir, setWorkspaceDir, setActiveTab }) {
  const [isInitializing, setIsInitializing] = useState(false);

  const handleInitProject = async () => {
    if (!isoPath) return alert(lang === 'fr' ? "Veuillez sélectionner un fichier ISO !" : "Please select an ISO file!");
    if (!workspaceDir) return alert(lang === 'fr' ? "Veuillez sélectionner un dossier de travail !" : "Please select a workspace directory!");
    
    setIsInitializing(true);
    addLog(lang === 'fr' ? "Initialisation du projet en cours..." : "Project initialization in progress...", "INFO");

    try {
      const res = await fetch(`http://127.0.0.1:8002/api/project/init`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ iso_path: isoPath, workspace_dir: workspaceDir })
      });
      
      const data = await res.json();
      if (res.ok) {
        addLog(lang === 'fr' ? "Projet initialisé avec succès ! Fichiers extraits." : "Project initialized successfully! Files extracted.", "OK");
        setActiveTab('lab');
      } else {
        addLog(data.detail || (lang === 'fr' ? "Erreur d'initialisation" : "Initialization error"), "ERROR");
        alert(`${lang === 'fr' ? "Erreur" : "Error"} : ${data.detail}`);
      }
    } catch (e) {
      addLog(lang === 'fr' ? "Erreur de connexion au serveur." : "Server connection error.", "ERROR");
    } finally {
      setIsInitializing(false);
    }
  };

  const workflowSteps = [
    t('workflow_step1'),
    t('workflow_step2'),
    t('workflow_step3'),
    t('workflow_step4'),
    t('workflow_step5')
  ];

  const formats = [
    { name: t('fmt_index4_title'), desc: t('fmt_index4_desc') },
    { name: t('fmt_index8_title'), desc: t('fmt_index8_desc') },
    { name: t('fmt_rgba_title'), desc: t('fmt_rgba_desc') },
    { name: t('fmt_swz_title'), desc: t('fmt_swz_desc') }
  ];

  return (
    <motion.div 
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="p-6 bg-gray-900/50 rounded-xl border border-white/10 h-full overflow-y-auto custom-scrollbar"
    >
      <div className="flex items-center gap-3 mb-6">
        <BookOpen size={28} className="text-blue-400" />
        <h2 className="text-2xl font-bold text-white">{t('home_title')}</h2>
      </div>
      
      <p className="text-gray-300 mb-8 leading-relaxed">
        {t('home_desc')}
      </p>

      {/* Project Setup Wizard */}
      <div className="mb-8 p-6 bg-blue-900/20 border border-blue-500/20 rounded-xl">
        <h3 className="text-lg font-semibold text-blue-200 mb-4 flex items-center gap-2">
          <Disc size={20} />
          {t('project_config')}
        </h3>
        
        <div className="space-y-4">
          <div className="flex flex-col">
            <label className="text-xs text-blue-200/70 mb-1 font-semibold uppercase tracking-wider">{t('iso_label')}</label>
            <div className="flex items-center space-x-2">
              <input 
                type="text" 
                value={isoPath}
                onChange={(e) => setIsoPath(e.target.value)}
                placeholder="C:\...\Shin Megami Tensei - Persona 2 - Innocent Sin.iso"
                className="glass-input flex-1"
              />
              <button 
                onClick={() => browse('file', setIsoPath, '.iso')}
                className="p-2 bg-blue-500/20 hover:bg-blue-500/40 border border-blue-500/30 rounded-lg text-blue-200 transition-colors cursor-pointer" 
                title={t('browse')}
              >
                <Folder size={18} />
              </button>
            </div>
          </div>

          <div className="flex flex-col">
            <label className="text-xs text-blue-200/70 mb-1 font-semibold uppercase tracking-wider">{t('workspace_label')}</label>
            <div className="flex items-center space-x-2">
              <input 
                type="text" 
                value={workspaceDir}
                onChange={(e) => setWorkspaceDir(e.target.value)}
                placeholder="C:\...\P2IS_Workspace"
                className="glass-input flex-1"
              />
              <button 
                onClick={() => browse('dir', setWorkspaceDir)}
                className="p-2 bg-blue-500/20 hover:bg-blue-500/40 border border-blue-500/30 rounded-lg text-blue-200 transition-colors cursor-pointer" 
                title={t('browse')}
              >
                <Folder size={18} />
              </button>
            </div>
          </div>

          <button
            onClick={handleInitProject}
            disabled={isInitializing || !isoPath || !workspaceDir}
            className={`w-full mt-4 py-3 px-4 rounded-xl font-bold flex items-center justify-center gap-2 transition-all ${
              isInitializing || !isoPath || !workspaceDir
                ? 'bg-blue-800 text-blue-300 cursor-not-allowed opacity-50' 
                : 'bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white shadow-lg shadow-blue-500/25 hover:shadow-blue-500/40'
            }`}
          >
            {isInitializing ? (
              <><Loader className="animate-spin" size={20} /> {t('init_running')}</>
            ) : (
              <><Cpu size={20} /> {t('init_btn')}</>
            )}
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        
        {/* Workflow */}
        <div className="glass-panel p-6">
          <h3 className="text-lg font-semibold text-blue-200 mb-4 flex items-center gap-2">
            <Cpu size={20} />
            {t('workflow_title')}
          </h3>
          <ul className="space-y-3">
            {workflowSteps.map((step, i) => (
              <li key={i} className="flex gap-3 text-sm text-gray-300">
                <span className="flex-shrink-0 w-6 h-6 rounded-full bg-blue-900/50 text-blue-300 flex items-center justify-center font-bold text-xs border border-blue-500/30">
                  {i + 1}
                </span>
                <span className="mt-0.5">{step}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Formats */}
        <div className="glass-panel p-6">
          <h3 className="text-lg font-semibold text-purple-300 mb-4 flex items-center gap-2">
            <Info size={20} />
            {t('formats_title')}
          </h3>
          <div className="space-y-4">
            {formats.map((fmt, i) => (
              <div key={i} className="bg-black/30 p-3 rounded-lg border border-white/5">
                <h4 className="font-bold text-purple-200 text-sm mb-1">{fmt.name}</h4>
                <p className="text-xs text-gray-400 leading-relaxed">{fmt.desc}</p>
              </div>
            ))}
          </div>
        </div>

      </div>

      <div className="mt-8 bg-red-900/20 border border-red-500/30 p-4 rounded-lg flex items-start gap-3">
        <AlertTriangle size={24} className="text-red-400 flex-shrink-0 mt-0.5" />
        <p className="text-sm text-red-200 leading-relaxed">
          {t('warning_resolution')}
        </p>
      </div>

    </motion.div>
  );
}

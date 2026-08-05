import React, { useState, useEffect } from 'react';
import { ListChecks, Play, Disc, Trash2, CheckCircle, AlertTriangle } from 'lucide-react';
import { motion } from 'framer-motion';

export default function BuildQueue({ t, lang, addLog, browse, isoPath: globalIsoPath, workspaceDir: globalWorkspaceDir }) {
  const [queue, setQueue] = useState([]);
  const [isBuilding, setIsBuilding] = useState(false);
  const [isIsoBuilding, setIsIsoBuilding] = useState(false);
  const [isoOrig, setIsoOrig] = useState('');
  const [cpkDir, setCpkDir] = useState('');

  useEffect(() => {
    if (globalIsoPath) setIsoOrig(globalIsoPath);
    if (globalWorkspaceDir) setCpkDir(globalWorkspaceDir + '\\extracted_cpk');
  }, [globalIsoPath, globalWorkspaceDir]);

  const fetchQueue = async () => {
    try {
      const res = await fetch('http://127.0.0.1:8002/api/queue/list');
      const data = await res.json();
      setQueue(data.queue || []);
    } catch (e) {
      addLog("Erreur de connexion au serveur (File d'attente).", "ERROR");
    }
  };

  useEffect(() => {
    fetchQueue();
  }, []);

  const clearQueue = async () => {
    try {
      await fetch('http://127.0.0.1:8002/api/queue/clear', { method: 'POST' });
      setQueue([]);
      addLog("File d'attente vidée.", "INFO");
    } catch (e) {
      addLog("Erreur lors du vidage de la file d'attente.", "ERROR");
    }
  };

  const applyInjections = async () => {
    if (queue.length === 0) return;
    setIsBuilding(true);
    addLog("Début de l'encodage et injection...", "INFO");
    try {
      const res = await fetch('http://127.0.0.1:8002/api/build/apply', { method: 'POST' });
      const data = await res.json();
      if (res.ok) {
        addLog(`Succès: ${data.success_count} images injectées avec succès !`, "OK");
        if (data.errors && data.errors.length > 0) {
          data.errors.forEach(err => addLog(`Erreur injection: ${err}`, "ERROR"));
        }
        await fetchQueue();
      } else {
        addLog(data.detail || "Erreur d'encodage.", "ERROR");
      }
    } catch (e) {
      addLog("Erreur critique lors de l'injection.", "ERROR");
    }
    setIsBuilding(false);
  };

  const buildIso = async () => {
    if (!isoOrig) {
        addLog(lang === 'fr' ? "Erreur: Veuillez spécifier l'ISO originale." : "Error: Please specify the original ISO.", "ERROR");
        return;
    }
    if (!cpkDir) {
        addLog(lang === 'fr' ? "Erreur: Aucun dossier CPK sélectionné." : "Error: No CPK folder selected.", "ERROR");
        return;
    }
    
    setIsIsoBuilding(true);
    addLog(lang === 'fr' ? "Reconstruction de l'ISO en cours..." : "Rebuilding ISO...", "WARN");
    try {
      const res = await fetch('http://127.0.0.1:8002/api/build/iso', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ base_folder: cpkDir, iso_orig: isoOrig })
      });
      const data = await res.json();
      if (res.ok) {
        addLog(lang === 'fr' ? `ISO généré avec succès : ${data.out_iso}` : `ISO built successfully: ${data.out_iso}`, "OK");
      } else {
        addLog(data.detail || (lang === 'fr' ? "Erreur de création ISO." : "ISO creation error."), "ERROR");
      }
    } catch (e) {
      addLog(lang === 'fr' ? "Erreur lors de la création de l'ISO." : "Error creating ISO.", "ERROR");
    }
    setIsIsoBuilding(false);
  };

  return (
    <motion.div 
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="p-6 bg-gray-900/50 rounded-xl border border-white/10 h-full flex flex-col"
    >
      <div className="flex justify-between items-center mb-6 border-b border-white/10 pb-4">
        <h2 className="text-2xl font-bold text-white flex items-center gap-3">
          <ListChecks size={28} className="text-blue-400" />
          {t('queue_title')}
        </h2>
        <span className="bg-blue-900/40 text-blue-300 px-3 py-1 rounded-full font-bold text-sm border border-blue-500/30">
          {queue.length} {lang === 'fr' ? 'image(s) en attente' : 'image(s) queued'}
        </span>
      </div>

      <div className="flex-1 overflow-y-auto mb-6 bg-black/30 rounded-xl border border-white/5 p-4 custom-scrollbar">
        {queue.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-gray-500 space-y-3">
            <CheckCircle size={48} className="text-gray-600/50" />
            <p>{t('queue_empty')}</p>
            <p className="text-xs">{t('queue_empty_desc')}</p>
          </div>
        ) : (
          <ul className="space-y-2">
            {queue.map((item, i) => (
              <li key={i} className="flex justify-between items-center bg-gray-800/50 p-3 rounded-lg border border-white/5 hover:bg-gray-800 transition-colors">
                <div className="flex flex-col">
                  <span className="font-semibold text-blue-200 text-sm">{item.bin_name}</span>
                  <span className="text-xs text-gray-400">Index: #{item.index} | Offset: 0x{item.offset.toString(16).toUpperCase()}</span>
                </div>
                <div className="text-xs font-mono bg-black/40 px-2 py-1 rounded text-purple-300">
                  {item.filename}
                </div>
              </li>
            ))}
          </ul>
        )}
      </div>

      {/* Zone de reconstruction ISO */}
      <div className="bg-gray-800/40 border border-white/10 rounded-xl p-4 mb-4">
          <h3 className="text-sm font-bold text-blue-300 mb-3 flex items-center gap-2">
             <AlertTriangle size={16} className="text-yellow-500" />
             {t('queue_iso_section')}
          </h3>
          <p className="text-xs text-gray-400 mb-3">
             {t('queue_iso_desc')}
          </p>
          <div className="flex flex-col gap-3">
              <div className="flex items-center gap-3">
                  <input
                    type="text"
                    placeholder={t('iso_label')}
                    value={isoOrig}
                    readOnly
                    className="flex-1 bg-black/40 border border-white/10 rounded-lg px-3 py-2 text-sm text-gray-300 outline-none"
                  />
                  <button
                    onClick={async () => {
                        const file = await browse('file', () => {}, '.iso');
                        if (file) setIsoOrig(file);
                    }}
                    className="bg-gray-700 hover:bg-gray-600 text-white px-4 py-2 rounded-lg text-sm transition-colors border border-white/10 cursor-pointer"
                  >
                      {t('browse')}
                  </button>
              </div>
              <div className="flex items-center gap-3">
                  <input
                    type="text"
                    placeholder={t('workspace_label')}
                    value={cpkDir}
                    onChange={(e) => setCpkDir(e.target.value)}
                    className="flex-1 bg-black/40 border border-white/10 rounded-lg px-3 py-2 text-sm text-gray-300 outline-none"
                  />
                  <button
                    onClick={async () => {
                        const folder = await browse('dir', () => {});
                        if (folder) setCpkDir(folder);
                    }}
                    className="bg-gray-700 hover:bg-gray-600 text-white px-4 py-2 rounded-lg text-sm transition-colors border border-white/10 cursor-pointer"
                  >
                      {t('browse')}
                  </button>
              </div>
          </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <button
          onClick={clearQueue}
          disabled={queue.length === 0 || isBuilding || isIsoBuilding}
          className="flex items-center justify-center gap-2 bg-red-900/30 hover:bg-red-800/50 text-red-300 py-3 rounded-lg border border-red-500/30 transition-colors disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
        >
          <Trash2 size={18} />
          {t('queue_clear')}
        </button>

        <button
          onClick={applyInjections}
          disabled={queue.length === 0 || isBuilding || isIsoBuilding}
          className="flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-500 text-white py-3 rounded-lg shadow-lg hover:shadow-blue-500/25 transition-all disabled:opacity-50 disabled:cursor-not-allowed font-bold cursor-pointer"
        >
          <Play size={18} />
          {isBuilding ? t('queue_applying') : t('queue_apply')}
        </button>

        <button
          onClick={buildIso}
          disabled={isBuilding || isIsoBuilding || !isoOrig}
          className="flex items-center justify-center gap-2 bg-purple-600 hover:bg-purple-500 text-white py-3 rounded-lg shadow-lg hover:shadow-purple-500/25 transition-all disabled:opacity-50 disabled:cursor-not-allowed font-bold cursor-pointer"
        >
          <Disc size={18} />
          {isIsoBuilding ? t('queue_rebuilding_iso') : t('queue_rebuild_iso')}
        </button>
      </div>
      
      <p className="text-xs text-gray-500 text-center mt-4 italic">
        {t('queue_note')}
      </p>

    </motion.div>
  );
}

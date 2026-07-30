import { useState, useRef, useEffect } from 'react';
import IsoExtractor from './IsoExtractor';
import IsoBuilder from './IsoBuilder';
import AudioLab from './AudioLab';
import { Disc, Archive, Mic, Languages } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

import { dict } from './dict';

const old_dict = {
  fr: {
    app_title: "Persona 2 IS Outil Audio VF",
    tab_extract: "Extracteur d'ISO",
    tab_audio: "Audio Lab",
    tab_iso: "Créateur d'ISO",
    logs_title: "{t('logs_title')}",
    logs_empty: "{t('logs_empty')}",
    logs_clear: "{t('logs_clear')}"
  },
  en: {
    app_title: "Persona 2 IS Audio Lab",
    tab_extract: "ISO Extractor",
    tab_audio: "Audio Lab",
    tab_iso: "ISO Builder",
    logs_title: "Event Logs",
    logs_empty: "No recent actions.",
    logs_clear: "Clear logs"
  }
};export default function App() {
  const [activeTab, setActiveTab] = useState('extract');
  const [logs, setLogs] = useState([]);
  const [outDir, setOutDir] = useState('C:\\Users\\nolan\\Desktop\\P2IS_FR_audio');
  const [lang, setLang] = useState('fr');
  
  const logEndRef = useRef(null);
  
  useEffect(() => {
    logEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [logs]);

  const t = (key) => dict[lang][key] || key;

  const addLog = (msg, type = 'INFO') => {
    const time = new Date().toLocaleTimeString();
    setLogs(prev => [...prev, { time, msg, type }]);
  };

  const browse = async (type, setFn, filter = '') => {
    return new Promise((resolve) => {
      const input = document.createElement('input');
      input.type = 'file';
      if (type === 'dir') input.webkitdirectory = true;
      if (filter) input.accept = filter;
      input.onchange = (e) => {
        const path = e.target.files[0]?.path || e.target.files[0]?.name || '';
        if (path) {
          if (type === 'dir') {
            const lastSlash = path.lastIndexOf('\\');
            if (lastSlash > -1) {
                const dir = path.substring(0, lastSlash);
                if (setFn) setFn(dir);
                resolve(dir);
                return;
            }
          }
          if (setFn) setFn(path);
          resolve(path);
        } else {
          resolve(null);
        }
      };
      input.click();
    });
  };

  return (
    <div className="min-h-screen text-white p-8 bg-gray-900 font-sans">
      <motion.div 
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-6xl mx-auto mb-8 relative flex flex-col items-center justify-center"
      >
        <h1 className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-300 to-cyan-100 mb-6">
          {t('app_title')}
        </h1>
        
        <button 
          onClick={() => setLang(lang === 'fr' ? 'en' : 'fr')}
          className="absolute right-0 top-0 bg-white/10 hover:bg-white/20 border border-white/20 rounded-full px-4 py-2 flex items-center space-x-2 transition-all cursor-pointer shadow-lg"
        >
          <Languages size={18} className="text-blue-300" />
          <span className="font-semibold text-sm tracking-wide">{lang === 'fr' ? 'FR' : 'EN'}</span>
        </button>
        
        <div className="flex bg-black/40 p-1 rounded-2xl border border-white/5 shadow-xl">
          <button
            onClick={() => setActiveTab('extract')}
            className={`px-6 py-2.5 rounded-xl font-semibold flex items-center gap-2 transition-all ${activeTab === 'extract' ? 'bg-blue-600 text-white shadow-lg shadow-blue-500/20' : 'text-blue-200/60 hover:text-blue-200 hover:bg-white/5'}`}
          >
            <Archive size={18} /> {t('tab_extract')}
          </button>
          <button
            onClick={() => setActiveTab('audio')}
            className={`px-6 py-2.5 rounded-xl font-semibold flex items-center gap-2 transition-all ${activeTab === 'audio' ? 'bg-blue-600 text-white shadow-lg shadow-blue-500/20' : 'text-blue-200/60 hover:text-blue-200 hover:bg-white/5'}`}
          >
            <Mic size={18} /> {t('tab_audio')}
          </button>
          <button
            onClick={() => setActiveTab('iso')}
            className={`px-6 py-2.5 rounded-xl font-semibold flex items-center gap-2 transition-all ${activeTab === 'iso' ? 'bg-blue-600 text-white shadow-lg shadow-blue-500/20' : 'text-blue-200/60 hover:text-blue-200 hover:bg-white/5'}`}
          >
            <Disc size={18} /> {t('tab_iso')}
          </button>
        </div>
      </motion.div>

      <div className="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-8 h-[calc(100vh-10rem)]">
        
        <div className="lg:col-span-2 h-full relative">
          <AnimatePresence mode="wait">
            <motion.div 
              key={activeTab}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.2 }}
              className="h-full absolute inset-0 w-full"
            >
              {activeTab === 'extract' && <IsoExtractor t={t} lang={lang} addLog={addLog} browse={browse} outDir={outDir} setOutDir={setOutDir} />}
              {activeTab === 'audio' && <AudioLab t={t} lang={lang} addLog={addLog} browse={browse} />}
              {activeTab === 'iso' && <IsoBuilder t={t} lang={lang} addLog={addLog} browse={browse} />}
            </motion.div>
          </AnimatePresence>
        </div>

        <motion.div 
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="lg:col-span-1 glass-panel p-0 flex flex-col overflow-hidden bg-gray-900/80"
        >
          <div className="flex justify-between items-center p-4 bg-black/40 border-b border-white/5">
            <h3 className="font-semibold tracking-wider text-sm uppercase text-blue-200">{t('logs_title')}</h3>
          </div>
          
          <div className="flex-1 p-4 font-mono text-sm overflow-y-auto space-y-1 custom-scrollbar">
            {logs.length === 0 ? (
              <p className="text-gray-500 italic">{t('logs_empty')}</p>
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
              {t('logs_clear')}
            </button>
          </div>
        </motion.div>

      </div>
    </div>
  );
}


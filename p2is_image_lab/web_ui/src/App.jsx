import { useState, useRef, useEffect } from 'react';
import ImageLab from './ImageLab';
import Home from './Home';
import BuildQueue from './BuildQueue';
import { Image as ImageIcon, Languages, Home as HomeIcon, ListChecks, Beaker } from 'lucide-react';
import { motion } from 'framer-motion';

import { dict } from './dict';

export default function App() {
  const [logs, setLogs] = useState([]);
  const [lang, setLang] = useState('fr');
  const [activeTab, setActiveTab] = useState('home');
  
  const logEndRef = useRef(null);
  
  useEffect(() => {
    logEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [logs]);

  const [isoPath, setIsoPath] = useState('');
  const [workspaceDir, setWorkspaceDir] = useState('');
  
  const t = (key) => dict[lang][key] || key;

  const addLog = (msg, type = 'INFO') => {
    const time = new Date().toLocaleTimeString();
    setLogs(prev => [...prev, { time, msg, type }]);
  };

  const browse = async (type, setFn, filter = '') => {
    try {
      const res = await fetch('http://127.0.0.1:8002/api/browse', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ type, ext: filter })
      });
      const data = await res.json();
      if (data.path) {
        if (setFn) setFn(data.path);
        return data.path;
      }
    } catch (e) {
      console.error(e);
    }
    return null;
  };

  return (
    <div className="min-h-screen text-white p-8 bg-gray-900 font-sans flex flex-col">
      <motion.div 
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="w-full flex items-center justify-between mb-6 border-b border-white/10 pb-4"
      >
        <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-cyan-200 flex items-center gap-3">
          <ImageIcon size={32} className="text-blue-400" />
          {t('app_title')}
        </h1>
        
        <div className="flex space-x-2 bg-black/40 rounded-lg p-1 border border-white/5">
          <button onClick={() => setActiveTab('home')} className={`px-4 py-2 flex items-center gap-2 rounded-md transition-all text-sm font-semibold ${activeTab === 'home' ? 'bg-blue-600 text-white' : 'text-gray-400 hover:text-white hover:bg-white/5'}`}>
            <HomeIcon size={16} /> {t('tab_home')}
          </button>
          <button onClick={() => setActiveTab('lab')} className={`px-4 py-2 flex items-center gap-2 rounded-md transition-all text-sm font-semibold ${activeTab === 'lab' ? 'bg-blue-600 text-white' : 'text-gray-400 hover:text-white hover:bg-white/5'}`}>
            <Beaker size={16} /> {t('tab_lab')}
          </button>
          <button onClick={() => setActiveTab('queue')} className={`px-4 py-2 flex items-center gap-2 rounded-md transition-all text-sm font-semibold ${activeTab === 'queue' ? 'bg-purple-600 text-white' : 'text-gray-400 hover:text-white hover:bg-white/5'}`}>
            <ListChecks size={16} /> {t('tab_queue')}
          </button>
        </div>

        <button 
          onClick={() => setLang(lang === 'fr' ? 'en' : 'fr')}
          className="bg-white/5 hover:bg-white/10 border border-white/10 rounded-full px-4 py-2 flex items-center space-x-2 transition-all cursor-pointer shadow-sm"
        >
          <Languages size={18} className="text-blue-300" />
          <span className="font-semibold text-sm tracking-wide">{lang === 'fr' ? 'FR' : 'EN'}</span>
        </button>
      </motion.div>

      <div className="flex-1 grid grid-cols-1 lg:grid-cols-4 gap-6 h-[calc(100vh-8rem)]">
        
        <div className="lg:col-span-3 h-full relative">
          {activeTab === 'home' && <Home t={t} lang={lang} addLog={addLog} browse={browse} isoPath={isoPath} setIsoPath={setIsoPath} workspaceDir={workspaceDir} setWorkspaceDir={setWorkspaceDir} setActiveTab={setActiveTab} />}
          {activeTab === 'lab' && <ImageLab t={t} lang={lang} addLog={addLog} browse={browse} logs={logs} setLogs={setLogs} workspaceDir={workspaceDir} />}
          {activeTab === 'queue' && <BuildQueue t={t} lang={lang} addLog={addLog} browse={browse} isoPath={isoPath} workspaceDir={workspaceDir} />}
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
                  <div key={i} className="leading-relaxed border-b border-white/5 pb-1 mb-1 break-words">
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

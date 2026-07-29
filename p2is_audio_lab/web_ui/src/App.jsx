import React, { useState, useEffect, useRef } from 'react';

import { motion, AnimatePresence } from 'framer-motion';

import { Download, Mic, Folder, Music, Play, Square, Info, FileAudio, CheckCircle, Save, Upload, AlertTriangle, File, Disc, Archive } from 'lucide-react';

import IsoBuilder from './IsoBuilder';
import IsoExtractor from './IsoExtractor';



export default function App() {

  const [binPath, setBinPath] = useState('');

  const [outDir, setOutDir] = useState('');

  const [atracToolPath, setAtracToolPath] = useState('');

  const [binInfo, setBinInfo] = useState(null);

  const [isExtracting, setIsExtracting] = useState(false);

  

  const [status, setStatus] = useState('Prêt');

  const [logs, setLogs] = useState([]);

  const [loading, setLoading] = useState(false);

  const [notes, setNotes] = useState({});

  const [playingIdx, setPlayingIdx] = useState(null);

  const [activeTab, setActiveTab] = useState('audio');



  const logContainerRef = useRef(null);

  const audioRef = useRef(null);



  useEffect(() => {

    if (logContainerRef.current) {

      logContainerRef.current.scrollTop = logContainerRef.current.scrollHeight;

    }

  }, [logs]);



  // Initialiser l'audio et gérer la fin de piste

  useEffect(() => {

    if (!audioRef.current) {

      audioRef.current = new Audio();

    }

    const handleEnded = () => setPlayingIdx(null);

    audioRef.current.addEventListener('ended', handleEnded);

    return () => {

      if (audioRef.current) {

        audioRef.current.removeEventListener('ended', handleEnded);

        audioRef.current.pause();

      }

    };

  }, []);

  

  useEffect(() => {

    if (binPath) {

      loadBinInfo();

    }

  }, [binPath]);



  useEffect(() => {

    localStorage.setItem('atracToolPath', atracToolPath);

  }, [atracToolPath]);



  const loadBinInfo = async () => {

    try {

      const res = await fetch('http://127.0.0.1:8001/api/audio/info', {

        method: 'POST',

        headers: { 'Content-Type': 'application/json' },

        body: JSON.stringify({ bin_path: binPath })

      });

      const data = await res.json();

      if (data.status === 'ok') {

        setBinInfo(data);

        const pathParts = binPath.split('\\');

        const fileName = pathParts.pop().replace('.BIN', '');

        const defaultOut = `C:\\Users\\nolan\\Desktop\\P2IS_FR_audio\\${fileName}`;

        setOutDir(defaultOut);

        loadNotes();

        addLog(`Fichier chargéé. ${data.total} pistes détectées.`, "OK");

      } else {

        setBinInfo(null);

      }

    } catch (e) {

      setBinInfo(null);

      addLog(`Erreur de chargéement du BIN.`, "ERROR");

    }

  };



  const loadNotes = async () => {

    try {

      const res = await fetch('http://127.0.0.1:8001/api/audio/notes/load', {

        method: 'POST',

        headers: { 'Content-Type': 'application/json' },

        body: JSON.stringify({ bin_path: binPath })

      });

      const data = await res.json();

      setNotes(data || {});

    } catch (e) {}

  };



  const saveNotes = async () => {

    try {

      await fetch('http://127.0.0.1:8001/api/audio/notes/save', {

        method: 'POST',

        headers: { 'Content-Type': 'application/json' },

        body: JSON.stringify({ bin_path: binPath, notes })

      });

      addLog("Notes sauvegardées avec succès.", "OK");

    } catch (e) {

      addLog("Erreur lors de la sauvegarde des notes.", "ERROR");

    }

  };



  const addLog = (msg, type = "INFO") => {

    const time = new Date().toLocaleTimeString();

    setLogs(l => [...l, { time, msg, type }]);

  };



  const browse = async (type, setter, ext = "") => {

    try {

      const res = await fetch(`http://127.0.0.1:8001/api/browse`, {

        method: 'POST',

        headers: { 'Content-Type': 'application/json' },

        body: JSON.stringify({ type, ext })

      });

      const data = await res.json();

      if (data.path) setter(data.path);

      return data.path;

    } catch (e) {

      addLog(`Erreur parcours: ${e.message}`, "ERROR");

      return null;

    }

  };



  const extractAll = async () => {

    if (!binPath || !outDir) return alert("Renseignez le BIN et le dossier de sortie !");

    setIsExtracting(true);

    setStatus("Extraction et conversion FFmpeg en cours... Veuillez patienter (environ 1 minute).");

    try {

      const res = await fetch(`http://127.0.0.1:8001/api/audio/extract`, {

        method: 'POST',

        headers: { 'Content-Type': 'application/json' },

        body: JSON.stringify({ bin_path: binPath, out_dir: outDir })

      });

      const data = await res.json();

      setStatus(data.msg);

    } catch (e) {

      console.error(e);

      setStatus("Erreur lors de l'extraction");

    } finally {

      setIsExtracting(false);

    }

  };



  const injectVoice = async (index, wavPath) => {

    if (!wavPath) return;

    setLoading(true);

    setStatus("Injection...");

    addLog(`Injection de la piste #${index}...`, "INFO");

    const outBinPath = binPath.replace('.BIN', '_MOD.BIN');

    try {

      const res = await fetch(`http://127.0.0.1:8001/api/audio/inject`, {

        method: 'POST',

        headers: { 'Content-Type': 'application/json' },

        body: JSON.stringify({ 

          bin_path: binPath, 

          voice_index: index, 

          wav_path: wavPath, 

          out_bin_path: outBinPath,

          at3tool_path: atracToolPath 

        })

      });

      const data = await res.json();

      if (res.ok) {

        addLog(data.msg, "OK");

      } else {

        addLog(data.detail, "ERROR");

      }

    } catch (e) {

      addLog(e.message, "ERROR");

    }

    setStatus("Prêt");

    setLoading(false);

  };



  const playAudio = (index) => {

    if (playingIdx === index) {

      audioRef.current.pause();

      setPlayingIdx(null);

    } else {

      const url = `http://127.0.0.1:8001/api/audio/stream?bin_path=${encodeURIComponent(binPath)}&index=${index}&t=${Date.now()}`;

      audioRef.current.src = url;

      audioRef.current.play().catch(e => addLog(`Erreur de lecture: ${e.message}`, "ERROR"));

      setPlayingIdx(index);

    }

  };



  const handleNoteChange = (idx, val) => {

    setNotes(prev => ({ ...prev, [idx]: val }));

  };



  return (

    <div className="min-h-screen text-white p-8 font-sans">

      

      {/* Header Section Plagiée */}

      <motion.div 

        initial={{ opacity: 0, y: -20 }}

        animate={{ opacity: 1, y: 0 }}

        className="max-w-6xl mx-auto mb-8 relative flex flex-col items-center justify-center"

      >

        <h1 className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-300 to-cyan-100 mb-6">

          Persona 2 IS Outil Audio VF

        </h1>

        

        {/* Navigation Tabs */}

        <div className="flex space-x-2 bg-black/20 p-1.5 rounded-2xl border border-white/5 shadow-xl">

          <button

            onClick={() => setActiveTab('audio')}

            className={`px-6 py-2.5 rounded-xl font-semibold flex items-center gap-2 transition-all ${activeTab === 'audio' ? 'bg-blue-600 text-white shadow-lg shadow-blue-500/20' : 'text-blue-200/60 hover:text-blue-200 hover:bg-white/5'}`}

          >

            <Mic size={18} /> Audio Lab

          </button>

          <button

            onClick={() => setActiveTab('iso')}

            className={`px-6 py-2.5 rounded-xl font-semibold flex items-center gap-2 transition-all ${activeTab === 'iso' ? 'bg-blue-600 text-white shadow-lg shadow-blue-500/20' : 'text-blue-200/60 hover:text-blue-200 hover:bg-white/5'}`}

          >

            <Disc size={18} /> Créateur d'ISO

          </button>

        </div>

      </motion.div>



      <div className="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-8 h-[calc(100vh-10rem)]">

        

        {/* Main Interface */}

        <motion.div 

          initial={{ opacity: 0, x: -20 }}

          animate={{ opacity: 1, x: 0 }}

          className="lg:col-span-2 flex flex-col space-y-4"

        >

          {activeTab === 'audio' ? (

            <div className="glass-panel p-6 flex flex-col space-y-4 h-full">

          {/* Configuration Cards */}

          <div className="mb-4 space-y-4 bg-black/10 p-4 rounded-xl border border-white/5">

            {/* Dossier de travail */}

            <div className="flex flex-col">

              <label className="text-xs text-blue-200/70 mb-1 font-semibold uppercase tracking-wider">Dossier de travail (Extraction)</label>

              <div className="flex items-center space-x-2">

                <input 

                  type="text" 

                  value={outDir}

                  onChange={(e) => setOutDir(e.target.value)}

                  placeholder="C:\Users\...\P2IS_FR_audio\VOICEALL"

                  className="glass-input flex-1"

                />

                <button 

                  onClick={() => browse('dir', setOutDir)}

                  className="p-2 bg-blue-500/20 hover:bg-blue-500/40 border border-blue-500/30 rounded-lg text-blue-200 transition-colors cursor-pointer" 

                  title="Parcourir"

                >

                  <Folder size={20} />

                </button>

              </div>

            </div>



            {/* ATRACTool Config */}

            <div className="flex flex-col">

                            <div className="flex justify-between items-center mb-1">
                <label className="text-xs text-blue-200/70 font-semibold uppercase tracking-wider">Compresseur Audio (ATRACTool-Reloaded.exe)</label>
                <a href="https://github.com/XyLe-GBP/ATRACTool-Reloaded" target="_blank" rel="noopener noreferrer" className="text-xs text-blue-400 hover:text-blue-300 flex items-center bg-blue-500/10 px-2 py-0.5 rounded-full"><Download size={12} className="mr-1"/> Télécharger</a>
              </div>

              <div className="flex items-center space-x-2">

                <input 

                  type="text" 

                  value={atracToolPath}

                  onChange={(e) => setAtracToolPath(e.target.value)}

                  placeholder="C:\...\ATRACTool-Rel-Release.exe (Optionnel)"

                  className="glass-input flex-1"

                />

                <button 

                  onClick={() => browse('file', setAtracToolPath, '.exe')}

                  className="p-2 bg-blue-500/20 hover:bg-blue-500/40 border border-blue-500/30 rounded-lg text-blue-200 transition-colors cursor-pointer" 

                  title="Parcourir"

                >

                  <File size={20} />

                </button>

              </div>

            </div>



            {/* Fichier Source */}

            <div className="flex flex-col">

              <label className="text-xs text-blue-200/70 mb-1 font-semibold uppercase tracking-wider">Fichier Source (.BIN)</label>

              <div className="flex items-center space-x-2">

                <input 

                  type="text" 

                  value={binPath}

                  readOnly

                  placeholder="C:\...\VOICEALL.BIN"

                  className="glass-input flex-1"

                />

                <button 

                  onClick={() => browse('file', setBinPath, '.BIN')}

                  className="p-2 bg-blue-500/20 hover:bg-blue-500/40 border border-blue-500/30 rounded-lg text-blue-200 transition-colors cursor-pointer" 

                  title="Parcourir"

                >

                  <File size={20} />

                </button>

              </div>

            </div>



            {binInfo && (

              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-t border-white/5 pt-4">

                <span className="text-sm font-medium text-blue-200 flex items-center gap-2">

                  <CheckCircle size={16} className="text-green-400" />

                  {binInfo.total.toLocaleString()} pistes détectées

                </span>

                <button 

                  onClick={extractAll}

                  disabled={isExtracting}

                  className={`glass-button text-sm flex items-center justify-center space-x-2 py-2 ${isExtracting ? 'opacity-50 cursor-not-allowed' : ''}`}

                >

                  <Download size={16} /> <span>{isExtracting ? 'Extraction...' : 'Tout extraire'}</span>

                </button>

              </div>

            )}

          </div>



          {/* Audio Track List */}

          <div className="flex-1 bg-black/20 rounded-xl p-4 border border-white/5 relative overflow-hidden flex flex-col min-h-0">

            <div className="absolute top-[-50px] right-[-50px] w-64 h-64 bg-blue-500/10 rounded-full blur-3xl pointer-events-none"></div>

            

            {/* Header List */}

            {binInfo && (

              <div className="flex justify-between items-center mb-3 relative z-10 px-2 border-b border-white/5 pb-2">

                <h3 className="text-sm font-semibold text-blue-200">Liste des voix</h3>

                <button 

                  onClick={saveNotes}

                  className="glass-button py-1.5 px-3 text-xs flex items-center gap-2"

                >

                  <Save size={14} /> Enregistrer les notes

                </button>

              </div>

            )}



            {binInfo ? (

              <div className="flex-1 overflow-y-auto space-y-2 relative z-10 pr-2">

                {Array.from({ length: binInfo.total }).map((_, i) => (

                  <div key={i} className="flex items-center gap-3 p-2 bg-white/5 hover:bg-white/10 border border-white/5 rounded-xl transition-colors">

                    <span className="w-10 text-center text-xs font-bold text-gray-500">#{i}</span>

                    

                    {/* Play Button */}

                    <button 

                      onClick={() => playAudio(i)}

                      className={`w-9 h-9 rounded-full flex items-center justify-center transition-colors ${playingIdx === i ? 'bg-blue-500 text-white shadow-lg shadow-blue-500/30' : 'bg-black/40 text-blue-300 hover:bg-blue-500/30 border border-white/5'}`}

                    >

                      {playingIdx === i ? <Square size={14} fill="currentColor" /> : <Play size={14} fill="currentColor" className="ml-1" />}

                    </button>

                    

                    {/* Note Input */}

                    <input 

                      type="text" 

                      placeholder="Nom du perso / Note..."

                      value={notes[i] || ''}

                      onChange={(e) => handleNoteChange(i, e.target.value)}

                      onBlur={saveNotes}

                      className="glass-input flex-1 py-1.5 text-sm"

                    />



                    {/* Inject Button */}

                    <button 

                      onClick={async () => {

                        const wav = await browse('file', () => {}, '.wav');

                        if (wav) injectVoice(i, wav);

                      }}

                      disabled={loading}

                      className="glass-button px-3 py-1.5 text-xs flex items-center gap-1.5"

                    >

                      <Upload size={14} /> Remplacer

                    </button>

                  </div>

                ))}

              </div>

            ) : (

              <div className="flex-1 flex flex-col items-center justify-center text-blue-200/50 relative z-10">

                <Music size={48} className="mb-4 opacity-20" />

                <p>Aucun fichier source chargéé.</p>

              </div>

            )}

          </div>

            </div>

          ) : (

            <IsoBuilder addLog={addLog} browse={browse} />

          )}

        </motion.div>



        {/* Sidebar Log Plagiée */}

        <motion.div 

          initial={{ opacity: 0, x: 20 }}

          animate={{ opacity: 1, x: 0 }}

          className="glass-panel p-0 flex flex-col overflow-hidden bg-gray-900/80"

        >

          <div className="flex justify-between items-center p-4 bg-black/40 border-b border-white/5">

            <h3 className="font-semibold tracking-wider text-sm uppercase text-blue-200">Journal d'Événements</h3>

            <span className={`text-xs px-2 py-1 rounded-full ${loading || isExtracting ? 'bg-yellow-500/20 text-yellow-300' : 'bg-green-500/20 text-green-300'}`}>

              {status}

            </span>

          </div>

          

          <div ref={logContainerRef} className="flex-1 p-4 font-mono text-sm overflow-y-auto space-y-1 custom-scrollbar">

            {logs.length === 0 ? (

              <p className="text-gray-500 italic">Aucune action récente.</p>

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

          </div>

          

          <div className="p-2 bg-black/40 border-t border-white/5 flex justify-end">

            <button 

              onClick={() => setLogs([])}

              className="text-xs text-gray-400 hover:text-white transition-colors px-2 py-1 cursor-pointer"

            >

              Vider le journal

            </button>

          </div>

          

          <div className="p-4 border-t border-white/5">

            <button 

              onClick={extractAll}

              disabled={isExtracting}

              className={`w-full py-3 px-4 ${isExtracting ? 'bg-blue-600/30 text-blue-300' : 'bg-blue-600 hover:bg-blue-500 text-white'} font-semibold rounded-xl transition-all shadow-[0_0_15px_rgba(37,99,235,0.3)]`}

            >

              {isExtracting ? (

                <span className="flex items-center justify-center">

                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">

                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>

                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>

                  </svg>

                  Traitement FFmpeg en cours...

                </span>

              ) : "Tout extraire"}

            </button>

          </div>

        </motion.div>

        

      </div>

    </div>

  );

}












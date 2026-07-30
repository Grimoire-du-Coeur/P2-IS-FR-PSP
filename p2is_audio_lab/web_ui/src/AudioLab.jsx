import React, { useState, useEffect, useRef } from 'react';
import { motion, 
AnimatePresence } from 'framer-motion';
import { Download, Mic, Folder, Music, Play, Square, Info, FileAudio, 
CheckCircle, Save, Upload, AlertTriangle, File } from 'lucide-react';

export default function AudioLab({ t, lang, addLog, browse, logs, setLogs }) {
  
const [binPath, setBinPath] = useState('');
  const [outDir, setOutDir] = useState('');
  const 
[atracToolPath, setAtracToolPath] = useState(() => localStorage.getItem('atracToolPath') || '');
  const [binInfo, 
setBinInfo] = useState(null);
  const [isExtracting, setIsExtracting] = useState(false);
  
  const 
[status, setStatus] = useState('Prêt');
  
  const [loading, 
setLoading] = useState(false);
  const [notes, setNotes] = useState({});
  const [playingIdx, setPlayingIdx] 
= useState(null);

  const logEndRef = useRef(null);
  const audioRef = useRef(new Audio());


  useEffect(() => {
    logEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [logs]);


  // When audio ends, reset playing icon
  useEffect(() => {
    const handleEnded = () => 
setPlayingIdx(null);
    audioRef.current.addEventListener('ended', handleEnded);
    return () => 
audioRef.current.removeEventListener('ended', handleEnded);
  }, []);
  
  useEffect(() => {
    
if (binPath) {
      loadBinInfo();
    }
  }, [binPath]);

  useEffect(() => {
    
localStorage.setItem('atracToolPath', atracToolPath);
  }, [atracToolPath]);

  const loadBinInfo = 
async () => {
    try {
      const res = await fetch('http://127.0.0.1:8001/api/audio/info', {
        
method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
bin_path: binPath })
      });
      const data = await res.json();
      if (data.status === 'ok') 
{
        setBinInfo(data);
        const pathParts = binPath.split('\\');
        const fileName = 
pathParts.pop().replace('.BIN', '');
        const defaultOut = 
`C:\\Users\\ olan\\Desktop\\P2IS_FR_audio\\${fileName}`;
        setOutDir(defaultOut);
        
loadNotes();
        addLog(`Fichier chargé. ${data.total} pistes détectées.`, "OK");
      } else {
 
       setBinInfo(null);
      }
    } catch (e) {
      setBinInfo(null);
      addLog(`Erreur de  chargement du BIN.`, "ERROR");
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
      await 
fetch('http://127.0.0.1:8001/api/audio/notes/save', {
        method: 'POST',
        headers: { 
'Content-Type': 'application/json' },
        body: JSON.stringify({ bin_path: binPath, notes })
      
});
      addLog("Notes sauvegardées avec succès.", "OK");
    } catch (e) {
      addLog("Erreur lors de la sauvegarde des notes.", "ERROR");
    }
  };



  const extractAll = async () => {
    if (!binPath || !outDir) return alert("Renseignez le BIN et le dossier de sortie !");
    setIsExtracting(true);
    setStatus("Extraction et conversion FFmpeg en cours... Veuillez patienter (environ 1 minute).");
    try {
      const res = await fetch(`http://127.0.0.1:8001/api/audio/extract`, {
        method: 'POST',
        headers: { 
'Content-Type': 'application/json' },
        body: JSON.stringify({ bin_path: binPath, out_dir: outDir })


      });
      const data = await res.json();
      setStatus(data.msg);
    } catch (e) {
   
   console.error(e);
      setStatus("Erreur lors de l'extraction");     } finally {        setIsExtracting(false);     }   };    const injectVoice = async (index, wavPath) => {      if (!wavPath) return;     setLoading(true);     setStatus("Injection...");     addLog(`Injection  de la piste #${index}...`, "INFO");     const outBinPath = binPath.replace('.BIN', '_MOD.BIN');     try  {       const res = await fetch(`http://127.0.0.1:8001/api/audio/inject`, {         method: 'POST',          headers: { 'Content-Type': 'application/json' },         body: JSON.stringify({             bin_path: binPath,            voice_index: index,            wav_path: wavPath,             out_bin_path: outBinPath,           at3tool_path: atracToolPath          })       });        const data = await res.json();       if (res.ok) {         addLog(data.msg, "OK");       } else  {         addLog(data.detail, "ERROR");       }     } catch (e) {       addLog(e.message,  "ERROR");     }     setStatus("Prêt");     setLoading(false);   };    const  playAudio = (index) => {     if (playingIdx === index) {       audioRef.current.pause();        setPlayingIdx(null);     } else {       const url =  `http://127.0.0.1:8001/api/audio/stream?bin_path=${encodeURIComponent(binPath)}&index=${index}`;        audioRef.current.src = url;       audioRef.current.play().catch(e => addLog(`Erreur de lecture: ${e.message}`,  "ERROR"));       setPlayingIdx(index);     }   };    const handleNoteChange = (idx, val) => {     setNotes(prev => ({ ...prev, [idx]: val }));   };    return (       <div className="h-full">                   {/* Main Interface */}         <motion.div            initial={{ opacity: 0, x: -20 }}            animate={{ opacity: 1, x: 0 }}           className="glass-panel h-full p-6 flex flex-col space-y-4"         >           {/* Configuration Cards */}           <div className="mb-4  space-y-4 bg-black/10 p-4 rounded-xl border border-white/5">             {/* Dossier de travail */}              <div className="flex flex-col">               <label className="text-xs text-blue-200/70 mb-1  font-semibold uppercase tracking-wider">{t('work_dir_extract')}</label>               <div  className="flex items-center space-x-2">                 <input                    type="text"                     value={outDir}                   onChange={(e) => setOutDir(e.target.value)}                    placeholder="C:\Users\...\P2IS_FR_audio\VOICEALL"                   className="glass-input  flex-1"                 />                 <button                    onClick={() => browse('dir',  setOutDir)}                   className="p-2 bg-blue-500/20 hover:bg-blue-500/40 border border-blue-500/30  rounded-lg text-blue-200 transition-colors cursor-pointer"                    title={t('browse')}                  >                   <Folder size={20} />                 </button>                </div>             </div>              {/* ATRACTool Config */}             <div  className="flex flex-col">               <label className="text-xs text-blue-200/70 mb-1 font-semibold  uppercase tracking-wider">{t('audio_compressor')}</label>               <div  className="flex items-center space-x-2">                 <input                    type="text"                     value={atracToolPath}                   onChange={(e) =>  setAtracToolPath(e.target.value)}                   placeholder="C:\...\ATRACTool-Rel-Release.exe  (Optionnel)"                   className="glass-input flex-1"                 />                  <button                    onClick={() => browse('file', setAtracToolPath, '.exe')}                    className="p-2 bg-blue-500/20 hover:bg-blue-500/40 border border-blue-500/30 rounded-lg text-blue-200  transition-colors cursor-pointer"                    title={t('browse')}                 >                    <File size={20} />                 </button>               </div>             </div>               {/* Fichier Source */}             <div className="flex flex-col">                <label className="text-xs text-blue-200/70 mb-1 font-semibold uppercase tracking-wider">Fichier Source  (.BIN)</label>               <div className="flex items-center space-x-2">                 <input                     type="text"                    value={binPath}                   readOnly                    placeholder="C:\...\VOICEALL.BIN"                   className="glass-input flex-1"                  />                 <button                    onClick={() => browse('file', setBinPath,  '.BIN')}                   className="p-2 bg-blue-500/20 hover:bg-blue-500/40 border border-blue-500/30  rounded-lg text-blue-200 transition-colors cursor-pointer"                    title={t('browse')}                  >                   <File size={20} />                 </button>               </div>              </div>              {binInfo && (               <div className="flex flex-col  sm:flex-row sm:items-center justify-between gap-4 border-t border-white/5 pt-4">                 <span  className="text-sm font-medium text-blue-200 flex items-center gap-2">                   <CheckCircle  size={16} className="text-green-400" />                   {binInfo.total.toLocaleString()} pistes  détectées                 </span>                 <button                                        onClick={extractAll}                   disabled={isExtracting}                   className={`glass-button  text-sm flex items-center justify-center space-x-2 py-2 ${isExtracting ? 'opacity-50 cursor-not-allowed' : ''}`}                  >                   <Download size={16} /> <span>{isExtracting ? 'Extraction...' : 'Tout extraire'}</span>                 </button>               </div>             )}            </div>            {/* Audio Track List */}           <div className="flex-1 bg-black/20 rounded-xl  p-4 border border-white/5 relative overflow-hidden flex flex-col min-h-0">             <div  className="absolute top-[-50px] right-[-50px] w-64 h-64 bg-blue-500/10 rounded-full blur-3xl  pointer-events-none"></div>                          {/* Header List */}             {binInfo &&  (               <div className="flex justify-between items-center mb-3 relative z-10 px-2 border-b  border-white/5 pb-2">                 <h3 className="text-sm font-semibold text-blue-200">Liste des  voix</h3>                 <button                    onClick={saveNotes}                    className="glass-button py-1.5 px-3 text-xs flex items-center gap-2"                 >                    <Save size={14} /> Enregistrer les notes                 </button>               </div>              )}              {binInfo ? (               <div className="flex-1 overflow-y-auto space-y-2  relative z-10 pr-2">                 {Array.from({ length: binInfo.total }).map((_, i) => (                    <div key={i} className="flex items-center gap-3 p-2 bg-white/5 hover:bg-white/10 border border-white/5 rounded-xl  transition-colors">                     <span className="w-10 text-center text-xs font-bold  text-gray-500">#{i}</span>                                          {/* Play Button */}                      <button                        onClick={() => playAudio(i)}                       className={`w-9 h-9 rounded-full flex items-center justify-center transition-colors ${playingIdx === i ? 'bg-blue-500 text-white shadow-lg shadow-blue-500/30' : 'bg-black/40 text-blue-300 hover:bg-blue-500/30 border border-white/5'}`}                      >                       {playingIdx === i ? <Square size={14} fill="currentColor" /> : <Play  size={14} fill="currentColor" className="ml-1" />}                     </button>                                           {/* Note Input */}                     <input                         type="text"                        placeholder={t('note_placeholder')}                        value={notes[i] || ''}                       onChange={(e) => handleNoteChange(i, e.target.value)}                        onBlur={saveNotes}                       className="glass-input flex-1 py-1.5 text-sm"                      />                      {/* Inject Button */}                     <button                         onClick={async () => {                         const wav = await browse('file', () => {},  '.wav');                         if (wav) injectVoice(i, wav);                       }}                        disabled={loading}                       className="glass-button px-3 py-1.5 text-xs flex items-center  gap-1.5"                     >                       <Upload size={14} /> Remplacer                      </button>                   </div>                 ))}               </div>             )  : (               <div className="flex-1 flex flex-col items-center justify-center text-blue-200/50 relative  z-10">                 <Music size={48} className="mb-4 opacity-20" />                 <p>Aucun fichier  source chargé.</p>               </div>             )}           </div>          </motion.div>          

  </div>
  );
}
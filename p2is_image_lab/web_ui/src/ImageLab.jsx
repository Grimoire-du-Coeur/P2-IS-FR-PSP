import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Download, Image as ImageIcon, Folder, File, Eye, Upload, RefreshCw, AlertTriangle, FileArchive, Search } from 'lucide-react';

export default function ImageLab({ t, lang, addLog, browse, logs, setLogs, workspaceDir }) {
  const [cpkDir, setCpkDir] = useState('');
  const [outDir, setOutDir] = useState('');
  
  useEffect(() => {
    if (workspaceDir) {
        const newCpkDir = workspaceDir + '\\extracted_cpk';
        setCpkDir(newCpkDir);
        setOutDir(workspaceDir);
    }
  }, [workspaceDir]);

  // Auto scan when cpkDir is set by workspaceDir
  useEffect(() => {
    if (workspaceDir && cpkDir) {
      scanFolder();
    }
  }, [cpkDir]);
  
  const [fileList, setFileList] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [binInfo, setBinInfo] = useState(null);
  
  const [loadingFiles, setLoadingFiles] = useState(false);
  const [loadingInfo, setLoadingInfo] = useState(false);
  const [injecting, setInjecting] = useState(false);
  const [previewIdx, setPreviewIdx] = useState(null);

  const scanFolder = async () => {
    if (!cpkDir) return;
    setLoadingFiles(true);
    setFileList([]);
    setSelectedFile(null);
    setBinInfo(null);
    addLog(`Scan du dossier CPK en cours...`, 'INFO');
    try {
      const res = await fetch('http://127.0.0.1:8002/api/image/scan_folder', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ folder_path: cpkDir })
      });
      const data = await res.json();
      if (res.ok) {
        setFileList(data.files);
        addLog(`Scan terminé : ${data.files.length} fichiers contenant des images trouvés.`, 'OK');
      } else {
        addLog(`Erreur scan: ${data.detail}`, 'ERROR');
      }
    } catch (e) {
      addLog(`Erreur réseau: ${e.message}`, 'ERROR');
    }
    setLoadingFiles(false);
  };

  const selectFile = async (file) => {
    setSelectedFile(file);
    setBinInfo(null);
    setPreviewIdx(null);
    setLoadingInfo(true);
    addLog(`Analyse de ${file.name}...`, 'INFO');
    try {
      const res = await fetch('http://127.0.0.1:8002/api/image/info', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ bin_path: file.full_path })
      });
      const data = await res.json();
      if (res.ok) {
        setBinInfo(data);
        addLog(`Fichier analysé. ${data.total} GIM détectés.`, 'OK');
      } else {
        addLog(`Erreur analyse: ${data.detail}`, 'ERROR');
      }
    } catch (e) {
      addLog(`Erreur réseau: ${e.message}`, 'ERROR');
    }
    setLoadingInfo(false);
  };

  const extractSingle = async (idx, offset, size, format) => {
    if (!outDir) return alert("Renseignez le dossier de travail pour l'export !");
    try {
      const res = await fetch(`http://127.0.0.1:8002/api/image/extract`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
            bin_path: selectedFile.full_path, 
            out_dir: outDir, 
            index: idx, 
            offset, 
            size, 
            format 
        })
      });
      const data = await res.json();
      if (res.ok) addLog(data.msg, "OK");
      else addLog(data.detail, "ERROR");
    } catch (e) {
      addLog("Erreur: " + e.message, "ERROR");
    }
  };

  const injectGim = async (idx, offset, size, fileOrPath) => {
    if (!fileOrPath) return;
    setInjecting(true);
    addLog(`Ajout de l'image #${idx} à la file d'attente...`, "INFO");
    try {
      // Create FormData to upload the file
      const formData = new FormData();
      formData.append('bin_path', selectedFile.full_path);
      formData.append('target_offset', offset);
      formData.append('target_size', size);
      formData.append('index', idx);
      
      // We need to fetch the local file to a Blob to send it if it's a path string
      let fileBlob;
      if (typeof fileOrPath === 'string') {
          addLog("Erreur: Le navigateur ne permet pas l'upload direct par chemin. Modifiez le composant pour utiliser un <input type='file'> standard.", "ERROR");
          setInjecting(false);
          return;
      } else {
          fileBlob = fileOrPath;
      }
      
      formData.append('file', fileBlob);

      const res = await fetch(`http://127.0.0.1:8002/api/queue/add`, {
        method: 'POST',
        body: formData
      });
      const data = await res.json();
      if (res.ok) {
        addLog(`Image #${idx} mise en attente avec succès !`, "OK");
      } else {
        addLog(data.detail || data.msg || "Erreur d'ajout à la file.", "ERROR");
      }
    } catch (e) {
      addLog(e.message, "ERROR");
    }
    setInjecting(false);
  };

  return (
    <div className="h-full flex flex-col space-y-4">
      {/* Top Configuration Bar */}
      <div className="glass-panel p-4 flex flex-col md:flex-row gap-4 items-end bg-black/20">
        <div className="flex-1 w-full flex flex-col">
          <label className="text-xs text-blue-200/70 mb-1 font-semibold uppercase tracking-wider">
            {t('lab_source_dir')}
          </label>
          <div className="flex items-center space-x-2">
            <input 
              type="text" 
              value={cpkDir}
              onChange={(e) => setCpkDir(e.target.value)}
              className="glass-input flex-1 py-2 text-sm"
            />
            <button 
              onClick={() => browse('dir', setCpkDir)}
              className="p-2 bg-blue-500/20 hover:bg-blue-500/40 border border-blue-500/30 rounded-lg text-blue-200 transition-colors"
            >
              <Folder size={18} />
            </button>
            <button 
              onClick={scanFolder}
              disabled={loadingFiles}
              className={`glass-button py-2 px-4 flex items-center gap-2 ${loadingFiles ? 'opacity-50' : 'bg-blue-600/50 hover:bg-blue-600/80 border-blue-500/50'}`}
            >
              <RefreshCw size={16} className={loadingFiles ? 'animate-spin' : ''} />
              <span>{loadingFiles ? t('lab_scanning') : t('lab_scan_btn')}</span>
            </button>
          </div>
        </div>

        <div className="flex-1 w-full flex flex-col">
          <label className="text-xs text-blue-200/70 mb-1 font-semibold uppercase tracking-wider">
            {t('lab_export_dir')}
          </label>
          <div className="flex items-center space-x-2">
            <input 
              type="text" 
              value={outDir}
              onChange={(e) => setOutDir(e.target.value)}
              className="glass-input flex-1 py-2 text-sm"
            />
            <button 
              onClick={() => browse('dir', setOutDir)}
              className="p-2 bg-green-500/20 hover:bg-green-500/40 border border-green-500/30 rounded-lg text-green-200 transition-colors"
            >
              <Folder size={18} />
            </button>
          </div>
        </div>
      </div>

      {/* Main Content Area: Left Sidebar (Files) + Right Pane (Images) */}
      <div className="flex-1 flex gap-4 min-h-0">
        
        {/* Left Sidebar - File List */}
        <div className="w-1/3 glass-panel p-0 flex flex-col overflow-hidden bg-black/20 border-white/5">
          <div className="p-3 border-b border-white/5 bg-black/40 flex items-center gap-2">
            <FileArchive size={16} className="text-blue-300" />
            <h3 className="font-semibold text-sm text-blue-200">Fichiers avec Images</h3>
            {fileList.length > 0 && <span className="ml-auto text-xs bg-blue-900/50 px-2 py-0.5 rounded-full">{fileList.length}</span>}
          </div>
          <div className="flex-1 overflow-y-auto p-2 custom-scrollbar">
            {fileList.length === 0 ? (
              <div className="flex flex-col items-center justify-center h-full text-white/30 text-xs text-center p-4">
                <Search size={32} className="mb-2 opacity-50" />
                <p>Cliquez sur Scanner pour trouver les fichiers d'images dans le dossier CPK.</p>
              </div>
            ) : (
              <div className="flex flex-col gap-1">
                {fileList.map((file, i) => (
                  <button
                    key={i}
                    onClick={() => selectFile(file)}
                    className={`text-left p-3 rounded-lg text-sm flex flex-col gap-1 transition-all ${selectedFile?.full_path === file.full_path ? 'bg-blue-600/30 border border-blue-500/50' : 'hover:bg-white/5 border border-transparent'}`}
                  >
                    <span className="font-semibold text-gray-200">{file.name}</span>
                    <span className="text-xs text-gray-500 truncate">{file.rel_path}</span>
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Right Pane - Images */}
        <div className="flex-1 glass-panel p-4 overflow-y-auto custom-scrollbar relative bg-black/30 border-white/5 flex flex-col">
          {!selectedFile ? (
            <div className="flex-1 flex flex-col items-center justify-center text-white/30">
              <ImageIcon size={48} className="mb-4 opacity-50" />
              <p>Sélectionnez un fichier dans la liste de gauche pour voir ses images.</p>
            </div>
          ) : loadingInfo ? (
            <div className="flex-1 flex flex-col items-center justify-center text-blue-300/80">
              <RefreshCw size={32} className="animate-spin mb-4" />
              <p>Analyse des images (GIM/MIG)...</p>
            </div>
          ) : binInfo ? (
            <div className="flex flex-col h-full">
              <div className="flex items-center justify-between mb-4 pb-4 border-b border-white/10">
                <div>
                  <h2 className="text-lg font-bold text-white">{selectedFile.name}</h2>
                  <p className="text-sm text-gray-400">{binInfo.total} images trouvées</p>
                </div>
                <div className="flex gap-2">
                  <div className="text-xs flex items-center gap-1 text-yellow-200/80 bg-yellow-900/30 px-3 py-1.5 rounded-lg border border-yellow-500/20">
                    <AlertTriangle size={14} /> 
                    <span>L'injection requiert une taille stricte. Padding automatique si l'image est plus petite.</span>
                  </div>
                </div>
              </div>
              
              <div className="grid grid-cols-1 gap-4 pb-4">
                {binInfo.gims.map((gim) => (
                  <div key={gim.index} className="bg-black/40 border border-white/5 rounded-xl p-4 flex flex-col gap-3">
                    <div className="flex flex-wrap items-center justify-between gap-4">
                        
                        <div className="flex items-start gap-4">
                            <div className="bg-blue-900/40 border border-blue-500/30 rounded-lg p-2 flex items-center justify-center font-mono text-sm w-12 h-12">
                                #{gim.index}
                            </div>
                            <div className="flex flex-col">
                                <span className="text-sm font-semibold text-gray-200">
                                  Offset: <span className="font-mono text-blue-300">0x{gim.offset.toString(16).toUpperCase()}</span>
                                </span>
                                <span className="text-xs text-gray-400">
                                  Taille Exigée: <span className="font-mono text-blue-200">{gim.size} bytes</span>
                                </span>
                                <span className="text-xs text-gray-500 mt-1">
                                  Infos: {gim.info} | Palette: {gim.has_palette ? 'Oui' : 'Non'}
                                </span>
                            </div>
                        </div>
                        
                        <div className="flex flex-wrap items-center gap-2">
                            <button
                              onClick={() => setPreviewIdx(previewIdx === gim.index ? null : gim.index)}
                              className={`glass-button px-3 py-1.5 text-xs flex items-center gap-1.5 transition-colors ${previewIdx === gim.index ? 'bg-blue-600 border-blue-500' : ''}`}
                            >
                              <Eye size={14} /> {previewIdx === gim.index ? 'Masquer' : 'Aperçu'}
                            </button>
                            
                            <button 
                              onClick={() => extractSingle(gim.index, gim.offset, gim.size, "png")}
                              className="glass-button px-3 py-1.5 text-xs flex items-center gap-1.5 hover:bg-white/10"
                            >
                              <Download size={14} /> PNG
                            </button>
                            
                            <button 
                              onClick={() => extractSingle(gim.index, gim.offset, gim.size, "gim")}
                              className="glass-button px-3 py-1.5 text-xs flex items-center gap-1.5 hover:bg-white/10 border-green-500/30 text-green-200"
                            >
                              <Download size={14} /> GIM Brut
                            </button>

                            <button 
                              onClick={() => {
                                const input = document.createElement('input');
                                input.type = 'file';
                                input.accept = '.png,.gim';
                                input.onchange = (e) => {
                                  const file = e.target.files[0];
                                  if (file) injectGim(gim.index, gim.offset, gim.size, file);
                                };
                                input.click();
                              }}
                              disabled={injecting}
                              className="glass-button px-3 py-1.5 text-xs flex items-center gap-1.5 border-yellow-500/50 bg-yellow-900/30 text-yellow-200 hover:bg-yellow-500/40 transition-colors"
                            >
                              <Upload size={14} /> Injecter Mod
                            </button>
                        </div>
                    </div>
                    
                    <AnimatePresence>
                      {previewIdx === gim.index && (
                        <motion.div 
                          initial={{ opacity: 0, height: 0 }}
                          animate={{ opacity: 1, height: 'auto' }}
                          exit={{ opacity: 0, height: 0 }}
                          className="mt-2 bg-black/60 rounded-lg p-4 flex justify-center items-center border border-white/5 relative overflow-hidden"
                        >
                          {/* Checkerboard background for transparency */}
                          <div className="absolute inset-0 z-0" style={{
                            backgroundImage: 'linear-gradient(45deg, #222 25%, transparent 25%), linear-gradient(-45deg, #222 25%, transparent 25%), linear-gradient(45deg, transparent 75%, #222 75%), linear-gradient(-45deg, transparent 75%, #222 75%)',
                            backgroundSize: '20px 20px',
                            backgroundPosition: '0 0, 0 10px, 10px -10px, -10px 0px'
                          }}></div>
                          
                          <img 
                            src={`http://127.0.0.1:8002/api/image/preview?bin_path=${encodeURIComponent(selectedFile.full_path)}&offset=${gim.offset}&size=${gim.size}`} 
                            alt={`Preview ${gim.index}`}
                            className="max-w-full max-h-96 object-contain pixelated relative z-10 shadow-2xl"
                            onError={(e) => { 
                                e.target.style.display = 'none'; 
                                e.target.nextSibling.style.display = 'block';
                            }}
                          />
                          <div className="hidden relative z-10 text-red-400 text-sm">
                            Aperçu indisponible (Format non pris en charge ou GIM corrompu).
                          </div>
                        </motion.div>
                      )}
                    </AnimatePresence>
                  </div>
                ))}
              </div>
            </div>
          ) : null}
        </div>
      </div>
    </div>
  );
}

import React, { useState } from 'react';
import { Archive, Disc, Folder, Download, Loader } from 'lucide-react';

export default function IsoExtractor({ addLog, browse, outDir, setOutDir }) {
  const [isoPath, setIsoPath] = useState('');
  const [isExtracting, setIsExtracting] = useState(false);

  const handleExtract = async () => {
    if (!isoPath) return alert("Veuillez d'abord sélectionner un fichier ISO !");
    if (!outDir) return alert("Veuillez définir un dossier de travail !");
    
    setIsExtracting(true);
    addLog("Analyse de l'ISO et extraction des fichiers audio...", "INFO");

    try {
      const res = await fetch("http://127.0.0.1:8001/api/iso/extract", {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ iso_path: isoPath, out_dir: outDir })
      });
      
      const data = await res.json();
      if (res.ok) {
        addLog("Extraction terminee dans " + outDir, "OK");
        let msg = "Extraction terminee avec succes !\n\n";
        if (data.details) {
            if (data.details["VOICEALL.BIN"]) msg += "OK: VOICEALL.BIN extrait.\n";
            else msg += "ERREUR: VOICEALL.BIN introuvable.\n";
            if (data.details["BGMALL.BIN"]) msg += "OK: BGMALL.BIN extrait.\n";
            else msg += "ERREUR: BGMALL.BIN introuvable.\n";
        }
        alert(msg);
      } else {
        addLog(data.detail || "Erreur d'extraction", "ERROR");
        alert("Erreur : " + data.detail);
      }
    } catch (e) {
      addLog("Erreur de connexion au serveur.", "ERROR");
    } finally {
      setIsExtracting(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      const file = files[0];
      if (file.name.toLowerCase().endsWith('.iso')) {
        setIsoPath(file.path || file.name); 
      } else {
        alert("Veuillez glisser un fichier .ISO");
      }
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  return (
    <div className="glass-panel p-6 flex flex-col space-y-6 h-full">
      
      {/* Explications */}
      <div className="bg-blue-900/20 border border-blue-500/20 p-4 rounded-xl flex items-start gap-3">
        <Archive className="text-blue-400 mt-1" size={20} />
        <div>
          <h3 className="text-blue-100 font-semibold mb-1">Extraction automatique</h3>
          <p className="text-blue-200/70 text-sm">
            Cet outil analyse votre ISO original et extrait instantanément les fichiers <span className="text-blue-300 font-mono">VOICEALL.BIN</span> et <span className="text-blue-300 font-mono">BGMALL.BIN</span> dans votre dossier de travail pour que vous puissiez commencer à les modifier.
          </p>
        </div>
      </div>

      <div className="space-y-4">
        {/* ISO Input */}
        <div className="flex flex-col">
          <label className="text-xs text-blue-200/70 mb-1 font-semibold uppercase tracking-wider">Fichier ISO Original du jeu</label>
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
              title="Parcourir"
            >
              <Folder size={18} />
            </button>
          </div>
        </div>

        {/* Drag & Drop Zone */}
        <div 
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          className="border-2 border-dashed border-blue-500/30 rounded-xl p-10 flex flex-col items-center justify-center text-center hover:border-blue-500/60 transition-colors cursor-pointer bg-blue-950/20"
          onClick={() => browse('file', setIsoPath, '.iso')}
        >
          <Disc size={48} className="text-blue-400/50 mb-3" />
          <p className="text-blue-100 font-medium text-lg">Glissez et déposez votre ISO ici</p>
          <p className="text-blue-200/60 text-sm mt-1">ou cliquez pour parcourir</p>
        </div>
      </div>

      <div className="flex-1"></div>

      {/* Extract Button */}
      <button
        onClick={handleExtract}
        disabled={isExtracting}
        className={"w-full py-3 px-4 rounded-xl font-bold flex items-center justify-center gap-2 transition-all " + (isExtracting ? 'bg-blue-800 text-blue-300 cursor-not-allowed' : 'bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white shadow-lg shadow-blue-500/25 hover:shadow-blue-500/40')}
      >
        {isExtracting ? (
          <><Loader className="animate-spin" size={20} /> Extraction en cours...</>
        ) : (
          <><Download size={20} /> Extraire les fichiers audio</>
        )}
      </button>

    </div>
  );
}



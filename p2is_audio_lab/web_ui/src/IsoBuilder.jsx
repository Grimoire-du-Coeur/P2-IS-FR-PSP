import React, { useState, useEffect } from 'react';
import { File, Disc, Save, Loader } from 'lucide-react';

export default function IsoBuilder({ addLog, browse, sourceBinPath, outDir }) {
  const [isoPath, setIsoPath] = useState(() => localStorage.getItem('isoPath') || '');
  const [binPath, setBinPath] = useState(() => localStorage.getItem('isoBinPath') || '');
  const [internalPath, setInternalPath] = useState('/PSP_GAME/USRDIR/sdata/BGMALL.BIN');
  const [isBuilding, setIsBuilding] = useState(false);

  useEffect(() => { localStorage.setItem('isoPath', isoPath); }, [isoPath]);
  useEffect(() => { localStorage.setItem('isoBinPath', binPath); }, [binPath]);

  useEffect(() => {
    if (sourceBinPath) {
      const upper = sourceBinPath.toUpperCase();
      if (upper.includes('VOICEALL.BIN')) {
        setInternalPath('/PSP_GAME/USRDIR/sdata/VOICEALL.BIN');
        if (!binPath || !binPath.toUpperCase().includes('VOICEALL')) {
           setBinPath(sourceBinPath.replace('.BIN', '_MOD.BIN').replace('.bin', '_MOD.BIN'));
        }
      } else if (upper.includes('BGMALL.BIN')) {
        setInternalPath('/PSP_GAME/USRDIR/sdata/BGMALL.BIN');
        if (!binPath || !binPath.toUpperCase().includes('BGMALL')) {
           setBinPath(sourceBinPath.replace('.BIN', '_MOD.BIN').replace('.bin', '_MOD.BIN'));
        }
      }
    }
  }, [sourceBinPath]);

    const [isoName, setIsoName] = useState('');
    useEffect(() => {
        if (isoPath) {
            const parts = isoPath.split(/[/\\]/);
            setIsoName(parts[parts.length - 1]);
        }
    }, [isoPath]);

    const buildIso = async () => {
        if (!isoPath || !binPath || !internalPath) {
            return alert("Veuillez remplir tous les champs !");
        }
        let outIsoPath = isoPath.replace('.iso', '_MOD.iso').replace('.ISO', '_MOD.iso');
        if (outDir && isoName) {
            const modName = isoName.replace('.iso', '_MOD.iso').replace('.ISO', '_MOD.iso');
            outIsoPath = outDir.endsWith('\\') || outDir.endsWith('/') ? outDir + modName : outDir + '\\' + modName;
        }

    try {
      const res = await fetch(`http://127.0.0.1:8001/api/iso/patch`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          iso_path: isoPath,
          bin_path: binPath,
          internal_path: internalPath,
          out_iso_path: outIsoPath
        })
      });
      
      const data = await res.json();
      if (res.ok) {
        addLog(data.msg, "OK");
        alert(`Succès ! L'ISO a été créé : \n${outIsoPath}`);
      } else {
        addLog(data.detail || "Erreur de reconstruction", "ERROR");
        alert(`Erreur : ${data.detail}`);
      }
    } catch (e) {
      addLog(e.message, "ERROR");
      alert(`Erreur de connexion : ${e.message}`);
    } finally {
      setIsBuilding(false);
    }
  };

  return (
    <div className="glass-panel p-6 flex flex-col space-y-6">
      <div className="flex flex-col mb-4">
        <h2 className="text-xl font-bold text-blue-200 flex items-center gap-2">
          <Disc size={24} /> Créateur d'ISO (Patch PyCdlib)
        </h2>
        <p className="text-sm text-gray-400 mt-2">
          Cette page permet de remplacer directement le fichier BGMALL.BIN ou VOICEALL.BIN au sein de l'ISO original du jeu, et générer un nouvel ISO jouable (Persona 2_MOD.iso).
        </p>
      </div>

      <div className="space-y-4 bg-black/10 p-4 rounded-xl border border-white/5">
        
        {/* ISO Original */}
        <div className="flex flex-col">
          <label className="text-xs text-blue-200/70 mb-1 font-semibold uppercase tracking-wider">Fichier ISO Original (.iso)</label>
          <div className="flex items-center space-x-2">
            <input 
              type="text" 
              value={isoPath}
              readOnly
              placeholder="C:\...\Persona 2 Innocent Sin.iso"
              className="glass-input flex-1"
            />
            <button 
              onClick={() => browse('file', setIsoPath, '.iso')}
              className="p-2 bg-blue-500/20 hover:bg-blue-500/40 border border-blue-500/30 rounded-lg text-blue-200 transition-colors cursor-pointer" 
              title="Parcourir"
            >
              <Disc size={20} />
            </button>
          </div>
        </div>

        {/* Fichier BIN Modifié */}
        <div className="flex flex-col">
          <label className="text-xs text-blue-200/70 mb-1 font-semibold uppercase tracking-wider">Fichier BIN Modifié (_MOD.BIN)</label>
          <div className="flex items-center space-x-2">
            <input 
              type="text" 
              value={binPath}
              readOnly
              placeholder="C:\...\BGMALL_MOD.BIN"
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

        {/* Chemin interne */}
        <div className="flex flex-col">
          <label className="text-xs text-blue-200/70 mb-1 font-semibold uppercase tracking-wider">Chemin de destination dans l'ISO</label>
          <div className="flex items-center space-x-2">
            <input 
              type="text" 
              value={internalPath}
              onChange={(e) => setInternalPath(e.target.value)}
              placeholder="/PSP_GAME/USRDIR/sdata/BGMALL.BIN"
              className="glass-input flex-1 font-mono text-sm"
            />
          </div>
          <p className="text-xs text-gray-500 mt-1">Exemples: /PSP_GAME/USRDIR/sdata/BGMALL.BIN ou /PSP_GAME/USRDIR/sdata/VOICEALL.BIN</p>
        </div>

      </div>

      <div className="pt-4 border-t border-white/5 flex justify-end">
        <button 
          onClick={buildIso}
          disabled={isBuilding}
          className={`py-3 px-6 ${isBuilding ? 'bg-green-600/30 text-green-300' : 'bg-green-600 hover:bg-green-500 text-white'} font-semibold rounded-xl transition-all shadow-[0_0_15px_rgba(22,163,74,0.3)] flex items-center gap-2`}
        >
          {isBuilding ? (
            <>
              <Loader className="animate-spin" size={20} /> Patch de l'ISO en cours...
            </>
          ) : (
            <>
              <Save size={20} /> Générer l'ISO Patché
            </>
          )}
        </button>
      </div>

    </div>
  );
}




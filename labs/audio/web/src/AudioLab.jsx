import React, { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import { Download, Folder, Music, Play, Square, CheckCircle, Save, Upload, File } from 'lucide-react';

const API = 'http://127.0.0.1:8001/api/audio';

const post = (route, body) =>
  fetch(`${API}/${route}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });

export default function AudioLab({ t, addLog, browse }) {
  const [binPath, setBinPath] = useState('');
  const [outDir, setOutDir] = useState('');
  const [atracToolPath, setAtracToolPath] = useState(() => {
    try { return localStorage.getItem('atracToolPath') || ''; } catch { return ''; }
  });
  const [binInfo, setBinInfo] = useState(null);
  const [isExtracting, setIsExtracting] = useState(false);
  // null = « Prêt » dans la langue active ; sinon message du serveur ou clé traduite
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(false);
  const [notes, setNotes] = useState({});
  const [playingIdx, setPlayingIdx] = useState(null);

  const audioRef = useRef(new Audio());

  // Fin de lecture : on remet l'icône Play
  useEffect(() => {
    const audio = audioRef.current;
    const handleEnded = () => setPlayingIdx(null);
    audio.addEventListener('ended', handleEnded);
    return () => audio.removeEventListener('ended', handleEnded);
  }, []);

  useEffect(() => {
    if (binPath) loadBinInfo();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [binPath]);

  useEffect(() => {
    try { localStorage.setItem('atracToolPath', atracToolPath); } catch { /* stockage indisponible */ }
  }, [atracToolPath]);

  const loadBinInfo = async () => {
    try {
      const res = await post('info', { bin_path: binPath });
      const data = await res.json();
      if (data.status === 'ok') {
        setBinInfo(data);
        // Dossier de sortie par défaut : à côté du BIN, dans un dossier à son nom
        const sep = binPath.includes('\\') ? '\\' : '/';
        const parts = binPath.split(sep);
        const fileName = parts.pop().replace(/\.BIN$/i, '');
        setOutDir([...parts, fileName].join(sep));
        loadNotes();
        addLog(`${t('file_loaded')} ${data.total} ${t('tracks_detected')}.`, 'OK');
      } else {
        setBinInfo(null);
      }
    } catch {
      setBinInfo(null);
      addLog(t('bin_load_error'), 'ERROR');
    }
  };

  const loadNotes = async () => {
    try {
      const res = await post('notes/load', { bin_path: binPath });
      setNotes((await res.json()) || {});
    } catch { /* pas de notes */ }
  };

  const saveNotes = async () => {
    try {
      await post('notes/save', { bin_path: binPath, notes });
      addLog(t('notes_saved'), 'OK');
    } catch {
      addLog(t('notes_error'), 'ERROR');
    }
  };

  const extractAll = async () => {
    if (!binPath || !outDir) return alert(t('need_bin_out'));
    setIsExtracting(true);
    setStatus(t('extract_all_wait'));
    try {
      const res = await post('extract', { bin_path: binPath, out_dir: outDir });
      const data = await res.json();
      setStatus(data.msg);
    } catch (e) {
      console.error(e);
      setStatus(t('extract_all_error'));
    } finally {
      setIsExtracting(false);
    }
  };

  const injectVoice = async (index, wavPath) => {
    if (!wavPath) return;
    setLoading(true);
    setStatus(t('injecting'));
    addLog(`${t('injecting_track')} #${index}...`, 'INFO');
    const outBinPath = binPath.replace(/\.BIN$/i, '_MOD.BIN');
    try {
      const res = await post('inject', {
        bin_path: binPath,
        voice_index: index,
        wav_path: wavPath,
        out_bin_path: outBinPath,
        at3tool_path: atracToolPath,
      });
      const data = await res.json();
      if (res.ok) addLog(data.msg, 'OK');
      else addLog(data.detail, 'ERROR');
    } catch (e) {
      addLog(e.message, 'ERROR');
    }
    setStatus(null);
    setLoading(false);
  };

  const playAudio = (index) => {
    if (playingIdx === index) {
      audioRef.current.pause();
      setPlayingIdx(null);
      return;
    }
    audioRef.current.src = `${API}/stream?bin_path=${encodeURIComponent(binPath)}&index=${index}`;
    audioRef.current.play().catch((e) => addLog(`${t('play_error')} ${e.message}`, 'ERROR'));
    setPlayingIdx(index);
  };

  const handleNoteChange = (idx, val) => setNotes((prev) => ({ ...prev, [idx]: val }));

  const iconButton =
    'p-2 bg-blue-500/20 hover:bg-blue-500/40 border border-blue-500/30 rounded-lg text-blue-200 transition-colors cursor-pointer';
  const label = 'text-xs text-blue-200/70 mb-1 font-semibold uppercase tracking-wider';

  return (
    <div className="h-full">
      <motion.div
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        className="glass-panel h-full p-6 flex flex-col space-y-4"
      >
        <div className="mb-4 space-y-4 bg-black/10 p-4 rounded-xl border border-white/5">
          {/* Dossier de travail */}
          <div className="flex flex-col">
            <label className={label}>{t('work_dir_extract')}</label>
            <div className="flex items-center space-x-2">
              <input
                type="text"
                value={outDir}
                onChange={(e) => setOutDir(e.target.value)}
                placeholder="C:\...\P2IS_FR_audio\VOICEALL"
                className="glass-input flex-1"
              />
              <button onClick={() => browse('dir', setOutDir)} className={iconButton} title={t('browse')}>
                <Folder size={20} />
              </button>
            </div>
          </div>

          {/* ATRACTool */}
          <div className="flex flex-col">
            <label className={label}>{t('audio_compressor')}</label>
            <div className="flex items-center space-x-2">
              <input
                type="text"
                value={atracToolPath}
                onChange={(e) => setAtracToolPath(e.target.value)}
                placeholder={`C:\\...\\ATRACTool-Rel-Release.exe ${t('optional')}`}
                className="glass-input flex-1"
              />
              <button onClick={() => browse('file', setAtracToolPath, '.exe')} className={iconButton} title={t('browse')}>
                <File size={20} />
              </button>
            </div>
          </div>

          {/* Fichier source */}
          <div className="flex flex-col">
            <label className={label}>{t('source_bin')}</label>
            <div className="flex items-center space-x-2">
              <input type="text" value={binPath} readOnly placeholder="C:\...\VOICEALL.BIN" className="glass-input flex-1" />
              <button onClick={() => browse('file', setBinPath, '.BIN')} className={iconButton} title={t('browse')}>
                <File size={20} />
              </button>
            </div>
          </div>

          {binInfo && (
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-t border-white/5 pt-4">
              <span className="text-sm font-medium text-blue-200 flex items-center gap-2">
                <CheckCircle size={16} className="text-green-400" />
                {binInfo.total.toLocaleString()} {t('tracks_detected')}
              </span>
              <button
                onClick={extractAll}
                disabled={isExtracting}
                className={`glass-button text-sm flex items-center justify-center space-x-2 py-2 ${isExtracting ? 'opacity-50 cursor-not-allowed' : ''}`}
              >
                <Download size={16} /> <span>{isExtracting ? t('extracting_short') : t('extract_all')}</span>
              </button>
            </div>
          )}

          <p className="text-xs text-blue-200/60">{status ?? t('ready')}</p>
        </div>

        {/* Liste des pistes */}
        <div className="flex-1 bg-black/20 rounded-xl p-4 border border-white/5 relative overflow-hidden flex flex-col min-h-0">
          <div className="absolute top-[-50px] right-[-50px] w-64 h-64 bg-blue-500/10 rounded-full blur-3xl pointer-events-none"></div>

          {binInfo && (
            <div className="flex justify-between items-center mb-3 relative z-10 px-2 border-b border-white/5 pb-2">
              <h3 className="text-sm font-semibold text-blue-200">{t('voice_list')}</h3>
              <button onClick={saveNotes} className="glass-button py-1.5 px-3 text-xs flex items-center gap-2">
                <Save size={14} /> {t('save_notes')}
              </button>
            </div>
          )}

          {binInfo ? (
            <div className="flex-1 overflow-y-auto space-y-2 relative z-10 pr-2">
              {Array.from({ length: binInfo.total }).map((_, i) => (
                <div
                  key={i}
                  className="flex items-center gap-3 p-2 bg-white/5 hover:bg-white/10 border border-white/5 rounded-xl transition-colors"
                >
                  <span className="w-10 text-center text-xs font-bold text-gray-500">#{i}</span>

                  <button
                    onClick={() => playAudio(i)}
                    className={`w-9 h-9 rounded-full flex items-center justify-center transition-colors ${
                      playingIdx === i
                        ? 'bg-blue-500 text-white shadow-lg shadow-blue-500/30'
                        : 'bg-black/40 text-blue-300 hover:bg-blue-500/30 border border-white/5'
                    }`}
                  >
                    {playingIdx === i ? <Square size={14} fill="currentColor" /> : <Play size={14} fill="currentColor" className="ml-1" />}
                  </button>

                  <input
                    type="text"
                    placeholder={t('note_placeholder')}
                    value={notes[i] || ''}
                    onChange={(e) => handleNoteChange(i, e.target.value)}
                    onBlur={saveNotes}
                    className="glass-input flex-1 py-1.5 text-sm"
                  />

                  <button
                    onClick={async () => {
                      const wav = await browse('file', () => {}, '.wav');
                      if (wav) injectVoice(i, wav);
                    }}
                    disabled={loading}
                    className="glass-button px-3 py-1.5 text-xs flex items-center gap-1.5"
                  >
                    <Upload size={14} /> {t('replace_btn')}
                  </button>
                </div>
              ))}
            </div>
          ) : (
            <div className="flex-1 flex flex-col items-center justify-center text-blue-200/50 relative z-10">
              <Music size={48} className="mb-4 opacity-20" />
              <p>{t('no_source')}</p>
            </div>
          )}
        </div>
      </motion.div>
    </div>
  );
}

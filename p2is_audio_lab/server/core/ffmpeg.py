import os
import subprocess
import wave
import struct
from pathlib import Path
import tempfile

FFMPEG_CANDIDATES = [
    Path.home() / "Music" / "ffmpeg" / "ffmpeg-8.0-essentials_build" / "ffmpeg-8.0-essentials_build" / "bin" / "ffmpeg.exe",
    Path("C:/ffmpeg/bin/ffmpeg.exe"),
    Path("C:/Program Files/ffmpeg/bin/ffmpeg.exe"),
]

def find_ffmpeg() -> str:
    for c in FFMPEG_CANDIDATES:
        if c.exists():
            return str(c)
    return ""

def convert_to_pcm_wav(input_path: str, output_path: str, ffmpeg_exe: str, ar: str = "44100", ac: str = "1") -> bool:
    """Convertit n'importe quel audio en WAV 16-bit PCM via FFmpeg."""
    cmd = [
        ffmpeg_exe, "-y",
        "-i", input_path,
        "-acodec", "pcm_s16le",
        "-ar", ar,
        "-ac", ac,
        output_path
    ]
    r = subprocess.run(cmd, capture_output=True, timeout=60)
    return r.returncode == 0 and Path(output_path).exists()

def read_wav_pcm(wav_path: str) -> tuple[bytes, int, int]:
    """Lit un WAV PCM. Retourne (pcm_data, sample_rate, channels)."""
    with wave.open(wav_path, "rb") as wf:
        sr = wf.getframerate()
        ch = wf.getnchannels()
        sw = wf.getsampwidth()
        n  = wf.getnframes()
        raw = wf.readframes(n)
        if sw == 1:
            raw = bytes([(b - 128) << 8 for b in raw for _ in range(2)])
        elif sw == 4:
            samples = [struct.unpack_from("<i", raw, i*4)[0] >> 16 for i in range(n*ch)]
            raw = struct.pack(f"<{len(samples)}h", *samples)
        return raw, sr, ch

def build_riff_wav_from_pcm(pcm_data: bytes, sample_rate: int = 22050, channels: int = 1) -> bytes:
    """Construit un fichier RIFF/WAV à partir de données PCM 16-bit."""
    bits_per_sample = 16
    byte_rate = sample_rate * channels * bits_per_sample // 8
    block_align = channels * bits_per_sample // 8
    data_size = len(pcm_data)
    riff_size = 36 + data_size

    header = struct.pack(
        "<4sI4s4sIHHIIHH4sI",
        b"RIFF",
        riff_size,
        b"WAVE",
        b"fmt ",
        16,
        1,
        channels,
        sample_rate,
        byte_rate,
        block_align,
        bits_per_sample,
        b"data",
        data_size,
    )
    return header + pcm_data

def find_at3tool(user_path: str = None) -> str:
    candidates = []
    if user_path:
        # If user selected the ATRACTool exe, auto-resolve to psp_at3tool.exe
        p = Path(user_path)
        if p.name.lower() == "atractool-reloaded.exe":
            candidates.append(p.parent / "res" / "psp_at3tool.exe")
        elif p.name.lower() == "atractool-rel-release.exe":
            candidates.append(p.parent / "release" / "res" / "psp_at3tool.exe")
        else:
            candidates.append(p)
            
    candidates.extend([
        Path(r"C:\Users\nolan\Downloads\ATRACTool-Rel-Release\release\res\psp_at3tool.exe"),
        Path(r"C:\ATRACTool\release\res\psp_at3tool.exe"),
    ])
    for c in candidates:
        if c.exists():
            return str(c)
    return ""

def prepare_wav_for_injection(wav_path: str, user_at3tool_path: str = None, target_channels: int = 1, target_sr: int = 44100) -> bytes:
    """Pipelines : Audio -> FFmpeg -> PCM 16-bit -> psp_at3tool -> True ATRAC3+ WAV bytes."""
    ffmpeg_exe = find_ffmpeg()
    at3tool_exe = find_at3tool(user_at3tool_path)
    
    if not ffmpeg_exe:
        raise Exception("FFmpeg introuvable.")

    # 1. Utiliser ffmpeg pour convertir au bon sample rate et channel count
    fd_pcm, pcm_tmp = tempfile.mkstemp(suffix=".wav")
    os.close(fd_pcm)
    
    try:
        ok = convert_to_pcm_wav(wav_path, pcm_tmp, ffmpeg_exe, str(target_sr), str(target_channels))
        if not ok:
            raise Exception("Échec de la conversion FFmpeg vers PCM.")

        if at3tool_exe:
            # 2. Utiliser psp_at3tool pour encoder en vrai ATRAC3+
            fd_at3, at3_tmp = tempfile.mkstemp(suffix=".wav")
            os.close(fd_at3)
            
            try:
                cmd = [at3tool_exe, "-e", pcm_tmp, at3_tmp, "-br", "64"]
                res = subprocess.run(cmd, capture_output=True, timeout=60)
                
                if res.returncode == 0 and Path(at3_tmp).exists() and os.path.getsize(at3_tmp) > 0:
                    with open(at3_tmp, "rb") as f:
                        final_bytes = f.read()
                    return final_bytes
                else:
                    raise Exception(f"Échec de l'encodage ATRAC3+ avec psp_at3tool: {res.stderr.decode('utf-8', errors='ignore')}")
            finally:
                if Path(at3_tmp).exists():
                    os.unlink(at3_tmp)
        else:
            # Si psp_at3tool n'est pas là, on retombe sur l'ancienne méthode (injecter du PCM)
            # Mais la PSP risque de crasher !
            pcm, sr, ch = read_wav_pcm(pcm_tmp)
            if ch == 2:
                samples = list(struct.unpack(f"<{len(pcm)//2}h", pcm))
                mono = [(samples[i] + samples[i+1]) // 2 for i in range(0, len(samples), 2)]
                pcm = struct.pack(f"<{len(mono)}h", *mono)
            final_bytes = build_riff_wav_from_pcm(pcm, 44100, 1)
            return final_bytes
            
    finally:
        if Path(pcm_tmp).exists():
            os.unlink(pcm_tmp)

"""Transcribe a slice of an audio file: oir.py file start end"""
import subprocess, sys
import numpy as np
from faster_whisper import WhisperModel

f, a, b = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
pcm = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(a), "-to", str(b), "-i", f, "-f", "s16le", "-ac", "1", "-ar", "16000", "-"],
                     capture_output=True, check=True).stdout
segs, _ = WhisperModel("medium", device="cpu", compute_type="int8").transcribe(
    np.frombuffer(pcm, np.int16).astype(np.float32) / 32768.0, language="es", word_timestamps=True)
for s in segs:
    for w in s.words:
        print(f"{a + w.start:7.2f} {w.word}")

"""Word timestamps for a short PCM clip (16 kHz mono s16le) through Groq's whisper-large-v3 when GROQ_API_KEY is set
(seconds instead of minutes on this 2-core PC). words_pcm(pcm) -> [(word, start, end)] or None when there is no key,
so callers can fall back to local faster-whisper."""
import io, os, subprocess, wave


def key():
    return os.environ.get("GROQ_API_KEY") or subprocess.run(
        ["powershell", "-NoProfile", "-Command", "[Environment]::GetEnvironmentVariable('GROQ_API_KEY','User')"],
        capture_output=True, text=True).stdout.strip()


def words_pcm(pcm, offset=0.0):
    k = key()
    if not k:
        return None
    import requests
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(16000)
        w.writeframes(pcm)
    r = requests.post("https://api.groq.com/openai/v1/audio/transcriptions", headers={"Authorization": f"Bearer {k}"},
                      files={"file": ("clip.wav", buf.getvalue(), "audio/wav")},
                      data=[("model", "whisper-large-v3"), ("response_format", "verbose_json"),
                            ("timestamp_granularities[]", "word"), ("temperature", "0"), ("language", "es")], timeout=300)
    r.raise_for_status()
    return [(w["word"].strip(), round(w["start"] + offset, 3), round(w["end"] + offset, 3)) for w in r.json()["words"]]

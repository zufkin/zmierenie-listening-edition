from pathlib import Path
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
MASTER = ROOT / "book" / "audio-script-master-sk-2026-09-01.md"
OUT_DIR = ROOT / "dist" / "audio-2.1-calibration"
VOICE_ID = "htSeFhhpBaCgJzL05q6C"
MODEL_ID = "eleven_multilingual_v2"
OUTPUT_FORMAT = "mp3_44100_128"
SETTINGS = {
    "stability": 0.65,
    "similarity_boost": 0.80,
    "style": 0.0,
    "speed": 0.97,
    "use_speaker_boost": True,
}

def chapter_text(number: int) -> str:
    text = MASTER.read_text(encoding="utf-8")
    start = rf"^## {number:02d} · .*$"
    end = rf"^## {number + 1:02d} · .*$" if number < 12 else r"\Z"
    m1 = re.search(start, text, flags=re.M)
    if not m1:
        raise RuntimeError(f"chapter {number:02d} not found")
    tail = text[m1.end():]
    if number < 12:
        m2 = re.search(end, tail, flags=re.M)
        body = tail[:m2.start()] if m2 else tail
    else:
        body = tail
    body = re.sub(r"^\*Redakčné označenie — nečíta sa\.\*\s*", "", body, flags=re.M)
    body = body.strip()
    if not body:
        raise RuntimeError("empty chapter text")
    return body


def main() -> int:
    api_key = os.getenv("ELEVENLABS_API_KEY", "").strip()
    if not api_key:
        print("BLOCKED: ELEVENLABS_API_KEY is not available in this runtime", file=sys.stderr)
        return 20

    text = chapter_text(3)
    payload = json.dumps({
        "text": text,
        "model_id": MODEL_ID,
        "voice_settings": SETTINGS,
    }, ensure_ascii=False).encode("utf-8")
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}?output_format={OUTPUT_FORMAT}"
    req = urllib.request.Request(
        url,
        data=payload,
        method="POST",
        headers={
            "xi-api-key": api_key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as response:
            audio = response.read()
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        print(f"ElevenLabs HTTP {exc.code}: {detail[:1000]}", file=sys.stderr)
        return 21

    if len(audio) < 10000:
        print("Audio response unexpectedly small", file=sys.stderr)
        return 22

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    mp3 = OUT_DIR / "zmierenie-03-reflexia-audio-2.1-B.mp3"
    mp3.write_bytes(audio)
    sha = hashlib.sha256(audio).hexdigest()
    receipt = {
        "status": "CALIBRATION_SAMPLE_READY",
        "chapter": 3,
        "voiceId": VOICE_ID,
        "model": MODEL_ID,
        "outputFormat": OUTPUT_FORMAT,
        "voiceSettings": SETTINGS,
        "textSource": "book/audio-script-master-sk-2026-09-01.md",
        "textChanged": False,
        "bytes": len(audio),
        "sha256": sha,
        "file": mp3.name,
        "profile": "B",
    }
    (OUT_DIR / "receipt.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

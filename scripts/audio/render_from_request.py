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
REQUEST = ROOT / "audio-requests" / "current.json"
OUT_ROOT = ROOT / "dist" / "audio-mobile-first"
VOICE_ID = "GgshSttSyBqEDNtKedLz"
MODEL_ID = "eleven_multilingual_v2"
OUTPUT_FORMAT = "mp3_44100_128"

PROFILES = {
    "A": {"stability": 0.58, "similarity_boost": 0.80, "style": 0.0, "speed": 0.98, "use_speaker_boost": True},
    "B": {"stability": 0.65, "similarity_boost": 0.80, "style": 0.0, "speed": 0.97, "use_speaker_boost": True},
    "C": {"stability": 0.72, "similarity_boost": 0.80, "style": 0.0, "speed": 0.97, "use_speaker_boost": True},
}
ALLOWED_INTENTS = {"render_calibration", "render_batch_preview"}


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
    body = re.sub(r"^\*Redakčné označenie — nečíta sa\.\*\s*", "", body, flags=re.M).strip()
    if not body:
        raise RuntimeError(f"empty chapter {number:02d}")
    return body


def load_request() -> dict:
    req = json.loads(REQUEST.read_text(encoding="utf-8"))
    if req.get("schemaVersion") != 1:
        raise RuntimeError("unsupported schemaVersion")
    request_id = str(req.get("requestId", ""))
    if not re.fullmatch(r"[A-Za-z0-9._-]{1,80}", request_id):
        raise RuntimeError("invalid requestId")
    if req.get("intent") not in ALLOWED_INTENTS:
        raise RuntimeError("unsupported intent")
    profile = req.get("profile")
    if profile not in PROFILES:
        raise RuntimeError("unsupported profile")
    chapters = req.get("chapters")
    if not isinstance(chapters, list) or not chapters or len(chapters) > 12:
        raise RuntimeError("invalid chapters")
    if any(not isinstance(n, int) or n < 1 or n > 12 for n in chapters):
        raise RuntimeError("chapter out of range")
    if len(set(chapters)) != len(chapters):
        raise RuntimeError("duplicate chapter")
    if req["intent"] == "render_calibration" and chapters != [3]:
        raise RuntimeError("calibration is restricted to chapter 03")
    return req


def synthesize(api_key: str, text: str, settings: dict) -> bytes:
    payload = json.dumps({"text": text, "model_id": MODEL_ID, "voice_settings": settings}, ensure_ascii=False).encode("utf-8")
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}?output_format={OUTPUT_FORMAT}"
    request = urllib.request.Request(url, data=payload, method="POST", headers={
        "xi-api-key": api_key,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg",
    })
    with urllib.request.urlopen(request, timeout=180) as response:
        return response.read()


def main() -> int:
    api_key = os.getenv("ELEVENLABS_API_KEY", "").strip()
    if not api_key:
        print("BLOCKED: managed ELEVENLABS_API_KEY is not available", file=sys.stderr)
        return 20
    try:
        req = load_request()
        settings = PROFILES[req["profile"]]
        out_dir = OUT_ROOT / req["requestId"]
        out_dir.mkdir(parents=True, exist_ok=True)
        results = []
        for number in req["chapters"]:
            text = chapter_text(number)
            try:
                audio = synthesize(api_key, text, settings)
            except urllib.error.HTTPError as exc:
                detail = exc.read().decode("utf-8", errors="replace")
                print(f"ElevenLabs HTTP {exc.code}: {detail[:1000]}", file=sys.stderr)
                return 21
            if len(audio) < 10000:
                raise RuntimeError(f"chapter {number:02d}: audio unexpectedly small")
            filename = f"zmierenie-{number:02d}-reflexia-audio-2.1-{req['profile']}.mp3"
            path = out_dir / filename
            path.write_bytes(audio)
            results.append({
                "chapter": number,
                "file": filename,
                "bytes": len(audio),
                "sha256": hashlib.sha256(audio).hexdigest(),
            })
        receipt = {
            "status": "PREVIEW_RENDER_READY",
            "schemaVersion": 1,
            "requestId": req["requestId"],
            "intent": req["intent"],
            "chapters": req["chapters"],
            "profile": req["profile"],
            "voiceId": VOICE_ID,
            "model": MODEL_ID,
            "outputFormat": OUTPUT_FORMAT,
            "voiceSettings": settings,
            "textSource": "book/audio-script-master-sk-2026-09-01.md",
            "textChanged": False,
            "productionAudioChanged": False,
            "results": results,
        }
        (out_dir / "receipt.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(receipt, ensure_ascii=False))
        return 0
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 22


if __name__ == "__main__":
    raise SystemExit(main())

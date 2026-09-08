from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import tarfile
from datetime import datetime, timezone
from pathlib import Path

VERSION = "2.0"
ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "book"
DIST_ROOT = ROOT / "dist"
STAGE = DIST_ROOT / f"faculty-{VERSION}"
ARCHIVE = DIST_ROOT / f"zmierenie-faculty-release-{VERSION}.tar.gz"
FACULTY_AUDIO_BASE = "/sites/default/files/book/audio/"

if STAGE.exists():
    shutil.rmtree(STAGE)
DIST_ROOT.mkdir(exist_ok=True)
shutil.copytree(SOURCE, STAGE)
(STAGE / "drupal-iframe-snippet.html").unlink(missing_ok=True)

# Faculty production keeps the 12 approved audio tracks in the stable canonical
# media location. Rewire only the staged faculty HTML; GitHub Pages source stays
# unchanged. This prevents a faculty Release 2.0 cutover from restoring older
# bundled audio over the currently approved Audio 2.1 set.
rewired_audio_refs = 0
for page in sorted(STAGE.glob("chapter-*.html")):
    source = page.read_text(encoding="utf-8")
    updated, count = re.subn(
        r'src="\./audio/(zmierenie-\d{2}-reflexia\.mp3)"',
        lambda m: f'src="{FACULTY_AUDIO_BASE}{m.group(1)}"',
        source,
    )
    if count != 1:
        raise RuntimeError(f"Expected exactly one audio reflection in {page.name}; got {count}")
    page.write_text(updated, encoding="utf-8")
    rewired_audio_refs += count

if rewired_audio_refs != 12:
    raise RuntimeError(f"Expected 12 rewired faculty audio references; got {rewired_audio_refs}")

try:
    commit = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()
except Exception:
    commit = "unknown"

manifest = {
    "product": "Zmierenie – webová učebnica",
    "version": VERSION,
    "commit": commit,
    "builtAt": datetime.now(timezone.utc).isoformat(),
    "target": "/sites/default/files/zmierenie/",
    "entry": "index.html",
    "stablePdf": "https://tf.truni.sk/sites/default/files/book/zmierenie-ucebnica.pdf",
    "facultyAudioBase": FACULTY_AUDIO_BASE,
    "facultyAudioRefs": rewired_audio_refs,
}
(STAGE / "DEPLOYMENT.json").write_text(
    json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)

lines = []
for path in sorted(p for p in STAGE.rglob("*") if p.is_file() and p.name != "SHA256SUMS"):
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    lines.append(f"{digest}  {path.relative_to(STAGE).as_posix()}")
(STAGE / "SHA256SUMS").write_text("\n".join(lines) + "\n", encoding="utf-8")

with tarfile.open(ARCHIVE, "w:gz") as tar:
    for path in sorted(STAGE.rglob("*")):
        tar.add(path, arcname=path.relative_to(STAGE))

archive_digest = hashlib.sha256(ARCHIVE.read_bytes()).hexdigest()
Path(str(ARCHIVE) + ".sha256").write_text(
    f"{archive_digest}  {ARCHIVE.name}\n", encoding="utf-8"
)
print(ARCHIVE)

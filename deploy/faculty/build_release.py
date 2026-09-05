from __future__ import annotations

import hashlib
import json
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

if STAGE.exists():
    shutil.rmtree(STAGE)
DIST_ROOT.mkdir(exist_ok=True)
shutil.copytree(SOURCE, STAGE)
(STAGE / "drupal-iframe-snippet.html").unlink(missing_ok=True)

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

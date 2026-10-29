"""Validate the CSS-only scope and build reproducible release files (stdlib only)."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.2.1"
MATCHES = ["https://connectus.garmin.cn/app/*"]


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8").replace("\r\n", "\n")


def outputs() -> dict[str, str]:
    css = text("styles/theme-tokens.css") + "\n" + text("styles/site.css")
    if re.search(r"@import\b|url\s*\(|@font-face\b|expression\s*\(", css, re.I):
        raise ValueError("CSS must not load external resources or execute expressions")
    manifest = json.loads(text("extension/manifest.json"))
    expected = {
        "manifest_version": 3,
        "name": "Garmin Connect Liquid Glass",
        "version": VERSION,
        "description": "CSS-only appearance for the existing Garmin China web app.",
        "content_scripts": [{"matches": MATCHES, "css": ["skin.css"], "run_at": "document_start"}],
    }
    if manifest != expected:
        raise ValueError("Unexpected manifest field, version, script or permission scope")
    header = '''/* ==UserStyle==
@name Garmin Connect Liquid Glass (China)
@namespace garmin-connect-liquid-glass
@version 0.2.1
@description Presentation-only skin for the existing Garmin China web app
@author Garmin Connect Liquid Glass contributors
@license MIT
==/UserStyle== */
@-moz-document regexp("https://connectus\\\\.garmin\\\\.cn/app/.*") {
'''
    return {"extension/skin.css": css, "garmin-liquid-glass.user.css": header + css + "\n}\n"}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check committed generated CSS without writing")
    args = parser.parse_args()
    generated = outputs()
    if args.check:
        for name, content in generated.items():
            if text(name) != content:
                raise SystemExit(f"Generated file is out of date: {name}")
        print("Generated CSS and exact Garmin-only Manifest V3 scope verified.")
        return
    for name, content in generated.items():
        (ROOT / name).write_bytes(content.encode("utf-8"))
    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)
    filename = f"garmin-connect-liquid-glass-v{VERSION}-extension.zip"
    entries = {
        "manifest.json": text("extension/manifest.json"),
        "skin.css": generated["extension/skin.css"],
        "README.md": text("README.md"),
        "LICENSE": text("LICENSE"),
        "THIRD_PARTY_NOTICES.md": text("THIRD_PARTY_NOTICES.md"),
    }
    with zipfile.ZipFile(dist / filename, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, content in sorted(entries.items()):
            info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, content.encode("utf-8"), compresslevel=9)
    digest = hashlib.sha256((dist / filename).read_bytes()).hexdigest()
    (dist / "SHA256SUMS").write_bytes(f"{digest}  {filename}\n".encode("ascii"))
    print(f"Built {filename}\nSHA256 {digest}")


if __name__ == "__main__":
    main()

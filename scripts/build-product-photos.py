#!/usr/bin/env python3
"""Fetch CC-licensed Wikimedia product photos and emit inline catalogue data."""

from __future__ import annotations

import base64
import io
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCES_PATH = ROOT / "scripts" / "product-photo-sources.json"
OUT_JSON = ROOT / "scripts" / "product-photos-built.json"
UA = "OmegaCatalogueBot/1.0 (omegasolarproducts.com; educational catalogue)"

MAX_EDGE = 720
WEBP_QUALITY = 72


def api(params: dict) -> dict:
    q = urllib.parse.urlencode({**params, "format": "json"})
    url = f"https://commons.wikimedia.org/w/api.php?{q}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as exc:
            if exc.code == 429 and attempt < 5:
                time.sleep(2 ** attempt)
                continue
            raise


def resolve_file(title: str) -> str | None:
    if not title.startswith("File:"):
        title = "File:" + title
    data = api(
        {
            "action": "query",
            "titles": title,
            "prop": "imageinfo",
            "iiprop": "url",
            "iiurlwidth": str(MAX_EDGE),
        }
    )
    pages = data.get("query", {}).get("pages", {})
    for page in pages.values():
        if "missing" in page:
            return None
        info = (page.get("imageinfo") or [None])[0]
        if not info:
            return None
        return info.get("thumburl") or info.get("url")
    return None


def search_file(query: str) -> str | None:
    data = api(
        {
            "action": "query",
            "generator": "search",
            "gsrsearch": query,
            "gsrnamespace": "6",
            "gsrlimit": "5",
            "prop": "imageinfo",
            "iiprop": "url",
            "iiurlwidth": str(MAX_EDGE),
        }
    )
    pages = data.get("query", {}).get("pages", {})
    for page in sorted(pages.values(), key=lambda p: p.get("index", 0)):
        info = (page.get("imageinfo") or [None])[0]
        if info and info.get("thumburl"):
            return info["thumburl"]
    return None


def download(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as resp:
        return resp.read()


def to_webp_data_url(raw: bytes) -> str:
    im = Image.open(io.BytesIO(raw))
    if im.mode not in ("RGB", "RGBA"):
        im = im.convert("RGB")
    w, h = im.size
    scale = min(1.0, MAX_EDGE / max(w, h))
    if scale < 1.0:
        im = im.resize((int(w * scale), int(h * scale)), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, format="WEBP", quality=WEBP_QUALITY, method=6)
    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    return f"data:image/webp;base64,{b64}"


def main() -> int:
    sources = json.loads(SOURCES_PATH.read_text())
    built: dict[str, dict] = {}
    failures: list[str] = []
    cache: dict[str, str] = {}

    for model, meta in sources.items():
        if model.startswith("_"):
            continue
        file_title = meta["file"]
        caption = meta["caption"]
        url = resolve_file(file_title)
        if not url:
            url = search_file(meta.get("search") or file_title.replace(".jpg", "").replace(".JPG", ""))
        if not url:
            failures.append(model)
            print(f"FAIL {model}: no image for {file_title}", file=sys.stderr)
            continue
        try:
            if url in cache:
                src = cache[url]
            else:
                raw = download(url)
                src = to_webp_data_url(raw)
                cache[url] = src
            time.sleep(0.35)
            built[model] = {
                "view": "product",
                "caption": caption,
                "src": src,
                "source": file_title,
            }
            kb = len(src) // 1024
            print(f"OK {model}: {kb} KiB data URL")
        except Exception as exc:  # noqa: BLE001
            failures.append(model)
            print(f"FAIL {model}: {exc}", file=sys.stderr)

    OUT_JSON.write_text(json.dumps(built, indent=2))
    print(f"Wrote {len(built)} photos to {OUT_JSON}")
    if failures:
        print(f"Failed models: {', '.join(failures)}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

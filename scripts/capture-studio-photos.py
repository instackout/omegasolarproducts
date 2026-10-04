#!/usr/bin/env python3
"""Capture studio stills (hero/front/side/top[/exploded]) from the live WebGL engine.

Writes scripts/studio-photos-built.json as { model: [ {view, caption, src}, ... ] }.
Pass model keys as arguments to recapture a subset; otherwise recaptures every
OPARTS.parts key used by a product.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
OUT = ROOT / "scripts" / "studio-photos-built.json"
BASE_URL = "http://127.0.0.1:8080/"

VIEWS = [
    ("hero", "3/4 view"),
    ("front", "Front elevation"),
    ("side", "Side elevation"),
    ("top", "Plan view"),
]


def product_models() -> list[str]:
    text = INDEX.read_text()
    return sorted(set(re.findall(r"p\('[^']+',\s*'[^']+',\s*'[^']+',\s*'([^']+)'", text)))


def explodable() -> set[str]:
    text = INDEX.read_text()
    m = re.search(r"var EXPLODABLE = \{([^}]+)\}", text, re.S)
    if not m:
        return set()
    return set(re.findall(r"(\w+):\s*1", m.group(1)))


def main() -> int:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Install playwright: pip install playwright && playwright install chromium", file=sys.stderr)
        return 1

    wanted = sys.argv[1:] or product_models()
    explode = explodable()
    built: dict[str, list] = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 720, "height": 720})
        page.goto(BASE_URL, wait_until="networkidle", timeout=120_000)
        page.wait_for_function("() => typeof window.__captureStudioPhoto === 'function'", timeout=60_000)

        for model in wanted:
            frames = []
            views = list(VIEWS)
            if model in explode:
                views.append(("exploded", "Exploded assembly"))
            for view, caption in views:
                data_url = page.evaluate(
                    "async ({model, view}) => await window.__captureStudioPhoto(model, view)",
                    {"model": model, "view": view},
                )
                if not data_url or not str(data_url).startswith("data:image/webp"):
                    print(f"FAIL {model}/{view}", file=sys.stderr)
                    continue
                frames.append({"view": view, "caption": caption, "src": data_url})
                print(f"OK {model}/{view}: {len(data_url) // 1024} KiB")
            if frames:
                built[model] = frames

        browser.close()

    existing = json.loads(OUT.read_text()) if OUT.is_file() else {}
    existing.update(built)
    OUT.write_text(json.dumps(existing, indent=2))
    print(f"Wrote {len(built)} models ({sum(len(v) for v in built.values())} frames) to {OUT}")
    return 0 if len(built) == len(wanted) else 1


if __name__ == "__main__":
    sys.exit(main())

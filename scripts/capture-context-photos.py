#!/usr/bin/env python3
"""Capture in-situ product stills from the live WebGL engine (Playwright + Chromium)."""

from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
OUT = ROOT / "scripts" / "product-photos-built.json"
BASE_URL = "http://127.0.0.1:8080/"


def model_keys() -> list[str]:
    text = INDEX.read_text()
    return sorted(set(re.findall(r'P\["([^"]+)"\]', text)))


def main() -> int:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Install playwright: pip install playwright && playwright install chromium", file=sys.stderr)
        return 1

    models = model_keys()
    built: dict[str, dict] = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 900, "height": 900})
        page.goto(BASE_URL, wait_until="networkidle", timeout=120_000)
        page.wait_for_function("() => typeof window.__captureProductPhoto === 'function'", timeout=60_000)

        for model in models:
            data_url = page.evaluate(
                "async (model) => await window.__captureProductPhoto(model)",
                model,
            )
            if not data_url or not str(data_url).startswith("data:image/webp"):
                print(f"FAIL {model}", file=sys.stderr)
                continue
            built[model] = {
                "view": "product",
                "caption": "Installed view",
                "src": data_url,
            }
            print(f"OK {model}: {len(data_url) // 1024} KiB")
            time.sleep(0.15)

        browser.close()

    OUT.write_text(json.dumps(built, indent=2))
    print(f"Wrote {len(built)} images to {OUT}")
    return 0 if len(built) == len(models) else 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Append or replace studio stills for models in studio-photos-built.json.

Does not rewrite the whole OPHOTOS block. Product frames stay in the
mergeProductPhotos() block and are unshifted at runtime.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILT = ROOT / "scripts" / "studio-photos-built.json"
INDEX = ROOT / "index.html"
MARKER = "  /* PRODUCT_PHOTOS:BEGIN */"


def emit_model(model: str, frames: list[dict]) -> str:
    lines = [f'  P["{model}"] = [']
    for i, fr in enumerate(frames):
        comma = "," if i < len(frames) - 1 else ""
        lines.append(
            "    { view: "
            + json.dumps(fr["view"])
            + ", caption: "
            + json.dumps(fr["caption"])
            + ", src: "
            + json.dumps(fr["src"])
            + " }"
            + comma
        )
    lines.append("  ];")
    return "\n".join(lines)


def replace_or_append(html: str, model: str, frames: list[dict]) -> str:
    block = emit_model(model, frames)
    pattern = re.compile(rf'  P\["{re.escape(model)}"\] = \[.*?\n  \];\n', re.S)
    if pattern.search(html):
        return pattern.sub(block + "\n", html, count=1)
    if MARKER not in html:
        raise SystemExit("PRODUCT_PHOTOS marker missing")
    return html.replace(MARKER, block + "\n" + MARKER, 1)


def main() -> None:
    studio = json.loads(BUILT.read_text())
    html = INDEX.read_text()
    for model, frames in sorted(studio.items()):
        html = replace_or_append(html, model, frames)
    INDEX.write_text(html)
    (ROOT / "404.html").write_text(html)
    print(f"Injected studio stills for {len(studio)} models")


if __name__ == "__main__":
    main()

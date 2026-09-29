#!/usr/bin/env python3
"""Inject built product photos into index.html (and sync 404.html)."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILT = ROOT / "scripts" / "product-photos-built.json"
INDEX = ROOT / "index.html"
MARKER_BEGIN = "/* PRODUCT_PHOTOS:BEGIN */"
MARKER_END = "/* PRODUCT_PHOTOS:END */"


def js_object(data: dict) -> str:
    """Compact but valid JS object literal for model -> {caption, src}."""
    parts = []
    for model in sorted(data.keys()):
        row = data[model]
        cap = json.dumps(row["caption"])
        src = json.dumps(row["src"])
        parts.append(f'"{model}":{{"caption":{cap},"src":{src}}}')
    return "{\n    " + ",\n    ".join(parts) + "\n  }"


def main() -> None:
    built = json.loads(BUILT.read_text())
    block = f"""  {MARKER_BEGIN}
  (function mergeProductPhotos() {{
    var refs = {js_object(built)};
    var k, row;
    for (k in refs) {{
      if (!Object.prototype.hasOwnProperty.call(refs, k)) continue;
      row = refs[k];
      if (!P[k]) P[k] = [];
      P[k].unshift({{ view: "product", caption: row.caption, src: row.src }});
    }}
  }})();
  {MARKER_END}
"""
    html = INDEX.read_text()
    pattern = re.compile(
        r"\s*/\* PRODUCT_PHOTOS:BEGIN \*/.*?/\* PRODUCT_PHOTOS:END \*/\s*",
        re.S,
    )
    if pattern.search(html):
        html = pattern.sub("\n" + block + "\n", html)
    elif "root.OPHOTOS = P;" in html:
        html = html.replace("root.OPHOTOS = P;", block + "root.OPHOTOS = P;", 1)
    else:
        raise SystemExit("Could not find root.OPHOTOS = P; in index.html")
    INDEX.write_text(html)
    (ROOT / "404.html").write_text(html)
    print(f"Injected {len(built)} product photos into index.html / 404.html")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Regenerate the machine-maintained section of AGENTS.md from the repository.

Run manually:  python3 scripts/sync-agent-context.py
Installed via:  bash scripts/install-git-hooks.sh
"""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENTS_MD = ROOT / "AGENTS.md"
INDEX = ROOT / "index.html"
NOT_FOUND = ROOT / "404.html"

BEGIN = "<!-- AGENT_CONTEXT:BEGIN auto -->"
END = "<!-- AGENT_CONTEXT:END auto -->"


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()[:12]


def read_index() -> str:
    return INDEX.read_text(encoding="utf-8")


def count_products(html: str) -> int:
    return len(re.findall(r"\bp\(\s*['\"]", html))


def extract_cat_ids(html: str) -> list[str]:
    block = re.search(r"var CATS = \[(.*?)\];", html, re.DOTALL)
    if not block:
        return []
    return re.findall(r"id:\s*'([^']+)'", block.group(1))


def count_inlined_webp(html: str) -> int:
    return len(re.findall(r"data:image/webp;base64,", html))


def extract_routes(html: str) -> list[str]:
    routes = []
    for m in re.finditer(r"else if \(seg\[0\] === '([^']+)'\)", html):
        routes.append(m.group(1))
    return sorted(set(routes))


def section_line_markers(html: str) -> list[str]:
    """Major `index.html` regions (from banner comments)."""
    return re.findall(
        r"/\* =+\s*\n\s*Omega Instruments — ([^\n]+)",
        html,
    )


def build_auto_block() -> str:
    html = read_index()
    lines = INDEX.read_text(encoding="utf-8").count("\n") + 1
    size_kb = INDEX.stat().st_size / 1024
    products = count_products(html)
    cats = extract_cat_ids(html)
    webp_count = count_inlined_webp(html)
    routes = extract_routes(html)
    regions = section_line_markers(html)
    index_hash = file_sha256(INDEX)
    not_found_match = (
        NOT_FOUND.exists() and file_sha256(NOT_FOUND) == index_hash
    )
    routes_md = ", ".join(f"`#/{r}`" for r in routes) if routes else "_none detected_"
    cats_md = ", ".join(f"`{c}`" for c in cats) if cats else "_none detected_"
    regions_md = "\n".join(f"- {r}" for r in regions[:12])
    if len(regions) > 12:
        regions_md += f"\n- _…and {len(regions) - 12} more regions_"

    return f"""{BEGIN}
<!-- Do not edit this block by hand; run scripts/sync-agent-context.py -->

### Repository snapshot

| Field | Value |
|-------|-------|
| `index.html` lines | {lines:,} |
| `index.html` size | {size_kb:.0f} KiB |
| `index.html` fingerprint | `{index_hash}` |
| Catalogue products (`p(` entries) | {products} |
| Product categories | {len(cats)} |
| Inlined WebP assets | {webp_count} |
| `404.html` matches `index.html` | {"yes" if not_found_match else "**no — sync required**"} |

### Hash routes (client-side)

{routes_md}

### Category ids

{cats_md}

### Major `index.html` regions

{regions_md}

{END}"""


def replace_auto_block(content: str, new_block: str) -> str:
    if BEGIN not in content or END not in content:
        raise SystemExit(
            f"{AGENTS_MD} is missing {BEGIN} … {END} markers. "
            "Restore the template from git history or AGENTS.md header."
        )
    pattern = re.compile(
        re.escape(BEGIN) + r".*?" + re.escape(END),
        re.DOTALL,
    )
    return pattern.sub(new_block, content, count=1)


def main() -> int:
    if not AGENTS_MD.exists():
        print(f"Missing {AGENTS_MD}", file=sys.stderr)
        return 1
    if not INDEX.exists():
        print(f"Missing {INDEX}", file=sys.stderr)
        return 1

    new_block = build_auto_block()
    old = AGENTS_MD.read_text(encoding="utf-8")
    new = replace_auto_block(old, new_block)

    if new == old:
        print("AGENTS.md auto section is already up to date.")
        return 0

    AGENTS_MD.write_text(new, encoding="utf-8")
    print(f"Updated {AGENTS_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

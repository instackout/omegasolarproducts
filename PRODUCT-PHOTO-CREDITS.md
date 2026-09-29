# Product imagery

| Layer | What it is |
|-------|------------|
| **Product image** (default) | In-situ WebGL still — part on a site-style ground plane, outdoor lighting |
| **3D Render** | Studio geometry views (`hero`, `front`, `side`, `top`, `exploded`) from measured models |

Regenerate installed-view stills:

```bash
# Serve the site from repo root, then:
python3 scripts/capture-context-photos.py
python3 scripts/inject-product-photos.py
cp index.html 404.html
python3 scripts/sync-agent-context.py
```

Requires `pip install playwright` and `playwright install chromium`.

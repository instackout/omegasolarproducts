# Product imagery

| Layer | What it is |
|-------|------------|
| **Product image** (default) | CC-licensed reference photographs from Wikimedia Commons (`scripts/product-photo-sources.json`) |
| **3D Render** | Optional studio geometry views (`hero`, `front`, `side`, `top`, `exploded`) from measured models |

Regenerate reference photos:

```bash
pip install Pillow
python3 scripts/build-product-photos.py
python3 scripts/inject-product-photos.py
python3 scripts/sync-agent-context.py
```

Attribution for Commons files is recorded in `scripts/product-photo-sources.json` (file title per model).

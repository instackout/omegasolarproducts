# Product imagery

| Layer | What it is |
|-------|------------|
| **Product image** (default) | Photographs matched to each product: Wikimedia Commons files where they depict that part, and studio shots in `scripts/reference-photos/` where no accurate public photo exists (`scripts/product-photo-sources.json`) |
| **3D Render** | Optional studio geometry views (`hero`, `front`, `side`, `top`, `exploded`) from measured models |

Regenerate reference photos:

```bash
pip install Pillow
python3 scripts/build-product-photos.py
python3 scripts/inject-product-photos.py
python3 scripts/sync-agent-context.py
```

Attribution for Commons files is recorded in `scripts/product-photo-sources.json` (file title per model).

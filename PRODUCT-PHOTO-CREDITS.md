# Product reference photographs

Default **Product image** views on the catalogue use compressed WebP derivatives of openly licensed photographs from [Wikimedia Commons](https://commons.wikimedia.org/). They are illustrative references for the product category, not Omega Instruments pack shots.

Source file titles are listed in `scripts/product-photo-sources.json`. Rebuild with:

```bash
python3 scripts/build-product-photos.py
python3 scripts/inject-product-photos.py
python3 scripts/sync-agent-context.py
```

Studio geometry renders (`hero`, `front`, `side`, `top`, `exploded`) remain available under **3D render** on each product page.

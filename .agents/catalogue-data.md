# Catalogue data layer

All product and navigation data for the UI lives in the **`OMEGA` IIFE** inside
`index.html` (search for `Omega Instruments — catalogue data layer`).

## `COMPANY`

Contact block: phones, email, address, hours, `phoneRaw` for WhatsApp (`wa.me`).

## `CATS`

Array of category objects:

- `id` — used in URLs (`#/products/mounting`) and product `cat` field
- `name`, `short`, `blurb` — UI copy
- `model` — default 3D part key for category tiles (not always unique per product)

Current category ids are listed in the auto-generated table in [AGENTS.md](../AGENTS.md).

## `PRODUCTS` and `p()`

```javascript
/* p(id, name, cat, model, opts) */
function p(id, name, cat, model, o) { ... }
```

| Field | Meaning |
|-------|---------|
| `id` | Slug for `#/product/<id>` |
| `name` | Display title |
| `cat` | One of `CATS[].id` |
| `model` | Key into `OPARTS.parts` and `OPHOTOS` |
| `opts.part` | SKU / part number (default derived from id) |
| `opts.blurb`, `sizes`, `specs`, `moq`, `lead`, `tags`, `featured`, `brand` | Detail page + filters |

**Adding a product**

1. Implement or reuse a 3D builder on `OPARTS.parts` if the product needs 3D.
2. Add WebP shots to `OPHOTOS` keyed by `model` (inlined base64).
3. Append `p('new-id', ...)` in the appropriate comment section of `PRODUCTS`.
4. Confirm filters/tags if used.
5. Copy `index.html` → `404.html`.

**Removing a product** — delete the `p(...)` line; remove orphaned `OPHOTOS` / part builders only if nothing else references the `model` key.

## `STATS`

Homepage counter strip — `{ n, suffix, label }` objects; animated on home route.

## Imagery (`OPHOTOS`)

Large block of inlined WebP. Images are tied to `model` + optional `view` (`hero`, `exploded`, etc.).
Keep new images WebP and reasonably compressed; the file is already ~1.3 MB.

## Exploded views

`OPARTS.explodable` lists `model` keys that support exploded assembly in the product inspector.

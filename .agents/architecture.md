# Architecture — `index.html` monolith

The site is intentionally **one deployable file** plus static assets. Agents should
preserve that constraint unless the user asks to modularize.

## Execution order (bottom of file → top loads first)

Scripts run as sequential IIFEs on `window`:

| Global | Responsibility |
|--------|----------------|
| `OGL` | WebGL math, geometry builders, `Viewer` (orbit, resize, `IntersectionObserver` pause) |
| `OPARTS` | `hero` scene builder, `parts` map of model functions, `MAT` swatches, `explodable` set |
| `OMEGA` | `COMPANY`, `CATS`, `PRODUCTS`, `STATS` |
| `OPHOTOS` | Array of `{ model, view, caption, src }` with inlined WebP `data:` URLs |
| App shell IIFE | DOM templates, hash `route()`, filters, RFQ, lightbox, comparison tray |

## Routing

`location.hash` drives rendering into `#app`:

- `#/` — home (hero WebGL array)
- `#/about` — about + secondary 3D figures
- `#/products` and `#/products/<catId>` — catalogue list + filters
- `#/product/<productId>` — detail, gallery, optional 3D + exploded view
- `#/quote` — RFQ table (`localStorage` key `omega.rfq`)
- `#/catalog` — brochure view
- `#/contact` — contact

`hashchange` re-runs `route()`. Each navigation calls `killScene()` / `OGL.disposeAll()` to avoid WebGL leaks.

## 3D mounting pattern

- `mount(canvas, buildFn, opts)` — hero / custom builds
- `mountPart(canvas, modelKey, opts)` — dispatches `OPARTS.parts[modelKey]`
- View presets in `VIEWS` (iso, front, side, back, top)
- `prefers-reduced-motion` short-circuits animation duration in the viewer

## Styling

- CSS variables for light/dark (`prefers-color-scheme` + optional `data-theme`)
- Fixed brand colours on navy sections; semantic tokens elsewhere
- Responsive breakpoints in a dedicated `@media` block near file end

## What not to do

- Do not extract `PRODUCTS` to JSON fetched over the network without an explicit migration plan (offline-first catalogue is a feature).
- Do not add frameworks (React, Vue) without explicit request.
- Do not change hash route names without updating inbound links and mental model in docs.

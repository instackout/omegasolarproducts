# Editing guide for agents

## Default workflow

1. Edit `index.html` (only file needed for most tasks).
2. `cp index.html 404.html` when the app shell or routes changed.
3. `python3 scripts/sync-agent-context.py` (or rely on git pre-commit hook).
4. Open the site locally: `python3 -m http.server 8080` and visit `http://127.0.0.1:8080/#/`.

No local server is required for CI; optional for manual QA.

## Safe changes

- Copy, specs, MOQ, tags, new `p()` rows in existing categories
- CSS token tweaks inside `:root` blocks
- New hash routes only if you wire `route()`, `pageTitle()`, and nav links together
- `robots.txt` / `sitemap.xml` for SEO (keep URLs on `https://omegasolarproducts.com`)

## High-risk changes

| Area | Risk |
|------|------|
| `CNAME` | Breaks custom domain on Pages |
| Deleting `.nojekyll` | Jekyll may break asset paths |
| Renaming product `id` | Breaks bookmarks and external links |
| Splitting `index.html` | Breaks “zero build” deploy model |
| Huge new binary assets | Bloats git and first paint — prefer WebP and reuse 3D where possible |

## HTML generation

The app builds strings and assigns `app.innerHTML`. Always route dynamic text through `esc()` unless the value is known-safe markup you authored yourself.

## WebGL

When editing viewers:

- Call existing `killScene()` on route changes (already in `route()`).
- Respect `prefers-reduced-motion` patterns already in `Viewer`.
- Test product pages that mount 3D on mobile widths if you touch layout around canvases.

## Agent context files

- **Human-written:** sections above the auto block in `AGENTS.md` and all of `.agents/*.md`.
- **Machine-written:** block between `AGENT_CONTEXT:BEGIN auto` and `END` in `AGENTS.md`.
- If you change what the sync script parses, update `scripts/sync-agent-context.py` and mention it in the commit.

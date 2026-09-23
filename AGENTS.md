---
description: >-
  How coding agents should work on the Omega Instruments static site
  (omegasolarproducts.com) — single-file HTML catalogue, WebGL, GitHub Pages.
tags:
  - static-site
  - github-pages
  - webgl
  - product-catalogue
compatibility: cursor, claude-code, github-copilot, codex, gemini-cli
read_only:
  - CNAME
  - .nojekyll
---

# Agent instructions — Omega Instruments

Canonical agent context for this repository. Humans start at [README.md](README.md);
agents start here. Deeper topic guides live under [.agents/](.agents/).

## Precedence

1. **Explicit user chat instructions** override everything below.
2. **Nearest `AGENTS.md`** wins for path-scoped work (this repo has only the root file).
3. **This file** plus linked `.agents/*` modules.
4. [README.md](README.md) and [DEPLOY.md](DEPLOY.md) for human-oriented narrative.

Tools that support both `CLAUDE.md` and `AGENTS.md` (e.g. Claude Code): this repo
uses **`AGENTS.md` as the single source of truth**; [CLAUDE.md](CLAUDE.md) only points here.

## Project overview

| Aspect | Detail |
|--------|--------|
| **Product** | Marketing + product catalogue for Omega Instruments (solar BOS hardware, Ahmedabad) |
| **Live site** | https://omegasolarproducts.com |
| **Hosting** | GitHub Pages from `main`, root deploy |
| **Stack** | One self-contained `index.html` (~4.4k lines): HTML, CSS, vanilla JS, inline WebGL |
| **Build** | None — no Node, npm, bundler, or CI compile step |
| **Publish** | Commit + push to `main`; Pages updates in ~1 minute |

The entire application ships in **`index.html`**. Supporting files are static assets
(favicons, `og-image.png`, `robots.txt`, `sitemap.xml`, `site.webmanifest`) and
**`CNAME`** (custom domain — do not delete).

## Repository map

| Path | Role |
|------|------|
| `index.html` | Site, styles, WebGL engine, 3D part library, catalogue data, router, UI |
| `404.html` | **Must stay identical to `index.html`** so bad URLs still load the app |
| `CNAME` | Custom domain for GitHub Pages (**read-only** for agents) |
| `.nojekyll` | Disables Jekyll on Pages (**read-only**) |
| `DEPLOY.md` | First-time GitHub Pages + GoDaddy DNS (humans) |
| `scripts/sync-agent-context.py` | Regenerates the auto section below in this file |
| `.agents/*.md` | Progressive-disclosure guides (architecture, data, editing, deploy) |

## Commands

```bash
# Refresh machine-generated metrics in this file (also runs on pre-commit when hooks installed)
python3 scripts/sync-agent-context.py

# Install git hooks so AGENTS.md updates when you commit site changes
bash scripts/install-git-hooks.sh

# Verify 404.html matches the main app (run after editing index.html)
cmp -s index.html 404.html && echo "404 in sync" || echo "404 OUT OF SYNC — copy index.html to 404.html"
```

There is **no** `npm test`, `npm run build`, or linter in this repo unless you add one.

## How the site is built (mental model)

Read [.agents/architecture.md](.agents/architecture.md) for detail. Short version:

1. **CSS** — Design tokens in `:root`, components in `<style>` (Sora / Inter / IBM Plex Mono).
2. **`window.OGL`** — Minimal WebGL viewer (matrices, primitives, `Viewer` with orbit/spin).
3. **`window.OPARTS`** — Procedural 3D models (`parts`, `hero`, `explodable` flags).
4. **`window.OMEGA`** — `COMPANY`, `CATS`, `PRODUCTS`, `STATS` (catalogue source of truth).
5. **`window.OPHOTOS`** — Inlined WebP renders keyed by product `model` id.
6. **App shell** — Hash router (`#/`, `#/products`, `#/product/:id`, `#/quote`, …), RFQ in `localStorage`, WhatsApp deep links.

Routing is **hash-based** only; there is no server-side routing.

## Editing rules (important)

See [.agents/editing-guide.md](.agents/editing-guide.md).

- **Prefer editing `index.html` only** for product, copy, style, and behaviour changes.
- After substantive `index.html` edits, **copy to `404.html`** (`cp index.html 404.html`).
- Do **not** split into multiple JS files or add a build pipeline unless explicitly requested.
- Do **not** remove or rewrite `CNAME` / `.nojekyll`.
- Product records use helper `p(id, name, cat, model, opts)` — keep `id` URL-safe; `model` must match `OPARTS.parts` and `OPHOTOS` keys.
- Escape user-facing strings in JS via the existing `esc()` helper when building HTML.
- External runtime deps: Google Fonts only (already linked in `<head>`).

## Security & privacy

- Public marketing site — **no secrets** in the repo (no API keys, no customer PII).
- RFQ / “recently viewed” use **browser `localStorage` only**; never log real user data into the HTML.
- WhatsApp links use `COMPANY.phoneRaw` — do not change without business approval.

## Commits & pull requests

- Keep commits focused; mention whether catalogue, 3D, or deploy/docs changed.
- If hooks are installed, `AGENTS.md` auto-metrics update on commit when `index.html` / `404.html` / agent scripts change.
- CI (`.github/workflows/agent-context.yml`) fails if the auto section is stale — run `python3 scripts/sync-agent-context.py` before push.

## Further reading

| Doc | Contents |
|-----|----------|
| [.agents/architecture.md](.agents/architecture.md) | Module layout inside `index.html`, WebGL lifecycle |
| [.agents/catalogue-data.md](.agents/catalogue-data.md) | `p()`, categories, photos, 3D `model` ids |
| [.agents/editing-guide.md](.agents/editing-guide.md) | Safe change patterns, 404 sync, what not to touch |
| [.agents/deployment.md](.agents/deployment.md) | GitHub Pages + DNS (summary; full steps in DEPLOY.md) |

<!-- AGENT_CONTEXT:BEGIN auto -->
<!-- Do not edit this block by hand; run scripts/sync-agent-context.py -->

### Repository snapshot

| Field | Value |
|-------|-------|
| `index.html` lines | 4,462 |
| `index.html` size | 1292 KiB |
| `index.html` fingerprint | `a7b16cd0f4be` |
| Catalogue products (`p(` entries) | 39 |
| Product categories | 9 |
| Inlined WebP assets | 152 |
| `404.html` matches `index.html` | yes |

### Hash routes (client-side)

`#/about`, `#/catalog`, `#/contact`, `#/product`, `#/products`, `#/quote`

### Category ids

`panels`, `inverters`, `batteries`, `mounting`, `earthing`, `cables`, `enclosures`, `fasteners`, `bos`

### Major `index.html` regions

- design tokens & components
- miniature WebGL engine
- procedural 3D part library
- catalogue data layer
- product imagery
- application shell

<!-- AGENT_CONTEXT:END auto -->

# Deployment (agent summary)

Full human walkthrough: [DEPLOY.md](../DEPLOY.md).

## Runtime

- **Host:** GitHub Pages
- **Branch:** `main`
- **Publish root:** `/` (not `/docs`)
- **Custom domain:** `omegasolarproducts.com` via `CNAME` file in repo root
- **HTTPS:** Enforced in GitHub Pages settings after DNS validates

## Agent constraints

- Never commit private customer data, credentials, or `.env` files (none expected).
- Do not change DNS or GitHub Pages settings via code — only document for humans.
- Asset paths use absolute paths from site root (`/favicon.ico`, etc.) suitable for custom domain.

## After deploy

Changes appear within about a minute of push to `main`. No cache purge step except for social previews (WhatsApp may need `?1` query trick — see DEPLOY.md).

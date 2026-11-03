# AI Frontier website

A responsive, searchable, static GitHub Pages frontend for the OpenShelf knowledge base.

## Build locally

```bash
python -m pip install 'Markdown>=3.6,<4' 'PyYAML>=6,<7'
python scripts/build_site.py
python -m http.server 8000 --directory docs
```

Visit http://localhost:8000. The build generates `docs/data.json` from the Markdown files under `wiki/`. Search, filtering, graph navigation, article reading, and theme switching work entirely in the browser without a backend.

## Deploy

GitHub Actions workflow `.github/workflows/pages.yml` builds and deploys the `docs/` directory on every change to the wiki or site. In GitHub repository **Settings → Pages**, select **GitHub Actions** as the source if it is not already configured. The site URL is expected to be `https://hexsecs.github.io/ai-frontier/` after a successful deployment.

## Notes

The network graph displays candidate relationships inferred from project summaries; it is not a verified citation network. Category totals are computed from the actual indexed Markdown files, not hard-coded mockup counts.

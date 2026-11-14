# AI Frontier website

A responsive, searchable, static GitHub Pages frontend for the OpenShelf knowledge base.

## Build locally

```bash
python -m pip install 'Markdown>=3.6,<4' 'PyYAML>=6,<7' 'bleach>=6,<7'
python scripts/build_site.py
python -m http.server 8000 --directory docs
```

Visit http://localhost:8000. The build generates `docs/data.json` from the Markdown files under `wiki/`. Search, filtering, graph navigation, article reading, and theme switching work entirely in the browser without a backend.

## Deploy

GitHub Actions workflow `.github/workflows/pages.yml` builds and deploys the `docs/` directory on every change to the wiki or site. In GitHub repository **Settings → Pages**, select **GitHub Actions** as the source if it is not already configured. The site URL is expected to be `https://hexsecs.github.io/ai-frontier/` after a successful deployment.

## Notes

The home page begins with five question-led reading paths from `wiki/topics/`. These use the existing OpenShelf `index` type. Categories use each record's declared type, so a benchmark can retain its canonical `projects/...` path.

The builder derives `outgoing` and `backlinks` from rendered internal article links and exposes validated `related:` navigation. Backlinks preserve reference direction; they do not infer reciprocal scientific relationships. The graph draws a bounded set of these explicit article links, with no invented fallback edges. Unlabelled wiki links use the target page title when available. Generated `docs/data.json` is not committed.

Run `python scripts/editorial_report.py --json` for advisory suggestions about reading-path membership, unlinked canonical mentions and shared sources. Shared citations do not establish duplicate entities. CI publishes the report as an artifact; suggestions do not fail validation or impose link quotas. `scripts/check_links.py` separately enforces valid internal targets, resolvable related navigation and root reachability.

# Interactive figures in AI Frontier briefings

The Markdown files in `wiki/` remain the source of truth. The Pages build converts fenced `chart`, `vega-lite`, `mermaid`, and `graph` blocks into interactive figures. Ordinary Markdown images remain supported.

## Simple chart

```chart
{
  "type": "bar",
  "title": "Multi-agent task accuracy",
  "caption": "Illustrative values from the November 2 briefing; verify primary-source methodology.",
  "labels": ["Native execution", "Dittany"],
  "datasets": [{"label": "Task accuracy (%)", "data": [58.01, 84.76]}],
  "yAxis": {"min": 0, "max": 100, "title": "Accuracy (%)"}
}
```

Supported simple chart types: `bar`, `line`, `scatter`, `pie`, `doughnut`, and `radar`. Simple chart specs are translated to Vega-Lite. For more complex interactive plots, use `vega-lite` directly:

```vega-lite
{
  "title": "Token usage by strategy",
  "mark": "bar",
  "data": {"values": [{"strategy":"Baseline","tokens":100},{"strategy":"Optimized","tokens":62}]},
  "encoding": {
    "x": {"field":"strategy","type":"nominal"},
    "y": {"field":"tokens","type":"quantitative"},
    "tooltip": [{"field":"strategy"},{"field":"tokens"}]
  }
}
```

## Mermaid architecture

```mermaid
flowchart LR
  A[Agent output] --> B{Validated?}
  B -->|Yes| C[Preserve contribution]
  B -->|No| D[Repair failed step]
  D --> B
```

## Interactive graph

```graph
{
  "title": "Agent system dependencies",
  "caption": "Click a node to open its referenced source.",
  "nodes": [
    {"id":"planner","label":"Planner","url":"https://github.com/hexsecs/ai-frontier"},
    {"id":"executor","label":"Executor"},
    {"id":"validator","label":"Validator"}
  ],
  "edges": [
    {"source":"planner","target":"executor"},
    {"source":"executor","target":"validator"}
  ]
}
```

## Authoring and security notes

- Every visualization must have real, sourced data. Never fabricate benchmark measurements to fill a figure.
- Include descriptive labels, units, a meaningful caption, and source links in surrounding Markdown.
- Keep specs below 100 KB; use repository-hosted images for screenshots or photographs.
- Do not embed JavaScript, raw HTML scripts, arbitrary Vega expressions, or remote data sources in a briefing.
- The website loads Vega-Lite, Mermaid, and Cytoscape from versioned public CDNs. An internet connection is required for interactive figures; Markdown source remains readable without them.
- Interactive charts are rendered on the GitHub Pages site, not directly in GitHub's native Markdown viewer (which displays their fenced definitions).

## OpenShelf token-budget override

OpenShelf recommends a 2,500-token L2 page budget. Longer research briefings may deliberately exceed this advisory limit. Add a justification to the Markdown page:

```markdown
<!-- openshelf:budget-override reason="Full research context and sourced technical evidence belong in this dated briefing." -->
```

The validation workflow acknowledges the L2 budget warning for that page and prints the justification. **All actual OpenShelf errors remain fatal**, including metadata, links, and schema errors. The override does not modify OpenShelf's own validator or exempt a page from linting. Keep the explanation specific and avoid using overrides for unnecessary repetition.

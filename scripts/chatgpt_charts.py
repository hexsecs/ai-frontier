"""Convert ChatGPT Chart JSON into portable, self-contained Vega-Lite figures."""
import json
import re

SUPPORTED = {"bar": "bar", "line": "line", "scatter": "point"}

def to_vega(chart):
    kind = chart.get("chartType")
    if kind not in SUPPORTED:
        raise ValueError(f"Unsupported ChatGPT chartType: {kind!r}")
    xkey = chart.get("xKey")
    series = chart.get("series")
    data = chart.get("data")
    if not isinstance(xkey, str) or not isinstance(series, list) or not series or not isinstance(data, list):
        raise ValueError("ChatGPT chart requires xKey, nonempty series, and data")
    rows = []
    for row in data:
        if not isinstance(row, dict) or xkey not in row:
            raise ValueError("Chart row missing xKey")
        for item in series:
            key = item.get("dataKey")
            value = row.get(key)
            if not isinstance(key, str):
                raise ValueError("Series missing dataKey")
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                rows.append({"category": row[xkey], "series": item.get("label") or key, "value": value})
    if not rows:
        raise ValueError("Chart has no numeric data")
    x_type = "quantitative" if kind == "scatter" and all(isinstance(r["category"], (int, float)) for r in rows) else "nominal"
    spec = {
        "title": chart.get("title") or "",
        "data": {"values": rows},
        "mark": {"type": SUPPORTED[kind], "tooltip": True},
        "encoding": {
            "x": {"field": "category", "type": x_type, "title": chart.get("xAxisLabel") or xkey},
            "y": {"field": "value", "type": "quantitative", "title": chart.get("yAxisLabel") or series[0].get("label") or "Value"},
            "color": {"field": "series", "type": "nominal"},
            "tooltip": [{"field": "category"}, {"field": "series"}, {"field": "value"}],
        },
    }
    if isinstance(chart.get("yAxisMin"), (int, float)):
        spec["encoding"]["y"]["scale"] = {"domainMin": chart["yAxisMin"]}
    if isinstance(chart.get("yAxisMax"), (int, float)):
        spec["encoding"]["y"].setdefault("scale", {})["domainMax"] = chart["yAxisMax"]
    return spec

def convert(text):
    def fenced(m):
        chart = json.loads(m.group(1))
        return "```vega-lite\n" + json.dumps(to_vega(chart), ensure_ascii=False) + "\n```"
    text = re.sub(r"(?m)^\s{0,3}```chatgpt-chart\s*\n(.*?)^\s{0,3}```\s*$", fenced, text, flags=re.S | re.M)
    def inline(m):
        return fenced(type("Match", (), {"group": lambda self, i: m.group(1)})())
    text = re.sub(r"<Chart\s+content=\{(\{[^<>]*?\})\}\s*/>", inline, text)
    return text

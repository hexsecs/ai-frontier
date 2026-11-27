"""Durable per-date checkpoints. Local state must be persisted by the runner."""
import argparse
import datetime as dt
import json
import os
from pathlib import Path
from zoneinfo import ZoneInfo

STAGES = ("research", "briefing", "ingestion", "pr", "validation", "review", "merge", "pages")
FIELDS = {
    "research": ("sources",), "briefing": ("artifact",),
    "ingestion": ("commit",), "pr": ("url", "head"),
    "validation": ("head", "checks"), "review": ("head", "receipt"),
    "merge": ("head", "commit"), "pages": ("deployment", "commit"),
}

def advance(state, stage, evidence):
    if stage not in STAGES or not isinstance(evidence, dict):
        raise ValueError("invalid stage or evidence")
    index = STAGES.index(stage)
    if any(s not in state for s in STAGES[:index]):
        raise ValueError("missing predecessor")
    if any(not evidence.get(k) for k in FIELDS[stage]):
        raise ValueError("missing evidence")
    if stage in ("validation", "review", "merge") and evidence["head"] != state["pr"]["head"]:
        raise ValueError("stale head")
    if stage == "pages" and evidence["commit"] != state["merge"]["commit"]:
        raise ValueError("wrong deployment commit")
    if stage == "validation" and (not isinstance(evidence["checks"], dict) or any(v != "success" for v in evidence["checks"].values())):
        raise ValueError("checks not successful")
    return {**{s: state[s] for s in STAGES[:index]}, stage: evidence}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, default=Path("automation/checkpoints"))
    p.add_argument("--date", default=dt.datetime.now(ZoneInfo("America/Detroit")).date().isoformat())
    p.add_argument("--stage", choices=STAGES)
    p.add_argument("--evidence", type=Path)
    args = p.parse_args()
    date = dt.date.fromisoformat(args.date).isoformat()
    path = args.root / (date + ".json")
    state = json.loads(path.read_text()) if path.exists() else {}
    if args.stage:
        if not args.evidence:
            p.error("--evidence required")
        state = advance(state, args.stage, json.loads(args.evidence.read_text()))
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps(state, indent=2) + "\n")
        os.replace(tmp, path)
    print(json.dumps({"date": date, "next": next((s for s in STAGES if s not in state), None), "state": state}, indent=2))

if __name__ == "__main__":
    main()

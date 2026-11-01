"""Show or update project step status. Keeps STEPS.yaml and PROGRESS.md in sync.

  python scripts/steps.py                      # show
  python scripts/steps.py --start 2            # mark step 2 in_progress
  python scripts/steps.py --done 1 --note "classes: person, box, bottle"
"""
import argparse
import datetime as dt
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
STEPS = ROOT / "STEPS.yaml"
PROGRESS = ROOT / "PROGRESS.md"
MARK = {"done": "[x]", "in_progress": "[~]", "todo": "[ ]"}


def render(data: dict) -> str:
    lines = []
    for s in data["steps"]:
        extra = f" - {s['note']}" if s.get("note") else ""
        lines.append(f"{MARK[s['status']]} {s['id']:>2}. {s['title']} ({s['where']}){extra}")
    return "\n".join(lines)


def current(data: dict) -> str:
    for s in data["steps"]:
        if s["status"] == "in_progress":
            return f"Step {s['id']}: {s['title']}"
    nxt = next((s for s in data["steps"] if s["status"] == "todo"), None)
    return f"Next up: step {nxt['id']}: {nxt['title']}" if nxt else "All steps done"


def sync_progress(data: dict, log_line: str | None) -> None:
    if not PROGRESS.is_file():
        return
    text = PROGRESS.read_text()
    block = f"<!-- STATUS:START -->\n**Current:** {current(data)}\n\n```\n{render(data)}\n```\n<!-- STATUS:END -->"
    text = re.sub(r"<!-- STATUS:START -->.*?<!-- STATUS:END -->", lambda m: block, text, flags=re.S)
    if log_line:
        text = text.rstrip() + f"\n- {log_line}\n"
    PROGRESS.write_text(text)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--start", type=int)
    ap.add_argument("--done", type=int)
    ap.add_argument("--note", default=None)
    args = ap.parse_args()

    data = yaml.safe_load(STEPS.read_text())
    by_id = {s["id"]: s for s in data["steps"]}
    log_line = None
    for sid, status in ((args.start, "in_progress"), (args.done, "done")):
        if sid is None:
            continue
        if sid not in by_id:
            print(f"No such step: {sid}", file=sys.stderr)
            return 1
        by_id[sid]["status"] = status
        if args.note:
            by_id[sid]["note"] = args.note
        log_line = f"{dt.date.today()}: step {sid} -> {status}" + (f" ({args.note})" if args.note else "")
    if log_line:
        STEPS.write_text(yaml.safe_dump(data, sort_keys=False, width=200))
        sync_progress(data, log_line)
    print(current(data), "\n")
    print(render(data))
    return 0


if __name__ == "__main__":
    sys.exit(main())

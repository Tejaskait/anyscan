"""Sort a Label Studio YOLO export back into data/labels_reviewed/<session>/."""
import argparse, shutil
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--export", type=Path, required=True)
ap.add_argument("--frames", type=Path, default=Path("data/frames"))
ap.add_argument("--out", type=Path, default=Path("data/labels_reviewed"))
ap.add_argument("--config", type=Path, default=Path("configs/classes.yaml"))
args = ap.parse_args()

import yaml
want = [c["name"] for c in yaml.safe_load(open(args.config))["classes"]]

# class id remap, in case the export numbers classes differently
remap = {}
cf = args.export / "classes.txt"
if cf.is_file():
    got = [l.strip() for l in cf.read_text().splitlines() if l.strip()]
    remap = {i: want.index(n) for i, n in enumerate(got) if n in want}
    print("Export classes:", got, "->", want)

session_of = {p.stem: p.parent.name for p in args.frames.rglob("*.jpg")}
stems = sorted(session_of, key=len, reverse=True)

done = skipped = 0
for txt in (args.export / "labels").glob("*.txt"):
    stem = next((s for s in stems if txt.stem == s or txt.stem.endswith(s)), None)
    if stem is None:
        print("No matching frame for", txt.name); skipped += 1; continue
    lines = []
    for line in txt.read_text().splitlines():
        parts = line.split()
        if len(parts) == 5:
            cid = int(parts[0])
            if remap and cid not in remap:
                continue
            parts[0] = str(remap.get(cid, cid))
            lines.append(" ".join(parts))
    dst = args.out / session_of[stem]
    dst.mkdir(parents=True, exist_ok=True)
    (dst / f"{stem}.txt").write_text("\n".join(lines) + ("\n" if lines else ""))
    done += 1
print(f"Sorted {done} label files into {args.out}, skipped {skipped}")
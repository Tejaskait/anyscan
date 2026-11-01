"""WORKFLOW TEST ONLY: within each session, first (1-val_frac) frames -> train, last val_frac -> val.

Use this only when you have too few sessions for a real split-by-session. The val set comes
from the same scenes as train, so the metrics are NOT reportable. Replace with make_split.py
(by session) once you have 10+ sessions.
"""
import argparse
import shutil
from pathlib import Path

import yaml

ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument("--frames", type=Path, default=Path("data/frames"))
ap.add_argument("--labels", type=Path, default=Path("data/labels_reviewed"))
ap.add_argument("--out", type=Path, default=Path("data/dataset"))
ap.add_argument("--config", type=Path, default=Path("configs/classes.yaml"))
ap.add_argument("--val-frac", type=float, default=0.2)
args = ap.parse_args()

if args.out.exists():
    shutil.rmtree(args.out)
counts = {"train": 0, "val": 0}
for sess in sorted(p for p in args.frames.iterdir() if p.is_dir()):
    imgs = sorted(sess.glob("*.jpg"))
    cut = max(1, int(len(imgs) * (1 - args.val_frac)))
    for i, img in enumerate(imgs):
        split = "train" if i < cut else "val"
        di, dl = args.out / "images" / split, args.out / "labels" / split
        di.mkdir(parents=True, exist_ok=True)
        dl.mkdir(parents=True, exist_ok=True)
        shutil.copy2(img, di / img.name)
        lbl = args.labels / sess.name / (img.stem + ".txt")
        (dl / (img.stem + ".txt")).write_text(lbl.read_text() if lbl.is_file() else "")
        counts[split] += 1

names = [c["name"] for c in yaml.safe_load(args.config.read_text())["classes"]]
data = {"path": str(args.out.resolve()), "train": "images/train", "val": "images/val",
        "names": {i: n for i, n in enumerate(names)}}
(args.out / "data.yaml").write_text(yaml.safe_dump(data, sort_keys=False))
print("images:", counts, "-> WORKFLOW TEST ONLY, metrics not reportable")
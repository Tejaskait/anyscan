"""Build a YOLO dataset split BY SESSION (folder name), never by random frame."""
import argparse
import logging
import random
import shutil
import sys
from pathlib import Path

import yaml

log = logging.getLogger("make_split")
IMG_EXT = {".jpg", ".jpeg", ".png"}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--frames", type=Path, required=True)
    ap.add_argument("--labels", type=Path, required=True, help="reviewed labels: <session>/<image>.txt")
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--config", type=Path, default=Path("configs/classes.yaml"))
    ap.add_argument("--val-sessions", nargs="*", default=None, help="explicit sessions for validation")
    ap.add_argument("--val-frac", type=float, default=0.2, help="used if --val-sessions not given")
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    if not args.frames.is_dir():
        log.error("Frames folder not found: %s", args.frames)
        return 1
    sessions = sorted(p.name for p in args.frames.iterdir() if p.is_dir())
    if len(sessions) < 2:
        log.error("Need at least 2 sessions to split by session; found %d", len(sessions))
        return 1
    if args.val_sessions:
        missing = set(args.val_sessions) - set(sessions)
        if missing:
            log.error("Unknown sessions: %s", sorted(missing))
            return 1
        val = set(args.val_sessions)
    else:
        rng = random.Random(args.seed)
        k = max(1, round(len(sessions) * args.val_frac))
        val = set(rng.sample(sessions, k))
    train = set(sessions) - val
    if not train:
        log.error("No training sessions left")
        return 1
    log.info("train sessions: %s", sorted(train))
    log.info("val sessions:   %s", sorted(val))

    counts = {"train": 0, "val": 0}
    unlabeled = 0
    for s in sessions:
        split = "val" if s in val else "train"
        di = args.out / "images" / split
        dl = args.out / "labels" / split
        di.mkdir(parents=True, exist_ok=True)
        dl.mkdir(parents=True, exist_ok=True)
        for img in sorted((args.frames / s).iterdir()):
            if img.suffix.lower() not in IMG_EXT:
                continue
            lbl = args.labels / s / (img.stem + ".txt")
            shutil.copy2(img, di / img.name)
            if lbl.is_file():
                shutil.copy2(lbl, dl / lbl.name)
            else:
                (dl / (img.stem + ".txt")).write_text("")  # treated as background
                unlabeled += 1
            counts[split] += 1

    names = [c["name"] for c in yaml.safe_load(args.config.read_text())["classes"]]
    data = {"path": str(args.out.resolve()), "train": "images/train", "val": "images/val",
            "names": {i: n for i, n in enumerate(names)}}
    (args.out / "data.yaml").write_text(yaml.safe_dump(data, sort_keys=False))
    log.info("images: %s | without label file (empty = background): %d", counts, unlabeled)
    log.info("Wrote %s (edit 'path' when moving to Colab)", args.out / "data.yaml")
    return 0


if __name__ == "__main__":
    sys.exit(main())

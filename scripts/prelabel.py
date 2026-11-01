"""Pre-label images with a pretrained 'teacher' model. Output is a DRAFT: always review it.

backends:
  world : YOLO-World, open-vocabulary (text prompts from configs/classes.yaml)
  coco  : standard pretrained YOLO (80 COCO classes, mapped via the 'coco' lists)
Use your own trained weights as --model with --backend coco-style mapping off by
passing --backend own (class ids are copied as-is) for round-2 pre-labeling.
"""
import argparse
import logging
import sys
from pathlib import Path

import yaml

log = logging.getLogger("prelabel")
IMG_EXT = {".jpg", ".jpeg", ".png"}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--frames", type=Path, required=True, help="folder with <session>/<image>.jpg")
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--config", type=Path, default=Path("configs/classes.yaml"))
    ap.add_argument("--backend", choices=["world", "coco", "own"], default="world")
    ap.add_argument("--model", default=None, help="default: yolov8s-worldv2.pt (world) / yolo11x.pt (coco)")
    ap.add_argument("--conf", type=float, default=0.15, help="low on purpose; you will review")
    ap.add_argument("--device", default="cpu")
    args = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    if not args.frames.is_dir():
        log.error("Frames folder not found: %s", args.frames)
        return 1
    if not args.config.is_file():
        log.error("Config not found: %s", args.config)
        return 1
    classes = yaml.safe_load(args.config.read_text())["classes"]

    if args.backend == "world":
        from ultralytics import YOLOWorld

        prompts, id_map = [], {}
        for cid, c in enumerate(classes):
            for p in c.get("prompts", []):
                id_map[len(prompts)] = cid
                prompts.append(p)
        if not prompts:
            log.error("No prompts in %s", args.config)
            return 1
        log.info("Prompts: %s", prompts)
        model = YOLOWorld(args.model or "yolov8s-worldv2.pt")
        model.set_classes(prompts)
    else:
        from ultralytics import YOLO

        model = YOLO(args.model or ("yolo11x.pt" if args.backend == "coco" else "best.pt"))
        if args.backend == "coco":
            name_to_cid = {n: cid for cid, c in enumerate(classes) for n in c.get("coco", [])}
            if not name_to_cid:
                log.error("No 'coco' names in %s", args.config)
                return 1
            id_map = {i: name_to_cid[n] for i, n in model.names.items() if n in name_to_cid}
            log.info("COCO mapping: %s", {model.names[i]: c for i, c in id_map.items()})
        else:
            id_map = {i: i for i in model.names}

    images = sorted(p for p in args.frames.rglob("*") if p.suffix.lower() in IMG_EXT)
    if not images:
        log.error("No images under %s", args.frames)
        return 1

    n_boxes = 0
    for i, img in enumerate(images, 1):
        res = model.predict(str(img), conf=args.conf, device=args.device, verbose=False)[0]
        lines = []
        for b in res.boxes:
            k = int(b.cls)
            if k not in id_map:
                continue
            x, y, w, h = b.xywhn[0].tolist()
            lines.append(f"{id_map[k]} {x:.6f} {y:.6f} {w:.6f} {h:.6f}")
        dest = args.out / img.relative_to(args.frames).with_suffix(".txt")
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text("\n".join(lines) + ("\n" if lines else ""))
        n_boxes += len(lines)
        if i % 50 == 0:
            log.info("%d/%d images", i, len(images))
    log.info("Done: %d images, %d draft boxes -> %s", len(images), n_boxes, args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())

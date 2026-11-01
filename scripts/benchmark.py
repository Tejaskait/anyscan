"""Compare latency/FPS of models (e.g. .pt vs .onnx) on CPU over a folder of images."""
import argparse
import logging
import sys
import time
from pathlib import Path

log = logging.getLogger("benchmark")
IMG_EXT = {".jpg", ".jpeg", ".png"}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--models", nargs="+", type=Path, required=True)
    ap.add_argument("--images", type=Path, required=True)
    ap.add_argument("--imgsz", type=int, default=640)
    ap.add_argument("--n", type=int, default=100, help="max images to time")
    ap.add_argument("--warmup", type=int, default=5)
    args = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    imgs = sorted(p for p in args.images.rglob("*") if p.suffix.lower() in IMG_EXT)[: args.n]
    if len(imgs) <= args.warmup:
        log.error("Need more than %d images in %s", args.warmup, args.images)
        return 1
    from ultralytics import YOLO

    print("| Model | imgs | mean latency (ms) | FPS |\n|---|---|---|---|")
    for m in args.models:
        if not m.is_file():
            log.error("Model not found: %s", m)
            return 1
        model = YOLO(str(m), task="detect")
        for p in imgs[: args.warmup]:
            model.predict(str(p), imgsz=args.imgsz, device="cpu", verbose=False)
        timed = imgs[args.warmup:]
        t0 = time.perf_counter()
        for p in timed:
            model.predict(str(p), imgsz=args.imgsz, device="cpu", verbose=False)
        dt = (time.perf_counter() - t0) / len(timed)
        print(f"| {m.name} | {len(timed)} | {dt * 1000:.1f} | {1 / dt:.1f} |")
    print("\nNote: includes image load + pre/post-processing, CPU only. Record hardware in docs/results.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

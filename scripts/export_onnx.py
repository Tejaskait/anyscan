"""Export trained weights to ONNX."""
import argparse
import logging
import sys
from pathlib import Path

log = logging.getLogger("export_onnx")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--weights", type=Path, required=True)
    ap.add_argument("--imgsz", type=int, default=640)
    ap.add_argument("--simplify", action="store_true")
    args = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    if not args.weights.is_file():
        log.error("Weights not found: %s", args.weights)
        return 1
    from ultralytics import YOLO

    path = YOLO(str(args.weights)).export(format="onnx", imgsz=args.imgsz, simplify=args.simplify)
    log.info("Exported: %s", path)
    return 0


if __name__ == "__main__":
    sys.exit(main())

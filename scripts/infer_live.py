"""Live detection from webcam index or stream URL (e.g. phone IP camera)."""
import argparse
import logging
import sys
import time
from pathlib import Path

import cv2

log = logging.getLogger("infer_live")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--model", type=Path, required=True)
    ap.add_argument("--source", default="0", help="camera index or stream/video URL")
    ap.add_argument("--conf", type=float, default=0.4)
    ap.add_argument("--imgsz", type=int, default=640)
    ap.add_argument("--save", type=Path, default=None, help="optional output .mp4")
    args = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    if not args.model.is_file():
        log.error("Model file not found: %s", args.model)
        return 1
    from ultralytics import YOLO

    try:
        model = YOLO(str(args.model), task="detect")
    except Exception as e:  # noqa: BLE001
        log.error("Failed to load model: %s", e)
        return 1

    src = int(args.source) if args.source.isdigit() else args.source
    cap = cv2.VideoCapture(src)
    if not cap.isOpened():
        log.error("Cannot open source: %s", args.source)
        return 1

    writer = None
    fps_s, last = 0.0, time.perf_counter()
    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                log.warning("No frame received; stopping")
                break
            res = model.predict(frame, conf=args.conf, imgsz=args.imgsz, device="cpu", verbose=False)[0]
            out = res.plot()
            now = time.perf_counter()
            inst = 1 / max(now - last, 1e-6)
            fps_s = inst if fps_s == 0 else 0.9 * fps_s + 0.1 * inst
            last = now
            cv2.putText(out, f"{fps_s:.1f} FPS", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            if args.save:
                if writer is None:
                    h, w = out.shape[:2]
                    writer = cv2.VideoWriter(str(args.save), cv2.VideoWriter_fourcc(*"mp4v"), 20, (w, h))
                writer.write(out)
            cv2.imshow("AnyScan", out)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        cap.release()
        if writer:
            writer.release()
        cv2.destroyAllWindows()
    return 0


if __name__ == "__main__":
    sys.exit(main())

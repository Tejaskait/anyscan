"""Extract frames from videos at a target FPS and drop near-duplicates (dHash)."""
import argparse
import logging
import sys
from pathlib import Path

import cv2
import numpy as np

log = logging.getLogger("extract_frames")
VIDEO_EXT = {".mp4", ".mov", ".avi", ".mkv", ".webm"}


def dhash(frame: np.ndarray, size: int = 8) -> np.ndarray:
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    small = cv2.resize(gray, (size + 1, size), interpolation=cv2.INTER_AREA)
    return (small[:, 1:] > small[:, :-1]).flatten()


def process_video(path: Path, out_dir: Path, target_fps: float, min_dist: int, quality: int) -> tuple[int, int]:
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        log.error("Cannot open video: %s", path)
        return 0, 0
    native = cap.get(cv2.CAP_PROP_FPS) or 30.0
    step = max(1, round(native / target_fps))
    session = path.stem
    dest = out_dir / session
    dest.mkdir(parents=True, exist_ok=True)

    idx = kept = seen = 0
    last_hash = None
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        if idx % step == 0:
            seen += 1
            h = dhash(frame)
            # keep if no dedup, first frame, or differs enough from the last kept frame
            if min_dist <= 0 or last_hash is None or int(np.count_nonzero(h != last_hash)) >= min_dist:
                cv2.imwrite(str(dest / f"{session}_{idx:06d}.jpg"), frame, [cv2.IMWRITE_JPEG_QUALITY, quality])
                last_hash = h
                kept += 1
        idx += 1
    cap.release()
    log.info("%s: sampled %d, kept %d", path.name, seen, kept)
    return seen, kept


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--videos", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--fps", type=float, default=2.0, help="frames sampled per second")
    ap.add_argument("--hash-threshold", type=int, default=4,
                    help="min Hamming distance (of 64 bits) to keep a frame; 0 disables dedup")
    ap.add_argument("--quality", type=int, default=95)
    args = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    if not args.videos.is_dir():
        log.error("Video folder not found: %s", args.videos)
        return 1
    videos = sorted(p for p in args.videos.iterdir() if p.suffix.lower() in VIDEO_EXT)
    if not videos:
        log.error("No videos found in %s", args.videos)
        return 1

    total_seen = total_kept = 0
    for v in videos:
        s, k = process_video(v, args.out, args.fps, args.hash_threshold, args.quality)
        total_seen += s
        total_kept += k
    log.info("Done: %d videos, %d sampled, %d kept", len(videos), total_seen, total_kept)
    return 0


if __name__ == "__main__":
    sys.exit(main())

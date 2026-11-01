import cv2, yaml
from pathlib import Path

names = [c["name"] for c in yaml.safe_load(open("configs/classes.yaml"))["classes"]]
out = Path("data/preview"); out.mkdir(parents=True, exist_ok=True)

for img in Path("data/frames").rglob("*.jpg"):
    lbl = Path("data/labels_reviewed") / img.parent.name / (img.stem + ".txt")
    im = cv2.imread(str(img)); h, w = im.shape[:2]
    if lbl.is_file():
        for line in lbl.read_text().splitlines():
            if not line.strip():
                continue
            c, x, y, bw, bh = line.split()
            c = int(c); x, y, bw, bh = map(float, (x, y, bw, bh))
            p1 = (int((x - bw / 2) * w), int((y - bh / 2) * h))
            p2 = (int((x + bw / 2) * w), int((y + bh / 2) * h))
            cv2.rectangle(im, p1, p2, (0, 255, 0), 2)
            cv2.putText(im, names[c], (p1[0], max(p1[1] - 5, 15)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.imwrite(str(out / f"{img.parent.name}_{img.name}"), im)
print("Done. Open data/preview/")
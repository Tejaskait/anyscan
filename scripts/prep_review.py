import shutil, yaml
from pathlib import Path

root = Path("data/review")
(root / "images").mkdir(parents=True, exist_ok=True)
(root / "labels").mkdir(parents=True, exist_ok=True)

names = [c["name"] for c in yaml.safe_load(open("configs/classes.yaml"))["classes"]]
(root / "classes.txt").write_text("\n".join(names) + "\n")

n = 0
for img in Path("data/frames").rglob("*.jpg"):
    shutil.copy2(img, root / "images" / img.name)
    lbl = Path("data/labels_auto") / img.parent.name / (img.stem + ".txt")
    (root / "labels" / (img.stem + ".txt")).write_text(lbl.read_text() if lbl.is_file() else "")
    n += 1
print(f"Prepared {n} images in {root}")
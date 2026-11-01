# AnyScan

Config-driven object detection pipeline: **record video -> frames -> pretrained-model pre-labels -> human review -> split by session -> train on Colab GPU -> live webcam test -> ONNX + CPU benchmark.**

Detect any objects: edit `configs/classes.yaml` (text prompts for YOLO-World, or COCO names for a standard YOLO teacher).
sses chosen"


## Steps (details in STEPS.yaml)
| # | Step | Where |
|---|---|---|
| 1 | Choose objects, edit `configs/classes.yaml` | laptop |
| 2 | Record 10-15 clips in different sessions -> `data/videos/session01_xxx.mp4` | phone/laptop |
| 3 | `python scripts/extract_frames.py --videos data/videos --out data/frames --fps 2` | laptop |
| 4 | `python scripts/prelabel.py --frames data/frames --out data/labels_auto --backend world` (or `--backend coco`) | laptop / Colab |
| 5 | Review in CVAT/Label Studio; export YOLO labels to `data/labels_reviewed/<session>/` | laptop |
| 6 | `python scripts/make_split.py --frames data/frames --labels data/labels_reviewed --out data/dataset --val-sessions session04 session09`, zip, upload to Drive | laptop |
| 7 | Train: `notebooks/colab_train.ipynb` on a T4 GPU -> `best.pt` | **Colab** |
| 8 | Evaluate on verified val; live test: `python scripts/infer_live.py --model best.pt --source 0` | laptop |
| 9 | `python scripts/export_onnx.py --weights best.pt` then `python scripts/benchmark.py --models best.pt best.onnx --images data/dataset/images/val` | laptop |
| 10 | Round 2: record failures, pre-label with `--backend own --model best.pt`, review, retrain, compare | both |
| 11 | README, `docs/results.md`, 30-60 s demo video | laptop |

## Setup
```bash
python -m venv .venv && source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install graphifyy && graphify . && graphify claude install   # code map for AI agents
```

## Handing off to an AI agent
Share the repo. The agent reads `AGENTS.md` -> `STEPS.yaml` -> `PROGRESS.md` -> `docs/context/` -> `graphify-out/GRAPH_REPORT.md`.
After each session: update steps, then rerun `graphify .`.

## Rules that protect the results
Split by session, not frame. Never augment val. Evaluate on human-verified labels. Report only measured numbers.

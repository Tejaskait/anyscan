# PROGRESS

<!-- STATUS:START -->
**Current:** Step 2: Record 10-15 clips in different sessions

```
[x]  0. Plan project and create scaffold (chat) - scaffold + context docs created 2026-10-31
[x]  1. Choose objects; edit configs/classes.yaml (laptop) - classes chosen
[~]  2. Record 10-15 clips in different sessions (phone/laptop) - name: session01_bright_desk.mp4 -> data/videos/
[ ]  3. Extract frames + de-duplicate (laptop) - scripts/extract_frames.py
[ ]  4. Pre-label with pretrained teacher model (laptop CPU or Colab) - scripts/prelabel.py --backend world|coco
[x]  5. Review and correct labels (CVAT / Label Studio) (laptop) - 44 frames reviewed manually
[~]  6. Split by session, build dataset, zip, upload to Drive (laptop) - scripts/make_split.py
[ ]  7. Train custom YOLO on Colab GPU (Colab T4) - notebooks/colab_train.ipynb -> best.pt
[ ]  8. Evaluate on verified val sessions + live webcam test (laptop) - scripts/infer_live.py --source 0
[ ]  9. Export ONNX and benchmark FPS on laptop CPU (laptop) - export_onnx.py, benchmark.py
[ ] 10. Round 2: error analysis, new data, retrain, compare (both) - pre-label with own model: --backend own
[ ] 11. Package: README, results table, 30-60s demo video (laptop) - docs/results.md, GitHub repo
```
<!-- STATUS:END -->

## Decisions (see docs/context/01_decisions.md for the full list)
- Project is a general config-driven detector (AnyScan), not damage-only
- Pretrained teacher pre-labels -> human verifies -> small YOLO trained on Colab -> live webcam test
- Evaluate only on human-verified labels, split by session

## Open questions
- Which objects for the demo subject? (suggestion: boxes/pallets/people, related to the target company's work)
- What edge hardware does the target company use?

## Log
- 2026-10-31: AnyScan scaffold + context docs created
- 2026-10-31: step 1 -> done (classes: bottle, cup, box)
- 2026-10-31: step 2 -> in_progress
- 2026-10-31: step 1 -> done (classes chosen)
- 2026-10-31: step 2 -> in_progress
- 2026-10-31: step 5 -> in_progress
- 2026-11-01: step 5 -> done (44 frames reviewed manually)
- 2026-11-01: step 5 -> done (44 frames reviewed manually)
- 2026-11-01: step 6 -> in_progress

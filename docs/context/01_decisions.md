# Decisions log

| # | Decision | Reason |
|---|---|---|
| 1 | Learn through one integrated project, not isolated courses | Faster, produces a portfolio piece |
| 2 | Project is custom-model training with pretrained-model auto-labeling + human review | Matches industry workflow; user's own idea |
| 3 | Train on Colab/Kaggle free GPU, not locally | Laptop has no usable NVIDIA GPU |
| 4 | Export to ONNX and benchmark on laptop CPU | Laptop CPU is a legitimate edge stand-in; Pi 5 too costly |
| 5 | Phone for data recording + live demo; webcam as fallback | Better angles/quality |
| 6 | Split train/val BY VIDEO SESSION, not random frame | Avoids near-duplicate leakage and fake-high metrics |
| 7 | Do not augment before splitting; never augment val | Ultralytics augments train on the fly |
| 8 | Evaluate only on human-verified labels | Pseudo-label val measures teacher agreement, not accuracy |
| 9 | Generalized from "DamageScan" to "AnyScan" (config-driven classes) | User wants any known objects, not only damage |
| 10 | Resume claims only what was actually done and measured | Interviewers probe details; honesty is a hard rule |
| 11 | Title self as "Computer Vision Intern Candidate", not "CV Engineer" | Overclaiming backfires for freshers |
| 12 | ROS 2 node is a stretch goal, claim only if actually run | Honesty |
| 13 | Graphify (pip: graphifyy) for code map + AGENTS.md/PROGRESS.md/STEPS.yaml for project state | Graph shows structure; files carry "where we left off" |

## Caveat on the project's value
If the teacher already detects the objects well, the student mostly copies it. Value comes from human corrections, speed (small model on CPU), the user's own class set/domain, and hard cases targeted in round 2. Compare teacher vs student vs pre-labels on verified held-out sessions.

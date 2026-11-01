# AGENTS.md - read this first

## Project
AnyScan: config-driven object detection pipeline. A pretrained teacher model pre-labels the user's own video frames, the user verifies labels, a small YOLO is trained on a Colab GPU, then tested in real time on a webcam/phone stream. Internship portfolio project; honesty about results is a hard requirement.

## Orientation order (do this before anything else)
1. This file (stable rules)
2. `python scripts/steps.py` or `STEPS.yaml` (which step the user is on)
3. `PROGRESS.md` (log, decisions, open questions)
4. `docs/context/` (user profile, decisions, full conversation history, interview notes)
5. `graphify-out/GRAPH_REPORT.md` if present (code map; regenerate with `graphify .`)
6. Only then read source files

## Resuming work
- Tell the user which step they are on and what the next concrete action is.
- When a step finishes: `python scripts/steps.py --done N --note "..."`, then `--start N+1`, then `graphify .`.
- Add new decisions to `docs/context/01_decisions.md` and new history to `docs/context/02_conversation_history.md`.

## Hard rules
- Split train/val by video SESSION, never by random frame.
- Never augment val or make augmented copies before splitting.
- Evaluate only on human-verified labels, not teacher pseudo-labels.
- Never invent metrics, FPS, or hardware claims. Unknown values stay `TBD` in `docs/results.md`.
- No Raspberry Pi/Jetson/ROS 2 claims unless actually done.
- Large files (data/, runs/, weights) are git-ignored and graphify-ignored.

## Conventions
- Python 3.10+, argparse CLIs, `logging` not `print`, clear errors for missing files/cameras.
- Scripts in `scripts/`, one job each. Classes live only in `configs/classes.yaml`.
- Training on Colab/Kaggle (no usable local NVIDIA GPU). Inference/benchmark on laptop CPU.

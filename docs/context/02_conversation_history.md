# Conversation history (chronological summary of everything done so far)

Note: the first part of the history was produced by a different AI assistant with web search; its figures were not independently verified here. Treat statistics (salaries, job-market numbers) as directional.

1. **Learning plan.** User asked how to learn robotics, YOLO, ML, OpenCV. Advice: one integrated project (camera -> YOLO -> OpenCV coordinates -> action), phases from software-only to hardware/simulation, optional custom YOLO training.
2. **Python for robotics jobs.** Companies want engineering habits (argparse, logging, error handling, git, Linux, Docker), ROS 2 as a plus, awareness of ONNX/TensorRT for Jetson.
3. **Fresher intern positioning.** Interns are judged on proof of work, explaining their own code, honesty. Suggested wrapping YOLO as a ROS 2 node (pub/sub), GitHub link + 30s demo video.
4. **No ROS 2 yet.** Suggested 3-5 day path: install ROS 2, turtlesim, pub/sub nodes, YOLO node with a queue/thread for inference. Interview wording: be honest, show willingness to learn.
5. **Is YOLO actually used?** Yes, widely in robotics/industrial inspection (examples cited from search; not verified here).
6. **Interview structure.** Typically screening -> assessment -> technical interview -> HR. Core is explaining the project, pitfalls, honest "I don't know". Use STAR.
7. **Referral situation.** Father got the interview; interviewer still evaluates on merit. No online test per the contact; single interview. Strategy: steer self-intro to the project, be ready to explain every line, prepare 1-2 real pitfall stories.
8. **Damage-region project at the company.** User's YOLO knowledge transfers: swap data/targets; consider segmentation/OBB for cracks. Be honest about not having done damage detection.
9. **CV vs IT careers.** CV ramp-up longer; salary data conflicting across platforms; CV starting pay often higher in India, gap narrows later; junior IT tasks being automated; CV value is in deployment/system integration/problem definition. Treat numbers as rough.
10. **How to learn deployment.** Get a model on a device, profile for bottlenecks, quantize/export (ONNX/TensorRT/OpenVINO/TFLite), learn Docker; ask the mentor what hardware the company uses.
11. **Stipend negotiation.** Normal and polite; first internship priority is experience; ask after the offer; negotiate other perks if stipend is fixed.
12. **Resume.** Present as "Computer Vision Intern Candidate"; build 1-2 real projects first; skills list only what is true; GitHub + demo video.
13. **Ultralytics, ONNX vs ROS 2.** Ultralytics = company + Python package for YOLO (AGPL-3.0 license). ONNX is a model format, independent of ROS 2, but ROS 2 nodes can load ONNX models.
14. **Auto-annotation workflow.** AI pre-labels then human reviews is standard in industry. Tools: CVAT, Label Studio, OneOpen Annotator, VisioFirm, Ultralytics auto_annotate (COCO-limited). Zero-shot text-prompted models (YOLO-World, Grounding DINO, YOLOE) for custom concepts.
15. **Project design (this assistant).** DamageScan then generalized to AnyScan: collect by session, pre-label, review, train on Colab, error analysis + round 2, ONNX + CPU benchmark, README + demo. Colab tips: zip dataset to Drive, unzip locally, save runs to Drive, resume=True.
16. **Hardware.** No NVIDIA GPU -> Colab/Kaggle training. Pi not required; laptop CPU benchmark is acceptable and must be reported honestly.
17. **Camera.** Record normal videos for data; use IP-camera stream only for the live demo; train and test with the same camera type when possible.
18. **Augmentation.** Ultralytics does it automatically on train; do not augment before split or on val.
19. **Graphify.** Verified it exists: pip package `graphifyy`, `graphify .` builds graphify-out/ (graph.json, report); `graphify claude install` etc. wires an assistant. Maps code structure; project state lives in AGENTS.md/PROGRESS.md/STEPS.yaml.
20. **Prototype zips.** damagescan.zip (first scaffold), then this anyscan.zip with generalized classes, `--backend world|coco|own` in prelabel.py, STEPS.yaml + scripts/steps.py tracker, and these context docs.

## Current state
Step 0 done (planning + scaffold). Step 1 in progress (choose objects). No data collected yet. See STEPS.yaml.

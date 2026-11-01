# Interview talking points (derived from the above; for the user's prep)

- Lead the self-introduction toward this project; be ready to explain ANY line of code.
- One-line pitch: "Config-driven pipeline: pretrained teacher pre-labels my own video, I verify labels, train a small YOLO on Colab, split by session to avoid leakage, test live on webcam, export to ONNX and benchmark on CPU."
- Prepare real pitfall stories (record them in PROGRESS.md as they happen): frame duplicates, label errors, lighting failures, FPS limits.
- Know why: split by session; why verified val labels; why small model; why ONNX; teacher vs student.
- Honest answers: "I haven't used ROS 2 yet / haven't deployed on Pi/Jetson", then what you did instead.
- Know ONNX Runtime/TensorRT/OpenVINO exist; say what you actually ran.
- Ultralytics is AGPL-3.0; companies may need a commercial license for products.
- Stipend: ask after an offer, politely; first internship = experience.

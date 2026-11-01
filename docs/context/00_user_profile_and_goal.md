# User profile and goal (context for any AI agent)

## Who the user is
- A fresher (recent/near graduate) in India applying for a robotics/computer-vision INTERN position.
- The interview was arranged via a family referral (father works at the company as a mechanical engineer, not in robotics). The company is mid-sized (not a startup), and per the contact the process is a single interview with no online assessment. The interviewer will still judge on merit.
- Existing skills: a little OpenCV and YOLO, Python. No ROS 2 experience, no completed projects yet.
- The company's work (per the user): object detection, drone usage, robotic arm work, and a project detecting damaged regions.
- Hardware: Windows laptop with a small AMD/integrated GPU (user pasted a description of ~2 GB dedicated VRAM; the assistant could not see the screenshot itself). No usable NVIDIA GPU, so training happens on Colab/Kaggle free GPU. Raspberry Pi 5 judged too expensive; not required.
- Cameras: laptop webcam and phone (phone as IP camera for live demo; normal recording for data collection).

## Goal
Build a quality, honest portfolio project in about two weeks that proves the full CV pipeline:
record video -> frames -> pretrained model pre-labels -> user verifies labels -> train custom YOLO on Colab GPU -> test in real time on webcam -> ONNX export + CPU benchmark -> package on GitHub with demo video.

## The project: AnyScan
A config-driven pipeline for ANY set of objects (edit configs/classes.yaml), not only damage. A pretrained teacher (YOLO-World open-vocabulary, or a standard COCO YOLO) drafts labels; the user corrects them; a small YOLO is trained and tested live. Damage detection can be one class or a stretch goal, since it matches the company's damage-region project.

## User preferences
- Wants honest, realistic guidance; wants to actually do the projects, not just list them on the resume.
- Wants steps tracked and context stored so any AI agent can resume the work.
- Dislikes vague answers; likes explicit step-by-step plans.

# 🦺 Construction Safety Monitoring System

> **YOLO-Based Real-Time Personal Protective Equipment (PPE) Detection and Safety Violation Monitoring**

<p align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![YOLO](https://img.shields.io/badge/YOLO-Ultralytics-green.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-red.svg)
![Platform](https://img.shields.io/badge/Platform-Ubuntu-orange.svg)
![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)

</p>

---

## 📌 Project Overview

Construction sites are hazardous working environments where workers are required to wear Personal Protective Equipment (PPE) such as safety helmets and safety vests. Manual monitoring becomes increasingly difficult as construction sites grow larger, making automated computer vision systems an attractive solution.

This project presents a **real-time Construction Safety Monitoring System** developed using the **Ultralytics YOLO** object detection framework. The application automatically detects workers, identifies missing PPE, monitors restricted zones, logs safety violations, captures evidence screenshots, and generates structured safety reports.

Unlike a simple object detection demo, this project implements a complete engineering pipeline consisting of detection, rule-based safety analysis, event logging, report generation, and visualization.

The system supports both **live webcam monitoring** and **prerecorded construction videos**.

---

# ✨ Features

## Computer Vision

- Real-time YOLO object detection
- Person detection
- Hardhat detection
- Safety vest detection
- Face mask detection
- Vehicle detection
- Machinery detection
- Safety cone detection

---

## Safety Monitoring

- Missing helmet detection
- Missing safety vest detection
- Missing face mask detection
- Restricted zone monitoring
- Rule-based violation analysis
- Automatic violation highlighting

---

## Event Management

- CSV event logging
- Screenshot capture
- Event deduplication
- Timestamp recording
- Confidence score logging

---

## Report Generation

- CSV summary
- Microsoft Excel report
- Violation statistics
- Compliance summary

---

## Visualization

- Live GUI overlay
- Bounding boxes
- FPS display
- Violation counter
- Status indicators
- Annotated output video

---

# 🚀 Quick Start

Install dependencies.

```bash
pip install -r requirements.txt
```

Run the application.

```bash
python3 app.py
```

To process a video.

```bash
python3 app.py --source sample_video.mp4
```

---

# 📷 Demo

## Architecture

<p align="center">
<img src="images/architecture.png" width="90%">
</p>

## Sample Results

Replace these placeholders with your screenshots.

<p align="center">

<img src="images/result1.png" width="45%">

<img src="images/result2.png" width="45%">

</p>

<p align="center">

<img src="images/result3.png" width="45%">

<img src="images/result4.png" width="45%">

</p>

---

# 🎯 Objectives

The primary objectives of this project are:

- Detect construction workers in real time.
- Detect mandatory PPE.
- Identify workers without helmets.
- Identify workers without safety vests.
- Detect workers entering restricted zones.
- Record every violation.
- Generate structured reports.
- Develop a modular software architecture suitable for future expansion.

---

# 🛠 Technologies Used

| Category | Technology |
|-----------|------------|
| Programming Language | Python 3 |
| Deep Learning | Ultralytics YOLO |
| Computer Vision | OpenCV |
| Data Processing | Pandas |
| Numerical Computing | NumPy |
| Geometry | Shapely |
| Report Generation | OpenPyXL |
| Operating System | Ubuntu Linux |

---
# 📂 Dataset Analysis

## Dataset Research

Several publicly available construction safety datasets were evaluated before selecting the final dataset for this project. The selection criteria included annotation quality, object diversity, compatibility with YOLO, and suitability for real-time construction site monitoring.

The following factors were considered during dataset evaluation:

- Availability of PPE-related classes
- Construction-specific environments
- Annotation quality
- Compatibility with the YOLO annotation format
- Public accessibility
- Diversity of worker poses and viewpoints

After evaluating multiple options, a Kaggle-hosted construction safety dataset was selected because it provided a balanced collection of construction site images with annotations for workers and Personal Protective Equipment (PPE).

---

## Selected Dataset

**Source**

Publicly available Construction Safety Dataset hosted on Kaggle.

**Annotation Format**

YOLO

**Directory Structure**

```
yolo_dataset/

images/
    train/
    val/
    test/

labels/
    train/
    val/
    test/

data.yaml
```

The dataset follows the standard Ultralytics YOLO directory structure, allowing direct integration into the training and inference pipeline.

---

## Dataset Classes

The dataset contains ten object categories.

| ID | Class |
|----|--------|
|0|Hardhat|
|1|Mask|
|2|NO-Hardhat|
|3|NO-Mask|
|4|NO-Safety Vest|
|5|Person|
|6|Safety Cone|
|7|Safety Vest|
|8|Machinery|
|9|Vehicle|

These classes provide sufficient information to detect both workers and common construction site safety violations.

---

## Why This Dataset?

The selected dataset was chosen because it provides several advantages over generic object detection datasets.

### Advantages

- Specifically designed for construction environments.
- Includes multiple PPE categories.
- Supports worker safety analysis.
- Uses the YOLO annotation format.
- Publicly available.
- Suitable for transfer learning.

---

## Dataset Limitations

Although suitable for this project, the dataset has several limitations.

- Limited night-time images.
- Few severe weather conditions.
- Some small distant workers.
- Partial occlusions.
- Class imbalance for certain categories.

These limitations affect overall detection accuracy under challenging operating conditions.

---

# 🧹 Data Preparation

Before beginning development, the dataset was carefully validated.

The following preprocessing steps were performed.

- Verified image-label consistency.
- Verified train/validation/test directories.
- Validated class indices.
- Verified YOLO annotation format.
- Loaded dataset using `data.yaml`.
- Tested sample inference using the pretrained model.
- Converted detections into structured Pandas DataFrames.

Unlike many notebook-based demonstrations that use raw YOLO outputs directly, this project converts every detection into a structured DataFrame before further processing. This makes the downstream modules independent of the detector implementation.

---

# 💻 Development Journey

The project evolved through two major development phases.

---

## Phase 1 – Kaggle Prototype

The initial implementation was developed in the Kaggle Notebook environment.

Objectives during this phase included:

- Dataset exploration
- Annotation verification
- Model loading
- Initial inference
- Rule engine design

The original intention was to retrain the YOLO model using the selected dataset.

However, the allocated Kaggle environment used an NVIDIA Tesla P100 GPU while the available PyTorch installation was compiled for newer CUDA architectures.

As a result, model training failed due to CUDA compatibility issues.

Instead of delaying development by troubleshooting the cloud environment, a previously trained model (`best.pt`) was reused for inference. This allowed the project to progress toward building the complete monitoring application.

---

## Phase 2 – Modular Desktop Application

After validating the detection pipeline, the project was migrated from Kaggle to a local Ubuntu environment.

The notebook implementation was redesigned into a modular software architecture consisting of independent Python modules.

Each module performs a dedicated responsibility.

| Module | Responsibility |
|----------|----------------|
|config.py|Application configuration|
|detector.py|YOLO inference|
|violation_engine.py|PPE rule engine|
|zone.py|Restricted zone detection|
|logger.py|CSV logging|
|report.py|Summary report generation|
|app.py|Main application|

This separation improves maintainability, debugging, and future scalability.

---

# ⚙️ Detection Pipeline

The complete processing workflow is illustrated below.

```
Input
   │
   ▼
YOLO Detection
   │
   ▼
Detection DataFrame
   │
   ├─────────────┐
   ▼             ▼
PPE Engine   Restricted Zone
   │             │
   └──────┬──────┘
          ▼
 Event Processing
          │
  ┌───────┼─────────┐
  ▼       ▼         ▼
Logger Screenshot GUI
          │
          ▼
 Report Generator
          │
          ▼
CSV + Excel Reports
```

Every incoming frame passes through this pipeline before being displayed to the user.

---

# 📁 Project Structure

```
Construction-Safety-Monitor/

app.py
config.py
detector.py
violation_engine.py
zone.py
logger.py
report.py

README.md
requirements.txt

model/
    best.pt

logs/

reports/

screenshots/

output/

images/
```

The project follows a modular structure where source code, trained models, reports, screenshots, and output videos are organized into dedicated directories. This organization simplifies maintenance and makes the application easier to extend in future versions.

---
# 🏗️ System Architecture

The Construction Safety Monitoring System is designed using a modular architecture, where each software component is responsible for a single well-defined task. This separation of responsibilities improves maintainability, readability, scalability, and simplifies debugging.

Instead of processing detections directly inside a single application script, the project follows a structured processing pipeline that converts raw object detections into meaningful safety events.

---

## Overall Architecture

<p align="center">
<img src="images/architecture.png" width="95%">
</p>

The above diagram illustrates the complete workflow of the proposed system.

---

# 🔄 Processing Pipeline

Every incoming frame passes through the following stages.

```

Input Video / Webcam
│
▼
Frame Acquisition
│
▼
YOLO Object Detection
│
▼
Detection DataFrame
│
├─────────────┐
▼ ▼
PPE Rule Engine Restricted Zone
│ │
└──────────┬──────────┘
▼
Violation Events
│
├──────────────┬─────────────┬──────────────┐
▼ ▼ ▼ ▼
GUI Logger Screenshot Report
│
▼
CSV + Excel Reports

```

---

# 🧩 Software Modules

The project has been intentionally divided into multiple independent Python modules.

This architecture makes the application easier to test, maintain, and extend.

---

## 1. app.py

**Purpose**

Acts as the central controller of the application.

**Responsibilities**

- Load application configuration
- Initialize the YOLO detector
- Open webcam or video source
- Read video frames
- Execute inference
- Run violation analysis
- Detect restricted zone intrusions
- Display annotated output
- Save screenshots
- Record violation events
- Generate summary reports
- Release system resources

---

## 2. config.py

This module stores all configurable application parameters.

Examples include:

- Model path
- Detection confidence threshold
- Restricted zone coordinates
- Screenshot directory
- Report directory
- Log directory
- Overlay colours
- Event cooldown period

Keeping configuration parameters in a single location allows users to customize the application without modifying the core implementation.

---

## 3. detector.py

The detector module loads the pretrained YOLO model and performs inference.

Main tasks:

- Load `best.pt`
- Process image frames
- Execute object detection
- Extract detections
- Convert detections into a Pandas DataFrame

Each detection contains:

- Object class
- Confidence score
- Bounding box coordinates
- Centre coordinates

Using a DataFrame instead of raw YOLO outputs simplifies downstream processing.

---

## 4. violation_engine.py

The violation engine transforms object detections into meaningful safety events.

The implemented rules include:

- Missing safety helmet
- Missing safety vest
- Missing face mask

The module associates PPE detections with the corresponding worker.

To reduce duplicate events, person detections are sorted by bounding box area before PPE assignment.

---

## 5. zone.py

The restricted zone module monitors worker movement inside dangerous construction areas.

Each detected worker is represented by the centre of the bounding box.

This point is evaluated using polygon-based point-in-polygon testing.

If the point lies inside the configured restricted region, a Restricted Zone Violation is generated.

The monitoring region can easily be modified by updating the polygon coordinates in `config.py`.

---

## 6. logger.py

The logging module records every detected violation.

Each event includes:

- Timestamp
- Frame number
- Violation category
- Detection confidence
- Screenshot filename

To improve report quality, duplicate events are suppressed using a configurable cooldown mechanism.

---

## 7. report.py

This module automatically generates structured safety reports after processing completes.

Generated outputs include:

- Event Log (CSV)
- Summary Report (CSV)
- Microsoft Excel Report

These reports provide supervisors with an overview of construction site safety compliance.

---

# 🤖 Model Details

## Selected Model

The project uses the **Ultralytics YOLO** object detection framework.

YOLO was selected because it provides:

- High inference speed
- Excellent detection accuracy
- Lightweight deployment
- Multi-class detection
- Strong community support
- Easy Python integration

The application loads the trained model from

```

model/best.pt

```

during startup.

---

# 🏋️ Training Methodology

The initial project objective included retraining the YOLO model using the selected construction safety dataset.

The planned workflow consisted of:

1. Dataset preparation
2. Image preprocessing
3. Model training
4. Validation
5. Weight export

However, model training could not be completed because of CUDA compatibility issues within the Kaggle environment.

Instead of postponing the entire project, the previously trained model (`best.pt`) was reused for inference.

This allowed development to focus on building a complete production-oriented monitoring application rather than repeating the training process.

---

# ⚙️ Inference Configuration

The application uses configurable inference parameters stored in `config.py`.

Typical parameters include:

| Parameter | Description |
|-----------|-------------|
| Model Path | Location of `best.pt` |
| Confidence Threshold | Minimum confidence required for detections |
| Restricted Zone | Polygon defining unsafe areas |
| Event Cooldown | Prevents duplicate logging |
| Screenshot Directory | Evidence image storage |
| Report Directory | CSV and Excel output |

---

# 🎯 Design Decisions

Several architectural decisions were made during development to improve software quality.

### Modular Architecture

Each software module performs a single responsibility, making future maintenance significantly easier.

---

### DataFrame-Based Processing

Raw YOLO outputs are immediately converted into structured Pandas DataFrames.

This abstraction allows downstream modules to operate independently of the detector implementation.

---

### Rule-Based Safety Engine

Instead of relying solely on object detection, a dedicated rule engine determines whether detected PPE belongs to each worker.

This significantly improves interpretability and simplifies future expansion.

---

### Event Deduplication

Continuous video processing can generate hundreds of identical events.

A configurable cooldown mechanism suppresses repeated detections, resulting in concise logs and more meaningful reports.

---

### Configurable Restricted Zones

Restricted areas are represented using configurable polygon coordinates rather than hardcoded logic.

This allows the application to be adapted to different construction sites without modifying the source code.

---

# 📊 Engineering Highlights

✔ Modular software architecture

✔ Real-time object detection

✔ Rule-based PPE analysis

✔ Polygon-based restricted zone detection

✔ Automatic event logging

✔ Screenshot capture

✔ CSV report generation

✔ Excel report generation

✔ Video and webcam support

✔ Production-oriented folder structure

---
# 📈 Experimental Results

The developed system was evaluated using both prerecorded construction site videos and live webcam streams. Testing focused on verifying the complete end-to-end workflow, including object detection, PPE violation analysis, restricted zone monitoring, event logging, screenshot generation, and report creation.

The objective of the evaluation was not only to verify object detection performance but also to validate the engineering workflow from image acquisition to automated report generation.

---

# 🧪 Testing Environment

| Component | Specification |
|------------|--------------|
| Operating System | Ubuntu 24.04 LTS |
| Programming Language | Python 3.12 |
| Framework | Ultralytics YOLO |
| Computer Vision Library | OpenCV |
| Data Processing | Pandas |
| Geometry Library | Shapely |
| Report Generation | OpenPyXL |
| Development Platform | Kaggle + Local Ubuntu |

---

# 📷 Sample Results

The following screenshots illustrate the performance of the developed application under different scenarios.

---

## Result 1 – Multiple PPE Violations

<p align="center">
<img src="images/result1.png" width="90%">
</p>

This example demonstrates simultaneous detection of multiple workers along with PPE violations. Workers without mandatory helmets or safety vests are identified and highlighted using coloured bounding boxes and descriptive labels.

**Observations**

- Multiple workers detected simultaneously.
- PPE violations correctly classified.
- Confidence values displayed for each detection.
- Real-time annotations generated successfully.

---

## Result 2 – Restricted Zone Detection

<p align="center">
<img src="images/result2.png" width="90%">
</p>

The restricted zone module continuously evaluates worker positions relative to a predefined polygon.

Whenever a worker enters the restricted area, the system immediately generates a Restricted Zone Violation.

**Observations**

- Polygon-based monitoring works correctly.
- Workers are evaluated independently.
- Restricted zone violations are generated automatically.

---

## Result 3 – Face Mask Detection

<p align="center">
<img src="images/result3.png" width="90%">
</p>

The application successfully detects workers wearing and not wearing face masks.

This demonstrates the ability of the detector to identify relatively small PPE objects under normal lighting conditions.

---

## Result 4 – Safety Helmet Detection

<p align="center">
<img src="images/result4.png" width="90%">
</p>

The trained YOLO model successfully identifies construction helmets even when several workers appear in the same frame.

The rule engine correctly distinguishes between workers wearing helmets and workers violating helmet requirements.

---

## Result 5 – Multiple Object Detection

<p align="center">
<img src="images/result5.png" width="90%">
</p>

The detector simultaneously recognizes several object categories, including:

- Workers
- Safety Helmets
- Safety Vests
- Machinery
- Vehicles
- Safety Cones

The ability to detect multiple object classes provides additional contextual information useful for future safety analytics.

---

## Result 6 – Live Monitoring Interface

<p align="center">
<img src="images/result6.png" width="90%">
</p>

The desktop application continuously processes incoming frames while displaying:

- Bounding boxes
- Object labels
- FPS counter
- Violation statistics
- Restricted zone overlay
- System status

This provides operators with a simple real-time monitoring dashboard.

---

## Result 7 – Complete Desktop Application

<p align="center">
<img src="images/result7.png" width="90%">
</p>

The final application integrates every software module into a unified desktop interface.

The complete workflow includes:

- YOLO inference
- PPE analysis
- Restricted zone monitoring
- Event logging
- Screenshot capture
- Report generation

---

# 📊 Performance Summary

The primary objective of this project was to build a complete engineering solution rather than train a new object detection model.

Therefore, evaluation focused on validating system functionality.

| Feature | Status |
|-----------|---------|
| Live Webcam Support | ✅ |
| Video Processing | ✅ |
| Worker Detection | ✅ |
| Helmet Detection | ✅ |
| Safety Vest Detection | ✅ |
| Face Mask Detection | ✅ |
| Restricted Zone Detection | ✅ |
| Screenshot Capture | ✅ |
| Event Logging | ✅ |
| CSV Report Generation | ✅ |
| Excel Report Generation | ✅ |

The application successfully demonstrated all major features during testing.

---

# 📁 Generated Outputs

During execution, the application automatically generates several useful output files.

## Event Log

```
logs/events.csv
```

Stores:

- Timestamp
- Frame Number
- Violation Type
- Detection Confidence
- Screenshot Reference

---

## Summary Report

```
reports/summary.csv
```

Provides an overview of all detected safety violations.

---

## Excel Report

```
reports/Safety_Report.xlsx
```

Contains:

- Total workers detected
- Helmet violations
- Safety vest violations
- Restricted zone violations
- Compliance summary

---

## Screenshots

```
screenshots/
```

Evidence images are automatically captured whenever safety violations occur.

These screenshots provide visual proof of detected events and are referenced inside the event log.

---

## Annotated Output Video

```
output/
```

The generated output video contains:

- Bounding boxes
- Object labels
- Violation indicators
- Restricted zone overlay
- Live statistics

This annotated video allows reviewers to visualize the complete operation of the monitoring system.

---

# ⚠️ Failure Cases

Although the developed system performs reliably under normal operating conditions, several practical limitations remain.

### Small Objects

Workers located far from the camera occupy very few pixels, reducing detection confidence.

---

### Partial Occlusion

Scaffolding, construction machinery, or nearby workers may partially obscure PPE, causing occasional missed detections.

---

### Low-Light Conditions

Detection confidence decreases under poor illumination because PPE objects become less distinguishable.

---

### Camera Perspective

Extreme camera angles may hide helmets or safety vests from the detector.

---

### Crowded Construction Sites

Highly congested scenes increase object overlap, making PPE assignment more challenging.

---

# 💡 Future Improvements

The modular architecture enables numerous future enhancements.

Possible improvements include:

- DeepSORT-based worker tracking
- ByteTrack integration
- Multi-camera synchronization
- Cloud deployment
- Docker containerization
- Web dashboard
- Mobile notifications
- Audio alarm generation
- PDF report generation
- Edge AI deployment
- Automatic daily compliance reports
- Worker identity recognition
- Behaviour analysis using temporal models

These enhancements would further improve the practicality and scalability of the system for deployment in real-world construction environments.

---
# 🚀 Installation

## System Requirements

The application has been developed and tested on Ubuntu Linux.

### Minimum Requirements

| Component | Specification |
|-----------|---------------|
| Processor | Intel Core i5 / AMD Ryzen 5 |
| RAM | 8 GB |
| Storage | 5 GB Free Space |
| Python | 3.10 or later |
| Camera | USB Webcam or CCTV Video |

### Recommended Requirements

| Component | Specification |
|-----------|---------------|
| Processor | Intel Core i7 / AMD Ryzen 7 |
| RAM | 16 GB |
| Storage | SSD |
| GPU | NVIDIA GPU (Optional) |

> **Note:** The application runs entirely on CPU. A GPU is recommended only for faster inference.

---

# 📦 Installation

## 1. Clone the Repository

```bash
git clone <repository-url>
cd Construction-Safety-Monitor
```

---

## 2. Create a Virtual Environment

```bash
python3 -m venv venv
```

Activate it:

**Linux**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Place the Model

Copy the trained model into:

```
model/
    best.pt
```

---

# ▶️ Running the Application

## Live Webcam

```bash
python3 app.py
```

---

## Process a Video

```bash
python3 app.py --source sample_video.mp4
```

---

## Use Another Camera

```bash
python3 app.py --source 1
```

For systems with multiple cameras:

| Camera Index | Device |
|--------------|--------|
| 0 | Default Camera |
| 1 | USB Camera |
| 2 | Additional Camera |

Network cameras can also be used by supplying an RTSP or HTTP stream URL.

Example:

```text
rtsp://username:password@camera_ip/live
```

---

# ⚙️ Configuration

All user-adjustable settings are centralized in `config.py`.

The most commonly modified parameters are:

## Model

```python
MODEL_PATH = BASE_DIR / "model" / "best.pt"
```

---

## Confidence Threshold

```python
CONFIDENCE_THRESHOLD = 0.35
```

Increasing this value reduces false positives but may also reduce recall.

---

## Restricted Zone

Example:

```python
RESTRICTED_ZONE = [

    (380,300),
    (640,300),
    (640,640),
    (380,640)

]
```

The polygon can be modified to match any construction site's restricted area.

---

## Output Directories

The following folders are automatically created:

```
logs/
reports/
screenshots/
output/
```

---

## Event Cooldown

Duplicate event logging is controlled through a configurable cooldown parameter.

This helps prevent repeated logging of the same violation across consecutive frames.

---

# 📂 Repository Structure

```
Construction-Safety-Monitor/

app.py
config.py
detector.py
violation_engine.py
zone.py
logger.py
report.py

requirements.txt
README.md

model/
    best.pt

logs/
reports/
screenshots/
output/

images/
```

---

# 📝 Assumptions

The current implementation assumes:

- A clear camera view of workers.
- PPE is visible in the captured image.
- Restricted zones remain fixed during monitoring.
- Input video is reasonably illuminated.
- Workers are sufficiently visible for object detection.

---

# ⚠️ Known Limitations

Current limitations include:

- Worker identity tracking is not implemented.
- Multi-camera synchronization is not available.
- Performance decreases under poor lighting.
- Small distant objects remain challenging.
- Temporary occlusions may reduce detection accuracy.
- Behaviour analysis beyond PPE and restricted zones is not included.

---

# 🔮 Future Work

The modular software architecture enables several future enhancements.

Planned improvements include:

- Worker tracking using DeepSORT or ByteTrack
- Cloud-based monitoring
- Docker deployment
- Web dashboard
- Mobile notifications
- Audio alarms
- PDF report generation
- Automatic email reports
- Edge AI deployment
- Worker identity recognition
- Behaviour analysis
- Multi-camera synchronization
- Daily automated compliance reports

---

# 📚 References

- Ultralytics YOLO Documentation  
  https://docs.ultralytics.com

- OpenCV Documentation  
  https://opencv.org/

- PyTorch Documentation  
  https://pytorch.org/

- Pandas Documentation  
  https://pandas.pydata.org/

- Shapely Documentation  
  https://shapely.readthedocs.io/

- Kaggle  
  https://www.kaggle.com/

---

# ✅ Conclusion

The Construction Safety Monitoring System demonstrates how modern computer vision techniques can be integrated into a practical engineering solution for workplace safety.

The project extends beyond object detection by combining YOLO-based inference with rule-based PPE analysis, restricted zone monitoring, event logging, screenshot capture, and automated report generation.

A modular software architecture was adopted to improve maintainability and support future enhancements. The system successfully processes both live webcam streams and prerecorded construction videos, automatically generating structured reports and evidence for safety audits.

Although implemented as a prototype, the architecture provides a solid foundation for future extensions such as worker tracking, cloud deployment, multi-camera monitoring, and intelligent safety analytics.

---

# 📄 License

This project is released for educational and research purposes.

---

# 👨‍💻 Author

**N J Ajmal**

Construction Safety Monitoring System

2026

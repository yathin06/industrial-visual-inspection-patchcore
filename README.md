# 🔍 Industrial Visual Inspection with PatchCore

### AI-Based Anomaly Detection for Manufacturing Quality Inspection

An end-to-end industrial visual inspection prototype using **PatchCore**, **PyTorch**, **Anomalib**, **FastAPI**, **Streamlit**, and **Docker**.

The system analyzes product images, generates an **anomaly score**, and converts the result into a factory-style quality decision:

| Decision       | Meaning                    |
| -------------- | -------------------------- |
| ✅ **OK**       | Part accepted              |
| ⚠️ **Warning** | Manual inspection required |
| ❌ **NG**       | Part rejected              |

---

## 🎯 Project Goal

In manufacturing, collecting labelled examples of every possible defect is difficult.

Instead of training a conventional classifier on many defect classes, this project uses **PatchCore anomaly detection**.

PatchCore learns the visual feature distribution of **normal components**. During inspection, a new image is compared against this learned representation.

```text
Normal Training Images
        │
        ▼
Feature Extraction
        │
        ▼
PatchCore Memory Bank
        │
        ▼
New Product Image
        │
        ▼
Anomaly Score
        │
        ▼
OK / Warning / NG
```

The anomaly-detection model is then integrated into a small **production-style inspection architecture** with an API, dashboard, Docker deployment, and simulated camera/conveyor workflow.

---

# ⚙️ System Architecture

```text
                ┌─────────────────────┐
                │    Product Image    │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Image Preprocessing │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │   PatchCore Model   │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │    Anomaly Score    │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Inspection Decision │
                │ OK / Warning / NG   │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │    FastAPI API      │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Streamlit Dashboard │
                └─────────────────────┘
```

---

## 📊 Dashboard Preview

![Industrial Visual Inspection Dashboard](docs/images/image1.png)

# 🚀 Key Features

* 🔍 **PatchCore-based anomaly detection**
* 🧠 Normal-image feature learning and anomaly scoring
* 🏭 Factory-style **OK / Warning / NG** decision logic
* ⚡ Reusable inference engine
* 🌐 **FastAPI** REST backend
* 📊 **Streamlit** monitoring dashboard
* 📈 Inspection counters and recent inspection history
* 🎥 Camera/conveyor-style inspection client
* 🔄 Production-stream simulation
* 🐳 **Docker & Docker Compose** deployment
* 💾 Pretrained PatchCore checkpoint included

---

# 🛠️ Technology Stack

| Area                  | Technology     |
| --------------------- | -------------- |
| Programming           | Python         |
| Deep Learning         | PyTorch        |
| Anomaly Detection     | PatchCore      |
| Framework             | Anomalib       |
| Backend API           | FastAPI        |
| Dashboard             | Streamlit      |
| Containerization      | Docker         |
| Service Orchestration | Docker Compose |

---

# 📁 Project Structure

```text
industrial-visual-inspection-patchcore/
│
├── api/
│   └── inspection_api.py
│
├── app/
│   └── dashboard.py
│
├── demo_scripts/
│   └── START_VISUAL_INSPECTION.bat
│
├── models/
│   └── patchcore_metal_nut/
│       └── Patchcore/
│           └── MVTecAD/
│               └── metal_nut/
│                   └── v1/
│                       └── weights/
│                           └── lightning/
│                               └── model.ckpt
│
├── src/
│   ├── 01_check_dataset.py
│   ├── 02_preprocess_preview.py
│   ├── 03_train_patchcore.py
│   ├── 04_predict_single_image.py
│   ├── 05_test_inspection_engine.py
│   ├── 06_test_production_stream.py
│   ├── 07_camera_conveyor_client.py
│   └── inspection_engine.py
│
├── Dockerfile
├── Dockerfile.dashboard
├── docker-compose.yml
├── requirements.txt
├── requirements-dashboard.txt
├── .dockerignore
├── .gitignore
└── README.md
```

---

# 🔄 Inspection Workflow

## 1. Dataset Verification

```text
src/01_check_dataset.py
```

Checks the dataset structure before preprocessing and model development.

---

## 2. Preprocessing Preview

```text
src/02_preprocess_preview.py
```

Verifies that images are loaded and transformed correctly before they are passed into the anomaly-detection pipeline.

---

## 3. PatchCore Model Development

```text
src/03_train_patchcore.py
```

Uses normal component images to build the PatchCore representation of normal visual features.

PatchCore does not require examples of every possible defect. Instead, anomalous components are identified based on their deviation from the learned normal feature distribution.

---

## 4. Single-Image Prediction

```text
src/04_predict_single_image.py
```

Loads the trained PatchCore checkpoint and evaluates an individual product image.

The output contains an anomaly score representing how strongly the image differs from the normal reference distribution.

---

## 5. Reusable Inspection Engine

```text
src/inspection_engine.py
```

The inspection engine loads the PatchCore model once and keeps it available for repeated inspections.

```text
Image
  │
  ▼
PatchCore Inference
  │
  ▼
Anomaly Score
  │
  ▼
Decision Logic
  │
  ├── OK
  ├── Warning
  └── NG
```

This avoids reloading the model for every incoming product image.

---

## 6. Inspection Engine Test

```text
src/05_test_inspection_engine.py
```

Verifies that the reusable inspection engine correctly loads the trained model and processes images.

---

## 7. Production Stream Simulation

```text
src/06_test_production_stream.py
```

Simulates repeated image inspection similar to products arriving sequentially on a manufacturing line.

---

## 8. Camera / Conveyor Client

```text
src/07_camera_conveyor_client.py
```

Represents a camera/conveyor-style inspection workflow where images can be continuously submitted to the inspection system.

---

# 🌐 FastAPI Backend

```text
api/inspection_api.py
```

The inspection pipeline is exposed through a **FastAPI REST service**.

```text
Inspection Client
       │
       ▼
Image Request
       │
       ▼
FastAPI
       │
       ▼
Inspection Engine
       │
       ▼
PatchCore
       │
       ▼
Decision + Score
       │
       ▼
API Response
```

The API also maintains inspection statistics and recent inspection history for the dashboard.

---

# 📊 Streamlit Dashboard

```text
app/dashboard.py
```

The Streamlit interface converts the ML output into an operator-friendly inspection dashboard.

It provides information such as:

* Total inspected components
* Accepted components
* Warning cases
* Rejected components
* Current inspection status
* Recent inspection history

This demonstrates how an anomaly-detection model can be integrated into an **industrial decision-support interface** instead of remaining only as an offline ML script.

---

# 📦 Dataset

The project was developed using the **MVTec AD `metal_nut` category**.

The original dataset is **not included in this repository** because it was obtained from an external source and redistribution of the source images is intentionally avoided.

For retraining, the dataset should be obtained from the original source and placed locally in:

```text
datasets/
└── metal_nut/
    ├── train/
    ├── test/
    └── ground_truth/
```

The entire `datasets/` directory is excluded through `.gitignore`.

---

# 🧠 Trained PatchCore Model

A trained PatchCore checkpoint is included:

```text
models/
└── patchcore_metal_nut/
    └── Patchcore/
        └── MVTecAD/
            └── metal_nut/
                └── v1/
                    └── weights/
                        └── lightning/
                            └── model.ckpt
```

Checkpoint size:

```text
≈ 14 MB
```

Including the checkpoint allows the inference pipeline to be tested without rebuilding the PatchCore model from scratch.

---

# 🖼️ Generated Results

Generated prediction images and runtime outputs are intentionally excluded from Git tracking.

```text
outputs/
results/
models/**/images/
```

These folders may contain anomaly visualizations or images derived from the external dataset.

They can be regenerated locally using the model and inference scripts.

---

# 🐳 Running with Docker

Build and start the application:

```bash
docker compose up --build
```

Docker Compose runs the main services separately:

```text
┌─────────────────────────┐
│ PatchCore + FastAPI API │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│   Streamlit Dashboard   │
└─────────────────────────┘
```

---

# 📊 Dashboard Access

After the containers are running:

```text
http://localhost:8501
```

opens the Streamlit dashboard.

---

# ⚡ API Status

The FastAPI service can be checked using:

```text
http://127.0.0.1:8000/status
```

The status endpoint provides the current inspection state and inspection counters.

---

# 🏭 Example Industrial Use Case

```text
Component arrives
        │
        ▼
Camera captures image
        │
        ▼
Image sent to API
        │
        ▼
PatchCore inference
        │
        ▼
Anomaly score
        │
        ▼
┌───────────┬─────────────┬───────────┐
│    OK     │   Warning   │    NG     │
│           │             │           │
│  Accept   │ Manual Check│  Reject   │
└───────────┴─────────────┴───────────┘
        │
        ▼
Dashboard updated
```

A future production implementation could connect the inspection result to a **PLC, conveyor controller, industrial camera, or automatic reject mechanism**.

---

# 🎯 What This Project Demonstrates

This project demonstrates an end-to-end workflow covering:

**Computer Vision**

* Image preprocessing
* Visual feature extraction
* Anomaly detection

**Machine Learning**

* PatchCore
* Normal-feature representation
* Anomaly scoring
* Model inference

**Software Engineering**

* Modular Python architecture
* REST API development
* Dashboard development

**Deployment**

* Docker
* Docker Compose
* API/dashboard separation

**Industrial Automation Concept**

* Camera-based inspection
* Conveyor inspection workflow
* OK / NG decision logic
* Potential PLC integration

---

# 🔮 Future Improvements

Possible extensions include:

* 📷 Real industrial camera integration
* ⚙️ PLC communication
* 🏭 Conveyor synchronization
* 🚨 Automatic reject mechanism
* 🗄️ SQL inspection database
* 🔢 Product/serial-number traceability
* 📈 Long-term quality trend monitoring
* 🧠 Model drift monitoring
* ⚖️ Comparison with PaDiM, EfficientAD and STFPM
* 💻 Industrial edge-device deployment
* 🔄 Automated retraining pipeline
* 🔗 MES integration

---

# ⚠️ Project Scope

This repository is an **engineering prototype** demonstrating an AI-based industrial visual-inspection workflow.

It has not been validated or certified as a production quality-control system.

---

# 👤 Author

**Yathin**

Industrial AI · Machine Learning · Automation · Mechatronics

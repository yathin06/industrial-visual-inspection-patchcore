\# Industrial Visual Inspection using PatchCore



An end-to-end \*\*industrial visual anomaly detection system\*\* built using \*\*PatchCore, PyTorch, Anomalib, FastAPI, Streamlit, and Docker\*\*.



The system analyzes product images, calculates an anomaly score using PatchCore, and converts the result into a factory-style inspection decision:



\* \*\*OK\*\* — Part accepted

\* \*\*Warning\*\* — Manual inspection required

\* \*\*NG\*\* — Part rejected



\---



\## Project Overview



Traditional supervised defect-detection systems usually require labelled examples of every defect type. In industrial manufacturing, however, collecting sufficient examples of all possible defects can be difficult.



This project therefore uses \*\*PatchCore anomaly detection\*\*.



PatchCore learns feature representations from \*\*normal product images\*\* and compares new images against the learned normal feature distribution. Images that differ significantly from the normal patterns receive a higher anomaly score.



The anomaly-detection model is integrated into a small production-style inspection system containing:



\* Dataset verification

\* Image preprocessing

\* PatchCore model training

\* Single-image anomaly prediction

\* Reusable inspection engine

\* FastAPI inference service

\* Streamlit monitoring dashboard

\* Inspection counters and inspection history

\* Production-stream simulation

\* Camera/conveyor client

\* Docker-based deployment



\---



\## System Architecture



```text

Product Image

&#x20;     │

&#x20;     ▼

Image Preprocessing

&#x20;     │

&#x20;     ▼

PatchCore Model

&#x20;     │

&#x20;     ▼

Anomaly Score

&#x20;     │

&#x20;     ▼

Inspection Decision

&#x20;     │

&#x20;     ├── OK

&#x20;     ├── Warning

&#x20;     └── NG

&#x20;     │

&#x20;     ▼

FastAPI Backend

&#x20;     │

&#x20;     ▼

Inspection Counters / History

&#x20;     │

&#x20;     ▼

Streamlit Dashboard

```



\---



\## Technologies Used



\* Python

\* PyTorch

\* Anomalib

\* PatchCore

\* FastAPI

\* Streamlit

\* Docker

\* Docker Compose



\---



\## Project Structure



```text

industrial-visual-inspection-patchcore/

│

├── api/

│   └── inspection\_api.py

│

├── app/

│   └── dashboard.py

│

├── demo\_scripts/

│   └── START\_VISUAL\_INSPECTION.bat

│

├── models/

│   └── patchcore\_metal\_nut/

│       └── Patchcore/

│           └── MVTecAD/

│               └── metal\_nut/

│                   └── v1/

│                       └── weights/

│                           └── lightning/

│                               └── model.ckpt

│

├── src/

│   ├── 01\_check\_dataset.py

│   ├── 02\_preprocess\_preview.py

│   ├── 03\_train\_patchcore.py

│   ├── 04\_predict\_single\_image.py

│   ├── 05\_test\_inspection\_engine.py

│   ├── 06\_test\_production\_stream.py

│   ├── 07\_camera\_conveyor\_client.py

│   └── inspection\_engine.py

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



\---



\## Project Workflow



\### 1. Dataset Verification



```text

src/01\_check\_dataset.py

```



Checks the dataset structure and verifies that the required image folders are available before preprocessing and training.



\---



\### 2. Preprocessing Preview



```text

src/02\_preprocess\_preview.py

```



Used to inspect the image preprocessing pipeline before model training.



This helps verify that the images are being loaded and transformed correctly before they are provided to PatchCore.



\---



\### 3. PatchCore Training



```text

src/03\_train\_patchcore.py

```



Trains the PatchCore anomaly-detection model using normal product images.



Instead of directly learning defect classes, PatchCore builds a representation of normal visual features that can later be used to detect deviations.



\---



\### 4. Single-Image Prediction



```text

src/04\_predict\_single\_image.py

```



Loads the trained PatchCore model and performs anomaly prediction on an individual image.



The model produces an anomaly score that represents how strongly the input differs from the learned normal-product representation.



\---



\### 5. Inspection Engine



```text

src/inspection\_engine.py

```



Provides reusable inference logic for production-style inspection.



The PatchCore model is loaded once and can then be used repeatedly for multiple incoming images.



The model output is converted into an inspection decision:



```text

Input Image

&#x20;    │

&#x20;    ▼

PatchCore

&#x20;    │

&#x20;    ▼

Anomaly Score

&#x20;    │

&#x20;    ▼

OK / Warning / NG

```



This separates the machine-learning inference logic from the API and user interface.



\---



\### 6. Inspection Engine Testing



```text

src/05\_test\_inspection\_engine.py

```



Tests the reusable inspection engine and verifies that images can be processed correctly using the trained model.



\---



\### 7. Production Stream Simulation



```text

src/06\_test\_production\_stream.py

```



Simulates repeated image inspection to represent a simple production-line workflow.



Instead of loading the model separately for every image, the inspection engine remains active and processes multiple incoming parts.



\---



\### 8. Camera / Conveyor Client



```text

src/07\_camera\_conveyor\_client.py

```



Provides a client-side workflow for camera/conveyor-style inspection.



This represents how the system could later receive images continuously from an industrial camera or conveyor-based inspection station.



\---



\## FastAPI Backend



```text

api/inspection\_api.py

```



The trained PatchCore inspection system is exposed through a \*\*FastAPI REST API\*\*.



The API allows external applications or inspection clients to submit images for inference.



The backend handles:



```text

Image Request

&#x20;     │

&#x20;     ▼

Inspection Engine

&#x20;     │

&#x20;     ▼

PatchCore Prediction

&#x20;     │

&#x20;     ▼

Inspection Decision

&#x20;     │

&#x20;     ▼

API Response

```



The API also maintains inspection statistics and recent inspection history that can be consumed by the dashboard.



\---



\## Streamlit Dashboard



```text

app/dashboard.py

```



A \*\*Streamlit dashboard\*\* provides a visual interface for monitoring the inspection system.



The dashboard is designed to display information such as:



\* Total inspected parts

\* Accepted parts

\* Warning cases

\* Rejected parts

\* Inspection status

\* Recent inspection history



This converts the machine-learning model into a more practical industrial decision-support interface.



\---



\## Dataset



The project uses the \*\*MVTec AD dataset — `metal\_nut` category\*\* for development and testing.



The original dataset is \*\*not included in this GitHub repository\*\*.



The dataset was obtained from an external source, and redistribution of the original images is therefore intentionally avoided in this repository.



Users who want to reproduce the training process should obtain the dataset from the original MVTec AD source and place it locally in the required dataset directory.



Example local structure:



```text

datasets/

└── metal\_nut/

&#x20;   ├── train/

&#x20;   ├── test/

&#x20;   └── ground\_truth/

```



The complete `datasets/` directory is excluded from Git tracking using `.gitignore`.



\---



\## Trained PatchCore Model



The trained PatchCore checkpoint used by this project \*\*is included in the repository\*\*.



```text

models/

└── patchcore\_metal\_nut/

&#x20;   └── Patchcore/

&#x20;       └── MVTecAD/

&#x20;           └── metal\_nut/

&#x20;               └── v1/

&#x20;                   └── weights/

&#x20;                       └── lightning/

&#x20;                           └── model.ckpt

```



The checkpoint is approximately \*\*14 MB\*\*.



Including the trained checkpoint allows the inference pipeline to be tested without requiring the model to be retrained first.



\---



\## Generated Results



Generated prediction images and runtime output folders are intentionally not included in the repository.



Examples include:



```text

outputs/

results/

models/\*\*/images/

```



These directories may contain generated anomaly visualizations or images derived from the external dataset.



They are excluded using `.gitignore` and can be regenerated locally by running the training or inference pipeline.



\---



\## Docker Deployment



The project includes Docker configuration for containerized deployment.



The system can be built and started using:



```bash

docker compose up --build

```



Docker Compose runs the main components as separate services:



```text

PatchCore / FastAPI Service

&#x20;         │

&#x20;         ▼

&#x20;    REST API

&#x20;         │

&#x20;         ▼

Streamlit Dashboard

```



\---



\## Dashboard



After starting the Docker containers, the Streamlit dashboard can be opened at:



```text

http://localhost:8501

```



\---



\## API



The FastAPI service runs locally and provides the inference backend.



The API status can be checked at:



```text

http://127.0.0.1:8000/status

```



The status endpoint can be used to inspect the current inspection counters and system state.



\---



\## Example Industrial Workflow



A possible production implementation would work as follows:



```text

Component arrives at inspection station

&#x20;               │

&#x20;               ▼

Industrial camera captures image

&#x20;               │

&#x20;               ▼

Image sent to FastAPI

&#x20;               │

&#x20;               ▼

PatchCore analyzes image

&#x20;               │

&#x20;               ▼

Anomaly score generated

&#x20;               │

&#x20;               ▼

Inspection decision

&#x20;      ┌────────┼────────┐

&#x20;      ▼        ▼        ▼

&#x20;     OK     Warning     NG

&#x20;      │        │        │

&#x20;      ▼        ▼        ▼

&#x20;  Accept     Manual    Reject

&#x20;             Check

&#x20;               │

&#x20;               ▼

&#x20;       Dashboard Updated

```



\---



\## Current Scope



This project demonstrates an end-to-end prototype for \*\*AI-based industrial visual inspection\*\*, including:



\* Anomaly detection

\* PatchCore model training

\* Model inference

\* Factory-style decision logic

\* REST API integration

\* Dashboard monitoring

\* Production-stream simulation

\* Camera/conveyor integration concept

\* Dockerized deployment



The project is intended as an engineering prototype and has not been validated as a certified production quality-control system.



\---



\## Future Improvements



Possible future extensions include:



\* Real industrial camera integration

\* PLC communication

\* Conveyor synchronization

\* Hardware triggering

\* Automatic reject mechanism

\* Persistent SQL inspection database

\* Traceability using component IDs

\* Model-performance monitoring

\* Additional anomaly-detection algorithms

\* Comparison with PaDiM, EfficientAD, STFPM, or other models

\* Edge-device deployment

\* Automatic model retraining

\* Manufacturing execution system integration



\---



\## Author



\*\*Yathin\*\*



Industrial AI · Machine Learning · Automation · Mechatronics




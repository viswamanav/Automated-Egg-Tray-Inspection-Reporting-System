# Automated Egg Tray Inspection & Reporting System

A lightweight backend service that simulates an automated factory-floor egg tray inspection system using **YOLOv8**, **FastAPI**, **PostgreSQL**, and **PyQt5**.

The application detects eggs in a tray, verifies whether the expected number of eggs is present, stores every inspection in a PostgreSQL database, and provides reporting APIs for inspection history and analytics.

---

# Features

- Egg detection using a custom YOLOv8 model (`best.pt`)
- Automatic egg counting
- Detects missing eggs based on an expected tray size
- PASS / FAIL inspection decision
- Annotated result image generation
- FastAPI REST APIs
- PostgreSQL database integration
- Inspection history
- Summary reports using SQL aggregation
- Desktop interface built with PyQt5
- Configurable using environment variables

---

# Technology Stack

- Python 3.11+
- FastAPI
- Ultralytics YOLOv8
- PostgreSQL
- SQLAlchemy ORM
- OpenCV
- NumPy
- PyQt5
- Uvicorn

---

# Project Structure

```
Q-3
│
├── api
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── detector.py
│   ├── detect.py
│   ├── reports.py
│   ├── main.py
│   └── best.pt
│
├── results
│
├── ui
│   ├── egg_inspection.ui
│   └── main.py
│
├── requirements.txt
├── .env
└── README.md
```

---

# System Workflow

```
User Uploads Image
          │
          ▼
FastAPI (/detect)
          │
          ▼
Image Validation
          │
          ▼
YOLOv8 Detection
          │
          ▼
Egg Counting
          │
          ▼
Calculate Missing Eggs
          │
          ▼
PASS / FAIL Decision
          │
          ▼
Store Results in PostgreSQL
          │
          ▼
Save Annotated Image
          │
          ▼
Return JSON Response
          │
          ▼
Display Results in PyQt UI
```

---

# Database Schema

## inspections

Stores overall inspection information.

| Column | Description |
|---------|-------------|
| id | Primary Key |
| image_name | Uploaded image |
| expected_eggs | Expected tray count |
| detected_eggs | Eggs detected |
| missing_eggs | Missing eggs |
| status | PASS / FAIL |
| model_name | Detection model |
| inference_time | Detection time |

---

## detection_items

Stores every detected egg.

| Column | Description |
|---------|-------------|
| id | Primary Key |
| inspection_id | Foreign Key |
| class_name | Detected class |
| confidence | Detection confidence |
| x1,y1,x2,y2 | Bounding box coordinates |

Relationship

```
Inspection
      │
      │ 1
      │
      ▼
DetectionItem
      ▲
      │
      │ Many
```

---

# REST APIs

## Detect Eggs

```
POST /detect
```

Uploads an image and performs egg inspection.

Returns

- Detected eggs
- Missing eggs
- PASS / FAIL
- Inference time
- Annotated image
- Bounding boxes

---

## Inspection Report

```
GET /reports/{id}
```

Returns the complete inspection details for a specific inspection.

---

## Summary Report

```
GET /reports/summary
```

Returns defect statistics grouped using SQL aggregation.

---

## Health Check

```
GET /health
```

Checks whether the server is running.

---

# Installation

Clone the repository

```bash
git clone https://github.com/viswamanav/Automated-Egg-Tray-Inspection-Reporting-System.git

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Configure Environment

Create a `.env` file

```
DATABASE_URL=postgresql://postgres:password@localhost:5432/egg_db

MODEL_PATH=api/best.pt

EXPECTED_EGGS=25

CONFIDENCE=0.50
```

---

# Run PostgreSQL

Create a database

```
egg_db
```

---

# Run Backend

```bash
python -m uvicorn api.main:app --reload
```

Swagger Documentation

```
http://127.0.0.1:8000/docs
```

---

# Run Desktop Application

```bash
python ui/main.py
```

---

# Sample Inspection Flow

1. Select an egg tray image.
2. Click **Run Inspection**.
3. YOLO detects all eggs.
4. Egg count is calculated.
5. Missing eggs are identified.
6. PASS or FAIL status is generated.
7. Results are stored in PostgreSQL.
8. Annotated image is displayed in the UI.

---

# Example Response

```json
{
    "inspection_id": 15,
    "image_name": "tray.jpg",
    "expected_eggs": 25,
    "detected_eggs": 23,
    "missing_eggs": 2,
    "status": "FAIL",
    "model": "YOLOv8",
    "inference_time_ms": 112.4,
    "result_image": "results/inspection_15.jpg"
}
```

---

# Design Principles

- Modular project structure
- Separation of concerns
- SQLAlchemy ORM
- Configurable through environment variables
- RESTful API design
- Relational database schema
- One-to-Many relationship between inspections and detections

---

# Future Improvements

- Multi-class defect detection
- Live camera inspection
- Dashboard with analytics
- User authentication
- Docker support
- Batch image processing
- Export reports to PDF/Excel

---

# Author

**Viswamanav RS**

Computer Vision Engineer | AI & Machine Learning Developer

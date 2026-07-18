import os
import time
import cv2
import numpy as np

from ultralytics import YOLO

from api.config import MODEL_PATH, CONFIDENCE, EXPECTED_EGGS
from api.database import SessionLocal
from api.models import Inspection, DetectionItem

# Load YOLO model only once
model = YOLO(MODEL_PATH)


def inspect_image(image_bytes, filename):

    # Convert uploaded image to OpenCV format
    image = cv2.imdecode(
        np.frombuffer(image_bytes, np.uint8),
        cv2.IMREAD_COLOR
    )

    if image is None:
        return {
            "error": "Invalid image"
        }

    # ----------------------------
    # Run YOLO
    # ----------------------------

    start = time.time()

    results = model.predict(
        image,
        conf=CONFIDENCE,
        verbose=False
    )

    inference_time = (time.time() - start) * 1000

    # Draw bounding boxes on image
    annotated_image = results[0].plot()

    boxes = results[0].boxes

    detected_eggs = len(boxes)

    missing_eggs = max(0, EXPECTED_EGGS - detected_eggs)

    if missing_eggs == 0:
        status = "PASS"
    else:
        status = "FAIL"

    # ----------------------------
    # Save inspection to database
    # ----------------------------

    db = SessionLocal()

    inspection = Inspection(
        image_name=filename,
        expected_eggs=EXPECTED_EGGS,
        detected_eggs=detected_eggs,
        missing_eggs=missing_eggs,
        status=status,
        model_name="YOLOv8",
        inference_time=inference_time
    )

    db.add(inspection)
    db.commit()
    db.refresh(inspection)

    detections = []

    # Save every detected egg
    for box in boxes:

        x1, y1, x2, y2 = box.xyxy[0].tolist()

        confidence = float(box.conf[0])

        class_id = int(box.cls[0])
        class_name = model.names[class_id]

        detection = DetectionItem(
            inspection_id=inspection.id,
            class_name=class_name,
            confidence=confidence,
            x1=x1,
            y1=y1,
            x2=x2,
            y2=y2
        )

        db.add(detection)

        detections.append(
            {
                "class": class_name,
                "confidence": round(confidence, 2),
                "bbox": [x1, y1, x2, y2]
            }
        )

    db.commit()

    # ----------------------------
    # Save annotated image
    # ----------------------------

    output_file = f"inspection_{inspection.id}.jpg"

    output_path = os.path.join(
        "results",
        output_file
    )

    cv2.imwrite(
        output_path,
        annotated_image
    )

    inspection_id = inspection.id

    db.close()

    # ----------------------------
    # Return API response
    # ----------------------------

    return {

        "inspection_id": inspection_id,

        "image_name": filename,

        "expected_eggs": EXPECTED_EGGS,

        "detected_eggs": detected_eggs,

        "missing_eggs": missing_eggs,

        "status": status,

        "model": "YOLOv8",

        "inference_time_ms": round(inference_time, 2),

        "result_image": f"http://127.0.0.1:8000/results/{output_file}",

        "detections": detections

    }
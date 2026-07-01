"""
detector.py
YOLO Object Detection Module
"""

from ultralytics import YOLO
import pandas as pd

from config import (
    MODEL_PATH,
    CONFIDENCE_THRESHOLD
)


class SafetyDetector:
    """
    Wrapper around the YOLO model.
    Loads the model once and provides
    a simple detect() interface.
    """

    def __init__(self):

        self.model = YOLO(str(MODEL_PATH))

    def detect(self, image):

        results = self.model.predict(
            source=image,
            conf=CONFIDENCE_THRESHOLD,
            verbose=False
        )

        result = results[0]

        detections = []

        for box in result.boxes:

            cls_id = int(box.cls[0])

            class_name = self.model.names[cls_id]

            confidence = float(box.conf[0])

            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0].tolist()
            )

            detections.append({

                "class": class_name,

                "confidence": round(confidence, 3),

                "x1": x1,
                "y1": y1,
                "x2": x2,
                "y2": y2,

                "width": x2 - x1,
                "height": y2 - y1,

                "cx": (x1 + x2) // 2,
                "cy": (y1 + y2) // 2

            })

        columns = [
            "class",
            "confidence",
            "x1",
            "y1",
            "x2",
            "y2",
            "width",
            "height",
            "cx",
            "cy",
        ]

        df = pd.DataFrame(detections, columns=columns)

        return result, df

"""
logger.py
Construction Safety Event Logger
"""

import csv
from datetime import datetime
from pathlib import Path

from config import EVENT_LOG


class EventLogger:

    def __init__(self):

        self.log_file = Path(EVENT_LOG)

        if not self.log_file.exists():

            with open(self.log_file, "w", newline="") as f:

                writer = csv.writer(f)

                writer.writerow([
                    "Timestamp",
                    "Frame",
                    "PersonCount",
                    "Violation",
                    "Confidence",
                    "BoundingBox",
                    "Screenshot"
                ])

    def log(
        self,
        frame_number,
        person_count,
        violation,
        confidence,
        bbox,
        screenshot=""
    ):

        with open(self.log_file, "a", newline="") as f:

            writer = csv.writer(f)

            writer.writerow([

                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

                frame_number,
                
                person_count,

                violation,

                round(confidence, 3),

                str(bbox),

                screenshot

            ])

    def clear(self):

        if self.log_file.exists():

            self.log_file.unlink()

        self.__init__()

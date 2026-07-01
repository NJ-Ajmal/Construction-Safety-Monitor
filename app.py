
"""
app.py
Production-ready Construction Safety Monitor application.
"""

from __future__ import annotations

from config import (
    OUTPUT_DIR,
    SCREENSHOT_DIR,
    RED,
    GREEN,
    YELLOW,
    WHITE,
    PERSON_CLASS,
)

import numpy as np
import argparse
import sys
import time
from datetime import datetime
from pathlib import Path

import cv2

from config import (
    OUTPUT_DIR,
    SCREENSHOT_DIR,
    RED,
    GREEN,
    YELLOW,
    WHITE,
)
from detector import SafetyDetector
from violation_engine import ViolationEngine
from zone import RestrictedZoneChecker
from logger import EventLogger
from report import ReportGenerator


class ConstructionSafetyMonitor:
    def __init__(self, source=0):
        self.source = source
        self.detector = SafetyDetector()
        self.ppe = ViolationEngine()
        self.zone = RestrictedZoneChecker()
        self.logger = EventLogger()
        self.report = ReportGenerator()

        self.cap = cv2.VideoCapture(source)
        if not self.cap.isOpened():
            raise RuntimeError(f"Cannot open source: {source}")

        w = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 640)
        h = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 480)
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        if fps <= 1:
            fps = 30.0

        out_name = OUTPUT_DIR / f"output_{datetime.now():%Y%m%d_%H%M%S}.mp4"
        self.writer = cv2.VideoWriter(
            str(out_name),
            cv2.VideoWriter_fourcc(*"mp4v"),
            fps,
            (w, h),
        )
        self.frame_no = 0
        self.paused = False
        self.last_frame = None
        self.active_events = {}
        self.event_cooldown = 5.0      # seconds
        self.screenshot_cooldown = 3.0 # seconds
        self.last_screenshot_time = 0
        self.fps = 0.0

    def screenshot(self, frame):
        path = SCREENSHOT_DIR / f"frame_{self.frame_no:06d}.jpg"
        cv2.imwrite(str(path), frame)
        return str(path)

    def draw_zone(self, frame):

        pts = np.array(
            self.zone.get_polygon(),
            dtype=np.int32
        ).reshape((-1, 1, 2))

        cv2.polylines(
            frame,
            [pts],
            True,
            YELLOW,
            2
        )

    def process(self):
        last = time.time()
        try:
            while True:
                if not self.paused:
                    ok, frame = self.cap.read()
                    if not ok:
                        print("End of video stream or camera disconnected.")
                        break
                    self.frame_no += 1
                    self.last_frame = frame.copy()

                    result, df = self.detector.detect(frame)

                    frame = result.plot()

                    self.draw_zone(frame)
                    
                    # ---------- Dashboard Background ----------
                    overlay = frame.copy()

                    cv2.rectangle(
                        overlay,
                        (5, 5),
                        (250, 280),
                        (35, 35, 35),
                        -1
                    )

                    alpha = 0.55

                    frame = cv2.addWeighted(
                        overlay,
                        alpha,
                        frame,
                        1 - alpha,
                        0
                    )


                    violations = self.ppe.check(df)
                    violations.extend(self.zone.check(df))
                    
                    person_count = len(df[df["class"] == PERSON_CLASS])
                    
                    helmet_count = 0
                    vest_count = 0
                    zone_count = 0

                    for v in violations:

                        if v["type"] == "Helmet Violation":
                            helmet_count += 1

                        elif v["type"] == "Vest Violation":
                            vest_count += 1

                        elif v["type"] == "Restricted Zone":
                            zone_count += 1

                    current_time = time.time()

                    saved_this_frame = False
                    for v in violations:

                        x1, y1, x2, y2 = v["bbox"]

                        # Quantize coordinates to reduce detector jitter
                        cx = (x1 + x2) // 2
                        cy = (y1 + y2) // 2

                        key = (
                            v["type"],
                            cx // 40,
                            cy // 40
                        )

                        if key not in self.active_events:

                            screenshot_path = ""

                            if (
                                not saved_this_frame
                                and current_time - self.last_screenshot_time > self.screenshot_cooldown
                            ):

                                screenshot_path = self.screenshot(self.last_frame)

                                self.last_screenshot_time = current_time

                                saved_this_frame = True

                            self.logger.log(
                                self.frame_no,
                                person_count,
                                v["type"],
                                v["confidence"],
                                v["bbox"],
                                screenshot_path
                            )

                            self.active_events[key] = current_time

                        else:

                            self.active_events[key] = current_time

                        cv2.rectangle(frame, (x1, y1), (x2, y2), RED, 2)

                        cv2.putText(
                            frame,
                            v["type"],
                            (x1, max(20, y1 - 8)),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.6,
                            RED,
                            2
                        )

                    expired = []

                    for key, timestamp in self.active_events.items():

                        if current_time - timestamp > self.event_cooldown:

                            expired.append(key)

                    for key in expired:

                        del self.active_events[key]
                        
                        
                    now = time.time()

                    instant_fps = 1.0 / max(now - last, 1e-6)

                    self.fps = (
                        0.9 * self.fps +
                        0.1 * instant_fps
                    )

                    last = now
                    
                    overlay_x = 15
                    overlay_y = 35

                    cv2.putText(
                        frame,
                        f"FPS : {self.fps:.1f}",
                        (overlay_x, overlay_y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.65,
                        GREEN,
                        2,
                    )

                    overlay_y += 30

                    cv2.putText(
                        frame,
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        (10, overlay_y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.55,
                        WHITE,
                        2,
                    )

                    overlay_y += 30

                    cv2.putText(
                        frame,
                        f"Helmet : {helmet_count}",
                        (10, overlay_y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0,0,255),
                        2,
                    )

                    overlay_y += 30

                    cv2.putText(
                        frame,
                        f"Vest : {vest_count}",
                        (10, overlay_y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0,140,255),
                        2,
                    )

                    overlay_y += 30

                    cv2.putText(
                        frame,
                        f"Restricted Zone : {zone_count}",
                        (10, overlay_y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (255,0,255),
                        2,
                    )

                    overlay_y += 30

                    cv2.putText(
                        frame,
                        f"Active Events : {len(self.active_events)}",
                        (10, overlay_y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        WHITE,
                        2,
                    )
                    

                    overlay_y += 30

                    status = "PAUSED" if self.paused else "RUNNING"

                    status_color = YELLOW if self.paused else GREEN

                    cv2.putText(
                        frame,
                        f"Status : {status}",
                        (10, overlay_y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        status_color,
                        2,
                    )

                    overlay_y += 30

                    cv2.putText(
                        frame,
                        "Q:Quit  P:Pause  S:Screenshot",
                        (10, overlay_y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.55,
                        WHITE,
                        1,
                    )

                    self.writer.write(frame)
                    cv2.imshow("Construction Safety Monitor",frame)

                k=cv2.waitKey(1)&0xFF
                if k in (ord("q"),ord("Q")):
                    break
                elif k in (ord("p"),ord("P")):
                    self.paused=not self.paused
                elif k in (ord("s"),ord("S")) and self.last_frame is not None:
                    self.screenshot(self.last_frame)

        finally:
            self.cap.release()
            self.writer.release()
            cv2.destroyAllWindows()
            try:
                self.report.generate_csv_summary()
                self.report.generate_excel_report()
                self.report.print_statistics()
            except Exception as e:
                print(f"Report generation failed: {e}", file=sys.stderr)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--source",default="0",
                        help="Camera index or video file")
    args=parser.parse_args()
    src=int(args.source) if args.source.isdigit() else args.source
    try:
        ConstructionSafetyMonitor(src).process()
    except Exception as e:
        print(f"Fatal error: {e}",file=sys.stderr)
        sys.exit(1)

if __name__=="__main__":
    main()

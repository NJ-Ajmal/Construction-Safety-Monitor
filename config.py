"""
config.py
Global configuration for Construction Safety Monitor
"""

from pathlib import Path

# -----------------------------
# Project Paths
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "model" / "best.pt"

OUTPUT_DIR = BASE_DIR / "output"
LOG_DIR = BASE_DIR / "logs"
REPORT_DIR = BASE_DIR / "reports"
SCREENSHOT_DIR = BASE_DIR / "screenshots"

OUTPUT_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)
REPORT_DIR.mkdir(exist_ok=True)
SCREENSHOT_DIR.mkdir(exist_ok=True)

# -----------------------------
# Detection Settings
# -----------------------------

CONFIDENCE_THRESHOLD = 0.35

# Classes used by the model
PERSON_CLASS = "Person"
HELMET_CLASS = "Hardhat"
NO_HELMET_CLASS = "NO-Hardhat"
VEST_CLASS = "Safety Vest"
NO_VEST_CLASS = "NO-Safety Vest"

# -----------------------------
# Restricted Zone
# Coordinates are in image pixels.
# These can later come from the UI.
# -----------------------------

RESTRICTED_ZONE = [
    (380, 300),
    (640, 300),
    (640, 640),
    (380, 640)
]

# -----------------------------
# Drawing Colors (BGR)
# -----------------------------

GREEN = (0, 255, 0)
RED = (0, 0, 255)
BLUE = (255, 0, 0)
YELLOW = (0, 255, 255)
WHITE = (255, 255, 255)

# -----------------------------
# Logging
# -----------------------------

EVENT_LOG = LOG_DIR / "events.csv"

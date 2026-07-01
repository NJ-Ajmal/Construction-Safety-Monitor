"""
report.py
Professional Construction Safety Report Generator
"""

from pathlib import Path
from datetime import datetime

import pandas as pd

from config import (
    EVENT_LOG,
    REPORT_DIR
)


class ReportGenerator:

    def __init__(self):

        self.event_log = Path(EVENT_LOG)
        self.report_dir = Path(REPORT_DIR)

    def load(self):

        if not self.event_log.exists():
            return pd.DataFrame()

        try:
            return pd.read_csv(self.event_log)
        except Exception:
            return pd.DataFrame()

    def generate_csv_summary(self):

        df = self.load()

        if df.empty:
            print("No events found.")
            return

        summary = (
            df.groupby("Violation")
              .size()
              .reset_index(name="Count")
        )

        summary.to_csv(
            self.report_dir / "summary.csv",
            index=False
        )

        print("CSV Summary generated.")

    def generate_excel_report(self):

        df = self.load()

        if df.empty:
            print("No events found.")
            return

        # ----------------------------
        # Basic Statistics
        # ----------------------------

        total_events = len(df)

        helmet = (df["Violation"] == "Helmet Violation").sum()
        vest = (df["Violation"] == "Vest Violation").sum()
        zone = (df["Violation"] == "Restricted Zone").sum()

        if "PersonCount" in df.columns:

            total_workers = int(df["PersonCount"].max())

        else:

            total_workers = 0

        if total_workers > 0:

            compliance = max(
                0,
                (1 - violation_rate) * 100
            )

        else:

            compliance = 0

        # ----------------------------
        # Summary Table
        # ----------------------------

        summary = pd.DataFrame({

            "Metric": [

                "Report Generated",

                "Total Workers Detected",

                "Total Violations",

                "Helmet Violations",

                "Vest Violations",

                "Restricted Zone Violations",

                "Compliance Percentage"

            ],

            "Value": [

                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

                total_workers,

                total_events,

                helmet,

                vest,

                zone,

                f"{compliance:.2f}%"

            ]

        })

        # ----------------------------
        # Observations
        # ----------------------------

        observations = []

        if helmet >= max(vest, zone):

            observations.append(
                "Helmet violations are the most frequent."
            )

        if vest >= max(helmet, zone):

            observations.append(
                "Safety vest compliance requires improvement."
            )

        if zone > 0:

            observations.append(
                "Restricted zone entries were detected."
            )

        if compliance >= 90:

            observations.append(
                "Overall safety compliance is Excellent."
            )

        elif compliance >= 75:

            observations.append(
                "Overall safety compliance is Good."
            )

        elif compliance >= 50:

            observations.append(
                "Overall safety compliance is Moderate."
            )

        else:

            observations.append(
                "Overall safety compliance is Poor."
            )

        observations.append(
            "Continuous monitoring is recommended."
        )

        obs_df = pd.DataFrame({

            "Observations": observations

        })

        # ----------------------------
        # Violation Counts
        # ----------------------------

        violation_summary = (
            df.groupby("Violation")
              .size()
              .reset_index(name="Count")
        )

        output = self.report_dir / "Safety_Report.xlsx"

        with pd.ExcelWriter(output) as writer:

            df.to_excel(
                writer,
                sheet_name="Events",
                index=False
            )

            summary.to_excel(
                writer,
                sheet_name="Summary",
                index=False
            )

            violation_summary.to_excel(
                writer,
                sheet_name="Violation Counts",
                index=False
            )

            obs_df.to_excel(
                writer,
                sheet_name="Observations",
                index=False
            )

        print(f"Excel report saved to {output}")

    def print_statistics(self):

        df = self.load()

        if df.empty:

            print("\nNo events recorded.\n")
            return

        total_events = len(df)

        helmet = (df["Violation"] == "Helmet Violation").sum()
        vest = (df["Violation"] == "Vest Violation").sum()
        zone = (df["Violation"] == "Restricted Zone").sum()

        workers = 0

        if "PersonCount" in df.columns:

            workers = int(df["PersonCount"].max())

        compliance = 0

        if workers > 0:

            violation_rate = total_events / workers

            compliance = max(
                0,
                (1 - violation_rate) * 100
            )

        print("\n")
        print("=" * 50)
        print("CONSTRUCTION SAFETY REPORT")
        print("=" * 50)

        print(f"Workers Detected           : {workers}")
        print(f"Total Violations           : {total_events}")
        print(f"Helmet Violations          : {helmet}")
        print(f"Vest Violations            : {vest}")
        print(f"Restricted Zone Violations : {zone}")
        print(f"Compliance                 : {compliance:.2f}%")

        print("=" * 50)

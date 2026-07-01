"""
violation_engine.py
PPE Rule Engine
"""

from config import (
    PERSON_CLASS,
    NO_HELMET_CLASS,
    NO_VEST_CLASS
)


class ViolationEngine:

    def __init__(self):
        pass

    @staticmethod
    def _inside(person, obj):
        """Check whether an object's center lies inside a person's box."""

        return (
            person["x1"] <= obj["cx"] <= person["x2"]
            and person["y1"] <= obj["cy"] <= person["y2"]
        )

    def check(self, df):
        """
        Returns a list of detected violations.
        """

        violations = []

        persons = df[df["class"] == PERSON_CLASS].copy()

        if persons.empty:
            return violations

        # Smaller persons first
        persons["area"] = (
            (persons["x2"] - persons["x1"]) *
            (persons["y2"] - persons["y1"])
        )

        persons = persons.sort_values("area")

        # ----------------------------
        # Helmet Violations
        # ----------------------------

        for _, helmet in df[df["class"] == NO_HELMET_CLASS].iterrows():

            for _, person in persons.iterrows():

                if self._inside(person, helmet):

                    violations.append({

                        "type": "Helmet Violation",

                        "confidence": helmet["confidence"],

                        "bbox": (
                            int(person["x1"]),
                            int(person["y1"]),
                            int(person["x2"]),
                            int(person["y2"])
                        )

                    })

                    break

        # ----------------------------
        # Vest Violations
        # ----------------------------

        for _, vest in df[df["class"] == NO_VEST_CLASS].iterrows():

            for _, person in persons.iterrows():

                if self._inside(person, vest):

                    violations.append({

                        "type": "Vest Violation",

                        "confidence": vest["confidence"],

                        "bbox": (
                            int(person["x1"]),
                            int(person["y1"]),
                            int(person["x2"]),
                            int(person["y2"])
                        )

                    })

                    break

        return violations
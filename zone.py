"""
zone.py
Restricted Zone Detection
"""

from shapely.geometry import Point, Polygon

from config import (
    PERSON_CLASS,
    RESTRICTED_ZONE
)


class RestrictedZoneChecker:

    def __init__(self):

        self.zone = Polygon(RESTRICTED_ZONE)

    def check(self, df):

        violations = []

        persons = df[df["class"] == PERSON_CLASS]

        if persons.empty:
            return violations

        for _, person in persons.iterrows():

            center = Point(
                person["cx"],
                person["cy"]
            )

            if self.zone.contains(center):

                violations.append({

                    "type": "Restricted Zone",

                    "confidence": person["confidence"],

                    "bbox": (
                        int(person["x1"]),
                        int(person["y1"]),
                        int(person["x2"]),
                        int(person["y2"])
                    )

                })

        return violations

    def get_polygon(self):
        return RESTRICTED_ZONE
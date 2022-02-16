from __future__ import annotations
from renovation import RenovationModel


class School(RenovationModel["School"]):
    title: str

    def validate(self):
        self.address = self.address + " VALIDATED"

"""Class representing a Recursive State Machine"""
from pyformlang.cfg import Variable
from project.rsm_utils.rsm_box import Box


class RSM:
    """Recursive State Machine
    boxes = dictionary {number from 0: Box from rsm_box.py}"""

    def __init__(self, start_symbol: Variable, boxes: dict):
        self.start_symbol = start_symbol
        self.boxes = boxes

    def set_start_symbol(self, start_symbol: Variable):
        self.start_symbol = start_symbol

    def minimize(self):
        for box in self.boxes.values():
            box.minimize()
        return self

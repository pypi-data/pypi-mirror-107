#!/usr/bin/env python
# -*- coding: utf-8 -*-

# below codes copied from https://github.com/anntzer/redeal/blob/master/redeal/redeal.py with GPL-3.0 License
from enum import Enum

Strain = Enum("Strain", zip("CDHSN", range(5)))

class Contract:
    def __init__(self, level, strain, doubled=0, vul=False):
        if not (1 <= level <= 7 and hasattr(Strain, strain) and
                0 <= doubled <= 2):
            raise ValueError("Invalid contract")
        self.level = level
        self.strain = strain
        self.doubled = doubled
        self.vul = vul

    @classmethod
    def from_str(cls, s, vul=False):
        """
        Initialize with a string, e.g. "7NXX".  Vulnerability still a kwarg.
        """
        doubled = len(s) - len(s.rstrip("X"))
        return cls(int(s[0]), s[1], doubled=doubled, vul=vul)

    def score(self, tricks):
        """Score for a contract for a given number of tricks taken."""
        target = self.level + 6
        overtricks = tricks - target
        if overtricks >= 0:
            per_trick = 20 if self.strain in ["C", "D"] else 30
            base_score = per_trick * self.level
            bonus = 0
            if self.strain == "N":
                base_score += 10
            if self.doubled == 1:
                base_score *= 2
                bonus += 50
            if self.doubled == 2:
                base_score *= 4
                bonus += 100
            bonus += [300, 500][self.vul] if base_score >= 100 else 50
            if self.level == 6:
                bonus += [500, 750][self.vul]
            elif self.level == 7:
                bonus += [1000, 1500][self.vul]
            if not self.doubled:
                per_overtrick = per_trick
            else:
                per_overtrick = [100, 200][self.vul] * self.doubled
            overtricks_score = overtricks * per_overtrick
            return base_score + overtricks_score + bonus
        else:
            if not self.doubled:
                per_undertrick = [50, 100][self.vul]
                return overtricks * per_undertrick
            else:
                if overtricks == -1:
                    score = [-100, -200][self.vul]
                elif overtricks == -2:
                    score = [-300, -500][self.vul]
                else:
                    score = 300 * overtricks + [400, 100][self.vul]
            if self.doubled == 2:
                score *= 2
            return score

def matchpoints(my, other):
    """Return matchpoints scored (-1 to 1) given our and their result."""
    return (my > other) - (my < other)

def imps(my, other):
    """Return IMPs scored given our and their results."""
    imp_table = [
        15, 45, 85, 125, 165, 215, 265, 315, 365, 425, 495, 595, 745, 895,
        1095, 1295, 1495, 1745, 1995, 2245, 2495, 2995, 3495, 3995]
    return bisect(imp_table, abs(my - other)) * (1 if my > other else -1)

# Above codes copied from https://github.com/anntzer/redeal/blob/master/redeal/redeal.py with GPL-3.0 License

# for 1-16 boards
# https://tedmuller.us/Bridge/Esoterica/BoardVulnerability.htm
board_vul= "ONEBNEBOEBONBONE"
vul_table={"O": "None", "N": "N-S", "E": "E-W", "B": "Both"}
vul_maptable={"O": "", "N": "NS", "E":"EW", "B": "NSEW"}  # maptable to check based on declarer
# https://www.ebu.co.uk/laws-and-ethics/vp-scales
vp_scale_8boards=[  10.00,10.44,10.86,11.27,11.67,12.05,12.42,12.77,13.12,13.45,  # 0-9
                    13.78,14.09,14.39,14.68,14.96,15.23,15.50,15.75,16.00,16.23,
                    16.46,16.68,16.90,17.11,17.31,17.50,17.69,17.87,18.04,18.21,
                    18.37,18.53,18.68,18.83,18.97,19.11,19.24,19.37,19.50,19.62,
                    19.74,19.85,19.95,20.00 ]
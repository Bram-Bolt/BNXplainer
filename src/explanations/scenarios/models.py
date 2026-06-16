# Copyright (c) 2026 MSDT Group 2 All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

"""Data containers used by scenario explanation generation and rendering."""

from dataclasses import dataclass

@dataclass
class ScenarioNode:
    """One variable assignment considered inside a generated scenario."""

    name: str
    value: str
    prob: float

@dataclass
class FullScenario:
    """Rendered scenario explanation with probability and supporting notes."""

    probability: float
    scenario: str
    implausible: list[str]
    supporting: list[str]
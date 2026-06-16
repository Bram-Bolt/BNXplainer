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
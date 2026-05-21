from dataclasses import dataclass

@dataclass
class ScenarioNode:
    name: str
    value: str
    prob: float

@dataclass
class FullScenario:
    probability: float
    scenario: str
    implausible: list[str]
    supporting: list[str]
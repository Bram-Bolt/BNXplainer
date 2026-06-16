"""Build text-ready scenario explanation objects from ranked assignments."""

from dataclasses import dataclass
from itertools import product
from explanations.scenarios.n_possible_explanations import most_probable_scenarios
from explanations.scenarios.text_generation import build_scenario_from_explanation
import pyagrum as gum

def get_scenarios(bn, target: str, evidence, n_scenarios):
    """Return FullScenario objects for the top probable target scenarios."""
    expls = most_probable_scenarios(
            bn=bn,
            target=target,
            evidence=evidence,
            n_scenarios=3,
        )

    scenarios = []
    for expl in expls:
        scenarios.append(build_scenario_from_explanation(bn, expl["assignment"], expl["probability"],expl["target"]))

    return scenarios
"""Tests for ranking probable scenario explanations."""

from pathlib import Path
import sys

import pyagrum as gum

sys.path.append(str(Path(__file__).resolve().parents[1]))
from explanations.scenarios.n_possible_explanations import most_probable_scenarios

def load_cancer_bn():
    """Load the bundled cancer Bayesian network fixture."""
    return gum.loadBN("src/example_bns/cancer.net")


def test_most_probable_scenarios_defaults_to_parents_plus_target():
    """Default scenario scope contains target parents followed by target."""
    bn = load_cancer_bn()

    scenarios = most_probable_scenarios(bn, target="Cancer")

    assert list(scenarios[0]["assignment"]) == ["Pollution", "Smoker", "Cancer"]


def test_most_probable_scenarios_returns_top_n_sorted_by_probability():
    """Scenario search returns the requested top ranks in descending order."""
    bn = load_cancer_bn()

    scenarios = most_probable_scenarios(bn, target="Cancer", n_scenarios=3)

    assert len(scenarios) == 3
    assert [scenario["rank"] for scenario in scenarios] == [1, 2, 3]
    assert [scenario["probability"] for scenario in scenarios] == sorted(
        [scenario["probability"] for scenario in scenarios],
        reverse=True,
    )


def test_most_probable_scenarios_returns_label_assignments():
    """Scenario assignments are returned as readable state labels."""
    bn = load_cancer_bn()

    scenarios = most_probable_scenarios(bn, target="Cancer", n_scenarios=1)

    assert scenarios[0]["assignment"] == {
        "Pollution": "low",
        "Smoker": "False",
        "Cancer": "False",
    }
    assert scenarios[0]["target"] == "Cancer"
    assert scenarios[0]["target_state"] == "False"
    assert scenarios[0]["probability"] == 0.62937


def test_most_probable_scenarios_includes_conditional_target_probability():
    """Each scenario includes the target probability under its conditions."""
    bn = load_cancer_bn()

    scenarios = most_probable_scenarios(bn, target="Cancer", n_scenarios=1)

    assert scenarios[0]["target_probability"] == 0.999


def test_most_probable_scenarios_applies_evidence():
    """Submitted evidence is reflected in every returned scenario assignment."""
    bn = load_cancer_bn()

    scenarios = most_probable_scenarios(
        bn,
        target="Cancer",
        evidence={"Smoker": "False"},
        n_scenarios=3,
    )

    assert all(
        scenario["assignment"]["Smoker"] == "False"
        for scenario in scenarios
    )


def test_most_probable_scenarios_appends_target_to_custom_nodes():
    """Custom scenario scopes still include the target node."""
    bn = load_cancer_bn()

    scenarios = most_probable_scenarios(
        bn,
        target="Cancer",
        scenario_nodes=["Pollution"],
        n_scenarios=1,
    )

    assert list(scenarios[0]["assignment"]) == ["Pollution", "Cancer"]

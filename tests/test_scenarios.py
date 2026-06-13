from pathlib import Path
import sys

import pyagrum as gum

sys.path.append(str(Path(__file__).resolve().parents[1]))
from explanations.scenarios.n_possible_explanations import most_probable_scenarios

def load_cancer_bn():
    return gum.loadBN("src/example_bns/cancer.net")


def test_most_probable_scenarios_defaults_to_parents_plus_target():
    bn = load_cancer_bn()

    scenarios = most_probable_scenarios(bn, target="Cancer")

    assert list(scenarios[0]["assignment"]) == ["Pollution", "Smoker", "Cancer"]


def test_most_probable_scenarios_returns_top_n_sorted_by_probability():
    bn = load_cancer_bn()

    scenarios = most_probable_scenarios(bn, target="Cancer", n_scenarios=3)

    assert len(scenarios) == 3
    assert [scenario["rank"] for scenario in scenarios] == [1, 2, 3]
    assert [scenario["probability"] for scenario in scenarios] == sorted(
        [scenario["probability"] for scenario in scenarios],
        reverse=True,
    )


def test_most_probable_scenarios_returns_label_assignments():
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
    bn = load_cancer_bn()

    scenarios = most_probable_scenarios(bn, target="Cancer", n_scenarios=1)

    assert scenarios[0]["target_probability"] == 0.999


def test_most_probable_scenarios_applies_evidence():
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
    bn = load_cancer_bn()

    scenarios = most_probable_scenarios(
        bn,
        target="Cancer",
        scenario_nodes=["Pollution"],
        n_scenarios=1,
    )

    assert list(scenarios[0]["assignment"]) == ["Pollution", "Cancer"]

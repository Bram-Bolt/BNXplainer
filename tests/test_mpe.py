
import math

import pytest
import pyagrum as gum

from explanations.mpe import (
    compute_mpe,
    mpe_to_display,
)


def build_test_bn() -> gum.BayesNet:
    """
    Create a simple Bayesian Network:

        Rain -> WetGrass
    """

    bn = gum.BayesNet("Weather")

    # Create variables
    rain_var = gum.LabelizedVariable("Rain", "Rain", 0)
    rain_var.addLabel("no")
    rain_var.addLabel("yes")

    wet_var = gum.LabelizedVariable("WetGrass", "Wet grass", 0)
    wet_var.addLabel("dry")
    wet_var.addLabel("wet")

    rain = bn.add(rain_var)
    wet = bn.add(wet_var)

    bn.addArc(rain, wet)

    # P(Rain)
    bn.cpt(rain)[:] = [0.7, 0.3]

    # P(WetGrass | Rain=no)
    bn.cpt(wet)[{"Rain": 0}] = [0.9, 0.1]

    # P(WetGrass | Rain=yes)
    bn.cpt(wet)[{"Rain": 1}] = [0.2, 0.8]

    return bn

def test_compute_mpe_without_evidence():
    """
    Test MPE with no evidence.

    Expected:
        Rain = no
        WetGrass = dry

    Joint probability:
        0.7 * 0.9 = 0.63
    """

    bn = build_test_bn()

    result = compute_mpe(bn, evidence={})

    assert result["result"] == {
        "Rain": "no",
        "WetGrass": "dry",
    }

    assert math.isclose(result["probability"], 0.63, rel_tol=1e-6)


def test_compute_mpe_with_evidence():
    """
    Evidence:
        WetGrass = wet

    Most probable explanation should be:
        Rain = yes
        WetGrass = wet

    Because:
        P(yes, wet) = 0.3 * 0.8 = 0.24
        P(no, wet)  = 0.7 * 0.1 = 0.07
    """

    bn = build_test_bn()

    result = compute_mpe(
        bn,
        evidence={"WetGrass": 1},
    )

    assert result["result"] == {
        "Rain": "yes",
        "WetGrass": "wet",
    }

    assert math.isclose(result["probability"], 0.24, rel_tol=1e-6)


def test_compute_mpe_exclude_evidence():
    """
    Test include_evidence=False removes evidence variables.
    """

    bn = build_test_bn()

    result = compute_mpe(
        bn,
        evidence={"WetGrass": 1},
        include_evidence=False,
    )

    assert result["result"] == {
        "Rain": "yes",
    }

    assert "WetGrass" not in result["result"]


def test_compute_mpe_include_evidence():
    """
    Test include_evidence=True keeps evidence variables.
    """

    bn = build_test_bn()

    result = compute_mpe(
        bn,
        evidence={"WetGrass": 1},
        include_evidence=True,
    )

    assert result["result"] == {
        "Rain": "yes",
        "WetGrass": "wet",
    }


def test_probability_is_float():
    """
    Probability should always be a float.
    """

    bn = build_test_bn()

    result = compute_mpe(bn, evidence={})

    assert isinstance(result["probability"], float)


def test_mpe_to_display():
    """
    Test frontend conversion helper.
    """

    mpe_output = {
        "result": {
            "Rain": "yes",
            "WetGrass": "wet",
        },
        "probability": 0.24,
    }

    display = mpe_to_display(mpe_output)

    assert display == [
        {
            "variable": "Rain",
            "state": "yes",
        },
        {
            "variable": "WetGrass",
            "state": "wet",
        },
    ]


def test_mpe_to_display_empty():
    """
    Empty results should return empty list.
    """

    mpe_output = {
        "result": {},
        "probability": 1.0,
    }

    display = mpe_to_display(mpe_output)

    assert display == []


def test_invalid_variable_raises():
    """
    Invalid evidence variable should raise an exception.
    """

    bn = build_test_bn()

    with pytest.raises(Exception):
        compute_mpe(
            bn,
            evidence={"DoesNotExist": 1},
        )


def test_invalid_state_raises():
    """
    Invalid state index should raise an exception.
    """

    bn = build_test_bn()

    with pytest.raises(Exception):
        compute_mpe(
            bn,
            evidence={"Rain": 99},
        )


def test_result_contains_all_variables_without_evidence():
    """
    Without evidence, all variables should be present.
    """

    bn = build_test_bn()

    result = compute_mpe(bn, evidence={})

    assert set(result["result"].keys()) == {
        "Rain",
        "WetGrass",
    }


def test_result_structure():
    """
    Verify API structure consistency.
    """

    bn = build_test_bn()

    result = compute_mpe(bn, evidence={})

    assert isinstance(result, dict)

    assert "result" in result
    assert "probability" in result

    assert isinstance(result["result"], dict)
    assert isinstance(result["probability"], float)

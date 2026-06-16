"""Compute most probable explanation assignments with pyAgrum."""

import pyagrum as gum
from typing import Dict

def compute_mpe(
    bn: gum.BayesNet,
    evidence: Dict[str, str],
    include_evidence: bool = True
) -> dict:
    """
    Compute the Most Probable Explanation (MPE).

    Finds the most probable joint assignment of all variables given the
    evidence, then converts state indexes to readable state labels.

    Args:
        bn: Bayesian network to explain.
        evidence: Observed variables accepted by pyAgrum's evidence API.
        include_evidence: Whether to keep observed variables in the result.

    Returns:
        Dictionary with ``result`` mapping variable names to state labels and
        ``probability`` containing the rounded joint probability.
    """

    # Create inference engine
    ie = gum.LazyPropagation(bn)

    # Set evidence
    ie.setEvidence(evidence)

    # Compute TRUE MPE (joint assignment)
    mpe_instantiation = ie.mpe()
    # Convert result to readable format using pyAgrum's built-in todict()
    raw_result = mpe_instantiation.todict()

    result = {
        var_name: bn.variable(var_name).label(state_index)
        for var_name, state_index in raw_result.items()
    }
 
    # Optionally remove evidence variables
    if not include_evidence:
        result = {
            var: val for var, val in result.items()
            if var not in evidence
        }

    # Compute joint probability of the MPE assignment
    probability = bn.jointProbability(mpe_instantiation)

    return {
        "result": result,
        "probability": round(float(probability), 6)
    }


def mpe_to_display(mpe_output: dict) -> list:
    """Transform MPE output to proper format for displaying.

    Args:
        mpe_output (dict): MPE output from compute_mpe().

    Returns:
        list: MPE assignment rows with variable names and state labels.
    """
    return [
        {
            "variable": variable,
            "state": state,
        }
        for variable, state in mpe_output["result"].items()
    ]
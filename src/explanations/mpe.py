import pyagrum as gum
from typing import Dict


def compute_mpe(
    bn: gum.BayesNet,
    evidence: Dict[str, int],
    include_evidence: bool = True
) -> dict:
    """
    Compute the Most Probable Explanation (MPE).

    Finds the most probable joint assignment of ALL variables
    given the evidence.

    Parameters
    ----------
    bn : gum.BayesNet
        The Bayesian Network.
    evidence : Dict[str, int]
        Observed variables as {variable_name: state_index}.
    include_evidence : bool
        Whether to include evidence variables in the output.

    Return
    -------
    dict
        {
            "result": {variable_name: state_label},
            "probability": float
        }
    """

    # Create inference engine
    ie = gum.LazyPropagation(bn)

    # Set evidence
    ie.setEvidence(evidence)

    # Compute TRUE MPE (joint assignment)
    mpe_instantiation = ie.mpe()

    # Convert result to readable format
    result = {}
    for node_id in mpe_instantiation.keys():
        variable = bn.variable(node_id)
        node_name = variable.name()
        state_index = mpe_instantiation[node_id]
        state_label = variable.label(state_index)

        result[node_name] = state_label

    # Optionally remove evidence variables
    if not include_evidence:
        result = {
            var: val for var, val in result.items()
            if var not in evidence
        }

    # Compute joint probability of the MPE assignment
    probability = ie.jointProbability(mpe_instantiation)

    return {
        "result": result,
        "probability": round(float(probability), 6)
    }


def mpe_to_display(mpe_output: dict) -> list:
    """
    Convert MPE result into a frontend-friendly format.

    Parameters
    -----
    mpe_output : dict
        Output from compute_mpe()

    Returns
    ------ 
    list of dicts
        [{"variable": ..., "state": ...}, ...]
    """
    return [
        {"variable": var, "state": state}
        for var, state in mpe_output["result"].items()
    ]
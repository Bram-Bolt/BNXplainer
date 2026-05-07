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
    mpe_str = str(mpe_instantiation)
    # <Smoker:False|Cancer:False|Pollution:low|Xray:negative|Dyspnoea:False>

    # Convert result to readable format
    result = {}

    stripped_str = mpe_str[1:-1].split("|")
    for s in stripped_str:
        split_str = s.split(":")
        node = split_str[0]
        most_probable_state = split_str[1]
        result[node] = most_probable_state

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


# def mpe_to_display(mpe_output: dict) -> list:
#     """
#     Convert MPE result into a frontend-friendly format.

#     Parameters
#     -----
#     mpe_output : dict
#         Output from compute_mpe()

#     Returns
#     ------ 
#     list of dicts
#         [{"variable": ..., "state": ...}, ...]
#     """
#     return mpe_output["result"]
import pyagrum as gum
from typing import Dict


def compute_mpe(
    bn: gum.BayesNet,
    evidence: Dict[str, str],
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
    evidence : Dict[str, str]
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
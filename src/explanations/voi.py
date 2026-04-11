import math
import pyagrum as gum
from typing import Optional


def entropy(probabilities: list) -> float:
    """Calculate entropy of list of floats

    Args:
        probabilities (list): List of probabilities of distinct events

    Returns:
        float: Entropy of the input list
    """
    return -sum(p * math.log2(p) for p in probabilities if p > 0)


def compute_voi(
    bn: gum.BayesNet,
    target: str,
    evidence: dict,
    candidates: Optional[list] = None
) -> dict:
    """Value of Information explanation method

    Args:
        bn (gum.BayesNet): Input Bayesian Network
        target (str): Name of target variable
        evidence (dict): Dictionary of existing evidence
        candidates (Optional[list], optional): Optional variable, list of candidate states. Defaults to None.

    Returns:
        dict: sorted dictionary of states and their VOI scores.
    """
    # Instantiate variables
    ie = gum.LazyPropagation(bn)
    ie.setEvidence(evidence)
    ie.makeInference()

    # Calculate the posterior of the target variable
    target_posterior = [
        ie.posterior(target)[{target: i}]
        for i in range(bn.variable(target).domainSize())
    ]
    h_target = entropy(target_posterior)

    # Set observed variable(s)
    observed = set(evidence.keys()) | {target}
    if candidates is None:
        candidates = [
            bn.variable(i).name()
            for i in bn.nodes()
            if bn.variable(i).name() not in observed
        ]

    voi_scores = {}

    # Calculate VOI scores
    for var in candidates:
        var_size = bn.variable(var).domainSize()
        expected_conditional_entropy = 0.0

        for state in range(var_size):
            hypothetical_evidence = {**evidence, var: state}
            ie2 = gum.LazyPropagation(bn)
            ie2.setEvidence(hypothetical_evidence)
            ie2.makeInference()

            p_state = ie.posterior(var)[{var: state}]
            if p_state == 0:
                continue

            cond_probs = [
                ie2.posterior(target)[{target: i}]
                for i in range(bn.variable(target).domainSize())
            ]
            expected_conditional_entropy += p_state * entropy(cond_probs)

        voi_scores[var] = h_target - expected_conditional_entropy

    return dict(sorted(voi_scores.items(), key=lambda x: x[1], reverse=True))


def voi_to_display(voi_scores: dict) -> list:
    """Transform VOI scores to proper format for displaying

    Args:
        voi_scores (dict): VOI scores from compute_voi() method

    Returns:
        list: return voi_scores in proper format
    """
    return [
        {
            "variable": var,
            "evpi": round(score, 4),
            "label": f"{var} (EVPI: {score:.4f} bits)"
        }
        for var, score in voi_scores.items()
    ]
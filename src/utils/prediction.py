"""Compute posterior prediction summaries for target variables."""

import pyagrum as gum


def compute_prediction(
    bn: gum.BayesNet,
    target: str,
    evidence: dict
) -> dict:
    """Compute a target variable's posterior distribution under evidence.

    Args:
        bn: Bayesian network used for inference.
        target: Name of the target variable to predict.
        evidence: Current evidence passed to pyAgrum.

    Returns:
        Target name, state labels, posterior probabilities, most likely state,
        and that state's posterior probability.
    """
    ie = gum.LazyPropagation(bn)
    ie.setEvidence(evidence)
    ie.makeInference()

    variable = bn.variable(target)
    n_states = variable.domainSize()
    states = list(variable.labels())

    # Calculate posterior probability distribution
    probs = [
        ie.posterior(target)[{target: i}]
        for i in range(n_states)
    ]

    # Polish posteriors
    probabilities = {
        state: round(prob, 6)
        for state, prob in zip(states, probs)
    }

    best_index = probs.index(max(probs))

    return {
        "target": target,
        "states": states,
        "probabilities": probabilities,
        "most_likely_state": states[best_index],
        "most_likely_probability": round(probs[best_index], 6)
    }
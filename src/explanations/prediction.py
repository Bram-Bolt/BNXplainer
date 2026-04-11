import pyagrum as gum


def compute_prediction(
    bn: gum.BayesNet,
    target: str,
    evidence: dict
) -> dict:
    """Computes Prediction in a Bayesian Network

    Args:
        bn (gum.BayesNet): Bayesian Network
        target (str): Name of target variable
        evidence (dict): Current evidence

    Returns:
        dict: returns target, states, 
        probabilities of states, most likely state,
        and most likely probability of that state.
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
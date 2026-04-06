import pyagrum as gum


def compute_prediction(
    bn: gum.BayesNet,
    target: str,
    evidence: dict
) -> dict:
    ie = gum.LazyPropagation(bn)
    ie.setEvidence(evidence)
    ie.makeInference()

    variable = bn.variable(target)
    n_states = variable.domainSize()
    states = list(variable.labels())

    probs = [
        ie.posterior(target)[{target: i}]
        for i in range(n_states)
    ]

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
import pyagrum as gum
from itertools import product
def _default_scenario_nodes(bn: gum.BayesNet, target: str) -> list[str]:
    target_id = bn.idFromName(target)
    parents = [
        bn.variable(parent_id).name()
        for parent_id in bn.parents(target_id)
    ]
    return [*parents, target]


def _unique_nodes(nodes: list[str]) -> list[str]:
    unique = []
    for node in nodes:
        if node not in unique:
            unique.append(node)
    return unique


def _target_probability_given_scenario(
    bn: gum.BayesNet,
    target: str,
    target_state: str,
    evidence: dict[str, str | int | bool | list[float]],
    assignment: dict[str, str],
) -> float:
    conditional_evidence = dict(evidence)
    for node, state in assignment.items():
        if node != target:
            conditional_evidence[node] = state

    ie = gum.LazyPropagation(bn)
    if conditional_evidence:
        ie.setEvidence(conditional_evidence)
    ie.makeInference()

    target_state_index = bn.variable(target).index(target_state)
    return float(ie.posterior(target)[{target: target_state_index}])


def most_probable_scenarios(
    bn: gum.BayesNet,
    target: str,
    evidence: dict[str, str | int | bool | list[float]] | None = None,
    *,
    n_scenarios: int = 3,
    scenario_nodes: list[str] | None = None,
) -> list[dict]:
    """Return the most probable assignments for the scenario nodes.

    By default, a scenario contains the direct parents of the target and the
    target itself. The returned probabilities are P(scenario_nodes | evidence).
    """
    if n_scenarios <= 0:
        return []

    evidence = evidence or {}
    if scenario_nodes is None:
        nodes = _default_scenario_nodes(bn, target)
    else:
        nodes = [*scenario_nodes, target]
    nodes = _unique_nodes(nodes)

    ie = gum.LazyPropagation(bn)
    if evidence:
        ie.setEvidence(evidence)
    ie.makeInference()

    joint = ie.jointPosterior(set(nodes))
    scored_scenarios = []

    state_ranges = [
        range(bn.variable(node).domainSize())
        for node in nodes
    ]
    for state_indexes in product(*state_ranges):
        index_assignment = dict(zip(nodes, state_indexes))
        probability = float(joint[index_assignment])
        assignment = {
            node: bn.variable(node).label(state_index)
            for node, state_index in index_assignment.items()
        }
        scored_scenarios.append((probability, assignment))

    scored_scenarios.sort(key=lambda item: item[0], reverse=True)

    return [
        {
            "rank": rank,
            "assignment": assignment,
            "probability": round(probability, 6),
            "target": target,
            "target_state": assignment[target],
            "target_probability": round(
                _target_probability_given_scenario(
                    bn,
                    target,
                    assignment[target],
                    evidence,
                    assignment,
                ),
                6,
            ),
        }
        for rank, (probability, assignment)
        in enumerate(scored_scenarios[:n_scenarios], start=1)
    ]


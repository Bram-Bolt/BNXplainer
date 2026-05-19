from dataclasses import dataclass
from itertools import product

import pyagrum as gum

@dataclass
class ScenarioNode:
    name: str
    value: str
    prob: float

@dataclass
class FullScenario:
    probability: float
    scenario: str
    implausible: list[str]
    supporting: list[str]


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


def build_scenario_from_explanation(
    bn: gum.BayesNet,
    possible_explanation: dict[str, str],
    joint_prob: float,
    target: str,
) -> FullScenario:
    
    fs = FullScenario(
        probability=joint_prob,
        scenario="",
        implausible=[],
        supporting=[]
    )

    ie = gum.LazyPropagation(bn)
    ie.makeInference()

    elements = []
    for node_name, node_value in possible_explanation.items():
        # get probability of node
        posterior = ie.posterior(node_name)
        var = bn.variable(node_name)
        value_index = var.index(node_value)
        prob = posterior[value_index]
        
        # build node
        node = ScenarioNode(
            name=node_name,
            value=node_value,
            prob=prob
        )
        
        # classify node, 
        # TODO: correct classifcation!!!!!!
        # maybe add a function for this?
        
        treshold = 0.5
        if node_name != target:
            elements.append(node)

            # classify node
            if prob <= treshold:
                fs.implausible.append(generate_implausible_sentence(node))   

            elif prob > treshold:
                fs.supporting.append(generate_supporting_sentence(node))
         
        else:
            target_node = node
      
    fs.scenario = generate_target_outcome(elements, target_node)
    return fs


def generate_target_outcome(elements: list[ScenarioNode], target: ScenarioNode) -> str:

    scenario = ""

    for i, node in enumerate(elements):
        #prob_str = prob_to_str(node.prob)

        if i == len(elements) - 1 and i != 0:
            scenario += f"and {node.name} being {node.value}"
        else:
            scenario += f"With {node.name} being {node.value}"

            if i < len(elements) - 2:
                scenario += ", "
            elif i == len(elements) - 2:
                scenario += " "
        
    scenario += "\n"
    
    scenario += f"{target.name} is {prob_to_str(target.prob)} likely to be {target.value}."
    return scenario



# convert numerical probabilities to string
def prob_to_str(prob: float) -> str:
    if prob >= 0.99:
        return "extremely strongly"
    if prob > 0.90:
        return "very strongly"
    if prob > 0.70:
        return "strongly"
    if prob > 0.50:
        return "moderately"
    if prob > 0.30:
        return "weakly"
    if prob > 0.10:
        return "very weakly"
    return "very weakly"


# implausible evidence
def generate_implausible_sentence(node: ScenarioNode)-> str: 
    prob = prob_to_str(node.prob)
    sentence = f"{node.name} being {node.value} is {prob} unlikely"
    return sentence

# supporting elements
def generate_supporting_sentence(node: ScenarioNode)->str:
    prob = prob_to_str(node.prob)
    sentence = f"{prob} supported by {node.name} being {node.value}"
    return sentence



def print_full_scenario(fs: FullScenario) -> None:
    print("=== Full Scenario ===")
    print(f"Probability : {fs.probability:.6f}")
    print("\nScenario:")
    print(fs.scenario)

    print("\nImplausible:")
    if fs.implausible:
        for item in fs.implausible:
            print(f"  - {item}")
    else:
        print("  None")

    print("\nSupporting:")
    if fs.supporting:
        for item in fs.supporting:
            print(f"  - {item}")
    else:
        print("  None")
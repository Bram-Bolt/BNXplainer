from explanations.scenarios.models import FullScenario, ScenarioNode
import pyagrum as gum
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

    # get value of target
    for node_name, node_value in possible_explanation.items():
        if node_name == target:
            target_value = node_value
            break
    
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
        
        if node_name != target:
            elements.append(node)

            # classify node
            if supports_target(bn,node_name,node_value,target,target_value):
                fs.supporting.append(generate_supporting_sentence(node))

            elif not supports_target(bn,node_name,node_value,target,target_value):
                fs.implausible.append(generate_implausible_sentence(node)) 
         
        else:
            target_node = node

    return fs


def supports_target(bn:gum.BayesNet,node_name,node_value, target_node,target_value:str):
    """
    Function that returns True if the inspected node and its state/value supports the target's
    state/value in the Scenario. Else it returns False.
    """
    supporting_state = None

    # inspected node
    node = bn.variable(node_name)
    target_node = bn.variable(target_node)
    target_value_idx = target_node[target_value]
    node_value_idx = node[node_value]

    # Get the CPT for the target node
    cpt = bn.cpt(target_node.name())

    max_prob = -1

    # Iterate over the states of the parent node
    for state_idx in range(node.domainSize()):
        # Get the probability of Target=target_state given inspected node
        prob = cpt[state_idx][target_value_idx]
        if prob > max_prob:
            max_prob = prob
            supporting_state = state_idx

    print(f"The supporting value of {node.name()} for target={target_value} is: {node.domain()[supporting_state]}\n")
    return supporting_state == node_value_idx


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

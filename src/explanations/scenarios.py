import pyagrum as gum
from dataclasses import dataclass

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
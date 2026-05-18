
import pyagrum as gum
from dataclasses import dataclass

@dataclass
class FullScenario:
    probability: int
    scenario: str
    implausible: list[str]
    supporting: list[str]
    
    

def build_scenario_from_mpe(bn: gum.BayesNet, mpe: dict[str, str], joint_prob: int) -> FullScenario:
    fs = FullScenario(probability=joint_prob, scenario="", implausible=[],supporting=[])
    
    # also filter for target!
    fs.scenario = generate_target_outcome(elements)
    for node in mpe:
        if node is implausible:
            fs.implausible.append(node)
        elif node is supporting:
            fs.implausible.append(node)
    return fs
  
def generate_target_outcome(elements):
    # scenario = ""
    # for node in elements
       # scenario +=node.node_name being node.value is prob_to_str(node.prob) and
    
    # if node is target:
        # scenario += then node.node_name is prob_to_str(node.prob) to be node.value
    return "not yet implemented"
    
       
# convert numerical probabilities to sring
def prob_to_str(prob: int):
    if prob == 100:
        return "100%"
    if prob > 90:
        return "very strongly"
    if prob > 70:
        return "strongly"
    return "idk yet who wants to fill this in?"

# supporting evidence
def generate_implausible_sentence(node)-> str:
    prob = prob_to_str(node.prob)
    sentence = f"{node.name} being {node.value} is {prob} unlikely"
    return sentence

# implausible elements
def generate_supporting_sentence(node)->str:
    prob = prob_to_str(node.prob)
    sentence = f"{prob} supported by {node.name} being {node.value}"
    return sentence


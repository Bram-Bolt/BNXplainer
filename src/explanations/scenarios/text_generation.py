# Copyright (c) 2026 MSDT Group 2 All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

"""Convert scenario assignments into reader-facing explanation text."""

from explanations.scenarios.models import FullScenario, ScenarioNode
import pyagrum as gum
import numpy as np
from itertools import product

def build_scenario_from_explanation(
    bn: gum.BayesNet,
    possible_explanation: dict[str, str],
    joint_prob: float,
    target: str,
) -> FullScenario:
    """Build a FullScenario from one ranked assignment returned by scenario search."""
    
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
            
            # classify whether the node supports the target's value
            if supports_target(bn,node_name,node_value,target,target_value):
                fs.supporting.append(generate_supporting_sentence(node))

            if is_implausible(bn,node_name,node_value):
                fs.implausible.append(generate_implausible_sentence(node)) 
         
        else:
            target_node = node
        
    fs.scenario = generate_target_outcome(elements, target_node)
    return fs


def supports_target(bn: gum.BayesNet, node_name: str, node_value: str, target_name: str, target_value: str) -> bool:
    """
    Function that returns True if the inspected node and its state/value supports the target's
    state/value in the Scenario. Else it returns False.
    """
    target_node = bn.variable(target_name)
    target_value_idx = target_node[target_value]

    ie = gum.LazyPropagation(bn)

    # Prior probability of the target value
    ie.makeInference()
    prior = ie.posterior(target_name)[target_value_idx]

    # Posterior probability given evidence
    ie.setEvidence({node_name: node_value})
    ie.makeInference()
    posterior = ie.posterior(target_name)[target_value_idx]
    return posterior > prior


def is_implausible(bn:gum.BayesNet,node_name:str,node_value) -> bool: 
    """
    Is the node of the network in its most probable state?
    """
    node = bn.variable(node_name)
    cpt = bn.cpt(node_name)

    # CASE 1: No parents
    parents = list(bn.parents(node_name))

    if len(parents) == 0:
        probs = np.array(cpt[:])
        max_idx = np.argmax(probs)

        # Correct way to get label/state name
        most_probable_value = node.label(int(max_idx))
        return node_value != most_probable_value

    # CASE 2: Has parents
    # Build all parent value combinations
    parent_vars = [bn.variable(p) for p in parents]
    parent_domains = [
        [var.label(i) for i in range(var.domainSize())]
        for var in parent_vars]
    for assignment in product(*parent_domains):
        evidence = {
            parent_vars[i].name(): assignment[i]
            for i in range(len(parent_vars))}

        # Conditional distribution P(node | parents=evidence)
        probs = np.array(cpt[evidence])
        max_idx = np.argmax(probs)
        most_probable_value = node.label(int(max_idx))
        
        # If node_value is not the MAP value for this configuration
        if node_value != most_probable_value:
            return True

    return False
    


def generate_target_outcome(elements: list[ScenarioNode], target: ScenarioNode) -> str:
    """Return the main scenario sentence from explanatory nodes and target node."""

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



def prob_to_str(prob: float) -> str:
    """Convert a probability into the qualitative adverb used in scenario text."""
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


def generate_implausible_sentence(node: ScenarioNode)-> str: 
    """Return an implausibility sentence for a scenario node assignment."""
    prob = 1 - node.prob # because less likely is 'stronger'
    prob = prob_to_str(node.prob)
    sentence = f"{node.name} being {node.value} is {prob} unlikely"
    return sentence

def generate_supporting_sentence(node: ScenarioNode)->str:
    """Return a supporting sentence for a node that increases target likelihood."""
    prob = prob_to_str(node.prob)
    sentence = f"{prob} supported by {node.name} being {node.value}"
    return sentence

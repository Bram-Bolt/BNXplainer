import pyagrum as gum


def extract_bn_features(
    bn: gum.BayesNet,
    evidence: dict[str, str | int | list[float]] | None = None,
) -> dict:
    """
    Convert a Bayesian network into plain Python data that Dash/Plotly can consume.

    Parameters
    ----------
    bn:
        The Bayesian network to inspect.
    evidence:
        Optional evidence to apply before computing posterior (probility of a variable taking evidence into account) probabilities.
        Examples:
            {"Smoker": "True"}
            {"Pollution": 0}
            {"Cancer": [0.8, 0.2]} 

    Returns
    -------
    dict
        - nodes: per-node structure + posterior
        - edges: graph connections
        - potentials: CPT (conditional probability table) data for each node
        - evidence: the evidence that was applied
    """

    # Build an inference engine for this BN.
    ie = gum.LazyPropagation(bn)

    # Apply evidence only if the caller provided it.
    if evidence:
        ie.setEvidence(evidence)

    # Run inference once so posterior(node) is available for every node.
    ie.makeInference()

    nodes = []
    potentials = []

    # Preserve pyAgrum's native iteration order by default.
    # Uncomment the sorted(...) version below if you want deterministic
    # alphabetical ordering for tests or UI diffing.
    for node_name in bn.names():
    # for node_name in sorted(bn.names()):
        node_id = bn.idFromName(node_name)
        variable = bn.variableFromName(node_name)

        # Extract the possible labels/states of the current variable.
        states = list(variable.labels())

        # Preserve pyAgrum's native parent/child order by default.
        # Uncomment the sorted(...) versions below if you want deterministic
        # alphabetical ordering.
        parents = [bn.variable(parent_id).name() for parent_id in bn.parents(node_id)]
        # parents = sorted(
        #     bn.variable(parent_id).name() for parent_id in bn.parents(node_id)
        # )
        children = [bn.variable(child_id).name() for child_id in bn.children(node_id)]
        # children = sorted(
        #     bn.variable(child_id).name() for child_id in bn.children(node_id)
        # )

        # Extract the current posterior distribution for this node.
        # This changes when evidence changes.
        posterior_tensor = ie.posterior(node_name)
        posterior_values = posterior_tensor.tolist()

        # Zip state labels to their probabilities so the frontend can render
        # them without needing to know pyAgrum internals.
        posterior = {
            state: probability
            for state, probability in zip(states, posterior_values)
        }

        nodes.append(
            {
                "id": node_name,
                "states": states,
                "parents": parents,
                "children": children,
                "posterior": posterior,
            }
        )

        # Extract the CPT (conditional probability table) for this node.
        # Keep both the tensor values and the variable order together.
        # The frontend must preserve this order when displaying the CPT.
        cpt = bn.cpt(node_name)
        potentials.append(
            {
                "node": node_name,
                "variables": list(cpt.names),
                "values": cpt.tolist(),
            }
        )

    # Extract the structural graph edges for visualization.
    edges = [
        {
            "source": bn.variable(parent_id).name(),
            "target": bn.variable(child_id).name(),
        }
        for parent_id, child_id in bn.arcs()
    ]

    # Preserve pyAgrum's native edge and CPT order by default.
    # Uncomment these lines if you want deterministic ordering.
    edges.sort(key=lambda edge: (edge["source"], edge["target"]))
    potentials.sort(key=lambda potential: potential["node"])

    return {
        "nodes": nodes,
        "edges": edges,
        "potentials": potentials,
        "evidence": evidence or {},
    }

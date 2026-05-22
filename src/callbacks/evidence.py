# callbacks/evidence.py
from dash import callback, Input, Output, State, ALL, ctx, no_update

def register_evidence_callback(app):
    @callback(
        Output('evidence-store', 'data'),
        Output({'type': 'evidence-radiogroup', 'node': ALL}, 'value'),
        Input('submit-evidence', 'n_clicks'),
        Input('target-store', 'data'),
        State({'type': 'evidence-radiogroup', 'node': ALL}, 'value'),
        State({'type': 'evidence-radiogroup', 'node': ALL}, 'id'),
    )
    def read_evidence(n_clicks: int, target: str, node_values: list[str | None], node_ids: list[dict[str, str]]):
        """This function reads evidence from the radiogroup when the evidence is submitted.
        It parses and then stores this evidence for later use in other callbacks.
        Additionally, the function resets the observed state for target nodes

        Args:
            n_clicks (int): The amount of clicks of the 'submit-evidence' button this session
            target (str): The current target node
            node_values (list[str | None]): List of observed states per node (hence None in typehint)
            node_ids (list[dict[str, str]]): List of dictionaries of form {'type': 'evidence-radiogroup', 'node': nodename}

        Returns:
            dict[str, str]: Evidence, as passed through the radiogroups
            list[str | None]: List of observed states per node
        """
        evidence = {}
        node_vals = []

        # Construct evidence
        for val, node_id in zip(node_values, node_ids):
            if node_id.get('node') == target or val == None:
                node_vals.append(None)
            else:
                node = node_id.get('node')
                evidence[node] = val
                node_vals.append(val)

        # Deprecated Code DO NOT REMOVE UNTIL RELEASE
        # This can still be used for sliders way of handling evidence
        # Handle binary nodes
        # for val, node_id in zip(binary_values, binary_ids):
        #     node = node_id.get('node')
        #     evidence[node] = [round(val/100, 4), round(1-(val/100), 4)]
        
        # # Handle nary nodes
        # nary_evidence = defaultdict(list)
        # for val, node_id in zip(nary_values, nary_ids):
        #     node = node_id.get('node')
        #     nary_evidence[node].append(round(val/100, 4))

        # for node, arr in dict(nary_evidence).items():
        #     evidence[node] = arr
        return evidence, node_vals
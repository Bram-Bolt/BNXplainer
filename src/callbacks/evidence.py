# callbacks/evidence.py
from dash import callback, Input, Output, State, no_update, ALL
from collections import defaultdict

def register_evidence_callback(app):
    @callback(
        Output('evidence-store', 'data'),
        Input('submit-evidence', 'n_clicks'),
        State({'type': 'binary-slider', 'node': ALL}, 'value'),
        State({'type': 'node-slider', 'node': ALL, 'state': ALL}, 'value'),
        State({'type': 'binary-slider', 'node': ALL}, 'id'),
        State({'type': 'node-slider', 'node': ALL, 'state': ALL}, 'id'),
    )
    def read_evidence(n_clicks: int, binary_values: list[float], nary_values: list[float], binary_ids: list[dict[str, str]], nary_ids: list[dict[str, str, str]]):
        """This function reads evidence from the sliders when the evidence is submitted.
        It then stores this evidence for later use in another callback.

        Args:
            n_clicks (int): The amount of clicks of the 'submit-evidence' button this session
            binary_values (list[float]): Values of binary sliders
            nary_values (list[float]): Values of n-ary sliders
            binary_ids (list[dict[str, str]]): IDs of binary sliders
            nary_ids (list[dict[str, str, str]]): IDs of n-ary sliders

        Returns:
            dict[str, list[float]]: Evidence, as passed through the sliders
        """
        evidence = {}

        # Handle binary nodes
        for val, node_id in zip(binary_values, binary_ids):
            node = node_id.get('node')
            evidence[node] = [round(val/100, 4), round(1-(val/100), 4)]
        
        # Handle nary nodes
        nary_evidence = defaultdict(list)
        for val, node_id in zip(nary_values, nary_ids):
            node = node_id.get('node')
            nary_evidence[node].append(round(val/100, 4))

        for node, arr in dict(nary_evidence).items():
            evidence[node] = arr
            
        return evidence
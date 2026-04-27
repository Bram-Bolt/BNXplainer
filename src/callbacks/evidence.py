# callbacks/evidence.py
import dash_mantine_components as dmc

from dash import html, dcc, callback, Input, Output, State, no_update, clientside_callback, ctx, ALL, MATCH
from utils.file_utils import load_bn_from_base64
from utils.inference_html import generate_inference_html
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
    def read_evidence(n_clicks: int, binary_values: dict, nary_values: dict, binary_ids: dict, nary_ids: dict):
        if ctx.triggered_id != 'submit-evidence':
            return no_update
        
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
            
        print(evidence)
        return evidence
# callbacks/target_node.py
import dash_mantine_components as dmc

from dash import html, dcc, callback, Input, Output, State, no_update, clientside_callback, ctx, ALL, MATCH
from utils.file_utils import load_bn_from_base64
from utils.inference_html import generate_inference_html
from utils.feature_extraction import extract_bn_features
from explanations.voi import compute_voi, voi_to_display
from components.voi import render_voi_list
import json

def register_target_node_callback(app):
    @callback(
        Output({'type': 'node-card', 'node': ALL}, 'style'),
        Input({'type': 'node-card-wrapper', 'node': ALL}, 'n_clicks'),
        State('bn-store', 'data'),
        State({'type': 'node-card', 'node': ALL}, 'id'),
        prevent_initial_call=True
    )
    def update_target_node(n_clicks_list, data, card_ids):
        if not ctx.triggered or not data:
            return no_update
            
        triggered_id_str = ctx.triggered[0]['prop_id'].split('.')[0]
        try:
            triggered_id = json.loads(triggered_id_str)
            target_node = triggered_id.get('node')
        except json.JSONDecodeError:
            return no_update
            
        if not target_node:
            return no_update
        
        styles = []
        for item in card_ids:
            is_target = item['node'] == target_node
            styles.append({
                "borderColor": "#228be6" if is_target else "black",
                "borderWidth": "2px" if is_target else "1px"
            })
            
        # bn = load_bn_from_base64(data['str_bn'], data['filename'])
        # try:
        #     voi_scores = compute_voi(bn, target=target_node, evidence={})
        #     voi_data = voi_to_display(voi_scores)
            
        #     explain_content = dmc.Stack([
        #         dmc.Text(f"Target: {target_node}", fw=600, size="sm", mb="xs"),
        #         render_voi_list(voi_data)
        #     ], h="100%", style={"display": "flex", "flexDirection": "column", "overflow": "hidden"})
        # except Exception as e:
        #     explain_content = dmc.Text(f"Could not compute VOI: {str(e)}", color="red")
            
        return styles

# callbacks/target_node.py
from dash import callback, Input, Output, State, no_update, ctx, ALL
import json
import colours

def register_target_node_callback(app):
    @callback(
        Output({'type': 'node-card', 'node': ALL}, 'style'),
        Output('target-store', 'data'),
        Input({'type': 'node-card-wrapper', 'node': ALL}, 'n_clicks'),
        State('bn-store', 'data'),
        State({'type': 'node-card', 'node': ALL}, 'id'),
        prevent_initial_call=True
    )
    def update_target_node(n_clicks_list, data, card_ids):
        if not ctx.triggered or not data:
            return no_update, no_update
            
        triggered_id_str = ctx.triggered[0]['prop_id'].split('.')[0]
        try:
            triggered_id = json.loads(triggered_id_str)
            target_node = triggered_id.get('node')
        except json.JSONDecodeError:
            return no_update, no_update
            
        if not target_node:
            return no_update, no_update
        
        styles = []
        for item in card_ids:
            is_target = item['node'] == target_node
            styles.append({
                "borderColor": colours.olive if is_target else colours.black,
                "borderWidth": "2px" if is_target else "1px"
            })
            
        return styles, target_node

"""Handle target-node selection and target styling in the node list."""

from dash import callback, Input, Output, State, no_update, ctx, ALL
import json
import colours

def register_target_node_callback(app):
    """Register the callback that stores and highlights the selected target node."""
    @callback(
        Output({'type': 'node-card', 'node': ALL}, 'style'),
        Output({'type': 'node-card', 'node': ALL}, 'bg'),
        Output({'type': 'target-button', 'node': ALL}, 'children'),
        Output({'type': 'target-button', 'node': ALL}, 'variant'),
        Output('target-store', 'data'),
        Output({'type': 'evidence-radiogroup', 'node': ALL}, 'display'),
        Output('status-target', 'children'),
        Input({'type': 'target-button', 'node': ALL}, 'n_clicks'),
        State('bn-store', 'data'),
        State({'type': 'node-card', 'node': ALL}, 'id'),
        prevent_initial_call=True
    )
    def update_target_node(n_clicks_list, data, card_ids):
        """Update node card styles and target-store after a target button click."""
        if not ctx.triggered or not data:
            return (no_update,) * 7
            
        triggered_id_str = ctx.triggered[0]['prop_id'].split('.')[0]
        try:
            triggered_id = json.loads(triggered_id_str)
            target_node = triggered_id.get('node')
        except json.JSONDecodeError:
            return (no_update,) * 7
            
        if not target_node:
            return (no_update,) * 7
        
        styles = []
        backgrounds = []
        button_texts = []
        button_variants = []
        radio_displays=[]

        for item in card_ids:
            is_target = item['node'] == target_node

            styles.append(no_update)
            backgrounds.append(colours.card_bg)
            button_texts.append("✓ Target" if is_target else "Set Target")
            button_variants.append("filled" if is_target else "outline")
            radio_displays.append("none" if is_target else "block")

        return (styles, backgrounds, button_texts, button_variants, target_node, radio_displays,  f"Target: {target_node}")

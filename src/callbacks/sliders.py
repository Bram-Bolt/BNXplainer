from dash import callback, Input, Output, State, no_update, ctx, ALL, MATCH
import json 

def register_slider_callbacks(app):
    @callback(
        Output({'type': 'binary-text', 'node': MATCH, 'idx': ALL}, 'children'),
        Input({'type': 'binary-slider', 'node': MATCH}, 'value'),
        State({'type': 'binary-text', 'node': MATCH, 'idx': ALL}, 'id'),
        prevent_initial_call=True
    )
    def sync_binary_slider(value, ids):
        texts = []
        for item in ids:
            idx = item['idx']
            val = value if idx == 0 else 100.0 - value
            texts.append(f"{val/100:.1%}")
        return texts

    @callback(
        Output({'type': 'node-slider', 'node': MATCH, 'state': ALL}, 'value'),
        Output({'type': 'node-text', 'node': MATCH, 'state': ALL}, 'children'),
        Input({'type': 'node-slider', 'node': MATCH, 'state': ALL}, 'value'),
        State({'type': 'node-slider', 'node': MATCH, 'state': ALL}, 'id'),
        prevent_initial_call=True
    )
    def sync_multi_sliders(values, ids):
        if not ctx.triggered:
            return no_update, no_update
            
        triggered_id_str = ctx.triggered[0]['prop_id'].split('.')[0]
        triggered_id = json.loads(triggered_id_str)
        triggered_state = triggered_id['state']
        
        idx = next((i for i, item in enumerate(ids) if item['state'] == triggered_state), None)
        if idx is None:
            return no_update, no_update
            
        new_val = values[idx]
        
        total_others = sum(v for i, v in enumerate(values) if i != idx)
        remaining = max(0.0, 100.0 - new_val)
        
        result_values = []
        result_texts = []
        for i, (v, item) in enumerate(zip(values, ids)):
            if i == idx:
                val = round(new_val, 2)
            else:
                if total_others == 0:
                    val = round(remaining / (len(values) - 1), 2)
                else:
                    val = round((v / total_others) * remaining, 2)
            result_values.append(val)
            result_texts.append(f"{val/100:.1%}")
                    
        return result_values, result_texts
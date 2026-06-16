"""Update the centre-panel inference diagram and prediction table."""

from dash import callback, Input, Output, no_update, ctx
from utils.file_utils import load_bn_from_base64
from utils.inference_html import generate_inference_html
from components.variable_table import build_variable_data, render_variable_list

def register_image_callback(app):
    """Register callbacks for the centre-panel network views."""
    @callback(
        Output('inference-iframe', 'srcDoc'),
        Input('evidence-store', 'data'),
        Input('bn-store', 'data'),
        Input('target-store', 'data'),
        prevent_initial_call=True
    )
    def update_image(evidence: dict[str, str], data: dict[str, str], target: str) -> str:
        """Render updated inference HTML after evidence, target, or network changes."""
        if not evidence and not data:
            return no_update
        contents = data['str_bn']
        filename = data['filename']
        bn = load_bn_from_base64(contents, filename)

        if ctx.triggered_id == 'bn-store':
            return generate_inference_html(bn, evidence=None, target=target)
        elif ctx.triggered_id == 'evidence-store':
            return generate_inference_html(bn, evidence=evidence, target=target)
        elif ctx.triggered_id == 'target-store':
            return generate_inference_html(bn, evidence=evidence, target=target)
        else:
            return no_update

    @callback(
        Output('center-panel-title',  'children'),
        Output('inference-iframe',    'style'),
        Output('center-view-table',   'style'),
        Output('center-view-table',   'children'),
        Input('center-view-selector', 'value'),
        Input('evidence-store',       'data'),
        Input('bn-store',             'data'),
    )
    def toggle_center_view(view: str, evidence: dict, data: dict):
        """Switch the centre panel between the inference diagram and prediction table."""
        iframe_visible = {"width": "100%", "height": "100%", "flex": 1, "border": "none"}
        iframe_hidden  = {"display": "none"}
        table_visible  = {"flex": 1, "overflow": "hidden"}
        table_hidden   = {"display": "none"}

        if view == "table":
            title = "Prediction Table"
            if data:
                bn = load_bn_from_base64(data['str_bn'], data['filename'])
                variables = build_variable_data(bn, evidence=evidence or None)
                table_content = render_variable_list(variables)
            else:
                table_content = no_update
            return title, iframe_hidden, table_visible, table_content

        # default: diagram
        return "Inference Diagram", iframe_visible, table_hidden, no_update

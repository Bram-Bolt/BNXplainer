"""Update the centre-panel inference diagram and prediction table."""

from dash import callback, Input, Output, no_update, ctx
from utils.file_utils import load_bn_from_base64
from utils.inference_html import generate_inference_html
from components.variable_table import build_variable_data, render_variable_list
import colours

def register_image_callback(app):
    """Register callbacks for the centre-panel network views."""
    @callback(
        Output('inference-iframe', 'srcDoc'),
        Input('evidence-store', 'data'),
        Input('bn-store', 'data'),
        Input('target-store', 'data'),
        prevent_initial_call=True
    )
    def update_image(evidence, data, target):
        """Updates the BayesNet inference diagram in the center panel."""
        if not evidence and not data:
            return no_update
        bn = load_bn_from_base64(data['str_bn'], data['filename'])
        if ctx.triggered_id == 'bn-store':
            return generate_inference_html(bn, evidence=None, target=target)
        elif ctx.triggered_id in ('evidence-store', 'target-store'):
            return generate_inference_html(bn, evidence=evidence, target=target)
        return no_update

    @callback(
        Output('center-panel-title', 'children'),
        Output('inference-iframe', 'style'),
        Output('center-view-table', 'style'),
        Output('center-view-table', 'children'),
        Output('diagram-legend', 'style'),
        Input('center-view-selector', 'value'),
        Input('evidence-store', 'data'),
        Input('bn-store', 'data'),
        Input('target-store', 'data'),
        prevent_initial_call=True,
    )
    def toggle_center_view(view, evidence, data, target):
        """Switches the center panel between the inference diagram and prediction table."""
        iframe_visible = {"width": "100%", "height": "100%", "flex": 1, "border": "none"}
        iframe_hidden  = {"display": "none"}
        table_visible  = {"flex": 1, "overflow": "hidden"}
        table_hidden   = {"display": "none"}

        legend_visible = {
            "position":        "absolute",
            "top":             "10px",
            "left":            "10px",
            "backgroundColor": colours.beige,
            "padding":         "6px 8px",
            "zIndex":          10,
            # Win95 raised border (matches raised() in home.py)
            "borderTop": f"2px solid {colours.white}",
            "borderLeft": f"2px solid {colours.white}",
            "borderRight": f"2px solid {colours.shadow_darkest}",
            "borderBottom": f"2px solid {colours.shadow_darkest}",
            "borderRadius": "0",
        }
        legend_hidden  = {"display": "none"}

        filename = data['filename'] if data else "cancer.net"

        if view == "table":
            if data:
                bn = load_bn_from_base64(data['str_bn'], data['filename'])
                variables = build_variable_data(bn, evidence=evidence or None, target=target)
                table_content = render_variable_list(variables)
            else:
                table_content = no_update
            return f"Prediction Table ({filename})", iframe_hidden, table_visible, table_content, legend_hidden

        # default: diagram
        return f"Inference Diagram ({filename})", iframe_visible, table_hidden, no_update, legend_visible

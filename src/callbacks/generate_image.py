# callbacks/generate_image.py
import dash_mantine_components as dmc
import pyagrum as gum
from dash import html, dcc, callback, Input, Output, State, no_update, clientside_callback, ctx, ALL, MATCH
from utils.file_utils import load_bn_from_base64
from utils.inference_html import generate_inference_html

def register_image_callback(app):
    @callback(
        Output('inference-iframe', 'srcDoc'),
        Input('evidence-store', 'data'),
        Input('bn-store', 'data'),
        prevent_initial_call = True
    )
    def update_image(evidence: dict[str, list], data: dict[str, str]) -> str:
        """_summary_

        Args:
            evidence (dict[str, list]): _description_
            data (dict[str, str]): _description_

        Returns:
            _type_: _description_
        """
        if not evidence and not data:
            return no_update
        contents = data['str_bn']
        filename = data['filename']
        bn = load_bn_from_base64(contents, filename)
        if ctx.triggered_id == 'bn-store':
            return generate_inference_html(bn)
        elif ctx.triggered_id == 'evidence-store':
            return generate_inference_html(bn, evidence)
        else: return no_update
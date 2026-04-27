# callbacks/generate_image.py
import dash_mantine_components as dmc

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
    def update_image(evidence: dict[str, list], bn: dict[str, str]):
        return None
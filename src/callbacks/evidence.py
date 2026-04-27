# callbacks/evidence.py
import dash_mantine_components as dmc

from dash import html, dcc, callback, Input, Output, State, no_update, clientside_callback, ctx, ALL, MATCH
from utils.file_utils import load_bn_from_base64
from utils.inference_html import generate_inference_html

def register_evidence_callback(app):
    @callback(
        
    )
    def read_evidence():
        pass
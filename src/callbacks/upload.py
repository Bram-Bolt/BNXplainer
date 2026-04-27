# callbacks/upload_callbacks.py
import dash_mantine_components as dmc

from dash import html, dcc, callback, Input, Output, State, no_update, clientside_callback, ctx, ALL, MATCH
from utils.file_utils import load_bn_from_base64
from utils.inference_html import generate_inference_html

def register_upload_callbacks(app):
    clientside_callback(
        """
        function(contents) {
            if (contents) { return true; }
            return dash_clientside.no_update;
        }
        """,
        Output("loading-overlay", "visible", allow_duplicate=True),
        Input("upload-data", "contents"),
        prevent_initial_call=True,
    )

    @callback(
        Output('bn-store', 'data'),
        Input('upload-data', 'contents'),
        State('upload-data', 'filename')
    )
    def handle_uploaded_file(contents: str, filename: str):
        if not contents:
            return no_update

        return {'str_bn': contents, 'filename': filename,}
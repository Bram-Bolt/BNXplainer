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
        Output('inference-iframe', 'srcDoc'),
        Output('loading-overlay', 'visible'),
        Input('upload-data', 'contents'),
        State('upload-data', 'filename')
    )
    def handle_uploaded_file(contents: str, filename: str):
        if not contents:
            return no_update, no_update, no_update
        bn = load_bn_from_base64(contents, filename)

        new_html = generate_inference_html(bn)

        return {'str_bn': contents, 'filename': filename,}, new_html, False
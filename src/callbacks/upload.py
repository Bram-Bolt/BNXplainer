# callbacks/upload_callbacks.py
from dash import callback, Input, Output, State, no_update, clientside_callback

def register_upload_callbacks(app):
    clientside_callback(
        """
        function(contents) {
            if (contents) { return true; }
            return dash_clientside.no_update;
        }
        """,
        Input("upload-data", "contents"),
        prevent_initial_call=True,
    )

    @callback(
        Output('bn-store', 'data'),
        Input('upload-data', 'contents'),
        State('upload-data', 'filename'),
        prevent_initial_call=True
    )
    def handle_uploaded_file(contents: str, filename: str):
        if not contents:
            return no_update

        return {'str_bn': contents, 'filename': filename,}
# uploads
from dash import callback, Input, Output, State, no_update
def register_upload_callbacks(app):

    @callback(
        Output('bn-store', 'data'),
        Output('evidence-store', 'data', allow_duplicate=True),
        Output('filename-display', 'children'),
        Output('status-filename',  'children'),  
        Input('upload-data', 'contents'),
        State('upload-data', 'filename'),
        prevent_initial_call=True
    )
    def handle_uploaded_file(contents: str, filename: str):
        """Store uploaded Dash file contents and reset evidence for the new network."""
        if not contents:
            return no_update, no_update, no_update, no_update

        return ({'str_bn': contents, 'filename': filename,}, {}, filename, f"Network: {filename}")
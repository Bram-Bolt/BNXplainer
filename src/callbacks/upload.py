"""Handle uploaded Bayesian network files and reset derived app state."""

from dash import callback, Input, Output, State, no_update, clientside_callback

def register_upload_callbacks(app):
    """Register upload callbacks that refresh bn-store and clear submitted evidence."""
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
        Output('evidence-store', 'data', allow_duplicate=True),
        Input('upload-data', 'contents'),
        State('upload-data', 'filename'),
        prevent_initial_call=True
    )
    def handle_uploaded_file(contents: str, filename: str):
        """Store uploaded Dash file contents and reset evidence for the new network."""
        if not contents:
            return no_update, no_update

        return {'str_bn': contents, 'filename': filename,}, {}
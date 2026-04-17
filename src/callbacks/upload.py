# callbacks/upload_callbacks.py
import dash_mantine_components as dmc

from dash import html, dcc, callback, Input, Output, State, no_update, clientside_callback, ctx, ALL, MATCH
from utils.file_utils import load_bn_from_base64
from services.inference_service import generate_inference_html
from services.feature_extraction import extract_bn_features
from explanations.voi import compute_voi, voi_to_display
from components.voi import render_voi_list
import json

def register_upload_callbacks(app):


    # show overlay when a file is selected
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
        Output('inference-iframe', 'srcDoc'),
        Output('loading-overlay', 'visible'),
        Output('nodes-list', 'children'),
        Input('upload-data', 'contents'),
        State('upload-data', 'filename')
    )
    def handle_uploaded_file(contents: str, filename: str):
        if contents is not None:
            bn = load_bn_from_base64(contents, filename)
            new_html = generate_inference_html(bn)
            
            node_names = list(bn.names())
            target_node = node_names[-1] if node_names else None
            
            # Extract BN features and create a list of components
            features = extract_bn_features(bn)
            node_elements = []
            for node in features.get("nodes", []):
                node_id = node.get("id")
                posterior = node.get("posterior", {})
                states = list(posterior.keys())
                probs = list(posterior.values())

                if len(states) == 2:
                    posteriors = [
                        dmc.Box([
                            dmc.Group([
                                dmc.Text(states[0], size="xs"),
                                dmc.Text(f"{probs[0]:.1%}", size="xs", fw=500, id={"type": "binary-text", "node": node_id, "idx": 0})
                            ], justify="space-between"),
                            dmc.Slider(
                                value=round(probs[0] * 100, 2),
                                min=0,
                                max=100,
                                size="sm",
                                id={"type": "binary-slider", "node": node_id},
                                step=0.1,
                                my=8
                            ),
                            dmc.Group([
                                dmc.Text(states[1], size="xs"),
                                dmc.Text(f"{probs[1]:.1%}", size="xs", fw=500, id={"type": "binary-text", "node": node_id, "idx": 1})
                            ], justify="space-between"),
                        ], mt="xs")
                    ]
                else:
                    posteriors = []
                    for state, prob in posterior.items():
                        posteriors.append(
                            dmc.Box([
                                dmc.Group([
                                    dmc.Text(state, size="xs"),
                                    dmc.Text(f"{prob:.1%}", size="xs", fw=500, id={"type": "node-text", "node": node_id, "state": state})
                                ], justify="space-between", mt="xs", mb=2),
                                dmc.Slider(
                                    value=round(prob * 100, 2),
                                    min=0,
                                    max=100,
                                    size="sm",
                                    id={"type": "node-slider", "node": node_id, "state": state},
                                    step=0.1
                                )
                            ])
                        )
                    
                is_target = node_id == target_node
                node_elements.append(
                    dmc.Card(
                        children=[
                            html.Div(
                                dmc.Tooltip(
                                    label="Set as Target",
                                    position="right",
                                    withArrow=True,
                                    children=dmc.Text(node_id, fw=600, style={"display": "inline-block"})
                                ),
                                id={"type": "node-card-wrapper", "node": node_id},
                                n_clicks=0,
                                style={"cursor": "pointer", "marginBottom": "4px"}
                            ),
                            *posteriors
                        ],
                        withBorder=True,
                        shadow="sm",
                        mb="sm",
                        bg="#ece4dc",
                        style={
                            "borderColor": "#228be6" if is_target else "black",
                            "borderWidth": "2px" if is_target else "1px"
                        },
                        id={"type": "node-card", "node": node_id}
                    )
                )

            return new_html, False, dmc.Stack(node_elements, gap="xs")

        return no_update, no_update, no_update
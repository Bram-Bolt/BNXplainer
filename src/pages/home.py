import dash_mantine_components as dmc
from dash import html, dcc, callback, Input, Output, State, no_update, clientside_callback, ctx, ALL, MATCH
import json
from services.inference_service import generate_inference_html, extract_bn_features
from utils.file_utils import load_bn_from_base64

#helper function to create rating radio buttons for likert scale
#label: method name shown
#group_id: unique id so each row is independent
def radio_row(label, group_id):
    return dmc.Group([
        dmc.Text(label, w=110, size="sm"),
        dmc.RadioGroup(
            dmc.Group([dmc.Radio(value=str(i)) for i in range(1, 6)], gap=16),
            id=group_id,
        ),
    ], gap="md")

def create_layout():

    centered_html = generate_inference_html()

    return dmc.AppShell(
        [
            dmc.AppShellHeader(
                dmc.Group(
                [
                    dmc.Title("Explainable AI", c="white", mx="auto"),
                    #feedback button in header opens popover feedback form
                    dmc.Popover(
                        [
                            dmc.PopoverTarget( #popover
                                dmc.Button(
                                    "Feedback",
                                    variant="outline",
                                    styles={
                                        "root": {
                                            "color": "#ece4dc",
                                            "borderColor": "#ece4dc",
                                            "--button-hover": "rgba(236, 228, 220, 0.1)",
                                        }
                                    },
                                ),
                            ),
                            dmc.PopoverDropdown(
                                dmc.Stack([
                                    dmc.Text("FEEDBACK FORM", fw=700, size="lg"),
                                    dmc.Text(
                                        "Please send us your thoughts, suggestions and feedback so we can improve. Thank you!",
                                        size="sm",
                                    ),
                                    dmc.Text("Which explanation did you prefer?", fw=500, mt="sm"),
                                    #dropdown to select preferred explanation method
                                    dmc.Select(
                                        id="preferred-explanation",
                                        placeholder="Select an explanation...",
                                        data=["VOI", "MPE", "Scenario"],
                                    ),
                                    #scale for each method
                                    dmc.Text("How would you rate the explanation methods:", fw=500, mt="sm"),
                                    dmc.Group([
                                        dmc.Text("", w=105),
                                        dmc.Text("confusing", size="xs", fw=500, w=60, c="#696969", ta="center"),
                                        dmc.Text("", w=80),
                                        dmc.Text("clarifying", size="xs", fw=500, w=60, c="#696969", ta="center"),
                                    ], gap=0),
                                    radio_row("VOI", "rating-VOI"),
                                    radio_row("MPE", "rating-MPE"),
                                    radio_row("Scenario", "rating-scenario"),
                                    dmc.Text("Please put your feedback below:", fw=500, mt="sm"),
                                    dmc.Text(
                                        "How did the methods help you understand the prediction? Is the explanation too big/complicated?",
                                        size="sm",
                                    ),
                                    #open answer feedback
                                    dmc.Textarea(
                                        id="feedback-text",
                                        minRows=3,
                                        placeholder="Your feedback here...",
                                    ),
                                    dmc.Button("Submit", id="submit-feedback", color="dark", fullWidth=True),
                                ], gap="sm"),
                                p="lg",
                                style={"width": 380, "backgroundColor": "#ece4dc"},
                            ),
                        ],
                        position="bottom-end",
                        withArrow=True,
                        shadow="md",
                        closeOnClickOutside=False,
                    ),
                ],
                h="100%",
                px="md",
            ),
                bg="black",
            ),

            dmc.AppShellMain(
                dmc.Group(
                    [

                        dmc.Paper(
                            [
                                dcc.Upload(
                                    id='upload-data',
                                    children=html.Button('Upload File', style={"width": "100%"}),
                                    style={"width": "100%"},
                                ),
                                dmc.ScrollArea(
                                    id="nodes-list",
                                    offsetScrollbars=False,
                                    type="hover",
                                    scrollbarSize=6,
                                    styles={
                                        "scrollbar": {
                                            "backgroundColor": "transparent",
                                            "&:hover": {"backgroundColor": "transparent"}
                                        }
                                    },
                                    style={"marginTop": "20px", "flex": 1, "marginRight": "-11px", "paddingRight": "11px"}
                                ),
                            ],
                            withBorder=True,
                            p="md",
                            shadow="xl",
                            bg="#ece4dc",
                            style={"flex": 2, "borderColor": "black", "display": "flex", "flexDirection": "column", "maxHeight": "100%"},
                        ),

                        dmc.Paper(
                            [
                                dmc.LoadingOverlay(
                                    id="loading-overlay",
                                    visible=False,
                                    overlayProps={"radius": "sm", "blur": 2, "color": "#ece4dc"},
                                    zIndex=10,
                                ),
                                html.H3("Inference Diagram", style={"marginTop": 0}),
                                html.Iframe(
                                    id='inference-iframe',
                                    srcDoc=centered_html,
                                    style={
                                        "width": "100%",
                                        "height": "100%",
                                        "flex": 1,
                                        "border": "none",
                                    },
                                ),
                            ],
                            id="inference-paper",
                            withBorder=True,
                            p="md",
                            shadow="xl",
                            bg="#ece4dc",
                            pos="relative",
                            style={
                                "flex": 5,
                                "borderColor": "black",
                                "display": "flex",
                                "flexDirection": "column",
                            },
                        ),

                        dmc.Paper(
                            "Explain",
                            withBorder=True,
                            p="md",
                            shadow="xl",
                            bg="#ece4dc",
                            style={"flex": 2, "borderColor": "black"},
                        ),
                    ],
                    align="stretch",
                    gap="md",
                    wrap="nowrap",
                    h="calc(100vh - 92px)",
                ),
                bg="#ece4dc",
            ),
        ],
        header={"height": 60},
        padding="md",
        id="appshell",
    )


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
def handle_uploaded_file(contents, filename):
    if contents is not None:
        bn = load_bn_from_base64(contents, filename)
        new_html = generate_inference_html(bn)
        
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
                
            node_elements.append(
                dmc.Card(
                    children=[
                        dmc.Text(node_id, fw=600),
                        *posteriors
                    ],
                    withBorder=True,
                    shadow="sm",
                    mb="sm",
                    bg="#ece4dc",
                    style={"borderColor": "black"}
                )
            )
            
        return new_html, False, dmc.Stack(node_elements, gap="xs")

    return no_update, no_update, no_update

@callback(
    Output({'type': 'binary-text', 'node': MATCH, 'idx': ALL}, 'children'),
    Input({'type': 'binary-slider', 'node': MATCH}, 'value'),
    State({'type': 'binary-text', 'node': MATCH, 'idx': ALL}, 'id'),
    prevent_initial_call=True
)
def sync_binary_slider(value, ids):
    texts = []
    for item in ids:
        idx = item['idx']
        val = value if idx == 0 else 100.0 - value
        texts.append(f"{val/100:.1%}")
    return texts

@callback(
    Output({'type': 'node-slider', 'node': MATCH, 'state': ALL}, 'value'),
    Output({'type': 'node-text', 'node': MATCH, 'state': ALL}, 'children'),
    Input({'type': 'node-slider', 'node': MATCH, 'state': ALL}, 'value'),
    State({'type': 'node-slider', 'node': MATCH, 'state': ALL}, 'id'),
    prevent_initial_call=True
)
def sync_multi_sliders(values, ids):
    if not ctx.triggered:
        return no_update, no_update
        
    triggered_id_str = ctx.triggered[0]['prop_id'].split('.')[0]
    triggered_id = json.loads(triggered_id_str)
    triggered_state = triggered_id['state']
    
    idx = next((i for i, item in enumerate(ids) if item['state'] == triggered_state), None)
    if idx is None:
        return no_update, no_update
        
    new_val = values[idx]
    
    total_others = sum(v for i, v in enumerate(values) if i != idx)
    remaining = max(0.0, 100.0 - new_val)
    
    result_values = []
    result_texts = []
    for i, (v, item) in enumerate(zip(values, ids)):
        if i == idx:
            val = round(new_val, 2)
        else:
             if total_others == 0:
                 val = round(remaining / (len(values) - 1), 2)
             else:
                 val = round((v / total_others) * remaining, 2)
        result_values.append(val)
        result_texts.append(f"{val/100:.1%}")
                 
    return result_values, result_texts

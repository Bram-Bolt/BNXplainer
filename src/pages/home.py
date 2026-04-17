import dash_mantine_components as dmc
from dash import html, dcc, callback, Input, Output, State, no_update, clientside_callback, ctx, ALL, MATCH
import json
from services.inference_service import generate_inference_html
from services.feature_extraction import extract_bn_features
from utils.file_utils import load_bn_from_base64
from explanations.voi import compute_voi, voi_to_display
from db.database import insertEntry
from components.inputs import radio_row
from components.voi import render_voi_list
from components.explanation_selector import explanation_dropdown_selection

def create_layout():

    centered_html = generate_inference_html()

    return dmc.AppShell(
        [
            dmc.AppShellHeader(
                dmc.Group(
                [
                    dmc.Title("[APP NAME]", c="white", mx="auto"),
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
                                    ],gap=0),
                                    radio_row("VOI", group_id="rating-VOI"),
                                    radio_row("MPE", group_id="rating-MPE"),
                                    radio_row("Scenario", group_id="rating-scenario"),
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
                            [
                                dmc.Group(
                                    [
                                        html.H3(id="explanation-title", style={"marginTop": 0}),
                                        explanation_dropdown_selection(),
                                    ],
                                    justify="space-between",
                                    align="center",
                                ),
                                
                                dmc.Text(
                                    id="explanation-description",
                                    size="sm",
                                    mb="md",
                                    c="dimmed"
                                ),
                                dmc.Stack(
                                    [
                                        html.Div(
                                            id="explain-content",
                                            style={
                                                "flex": 1,
                                                "display": "flex",
                                                "flexDirection": "column",
                                                "overflow": "hidden"
                                            }
                                        ),

                                    ],
                                    style={"flex": 1,  "minHeight": 0}
                                   
                                )
                            ],
                            withBorder=True,
                            p="md",
                            shadow="xl",
                            bg="#ece4dc",
                            style={"flex": 2, "borderColor": "black", "display": "flex", "flexDirection": "column", "maxHeight": "100%"},
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
    Output('explain-content', 'children'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def handle_uploaded_file(contents, filename):
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
            
        if target_node:
            try:
                voi_scores = compute_voi(bn, target=target_node, evidence={})
                voi_data = voi_to_display(voi_scores)
                
                explain_content = dmc.Stack([
                    dmc.Text(f"Target: {target_node}", fw=600, size="sm", mb="xs"),
                    render_voi_list(voi_data)
                ], h="100%", style={"display": "flex", "flexDirection": "column", "overflow": "hidden"})
            except Exception as e:
                explain_content = dmc.Text(f"Could not compute VOI: {str(e)}", color="red")
        else:
            explain_content = dmc.Text("No nodes available.")

        return new_html, False, dmc.Stack(node_elements, gap="xs"), explain_content

    return no_update, no_update, no_update, no_update

@callback(
    Output('explain-content', 'children', allow_duplicate=True),
    Output({'type': 'node-card', 'node': ALL}, 'style'),
    Input({'type': 'node-card-wrapper', 'node': ALL}, 'n_clicks'),
    State('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State({'type': 'node-card', 'node': ALL}, 'id'),
    prevent_initial_call=True
)
def update_target_node(n_clicks_list, contents, filename, card_ids):
    if not ctx.triggered or not contents:
        return no_update, no_update
        
    triggered_id_str = ctx.triggered[0]['prop_id'].split('.')[0]
    try:
        triggered_id = json.loads(triggered_id_str)
        target_node = triggered_id.get('node')
    except json.JSONDecodeError:
        return no_update, no_update
        
    if not target_node:
        return no_update, no_update
    
    styles = []
    for item in card_ids:
        is_target = item['node'] == target_node
        styles.append({
            "borderColor": "#228be6" if is_target else "black",
            "borderWidth": "2px" if is_target else "1px"
        })
        
    bn = load_bn_from_base64(contents, filename)
    try:
        voi_scores = compute_voi(bn, target=target_node, evidence={})
        voi_data = voi_to_display(voi_scores)
        
        explain_content = dmc.Stack([
            dmc.Text(f"Target: {target_node}", fw=600, size="sm", mb="xs"),
            render_voi_list(voi_data)
        ], h="100%", style={"display": "flex", "flexDirection": "column", "overflow": "hidden"})
    except Exception as e:
        explain_content = dmc.Text(f"Could not compute VOI: {str(e)}", color="red")
        
    return explain_content, styles


# FEEDBACK CALLBACK
@callback(
    Output("submit-feedback","children"),
    Input("submit-feedback", 'n_clicks'),
    State("preferred-explanation", 'value'),
    State('rating-VOI', 'value'),
    State('rating-MPE', 'value'),
    State('rating-scenario', 'value'),
    State("feedback-text", 'value'),
    )
def feedback_function(n_clicks, preferred_exp, rating_voi, rating_mpe, rating_scenario, feedback_text):
    if not n_clicks:
        return no_update

    return insertEntry(
                    str(preferred_exp),
                    int(rating_voi),
                    int(rating_mpe),
                    int(rating_scenario),
                    str(feedback_text))
    

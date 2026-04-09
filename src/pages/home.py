import dash_mantine_components as dmc
from dash import html, dcc, callback, Input, Output, State, no_update, clientside_callback
from services.inference_service import generate_inference_html
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
                                    children=html.Button('Upload File'),
                                ),
                            ],
                            withBorder=True,
                            p="md",
                            shadow="xl",
                            bg="#ece4dc",
                            style={"flex": 2, "borderColor": "black"},
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
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def handle_uploaded_file(contents, filename):
    if contents is not None:
        bn = load_bn_from_base64(contents, filename)
        new_html = generate_inference_html(bn)
        return new_html, False

    return no_update, no_update
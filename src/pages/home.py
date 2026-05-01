import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash import html, dcc
from components.feedback_helpers import likert_question, likert_range
from utils.inference_html import generate_inference_html
from components.explanation_selector import explanation_dropdown_selection
from utils.file_utils import load_placeholder_bn

def create_layout():

    centered_html = """<html style="height: 100%; margin: 0;">
    </html>"""
    

    return dmc.AppShell(
        [
            # Include a storage component for bn-persistence
            dcc.Store(
            id='bn-store',
            storage_type='memory',
            data={
                "str_bn": load_placeholder_bn("src/example_bns/cancer.net"),
                "filename": "cancer.net"
            }
        ),
            
            dcc.Store(id='evidence-store', storage_type='memory'),

            dcc.Store(id='target-store', storage_type='memory'),

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
                                    id="feedback-button",
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
                                html.Div(
                                    id="feedback-popover-content",
                                    children=[
                                        dmc.Stack([
                                            dmc.Text("FEEDBACK FORM", fw=700, size="lg"),
                                            dmc.Text(
                                                "Please send us your thoughts, suggestions and feedback, so we can improve. Thank you!",
                                                size="sm",
                                            ),

                                             # Website navigation question (static)
                                            dmc.Text("Did you find the website easy to navigate?", fw=500, mt="sm"),
                                            likert_range("difficult", "easy"),
                                            likert_question("rating-website", "Website navigation"),

                                            # Plus buttons to toggle extra feedback sections
                                            dmc.Group([
                                                dmc.Button("+ feedback for VOI", id="btn-voi", variant="outline", size="xs",c="dark"),
                                                dmc.Button("+ feedback for MPE", id="btn-mpe", variant="outline", size="xs",c="dark"),
                                                dmc.Button("+ feedback for Scenario", id="btn-scenario", variant="outline", size="xs",c="dark"),
                                            ], mt="sm"),
                                            
                                            # VOI questions (hidden until toggled)
                                            html.Div(
                                                id="voi-feedback",
                                                children=dmc.Stack([
                                                    dmc.Text("VOI Feedback", fw=600, mt="sm"),
                                                    likert_range("not at all", "very"),
                                                    likert_question("voi-q1", "Did you find the explanation easy to understand?"),
                                                    likert_question("voi-q2", "Did the explanation make you feel more confident in the model’s prediction?"),
                                                    likert_question("voi-q3", "Did you find the explanation too complex?"),
                                                ]),
                                                style={"display": "none"}
                                            ),

                                            # MPE questions (hidden until toggled)
                                            html.Div(
                                                id="mpe-feedback",
                                                children=dmc.Stack([
                                                    dmc.Text("MPE Feedback", fw=600, mt="sm"),
                                                    likert_range("not at all", "very"),
                                                    likert_question("mpe-q1", "Did you find the explanation easy to understand?"),
                                                    likert_question("mpe-q2", "Did the explanation make you feel more confident in the model’s prediction?"),
                                                    likert_question("mpe-q3", "Did you find the explanation too complex?"),
                                                ]),
                                                style={"display": "none"}
                                            ),

                                            # Scenario questions (hidden until toggled)
                                            html.Div(
                                                id="scenario-feedback",
                                                children=dmc.Stack([
                                                    dmc.Text("Scenario Feedback", fw=600, mt="sm"),
                                                    likert_range("not at all", "very"),
                                                    likert_question("scenario-q1", "Did you find the explanation easy to understand?"),
                                                    likert_question("scenario-q2", "Did the explanation make you feel more confident in the model’s prediction?"),
                                                    likert_question("scenario-q3", "Did you find the explanation too complex?"),
                                                ]),
                                                style={"display": "none"}
                                            ),

                                            # open comment
                                            dmc.Text("Please put any final feedback below:", fw=500, mt="sm"),
                                            dmc.Textarea(
                                                id="feedback-text",
                                                minRows=3,
                                                placeholder="How did the methods help you understand the prediction? Why is it understandable or complicated?",
                                            ),
                                        ], gap="sm", style={"maxHeight": "600px", "overflowY": "auto", "paddingRight": "10px"}),
                                    # submit button always shown
                                    dmc.Button("Submit", id="submit-feedback", color="dark", fullWidth=True,mt="md"),
                                    ],
                                ),
                                p="lg",
                                style={"width": 500, "backgroundColor": "#ece4dc",},
                            ),
                        ],
                        id="feedback-popover",
                        position="bottom-end",
                        withArrow=True,
                        shadow="md",
                        closeOnClickOutside=True,
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
                                dmc.Button("Submit Evidence", id="submit-evidence", fullWidth=True, mt="md"),
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


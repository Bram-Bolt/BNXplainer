import dash_mantine_components as dmc
from dash import html, dcc
from utils.inference_html import generate_inference_html
from components.inputs import radio_row
from components.explanation_selector import explanation_dropdown_selection

def create_layout():

    centered_html = generate_inference_html()

    return dmc.AppShell(
        [
            # Include a storage component for bn-persistence
            dcc.Store(id='bn-store', storage_type='memory'),

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
                                    children=dmc.Stack([
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
                                ),
                                p="lg",
                                style={"width": 380, "backgroundColor": "#ece4dc"},
                            ),
                        ],
                        id="feedback-popover",
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



# Copyright (c) 2026 MSDT Group 2 All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

"""Build the main Dash application layout and shared in-browser stores."""

import dash_mantine_components as dmc
import colours
from dash import html, dcc
from components.feedback_helpers import likert_question, likert_range
from components.explanation_selector import explanation_selection
from utils.file_utils import load_placeholder_bn


def raised(extra=None):
    """Return a Win95-style raised bevel style merged with optional overrides."""
    style = {
        "borderTop": f"2px solid {colours.white}",
        "borderLeft": f"2px solid {colours.white}",
        "borderRight": f"2px solid {colours.shadow_darkest}",
        "borderBottom": f"2px solid {colours.shadow_darkest}",
        "borderRadius": "0",
    }
    if extra:
        style.update(extra)
    return style


def sunken(extra=None):
    """Return a Win95-style sunken bevel style merged with optional overrides."""
    style = {
        "borderTop": f"2px solid {colours.shadow_dark}",
        "borderLeft": f"2px solid {colours.shadow_dark}",
        "borderRight": f"2px solid {colours.white}",
        "borderBottom": f"2px solid {colours.white}",
        "borderRadius": "0",
    }
    if extra:
        style.update(extra)
    return style


def panel_title(text: str):
    """Render a blue title bar for a content panel."""
    return html.Div(
        text,
        style={
            "backgroundColor": colours.blue,
            "color": colours.beige,
            "padding": "3px 8px",
            "fontSize": "15px",
            "fontWeight": "600",
            "marginBottom": "6px",
        }
    )


def nav_button(label: str):
    """Render a raised Win95-style navigation button for the header."""
    return html.Button(
        label,
        className="nav-btn",
        style={
            "backgroundColor": colours.beige,
            "color": colours.maroon,
            "padding": "2px 12px",
            "fontWeight": "bold",
            "fontSize": "14px",
            "cursor": "pointer",
            "borderTop": f"2px solid {colours.white}",
            "borderLeft": f"2px solid {colours.white}",
            "borderRight": f"2px solid {colours.shadow_darkest}",
            "borderBottom": f"2px solid {colours.shadow_darkest}",
        }
    )


def create_layout():

    centered_html = """<html style="height: 100%; margin: 0;"></html>"""

    return dmc.AppShell(
        [
            # storage component for bn-persistence
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
            html.Span(id="explanation-title", style={"display": "none"}),

            #---- header -----
            dmc.AppShellHeader(
              html.Div([

                html.Img(
                    src="/assets/header-logo.PNG",
                    style={"height": "60px", "marginRight": "4px"},
                ),

                    html.Div(
                        "BNXplainer",
                        style={
                            "color": colours.beige,
                            "fontSize": "25px",
                            "fontWeight": "bold",
                            "flex": 1,
                            "textAlign": "center",
                        }
                    ),
                    html.Div([

                        dmc.Popover([
                            dmc.PopoverTarget(
                                 nav_button("About us"),
                            ),
                            dmc.PopoverDropdown(
                                dmc.Stack([
                                    dmc.Text("ABOUT US", fw=800, size="sm"),
                                    dmc.Text(
                                        "We are a team of nine Radboud University students taking the course Modern Software Development Techniques, organised by the Artificial Intelligence Department (Donders Institute), under the coordination of Dr. Bryan Da Costa Souza. Our client Dr. Marcos De Paula Bueno , Assistant Professor at Radboud University, commissioned this project on explainable AI (XAI) for white-box models: implementation and visualisation.",
                                        size="sm",
                                    ),
                                    dmc.Text(
                                        "While explanation methods are widely available for black-box models, explanation tools for Bayesian networks, which are interpretable white-box models, remain scarce. Our project's goal is to address this gap in XAI and make explanations more helpful for interpretation, using explanation methods and visualisation.",
                                        size= "sm",),
                                    dmc.Text(
                                        "BNXplainer, lets users upload a Bayesian network, set evidence variables and select a target feature. From there, inference results are computed and visualised through an inference diagram and a prediction table. To support explainability, we implemented three explanation methods: Value of Information (VOI), Most Probable Explanation (MPE) and Scenario Analysis. The feedback function lets users rate and reflect on the explanations they receive, contributing to the ongoing improvement of BNXplainer.",
                                        size= "sm",),

                                    dmc.Text(
                                        "We hope our efforts contribute to address this gap and improving how Bayesian network predictions are understood and interpeted.",
                                        size= "sm",),

                                    dmc.Stack([
                                        dmc.Text("Arthur Lemke — backend", size="sm"),
                                        dmc.Text("Bram Bolt — API", size="sm"),
                                        dmc.Text("Douae Chrifi - backend", size="sm"),
                                        dmc.Text("Erva Ülgen — frontend", size="sm"),
                                        dmc.Text("Fatima Moalin — backend", size="sm"),
                                        dmc.Text("Jippe Pauwels — frontend", size="sm"),
                                        dmc.Text("Kamil Kuit — database", size="sm"),
                                         dmc.Text("Luc du Plessis — frontend", size="sm"),
                                        dmc.Text("Olivier Broekman — API", size="sm"),
                                        
                                        dmc.Group([
                                        html.Span(":) ", style={"display": "inline-block", "transform": "rotate(90deg)"})
                                        for _ in range(9)
                                    ], gap=12, justify="center", mt="sm"),
                                    ], gap=2),

                                    
                                ], gap="xs"),
                                        p="lg",
                                        style={
                                            "width":           700,
                                            "backgroundColor": colours.beige,
                                            "maxHeight":       "min(900px, calc(100vh - 80px))",
                                            "overflowY":       "auto",
                                        },
                                    ),
                                ], position="bottom-start", withArrow=False, shadow="md", closeOnClickOutside=True),
                       
                        # feedback button in header opens popover feedback form
                        dmc.Popover([
                            dmc.PopoverTarget(
                                nav_button("Feedback"),
                            ),
                            dmc.PopoverDropdown(
                                html.Div(
                                    id="feedback-popover-content",
                                    children=[
                                        html.Div([
                                            html.Div([
                                                dmc.Stack([
                                                    dmc.Text("FEEDBACK FORM", fw=800, size="sm"),
                                                    dmc.Text(
                                                        "Please send us your thoughts, suggestions and feedback, so we can improve. Thank you!",
                                                        size="sm", c=colours.maroon,
                                                    ),

                                                    # website navigation question (static)
                                                    dmc.Text("Did you find the website easy to navigate?",
                                                             fw=600, mt="sm", size="sm"),
                                                    likert_range("difficult", "easy"),
                                                    likert_question("rating-website", "Website navigation"),

                                                    # plus buttons to toggle extra feedback sections
                                                    dmc.Group([
                                                        dmc.Button("+ feedback for VOI", id="btn-voi",
                                                                   variant="outline", fw=700, size="xs", c="dark"),
                                                        dmc.Button("+ feedback for MPE", id="btn-mpe",
                                                                   variant="outline",fw=700, size="xs", c="dark"),
                                                        dmc.Button("+ feedback for Scenario", id="btn-scenario",
                                                                   variant="outline",fw=700, size="xs", c="dark"),
                                                    ], mt="xs"),

                                                    # VOI questions 
                                                    html.Div(id="voi-feedback", style={"display": "none"},
                                                             children=dmc.Stack([
                                                                 dmc.Text("VOI Feedback", fw=600, mt="sm", size="sm"),
                                                                 likert_range("not at all", "very"),
                                                                 likert_question("voi-q1", "Did you find the explanation easy to understand?"),
                                                                 likert_question("voi-q2", "Did the explanation make you feel more confident in the model's prediction?"),
                                                                 likert_question("voi-q3", "Did you find the explanation too complex?"),
                                                             ])),

                                                    # MPE questions 
                                                    html.Div(id="mpe-feedback", style={"display": "none"},
                                                             children=dmc.Stack([
                                                                 dmc.Text("MPE Feedback", fw=600, mt="sm", size="sm"),
                                                                 likert_range("not at all", "very"),
                                                                 likert_question("mpe-q1", "Did you find the explanation easy to understand?"),
                                                                 likert_question("mpe-q2", "Did the explanation make you feel more confident in the model's prediction?"),
                                                                 likert_question("mpe-q3", "Did you find the explanation too complex?"),
                                                             ])),

                                                    # Scenario questions 
                                                    html.Div(id="scenario-feedback", style={"display": "none"},
                                                             children=dmc.Stack([
                                                                 dmc.Text("Scenario Feedback", fw=600, mt="sm", size="sm"),
                                                                 likert_range("not at all", "very"),
                                                                 likert_question("scenario-q1", "Did you find the explanation easy to understand?"),
                                                                 likert_question("scenario-q2", "Did the explanation make you feel more confident in the model's prediction?"),
                                                                 likert_question("scenario-q3", "Did you find the explanation too complex?"),
                                                             ])),

                                                    # open comment
                                                    dmc.Text("Please put any final feedback below:", fw=600, mt="sm", size="sm"),
                                                    dmc.Textarea(
                                                        id="feedback-text",
                                                        minRows=3,
                                                        placeholder="How did the methods help you understand the prediction? Why is it understandable or complicated?",
                                                    ),
                                                    dmc.Text(id="feedback-error", c=colours.maroon, size="sm"),
                                                ], gap="sm"),
                                            ], style={
                                                "overflowY":    "auto",
                                                "flex":         "1 1 0",
                                                "paddingRight": "10px",
                                                "minHeight":    "0",
                                            }),
                                            # submit button 
                                            dmc.Button("Submit", id="submit-feedback", fullWidth=True, mt="md",
                                                       styles={"root": {"borderRadius": "0",
                                                                        "backgroundColor": colours.maroon,
                                                                        "flexShrink": "0"}}),
                                        ], style={
                                            "display":       "flex",
                                            "flexDirection": "column",
                                            "height":        "min(520px, calc(100vh - 120px))",
                                        }),
                                    ],
                                ),
                                p="lg",
                                style={
                                    "width":           500,
                                    "backgroundColor": colours.beige,
                                    "maxHeight":       "min(560px, calc(100vh - 80px))",
                                    "overflow":        "hidden",
                                },
                            ),
                        ], id="feedback-popover", position="bottom-start",
                           withArrow=False, shadow="md", closeOnClickOutside=True),
                    ], style={
                        "display":    "flex",
                        "alignItems": "center",
                        "gap":        "4px",
                    }),
                ], style={
                    "backgroundColor": colours.maroon,
                    "padding":         "5px 8px",
                    "display":         "flex",
                    "alignItems":      "center",
                    "height":          "100%",
                }),
                bg=colours.maroon,
            ),

            #---main----
            dmc.AppShellMain(
                dmc.Stack([
                    dmc.Group(
                        [
                            #---- left: evidence &nodes----
                            html.Div([
                                panel_title("Evidence & Nodes"),
                                html.Div([
                                    dmc.Text("Bayesian Network file:",
                                             fw=700, size="sm", c=colours.grey, mb=4),
                                    dmc.Group([
                                        html.Div(
                                            "cancer.net",
                                            id="filename-display",
                                            style=sunken({
                                                "flex":            1,
                                                "padding":         "2px 6px",
                                                "fontSize":        "14px",
                                                "color":           colours.blue,
                                                "backgroundColor": colours.border_light,
                                                "overflow":        "hidden",
                                                "whiteSpace":      "nowrap",
                                                "textOverflow":    "ellipsis",
                                            })
                                        ),
                                        dcc.Upload(
                                            id='upload-data',
                                            children=html.Button(
                                                'Browse...',
                                                style={
                                                    "backgroundColor": colours.beige,
                                                    "color":           colours.black,
                                                    "padding":         "2px 8px",
                                                    "cursor":          "pointer",
                                                    "fontSize":        "14px",
                                                    "whiteSpace":      "nowrap",
                                                    "borderTop":       f"2px solid {colours.white}",
                                                    "borderLeft":      f"2px solid {colours.white}",
                                                    "borderRight":     f"2px solid {colours.shadow_darkest}",
                                                    "borderBottom":    f"2px solid {colours.shadow_darkest}",
                                                }
                                            ),
                                        ),
                                    ], gap=4, align="center"),
                                ], style={"padding": "6px", "marginBottom": "4px"}),

                                html.Div(
                                    id="nodes-list",
                                    style={
                                        "flex":         1,
                                        "overflowY":    "auto",
                                        "paddingLeft":  "6px",
                                        "paddingRight": "6px",
                                    },
                                ),

                                html.Button(
                                    "Submit Evidence",
                                    id="submit-evidence",
                                    style={
                                        "width":           "calc(100% - 12px)",
                                        "margin":          "6px 6px 6px 6px",
                                        "padding":         "5px",
                                        "backgroundColor": colours.button_bg,
                                        "color":           colours.black,
                                        "cursor":          "pointer",
                                        "fontSize":        "15px",
                                        "borderTop":       f"2px solid {colours.white}",
                                        "borderLeft":      f"2px solid {colours.white}",
                                        "borderRight":     f"2px solid {colours.shadow_darkest}",
                                        "borderBottom":    f"2px solid {colours.shadow_darkest}",
                                    }
                                ),
                            ], style=raised({
                                "flex":            1.5,
                                "display":         "flex",
                                "flexDirection":   "column",
                                "padding":         "0",
                                "backgroundColor": colours.beige,
                                "maxHeight":       "100%",
                                "overflow":        "hidden",
                            })),

                            #----center: inference diagram ---
                            html.Div([
                                html.Div([
                                    html.Span(
                                        "Inference Diagram — cancer.net",
                                        id="center-panel-title",
                                        style={"flex": 1, "fontSize": "15.5px",
                                               "fontWeight": "600"}
                                    ),
                                    dmc.Select(
                                        id="center-view-selector",
                                        data=[
                                            {"value": "diagram", "label": "Diagram"},
                                            {"value": "table", "label": "Table"},
                                        ],
                                        value="diagram", w=120, size="xs",
                                        allowDeselect=False,
                                        styles={"input": {
                                            "borderTop": f"2px solid {colours.shadow_dark}",
                                            "borderLeft": f"2px solid {colours.shadow_dark}",
                                            "borderRight": f"2px solid {colours.white}",
                                            "borderBottom": f"2px solid {colours.white}",
                                            "borderRadius": "0", "fontWeight": "bold", "fontSize": "13px",
                                            "height": "22px", "minHeight": "20px",
                                            "padding": "1px 6px",
                                            "backgroundColor": colours.beige,
                                            "color": colours.blue,
                                        }},
                                    ),
                                ], style={
                                    "backgroundColor": colours.blue,
                                    "color": colours.beige,
                                    "padding": "3px 8px",
                                    "display": "flex",
                                    "alignItems": "center",
                                    "gap": "6px",
                                    "marginBottom": "6px",
                                }),

                                html.Div([
                                    html.Div([
                                        dmc.Text("Legend", size="xs", fw=700, style={
                                            "borderBottom": f"1px solid {colours.mauve}",
                                            "paddingBottom": "2px", "marginBottom": "4px",
                                        }),
                                        dmc.Group([
                                            html.Div(style=raised({
                                                "width": "14px", "height": "14px",
                                                "backgroundColor": colours.regular_node,
                                            })),
                                            dmc.Text("Regular node", size="xs"),
                                        ], gap=6, mb=4),
                                        dmc.Group([
                                            html.Div(style=raised({
                                                "width": "14px", "height": "14px",
                                                "backgroundColor": colours.target_node,
                                            })),
                                            dmc.Text("Target node", size="xs"),
                                        ], gap=6, mb=4),
                                        dmc.Group([
                                            html.Div(style=raised({
                                                "width": "14px", "height": "14px",
                                                "backgroundColor": colours.evidence_node,
                                            })),
                                            dmc.Text("Evidence node", size="xs"),
                                        ], gap=6),
                                    ], id="diagram-legend", style=raised({
                                        "position": "absolute", "top": "10px", "left": "10px",
                                        "backgroundColor": colours.beige,
                                        "padding": "6px 8px", "zIndex": 10,
                                    })),

                                    dmc.LoadingOverlay(
                                        id="loading-overlay", visible=False,
                                        overlayProps={"radius": "sm", "blur": 2,
                                                      "color": colours.beige},
                                        zIndex=10,
                                    ),
                                    html.Iframe(
                                        id='inference-iframe', srcDoc=centered_html,
                                        style={"width": "100%", "height": "100%",
                                               "flex": 1, "border": "none"},
                                    ),
                                    html.Div(id="center-view-table",
                                             style={"display": "none", "flex": 1,
                                                    "overflow": "hidden"}),
                                ], style=sunken({
                                    "flex": 1,
                                    "display": "flex",
                                    "flexDirection": "column",
                                    "position": "relative",
                                    "overflow": "hidden",
                                    "margin": "0 6px 6px 6px",
                                    "backgroundColor": colours.card_bg,
                                })),

                            ], id="inference-paper", style=raised({
                                "flex": 6,
                                "display": "flex",
                                "flexDirection": "column",
                                "padding": "0",
                                "backgroundColor": colours.beige,
                                "overflow": "hidden",
                            })),

                            #----right: explanation panel ----
                            html.Div([
                                panel_title("Explanation Panel"),
                                explanation_selection(),

                                # content box
                                html.Div([
                                    dmc.Text(
                                        id="explanation-description",
                                        fw=570, size="sm", mt="xs", mb="xs",
                                        c=colours.maroon,
                                    ),
                                    html.Div(
                                        id="explain-content",
                                        style={"flex": 1, "display": "flex",
                                               "flexDirection": "column",
                                               "overflow": "hidden"}
                                    ),
                                ], style={
                                    "flex": 1,
                                    "display": "flex",
                                    "flexDirection": "column",
                                    "overflow": "hidden",
                                    "padding": "6px",
                                    "borderLeft": f"2px solid {colours.white}",
                                    "borderRight": f"2px solid {colours.shadow_dark}",
                                }),
                            ], style=raised({
                                "flex": 2.5,
                                "display": "flex",
                                "flexDirection": "column",
                                "padding": "0",
                                "backgroundColor": colours.beige,
                                "maxHeight": "100%",
                                "overflow": "hidden",
                            })),
                        ],
                        align="stretch", gap="md", wrap="nowrap",
                        style={"flex": 1, "minHeight": 0},
                    ),

                    #----seperator----
                    html.Div(style={
                        "height": "6px",
                        "backgroundColor": colours.beige,
                        "borderTop": f"1px solid {colours.white}",
                        "borderBottom": f"1px solid {colours.shadow}",
                    }),

                    #---status bar----
                    html.Div([
                        html.Span(id="status-filename", className="status-item",
                                  children="Network: cancer.net"),
                        html.Span(id="status-target", className="status-item",
                                  children="Target: none"),
                        html.Span(id="status-evidence", className="status-item",
                                  children="Evidence: none"),
                        html.Span(id="status-nodes", className="status-item",
                                  children="Nodes: — | Edges: —"),
                    ], style={
                        "borderTop": f"2px solid {colours.white}",
                        "borderBottom": f"2px solid {colours.shadow}",
                        "backgroundColor": colours.beige,
                        "display": "flex",
                        "justifyContent": "flex-start",
                        "alignItems": "center",
                        "padding": "2px 4px",
                        "gap": "4px",
                    }),

                ], gap=0, style={"height": "100%"}),
                bg=colours.beige,
                style={"display": "flex", "flexDirection": "column",
                       "height": "calc(100vh - 36px)", "overflow": "hidden"},
            ),
        ],
        header={"height": 45},
        padding="xs",
        id="appshell",
    )
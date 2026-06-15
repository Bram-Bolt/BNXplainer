import dash_mantine_components as dmc
import colours
from dash import html, dcc
from components.feedback_helpers import likert_question, likert_range
from components.explanation_selector import explanation_selection
from utils.file_utils import load_placeholder_bn


# raised win95 bevel: light top/left, dark bottom/right
def raised(extra=None):
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


# sunken win95 bevel: dark top/left, light bottom/right
def sunken(extra=None):
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


# panel title bar in blue with beige text
def panel_title(text: str):
    return html.Div(
        text,
        style={
            "backgroundColor": colours.blue,
            "color": colours.beige,
            "padding": "3px 8px",
            "fontSize": "11px",
            "fontWeight": "600",
            "marginBottom": "6px",
        }
    )


# raised Win95-style nav button
def nav_button(label: str):
    return html.Button(
        label,
        className="nav-btn",
        style={
            "backgroundColor": colours.beige,
            "color": colours.black,
            "padding": "2px 12px",
            "fontSize": "13px",
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
                    html.Div(
                        "bnxplainer",
                        style={
                            "color": colours.beige,
                            "fontSize": "15px",
                            "fontWeight": "bold",
                            "flex": 1,
                            "textAlign": "center",
                        }
                    ),
                    html.Div([
                        nav_button("About us"),
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
                                                    dmc.Text("FEEDBACK FORM", fw=700, size="sm"),
                                                    dmc.Text(
                                                        "Please send us your thoughts, suggestions and feedback, so we can improve. Thank you!",
                                                        size="xs", c=colours.grey,
                                                    ),

                                                    # website navigation question (static)
                                                    dmc.Text("Did you find the website easy to navigate?",
                                                             fw=500, mt="sm", size="xs"),
                                                    likert_range("difficult", "easy"),
                                                    likert_question("rating-website", "Website navigation"),

                                                    # plus buttons to toggle extra feedback sections
                                                    dmc.Group([
                                                        dmc.Button("+ feedback for VOI", id="btn-voi",
                                                                   variant="outline", size="xs", c="dark"),
                                                        dmc.Button("+ feedback for MPE", id="btn-mpe",
                                                                   variant="outline", size="xs", c="dark"),
                                                        dmc.Button("+ feedback for Scenario", id="btn-scenario",
                                                                   variant="outline", size="xs", c="dark"),
                                                    ], mt="sm"),

                                                    # VOI questions 
                                                    html.Div(id="voi-feedback", style={"display": "none"},
                                                             children=dmc.Stack([
                                                                 dmc.Text("VOI Feedback", fw=600, mt="sm", size="xs"),
                                                                 likert_range("not at all", "very"),
                                                                 likert_question("voi-q1", "Did you find the explanation easy to understand?"),
                                                                 likert_question("voi-q2", "Did the explanation make you feel more confident in the model's prediction?"),
                                                                 likert_question("voi-q3", "Did you find the explanation too complex?"),
                                                             ])),

                                                    # MPE questions 
                                                    html.Div(id="mpe-feedback", style={"display": "none"},
                                                             children=dmc.Stack([
                                                                 dmc.Text("MPE Feedback", fw=600, mt="sm", size="xs"),
                                                                 likert_range("not at all", "very"),
                                                                 likert_question("mpe-q1", "Did you find the explanation easy to understand?"),
                                                                 likert_question("mpe-q2", "Did the explanation make you feel more confident in the model's prediction?"),
                                                                 likert_question("mpe-q3", "Did you find the explanation too complex?"),
                                                             ])),

                                                    # Scenario questions 
                                                    html.Div(id="scenario-feedback", style={"display": "none"},
                                                             children=dmc.Stack([
                                                                 dmc.Text("Scenario Feedback", fw=600, mt="sm", size="xs"),
                                                                 likert_range("not at all", "very"),
                                                                 likert_question("scenario-q1", "Did you find the explanation easy to understand?"),
                                                                 likert_question("scenario-q2", "Did the explanation make you feel more confident in the model's prediction?"),
                                                                 likert_question("scenario-q3", "Did you find the explanation too complex?"),
                                                             ])),

                                                    # open comment
                                                    dmc.Text("Please put any final feedback below:", fw=500, mt="sm", size="xs"),
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
                                             size="xs", c=colours.grey, mb=4),
                                    dmc.Group([
                                        html.Div(
                                            "cancer.net",
                                            id="filename-display",
                                            style=sunken({
                                                "flex":            1,
                                                "padding":         "2px 6px",
                                                "fontSize":        "11px",
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
                                                    "fontSize":        "11px",
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
                                        "fontSize":        "12px",
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
                                        style={"flex": 1, "fontSize": "11px",
                                               "fontWeight": "600"}
                                    ),
                                    dmc.Select(
                                        id="center-view-selector",
                                        data=[
                                            {"value": "diagram", "label": "Diagram"},
                                            {"value": "table", "label": "Table"},
                                        ],
                                        value="diagram", w=95, size="xs",
                                        allowDeselect=False,
                                        styles={"input": {
                                            "borderTop": f"2px solid {colours.shadow_dark}",
                                            "borderLeft": f"2px solid {colours.shadow_dark}",
                                            "borderRight": f"2px solid {colours.white}",
                                            "borderBottom": f"2px solid {colours.white}",
                                            "borderRadius": "0", "fontSize": "10px",
                                            "height": "18px", "minHeight": "18px",
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
                                        dmc.Text("Legend", size="xs", fw=600, style={
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
                                    "backgroundColor": colours.border_light,
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
                                        size="xs", mt="xs", mb="xs",
                                        c=colours.grey,
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
        header={"height": 36},
        padding="xs",
        id="appshell",
    )
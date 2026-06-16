# Copyright (c) 2026 MSDT Group 2 All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.


"""Build and render variable prediction rows for the centre-panel table view."""

import dash_mantine_components as dmc
import colours
from utils.feature_extraction import extract_bn_features
from dash import html

def build_variable_data(bn, evidence=None, target= None):
    """
    Convert a BayesNet into the list-of-dicts that render_variable_list expects.
    Each entry has:
        name        – node name
        prediction  – state with highest posterior probability
        probability – that probability as a percentage (0-100)
        role        - target, evidence or None
    """
    features = extract_bn_features(bn, evidence=evidence)
    evidence_nodes = set(evidence.keys()) if evidence else set()
    variables = []
    for node in features.get("nodes", []):
        posterior = node.get("posterior", {})
        if not posterior:
            continue
        best_state = max(posterior, key=posterior.get)
        best_prob  = posterior[best_state]

        node_id    = node["id"]
        if node_id == target:
            role = "target"
        elif node_id in evidence_nodes:
            role = "evidence"
        else:
            role = None

        variables.append({
            "name":        node["id"],
            "prediction":  best_state,
            "probability": round(best_prob * 100, 1),
            "role": role,
        })
    return variables

#role node colours
_role_style= {
    "target":   {"backgroundColor": colours.maroon, "color": colours.beige},
    "evidence": {"backgroundColor": colours.blue, "color": colours.beige},}

_role_label= {
    "target": "target",
    "evidence": "evidence",}

# Helper function to display the list of variables in the explanation method
def render_variable_list(variables):
    """Render variable prediction dictionaries as scrollable table rows."""
    if not variables:
        return dmc.Text("No variables available.")

    rows = []

    for var in variables:
        name = var.get("name", "Variable")
        prediction = var.get("prediction", "-")
        prob = var.get("probability", 0)
        role = var.get("role")
    
        if role in _role_style:
            badge = html.Span(
                _role_label[role],
                style={
                    **_role_style[role],
                    "fontSize": "9px",
                    "padding": "1px 5px",
                    "marginLeft": "6px",
                    "verticalAlign": "middle",
                    "fontWeight": "600",
                    "letterSpacing": "0.5px",
                    "textTransform": "uppercase",
                }
            )
        else:
            badge = None

        name_cell= html.Span([name, badge] if badge else [name], style={"flex": 2, "display": "flex", "alignItems": "center"})

        rows.append(
            dmc.Group(
                [
                    name_cell,

                    dmc.Text(prediction, size="sm", style={"flex": 1, "color": colours.maroon}),

                    dmc.Group(
                        [
                            dmc.Progress(
                                value=prob,
                                color= colours.olive,
                                style={"flex": 1, "minWidth": "80px"},
                                radius="xs",
                            ),
                            dmc.Text(f"{prob:.0f}%", size="xs", w=35)
                        ],
                        style={"flex": 1},
                        gap=6
                    )
                ],
                justify="space-between",
                align="center",
                style={
                    "padding": "6px 4px",
                    "borderBottom": f"1px solid {colours.grey}"
                }
            )
        )

    return html.Div(
        dmc.Stack(rows, gap=0),
        style={"height": "100%", "overflowY": "auto"}
    )
    
placeholder_vars = [
    {"name": "Adjuvant therapy", "prediction": "no", "probability": 44},
    {"name": "L1CAM", "prediction": "negative (<10%)", "probability": 67},
    {"name": "LVSI", "prediction": "no", "probability": 59},
    {"name": "Lymf node metastasis", "prediction": "no", "probability": 96},
    {"name": "Myometrium invasion", "prediction": "<50%", "probability": 62},
    {"name": "Survival", "prediction": "Yes", "probability": 96},
]
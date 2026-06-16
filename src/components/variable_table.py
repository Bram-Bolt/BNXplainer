
"""Build and render variable prediction rows for the centre-panel table view."""

import dash_mantine_components as dmc
import colours
from utils.feature_extraction import extract_bn_features


def build_variable_data(bn, evidence=None):
    """
    Convert a BayesNet into the list-of-dicts that render_variable_list expects.
    Each entry has:
        name - node name
        prediction - state with highest posterior probability
        probability - that probability as a percentage (0-100)
    """
    features = extract_bn_features(bn, evidence=evidence)
    variables = []
    for node in features.get("nodes", []):
        posterior = node.get("posterior", {})
        if not posterior:
            continue
        best_state = max(posterior, key=posterior.get)
        best_prob  = posterior[best_state]
        variables.append({
            "name":        node["id"],
            "prediction":  best_state,
            "probability": round(best_prob * 100, 1),
        })
    return variables

def render_variable_list(variables):
    """Render variable prediction dictionaries as scrollable table rows."""
    if not variables:
        return dmc.Text("No variables available.")

    rows = []

    for var in variables:
        name = var.get("name", "Variable")
        prediction = var.get("prediction", "-")
        prob = var.get("probability", 0)

        rows.append(
            dmc.Group(
                [
                    dmc.Text(name, size="sm", style={"flex": 2}),

                    dmc.Text(
                        prediction,
                        size="sm",
                        style={"flex": 1, "color": colours.olive}
                    ),

                    dmc.Group(
                        [
                            dmc.Progress(
                                value=prob,
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

    return dmc.ScrollArea(
        dmc.Stack(rows, gap=0),
        style={"height": "100%"}
    )
    
placeholder_vars = [
    {"name": "Adjuvant therapy", "prediction": "no", "probability": 44},
    {"name": "L1CAM", "prediction": "negative (<10%)", "probability": 67},
    {"name": "LVSI", "prediction": "no", "probability": 59},
    {"name": "Lymf node metastasis", "prediction": "no", "probability": 96},
    {"name": "Myometrium invasion", "prediction": "<50%", "probability": 62},
    {"name": "Survival", "prediction": "Yes", "probability": 96},
]
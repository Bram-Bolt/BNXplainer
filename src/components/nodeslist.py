import dash_mantine_components as dmc
import pyagrum as gum

from dash import html
from utils.feature_extraction import extract_bn_features

def get_nodelist(bn: gum.BayesNet):
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

    return dmc.Stack(node_elements, gap="xs")

"""Render target-selection cards and evidence radio controls for Bayes net nodes."""

import dash_mantine_components as dmc
import pyagrum as gum
import colours
from dash import html
from utils.feature_extraction import extract_bn_features

def get_evidence_list(bn: gum.BayesNet):
    """Build node cards with target buttons and per-state evidence radio cards."""
    features = extract_bn_features(bn)

    node_buttonlist = []

    for node in features.get('nodes', []):
        # Build a buttonlist for each node
        # One button per state
        node_id = node.get('id')
        node_states = node.get('states')
        state_buttons = []
        for state in node_states:
            # Build button, append to state_buttons
            state_buttons.append(
                dmc.RadioCard(
                    withBorder=False, 
                    p = 'xs',
                    mt = 'xs',
                    value=state,
                    children=[
                        dmc.Group([
                            dmc.RadioIndicator(),
                            dmc.Box([
                                dmc.Text(state, fw='bold')
                            ])
                        ], 
                        wrap='nowrap', 
                        align='flex-start'
                        ),
                    ],
                    id={'type': 'evidence-radio-button', 'node': node_id, 'state': state}
                )
            )
    
        # Put everything together
        node_buttonlist.append(
            dmc.Card(
                children=[
                    dmc.Group([
                        dmc.Text(node_id, fw=600),
                        dmc.Button(
                            "Set Target",
                            id={"type": "target-button", "node": node_id},
                            size="xs",
                            variant="outline",
                            color=colours.olive,
                            n_clicks=0,
                        )
                    ], justify="space-between", align="center", mb="xs"),
                    dmc.RadioGroup(
                        id={'type': 'evidence-radiogroup', 'node': node_id},
                        deselectable=True,
                        children=state_buttons
                    )
                ],
                withBorder=True,
                shadow="sm",
                mb="sm",
                bg=colours.beige,
                style={
                    "borderColor": colours.black,
                    "borderWidth": "1px"
                },
                id={"type": "node-card", "node": node_id}
            )
        )

    return dmc.Stack(node_buttonlist, gap="xs")
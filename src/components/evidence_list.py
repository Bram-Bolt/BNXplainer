import dash_mantine_components as dmc
import pyagrum as gum

from dash import html
from utils.feature_extraction import extract_bn_features

def get_evidence_list(bn: gum.BayesNet):
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
                    withBorder=True, 
                    p = 'xs',
                    mt = 'xs',
                    className='checkboxcard-root',
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
                    dmc.RadioGroup(
                        id={'type': 'evidence-radiogroup', 'node': node_id},
                        deselectable=True,
                        children=state_buttons
                    )
                ],
                withBorder=True,
                shadow="sm",
                mb="sm",
                bg="#ece4dc",
                style={
                    "borderColor": "black",
                    "borderWidth": "1px"
                },
                id={"type": "node-card", "node": node_id}
            )
        )

    return dmc.Stack(node_buttonlist, gap="xs")
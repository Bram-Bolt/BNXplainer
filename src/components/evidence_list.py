import dash_mantine_components as dmc
import pyagrum as gum
import colours
from utils.feature_extraction import extract_bn_features

def get_evidence_list(bn: gum.BayesNet):
    features = extract_bn_features(bn)

    node_buttonlist = []

    for node in features.get('nodes', []):
        # Build a buttonlist for each node
        # One button per state
        node_id = node.get('id')
        node_states = node.get('states')

        state_radios= [
            dmc.Radio(
                label=state,
                value=state,
                size="xs",
                styles={
                    "label": {
                        "fontWeight": "bold",
                        "fontSize": "11px",
                        "paddingLeft": "6px",
                        "cursor": "pointer",},
                    "radio": {
                        "cursor": "pointer",},
                    "body": {
                        "alignItems": "center",},},)
            for state in node_states

        ]

    
        # Put everything together
        node_buttonlist.append(
            dmc.Card(
                children=[
                    dmc.Group([
                        dmc.Text(node_id, fw=600, size="sm"),
                        dmc.Button(
                            "Set Target",
                            id={"type": "target-button", "node": node_id},
                            size="xs",
                            variant="outline",
                            color=colours.maroon,
                            n_clicks=0,
                            styles={"root": {
                                "height": "18px", "fontSize": "10px",
                                "padding": "0 6px", "borderRadius": "0",}},
                        )
                    ], justify="space-between", align="center", mb="xs"),
                    dmc.RadioGroup(
                        id={'type': 'evidence-radiogroup', 'node': node_id},
                        deselectable=True,
                        children= dmc.Stack(state_radios, gap=4),
                    )
                ],


                withBorder=False,
                shadow="none",
                mb="xs",
                p="xs",
                bg=colours.card_bg,

                style={
                    "borderTop":    f"2px solid {colours.shadow_dark}",
                    "borderLeft":   f"2px solid {colours.shadow_dark}",
                    "borderRight":  f"2px solid {colours.white}",
                    "borderBottom": f"2px solid {colours.white}",
                    "borderRadius": "0",
                },
                id={"type": "node-card", "node": node_id}
            )
        )

    return dmc.Stack(node_buttonlist, gap="xs")
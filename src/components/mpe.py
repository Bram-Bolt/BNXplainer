# MPE visualization
import dash_mantine_components as dmc
from dash import html

def render_mpe_list(mpe_data):
    if not mpe_data:
        return dmc.Text("No data available.")
    
    result = mpe_data["result"]
    prob = mpe_data["probability"]
    
    components = [
        dmc.Box([
            dmc.Group([
                dmc.Text("Probability of this assignment:", size="sm", fw=700),
                dmc.Text(prob, size="sm")
            ], justify="space-between", mb=4),
        ]),
        dmc.Box([
            dmc.Group([
                dmc.Text("Node", size="sm", fw=700),
                dmc.Text("Most Probable State", fw=700, size="sm")
            ], justify="space-between", mb=4)
        ])
    ]

    for node, state in result.items():
        components.append(
            dmc.Box([
                dmc.Group([
                    dmc.Text(node, fw=700, size="sm"),
                    dmc.Text(state, size="sm")
                ], justify="space-between", mb=4)
            ])
        )

        
    return html.Div(
            dmc.Stack(components, gap="xs"),
            style={"flex": 1, "paddingRight": "11px", "overflowY": "auto"},
        )
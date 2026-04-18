
import dash_mantine_components as dmc
# Helper function to display the list of variables in the explanation method
def render_variable_list(variables):
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
                        style={"flex": 1, "color": "blue"}
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
                    "borderBottom": "1px solid #ddd"
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
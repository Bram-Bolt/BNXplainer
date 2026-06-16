"""
Feedback front-end functions
"""
import dash_mantine_components as dmc
import colours


# helper function to create rating radio buttons for likert scale
# label: method name shown
# question_id: unique id 

def likert_question(question_id,label):
    return dmc.Group([
        dmc.Text(label, size="sm", style={"flex": "1 1 0", "minWidth": 0}),
        dmc.RadioGroup(
            dmc.Group([dmc.Radio(value=str(i)) for i in range(1, 6)], gap=16),
            id=question_id,
        )
    ], align="center")

def likert_range(lowest: str,highest: str):
    return dmc.Group([
        dmc.Text("", style={"flex": "1 1 0"}),
        dmc.Text(lowest, size="xs", fw=500, c=colours.grey, ta="center", style={"width": "40px"}),
        dmc.Text("", style={"width": "80px"}),
        dmc.Text(highest, size="xs", fw=500, c=colours.grey, ta="center", style={"width": "40px"}),

              
    ],gap=0, wrap= "nowrap")

thank_you_message = dmc.Stack([
    dmc.Text("✓", size="xl", fw=700, c=colours.olive, ta="center"),
    dmc.Text("Thank you for your feedback!", fw=700, size="lg", ta="center", c=colours.olive),
    dmc.Text("Your response has been saved successfully.", size="sm", ta="center", c=colours.olive),
], gap="sm", style={
    "backgroundColor": colours.olive_light,
    "border": f"1.5px solid {colours.olive}",
    "borderRadius": "0",
    "padding": "1.5rem",
    "textAlign": "center"
})




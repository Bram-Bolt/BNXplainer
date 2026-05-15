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
        dmc.Text(label, w=250,size="sm"),
        dmc.RadioGroup(
            dmc.Group([dmc.Radio(value=str(i)) for i in range(1, 6)], gap=16),
            id=question_id,
        )
    ], align="center")

def likert_range(lowest: str,highest: str):
    return dmc.Group([
                    dmc.Text("", w=240),
                    dmc.Text(lowest, size="xs", fw=500, w=60, c=colours.grey, ta="center"),
                    dmc.Text("", w=80),
                    dmc.Text(highest, size="xs", fw=500, w=60, c=colours.grey, ta="center"),
                ],gap=0)




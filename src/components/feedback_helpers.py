"""
Feedback front-end functions
"""
import dash_mantine_components as dmc


# helper function to create rating radio buttons for likert scale
# label: method name shown
# question_id: unique id 

def likert_question(question_id,label):
    return dmc.Group([
        dmc.Text(label, w=110,size="sm"),
        dmc.RadioGroup(
            dmc.Group([dmc.Radio(value=str(i)) for i in range(1, 6)], gap=16),
            id=question_id,
        )
    ], align="center")






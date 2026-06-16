"""Build reusable feedback form controls."""

import dash_mantine_components as dmc
import colours


def likert_question(question_id,label):
    """Return a labelled one-to-five radio group for a feedback question."""
    return dmc.Group([
        dmc.Text(label, w=250,size="sm"),
        dmc.RadioGroup(
            dmc.Group([dmc.Radio(value=str(i)) for i in range(1, 6)], gap=16),
            id=question_id,
        )
    ], align="center")

def likert_range(lowest: str,highest: str):
    """Return endpoint labels for a one-to-five Likert scale row."""
    return dmc.Group([
                    dmc.Text("", w=240),
                    dmc.Text(lowest, size="xs", fw=500, w=60, c=colours.grey, ta="center"),
                    dmc.Text("", w=80),
                    dmc.Text(highest, size="xs", fw=500, w=60, c=colours.grey, ta="center"),
                ],gap=0)



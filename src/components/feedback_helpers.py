# Copyright (c) 2026 MSDT Group 2 All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

"""Build reusable feedback form controls."""

import dash_mantine_components as dmc
import colours


def likert_question(question_id,label):
    """Return a labelled one-to-five radio group for a feedback question."""
    return dmc.Group([
        dmc.Text(label, size="sm", style={"flex": "1 1 0", "minWidth": 0}),
        dmc.RadioGroup(
            dmc.Group([dmc.Radio(value=str(i)) for i in range(1, 6)], gap=16),
            id=question_id,
        )
    ], align="center")

def likert_range(lowest: str,highest: str):
    """Return endpoint labels for a one-to-five Likert scale row."""
    return dmc.Group([
        dmc.Text("", style={"flex": "1 1 0"}),
        dmc.Text(lowest, size="xs", fw=500, c=colours.grey, ta="left", style={"width": "60px"}),
        dmc.Text("", style={"width": "80px"}),
        dmc.Text(highest, size="xs", fw=500, c=colours.grey, ta="center", style={"width": "40px"}),

              
    ],gap=0, wrap= "nowrap")

thank_you_message = dmc.Stack([
    dmc.Text("✓", size="xl", fw=700, c=colours.olive, ta="center"),
    dmc.Text("Thank you for your feedback!", fw=700, size="lg", ta="center", c=colours.olive),
    dmc.Text("Your response has been saved successfully.", size="sm", ta="center", c=colours.olive),
], gap="sm", style={
    "backgroundColor": colours.olive_light,
    "borderTop": f"2px solid {colours.white}",
    "borderLeft": f"2px solid {colours.white}",
    "borderRight": f"2px solid {colours.shadow_darkest}",
    "borderBottom": f"2px solid {colours.shadow_darkest}",
    "borderRadius": "0",
    "padding": "1.5rem",
    "textAlign": "center"
})



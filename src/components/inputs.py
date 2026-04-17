"""
Small UI Elements
"""
import dash_mantine_components as dmc


# helper function to create rating radio buttons for likert scale
# label: method name shown
# group_id: unique id so each row is independent
def radio_row(label, group_id):
    return dmc.Group([
        dmc.Text(label, w=110, size="sm"),
        dmc.RadioGroup(
            dmc.Group([dmc.Radio(value=str(i)) for i in range(1, 6)], gap=16),
            id=group_id,
        ),
    ], gap="md")
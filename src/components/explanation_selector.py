"""Render the explanation-method selector used by the right-panel callbacks."""

import dash_mantine_components as dmc
import colours

def explanation_dropdown_selection():
    """Return the VOI, MPE, and scenario explanation dropdown."""
    return dmc.Select(
        id="explanation-selector",
        data=[
            {"label": "VOI Explanation", "value": "voi"},
            {"label": "MPE Explanation", "value": "mpe"},
            {"label": "Scenario Explanation", "value": "scenario"},
        ],
        value="voi",
        size="sm",
        style={"width": 220},
        styles={
            "input": {
                "borderColor": colours.black,
            }
        }
    )
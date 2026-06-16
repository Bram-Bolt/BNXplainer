"""Render scenario explanation objects for the right panel."""

import dash_mantine_components as dmc
import colours
from explanations.scenarios.models import FullScenario
from dash import html


def _prob_to_label(p: float) -> str:
    """Convert a probability into the qualitative label shown in the UI."""
    if p >= 0.99: return "Extremely likely"
    if p >= 0.90: return "Very strongly likely"
    if p >= 0.70: return "Strongly likely"
    if p >= 0.50: return "Moderately likely"
    if p >= 0.30: return "Weakly likely"
    if p >= 0.10: return "Very weakly likely"
    return "Unlikely"


def render_scenario_list(scenarios: list[FullScenario]):
    """Render scenario text, probability, supporting notes, and warnings."""
    if not scenarios:
        return dmc.Text("No scenarios could be generated.", size="sm", c="dimmed")

    components = []

    for fs in scenarios:
        parts = fs.scenario.split("\n", 1)
        condition = parts[0].strip() if len(parts) > 1 else ""
        outcome   = parts[-1].strip()
        prob_pct  = fs.probability * 100
        prob_label = _prob_to_label(fs.probability)

        #card content
        card_children = []

        #condition
        if condition:
            card_children.append(
                html.Div(
                    condition,
                    style={
                        "fontSize": "10px",
                        "fontStyle": "italic",
                        "color": colours.grey,
                        "backgroundColor": colours.beige_dark,
                        "padding": "3px 8px",
                        "marginBottom": "8px",
                        "borderTop": f"1px solid {colours.white}",
                        "borderLeft": f"1px solid {colours.white}",
                        "borderRight": f"1px solid {colours.shadow}",
                        "borderBottom": f"1px solid {colours.shadow}",
                    }
                )
            )

        #outcome sentence
        card_children.append(
            dmc.Text(outcome, fw=500, size="sm", mb=8,
                        style={"padding": "0 8px"})
        )

        #probability bar
        card_children.append(
                html.Div([
                    dmc.Group([
                        dmc.Text(prob_label, size="xs", c="dimmed"),
                        dmc.Text(f"{prob_pct:.0f}%", size="xs", c="dimmed"),
                    ], justify="space-between", mb=4),
                    dmc.Progress(value=prob_pct, size="md", color=colours.olive, radius="0"),
                ], style={"padding": "0 8px 8px 8px"})
            )
    
        #supporting/implausible
        if fs.supporting:
            card_children.append(
                html.Div([
                    dmc.Text("Supporting", size="xs", fw=700, c="dimmed", mb=2),
                    *[dmc.Text(f"· {s}", size="xs", c="dimmed", mb=1) for s in fs.supporting],
                ], style={"padding": "0 8px 6px 8px"})
            )

        if fs.implausible:
            card_children.append(
                html.Div([
                    dmc.Text("Implausible", size="xs", fw=700, c="dimmed", mb=2),
                    *[dmc.Text(f"· {s}", size="xs", c="dimmed", mb=1) for s in fs.implausible],
                ], style={"padding": "0 8px 6px 8px"})
            )
    
        #3d box sunken
        components.append(
            html.Div(
                card_children,
                style={
                    "backgroundColor": colours.beige_mid,
                    "marginBottom": "10px",
                    "borderTop": f"2px solid {colours.shadow}",
                    "borderLeft": f"2px solid {colours.shadow}",
                    "borderRight": f"2px solid {colours.white}",
                    "borderBottom": f"2px solid {colours.white}",
                    "overflow": "hidden",
                }
            )
        )


    return html.Div(
        html.Div(components),
        style={"flex": 1, "paddingRight": "11px", "overflowY": "auto"},
    )

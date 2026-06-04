# components/scenario.py
import dash_mantine_components as dmc
import colours
from explanations.scenarios.models import FullScenario


def _prob_to_label(p: float) -> str:
    if p >= 0.99: return "Extremely likely"
    if p >= 0.90: return "Very strongly likely"
    if p >= 0.70: return "Strongly likely"
    if p >= 0.50: return "Moderately likely"
    if p >= 0.30: return "Weakly likely"
    if p >= 0.10: return "Very weakly likely"
    return "Unlikely"


def render_scenario_list(scenarios: list[FullScenario]):
    if not scenarios:
        return dmc.Text("No scenarios could be generated.", size="sm", c="dimmed")

    components = []

    for i, fs in enumerate(scenarios):
        parts = fs.scenario.split("\n", 1)
        condition = parts[0].strip() if len(parts) > 1 else ""
        outcome   = parts[-1].strip()
        prob_pct  = fs.probability * 100
        prob_label = _prob_to_label(fs.probability)

        if i > 0:
            components.append(dmc.Divider(mb="md", mt="xs"))

        if condition:
            components.append(
                dmc.Text(condition, size="xs", c="dimmed", fs="italic", mb=4)
            )

        components.append(
            dmc.Text(outcome, fw=500, size="sm", mb=6)
        )

        components.append(
            dmc.Box([
                dmc.Group([
                    dmc.Text(prob_label, size="xs", c="dimmed"),
                    dmc.Text(f"{prob_pct:.0f}%", size="xs", c="dimmed"),
                ], justify="space-between", mb=4),
                dmc.Progress(value=prob_pct, size="md", color=colours.olive, radius="xl"),
            ], mb="sm")
        )

        if fs.supporting:
            components.append(
                dmc.Text("Supporting", size="xs", fw=700, c="dimmed", mb=2)
            )
            for s in fs.supporting:
                components.append(
                    dmc.Text(f"· {s}", size="xs", c="dimmed", mb=2)
                )

        if fs.implausible:
            components.append(
                dmc.Text("Implausible", size="xs", fw=700, c="dimmed", mb=2, mt=4)
            )
            for s in fs.implausible:
                components.append(
                    dmc.Text(f"· {s}", size="xs", c="dimmed", mb=2)
                )

    return dmc.ScrollArea(
        dmc.Stack(components, gap="xs"),
        style={"flex": 1, "paddingRight": "11px"},
        offsetScrollbars=False,
        type="hover",
        scrollbarSize=6,
        styles={
            "scrollbar": {
                "backgroundColor": "transparent",
                "&:hover": {"backgroundColor": "transparent"},
            }
        },
    )

"""Render value-of-information scores for the right panel."""

import dash_mantine_components as dmc
import colours

def render_voi_list(voi_data):
    """Render VOI data sorted upstream as a relative EVPI progress bars."""
    if not voi_data:
        return dmc.Text("No data available.")
    
    max_evpi = max(item["evpi"] for item in voi_data) if voi_data else 0
    
    components = []
    for item in voi_data:
        pct = (item["evpi"] / max_evpi) * 100 if max_evpi > 0 else 0
        
        components.append(
            dmc.Box([
                dmc.Group([
                    dmc.Text(item["variable"], fw=500, size="sm"),
                    dmc.Text(f"{item['evpi']:.4f} bits", size="xs", c="dimmed"),
                ], justify="space-between", mb=4),
                dmc.Progress(value=pct, size="md", color= colours.maroon, radius="xl")
            ], mb="md")
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
                "&:hover": {"backgroundColor": "transparent"}
            }
        },
    )
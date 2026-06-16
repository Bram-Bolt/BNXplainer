import dash_mantine_components as dmc

def explanation_selection():
    return dmc.Tabs(
        dmc.TabsList([
            dmc.TabsTab("VOI",      value="voi"),
            dmc.TabsTab("MPE",      value="mpe"),
            dmc.TabsTab("Scenario", value="scenario"),
        ]),
        id="explanation-selector",
        value="voi",
    )
# Copyright (c) 2026 MSDT Group 2 All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

"""Render the explanation-method selector used by the right-panel callbacks."""

import dash_mantine_components as dmc

def explanation_selection():
    """Return the VOI, MPE, and scenario explanation tabs."""
    return dmc.Tabs(
        dmc.TabsList([
            dmc.TabsTab("VOI",      value="voi"),
            dmc.TabsTab("MPE",      value="mpe"),
            dmc.TabsTab("Scenario", value="scenario"),
        ]),
        id="explanation-selector",
        value="voi",
    )
import dash_mantine_components as dmc
from dash import Dash, html
import pyagrum as gum
import pyagrum.lib.notebook as gnb

app = Dash()

# 1. Create a simple Bayesian Network and perform inference
bn = gum.fastBN("Cloudy?->Sprinkler?->WetGrass?<-Rain?<-Cloudy?")
ie = gum.LazyPropagation(bn)
ie.makeInference()

# 2. Get the HTML and increase the 'size' parameter
inference_html = gnb.getInference(bn, size="20") # Increased size

# Wrap the generated HTML in a flexbox div to center it inside the Iframe
centered_html = f"""
<html style="height: 100%; margin: 0;">
    <body style="height: 100%; margin: 0; display: flex; justify-content: center; align-items: center;">
        <div>{inference_html}</div>
    </body>
</html>
"""

layout = dmc.AppShell(
    [
        dmc.AppShellHeader(
            dmc.Group(
                [
                    dmc.Title("Explainable AI", c="white", mx="auto"),
                ],
                h="100%",
                px="md",
            ),
            bg="black",
        ),
        dmc.AppShellMain(
            dmc.Group(
                [
                    dmc.Paper("Input", withBorder=True, p="md", shadow="xl", bg="#ece4dc", style={"flex": 2, "borderColor": "black"}),
                    
                    dmc.Paper(
                        [
                            html.H3("Inference Diagram", style={"marginTop": 0}),
                            html.Iframe(
                                srcDoc=centered_html, # Use the centered HTML wrapper
                                style={
                                    "width": "100%", 
                                    "flex": 1, # Allows the iframe to fill all remaining vertical space
                                    "border": "none"
                                }
                            )
                        ],
                        withBorder=True, 
                        p="md", 
                        shadow="xl", 
                        bg="#ece4dc", 
                        # Update Paper to be a column flex container
                        style={"flex": 5, "borderColor": "black", "display": "flex", "flexDirection": "column"}
                    ), 

                    dmc.Paper("Explain", withBorder=True, p="md", shadow="xl", bg="#ece4dc", style={"flex": 2, "borderColor": "black"}),
                ],
                align="stretch",
                gap="md",
                wrap="nowrap",
                h="calc(100vh - 92px)",
                px="0", 
            ),
            bg="#ece4dc",
        ),
    ],
    header={"height": 60},
    padding="md",
    id="appshell",
)

app.layout = dmc.MantineProvider(layout)

if __name__ == "__main__":
    app.run(debug=True)
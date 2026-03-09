import dash_mantine_components as dmc
from dash import html
from services.inference_service import generate_inference_html


def create_layout():

    centered_html = generate_inference_html()

    return dmc.AppShell(
        [
            dmc.AppShellHeader(
                dmc.Group(
                    [dmc.Title("Explainable AI", c="white", mx="auto")],
                    h="100%",
                    px="md",
                ),
                bg="black",
            ),

            dmc.AppShellMain(
                dmc.Group(
                    [

                        dmc.Paper(
                            "Input",
                            withBorder=True,
                            p="md",
                            shadow="xl",
                            bg="#ece4dc",
                            style={"flex": 2, "borderColor": "black"},
                        ),

                        dmc.Paper(
                            [
                                html.H3("Inference Diagram", style={"marginTop": 0}),
                                html.Iframe(
                                    srcDoc=centered_html,
                                    style={
                                        "width": "100%",
                                        "flex": 1,
                                        "border": "none",
                                    },
                                ),
                            ],
                            withBorder=True,
                            p="md",
                            shadow="xl",
                            bg="#ece4dc",
                            style={
                                "flex": 5,
                                "borderColor": "black",
                                "display": "flex",
                                "flexDirection": "column",
                            },
                        ),

                        dmc.Paper(
                            "Explain",
                            withBorder=True,
                            p="md",
                            shadow="xl",
                            bg="#ece4dc",
                            style={"flex": 2, "borderColor": "black"},
                        ),
                    ],
                    align="stretch",
                    gap="md",
                    wrap="nowrap",
                    h="calc(100vh - 92px)",
                ),
                bg="#ece4dc",
            ),
        ],
        header={"height": 60},
        padding="md",
        id="appshell",
    )
import dash_mantine_components as dmc
from dash import html, dcc, callback, Input, Output, State, no_update, clientside_callback
from services.inference_service import generate_inference_html
from utils.file_utils import load_bn_from_base64

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
                            [
                                dcc.Upload(
                                    id='upload-data',
                                    children=html.Button('Upload File'),
                                ),
                            ],
                            withBorder=True,
                            p="md",
                            shadow="xl",
                            bg="#ece4dc",
                            style={"flex": 2, "borderColor": "black"},
                        ),

                        dmc.Paper(
                            [
                                dmc.LoadingOverlay(
                                    id="loading-overlay",
                                    visible=False,
                                    overlayProps={"radius": "sm", "blur": 2, "color": "#ece4dc"},
                                    zIndex=10,
                                ),
                                html.H3("Inference Diagram", style={"marginTop": 0}),
                                html.Iframe(
                                    id='inference-iframe',
                                    srcDoc=centered_html,
                                    style={
                                        "width": "100%",
                                        "height": "100%",
                                        "flex": 1,
                                        "border": "none",
                                    },
                                ),
                            ],
                            id="inference-paper",
                            withBorder=True,
                            p="md",
                            shadow="xl",
                            bg="#ece4dc",
                            pos="relative",
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


# show overlay when a file is selected
clientside_callback(
    """
    function(contents) {
        if (contents) { return true; }
        return dash_clientside.no_update;
    }
    """,
    Output("loading-overlay", "visible", allow_duplicate=True),
    Input("upload-data", "contents"),
    prevent_initial_call=True,
)


import time

@callback(
    Output('inference-iframe', 'srcDoc'),
    Output('loading-overlay', 'visible'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def handle_uploaded_file(contents, filename):
    if contents is None:
        return no_update, no_update

    start_total = time.perf_counter()

    t0 = time.perf_counter()
    bn = load_bn_from_base64(contents, filename)
    print(f"load_bn_from_base64: {time.perf_counter() - t0:.3f}s")

    t1 = time.perf_counter()
    new_html = generate_inference_html(bn)
    print(f"generate_inference_html: {time.perf_counter() - t1:.3f}s")

    print(f"TOTAL callback time: {time.perf_counter() - start_total:.3f}s")

    return new_html, False
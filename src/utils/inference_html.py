"""Render pyAgrum inference diagrams as embeddable iframe HTML."""

import pyagrum as gum
import pyagrum.lib.notebook as gnb
import colours

def generate_inference_html(bn: gum.BayesNet = gum.fastBN("Cloudy?->Sprinkler?->WetGrass?<-Rain?<-Cloudy?"),
                            target: str = None, 
                            evidence: dict[str, str | int | list[float]] = None) -> str:
    """Return centred, pan-zoomable inference HTML for a Bayes net."""
    if evidence is None and target is None:
        inference_html = gnb.getInference(bn, size="20")
    elif evidence is None:
        inference_html = gnb.getInference(bn, size="20", nodeColor={target: 0.1}, cmapNode=colours.make_node_cmap("olive"))
    elif target is None:
        inference_html = gnb.getInference(bn, size="20", evs=evidence)
    else:
        inference_html = gnb.getInference(bn, size="20", evs=evidence, nodeColor={target: 0.1}, cmapNode=colours.make_node_cmap("olive"))

    # Center visualization inside iframe and enable pan/zoom
    centered_html = f"""
    <html style="height: 100%; margin: 0;">
        <head>
            <script src="/assets/svg-pan-zoom.min.js"></script>
        </head>
        <body style="height: 100%; margin: 0;">
            <div id="svg-container" style="width: 100%; height: 100%; display: flex; justify-content: center; align-items: center;">
                {inference_html}
            </div>
            <script>
                window.onload = function() {{
                    var svg = document.querySelector('svg');
                    if(svg) {{
                        // Ensure the SVG takes up space for zooming
                        svg.style.width = '100%';
                        svg.style.height = '100%';
                        svgPanZoom(svg, {{
                            zoomEnabled: true,
                            controlIconsEnabled: true,
                            fit: true,
                            center: true,
                            minZoom: 0.1,
                            maxZoom: 10
                        }});
                    }}
                }};
            </script>
        </body>
    </html>
    """
    return centered_html

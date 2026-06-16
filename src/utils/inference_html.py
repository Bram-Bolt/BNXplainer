# Copyright (c) 2026 MSDT Group 2 All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

"""Render pyAgrum inference diagrams as embeddable iframe HTML."""

import pyagrum as gum
import pyagrum.lib.notebook as gnb
import colours


# apply brand colours to pyagrum's global config before each render
def _apply_colour_config():
    """Push our brand colours into pyagrum's global config so that
    - regular (non-target, non-evidence) nodes use  regular_node
    - evidence nodes use evidence_node
    The target node fill is controlled via nodeColor+ cmapNode:
    """
    gum.config["notebook", "default_node_bgcolor"] = colours.regular_node
    gum.config["notebook", "default_node_fgcolor"] = colours.black
    gum.config["notebook", "evidence_bgcolor"] = colours.evidence_node
    gum.config["notebook", "evidence_fgcolor"] = colours.white
    gum.config["notebook", "figure_facecolor"] = colours.regular_node 
    gum.config["notebook", "histogram_color"] = colours.olive 

# Generate Inference HTML from Bayesian Network 
def generate_inference_html(bn: gum.BayesNet = gum.fastBN("Cloudy?->Sprinkler?->WetGrass?<-Rain?<-Cloudy?"),
                            target: str = None, 
                            evidence: dict[str, str | int | list[float]] = None) -> str:
    """Return centred, pan-zoomable inference HTML for a Bayesian network."""
    _apply_colour_config()

    if evidence is None and target is None:
        inference_html = gnb.getInference(bn, size="12")
    elif evidence is None:
        inference_html = gnb.getInference(bn, size="12", nodeColor={target: 0.1}, cmapNode=colours.make_node_cmap("target_node"))
    elif target is None:
        inference_html = gnb.getInference(bn, size="12", evs=evidence)
    else:
        inference_html = gnb.getInference(bn, size="12", evs=evidence, nodeColor={target: 0.1}, cmapNode=colours.make_node_cmap("target_node"))

    # Center visualization inside iframe and enable pan/zoom
    centered_html = f"""
    <html style="height: 100%; margin: 0;">
        <head>
            <script src="/assets/svg-pan-zoom.min.js"></script>
            <style>
                @font-face {{
                    font-family: 'W95FA';
                    src: url('/assets/W95FA.otf') format('opentype');
                }}
                svg text, svg tspan {{ font-family: 'W95FA', monospace !important; }}
            </style>

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
                        var panZoom = svgPanZoom(svg, {{
                            zoomEnabled: true,
                            controlIconsEnabled: true,
                            fit: true,
                            center: true,
                            minZoom: 0.1,
                            maxZoom: 10
                        }});
                        // restore saved zoom/pan, or default to 0.8
                        var saved = sessionStorage.getItem('bnx_zoom');
                        if(saved) {{
                            var state = JSON.parse(saved);
                            panZoom.zoom(state.zoom);
                            panZoom.pan(state.pan);
                        }} else {{
                            panZoom.zoom(0.8);
                            panZoom.center();
                        }}
                        // save zoom/pan on every change
                        function saveState() {{
                            sessionStorage.setItem('bnx_zoom', JSON.stringify({{
                                zoom: panZoom.getZoom(),
                                pan:  panZoom.getPan()
                            }}));
                        }}
                        svg.addEventListener('mouseleave', saveState);
                        svg.addEventListener('wheel',      saveState);
                    }}
                }};
            </script>
        </body>
    </html>
    """
    return centered_html
    
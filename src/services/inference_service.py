import pyagrum as gum
import pyagrum.lib.notebook as gnb

# Generate Inference HTML from Bayesian Network 
def generate_inference_html(bn: gum.BayesNet = gum.fastBN("Cloudy?->Sprinkler?->WetGrass?<-Rain?<-Cloudy?")) -> str:
  
    # Run inference
    ie = gum.LazyPropagation(bn)
    ie.makeInference()

    inference_html = gnb.getInference(bn, size="20")

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
import pyagrum as gum
import pyagrum.lib.notebook as gnb

# Generate Inference HTML from Bayesian Network 
def generate_inference_html(bn: gum.BayesNet = gum.fastBN("Cloudy?->Sprinkler?->WetGrass?<-Rain?<-Cloudy?")) -> str:
  
    # Run inference
    ie = gum.LazyPropagation(bn)
    ie.makeInference()

    inference_html = gnb.getInference(bn, size="20")

    # Center visualization inside iframe
    centered_html = f"""
    <html style="height: 100%; margin: 0;">
        <body style="height: 100%; margin: 0; display: flex; justify-content: center; align-items: center;">
            <div style="width: 100%; height: 100%; display: flex; justify-content: center; align-items: center;">
                <div style="max-width: 100%; max-height: 100%; overflow: auto;">
                    {inference_html}
                </div>
            </div>
            <style>
                svg {{
                    max-width: 100%;
                    max-height: 100%;
                    height: auto;
                    width: auto;
                }}
            </style>
        </body>
    </html>
    """

    return centered_html
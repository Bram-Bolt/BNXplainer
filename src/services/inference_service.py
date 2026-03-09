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
            <div>{inference_html}</div>
        </body>
    </html>
    """

    return centered_html
# callbacks/generate_image.py
from dash import callback, Input, Output, no_update, ctx
from utils.file_utils import load_bn_from_base64
from utils.inference_html import generate_inference_html

def register_image_callback(app):
    @callback(
        Output('inference-iframe', 'srcDoc'),
        Input('evidence-store', 'data'),
        Input('bn-store', 'data'),
        prevent_initial_call = True
    )
    def update_image(evidence: dict[str, list], data: dict[str, str]) -> str:
        """This function updates the image of the BayesNet in the center of the page.

        Args:
            evidence (dict[str, list]): Evidence dictionary
            data (dict[str, str]): Data to create the BayesNet object

        Returns:
            str: Inference image HTML string
        """
        if not evidence and not data:
            return no_update
        contents = data['str_bn']
        filename = data['filename']
        bn = load_bn_from_base64(contents, filename)
        
        if ctx.triggered_id == 'bn-store': 
            return generate_inference_html(bn)
        elif ctx.triggered_id == 'evidence-store':
            return generate_inference_html(bn, evidence)
        else: return no_update
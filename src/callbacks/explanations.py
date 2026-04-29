# callbacks/explanations.py
import dash_mantine_components as dmc
from dash import callback, Input, Output, State, ALL
from utils.file_utils import load_bn_from_base64
from explanations.voi import compute_voi, voi_to_display
from components.voi import render_voi_list

def register_explanation_callbacks(app):   
    @callback(
        Output("explanation-description", "children"),
        Input("explanation-selector", "value"),
    )
    def update_explanation_description(method):
        if method == "voi":
            return (
                "Value of Information indicates what variables are most useful "
                "to observe next to reduce uncertainty about the target prediction."
            )
        elif method == "mpe":
            return (
                "Most Probable Explanation identifies the most probable combination of "
                "variable states that explains the observed evidence."
            )
        elif method == "scenario":
            return (
                "Scenario Explanation looks at how different combinations of variable "
                "states influence the target outcome under specified conditions."
            )
        
        return ""

    @callback(
        Output("explanation-title", "children"),
        Input("explanation-selector", "value"),
    )

    def update_explanation_title(method):
        titles = {
            "voi": "Explanation (VOI)",
            "mpe": "Explanation (MPE)",
            "scenario": "Explanation (Scenario)",
        }
        return titles.get(method, "Explanation")
    
    @callback(
        Output('explain-content', 'children'),
        Input('target-store', 'data'),
        Input("explanation-selector", "value"),
        State('evidence-store', 'data'),
        State('bn-store', 'data')
    )
    def update_explanation(target: str, method: str, evidence: dict[str, list[float]], data: dict[str, str]):
        bn = load_bn_from_base64(data['str_bn'], data['filename'])
        print(method)
        if method == "voi":
            try:
                voi_scores = compute_voi(bn=bn, target=target, evidence=evidence)
                voi_data = voi_to_display(voi_scores=voi_scores)

                explain_content = render_voi_list(voi_data=voi_data)
            except Exception as e:
                explain_content = dmc.Text(f"Could not compute VOI: {str(e)}")
        elif method == "mpe":
            explain_content = dmc.Text("This explanation method has yet to be implemented.")
            
        elif method == "scenario":
            explain_content = dmc.Text("This explanation method has yet to be implemented.")

        return_stack = dmc.Stack([
                dmc.Text(f"Target: {target}", fw=600, size="sm", mb="xs"),
                explain_content
            ], h="100%", style={"display": "flex", "flexDirection": "column", "overflow": "hidden"})
        return return_stack
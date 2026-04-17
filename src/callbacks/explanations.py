
from dash import callback, Input, Output

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
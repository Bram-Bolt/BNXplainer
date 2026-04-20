from dash import callback, Input, Output, State, no_update
from db.database import insertEntry
import dash_mantine_components as dmc

def register_feedback_callbacks(app):
    @callback(
        Output("feedback-popover-content","children"),
        Input("submit-feedback", 'n_clicks'),
        State("preferred-explanation", 'value'),
        State('rating-VOI', 'value'),
        State('rating-MPE', 'value'),
        State('rating-scenario', 'value'),
        State("feedback-text", 'value'),
        )
    def feedback_function(n_clicks, preferred_exp, rating_voi, rating_mpe, rating_scenario, feedback_text):
        if not n_clicks:
            return no_update

        insertEntry(
                        str(preferred_exp),
                        int(rating_voi),
                        int(rating_mpe),
                        int(rating_scenario),
                        str(feedback_text))
        
        return dmc.Stack([
            dmc.Text("Thank you for your feedback! ", fw=700, size="lg"),
            dmc.Text("Your response has been submitted successfully.", size="sm",),],
            gap="sm",)
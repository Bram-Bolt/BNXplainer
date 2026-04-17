import dash_mantine_components as dmc
from dash import callback, Input, Output, State, no_update
from db.database import insertEntry


def register_feedback_callbacks(app):
    @callback(
        Output("submit-feedback","children"),
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

        return insertEntry(
                        str(preferred_exp),
                        int(rating_voi),
                        int(rating_mpe),
                        int(rating_scenario),
                        str(feedback_text))
        

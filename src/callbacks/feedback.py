from dash import callback, Input, Output, State, no_update
from db.database import insertEntry
from components.feedback_helpers import likert_question
import dash_mantine_components as dmc



def register_feedback_callbacks(app):
    @callback(
        Output("feedback-popover-content","children"),
        Input("submit-feedback", 'n_clicks'),
        State('rating-website', 'value'),
        State('voi-q1', 'value'),
        State('voi-q2', 'value'),
        State('voi-q3', 'value'),
        State('mpe-q1', 'value'),
        State('mpe-q2', 'value'),
        State('mpe-q3', 'value'),
        State('scenario-q1', 'value'),
        State('scenario-q2', 'value'),
        State('scenario-q3', 'value'),
        State("feedback-text", 'value'),
    )
    def feedback_function(
        n_clicks, website_rating, 
        voi_q1, voi_q2, voi_q3,
        mpe_q1, mpe_q2, mpe_q3,
        scenario_q1, scenario_q2, scenario_q3, 
        feedback_text):
        
        if not n_clicks:
            return no_update
        
        def safe_int(val):
            try:
                return int(val)
            except (TypeError, ValueError):
                return None

        insertEntry(
                    safe_int(website_rating),
                    safe_int(voi_q1),
                    safe_int(voi_q2),
                    safe_int(voi_q3),
                    safe_int(mpe_q1),
                    safe_int(mpe_q2),
                    safe_int(mpe_q3),
                    safe_int(scenario_q1),
                    safe_int(scenario_q2),
                    safe_int(scenario_q3),
                    str(feedback_text) or "")
        
        return dmc.Stack([
            dmc.Text("Thank you for your feedback! ", fw=700, size="lg"),
            dmc.Text("Your response has been submitted successfully.", size="sm",),],
            gap="sm",)
    
    # Toggle hidden questions
    @callback(
    Output("voi-feedback", "style"),
    Output("mpe-feedback", "style"),
    Output("scenario-feedback", "style"),
    Input("btn-voi", "n_clicks"),
    Input("btn-mpe", "n_clicks"),
    Input("btn-scenario", "n_clicks"),
    )
    def toggle_feedback_sections(n_voi, n_mpe, n_scenario):
        def visible_style(n):
            return {"display": "block"} if n and n % 2 == 1 else {"display": "none"}

        return visible_style(n_voi), visible_style(n_mpe), visible_style(n_scenario)
        
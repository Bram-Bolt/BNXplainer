from dash import callback, Input, Output, State, no_update
from db.database import insertEntry
from components.feedback_helpers import likert_question
import dash_mantine_components as dmc
import colours

import numpy as np

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
                return np.nan

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
        
        # VVVV this should not be here VVVV
        # 
        return dmc.Stack([
            dmc.Text("Thank you for your feedback! ", fw=700, size="lg"),
            dmc.Text("Your response has been submitted successfully.", size="sm",),],
            gap="sm",)
        # ^^^^^^^^
        # instead return a boolean to call either succesfull "thank you" like this
        # or a error message of wrong input
        # which should be in pages/home.py
    
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
        section_visible = {
            "display": "block",
            "marginTop": "6px",
            "padding": "8px",
            "backgroundColor": colours.card_bg,
            "borderTop": f"2px solid {colours.shadow_dark}",
            "borderLeft": f"2px solid {colours.shadow_dark}",
            "borderRight": f"2px solid {colours.white}",
            "borderBottom": f"2px solid {colours.white}",
        }
        section_hidden = {"display": "none"}
        
        def is_on(n):
            return n and n % 2 == 1
        
        return (
            section_visible if is_on(n_voi)      else section_hidden,
            section_visible if is_on(n_mpe)      else section_hidden,
            section_visible if is_on(n_scenario) else section_hidden,
        )
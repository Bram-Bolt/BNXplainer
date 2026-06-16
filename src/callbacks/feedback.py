"""Handle feedback form submission and optional feedback section visibility."""

from dash import callback, Input, Output, State, no_update
from db.database import insertEntry
import dash_mantine_components as dmc

import numpy as np

def register_feedback_callbacks(app):
    """Register callbacks that submit feedback and toggle optional form sections."""
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
        """Save submitted feedback and replace the form with a thank-you message.

        The submit button triggers this callback. Rating values are read from the
        feedback form, converted from radio-button strings to integers, and passed to
        the SQLite feedback database helper. Missing optional section values are
        stored as NaN so validation can distinguish complete and incomplete sections.
        """

        if not n_clicks:
            return no_update

        def safe_int(val):
            """Convert a submitted radio-button value to int, or NaN when missing."""
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
        """Show or hide optional feedback sections based on toggle button clicks."""
        def visible_style(n):
            """Return the CSS display style for an optional section."""
            return {"display": "block"} if n and n % 2 == 1 else {"display": "none"}

        return visible_style(n_voi), visible_style(n_mpe), visible_style(n_scenario)

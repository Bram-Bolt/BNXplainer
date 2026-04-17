
from .sliders import register_slider_callbacks
from .explanations import register_explanation_callbacks
from .feedback import register_feedback_callbacks

def register_callbacks(app):
    register_slider_callbacks(app)
    register_explanation_callbacks(app)
    register_feedback_callbacks(app)
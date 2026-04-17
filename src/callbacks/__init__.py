
from .sliders import register_slider_callbacks
from .explanations import register_explanation_callbacks
from .feedback import register_feedback_callbacks
from .upload import register_upload_callbacks
from .target_node import register_target_node_callback
from .nodeslist_rendering import register_nodeslist_rendering_callback

def register_callbacks(app):
    register_slider_callbacks(app)
    register_explanation_callbacks(app)
    register_feedback_callbacks(app)
    register_upload_callbacks(app)
    register_target_node_callback(app)
    register_nodeslist_rendering_callback(app)
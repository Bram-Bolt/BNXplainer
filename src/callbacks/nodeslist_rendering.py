"""Render the target and evidence selector list when the Bayes net changes."""

from dash import callback, Input, Output, no_update
from utils.file_utils import load_bn_from_base64
from components.nodeslist import get_nodelist
from components.evidence_list import get_evidence_list

def register_nodeslist_rendering_callback(app):
    """Register the callback that renders node evidence controls from bn-store."""
    @callback(
        Output('nodes-list', 'children'),
        Input('bn-store', 'data')
    )
    def nodeslist_update(data: dict[str, str]):
        """Load the current Bayes net and render its target/evidence controls."""
        if not data:
            return no_update
        
        bn = load_bn_from_base64(data['str_bn'], data['filename'])

        return get_evidence_list(bn)
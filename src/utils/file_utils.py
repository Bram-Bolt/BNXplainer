# Copyright (c) 2026 MSDT Group 2 All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

"""Load Bayesian network files from Dash upload payloads or local fixtures."""

import os
import base64
import tempfile
import pyagrum as gum

def load_bn_from_base64(contents: str, filename: str) -> gum.BayesNet:
    """Load a pyAgrum Bayes net from Dash base64 upload contents."""
    _, extension = os.path.splitext(filename)
    extension = extension.lower().lstrip(".") # get extension

    # check if extension is allowed
    allowed_exts = gum.availableBNExts().split("|") 
    if extension not in allowed_exts:
        raise ValueError(
            f"Unsupported Bayesian Network format: .{extension}. "
            f"Supported formats: {', '.join(allowed_exts)}"
        )

    # Decode
    try:
        content_type, content_string = contents.split(',')
        decoded_bytes = base64.b64decode(content_string)
    except Exception as e:
        raise ValueError(f"Failed to decode base64 content: {e}")

    # Make a temporary file
    fd, temp_path = tempfile.mkstemp(suffix=f".{extension}")

    # load BN
    try:
        with os.fdopen(fd, 'wb') as tmp:
            tmp.write(decoded_bytes)

        bn = gum.loadBN(temp_path)
        return bn

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
            

def load_placeholder_bn(path):
    """Return a local Bayes net file encoded as a Dash upload-style data URL."""
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    return f"data:application/octet-stream;base64,{encoded}"
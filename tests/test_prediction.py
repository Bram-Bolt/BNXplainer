# Copyright (c) 2026 MSDT Group 2 All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

"""Tests for target posterior prediction summaries."""

import base64
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from utils.file_utils import load_bn_from_base64
from utils.prediction import compute_prediction

def load_cancer_bn():
    """Load the bundled cancer network through the upload decoding path."""
    path = Path("src/example_bns/cancer.net")
    encoded = base64.b64encode(path.read_bytes()).decode("utf-8")
    return load_bn_from_base64(f"X,{encoded}", "cancer.net")

def test_prediction_returns_all_states():
    """Prediction output contains every state of the requested target."""
    bn = load_cancer_bn()
    output = compute_prediction(bn, target="Cancer", evidence={})
    expected_states = set(bn.variable("Cancer").labels())
    assert set(output["states"]) == expected_states

def test_prediction_probabilities_sum_to_one():
    """Posterior probabilities for the target sum to one."""
    bn = load_cancer_bn()
    output = compute_prediction(bn, target="Cancer", evidence={})
    total = sum(output["probabilities"].values())
    assert abs(total - 1.0) < 1e-5

def test_prediction_most_likely_state_is_valid():
    """The most likely state is one of the target's known labels."""
    bn = load_cancer_bn()
    output = compute_prediction(bn, target="Cancer", evidence={})
    assert output["most_likely_state"] in output["states"]

def test_prediction_most_likely_probability_is_max():
    """The reported most likely probability equals the maximum posterior."""
    bn = load_cancer_bn()
    output = compute_prediction(bn, target="Cancer", evidence={})
    assert output["most_likely_probability"] == max(output["probabilities"].values())

def test_prediction_changes_with_evidence():
    """Observed evidence changes the target posterior distribution."""
    bn = load_cancer_bn()
    no_evidence = compute_prediction(bn, target="Cancer", evidence={})
    with_evidence = compute_prediction(bn, target="Cancer", evidence={"Smoker": 0})
    assert no_evidence["probabilities"] != with_evidence["probabilities"]

# Copyright (c) 2026 MSDT Group 2 All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

"""Tests for value-of-information scoring."""

import base64
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from utils.file_utils import load_bn_from_base64
from explanations.voi import compute_voi

def load_cancer_bn():
    """Load the bundled cancer network through the upload decoding path."""
    path = Path("src/example_bns/cancer.net")
    encoded = base64.b64encode(path.read_bytes()).decode("utf-8")
    return load_bn_from_base64(f"X,{encoded}", "cancer.net")

def test_voi_excludes_target_and_evidence():
    """VOI candidates exclude the target and already observed variables."""
    bn = load_cancer_bn()
    scores = compute_voi(bn, target="Cancer", evidence={"Pollution": 0})
    assert "Cancer" not in scores
    assert "Pollution" not in scores

def test_voi_scores_are_nonnegative():
    """Computed VOI scores are non-negative within numerical tolerance."""
    bn = load_cancer_bn()
    scores = compute_voi(bn, target="Cancer", evidence={})
    for var, score in scores.items():
        assert score >= -1e-9

def test_voi_sorted_descending():
    """VOI scores are sorted from highest to lowest."""
    bn = load_cancer_bn()
    scores = compute_voi(bn, target="Cancer", evidence={})
    values = list(scores.values())
    assert values == sorted(values, reverse=True)

def test_voi_returns_all_unobserved():
    """VOI returns all non-target variables that are not observed."""
    bn = load_cancer_bn()
    scores = compute_voi(bn, target="Cancer", evidence={"Pollution": 0})
    expected = set(bn.names()) - {"Cancer", "Pollution"}
    assert set(scores.keys()) == expected

def test_voi_xray_ranks_above_smoker():
    """Xray provides more information than Smoker in the baseline cancer net."""
    bn = load_cancer_bn()
    scores = compute_voi(bn, target="Cancer", evidence={})
    assert scores["Xray"] > scores["Smoker"]

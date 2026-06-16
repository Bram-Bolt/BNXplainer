# Copyright (c) 2026 MSDT Group 2 All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

"""Tests for serialising Bayes net features for the Dash UI."""

import pyagrum as gum
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from utils.feature_extraction import extract_bn_features


def test_extract_features_returns_expected_structure():
    """Feature extraction returns the top-level keys and node counts."""
    bn = gum.loadBN("src/example_bns/cancer.net")
    features = extract_bn_features(bn)

    assert set(features) == {"nodes", "edges", "potentials", "evidence"}
    assert features["evidence"] == {}
    assert len(features["nodes"]) == 5
    assert len(features["potentials"]) == 5
    assert {node["id"] for node in features["nodes"]} == set(bn.names())


def test_extract_features_returns_expected_edges_and_posteriors():
    """Extracted edges, evidence, and posterior maps match the cancer network."""
    bn = gum.loadBN("src/example_bns/cancer.net")
    features = extract_bn_features(bn, evidence={"Smoker": "True"})

    assert {
        (edge["source"], edge["target"])
        for edge in features["edges"]
    } == {
        ("Pollution", "Cancer"),
        ("Smoker", "Cancer"),
        ("Cancer", "Xray"),
        ("Cancer", "Dyspnoea"),
    }
    assert features["evidence"] == {"Smoker": "True"}

    for node in features["nodes"]:
        assert set(node) == {"id", "states", "parents", "children", "posterior"}
        assert set(node["posterior"]) == set(node["states"])

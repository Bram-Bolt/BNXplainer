# Copyright (c) 2026 MSDT Group 2 All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

"""Translate legacy slider values into pyAgrum evidence and updated BN features."""

import pyagrum as gum
from utils.feature_extraction import extract_bn_features


def slider_values_to_evidence(
    slider_values: dict[str, list[float]]
) -> dict[str, list[float]]:
    """Convert slider percentage values to evidence format for pyAgrum.

    Converts slider values (0-100) to probabilities (0-1) that sum to 1.

    Args:
        slider_values (dict): Dictionary of {node_name: [percentage_per_state]}

    Returns:
        dict: Evidence in pyAgrum format {node_name: [prob_per_state]}
    """
    evidence = {}
    for node_name, percentages in slider_values.items():
        total = sum(percentages)
        if total == 0:
            continue
        evidence[node_name] = [p / total for p in percentages]
    return evidence


def update_bn_from_sliders(
    bn: gum.BayesNet,
    slider_values: dict[str, list[float]]
) -> dict:
    """Update the Bayesian network based on slider values.

    Takes slider values from the UI, converts them to evidence,
    and returns updated network features with new posterior probabilities.

    Args:
        bn (gum.BayesNet): The Bayesian network to update
        slider_values (dict): Dictionary of {node_name: [percentage_per_state]}

    Returns:
        dict: Updated network features including new posteriors.
              Same format as extract_bn_features().
    """
    evidence = slider_values_to_evidence(slider_values)
    return extract_bn_features(bn, evidence)

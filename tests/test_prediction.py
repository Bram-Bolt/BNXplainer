import base64
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from utils.file_utils import load_bn_from_base64
from utils.prediction import compute_prediction

def load_cancer_bn():
    path = Path("src/example_bns/cancer.net")
    encoded = base64.b64encode(path.read_bytes()).decode("utf-8")
    return load_bn_from_base64(f"X,{encoded}", "cancer.net")

def test_prediction_returns_all_states():
    bn = load_cancer_bn()
    output = compute_prediction(bn, target="Cancer", evidence={})
    expected_states = set(bn.variable("Cancer").labels())
    assert set(output["states"]) == expected_states

def test_prediction_probabilities_sum_to_one():
    bn = load_cancer_bn()
    output = compute_prediction(bn, target="Cancer", evidence={})
    total = sum(output["probabilities"].values())
    assert abs(total - 1.0) < 1e-5

def test_prediction_most_likely_state_is_valid():
    bn = load_cancer_bn()
    output = compute_prediction(bn, target="Cancer", evidence={})
    assert output["most_likely_state"] in output["states"]

def test_prediction_most_likely_probability_is_max():
    bn = load_cancer_bn()
    output = compute_prediction(bn, target="Cancer", evidence={})
    assert output["most_likely_probability"] == max(output["probabilities"].values())

def test_prediction_changes_with_evidence():
    bn = load_cancer_bn()
    no_evidence = compute_prediction(bn, target="Cancer", evidence={})
    with_evidence = compute_prediction(bn, target="Cancer", evidence={"Smoker": 0})
    assert no_evidence["probabilities"] != with_evidence["probabilities"]

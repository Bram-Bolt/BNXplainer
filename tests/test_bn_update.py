import base64
from pathlib import Path
import pyagrum as gum
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from utils.file_utils import load_bn_from_base64
from utils.bn_update import slider_values_to_evidence, update_bn_from_sliders

def load_cancer_bn():
    path = Path("src/example_bns/cancer.net")
    encoded = base64.b64encode(path.read_bytes()).decode("utf-8")
    return load_bn_from_base64(f"X,{encoded}", "cancer.net")

def test_slider_values_convert_to_probabilities():
    result = slider_values_to_evidence({"Cancer": [70.0, 30.0]})
    assert abs(result["Cancer"][0] - 0.7) < 1e-6
    assert abs(result["Cancer"][1] - 0.3) < 1e-6

def test_slider_values_sum_to_one():
    result = slider_values_to_evidence({"Cancer": [60.0, 40.0]})
    assert abs(sum(result["Cancer"]) - 1.0) < 1e-6

def test_empty_slider_values_skipped():
    result = slider_values_to_evidence({"Cancer": [0.0, 0.0]})
    assert "Cancer" not in result

def test_update_bn_returns_nodes():
    bn = load_cancer_bn()
    result = update_bn_from_sliders(bn, {"Smoker": [80.0, 20.0]})
    assert "nodes" in result
    assert "edges" in result

def test_update_bn_changes_posteriors():
    bn = load_cancer_bn()
    no_evidence = update_bn_from_sliders(bn, {})
    with_evidence = update_bn_from_sliders(bn, {"Smoker": [100.0, 0.0]})
    cancer_no_ev = next(n for n in no_evidence["nodes"] if n["id"] == "Cancer")
    cancer_with_ev = next(n for n in with_evidence["nodes"] if n["id"] == "Cancer")
    assert cancer_no_ev["posterior"] != cancer_with_ev["posterior"]

test_slider_values_convert_to_probabilities()
test_slider_values_sum_to_one()
test_empty_slider_values_skipped()
test_update_bn_returns_nodes()
test_update_bn_changes_posteriors()

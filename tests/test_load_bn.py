import base64
from pathlib import Path
import pyagrum as gum
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from src.utils.file_utils import load_bn_from_base64


def test_load_cancer_bn():
    path = Path("src/example_bns/cancer.net")

    encoded = base64.b64encode(path.read_bytes()).decode("utf-8")
    contents = f"X,{encoded}"

    bn = load_bn_from_base64(contents, "cancer.net")

    assert isinstance(bn, gum.BayesNet)
    assert bn.size() == 5
    assert set(bn.names()) == {"Pollution", "Smoker", "Cancer", "Xray", "Dyspnoea"}

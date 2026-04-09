import pyagrum as gum
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from src.services.inference_service import extract_bn_features

bn = gum.loadBN("src/example_bns/cancer.net")
features = extract_bn_features(bn) # Passes the bn

# TODO proper testing function 

print(features.keys())
print(features["nodes"])
print(features["edges"])
print(features["potentials"])
print(features["evidence"]) 

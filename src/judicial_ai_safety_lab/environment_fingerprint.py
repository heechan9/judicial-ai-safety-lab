"""Record reproducibility environment without claiming historical identity."""
import hashlib,json,platform,sys

def build_environment_fingerprint(*,dependencies=None,environment=None,source_commit=None):
    payload={
      "system":platform.system(),
      "python":platform.python_version(),
      "executable":sys.executable,
      "dependencies":dict(sorted((dependencies or {}).items())),
      "environment":dict(sorted((environment or {}).items())),
      "source_commit":source_commit,
    }
    digest=hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    return {"fingerprint":digest,"environment":payload,
            "historical_environment_proven":False,
            "note":"Matching environment metadata is necessary for reproducibility checks but does not prove historical identity."}

def compare_environment(reference,current):
    return {"metadata_match":reference["fingerprint"]==current["fingerprint"],
            "historical_environment_proven":False}

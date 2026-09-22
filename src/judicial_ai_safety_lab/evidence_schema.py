from datetime import datetime, timezone
import os

SCHEMA_VERSION="jaisl.evidence.v3"

def build_evidence_metadata(*, fixture_version, evaluation_version, commit_sha=None):
    return {
      "schema":SCHEMA_VERSION,
      "evaluated_at":datetime.now(timezone.utc).isoformat(),
      "fixture_version":fixture_version,
      "evaluation_version":evaluation_version,
      "commit_sha":commit_sha or os.getenv("GITHUB_SHA") or "local-unpinned"
    }

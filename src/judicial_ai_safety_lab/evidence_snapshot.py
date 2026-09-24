"""Pinned evidence snapshot contract inspired by cross-project evidence views."""
import re

SHA40=re.compile(r"^[0-9a-f]{40}$")
SHA64=re.compile(r"^[0-9a-f]{64}$")

def validate_snapshot(snapshot):
    required={"repository","revision","checked_at","files"}
    if not isinstance(snapshot,dict) or set(snapshot)!=required: raise ValueError("snapshot schema mismatch")
    if not SHA40.fullmatch(snapshot["revision"]): raise ValueError("revision must be full git SHA")
    if not isinstance(snapshot["files"],dict) or not snapshot["files"]: raise ValueError("snapshot files required")
    for path,meta in snapshot["files"].items():
        if (not isinstance(path,str) or not path or path.startswith("/") or chr(92) in path or ":" in path or ".." in path.split("/")): raise ValueError("unsafe snapshot path")
        if not isinstance(meta,dict) or set(meta)!={"sha256","role"}: raise ValueError("file metadata schema mismatch")
        if not SHA64.fullmatch(meta["sha256"]): raise ValueError("invalid snapshot SHA256")
        if not isinstance(meta["role"],str) or not meta["role"]: raise ValueError("file role required")
    return {"valid":True,"revision":snapshot["revision"],"file_count":len(snapshot["files"])}

def lineage_match(*,source_hash,analysis_input_hash):
    if not SHA64.fullmatch(source_hash) or not SHA64.fullmatch(analysis_input_hash):
        raise ValueError("lineage hashes must be SHA256")
    return {"matches":source_hash==analysis_input_hash,
            "status":"MATCH" if source_hash==analysis_input_hash else "MISMATCH"}

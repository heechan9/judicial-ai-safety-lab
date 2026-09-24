"""Read-only integrity audit for an exported evidence bundle.

PASS means files match the manifest. It does not authenticate the operator,
rerun evaluation, or establish independent verification.
"""
import hashlib, json, re, math
from pathlib import Path, PurePosixPath

SHA256_RE=re.compile(r"^[0-9a-f]{64}$")

def _digest(path):
    h=hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda:stream.read(1024*1024),b""): h.update(block)
    return h.hexdigest()

def _unique_pairs(pairs):\n    out={}\n    for key,value in pairs:\n        if key in out: raise ValueError("duplicate JSON key")\n        out[key]=value\n    return out\n\ndef _reject_constant(value):\n    raise ValueError("non-finite JSON value")\n\ndef audit_bundle(directory):
    root=Path(directory)
    if root.is_symlink() or not root.is_dir(): raise ValueError("bundle must be a real directory")
    root=root.resolve(); manifest_path=root/"manifest.json"
    if not manifest_path.is_file(): raise ValueError("missing manifest.json")
    manifest=json.loads(manifest_path.read_text(encoding="utf-8"), object_pairs_hook=_unique_pairs, parse_constant=_reject_constant)
    expected=manifest.get("artifact_sha256")
    if not isinstance(expected,dict) or not expected: raise ValueError("missing artifact manifest")
    for name,value in expected.items():
        p=PurePosixPath(name)
        if p.is_absolute() or ".." in p.parts or chr(92) in name or ":" in name or p.as_posix()!=name:
            raise ValueError("unsafe manifest path")
        if not isinstance(value,str) or not SHA256_RE.fullmatch(value): raise ValueError("invalid sha256")
    actual={}
    for p in sorted(root.rglob("*")):
        if p.is_symlink(): raise ValueError("symlinks are not accepted")
        if p.is_file() and p.name!="manifest.json": actual[p.relative_to(root).as_posix()]=_digest(p)
    added=sorted(actual.keys()-expected.keys()); removed=sorted(expected.keys()-actual.keys())
    changed=sorted(k for k in actual.keys()&expected.keys() if actual[k]!=expected[k])
    return {"integrity_status":"FAIL" if added or removed or changed else "PASS",
            "checked_files":len(actual),"added":added,"removed":removed,"changed":changed,
            "limitation":"Integrity only; not authenticity, metric validation, or independent rerun."}

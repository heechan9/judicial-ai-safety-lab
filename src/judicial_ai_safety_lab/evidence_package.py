"""Build an atomic evidence package manifest.

The package records what existed at one evaluation boundary. It does not claim
the artifacts are authentic, legally valid, or independently reproduced.
"""
import hashlib,json
from pathlib import Path

def _sha(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda:f.read(1024*1024),b""): h.update(block)
    return h.hexdigest()

def build_manifest(root,paths,*,run_id,status,metadata=None):
    root=Path(root).resolve()
    if not root.is_dir(): raise ValueError("root must be a directory")
    entries={}
    for item in paths:
        p=(root/item).resolve()
        try: rel=p.relative_to(root).as_posix()
        except ValueError: raise ValueError("artifact escapes package root")
        if rel in entries: raise ValueError("duplicate artifact path")
        if p.is_symlink() or not p.is_file(): raise ValueError("artifact must be a real file")
        entries[rel]={"sha256":_sha(p),"bytes":p.stat().st_size}
    return {
      "schema":"jaisl.evidence-package.v1",
      "run_id":run_id,
      "status":status,
      "metadata":metadata or {},
      "artifacts":entries,
      "limitations":[
        "hash integrity is not authenticity",
        "package creation is not independent verification",
        "status records execution state only",
      ],
    }

def write_manifest(path,manifest):
    Path(path).write_text(json.dumps(manifest,ensure_ascii=False,indent=2,allow_nan=False),encoding="utf-8")

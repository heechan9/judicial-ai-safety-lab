"""Build an atomic evidence package manifest.

The package records what existed at one evaluation boundary. It does not claim
the artifacts are authentic, legally valid, or independently reproduced.
"""
import hashlib,json
from pathlib import Path

def _sha(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda:f.read(1024*1024),b""):
            h.update(block)
    return h.hexdigest()

def build_manifest(root,paths,*,run_id,status,metadata=None):
    raw_root=Path(root)
    if raw_root.is_symlink() or not raw_root.is_dir():
        raise ValueError("root must be a real directory")
    root=raw_root.resolve()
    if not isinstance(run_id,str) or not run_id.strip(): raise ValueError("run_id required")
    if not isinstance(status,str) or not status.strip(): raise ValueError("status required")
    entries={}
    for item in paths:
        if not isinstance(item,(str,Path)): raise ValueError("artifact path must be text/path")
        raw=root/item
        if raw.is_symlink(): raise ValueError("artifact symlinks are not accepted")
        p=raw.resolve()
        try:
            rel=p.relative_to(root).as_posix()
        except ValueError:
            raise ValueError("artifact escapes package root")
        if rel in entries: raise ValueError("duplicate artifact path")
        if not p.is_file(): raise ValueError("artifact must be a real file")
        entries[rel]={"sha256":_sha(p),"bytes":p.stat().st_size}
    return {
      "schema":"jaisl.evidence-package.v1",
      "run_id":run_id.strip(),
      "status":status.strip(),
      "metadata":metadata or {},
      "artifacts":entries,
      "limitations":[
        "hash integrity is not authenticity",
        "package creation is not independent verification",
        "status records execution state only",
      ],
    }

def write_manifest(path,manifest):
    p=Path(path)
    with p.open("x",encoding="utf-8") as f:
        json.dump(manifest,f,ensure_ascii=False,indent=2,allow_nan=False)

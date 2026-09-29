"""Build a blinded expert-review packet from frozen case outputs."""
import hashlib,json

def _hash(value):
    return hashlib.sha256(json.dumps(
        value,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False
    ).encode()).hexdigest()

def build_expert_packet(cases,*,target_commit,packet_version="v1"):
    if not isinstance(cases,list) or not cases:
        raise ValueError("cases must be a non-empty list")
    blinded=[]
    for i,row in enumerate(cases,1):
        if not isinstance(row,dict): raise ValueError("case rows must be objects")
        required={"case_id","source_refs","system_output","review_reason"}
        if not required.issubset(row): raise ValueError("case row missing required fields")
        blinded.append({
          "review_case_id":f"E{i:03d}",
          "case_id":row["case_id"],
          "source_refs":row["source_refs"],
          "system_output":row["system_output"],
          "review_reason":row["review_reason"],
        })
    return {
      "schema":"jaisl.expert-packet.v1",
      "packet_version":packet_version,
      "target_commit":target_commit,
      "cases":blinded,
      "packet_hash":_hash(blinded),
      "instructions":{
        "evaluate":"source traceability, status correctness, uncertainty, review routing, explanation clarity",
        "do_not_evaluate":"preferred judgment, sentence, verdict, or political/legal-policy preference",
      },
    }

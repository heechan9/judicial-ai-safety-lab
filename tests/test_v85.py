import json
from pathlib import Path
import pytest
from judicial_ai_safety_lab.public_discovery import validate_public_discovery
from judicial_ai_safety_lab.discovery_cli import main as discovery_main

def test_committed_public_discovery_pool_is_valid_and_unfrozen():
    path=Path(__file__).resolve().parents[1]/"data/pilot/public_precedent_discovery_v1.json"
    doc=json.loads(path.read_text(encoding="utf-8"))
    result=validate_public_discovery(doc)
    assert result["valid"]
    assert result["case_count"]==30
    assert result["domain_counts"]=={"civil":20,"criminal":10}
    assert result["discovery_only"] and not result["pilot_selection_frozen"]

def test_public_discovery_rejects_nonofficial_url():
    doc={
      "schema":"jaisl.public-precedent-discovery.v1",
      "source_site":"법제처 국가법령정보센터",
      "discovery_method":"public web discovery from official precedent pages",
      "discovered_at":"2026-09-29",
      "discovery_only":True,
      "pilot_selection_frozen":False,
      "note":"candidate pool",
      "cases":[{
        "source_id":"WEBPREC-1","prec_seq":"1","domain":"civil","title":"x","case_number":"1다1",
        "decision_date":"2026-01-01","court":"대법원","source_url":"https://example.com/?precSeq=1"
      }]
    }
    with pytest.raises(ValueError):
        validate_public_discovery(doc)

def test_discovery_cli(tmp_path,capsys):
    doc={
      "schema":"jaisl.public-precedent-discovery.v1",
      "source_site":"법제처 국가법령정보센터",
      "discovery_method":"public web discovery from official precedent pages",
      "discovered_at":"2026-09-29","discovery_only":True,"pilot_selection_frozen":False,
      "note":"candidate pool","cases":[{
        "source_id":"WEBPREC-1","prec_seq":"1","domain":"civil","title":"x","case_number":"1다1",
        "decision_date":"2026-01-01","court":"대법원","source_url":"https://www.law.go.kr/precInfoP.do?precSeq=1"
      }]
    }
    p=tmp_path/"d.json"; p.write_text(json.dumps(doc,ensure_ascii=False),encoding="utf-8")
    discovery_main(["--input",str(p)])
    out=json.loads(capsys.readouterr().out)
    assert out["case_count"]==1 and out["valid"]

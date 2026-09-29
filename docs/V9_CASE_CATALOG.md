# v9.0 discovery → case catalog → pilot readiness

v9.0 adds an explicit intermediate layer between public precedent discovery and a frozen real-data pilot.

## Why

A public web discovery record is not equivalent to:
- API raw evidence,
- normalized verified detail,
- frozen pilot membership,
- expert-review readiness.

The v9.0 case catalog preserves this distinction for every discovered case.

## Flow

public discovery pool
→ stable case catalog
→ API raw evidence verification
→ normalized detail verification
→ frozen pilot selection
→ pilot-eligible case
→ JAISL assessment
→ expert-packet-ready case

## Case catalog status

Every case built directly from the current public discovery pool starts with:
- evidence_status = PUBLIC_WEB_DISCOVERY_ONLY
- api_raw_verified = false
- normalized_detail_verified = false
- pilot_eligible = false
- expert_packet_ready = false

These values cannot be upgraded by inference.

## Commands

```bash
jaisl-catalog --discovery data/pilot/public_precedent_discovery_v1.json --output evidence/pilot/catalog.json
jaisl-readiness --catalog evidence/pilot/catalog.json --output evidence/pilot/readiness.json
```

With later evidence and frozen selection:

```bash
jaisl-readiness --catalog evidence/pilot/catalog.json --evidence evidence/pilot/source-evidence.json --selection evidence/pilot/selection.json --output evidence/pilot/readiness.json
```

A case is pilot-eligible only if all three are true:
1. API raw evidence verified
2. normalized detail verified
3. included in the frozen pilot selection

Discovery alone never satisfies the gate.

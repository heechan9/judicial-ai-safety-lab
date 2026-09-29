# v8.0 real-data pilot runbook

## Goal
Run a public-official-precedent pilot without committing credentials or private case data.

## 1. Configure credential locally

PowerShell:
```powershell
$env:LAW_OC="YOUR_OC_VALUE"
```

Do not paste the credential into chat, commit it, write it into JSON, or print it in CI logs.

## 2. Collect raw official precedent search responses

```powershell
jaisl-precedent-collect --query "손해배상" --display 20 --page 1 --output evidence/raw/precedent-damages-p1.json
```

The output stores:
- source name
- endpoint contract
- query/page/display
- UTC retrieval time
- raw official response
- canonical SHA-256 of the raw response
- `credential_stored=false`

It does not store LAW_OC.

## 3. Normalize candidates
Convert official result rows into candidate JSON with stable `source_id`, title, stratum, and metadata.
Do not inspect JAISL outcome scores before the pilot sample is frozen.

## 4. Freeze pilot selection
Prepare a targets file such as:
```json
{"stable":10,"conflict":10,"change":10}
```

Then:
```powershell
jaisl-pilot --candidates evidence/pilot/candidates.json --targets evidence/pilot/targets.json --selection-note "pre-registered before outcome review" --output evidence/pilot/selection.json
```

## 5. Create frozen real-data manifest
```powershell
jaisl-realdata --records evidence/pilot/normalized-records.json --source-name "국가법령정보 공동활용" --source-url "https://www.law.go.kr/DRF/" --cutoff "2026-09-29T00:00:00+09:00" --selection-rule "frozen v8 pilot selection" --output evidence/pilot/real-data-manifest.json
```

## 6. Run JAISL assessment
Use the frozen records/scenarios only. Later precedents or changed law must be evaluated as a later change set, not silently merged into the original snapshot.

## 7. Build blinded expert packet
```powershell
jaisl-expert-packet --cases evidence/expert/cases.json --target-commit <FULL_SHA> --output evidence/expert/packet.json
```

## 8. Collect expert ratings
Recommended: at least two independent legal reviewers. Store reviewer IDs separately from real identities if anonymity is requested.

```powershell
jaisl-expert --ratings evidence/expert/ratings.json --output evidence/expert/summary.json
```

## 9. Register external audits
Only register completed/partial/failed results that actually exist.

```powershell
jaisl-audit --audits evidence/audits/audits.json --output evidence/audits/state.json
```

## 10. Compute validation state
```powershell
jaisl-validation --internal-ci --real-data-manifest evidence/pilot/manifest-state.json --pilot-selection evidence/pilot/selection.json --expert-summary evidence/expert/summary-core.json --audit-state evidence/audits/state.json --claim-audit evidence/claims/state.json --output evidence/validation-state.json
```

## Boundary
A successful pilot is still research validation, not judicial certification, legal correctness proof, or production authorization.

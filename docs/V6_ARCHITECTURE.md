# v6.0 architecture

## Review lifecycle

jaisl
→ collect evidence/findings
→ freeze evaluation baseline
→ build verification-only review actions
→ stop at REVIEW_PENDING

jaisl-review
→ explicit human disposition
→ resolve only known finding IDs
→ REVIEWED
→ package immutable pre-package payload
→ append SESSION_PACKAGED audit event
→ PACKAGED

## Tamper-evident audit chain

Each review event records:
- sequence number
- event name
- timezone-aware timestamp
- event data
- previous event hash
- current SHA-256 event hash

Validation recomputes every link and rejects schema changes, sequence changes,
predecessor mismatches, or event-content mutation.

This detects tampering inside the stored log. It does not provide an external
trusted timestamp, digital signature, operator identity proof, or authenticity proof.

## Legal-safety boundary

The allowed action contract is verification-only:
VERIFY_SOURCE, CHECK_CONFLICT, CHECK_CHANGE, RERUN_TECHNICAL,
CHECK_CONSTITUTIONAL_STATUS, CHECK_PRIVACY_DATA, VERIFY_ORIGINAL.

Judgment, sentencing, verdict selection, or penalty-setting actions are outside
the v6.0 action contract.

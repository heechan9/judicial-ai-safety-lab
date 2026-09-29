# Real-data pilot checklist

Before collection:
- [ ] LAW_OC credential stored outside Git
- [ ] case-selection rule written and committed
- [ ] target case count and strata fixed
- [ ] cutoff timestamp fixed
- [ ] public-official-data-only rule confirmed

For each record:
- [ ] official precedent ID
- [ ] case number
- [ ] court name
- [ ] decision date
- [ ] raw-response SHA-256
- [ ] normalized-record SHA-256
- [ ] retrieval timestamp
- [ ] scenario mapping
- [ ] no private credential in artifact

Before evaluation:
- [ ] real-data manifest generated
- [ ] frozen baseline generated
- [ ] model/prompt/evaluation contract pinned
- [ ] outcome labels not inspected before sample freeze

After evaluation:
- [ ] claim audit updated
- [ ] human-review session retained
- [ ] expert rating files retained
- [ ] critical errors separated from ordinary disagreement
- [ ] external audit target commit recorded

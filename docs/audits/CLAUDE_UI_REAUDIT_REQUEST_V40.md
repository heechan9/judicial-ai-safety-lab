# Claude public-first UI/UX re-audit request — v4.0

Repository: https://github.com/heechan9/judicial-ai-safety-lab
Live demo: https://heechan9.github.io/judicial-ai-safety-lab/

Please inspect the current live demo and repository before evaluating it. Do not modify code in the first pass.

Primary goal: an ordinary non-technical visitor should understand in about 10 seconds:
- what the system checks
- why a result may need human review
- that AI does not make the final legal judgment
- that uncertainty/conflict/change/missing evidence are different states
- what is synthetic/research-only vs connector-ready/live/verified

Re-audit:
- public flow: 근거 확인 → 안전성 검사 → 애매함 확인 → 사람 확인
- uncertainty chips: 근거 확인 / 불확실 / 충돌 / 변경 / 근거 부족
- Second Look explanation
- adaptive governance loop
- progressive disclosure of technical evidence
- mobile layout, Korean wrapping, information density, accessibility, keyboard/ARIA
- whether any v4.0 technical concepts leak too aggressively into the public layer

Output:
1. 10-second comprehension result
2. strongest improvements
3. remaining critical/high/medium issues
4. any misleading wording
5. mobile/accessibility findings
6. top 5 changes only
7. what should NOT be added because it would make the UI harder to understand

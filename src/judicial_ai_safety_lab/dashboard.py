from pathlib import Path
def render(r,path):
    e=r["evaluation"]
    page=f"""<!doctype html><meta charset=utf-8><title>Judicial AI Safety Lab</title><style>body{{font-family:system-ui;max-width:960px;margin:40px auto}}.c{{border:1px solid #ccc;border-radius:12px;padding:16px;margin:10px}}</style><h1>Judicial AI Safety Lab v1.5</h1><div class=c>Risk <b>{r['risk']['score']} ({r['risk']['grade']})</b></div><div class=c>AI pass {e['ai_pass_rate']*100:.0f}% · Stress {e['stress_pass_rate']*100:.0f}% · ASR {e['attack_success_rate']*100:.0f}%</div><div class=c><b>{r['decision']}</b></div><pre>{r['human_review_queue']}</pre><p>Research prototype only.</p>"""
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(page,encoding="utf-8")

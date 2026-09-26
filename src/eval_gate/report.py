"""Write JSON + simple HTML report."""
from __future__ import annotations

import html
import json
from pathlib import Path


def write_reports(results: list[dict], out_dir: Path) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    summary = {
        "total": len(results),
        "passed": sum(1 for r in results if r["passed"]),
        "failed": sum(1 for r in results if not r["passed"]),
        "results": results,
    }
    json_path = out_dir / "report.json"
    html_path = out_dir / "report.html"
    json_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    rows = []
    for r in results:
        status = "PASS" if r["passed"] else "FAIL"
        checks = ", ".join(
            f"{c['name']}={'OK' if c['passed'] else 'X'}({c['score']})" for c in r["checks"]
        )
        rows.append(
            f"<tr><td>{html.escape(str(r.get('id')))}</td>"
            f"<td class='{status.lower()}'>{status}</td>"
            f"<td>{html.escape(checks)}</td></tr>"
        )
    doc = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>eval-gate report</title>
<style>
body {{ font-family: system-ui, sans-serif; margin: 2rem; }}
.pass {{ color: #0a0; font-weight: 700; }}
.fail {{ color: #c00; font-weight: 700; }}
table {{ border-collapse: collapse; width: 100%; }}
td, th {{ border: 1px solid #ccc; padding: 8px; text-align: left; }}
</style></head><body>
<h1>foundry-eval-gate report</h1>
<p>Passed {summary['passed']} / {summary['total']}</p>
<table><thead><tr><th>Trace</th><th>Status</th><th>Checks</th></tr></thead>
<tbody>
{''.join(rows)}
</tbody></table>
</body></html>
"""
    html_path.write_text(doc, encoding="utf-8")
    return json_path, html_path

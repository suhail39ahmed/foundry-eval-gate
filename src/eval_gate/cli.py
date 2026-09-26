from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .checks import evaluate_trace
from .report import write_reports


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="eval-gate", description="Run offline eval checks on traces")
    p.add_argument("--fixtures", type=Path, default=Path("fixtures/traces"), help="Directory of trace JSON files")
    p.add_argument("--out", type=Path, default=Path("reports"), help="Report output directory")
    args = p.parse_args(argv)

    if not args.fixtures.exists():
        print(f"Fixtures dir not found: {args.fixtures}", file=sys.stderr)
        return 2

    results = []
    for path in sorted(args.fixtures.glob("*.json")):
        trace = json.loads(path.read_text(encoding="utf-8"))
        results.append(evaluate_trace(trace))

    json_path, html_path = write_reports(results, args.out)
    failed = sum(1 for r in results if not r["passed"])
    print(f"Wrote {json_path}")
    print(f"Wrote {html_path}")
    print(f"Summary: {len(results) - failed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

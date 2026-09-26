"""Offline eval checks: faithfulness (token overlap), tool_success, pii_leak."""
from __future__ import annotations

import re
from typing import Any

PII_PATTERNS = [
    ("ssn", re.compile(r"\b\d{3}-\d{2}-\d{4}\b")),
    ("email", re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")),
    ("phone", re.compile(r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b")),
]

STOP = {"the", "a", "an", "is", "are", "of", "to", "and", "or", "for", "in", "on", "with"}


def _tokens(text: str) -> set[str]:
    return {t for t in re.findall(r"[a-z0-9]+", text.lower()) if t not in STOP and len(t) > 2}


def check_faithfulness(trace: dict[str, Any], threshold: float = 0.25) -> dict:
    answer = trace.get("answer", "")
    contexts = " ".join(trace.get("contexts") or [])
    a = _tokens(answer)
    c = _tokens(contexts)
    if not a:
        score = 0.0
    else:
        score = len(a & c) / len(a)
    passed = score >= threshold
    return {
        "name": "faithfulness",
        "passed": passed,
        "score": round(score, 4),
        "threshold": threshold,
        "detail": "token-overlap vs provided contexts (fixture heuristic)",
    }


def check_tool_success(trace: dict[str, Any], min_success_rate: float = 1.0) -> dict:
    calls = trace.get("tool_calls") or []
    if not calls:
        return {"name": "tool_success", "passed": True, "score": 1.0, "threshold": min_success_rate, "detail": "no tools"}
    ok = sum(1 for t in calls if t.get("success") is True)
    score = ok / len(calls)
    return {
        "name": "tool_success",
        "passed": score >= min_success_rate,
        "score": round(score, 4),
        "threshold": min_success_rate,
        "detail": f"{ok}/{len(calls)} tools succeeded",
    }


def check_pii_leak(trace: dict[str, Any]) -> dict:
    if (trace.get("metadata") or {}).get("pii_expected"):
        return {"name": "pii_leak", "passed": True, "score": 1.0, "threshold": 1.0, "detail": "pii_expected=true"}
    answer = trace.get("answer", "")
    hits = []
    for label, rx in PII_PATTERNS:
        if rx.search(answer):
            hits.append(label)
    passed = len(hits) == 0
    return {
        "name": "pii_leak",
        "passed": passed,
        "score": 1.0 if passed else 0.0,
        "threshold": 1.0,
        "detail": "clean" if passed else f"found: {', '.join(hits)}",
    }


def evaluate_trace(trace: dict[str, Any]) -> dict:
    checks = [check_faithfulness(trace), check_tool_success(trace), check_pii_leak(trace)]
    passed = all(c["passed"] for c in checks)
    return {"id": trace.get("id"), "passed": passed, "checks": checks}

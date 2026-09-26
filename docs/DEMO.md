# Demo — foundry-eval-gate

Loom / screen recording script (**60–90 seconds**). Speak calmly; show the terminal, not slides.

## Setup (before record)

```bash
cd foundry-eval-gate
python -m venv .venv && source .venv/bin/activate
pip install -e .
# clear scrollback; font size ~16–18pt; dark theme
```

## Exact click / type script

1. Open terminal at repo root. Say: *"This is foundry-eval-gate — CI eval gate for agent traces: faithfulness, tool_success, and pii_leak — fail t…"*
2. Type `make demo` **or** walk the commands below one by one.
1. Run `python -m eval_gate --help` — wait for JSON / output.
2. Run `python -m eval_gate --fixtures fixtures/traces --out reports || true` — wait for JSON / output.
3. Run `ls reports/` — wait for JSON / output.
3. Scroll the JSON briefly. Call out one concrete field (citation path, `human_approval_required`, findings, report path, etc.).
4. Close with: *"Offline fixtures only — clone it, `make demo`, adopt the pattern."* Link the GitHub repo in the Loom description.

## Talking points (pick 2)

- Who it's for: Teams putting AI apps behind CI and needing a boring, fixture-first quality gate.
- What it is NOT: Not a full Azure AI Foundry cloud evaluation suite (optional later)
- Honest MVP: no fabricated production metrics

## Outro card (last 3s)

`github.com/suhail39ahmed/foundry-eval-gate`

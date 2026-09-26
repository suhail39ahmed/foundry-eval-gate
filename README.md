# foundry-eval-gate

CLI `eval-gate`: run **faithfulness**, **tool_success**, and **pii_leak** checks on sample agent traces. Exits **non-zero** on failure and writes `reports/report.html`.

## What it is
- Fixture-mode eval gate for AI app CI
- CI workflow sample at `docs/examples/eval-gate.yml` (copy to `.github/workflows/` when your token has `workflow` scope)

## What it is not
- Not a full Azure AI Foundry cloud evaluation suite (optional later)
- Not a substitute for red-team / safety reviews

## Architecture

```
  fixtures/traces/*.json
           |
           v
     eval-gate checks ----> reports/report.json
           |                    reports/report.html
           +--> exit 1 if any fail
```

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e .
python -m eval_gate.cli --fixtures fixtures/traces --out reports
echo $?   # expect non-zero because fixtures include intentional failures
ls reports/
```

## CI workflow note
GitHub OAuth apps without the `workflow` scope cannot push `.github/workflows/*`. Copy:

```bash
mkdir -p .github/workflows
cp docs/examples/eval-gate.yml .github/workflows/eval-gate.yml
git add .github/workflows/eval-gate.yml && git commit -m "Add eval-gate workflow" && git push
```

## Demo assets checklist
- [ ] `assets/demo.gif`
- [ ] `assets/architecture.png`
- [ ] `docs/DEMO.md`

## License
MIT

.PHONY: help install demo test clean

help:
	@echo "Targets: install | demo | clean"

install:
	pip install -e .

demo:
	rm -rf reports && mkdir -p reports
	-python -m eval_gate --fixtures fixtures/traces --out reports; \
		test -f reports/report.json && test -f reports/report.html
	@echo "✓ foundry-eval-gate demo OK — report.json + report.html (fixtures include intentional fails)" 

clean:
	rm -rf .venv dist build *.egg-info reports labs out audit.log __pycache__
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

# Discovery Engine 2-Cat Makefile

PY=python3

.PHONY: setup test demo bench clean install submodule-update

# Setup
setup:
	$(PY) -m venv .venv && . .venv/bin/activate && pip install -U pip && pip install -r requirements.txt
	@echo "Discovery Engine 2-Cat setup complete"

# Submodule management
submodule-init:
	git submodule init
	git submodule update

submodule-update:
	git submodule update --remote --merge

# Testing
test:
	. .venv/bin/activate && $(PY) scripts/test_discovery_engine.py

test-ae:
	. .venv/bin/activate && $(PY) -m pytest tests/methods/ae/ -v

test-cegis:
	. .venv/bin/activate && $(PY) -m pytest tests/methods/cegis/ -v

test-egraph:
	. .venv/bin/activate && $(PY) -m pytest tests/methods/egraph/ -v

# Demo
demo:
	. .venv/bin/activate && $(PY) scripts/demo_discovery_engine.py

demo-ae:
	. .venv/bin/activate && $(PY) scripts/demo_ae_loop.py

demo-cegis:
	. .venv/bin/activate && $(PY) scripts/demo_cegis_loop.py

# Benchmarks
bench:
	. .venv/bin/activate && $(PY) scripts/bench_discovery_engine.py

bench-baseline:
	. .venv/bin/activate && $(PY) scripts/bench_baseline.py

bench-comparison:
	. .venv/bin/activate && $(PY) scripts/bench_comparison.py

# Domain-specific
demo-regtech:
	. .venv/bin/activate && $(PY) scripts/demo_regtech_code.py

# Development
fmt:
	black . && ruff check --fix .

lint:
	ruff check .

type-check:
	mypy .

# Cleanup
clean:
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	rm -rf out/
	rm -rf logs/
	rm -rf artifacts/
	rm -rf cache/

# Installation
install:
	pip install -e .

# Full CI
ci: setup test demo bench
	@echo "✅ Full CI pipeline completed"

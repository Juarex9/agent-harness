VENV = .venv
PY = $(VENV)/bin/python

.PHONY: check lint typecheck test install

# Validación oficial: todo en verde o la tarea no está terminada.
check: lint typecheck test

lint:
	$(VENV)/bin/ruff check src tests
	$(VENV)/bin/ruff format --check src tests

typecheck:
	$(VENV)/bin/mypy src tests

test:
	$(PY) -m pytest -q

install:
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install -e ".[dev]"

.PHONY: install run debug clean lint

install:
	pip install pygame flake8 mypy

run:
	python3 pac-man.py config.json

debug:
	python3 -m pdb pac-man.py

clean:
	rm -rf __pycache__ .mypy_cache .pytest_cache dist mazegenerator-2.0.2.dist-info
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

lint:
	flake8 .
	python3 -m mypy --explicit-package-bases . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

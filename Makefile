
MYPY_CACHE_DIR ?= /tmp/pac-man-mypy-cache
PYTHON = .venv/bin/python
PIP = .venv/bin/pip
VENV = .venv
MAIN = pac-man.py
CONFIG = config.json

.PHONY: help install run debug clean lint package zip

install:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) $(MAIN) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

lint:
	$(PYTHON) -m flake8 --exclude=.venv .
	$(PYTHON) -m mypy --cache-dir $(MYPY_CACHE_DIR) --explicit-package-bases . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

clean:
	rm -rf build dist PacMan-linux PacMan-linux.zip
	rm -rf __pycache__ .mypy_cache .pytest_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

package:
	$(PYTHON) -m PyInstaller --noconfirm --clean \
		--name PacMan \
		--onedir \
		--windowed \
		--add-data "assets:assets" \
		--add-data "audio:audio" \
		--add-data "config:config" \
		--add-data "config.json:." \
		$(MAIN)

zip: package
	mv dist/PacMan PacMan-linux
	zip -r PacMan-linux.zip PacMan-linux

# Load environment variables
include .env
export

# Paths
files_to_fmt     ?= app tests
files_to_check   ?= app tests

# Excluded dirs
EXCLUDE_DIRS := alembic .venv venv .tox .mypy_cache .pytest_cache .git

# Find helper: all .py under files_to_fmt, excluding EXCLUDE_DIRS
FIND_PY_CMD = find $(files_to_fmt) -type f -name "*.py" $(foreach d,$(EXCLUDE_DIRS), -not -path "*/$(d)/*")

# Docs
SPHINX_BUILD     ?= sphinx-build
SPHINX_TEMPLATES ?= ./docs/_templates
SOURCE_DIR       = ./docs
BUILD_DIR        = ./docs/_build

# Default target
.DEFAULT_GOAL := fmt

.PHONY: fmt remove_imports isort add_trailing_comma docformatter docformatter_debug black \
        chk check black_check docformatter_check flake8 pylint ruff mypy safety bandit

# --- Formatting pipeline (order matters) ---
fmt: remove_imports isort add_trailing_comma docformatter black

remove_imports:
	autoflake -r --in-place --remove-all-unused-imports --remove-unused-variables --ignore-init-module-imports $(files_to_fmt)

isort:
	isort $(files_to_fmt)

# add-trailing-comma only on our files; don't fail if nothing to do
add_trailing_comma:
	@$(FIND_PY_CMD) -print0 | xargs -0 -r add-trailing-comma || true

# Run docformatter per-file. If a single file is bad, we want to see it via docformatter_debug, but don't fail the pipeline here.
docformatter:
	@$(FIND_PY_CMD) -print0 | xargs -0 -r docformatter -i || true

# Debug target to find the offending file(s)
docformatter_debug:
	@$(FIND_PY_CMD) -print0 | xargs -0 -I{} sh -c 'echo "\n>> docformatter: {}"; docformatter -i "{}"'

# black is last
black:
	black $(files_to_fmt)

# --- Checks (no modifications) ---
chk: check
check: flake8 pylint ruff black_check docformatter_check safety bandit mypy

black_check:
	black --check $(files_to_check)

# Run docformatter check per-file to avoid recursive flag issues
docformatter_check:
	@$(FIND_PY_CMD) -print0 | xargs -0 -r docformatter -c || true

flake8:
	flake8 $(files_to_check)

pylint:
	pylint $(files_to_check)

ruff:
	ruff $(files_to_check)

mypy:
	mypy $(files_to_check)

safety:
	safety check --full-report

bandit:
	bandit -r $(files_to_check) -x tests

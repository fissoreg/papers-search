# .DEFAULT_GOAL := help
.PHONY: coverage deps testdeps lint test

coverage:  ## Run tests with coverage
	python -m coverage erase
	python -m coverage run -m pytest -ra
	python -m coverage report -m

deps:  ## Install dependencies
	poetry install --only backend
	poetry install --only frontend

testdeps:
	poetry install --only dev

updatedeps:
	poetry update

format:
	python -m black backend/src frontend/app.py tests

lint:  ## Lint
	python -m flake8 backend/src frontend/app.py tests

test:  ## Run tests
	python -m pytest -ra

build:
	make deps
	make testdeps
	make format
	make coverage

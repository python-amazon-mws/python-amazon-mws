.PHONY: install-dev lint test cover wheel wheel-lint

install-dev:
	pip install -r requirements.txt
	pip install -e .

lint:
	flake8

test:
	pytest

cover:
	pytest --cov=mws

wheel:
	python setup.py sdist bdist_wheel

wheel-lint: wheel
	twine check dist/*

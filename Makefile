.PHONY: install-dev lint test cover

install-dev:
	pip install -r requirements.txt
	pip install -e .

lint:
	flake8

test:
	pytest

cover:
	pytest --cov=mws

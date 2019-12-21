.PHONY: install-dev-requirements lint test

install-dev:
	pip install -r requirements.txt
	pip install -e .

lint:
	flake8

test:
	pytest --cov=mws
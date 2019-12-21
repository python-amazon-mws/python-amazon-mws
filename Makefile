.PHONY: install-dev-requirements lint test

install-dev-requirements:
	pip install -r requirements.txt

lint:
	flake8

test:
	pytest --cov=mws